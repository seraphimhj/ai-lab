# 选片队列（Picks）

> Claude（本地/工作机）基于 companion-log 和 current-focus 挖掘后写入。
> hermes 每日取第一条 pending 伴读推送，推送后把状态改为 pushed。

<!-- 每条格式：
- [ ] 材料/主题 | 命中薄弱点：xxx | 切入角度：一句话
  推送后改为：
- [x] 材料/主题 | 命中薄弱点：xxx | 切入角度：一句话 | pushed YYYY-MM-DD
-->

## 队列

- [x] InfoNCE 与 KL loss 同时学习冗余吗：判别式排序 vs 生成式对齐的分工（SimCLR / Sentence-BERT / E5） | 命中薄弱点：统一数学框架（递进 07-12 的 MLE→DPO，直接回应用户 07-12 的开放提问） | 切入角度：InfoNCE 把正负样本拉开相对排序、KL/交叉熵把预测对齐到目标分布——同是 softmax 交叉熵骨架下的两种监督信号，讲清何时冗余、何时互补，接上 RAG/Embedding 主线 | pushed 2026-07-13
- [x] 为什么生成比训练慢：KV cache 的内存账 + PagedAttention（vLLM, arXiv 2309.06180） | 命中薄弱点：retrieval 以外·推理系统 | 切入角度：先算一笔 70B 模型单条请求的显存账，再看 vLLM 把浪费的 60-80% 显存怎么拿回来 | pushed 2026-07-14
- [x] SPLADE：把「查询扩展」学进模型的稀疏召回（arXiv 2109.10086） | 命中薄弱点：RAG / Embedding 主线（直接回应用户 07-13 的显式请求，递进 07-13 的 InfoNCE/dense 讨论） | 切入角度：dense 和 sparse 的分界不在效果而在「表示放哪、用谁来检索」——SPLADE 用 BERT 的 MLM head 把语义扩展写回 30K 维词表、继续用倒排索引检索，讲清它和 dense embedding 各自把语义压到哪一层，而非复述 sparse-retrieval 概念页 | pushed 2026-07-15
- [ ] 数据和参数怎么分钱：Chinchilla 与 scaling laws（arXiv 2203.15556） | 命中薄弱点：retrieval 以外·预训练 + 端到端闭环·数据环节 | 切入角度：整篇论文就是一个约束优化问题——给定算力预算，损失对 N 和 D 的分配怎么解
- [ ] 你的评测集是从哪个分布采的：benchmark 失效的三种方式（contamination / Goodhart / 分布漂移） | 命中薄弱点：端到端闭环·评测环节 + 主线·模型评估（递进 07-12 的偏差传导） | 切入角度：评测这一环怎么骗人，以及为什么线上指标和离线指标会打架
- [ ] RLHF 之后：DPO / KTO / GRPO 一张家谱 | 命中薄弱点：retrieval 以外·后训练（递进 MLE→DPO） | 切入角度：每个方法都是在「reward 从哪来」「KL 锚在哪」两个轴上挪位置，一张图讲完演化逻辑
- [ ] Agent 的多步闭环：误差在 tool-call 循环里怎么复合（ReAct 的推理-行动-观察 vs 单步预测） | 命中薄弱点：端到端闭环·偏差传导 + 主线·Agent/工具使用/上下文工程（递进 07-12 的偏差传导，补队列里缺席的 Agent 主线） | 切入角度：单步 LLM 的误差彼此独立，但 agent 把上一步输出喂回下一步输入形成闭环，误差不再独立而是逐步复合——讲清 ReAct 每一环（推理/行动/观察）在哪里注入偏差、为什么长 horizon 任务成功率随步数近似指数衰减，以及 context engineering 究竟是在这条链的哪一环做拦截，而非泛泛复述 agent 概念页
- [ ] 【交叉·AlexNet × Attention】两次架构革命都守着同一条边界：让出「路径」、钉死「指南针」 | 命中薄弱点：端到端闭环·评测环节 + 主线·模型评估（递进 07-12 的偏差传导） | 切入角度：AlexNet 把「特征该长什么样」、Transformer 把「序列结构先验」都交给数据自己长，但两者都没敢让出损失/评价标准这根锚——而今天 LLM-as-judge / RLAIF 正在史上第一次尝试让权「指南针」本身，所以当下的评测危机无先例可抄
