# 伴读：为什么生成比训练慢——KV cache 的内存账与 PagedAttention

> 本次命中薄弱点：**retrieval 以外的空缺·推理系统**；目标是把“自回归为何慢、KV cache 为何吃显存、PagedAttention 究竟省了什么”连成一条因果链。

材料：Kwon et al., *Efficient Memory Management for Large Language Model Serving with PagedAttention*, SOSP 2023, arXiv:2309.06180。

## 全局地图

### 一句话摘要

生成慢的根因不是“模型又算了一遍全文”，而是每次只生成一个 token、却要搬运庞大的权重和不断增长的 KV cache；PagedAttention 不压缩真正需要的 KV，而是用分页按需分配、消灭预留与碎片，让显存能容纳更大的动态 batch，从而摊薄每个 token 的搬运成本。

### 结构地图

```text
训练 / prefill：整段 token 可并行
        |
        v
大矩阵乘大矩阵 -> 计算密集 -> GPU 较容易吃满

decode：下一个 token 依赖上一个 token
        |
        v
每步只处理少量 token -> 反复读权重和历史 KV -> 内存带宽受限
        |
        v
想靠 dynamic batching 摊薄权重搬运
        |
        v
batch 上限又被 KV cache 显存和碎片卡住
        |
        v
PagedAttention：固定大小 block + 按需分配 + 非连续物理存储
        |
        v
同样显存装入更多有效 token 状态 -> 更大 batch -> 更高吞吐
```

### 段落分类概览（Agent 判断，可覆盖）

- [骨] 自回归 decode 为什么是 memory-bound
- [肌] 一笔 70B 模型的 KV cache 显存账
- [骨] 旧式连续预分配的三种浪费
- [骨] PagedAttention 的分页解法
- [肌] 论文结果与适用边界
- [骨] 从单请求延迟到服务吞吐的闭环

## 第一段 [骨]：先校正问题——不是“训练一定比生成快”

严格说，训练一次当然比生成一个 token 贵得多。这里所谓“生成比训练慢”，指的是：**按 token 吞吐看，尤其 batch 较小时，decode 阶段远没有训练或 prompt prefill 那么容易榨满 GPU。**

训练时，一段序列的所有位置已知，可以同时计算；prefill 也一样，整段 prompt 可以并行。它们主要做大规模矩阵-矩阵乘法，单位时间有大量算术可覆盖数据搬运。

decode 不同。第 t+1 个 token 必须等第 t 个 token 出来，每一步往往只新增一个 token。计算退化为更“瘦”的矩阵运算：GPU 每一步仍要读取大部分模型权重，还要访问此前所有 token 的 KV cache，却只产出很少的新工作。因此论文说：

> **Original:** “This sequential generation process makes the workload memory-bound, underutilizing the computation power of GPUs.”
>
> **直译（信）：** 这种顺序生成过程使工作负载受内存限制，无法充分利用 GPU 的计算能力。
>
> **意译（达）：** decode 的瓶颈常常不是算不动，而是数据喂不够快；算力在等显存搬数据。

**结构标注：** 这是全文的第一根骨头：顺序依赖导致低并行度，低并行度把瓶颈从 FLOPS 推向内存带宽。

### 碰撞 1

先停一下：如果 KV cache 能避免重复计算，为什么它反而成了瓶颈？

答案不是“缓存无用”，而是一个经典交换：**用空间换计算。** 没有 KV cache，第 t 步会重新计算前 t 个 token 的 K、V，计算量随上下文反复累积；有 KV cache，只算新 token 的 K、V，但必须保存并读取全部历史状态。它把“重复算”的问题，换成了“持续占显存、持续搬数据”的问题。

## 第二段 [肌]：70B 模型的一条请求，到底吃多少 KV cache？

以常见的 Llama 2 70B 架构作说明，假设：

- 80 层
- 8 个 KV heads（使用 GQA；注意不是 64 个 query heads）
- 每个 head 维度 128
- K、V 各一份
- FP16/BF16，每个元素 2 bytes

每个 token 的 KV cache：

```text
2 (K 和 V)
x 80 (层)
x 8 (KV heads)
x 128 (head dim)
x 2 bytes
= 327,680 bytes
= 320 KiB / token
```

于是，单条序列仅 KV cache 就是：

| 总序列长度 | KV cache |
|---:|---:|
| 4,096 tokens | 1.25 GiB |
| 8,192 tokens | 2.50 GiB |
| 32,768 tokens | 10.00 GiB |

