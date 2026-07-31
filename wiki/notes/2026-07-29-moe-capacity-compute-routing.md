# MoE：把参数量和每-token 计算量解耦，一次路由要还的两笔账

> 本次命中：**retrieval 以外的空缺——预训练 / 推理系统**，并把 07-16 的 Chinchilla「参数与数据怎么分钱」推进到一个新问题：当总参数量不再等于每-token 激活参数量，旧账本该怎样改写？

材料：Switch Transformer（Fedus et al., 2021）与 Mixtral of Experts（Jiang et al., 2024）。

## 全局地图

### 一句话摘要

MoE 不是用更少的模型完成同样的计算，而是让模型拥有许多组参数、每个 token 只调用其中少数几组；它用**稀疏激活**买到更大的知识容量，却必须偿还训练时的负载均衡账，以及 serving 时的显存与跨设备通信账。

### 结构地图

```text
Dense Transformer
  每个 token -> 同一组 FFN 参数
  参数增大   -> 每-token FLOPs 同步增大

Sparse MoE Transformer
  每个 token -> router -> top-k experts -> 加权合并
                      |
                      +-> 收益：总容量与激活计算部分解耦
                      |
                      +-> 账 1：流量不均 / 专家坍缩 / 容量溢出
                      |
                      +-> 账 2：全体权重驻留 / all-to-all 通信

最终问题
  scaling law 里的 N，究竟应算总参数、激活参数，还是二者都算？
```

### 段落分类（Agent 判断，可覆盖）

- `[骨]` 1. MoE 真正解耦的是什么
- `[肌]` 2. 一次 token 路由如何发生
- `[骨]` 3. 第一笔账：负载均衡
- `[骨]` 4. 第二笔账：显存与通信
- `[骨]` 5. MoE 如何改写 Chinchilla 的账本
- `[肌]` 6. 一个系统设计判断题
- `[筋]` 7. 收束：不是免费午餐，而是换账本

---

## 1. `[骨]` MoE 真正解耦的是什么

先把 Transformer 的一层粗略拆成两块：attention 负责 token 之间交换信息，FFN 负责对每个 token 做非线性变换。MoE 通常不是把整层复制很多份，而是把其中的 **FFN 子层**换成多个 expert（专家）。

Dense 模型中，每个 token 都经过同一个 FFN：

```text
h -> FFN(h) -> output
```

MoE 中，每个 token 先由 router 打分，再只进入 top-k 个专家：

```text
                   +-> Expert 1 --+
h -> Router -> top-k               +-> weighted sum -> output
                   +-> Expert 6 --+
```

可以把核心关系写成：

```text
y = sum over i in TopK(x) of g_i(x) * E_i(x)
```

- `E_i`：第 i 个专家，本质上通常是一套 FFN 参数。
- `g_i(x)`：router 给当前 token 分配给专家 i 的权重。
- `TopK(x)`：只保留分数最高的 k 个专家。

**直觉层**：总参数量决定仓库里放了多少货架；top-k 决定每个 token 实际走过几排货架。

**关键纠偏**：MoE 解耦的是「专家总容量」与「专家部分的每-token 计算」，不是把整个模型的成本都解耦。attention、embedding、输出头仍是共享的 dense 计算；router、调度和通信还会产生额外成本。

> 英文锚点："sparsely activated" — 稀疏激活。重点不是参数本身稀疏，而是一次前向只激活参数集合的一小部分。

**结构标注**：核心论点；先限定“参数量 ≠ 每-token 计算量”的成立范围，防止把 MoE 理解成无条件降本。

### 停顿问题

如果一个模型有 64 个等大的专家、每个 token 只激活 2 个，那么**专家容量 / 专家激活计算**之比是 64 / 2 = 32。这个 32 倍代表的是容量杠杆，不是端到端必然加速 32 倍——你能指出还有哪些部分没有一起缩小吗？

---

## 2. `[肌]` Router 到底在做什么

对 token 的隐状态 `h`，router 通常先做一个很小的线性投影，再 softmax：

```text
router_logits = W_r * h
p = softmax(router_logits)
```

`p_i` 可以读成「这个 token 交给专家 i 的相对偏好」。随后选择 top-1 或 top-2：

- **Switch Transformer**把路由简化到 top-1：每个 token 只去一个专家，目标是降低路由与通信复杂度。
- **Mixtral 8x7B**采用 top-2：每个 token 选择两个专家并加权合并，以多一些计算换取更丰富的组合。

