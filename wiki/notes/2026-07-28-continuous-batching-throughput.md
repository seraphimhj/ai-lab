本次命中：*retrieval 以外的空缺 -> 推理系统*，承接 07-14 的「显存账」与 07-23 的「延迟账」，今天补齐生产 serving 的第三本账：*吞吐账*。

#+title: 伴读：Continuous Batching 如何把 GPU 从空转里救回来
#+date: [2026-07-28 Tue 09:00]
#+filetags: :reading:llm-serving:inference:
#+source: Orca (OSDI 2022) / vLLM continuous batching

* 全局地图

** 一句话摘要

Continuous batching 的关键不是「把 batch 调大」，而是把调度单位从*整条请求*缩小到*每一次 token 迭代*：短请求一结束就退场，等待请求立即补位，从而不再让整个 batch 被最长序列绑架。

** 结构地图

#+begin_example
request arrives
      |
      v
+-------------+       memory allows?
| waiting q   | --------------------------+
+-------------+                           |
                                          v
                                  +---------------+
                                  | current batch |
                                  +---------------+
                                          |
                                  one model iteration
                                          |
                                          v
                           +-----------------------------+
                           | emit token / update KV cache|
                           +-----------------------------+
                              |                    |
                         reached EOS?          not finished
                              |                    |
                              v                    +-----> next iteration
                         remove slot
                              |
                              v
                       admit waiting request
#+end_example

三本账放在一起看：

#+begin_example
07-14  PagedAttention       : 同样显存能容纳多少条活跃序列？
07-23  Speculative decoding: 单条序列走完要等多少次大模型前向？
07-28  Continuous batching : 每次前向中的 batch 槽位有多少在干活？

memory capacity  x  iterations per request  x  useful slots per iteration
       ^                    ^                         ^
 PagedAttention       speculative decoding     continuous batching
#+end_example

** 段落分类（Agent 判断，可覆盖）

- [骨] 生成任务为什么让传统 batching 失效：请求长度未知且不同。
- [骨] iteration-level scheduling：每轮都允许 batch 成员变化。
- [肌] 四条请求的玩具账本：浪费究竟发生在哪里。
- [骨] PagedAttention 与 continuous batching 为什么是一套，而非同义词。
- [肌] prefill/decode 混跑、延迟目标与公平性带来的真实约束。
- [筋] 从单卡调度过渡到线上指标与诊断。

* 逐段伴读

** 第 1 段：[骨] 真正的问题不是 batch 太小，而是 batch 被「封死」

*** 英文原文

Orca 对旧式 serving 的诊断是：

"Requests that have finished earlier than other requests in a batch cannot return to the client, while newly arrived requests have to wait until the current batch completely finishes."

*** 直译层（信）

「一个 batch 中比其他请求更早完成的请求无法返回给客户端，而新到达的请求必须等待当前 batch 完全结束。」

*** 意译层（达）

传统 static batching 把若干请求绑成一个不可变小队：一起进场，等最慢的成员走完后才集体散场。问题在分类模型里不大，因为每个样本通常只做一次前向；但生成模型不是一次前向，而是一个循环：

#+begin_example
prompt -> prefill -> token 1 -> token 2 -> ... -> EOS
#+end_example

每条请求何时遇到 EOS 事先不知道。有人只生成 20 token，有人生成 800 token。若 batch 的成员在 800 token 结束前不能变化，那么短请求完成后留下的槽位就会持续空转；排队的新请求明明可以使用这些槽位，却被挡在 batch 边界之外。

这里首次出现两个术语：

- *static batching（静态批处理）*：一个 batch 开始执行后，成员固定到整批结束。
- *head-of-line blocking（队首阻塞）*：前面的慢任务拖住后面的任务；这里更准确地说，是最长生成序列拖住整个 batch 的资源释放。

*** 结构标注

核心问题定义：把吞吐损失定位为「调度边界过粗」，而不是笼统归咎于 GPU 不够快。

*** 注疏：对手光

最强反驳是：「短请求已经 EOS，就用 padding 保持形状；GPU kernel 仍然可以一次跑完整 batch，未必算了无用 token。」

