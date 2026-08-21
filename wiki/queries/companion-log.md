# 伴读日志（Companion Log）

> hermes 每日追加：当天推送了什么 + 昨天推送收到的用户反馈。
> Claude 读这里挖掘新薄弱点。只追加，不修改历史。
> **推进门禁：最近一篇推送所在日期段必须有用户明确“已读”，或针对该篇的
> 评论/追问/理解反馈，Hermes 与 Claude 才能推进下一篇；“无反馈”不算。**

<!-- 每条格式：
## YYYY-MM-DD
- 推送：主题/材料（命中：哪条主线或薄弱点）
- 反馈：用户对上一次推送的反应要点——追问了什么、哪里卡壳、
  说了“已读”/“已懂”还是“没讲透”、有没有提出新问题。没有反馈不要写占位。
-->

## 2026-07-12
- 推送：从 MLE 到 DPO：目标函数的同源推导（命中：统一数学框架）
- 推送：端到端闭环：偏差传导的放大回路（命中：端到端闭环）
- 反馈：无反馈（首次每日推送，用户尚未反馈）
- 反馈：追问如何用易懂语言解释交叉熵的数学含义。
- 反馈：追问交叉熵、KL 散度、最大似然是否相同，以及为何有不同名称和表达。
- 反馈：指出微信中 LaTeX 公式反斜杠外露，阅读体验不好；后续应使用纯文本公式。
- 反馈：已懂并认可“MLE 是原则，NLL/交叉熵是优化形式，KL 是分布解释”的总结。
- 反馈：提出 Margin MSE 与 DPO 思想相似，抓住了二者学习相对偏好差值的共同骨架。
- 反馈：新问题：InfoNCE 与 KL loss 同时学习是否冗余。

## 2026-07-13
- 推送：InfoNCE 与 KL loss 同时学习，冗余吗？（命中：统一数学框架 + RAG / Embedding；对应 `wiki/notes/2026-07-13-infonce-vs-kl.md`）
- 反馈：已懂并确认在其场景中，KL 蒸馏 teacher 软标签，与 InfoNCE 互补。
- 反馈：新问题：请求介绍 SPLADE 召回方式。

## 2026-07-14
- 推送：为什么生成比训练慢：KV cache 的内存账与 PagedAttention（命中：retrieval 以外·推理系统；对应 `wiki/notes/2026-07-14-kv-cache-paged-attention.md`）

## 2026-07-15
- 推送：SPLADE——把“查询扩展”学进 30K 维词表（命中：RAG / 检索 / Embedding 主线；对应 `wiki/notes/2026-07-15-splade-learned-sparse-retrieval.md`）
- 反馈：首次微信投递因限流未收到，用户要求重新推送当天伴读。

## 2026-07-16
- 推送：数据和参数怎么分钱——Chinchilla 与 Scaling Laws（命中：retrieval 以外·预训练 + 端到端闭环·数据环节；对应 `wiki/notes/2026-07-16-chinchilla-scaling-laws.md`）

## 2026-07-17
- 推送：你的评测集是从哪个分布采的？——benchmark 失效的三种方式（命中：端到端闭环·评测环节 + 模型评估主线；对应 `wiki/notes/2026-07-17-benchmark-failure-distribution.md`）

## 2026-07-18
- 推送：RLHF 之后——DPO / KTO / GRPO 一张家谱（命中：retrieval 以外·后训练 + 统一数学框架；对应 `wiki/notes/2026-07-18-dpo-kto-grpo-family.md`）
- 反馈：追问 SPLADE 的 MLM head 如何对 token 打分。

## 2026-07-19
- 推送：SPLADE 的 MLM head 到底怎么给一个词打分——从 30K 维 logits 到稀疏权重（命中：RAG / 检索 / Embedding 主线；对应 `wiki/notes/2026-07-19-splade-mlm-head-term-scoring.md`）

## 2026-07-20
- 推送：Agent 的多步闭环——误差如何在 ReAct 循环里复合（命中：端到端闭环·偏差传导 + Agent / 工具使用 / 上下文工程主线；对应 `wiki/notes/2026-07-20-react-agent-error-compounding.md`）

## 2026-07-21
- 推送：两次架构革命都守着同一条边界——让出「路径」，钉死「指南针」（命中：端到端闭环·评测环节 + 模型评估主线；对应 `wiki/notes/2026-07-21-path-and-compass.md`）
- 反馈：新问题：Embedding 模型如何解决实体 mismatch。

## 2026-07-22
- 推送：Embedding 为什么会认错实体？——从单向量 mismatch 到三条修法（命中：RAG / 检索 / Embedding 主线；对应 `wiki/notes/2026-07-22-embedding-entity-mismatch.md`）

