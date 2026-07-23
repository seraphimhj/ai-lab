# 投机解码：用小模型猜，大模型一次并行验

命中薄弱点：retrieval 以外的推理系统；递进 07-14 的 KV cache「显存账」，今天改算自回归生成的「延迟账」。

来源：Leviathan et al., *Fast Inference from Transformers via Speculative Decoding*（arXiv:2211.17192）；Cai et al., *Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads*（arXiv:2401.10774）。

## 全局地图

### 一句话摘要

投机解码没有让大模型少判断，而是让便宜的 draft 模型先提出多个候选，再让大模型在一次前向中并行核验；它用更多总计算换更少串行轮次，而收益上限由「候选被接受的概率」决定。

### 结构地图

```text
普通解码
  大模型 -> token 1 -> 大模型 -> token 2 -> 大模型 -> token 3
             wait                    wait

投机解码
  小模型串行猜 k 个候选
          |
          v
  大模型一次并行验证 k 个位置
          |
          +-- 接受最长正确前缀
          +-- 在首个拒绝处纠正
          +-- 进入下一轮

延迟收益
  = 每轮平均产出的 token 数
    / (一次验证成本 + draft 成本 + 调度成本)
```

### 段落分类（Agent 判断）

- [骨] 生成为什么慢：真正欠下的是串行依赖债。
- [骨] 为什么一次验证多个 token，不等于大模型偷偷跳过计算。
- [肌] 精确采样如何保证输出分布不变。
- [骨] 接受率如何决定加速比上限。
- [肌] Medusa 如何去掉独立 draft 模型。
- [骨] 什么时候会更慢，以及系统设计该盯什么指标。

## 逐段伴读

### 1. [骨] 生成慢，不只是因为模型大

论文的起点是：

> “Decoding K tokens takes K serial runs of the model.”
>
> 生成 K 个 token，需要把大模型串行运行 K 次。

训练或 prompt prefill 时，一整段 token 已经已知，GPU 可以同时处理许多位置。生成时却不同：第 t+1 个 token 的条件里包含第 t 个 token，所以 t 没落地，t+1 就不能开始。KV cache 省掉了对旧 token 的重复计算，却没有消灭这个依赖链。

这正是 07-14「显存账」背面的「延迟账」：

```text
KV cache 解决：过去的 K/V 不要重算
它没有解决：未来 token 必须一个接一个确认
```

单 token decode 通常还是 memory-bound：每生成一个 token，都要把大模型的大量权重搬过计算单元，但一次只服务很少的 token，GPU 算力吃不满。真正昂贵的不是某个 token 的乘加本身，而是为每个 token 单独发动一次整台大机器。

结构标注：核心问题定义；把「模型计算量大」改写为「串行轮次多、每轮硬件利用率低」。

### 2. [骨] 投机解码把串行债改写成批量验证

设目标大模型为 p，便宜的 draft 模型为 q。每轮做三件事：

1. q 自回归猜出 k 个 token：x1, x2, ..., xk。
2. 把这 k 个候选一起送给 p；由于候选序列已经给定，p 可像短 prefill 一样并行算出每个位置的目标分布。
3. 从左到右核验，接受最长前缀；遇到第一个拒绝便纠正，然后开始下一轮。

关键区别是「生成」和「评分」：

- 生成第 i 个 token 时，输入中的第 i 个 token 还不存在，必须等待。
- 验证时，draft 已经把 k 个候选都写在纸上，大模型可以同时给这 k 个位置打分。

因此，“验证比生成便宜”不是说验证每个 token 的 FLOPs 神奇地更少。更准确地说：k 个位置合在一次大模型调用里，更容易并行，能摊薄权重读取、kernel launch 和同步成本。它甚至可能增加总 FLOPs，却降低 wall-clock latency。

这里容易混淆两种效率：

```text
算力效率：完成任务用了多少 FLOPs / 能量
延迟效率：用户等了多少毫秒

投机解码通常牺牲前者，争取后者。
```

结构标注：核心机制；回答“为什么验证比逐个生成便宜”。

### 3. [肌] “验”不是只看 argmax：精确采样保持分布不变

如果温度为 0，只做 greedy decoding，核验很直观：draft 候选等于大模型在该位置的 argmax 就接受，否则改用大模型的 token。

但随机采样时，不能把“不是大模型第一名”的候选一律拒绝。假设 draft 对候选 x 给概率 q(x)，目标模型给概率 p(x)，精确投机采样以