这只说对一半。mask 可以避免把 padding 当成有效语义，却不能让空槽自动变成另一条真实请求。即使某些算子跳过了无效位置，系统仍失去了本可承载新请求的并发机会。*语义上不计算 padding，不等于调度上没有机会成本。*

*** 碰撞问题

作者最想让你接受的点是：*生成 serving 的基本调度单位不应该是 request，而应该是 iteration。* 如果你的第一反应仍是「把 batch size 调大」，你是在改变容器大小，还没有改变容器何时可以换人。

** 第 2 段：[骨] Orca 把调度单位切到一次迭代

*** 英文原文

"We propose iteration-level scheduling, a new scheduling mechanism that schedules execution at the granularity of iteration (instead of request) where the scheduler invokes the execution engine to run only a single iteration of the model on the batch."

*** 直译层（信）

「我们提出迭代级调度（iteration-level scheduling）：调度器以迭代而非请求为粒度安排执行，并且每次只调用执行引擎，在当前 batch 上运行模型的一次迭代。」

*** 意译层（达）

旧调度器说：「这四条请求交给 GPU，全部生成完再来找我。」

Orca 的调度器说：「先让当前四条各走一步；一步之后把控制权还给我。我检查谁结束、谁能进入、显存是否足够，再组下一轮 batch。」

#+begin_example
static batching

schedule [A B C D] ---------------------------------> all done
                    batch membership is frozen

iteration-level scheduling

iter 1 [A B C D]
iter 2 [A B C D]
iter 3 [E B C D]    A ended; E enters immediately
iter 4 [E F C D]    B ended; F enters immediately
...
#+end_example

这就是常说的 *continuous batching（连续批处理）*、*in-flight batching（飞行中批处理）*。名字不同，核心都不是「不断攒一个新 batch」，而是*当前 batch 在生成途中就可以换成员*。

*** 点睛层（雅）

「continuous」容易误译成 GPU 永不停止。它真正强调的是 admission（准入）连续发生：请求不必等一个整批的时代结束，才能进入执行集合。GPU 是否始终满载还取决于请求流量、显存、kernel 形状以及 prefill/decode 调度。

*** 结构标注

核心机制：把不可变的 request-level batch 改成每轮可重组的 iteration-level batch。

*** 碰撞问题

如果调度器每轮都可换人，它获得了更高利用率，也同时获得了新的权力：谁先进入、谁被暂停、prefill 和 decode 谁优先。*吞吐优化从此不只是 kernel 问题，也变成排队与策略问题。*

** 第 3 段：[肌] 算一笔「槽位-迭代」账

假设 batch 最多容纳 4 条请求，A/B/C/D 分别还要生成 2、4、7、9 个 token。先用一个故意简化的模型：每轮每条活跃序列生成 1 token，每个槽位成本相同。

#+begin_example
request       A   B   C   D
output steps  2   4   7   9
#+end_example

有效工作量是：

#+begin_example
2 + 4 + 7 + 9 = 22 useful slot-iterations
#+end_example

静态 batch 必须跑到 D 的第 9 步才结束，容量账是：

#+begin_example
4 slots x 9 iterations = 36 slot-iterations
waste = 36 - 22 = 14
useful ratio = 22 / 36 = 61.11%
#+end_example

空泡如何出现：

#+begin_example
iteration  1 2 3 4 5 6 7 8 9
A          X X . . . . . . .
B          X X X X . . . . .
C          X X X X X X X . .
D          X X X X X X X X X
#+end_example

其中 `.` 不是模型「生成了 padding」，而是*一个可以服务等待请求、却没有被重新分配的执行槽位*。连续批处理会在 A 结束后让 E 进入，在 B 结束后让 F 进入。只要 waiting queue 不空且显存允许，后续多轮就能维持接近 4 条活跃序列。

但不要把 61.11% 当成真实 GPU utilization。它只是揭示结构性浪费的玩具指标。真实每轮成本并不相等：prefill 与 decode 的计算形态不同，序列长度会改变 attention/KV 访问成本，batch shape 也会改变 kernel 效率。

*** 结构标注

证据展开：用最小账本把「最长序列绑架 batch」从直觉变成可见的容量损失。