这里有一个容易误解的点：专家通常不是人工指定成“数学专家”“代码专家”。router 与 experts 联合训练，分工从优化中涌现；某些专家可能表现出领域或句法偏好，但不保证有整洁、稳定、可解释的标签。

一个 batch 中的真实执行不是逐 token 调 Python 函数，而是：

```text
1. router 给所有 token 分桶
2. 按目标专家重排 token
3. 各设备上的专家批量计算
4. 把结果送回 token 原位置
5. top-k 结果加权合并
```

第 2 和第 4 步正是通信账的来源。

**结构标注**：机制展开；为后面两笔账建立共同因果起点——router 不只做数学选择，还改变了 token 在硬件上的流向。

> 以上机制段在支持第 1 节的论证：稀疏激活在公式里是 top-k，在系统里则是一次真实的数据重排。

---

## 3. `[骨]` 第一笔账：训练侧的负载均衡

### 3.1 为什么专家会坍缩

假设训练早期，专家 A 偶然比其他专家好一点。router 会把更多 token 送给 A；A 获得更多梯度、学得更快；于是 router 更偏爱 A。这是一个正反馈：

```text
略好 -> 更多 token -> 更多训练 -> 更好 -> 更多 token
```

结果可能是少数热门专家挤爆，大量专家闲置。总参数很多，实际容量却退化成少数几个专家，这就是 **expert collapse（专家坍缩）**或严重的负载不均。

### 3.2 Auxiliary load-balancing loss 在惩罚什么

Switch Transformer 使用一类辅助损失，同时观察两件事：

```text
f_i = 实际被分到专家 i 的 token 比例
P_i = router 给专家 i 的平均概率
L_aux = alpha * N * sum_i(f_i * P_i)
```

这里 `N` 是专家数，`alpha` 是辅助损失权重。直觉上，当实际流量和概率质量都集中到同一批专家时，乘积和会变大；优化它会推动流量更均匀。

但这不是“强迫每个专家学一样的东西”。它只要求**工作量别极端失衡**，并不直接规定专家内部学什么。过强的均衡约束还可能伤害自然专门化：如果数据本来就不均匀，严格平均分流未必最优。

### 3.3 Capacity factor：高速公路每个出口能过多少车

工程实现通常给每个专家设置容量上限。以 top-1 的简化情形为例：

```text
expert_capacity ~= capacity_factor * tokens_in_batch / num_experts
```

若 1000 个 token、8 个专家、capacity factor = 1.25，则每个专家容量向上取整约为 157，总预留槽位为 1256。

- capacity factor 大：溢出少，但预留空槽和计算浪费更多。
- capacity factor 小：利用率紧凑，但热门专家可能溢出；溢出 token 可能被丢弃、跳过该层或改派，训练质量受损。

所以负载均衡不是审美问题，而是同时影响：

```text
有效模型容量 <-> token 是否被正常处理 <-> 硬件利用率
```

**结构标注**：第一笔核心代价；说明“稀疏”只有在流量可调度时才转化为有效容量。

### 压力测试

最强反驳是：“既然均匀分配这么重要，何不直接轮询，把 token 平均塞给所有专家？”

答案是：那会得到均衡，却失去**内容条件化计算**。MoE 的价值不只是少算，而是让不同 token 选择不同参数；轮询只解决硬件排队，不保留语义路由。真正困难的是同时满足两个目标：

```text
让 router 有选择性 + 不让选择性演化成拥堵
```

---

## 4. `[骨]` 第二笔账：serving 侧的显存与通信

### 4.1 不激活，不等于不用驻留

每个 token 只计算 top-k 个专家，并不意味着其余专家可以凭空消失。低延迟 serving 通常需要所有可能被 router 选中的专家权重已经在 GPU 或可快速访问的设备上。

因此会出现看似矛盾的组合：

```text
每-token FLOPs 较低
总权重显存仍很高
```

Mixtral 报告的典型数字能帮助建立尺度感：模型总参数约 46.7B，但每个 token 激活约 12.9B 参数。它不是“12.9B 模型只占 12.9B 的权重内存”，而是“46.7B 的容量，每个 token 走其中一部分路径”。量化能降低驻留字节数，但不会消除全部专家都可能被调用这一事实。

### 4.2 Expert parallelism 为什么触发 all-to-all

