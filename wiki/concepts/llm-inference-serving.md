---
title: LLM 推理服务优化——显存/延迟/吞吐三本账
created: 2026-07-24
updated: 2026-08-16
type: concept
tags: [inference, optimization, infra, llm]
sources: []
---

# LLM 推理服务优化——显存/延迟/吞吐三本账

自回归 decode 的根问题不是「模型算得慢」，而是**串行依赖 + 每步硬件利用率低**：第 t+1 个 token 的输入含第 t 个 token，t 没落地 t+1 就不能开始；每步只处理少量 token，却要把整套权重和不断增长的 KV cache 搬过计算单元，于是单 token decode 通常是 **memory-bound**——算力在等数据搬运。理解任何一项推理优化，先问它动的是哪一本账。

## 三本账的分工

不同优化改善不同指标，别用同一把尺子衡量：

```text
账目        典型手段                           主要改善指标
显存账      GQA/MQA、KV 量化、PagedAttention   同显存容纳更多有效 token → 更大 batch
延迟账      speculative decoding、Medusa       减少一个请求需要的串行大模型轮次
吞吐账      continuous / iteration-level batching  一张卡同时服务更多不等长请求、少空转
```

这三本账争夺同一批 GPU 计算与显存资源，必须在**真实并发分布**下一起评测——局部资源利用率最高，不等于线上目标最优。

## 显存账：KV cache 与 PagedAttention

**为什么 KV cache 既省计算又成瓶颈**：它是「用空间换计算」的经典交换——不缓存则每步重算历史 K/V，缓存则只算新 token 但必须持续保存并读取全部历史状态。KV 大小由**层数 × KV head 数 × head dim × 精度**决定，不是只看参数量；GQA/MQA 正是在推理侧大幅减 KV 的架构设计（Llama 2 70B 用 8 个 KV head，每 token 约 320 KiB；无 GQA 的 OPT-13B 每 token 高达 800 KB）。

**PagedAttention**（Kwon et al., SOSP 2023, arXiv:2309.06180）解决的不是「有效 KV 太大」，而是 **allocator/layout 的浪费**：旧式为每个请求按最大长度预分配一整块连续空间，profiling 显示只有 20.4%–38.2% 真正装有效 token，其余是 reservation（预留）/ internal（尾部永不用）/ external（空闲但不连续）三类碎片。解法与操作系统分页同形——把 KV 切成固定 token 数的逻辑块、允许物理非连续、用 block table 映射：

```text
逻辑 KV：  [L0] [L1] [L2] [L3]     ← 请求看到的连续上下文
             ↓ block table
物理显存： [P7] [P1] [P8] [P3]     ← 任意空闲块可复用
```

按需增长、消灭外部碎片、压低内部碎片、允许前缀/beam 共享（copy-on-write）。它主要改善**吞吐**（更大 batch 摊薄权重搬运），不保证 batch=1 单请求每 token 延迟同比下降，也不改变自回归的串行依赖。详见 [[2026-07-14-kv-cache-paged-attention]]。

## 延迟账：投机解码

自回归每步串行等上一个 token，投机解码用便宜的 draft 模型 q 先猜 k 个候选，大模型 p 在**一次前向里并行核验**：候选序列已给定，p 可像短 prefill 一样并行给每个位置打分。「验证比生成便宜」不是每 token 的 FLOPs 更少，而是 k 个位置合进一次调用、更易并行、摊薄权重读取与 kernel launch——它甚至增加总 FLOPs，却降低 wall-clock latency（**牺牲算力效率换延迟效率**）。

- **无损性**：随机采样时以 `accept(x)=min(1, p(x)/q(x))` 接受，拒绝后从残差分布 `max(0,p−q)` 归一化重采，产出 token 严格服从 p——经典投机解码是无损调度，不是量化式近似压缩。
- **接受率 α 是加速比总闸门**：每轮平均推进 `(1−α^{k+1})/(1−α)` 个 token；α 越低、k 越大边际存活率越低，别看到「一次验 k 个」就声称 k 倍加速。
- **Medusa** 去掉独立 draft 模型，在主干 hidden state 上挂多个 decoding head + tree attention，用「更远位置条件更弱」换掉「调度两个模型」的成本。

会更慢的场景：draft 与目标不一致（高温/跨语言/稀有标识符拉低 α）、draft 太贵、k 太大、高并发已填满 GPU（增每请求计算损总吞吐）。详见 [[2026-07-23-speculative-decoding-latency]]。

## 吞吐账：continuous / iteration-level batching

生产 serving 的真问题是「一张卡同时服务几百条不等长请求怎么不空转」。**病灶不是 batch 太小，而是调度边界过粗**：static batching 把若干请求绑成不可变小队——一起进场、等最慢成员走完才集体散场。分类模型里每样本只做一次前向，绑不绑无所谓；生成模型是个循环（prefill→token 1→…→EOS），每条何时遇 EOS 事先不知，有人 20 token、有人 800。于是**最长序列劫持整个 batch 的资源释放**（head-of-line blocking 的 serving 版），短请求 EOS 后留下的槽位持续空转，排队新请求明明能用却被挡在 batch 边界外。

**iteration-level scheduling（Orca, OSDI 2022）** 把调度粒度从「一条请求」下沉到「一次迭代」：每轮只让当前 batch 各走一步，一步之后交回控制权——检查谁 EOS 退场、谁能准入、显存是否够，再组下一轮。于是 batch 成员在生成途中就能换人，这就是 continuous / in-flight batching。名字的重点不在「GPU 永不停」而在 **admission（准入）连续发生**：新请求不必等一整批时代结束才进入执行集合。