这里的“总序列长度”包括 prompt 和已经生成的 output。它还没算模型权重、临时 activation、CUDA workspace 等。70B 权重若全用 FP16/BF16，单是参数约 130.4 GiB，通常必须做 tensor parallel 分摊到多张 GPU；KV cache 也会随注意力头分片，但**集群总账不会消失**。

论文原例是没有 GQA 的 OPT-13B：每 token KV 高达 800 KB，2048 tokens 的一条请求可占约 1.6 GB。这个对比很重要：**KV 大小由层数、KV head 数、head dim 和精度决定，不是只看“70B/13B”参数量。** GQA/MQA 正是在推理侧大幅减 KV 的架构设计。

**结构标注：** 这段把抽象的“显存瓶颈”变成可核算的容量约束。

## 第三段 [骨]：旧系统浪费的 60%-80%，浪费在哪里？

旧式 serving 系统为了让普通深度学习 kernel 看到连续 tensor，常为每个请求预先申请一整块连续空间，大小按最大可能长度估计。但 output 多长事前未知，于是出现三类损失：

```text
一块预分配的连续 KV 空间

[已经写入的 token][未来可能写入][最终永远用不到][空洞]
       有效             reservation     内部碎片      外部碎片
```

1. **Reservation（预留）**：未来也许会用，但当前别的请求不能用。
2. **Internal fragmentation（内部碎片）**：按最大长度申请，实际提前结束，尾部永远不用。
3. **External fragmentation（外部碎片）**：总空闲显存也许够，但被切成不连续小洞，塞不下一条新的连续大块。

> **Original:** “Our profiling results in Fig. 2 show that only 20.4% - 38.2% of the KV cache memory is used to store the actual token states in the existing systems.”
>
> **直译（信）：** 图 2 的 profiling 表明，在现有系统中，只有 20.4%-38.2% 的 KV cache 内存真正用于保存 token 状态。
>
> **意译（达）：** 所谓浪费 60%-80%，不是 KV 内容本身有这么多重复，而是分配方式让大部分容量处于“占着却没装有效 token”的状态。

**结构标注：** 这是问题定义，也是理解 PagedAttention 的关键边界：它主要解决 allocator/layout 的浪费，不是把每个有效 token 的 320 KiB 神奇压没。

### 碰撞 2

最容易产生的误解是：“既然碎片这么严重，做一次内存整理不就行了？”

论文的回答是，KV cache 本身很大，在线服务中搬动这些块会制造昂贵的数据复制和延迟尖峰；更重要的是，整理也解决不了“为了未知的未来长度而提前占位”。所以问题不是偶尔把房间收拾整齐，而是租房制度错了：**不该让每个请求一开始就包下一整层。**

## 第四段 [骨]：PagedAttention 做的事，和操作系统分页是同一个形状

PagedAttention 把一条序列的 KV cache 切成固定 token 数的逻辑块，并允许这些逻辑上连续的块散落在物理显存各处。每条序列维护一张 block table，把逻辑块号映射到物理块号。

```text
请求看到的逻辑 KV：  [L0] [L1] [L2] [L3]
                         |    |    |    |
block table              v    v    v    v
GPU 物理显存：         [P7] [P1] [P8] [P3]

逻辑连续，不要求物理连续。
```

> **Original:** “One can think of blocks as pages, tokens as bytes, and requests as processes.”
>
> **直译（信）：** 可以把块看作页，把 token 看作字节，把请求看作进程。
>
> **意译（达）：** vLLM 把操作系统早已解决的“每个进程以为自己拥有连续内存”搬到了 KV cache：请求拥有连续的逻辑上下文，底层只在需要时找任意空闲物理块。

这带来四件事：

1. **按需增长**：生成到新 block 时才申请，不为未知 output 提前包场。
2. **消灭外部碎片**：物理块等大，任意空闲块都可复用。
3. **压低内部碎片**：只有每条序列最后一个未填满 block 可能浪费。
4. **允许共享**：并行采样、beam search 或共同前缀可让多个逻辑块映射到同一物理块；发生分叉时再 copy-on-write。

需要付出的代价是间接寻址、block table 管理，以及专门的 attention kernel。PagedAttention 不是“免费午餐”，而是用一层地址映射换回显存利用率。

**结构标注：** 这是论文的核心机制：解除“逻辑连续 = 物理连续”的错误绑定。

### 旁逸：这和 RAG 的 chunking 相似，但目标相反