```text
accept(x) = min(1, p(x) / q(x))
```

的概率接受它。

直觉是：

- q 没有比 p 更偏爱 x，即 q(x) <= p(x)，就总能接受；
- q 过度推荐 x，即 q(x) > p(x)，只接受其中 p(x)/q(x) 的比例；
- 被拒绝后，不能随手从 p 重采，而要从归一化后的 max(0, p-q) 残差分布采样。

这样一增一减，最终产出的 token 仍严格服从 p。原论文强调：

> “without any changes to the outputs”
>
> 不改变输出分布。

所以，经典 speculative decoding 是无损的推理调度算法，不是量化那样的近似模型压缩。若实现采用“足够像就接受”的启发式规则，则可能更快，但已经放弃严格分布等价；要把这两类方案分开评测。

结构标注：机制证据；说明“加速”如何不偷换模型质量。

以上 1 段在支持第二节的核心机制：接受规则不仅查对错，还负责守住目标分布。

### 4. [骨] 接受率 alpha 才是加速比的总闸门

令 alpha 表示每个 draft token 被接受的平均概率，并先做一个简化假设：各位置接受事件近似独立；每轮猜 k 个，而且全部接受后目标模型还能顺手产出一个 bonus token。那么每轮平均推进的 token 数是：

```text
E[tokens per round]
  = 1 + alpha + alpha^2 + ... + alpha^k
  = (1 - alpha^(k+1)) / (1 - alpha)
```

为什么是这串等比数列？每轮至少会得到 1 个有效 token；要得到第 2 个，首个候选须被接受，概率为 alpha；要得到第 3 个，前两个都须接受，概率为 alpha^2；依此类推。

用 k=4、每个 draft 步骤成本约为一次大模型解码的 0.1 倍，并暂时把一次批量验证近似为一次大模型调用：

| 平均接受率 alpha | 每轮平均推进 token | 理想化加速比 |
|---:|---:|---:|
| 0.5 | 1.9375 | 1.38x |
| 0.8 | 3.3616 | 2.40x |
| 0.9 | 4.0951 | 2.93x |

这里的“理想化”很重要。真实分母还包括批量验证随 k 增长的成本、draft 的 KV cache、候选搬运、调度和 kernel 开销。因此不能看到“每轮验证 5 个位置”就声称 5 倍加速。

也不能无限增大 k。候选越往后，前缀全被接受的概率按 alpha 的幂衰减；而草稿与验证成本仍继续增加。alpha=0.5 时，第 4 个候选真正派上用场需要前三个都过关，机会只剩 0.5^3；长草稿大多会在前面被截断。

结构标注：核心定量框架；把“能不能加速”压缩为接受率、草稿长度和成本比三个变量。

### 5. [肌] Medusa：不再养一个小模型，直接让大模型长出几颗“预判头”

独立 draft 模型有现实成本：需要额外权重、额外 KV cache，还要调度两个模型；更麻烦的是 q 与 p 越不一致，alpha 越低。

Medusa 的改法是在原模型最后的 hidden state 上挂多个轻量 decoding heads：第 1 个头猜下一个 token，第 2 个头猜下下个，依此类推。多个头给出多条候选，再用 tree attention 把共享前缀的候选树一次送入主干模型验证。

```text
同一 hidden state
  +-- head 1 -> 猜位置 t+1
  +-- head 2 -> 猜位置 t+2
  +-- head 3 -> 猜位置 t+3
                |
                v
         candidate tree
                |
                v
       backbone parallel verify
```

它省掉了独立 draft 模型，但付出另一种代价：更远位置的预测没有真正看到前一个采样 token，条件信息更弱，所以通常要保留多个候选分支。Medusa 论文也区分 rejection sampling 与 typical acceptance：前者可保持原分布，后者用“足够合理”的阈值换取更长接受长度与更高速度，但不再承诺严格等价。

结构标注：支持性变体；展示同一“先猜后验”骨架如何重新安排 draft 成本。

以上 1 段在支持第四节：系统优化不只提高 alpha，也可以降低获得候选的成本。

### 6. [骨] 什么时候投机解码会更慢

它不是“装上就快”的免费午餐。以下场景会吞掉收益：