## 2026-07-23
- 推送：投机解码——用小模型猜，大模型一次并行验（命中：retrieval 以外·推理系统；对应 `wiki/notes/2026-07-23-speculative-decoding-latency.md`）

## 2026-07-24
- 推送：Late Interaction 与 MUVERA——交互究竟应该发生在哪一步？（命中：RAG / 检索 / Embedding 主线；对应 `wiki/notes/2026-07-24-late-interaction-muvera.md`）

## 2026-07-25
- 推送：「平均」如何在编码端和评测端抹掉决定性少数信号（命中：端到端闭环 + 模型评估 + RAG / Embedding；对应 `wiki/notes/2026-07-25-aggregation-erases-minority-signals.md`）

## 2026-07-26
- 推送：Self-RAG / CRAG——检索不再是一条管道，而是一个可纠错的动作（命中：RAG / 检索主线 + Agent / 上下文工程主线；对应 `wiki/notes/2026-07-26-self-rag-crag-agentic-retrieval.md`）

## 2026-07-27
- 推送：上下文工程如何拦住 Agent 的误差复合——compaction / 子代理隔离 / 按需检索 / 外部记忆（命中：端到端闭环·偏差传导 + Agent / 工具使用 / 上下文工程主线；对应 `wiki/notes/2026-07-27-context-engineering-error-firebreaks.md`）

## 2026-07-28
- 推送：Continuous Batching 如何把 GPU 从空转里救回来——从静态 batch 空泡到 iteration-level scheduling（命中：retrieval 以外·推理系统；对应 `wiki/notes/2026-07-28-continuous-batching-throughput.md`）

## 2026-07-29
- 推送：MoE——把参数量和每-token 计算量解耦，一次路由要还的两笔账（命中：retrieval 以外·预训练 + 推理系统；对应 `wiki/notes/2026-07-29-moe-capacity-compute-routing.md`）

## 2026-07-30
- 推送：模型会做对题，不等于它知道自己有多大把握——区分、校准与决策效用（命中：模型评估主线 + 统一数学框架；对应 `wiki/notes/2026-07-30-calibration-vs-ranking.md`）

## 2026-07-31
- 推送：谁能让模型诚实地报出概率？——Proper Scoring Rules、NLL 与 Brier 的统一框架（命中：统一数学框架 + 模型评估主线；对应 `wiki/notes/2026-07-31-proper-scoring-rules-honest-probabilities.md`）

## 2026-08-01
- 推送：LLM-as-judge 的系统性偏置——当「指南针」也学会了被迎合（命中：端到端闭环·评测环节 + 模型评估主线；对应 `wiki/notes/2026-08-01-llm-as-judge-systematic-bias.md`）

## 2026-08-02
- 推送：一条梯度看懂 SFT、DPO、PPO 与 GRPO——奖励到底该算到哪个 token 头上？（命中：统一数学框架 + retrieval 以外·后训练 + 端到端闭环；对应 `wiki/notes/2026-08-02-token-credit-assignment.md`）

## 2026-08-03
- 推送：数据配比不是预处理，而是隐形的目标函数——用 DoReMi 看懂预训练“给谁更多梯度”（命中：retrieval 以外·大模型预训练 + 统一数学框架 + 端到端闭环；对应 `wiki/notes/2026-08-03-doremi-data-mixture-objective.md`）

## 2026-08-04
- 推送：Agent 成功率 80%，为什么仍不敢上线？——τ-bench 与 pass^k 的可靠性账（命中：Agent / 工具使用 / 上下文工程 + 模型评估 + 端到端闭环；对应 `wiki/notes/2026-08-04-tau-bench-pass-k-agent-reliability.md`）

## 2026-08-05
- 推送：RAG 评测不是一个分数，而是一张故障定位图——用 RAGAS 与反事实实验拆开召回、证据利用和生成忠实度（命中：RAG / 检索 / Embedding + 模型评估 + 端到端闭环；对应 `wiki/notes/2026-08-05-rag-evaluation-causal-decomposition.md`）

## 2026-08-06
- 推送：BM25 的 12 分和 Dense 的 0.82，为什么不能直接相加？——从分数尺度到 RRF 混合检索（命中：RAG / 检索 / Embedding + 统一数学框架 + 端到端闭环；对应 `wiki/notes/2026-08-06-hybrid-retrieval-score-fusion.md`）