以上 1 个肌肉段在支持第 1、2 个骨架段的论证。

** 第 4 段：[骨] Continuous batching 与 PagedAttention 各救一维

continuous batching 常和 vLLM 的 PagedAttention 一起出现，因此很容易混成同一个概念。把系统想成一家酒店：

- continuous batching 管*前台排房*：客人退房后，能否立刻让排队客人入住。
- PagedAttention 管*房间切分与账册*：是否必须提前给每位客人预留一整层，以及零散空房能否重新组合利用。

两者解决的是正交问题：

#+begin_example
                     scheduling slots
                           |
                           v
continuous batching: finished sequence out, waiting sequence in

PagedAttention:      allocate KV cache in non-contiguous blocks
                           ^
                           |
                       memory slots
#+end_example

只有 continuous batching、没有灵活 KV 管理：调度器想补进新请求，却可能因连续显存碎片或过度预留而无法准入。

只有 PagedAttention、没有 continuous batching：显存能容纳更多序列，但静态 batch 的空槽仍要等最长请求结束才重用。

所以 07-14 和今天可以合成一句：

*PagedAttention 让更多请求「住得下」；continuous batching 让住得下的请求「接得上」。*

*** 结构标注

概念边界：区分显存容量与执行调度，再说明二者如何相乘。

*** 注疏：同构光

这里和操作系统的虚拟内存加进程调度是同一个形状：页式内存管理回答「状态放在哪里」，调度器回答「下一时间片运行谁」。只优化其中一个，都不能让系统整体饱和。

*** 碰撞问题

如果线上监控显示 GPU memory 已接近满载、GPU compute utilization 却不高，你应该先怀疑哪一层？不是立刻加显存；先看活跃序列数、每轮 batch token 数、waiting/running 队列和 prefill/decode 比例。*显存满只代表状态占满，不代表算力每轮都在做高价值工作。*

** 第 5 段：[肌] 真实系统比「有空位就补人」难在哪

*** 1. Prefill 和 decode 不是同一种工作

prefill 一次处理整个 prompt，通常并行度高、计算量大；decode 每条序列每轮通常只推进一个 token，更受模型权重与 KV cache 内存带宽限制。如果一个超长 prompt 的 prefill 突然进入，可能占据很长一次执行，拖高正在 decode 用户的 inter-token latency（ITL，token 间延迟）。

因此现代引擎还会做 chunked prefill：把长 prompt 切块，避免一条 prefill 独占过大的单轮预算。这里的目标不再是单纯「填满 batch size」，而是控制每轮的 token budget。

*** 2. 吞吐和延迟不是同一个目标

等待更久以攒更大的 batch，可能提高 tokens/s，却恶化 time to first token（TTFT，首 token 延迟）。优先 decode 可以保持流式输出顺滑，却可能让新请求的 prefill 饥饿。调度策略实际是在解一个多目标问题：

#+begin_example
maximize   total tokens / second
subject to TTFT SLO
           ITL SLO
           KV-cache capacity
           fairness / priority
#+end_example

*** 3. 「请求数」不是稳定的 batch 度量

一条 8K prompt 的 prefill 和一条单 token decode 都算一个 request，但成本完全不同。因此常见调度上限会同时考虑活跃序列数和本轮 batched tokens，而不只是 `batch_size = N`。

*** 4. 高负载下还会出现抢占

KV cache 不够时，引擎可能暂停或抢占某些序列，稍后重算或换回。continuous batching 提供了频繁决策点，但决策越灵活，公平性、优先级和重算成本也越需要显式设计。

*** 结构标注

边界条件：防止把论文核心机制误解成「一个无代价、永远提高所有指标的开关」。

以上 4 个肌肉单元在限定第 2、4 个骨架段的适用范围。

** 第 6 段：[筋] 从机制过渡到线上诊断

作者从「如何换 batch 成员」过渡到更重要的生产问题：「你的瓶颈到底是没有请求、没有显存槽、没有 token 预算，还是调度策略不肯放行？」

* 一次旁逸：它和 Agent 上下文工程是同一个形状

