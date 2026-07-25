# 伴读日志（Companion Log）

> hermes 每日追加：当天推送了什么 + 昨天推送收到的用户反馈。
> Claude 每周读这里挖掘新薄弱点。只追加，不修改历史。

<!-- 每条格式：
## YYYY-MM-DD
- 推送：主题/材料（命中：哪条主线或薄弱点）
- 反馈：用户对上一次推送的反应要点——追问了什么、哪里卡壳、
  说了"已懂"还是"没讲透"、有没有提出新问题。没有反馈就写"无反馈"。
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