当全部专家放不进一张卡时，常见做法是把不同专家放到不同设备。问题是 router 按 token 内容路由：GPU 0 上产生的 token 可能要去 GPU 3 的专家，GPU 3 的 token 又可能要去 GPU 1。

```text
GPU 0 tokens -> experts on GPU 1,2,3
GPU 1 tokens -> experts on GPU 0,2,3
GPU 2 tokens -> experts on GPU 0,1,3
GPU 3 tokens -> experts on GPU 0,1,2
```

这形成 **all-to-all（全互连交换）**：每台设备都可能向每台设备发送 token 激活。专家算得再快，如果网络带宽不足或小批量消息过碎，通信就会盖过省下的矩阵乘法。

这也解释了一个 serving 反直觉：

- 大 batch 时，专家收到足够多 token，矩阵乘法效率高，通信可被摊薄。
- 小 batch / 低并发时，每个专家只收到零星 token，kernel 和通信开销难以摊薄，MoE 的理论 FLOPs 优势未必变成延迟优势。

这与昨天的 continuous batching 正好接上：continuous batching 不只是让 GPU 忙起来；对 MoE，它还能增大每轮可供分桶的 token 池，让专家 batch 更饱满。但并发升高也会增加通信和显存压力，仍需联合调度。

**结构标注**：第二笔核心代价；把模型级稀疏计算翻译成硬件级的权重驻留与数据搬运。

### 旁逸：这里和 RAG 是同一个形状

```text
MoE：先路由到少数专家，再执行参数计算
RAG：先检索少数文档，再执行上下文计算
```

二者都用“选择少数资源”扩大可用容量，也都受同一种失败模式支配：**路由错了，后面算得再准也没用；路由太集中，热门资源形成拥堵；候选全集虽不参与本次计算，却仍要被存储和索引。**

差别在于，RAG 路由的是外部知识，MoE 路由的是内部参数。这个同构提示我们：router 评测不应只看最终 loss，还应单独看选择质量、负载分布和失败切片。

---

## 5. `[骨]` MoE 如何改写 Chinchilla 的账本

Dense scaling law 的简化直觉是：给定训练算力 `C`，参数量 `N` 和训练 token 数 `D` 之间要合理分配；因为粗略地说：

```text
training_compute proportional to N * D
```

但到了 MoE，`N` 裂成至少两个量：

```text
N_total  = 全部参数，近似描述容量与权重存储
N_active = 每个 token 激活的参数，近似描述单-token 前向计算
```

于是更合理的第一版账本变成：

```text
训练 FLOPs       主要跟 N_active * D 走
权重显存/检查点   主要跟 N_total 走
通信与路由开销    跟专家布局、top-k、batch、网络走
模型质量          同时受 N_total、N_active、D、路由质量影响
```

这正是 MoE 给 scaling laws 增加的新自由度：固定近似 FLOPs 时，可以增加专家数来增大 `N_total`，而不同比例地增大 `N_active`。

但不要把它简化成“把 Chinchilla 里的 N 换成 N_active”——这样会漏掉总容量对 loss 的贡献，也会漏掉路由与通信。MoE 的最优分配至少是一个四变量问题：

```text
给定硬件和预算，如何分配：
  训练 token D
  每-token 激活规模 N_active
  专家总容量 N_total
  路由/通信可承受度 H
```

**新的核心判断**：Dense 模型里“参数多”同时意味着容量大、计算多、显存多；MoE 把这三个曾被捆在一起的量拆开了，但没有让任何一个消失。

**结构标注**：理论提升；把 07-16 的二变量算力分配推进成容量、计算、数据与硬件共同约束的问题。

### 碰撞提问

“MoE 训练更便宜”这句话只说对了一半。更准确的说法是：

> 在相近的每-token 激活计算下，MoE 可以提供更大的总参数容量；但训练效率是否更高，还取决于负载均衡、token dropping、通信和硬件利用率。

如果有人只报 FLOPs，不报总参数、激活参数、专家布局、通信环境和实际吞吐，你会接受他的“更高效”结论吗？

---

## 6. `[肌]` 一个系统设计判断题

假设你要部署两个模型：

```text
A. Dense：总参数 30B，每 token 激活 30B
B. MoE：总参数 100B，每 token 激活 25B
```

不能仅凭 `25B < 30B` 就断言 B 更快。至少要继续问：