07-27 讲 compaction、子代理隔离、按需检索，是为了不让过期内容永久占据 context window。今天的 continuous batching 是为了不让已结束请求永久占据执行 batch。

#+begin_example
LLM serving                 Agent context
------------------------    -------------------------
finished request            stale observation
occupies batch slot         occupies context window
iteration-level eviction    compaction / isolation
admit waiting request       admit task-relevant evidence
#+end_example

共同原则是：*容量有限时，不只要问「装多少」，还要问「何时释放、由谁补位」。* 这也是 PagedAttention、continuous batching 与 context compaction 能互相照亮的原因。

* 压力测试：三个最容易混淆的判断

1. *「continuous batching 会缩短单条请求必须生成的步数。」*
   - 错。它主要回收 batch 空槽；减少大模型串行步数是 speculative decoding 的方向。

2. *「PagedAttention 提高吞吐，所以它就是 continuous batching 的实现。」*
   - 错。前者管理 KV cache 的内存块，后者管理每轮执行集合。它们协同，但层次不同。

3. *「GPU utilization 越高，用户体验一定越好。」*
   - 错。吞吐可以通过更激进地混入 prefill 提升，同时 TTFT 或 ITL 变差。必须在相同延迟 SLO 下比较吞吐。

* 全文复盘

** 理解轨迹

#+begin_example
单请求视角
  |
  +-- memory: KV cache / PagedAttention          [已接上 07-14]
  |
  +-- latency: speculative decoding              [已接上 07-23]
  |
  v
多请求视角
  |
  +-- static batch waste                         [今天定位]
  |
  +-- iteration-level scheduling                 [今天核心]
  |
  +-- continuous admission + paged KV memory     [今天合流]
  |
  v
生产约束
  +-- TTFT / ITL / throughput / fairness         [留下张力]
#+end_example

今天真正要带走的不是一个框架名，而是一条判断：*自回归生成把一次 inference 变成可中断的多轮过程；既然每轮都有请求完成，调度边界就也应该下沉到每轮。*

** 读后一句话（不可跳过）

读完之后，你最想对作者说的一句话是什么？

可以先用这个半成品逼自己表态，而不是复述：

「我接受 iteration-level scheduling 能回收空槽，但我认为线上真正决定收益上限的是 ______，因为 ______。」

** 终局问题

当 serving 系统可以在每个 token 边界重新决定「谁继续、谁暂停、谁进入」时，调度器实际上正在分配用户的等待时间。*如果 tokens/s 最大化与尾延迟、公平性冲突，什么才是正确的目标函数？*

** 术语表

| 英文 | 中文 | 本文含义 | 出现位置 |
|-
| static batching | 静态批处理 | batch 成员固定到整批完成 | 第 1 段 |
| iteration-level scheduling | 迭代级调度 | 每次模型迭代后重新安排执行集合 | 第 2 段 |
| continuous batching | 连续批处理 | 生成途中持续移出完成请求、准入等待请求 | 第 2 段 |
| head-of-line blocking | 队首阻塞 | 慢请求阻碍资源释放与后续准入 | 第 1 段 |
| prefill | 预填充 | 对 prompt 做初始并行计算并建立 KV cache | 第 5 段 |
| decode | 解码 | 基于已有 KV cache 逐 token 生成 | 第 5 段 |
| TTFT | 首 token 延迟 | 从请求到达至输出第一个 token 的时间 | 第 5 段 |
| ITL | token 间延迟 | 流式生成相邻 token 的等待时间 | 第 5 段 |
| PagedAttention | 分页式注意力内存管理 | 以非连续块管理 KV cache | 第 4 段 |

** 下一步线索

不是泛泛书单，只沿今天留下的裂缝继续两步：

1. Orca, OSDI 2022，重点读 Section 3 的 iteration-level scheduling 与 selective batching：为什么不同 token position 的请求能组成同一轮执行。
2. vLLM / PagedAttention 论文中 scheduler 与 block manager 的交界：调度器想准入新序列时，KV block 的可分配性如何成为硬约束。

* 最小复述

如果今天只留一句：

*Static batching 等最慢请求清场；continuous batching 每生成一轮就重新排座。PagedAttention 负责腾得出座，continuous batching 负责马上换人。*