两者都把连续对象切成固定/有限粒度的块，再用索引恢复关系；但 RAG chunking 是为了**语义选择**，PagedAttention blocking 是为了**物理分配**。前者问“哪些块相关”，后者问“这些块放哪儿”。不要因为表面都有 block 就混成同一类问题。

## 第五段 [肌]：它如何变成吞吐，而不只是“省显存”？

真正的闭环是：

```text
更少 KV 浪费
  -> 同一时刻容纳更多请求
  -> dynamic batch 更大
  -> 一次读取模型权重，可服务更多 token
  -> 每个 token 分摊到的权重搬运成本下降
  -> 吞吐上升
```

论文实验中，旧系统实际 token states 只占 KV 区的 20.4%-38.2%，vLLM 图示达到 96.3%；在相近延迟下，论文报告 vLLM 相对当时的 FasterTransformer 和 Orca 提升 2-4 倍吞吐。在不同数据、模型和基线配置下提升幅度不同，长序列、大模型及复杂 decoding 通常获益更明显。

注意两个限定：

- **它主要改善服务吞吐，不保证单条、batch=1 请求的每 token 延迟同比下降。** batch 很小时，分页省出的容量没有转化成并发，收益可能有限。
- **它不改变自回归的串行依赖。** 下一个 token 仍要等上一个；它优化的是“如何管理历史状态并扩大有效 batch”，不是把 decode 变成训练式全并行。

**结构标注：** 这段完成从内存分配到线上指标的因果闭环。

## 压力测试

有人反驳：“现代模型已经用了 GQA，70B 在 4K 上每条只要 1.25 GiB KV；PagedAttention 还有那么重要吗？”

这个反驳只打掉了“每个有效 token 太贵”的一部分，却没打掉三件事：

1. 并发请求数会把 1.25 GiB 线性放大；
2. 上下文从 4K 到 32K，单请求 KV 又放大 8 倍；
3. output 长度仍未知，连续预留和碎片问题仍在。

但反驳也提醒我们：当场景是短上下文、低并发、KV 量化充分、显存富余时，系统可能从 memory-bound 转为 compute-bound，PagedAttention 的边际收益会下降。论文自己也观察到：短序列且 KV 空间充裕时，优势不那么明显。

## 今日带走的判断框架

以后看到任何推理优化，不要只问“省了多少显存”，而要依次问：

```text
它减少的是：
  A. 有效状态本身？        例如 GQA、KV quantization
  B. 无效分配与碎片？      例如 PagedAttention
  C. 重复计算或重复存储？  例如 prefix caching、copy-on-write
  D. 权重搬运的摊销成本？  例如 continuous batching

最后，它改善的是：
  单请求延迟 / 首 token 延迟 / 每 token 延迟 / 吞吐 / 成本
```

PagedAttention 的主答案是 B，并通过更大 batch 间接改善 D，最终主要推高吞吐。

## 留给你的一个问题

如果线上目标从“最大吞吐”改成“严格限制 P99 延迟”，你还会尽可能把 batch 做大吗？PagedAttention 释放出的显存，应该全部拿去装更多请求，还是应留作调度余量？

这道题把显存管理重新接回端到端闭环：**局部资源利用率最高，不等于线上目标最优。**

## 术语表

| 英文 | 中文 | 本文含义 |
|---|---|---|
| decode | 解码/生成阶段 | 自回归地一次生成一个 token |
| prefill | 预填充阶段 | 并行处理整段 prompt，建立初始 KV cache |
| KV cache | 键值缓存 | 保存历史 token 在各层注意力中的 K、V 状态 |
| memory-bound | 内存带宽受限 | 算力在等数据搬运，而非计算单元已满载 |
| dynamic/continuous batching | 动态/连续批处理 | 每个迭代移除完成请求、加入新请求 |
| internal fragmentation | 内部碎片 | 已分配块内部最终未使用的空间 |
| external fragmentation | 外部碎片 | 空闲空间总量够但不连续，无法满足大块申请 |
| PagedAttention | 分页注意力 | 让逻辑连续 KV 存在非连续物理块上的 attention 方法 |
| copy-on-write | 写时复制 | 共享块保持共用，真正分叉写入时才复制 |

## 下一步线索

继续读原论文第 4.2-4.5 节：重点看 block table、copy-on-write，以及显存不足时 swapping 与 recomputation 两种抢占恢复策略。阅读时只追一个问题：**分页解决了“放哪里”，调度器又如何决定“谁先留在 GPU 上”？**