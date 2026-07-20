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
- [x] 数据和参数怎么分钱：Chinchilla 与 scaling laws（arXiv 2203.15556） | 命中薄弱点：retrieval 以外·预训练 + 端到端闭环·数据环节 | 切入角度：整篇论文就是一个约束优化问题——给定算力预算，损失对 N 和 D 的分配怎么解 | pushed 2026-07-16
- [x] 你的评测集是从哪个分布采的：benchmark 失效的三种方式（contamination / Goodhart / 分布漂移） | 命中薄弱点：端到端闭环·评测环节 + 主线·模型评估（递进 07-12 的偏差传导） | 切入角度：评测这一环怎么骗人，以及为什么线上指标和离线指标会打架 | pushed 2026-07-17
- [x] RLHF 之后：DPO / KTO / GRPO 一张家谱 | 命中薄弱点：retrieval 以外·后训练（递进 MLE→DPO） | 切入角度：每个方法都是在「reward 从哪来」「KL 锚在哪」两个轴上挪位置，一张图讲完演化逻辑 | pushed 2026-07-18
- [x] SPLADE 的 MLM head 到底怎么给一个词打分：从 30K 维 logits 到稀疏权重（arXiv 2109.10086 / DistilSPLADE） | 命中薄弱点：RAG / 检索 / Embedding 主线（直接回应用户 07-18 的追问，深度递进 07-15 SPLADE 的「表示放哪」到「权重怎么算出来的」） | 切入角度：07-15 讲了 SPLADE 把语义投回词表，但没拆开打分公式——对每个输入 token 位置 j，BERT 的 MLM head 都吐一条 30522 维 logit（本质是「这个位置最像词表里哪个词」的完形填空分布）；SPLADE 对每个词项 i 取所有位置上 log(1+ReLU(w_ij)) 的 max，ReLU 砍负分保非负、log 压住高频词的过度膨胀、跨位置 max 让「文中任一处点亮该词」即得分——于是「打分」本质是复用预训练的完形填空能力，再靠 FLOPS 正则把 30K 维里绝大多数压成 0，讲清这条 logit→权重的链路而非复述 sparse-retrieval 概念页 | pushed 2026-07-19
- [x] Agent 的多步闭环：误差在 tool-call 循环里怎么复合（ReAct 的推理-行动-观察 vs 单步预测） | 命中薄弱点：端到端闭环·偏差传导 + 主线·Agent/工具使用/上下文工程（递进 07-12 的偏差传导，补队列里缺席的 Agent 主线） | 切入角度：单步 LLM 的误差彼此独立，但 agent 把上一步输出喂回下一步输入形成闭环，误差不再独立而是逐步复合——讲清 ReAct 每一环（推理/行动/观察）在哪里注入偏差、为什么长 horizon 任务成功率随步数近似指数衰减，以及 context engineering 究竟是在这条链的哪一环做拦截，而非泛泛复述 agent 概念页 | pushed 2026-07-20
- [ ] 【交叉·AlexNet × Attention】两次架构革命都守着同一条边界：让出「路径」、钉死「指南针」 | 命中薄弱点：端到端闭环·评测环节 + 主线·模型评估（递进 07-12 的偏差传导） | 切入角度：AlexNet 把「特征该长什么样」、Transformer 把「序列结构先验」都交给数据自己长，但两者都没敢让出损失/评价标准这根锚——而今天 LLM-as-judge / RLAIF 正在史上第一次尝试让权「指南针」本身，所以当下的评测危机无先例可抄
- [ ] 投机解码：用小模型猜、大模型一次并行验，把自回归的串行债还上（Speculative Decoding, arXiv 2211.17192 / Medusa 2401.10774） | 命中薄弱点：retrieval 以外·推理系统（递进 07-14 的 KV cache，同属"为什么生成慢"但换一条账） | 切入角度：07-14 算的是"显存账"，这条算"延迟账"——自回归每步都得串行等上一个 token 落地，投机解码让 draft 模型一次猜 k 个、大模型一次前向并行验证，把 memory-bound 的逐 token 解码改写成 compute-bound 的批量验证；讲清"为什么验证比生成便宜""接受率如何决定加速比上限"，而非复述解码采样概念页
- [ ] late interaction 与 MUVERA：把 query-doc 交互推迟到检索时的第三条召回路（ColBERT arXiv 2004.12832 / MUVERA 2405.19504） | 命中薄弱点：RAG / Embedding 主线（递进 07-15 SPLADE 的"表示放哪、用谁检索"，补齐 dense/sparse 之外缺席的第三轴，方向与近期 colbert/muvera 页活跃连接一致） | 切入角度：dense 把一句话压成一个向量、SPLADE 压回 30K 词表，两者都在 query 编码阶段就把交互算完；late interaction 反过来保留每个 token 的向量、把匹配推迟到检索时逐 token 做 MaxSim，用精度换存储；MUVERA 再用 Fixed Dimensional Encoding 把多向量塌回单向量、拿现成 MIPS 找回大部分精度。用"交互推迟到哪一步"这一根轴把三种召回排成一条谱，讲清各自把语义交互挪到了链条的哪一环，而非复述 colbert 概念页
- [ ] Self-RAG / CRAG：把「要不要检索、检索得对不对」交给模型自己决策（Self-RAG arXiv 2310.11511 / CRAG 2401.15884） | 命中薄弱点：RAG / 检索主线 + 主线·Agent/上下文工程（连接度信号：self-rag 概念页近期被 CRAG 等新页高频链接、方向活跃；递进 07-15/07-19 SPLADE 的「怎么检索」到「何时检索、检索错了怎么办」） | 切入角度：前面几条讲的都是召回机制（sparse / late interaction 把语义放哪、分数怎么算），这条换一根轴——把检索从固定管线升级成模型的一个可决策动作：Self-RAG 用 reflection token 让模型边生成边自评「此处要不要检索」「retrieved 段落是否支持当前句」，CRAG 再挂一个轻量评估器给检索质量打分、触发「采用 / 丢弃 / 网络补检」三态；讲清 RAG 从静态拼接走向 agentic 自纠的这一步、误差在链条哪一环被拦下，正好把 RAG 主线接到 Agent 主线上，而非复述 self-rag 概念页