一笔「槽位-迭代」玩具账让浪费可见——batch 容 4 条，A/B/C/D 各还需 2/4/7/9 步：有效工作 `2+4+7+9=22`，static batch 必须跑到 D 的第 9 步、容量 `4×9=36`，利用率仅 `22/36≈61%`，那 14 个空槽不是「算了 padding」，而是**可服务等待请求却没被重分配的执行槽**——continuous batching 在 A 结束即让 E 进、B 结束即让 F 进，只要 waiting queue 不空且显存允许就维持接近满载。（注意 61% 只是揭示结构性浪费的玩具指标，非真实 utilization：prefill/decode 计算形态不同、序列长度改变 KV 访问成本、batch shape 改变 kernel 效率。）

**它和 PagedAttention 正交、却不是同一个**：像酒店，continuous batching 管前台排房（客人退房能否立刻让排队客入住），PagedAttention 管房间切分与账册（是否必须整层预留、零散空房能否重组）。只有前者没有灵活 KV：想补新请求却因显存碎片/过度预留无法准入；只有后者没有前者：显存够却仍等最长请求清场。合成一句——**PagedAttention 让更多请求「住得下」，continuous batching 让住得下的请求「接得上」**；同 OS 的分页内存（状态放哪）+ 进程调度（下一时间片跑谁），只优化一个都饱和不了。据此有个诊断反射：**显存近满而 compute utilization 不高时别急着加显存**，先看活跃序列数、每轮 batched tokens、waiting/running 队列与 prefill/decode 比例——显存满只代表状态占满，不代表算力每轮在做高价值工作。

**「有空位就补人」在真实系统里的四个约束**（防止误读成无代价开关）：① prefill（整 prompt 并行、计算量大）与 decode（每序列每轮推一 token、内存带宽受限）不是同一种工作，超长 prompt 的 prefill 会独占一轮、拖高在 decode 用户的 ITL，故有 **chunked prefill** 切块控制每轮 token budget；② 吞吐与延迟是多目标——攒更大 batch 提 tokens/s 却恶化 TTFT，优先 decode 顺滑流式却让新请求 prefill 饥饿，实为 `max tokens/s s.t. TTFT/ITL SLO、KV 容量、公平/优先级`；③「请求数」不是稳定的 batch 度量（一条 8K prefill 与一条单 token decode 都算 1 个 request 但成本天差），故调度上限同时看活跃序列数与本轮 batched tokens；④ 高负载下 KV 不够会**抢占**（暂停/重算/换回），决策点越频繁，公平性/优先级/重算成本越要显式设计。

**三本账在此合流**——三者相乘才是端到端吞吐，各救一维、缺一不可：

```text
memory capacity  ×  iterations per request  ×  useful slots per iteration
      ↑                    ↑                          ↑
 PagedAttention     speculative decoding       continuous batching
（同显存装多少活跃序列）（单序列走完几次前向）  （每轮 batch 槽位多少在干活）
```

**一处同构**：它和 Agent 上下文工程是同一个形状——finished request 占着 batch slot ↔ stale observation 占着 context window，iteration-level eviction ↔ compaction/子代理隔离，admit waiting request ↔ 只把 task-relevant 证据放进窗口。共同原则：容量有限时不只问「装多少」，还要问「何时释放、由谁补位」（呼应 [[context-engineering]] 的「写权限闸门」、[[react-agent]] 的记忆环）。详见 [[2026-07-28-continuous-batching-throughput]]。

## 判断框架

看到任何推理优化，依次问：

```text
它减少的是：A 有效状态本身？(GQA/量化)  B 无效分配与碎片？(PagedAttention)
           C 重复计算/存储？(prefix caching)  D 权重搬运摊销？(continuous batching)
           E 串行轮次？(speculative decoding)
它改善的是：首 token 延迟 / 每 token 延迟(ITL) / 吞吐 / 每 token 成本 / 质量不回退
```

## 相关概念

- [[flash-attention]] — attention kernel 的 IO-aware 优化，与本页的显存/搬运账互补
- [[model-quantization]] — 从「有效状态」一端减 KV/权重，另一条降本路径
- [[mixture-of-experts]] — 参数量与每-token 计算量解耦，推理侧另一根账（routing/负载均衡）
- [[scaling-laws]] — 训练侧的算力分配账，与推理侧成本账对照
- [[context-engineering]] — 「容量有限时何时释放、由谁补位」在 Agent 上下文侧的同构问题（batch slot ↔ context window）
- [[react-agent]] — 上同构的另一端：iteration-level eviction ↔ 记忆环 compaction
- [[self-rag]] — 投机解码的「便宜提议 + 核验」骨架在检索控制流的同构（精确核验器 vs 概率核验器）

## 伴读来源

- [[2026-07-14-kv-cache-paged-attention]] — 显存账：memory-bound、KV 显存核算、PagedAttention 分页解法
- [[2026-07-23-speculative-decoding-latency]] — 延迟账：接受率、无损采样、Medusa、何时更慢
- [[2026-07-28-continuous-batching-throughput]] — 吞吐账：iteration-level scheduling、槽位-迭代玩具账、与 PagedAttention 正交、prefill/decode 多目标约束、Agent 上下文同构