## 2026-08-07
- 推送：Cross-Encoder 为什么更准，却不能直接替代召回？——从联合编码到 reranker 的召回上限（命中：RAG / 检索 / Embedding + 端到端闭环；对应 `wiki/notes/2026-08-07-cross-encoder-reranking-recall-ceiling.md`）

## 2026-08-08
- 推送：离线高分为什么可能让 Agent 上线变差？——反事实评估与 IPS（命中：模型评估 + Agent / 工具使用 + 端到端闭环；对应 `wiki/notes/2026-08-08-counterfactual-offline-evaluation-ips.md`）

## 2026-08-09
- 推送：同一段系统提示词，为什么还要算一千遍？——Prefix Caching 与共享上下文的复用边界（命中：retrieval 以外·推理系统 + Agent / 上下文工程 + 端到端闭环；对应 `wiki/notes/2026-08-09-prefix-caching-shared-context.md`）

## 2026-08-10
- 推送：长 Prompt 为什么会堵住整张卡？——Chunked Prefill 与推理调度的队头阻塞（命中：retrieval 以外·推理系统 + Agent / 上下文工程 + 端到端闭环；对应 `wiki/notes/2026-08-10-chunked-prefill-scheduling.md`）

## 2026-08-11
- 推送：难负例不是“更难的数据”——从有效梯度、假负例到采样分布如何改写检索边界（命中：RAG / 检索 / Embedding + 统一数学框架 + 端到端闭环；对应 `wiki/notes/2026-08-11-hard-negatives-false-negatives.md`）

## 2026-08-12
- 推送：采样不是搬运数据——Importance Sampling 如何统一 DoReMi、难负例与离线评估（命中：统一数学框架 + 端到端闭环；对应 `wiki/notes/2026-08-12-importance-sampling-hidden-objective.md`）

## 2026-08-13
- 推送：KL 正则不是“防止模型变坏”的装饰项——从信任域、指数倾斜到 DPO（命中：统一数学框架 + retrieval 以外·后训练 + 端到端闭环；对应 `wiki/notes/2026-08-13-kl-regularization-trust-region.md`）

## 2026-08-14
- 推送：Teacher Forcing 的隐形裂缝——训练时总看正确历史，上线后却活在自己的历史里（命中：端到端闭环 + 统一数学框架 + Agent / 上下文工程；对应 `wiki/notes/2026-08-14-teacher-forcing-exposure-bias.md`）

## 2026-08-15
- 推送：从 Teacher Forcing 到 DAgger——为什么“偶尔喂模型自己的答案”仍可能学错（命中：端到端闭环 + 统一数学框架 + Agent / 上下文工程；对应 `wiki/notes/2026-08-15-scheduled-sampling-dagger-distribution-shift.md`）

## 2026-08-16
- 推送：DAgger 之后为什么是 RL——把训练分布直接做成部署分布，而不是去追它（命中：端到端闭环 + 统一数学框架 + retrieval 以外·后训练；递进 08-14/15 的分布错位，收口 08-02 信用分配 / 08-12 IS / 08-13 KL；对应 `wiki/notes/2026-08-16-dagger-to-rl-on-policy.md`）

## 2026-08-17
- 推送：PPO 的 clip 到底剪掉了什么？——旧策略数据、重要性比率与一笔有意为之的偏差（命中：统一数学框架 + 端到端闭环 + retrieval 以外·后训练；递进 08-16 的 on-policy 数据过期问题，接回 08-12 importance sampling 与 08-13 trust region；对应 `wiki/notes/2026-08-17-ppo-clipping-stale-policy-data.md`）

## 2026-08-18
- 推送：GAE 到底在估计什么？——PPO 更新前那笔被忽略的优势账（命中：统一数学框架 + 端到端闭环 + retrieval 以外·后训练；递进 08-17 的 PPO clipping，区分“GAE 决定信用方向”与“clip 限制策略步幅”；对应 `wiki/notes/2026-08-18-gae-advantage-bias-variance.md`）

## 2026-08-19
- 推送：从 GAE 到 GRPO——不用 Critic，不等于没有基线（命中：统一数学框架 + 端到端闭环 + retrieval 以外·后训练；递进 08-18 的优势估计，把 critic 的跨时间基线与同题组内基线放进同一控制变量框架；对应 `wiki/notes/2026-08-19-grpo-group-relative-baseline.md`）

## 2026-08-21
- 推送：GRPO 的长度偏置——一句序列奖励如何在 token 级更新里改写目标（命中：统一数学框架 + 端到端闭环 + retrieval 以外·后训练；递进 08-19 的组内基线，区分 per-sequence 与 per-token 归一化及信用稀释；对应 `wiki/notes/2026-08-21-grpo-length-bias-token-policy-gradient.md`）