1. draft 与目标模型不一致。开放式高温采样、跨语言切换、代码中的稀有标识符，都可能拉低 alpha。
2. draft 太贵。小模型虽小，却要串行跑 k 步；若成本比不够低，省下的大模型轮次会被草稿吃回去。
3. k 选得太大。远端候选的边际存活率很低，却仍消耗计算与显存。
4. 高并发服务已把 GPU 填满。投机验证增加每请求的计算量，可能改善单请求 latency，却损害总吞吐，排队后端到端延迟反而上升。
5. 验证实现不够好。若 attention mask、候选树和 KV cache 管理引入大量搬运，理论并行性不会自动变成真实加速。

所以线上不应只报 tokens/s。至少要分开看：

```text
acceptance rate by position
accepted tokens per verification
cost(draft) / cost(target decode)
verification latency as k changes
inter-token latency (ITL)
throughput under target concurrency
output-distribution or quality regression
```

这把 07-14 的 PagedAttention 与今天连起来了：PagedAttention 提高“同一时刻能容纳多少请求”的容量利用率；投机解码减少“一个请求需要多少次串行大模型调用”。一个主要管空间，一个主要管时间，但二者会争夺同一批 GPU 计算与显存资源，必须在真实并发分布下一起评测。

结构标注：边界条件与端到端闭环；把论文机制接回 serving 指标和线上流量。

## 注疏：一个容易反直觉的侧光

这里的论证结构和 CPU speculative execution 是同一个形状：先沿高概率路径做未来工作，猜对就省等待，猜错就丢弃并回滚。但两者有一个关键差异：CPU 分支预测通常猜一条确定路径；随机 LLM 解码必须通过接受-拒绝与残差采样，守住整个概率分布，而不只是守住“最后结果看起来合理”。

最强反驳是：既然总 FLOPs 可能增加，这只是把成本藏起来，不能叫效率提升。

更准确的回应不是否认，而是拆开目标函数：如果目标是单请求低延迟、GPU 在单 token decode 时又严重 memory-bound，那么用闲置算力换更少的权重读取和同步轮次是合理交易；如果目标是满载集群的每瓦吞吐，反驳可能成立。投机解码没有统一的“更高效”，只有相对于工作负载目标的 Pareto 交换。

## 全文复盘

### 理解轨迹

```text
KV cache：旧状态不重算
    |
    v
仍有串行依赖：每个新 token 要等前一个
    |
    v
cheap draft 提前写出未来候选
    |
    v
large target 批量并行验证
    |
    +-- exact acceptance：守住目标分布
    |
    +-- acceptance rate：决定每轮能前进多远
    |
    +-- cost ratio / concurrency：决定理论收益能否落地
```

### 读后一句话

请保留一句自己的判断：投机解码究竟是在“减少计算”，还是在“购买并行性”？如果你只能选一个线上指标证明它有价值，你会选 ITL、吞吐、每 token 成本，还是质量不回退？

### 终局问题

当系统用 typical acceptance 接受“足够合理”而非严格同分布的候选时，它已经从无损调度跨进了近似推理；那么这部分质量债，应该由解码器的局部概率差异来度量，还是必须回到用户任务的端到端成功率来度量？

### 术语表

| English | 中文 | 本文含义 | 位置 |
|---|---|---|---|
| autoregressive decoding | 自回归解码 | 下一个 token 依赖此前已生成前缀 | 第 1 节 |
| draft model | 草稿模型 | 低成本提出未来候选的模型 q | 第 2 节 |
| target model | 目标模型 | 最终定义输出分布的大模型 p | 第 2 节 |
| verification | 验证 | 目标模型并行评估多个候选位置 | 第 2 节 |
| rejection sampling | 接受-拒绝采样 | 通过概率校正保持目标分布不变 | 第 3 节 |
| acceptance rate | 接受率 | draft token 通过目标模型核验的平均概率 | 第 4 节 |
| bonus token | 奖励 token | 草稿全通过后，目标模型顺手产生的额外 token | 第 4 节 |
| tree attention | 树形注意力 | 共享候选前缀、并行验证多分支的注意力结构 | 第 5 节 |
| memory-bound | 内存带宽受限 | 耗时主要卡在权重/数据搬运而非乘加峰值 | 第 1、2 节 |

### 下一步线索

下一步只追一条：重读 Leviathan et al.（arXiv:2211.17192）的 Algorithm 1 与 Theorem 3.8，把今天的 accept(x)=min(1,p/q) 和期望 token 数推导逐行对照；随后看 Medusa（arXiv:2401.10774）第 2 节，比较 rejection sampling 与 typical acceptance 究竟在哪一步放弃“输出分布不变”。