1. **显存**：100B 全部权重以何种精度驻留？单机能否放下？
2. **设备布局**：专家是否跨卡？互连是 NVLink、PCIe 还是跨节点网络？
3. **top-k 与批量**：每轮每个专家能收到多少 token？矩阵乘法是否吃得饱？
4. **负载偏斜**：热门专家是否成为尾延迟瓶颈？
5. **延迟还是吞吐**：目标是单请求低延迟，还是高并发总吞吐？
6. **质量等价性**：两者是否在同一任务、同一质量水平下比较？

这六问把“模型论文里的 FLOPs”接回“线上系统的真实账单”。

**结构标注**：应用检验；将两笔账转化为可执行的部署审查清单。

> 本节在支持第 4、5 节：单-token 算术成本只是 serving 成本的一项，而不是结论。

---

## 7. `[筋]` 收束：MoE 不是免费午餐，而是换账本

作者从“为什么可以少算”过渡到“为什么系统未必更便宜”：MoE 把 dense 模型中绑定的容量、计算和存储拆开，让我们能单独调节它们；代价是 router 成为新的控制面，负载均衡和通信成为新的瓶颈。

最短记忆版本：

```text
MoE 的一条收益：
  大总容量 + 小激活子集

MoE 的两笔新账：
  训练：流量要均衡，否则专家坍缩或 token 溢出
  推理：权重要驻留，token 要跨设备搬运

MoE 的一个新问题：
  scaling law 里的“模型大小”不再是单一数字
```

---

## 全文复盘

### 理解轨迹

```text
参数量 = 计算量（dense 直觉）
        |
        v
总参数 N_total != 激活参数 N_active（MoE 核心）
        |
        +-> router 选择带来条件化计算
        |
        +-> 选择偏斜 -> 负载均衡账
        |
        +-> 专家分布 -> 显存与通信账
        |
        v
Chinchilla 的 N 被拆成容量、激活计算与硬件约束
```

### 读后一句话（不可快进）

**读完之后，你最想纠正别人关于 MoE 的哪一句常见说法？**

不要复述“MoE 是多个专家”；试着给出一个带判断的句子，例如：“MoE 省的是每-token 专家计算，不是总权重显存，所以 FLOPs 低不等于单请求延迟低。”

### 终局问题

如果 router 决定了每个 token 能访问哪部分参数，那么模型的“知识”究竟主要存在于专家权重里，还是存在于 router 划分输入空间的方式里？当路由错误时，我们该把它看成检索失败、模型容量不足，还是训练目标错配？

### 术语表

| 英文 | 中文 | 本文含义 | 出现位置 |
|---|---|---|---|
| Mixture of Experts (MoE) | 专家混合模型 | 用路由器为每个 token 稀疏选择少数 FFN 专家 | 第 1 节 |
| sparse activation | 稀疏激活 | 每次前向只使用总参数的一部分 | 第 1 节 |
| router / gating network | 路由器 / 门控网络 | 根据 token 隐状态给专家打分并选 top-k | 第 2 节 |
| top-k routing | 前 k 路由 | 每个 token 只进入得分最高的 k 个专家 | 第 2 节 |
| expert collapse | 专家坍缩 | 流量集中到少数专家，其他专家失去训练机会 | 第 3 节 |
| auxiliary load-balancing loss | 辅助负载均衡损失 | 抑制专家流量极端偏斜的训练目标 | 第 3 节 |
| capacity factor | 容量因子 | 每个专家预留 token 槽位相对平均流量的倍率 | 第 3 节 |
| token dropping | token 丢弃 | 专家容量溢出后，部分 token 无法正常经过该专家 | 第 3 节 |
| expert parallelism | 专家并行 | 将不同专家放到不同设备 | 第 4 节 |
| all-to-all | 全互连交换 | 各设备按路由结果互相发送 token 激活 | 第 4 节 |
| N_total / N_active | 总参数 / 激活参数 | 分别近似描述容量存储与单-token 参数计算规模 | 第 5 节 |

### 下一步线索

1. **Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity**，重点看第 2 节的 top-1 routing、expert capacity 与 auxiliary loss：<https://arxiv.org/abs/2101.03961>
2. **Mixtral of Experts**，重点看第 2 节架构描述与“总参数 46.7B、每 token 使用 12.9B”的容量/激活区分：<https://arxiv.org/abs/2401.04088>
3. 把本文和 07-16 的 Chinchilla 笔记并读：`2026-07-16-chinchilla-scaling-laws.md`。具体追问不是“谁更强”，而是：**dense scaling law 的参数轴拆成 total / active 之后，数据最优配比是否还保持原来的形状？**
