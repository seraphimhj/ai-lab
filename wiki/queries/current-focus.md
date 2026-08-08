# 当前主线（Current Focus）

> 供 hermes 每日选片、Claude 挖掘薄弱点、每周分诊使用。每周日复盘时更新。
> 最后更新：2026-08-08

## 主线方向（推送内容优先落在这三个圈内）

1. **RAG / 检索 / Embedding**
2. **Agent / 工具使用 / 上下文工程**
3. **模型评估**

## 薄弱点（选片时优先补这些，可跨主线）

> 每条带「最后确认」日期：当反馈或新增 [[链接]] 表明它仍是薄弱点时由挖掘刷新；
> 超过 3 周无任何支持，healthcheck 会提醒降权或移除——薄弱点也有半衰期。

- **统一数学框架**（最后确认：2026-08-05）：用一个框架理解各种 loss 和训练目标
  （MLE、对比学习、RLHF/DPO 的目标函数同源关系），而不是逐个记方法
  （07-30/07-31 伴读 + 新建 [[probability-calibration]] 把 proper scoring rule 的
  excess risk=KL(q||p) 与 MLE/NLL/交叉熵首次系统同源，并把训练端 KL 锚[[dpo]]
  与评测端 KL 尺接成同一散度的两副面孔；08-04 反哺再把这副「锚 vs 尺」的双面性
  正式写进 [[dpo]] 概念页本身——KL 不在 DPO 里消失而是被折进损失、β=锚绳松紧；
  08-05 反哺补上第三副面孔——把此前无任何概念页反链的 07-13 [[2026-07-13-infonce-vs-kl]]
  接进 [[dpo]]，KL 在蒸馏/构造端当「目标」（InfoNCE=one-hot KL、蒸馏=软分布 KL，主动最小化），
  与「锚」「尺」凑成同一散度沿闭环三工位的三副面孔，直接为待推的【交叉·KL 三副面孔】pick
  垫好概念层，新增链接支持该薄弱点仍活跃）
- **端到端闭环**（最后确认：2026-08-08）：数据 → 采样 → 目标函数 → 评测 → 线上分布，
  这条链怎么连通、每一环的偏差如何传导（07-25 伴读把「过早聚合抹掉少数信号」在编码端与评测端打通、
  评测偏差经选模反向注入数据环——已聚成 [[benchmark-evaluation]]；07-26 把检索端也接上——
  SPLADE 词表维/[[colbert-retrieval|ColBERT]] MaxSim 是「拒绝过早聚合」在召回环的同构修法；
  07-27 反哺把病灶接回 dense 编码端本身——[[dense-passage-retrieval|DPR]] 单向量瓶颈=编码端的过早聚合，
  「交互推迟到哪一步」这根轴把 dense/sparse/late-interaction 串成同一病灶的三处修法；
  07-30 再把病灶接进 Agent 侧——[[react-agent|ReAct]] 的 context 压缩把「未验证」聚合成「已确认」，
  是同一病灶在时间维/记忆环的第四处发作，分栏账本=拒绝过早聚合在 Agent 记忆上的同构修法；
  07-31 再补上闭环的目标环节——[[probability-calibration]] proper scoring rule 只保证 p 追向
  「被评分的标签分布」，标签有噪声/judge 有偏时「目标一旦错了，优化越成功越稳定地学错」，
  ECE 整体平均又与编码/评测端过早聚合同构；
  08-03 反哺把 07-27 firebreak 伴读接进 [[context-engineering]]——四道保险丝按「切断哪类故障、错误能传多远」重排成故障域设计，
  与分布式系统的 checkpoint/bulkhead/lazy-loading/durable-state 同构，把「偏差传导」从『误差从哪注入』翻到『误差传播半径与恢复路径』这根可靠性轴；
  08-06 反哺再把这根「故障域/保险丝」轴接进检索环——[[self-rag]] 从「机制清单」抬成 Self-RAG ISSUP 与 CRAG evaluator 两处不同保险丝
  （拦『答案越过证据边界』vs 拦『坏证据进上下文』），接住 07-20 误差复合、与 07-27 故障域设计同构，四类反思判断不可压成一个 confidence＝07-25 拒绝过早聚合在检索控制流的复现；
  08-08 反哺再把「偏差从哪注入」补上编码环最上游的一处——[[sparse-retrieval]] 首链 [[2026-07-22-embedding-entity-mismatch]]，
  点明 dense embedding「按 semantic-similarity 训练、当 retrieval-relevance 用」是一次训练分布↔使用分布错位，实体 mismatch=该错位在实体敏感查询上的发作，
  稀疏 exact-match 因无此学习目标错位而能当身份锚兜底（＝三处修法的词表层第一处），新增链接支持该薄弱点仍活跃）
- **retrieval 以外的空缺**（最后确认：2026-08-07）：大模型预训练（数据配比、scaling、MoE 容量账）、
  后训练（对齐方法演进）、推理系统（serving、KV cache、投机解码、吞吐/batching——已聚成 [[llm-inference-serving]]）
  （08-01 反哺把 07-29 MoE 伴读接进 [[mixture-of-experts]]——N_total/N_active 解耦、两笔账、
  router=内部参数检索器的 MoE↔RAG 同构、Chinchilla 四变量账本；
  08-02 反哺把 07-28 continuous batching 伴读回填进 [[llm-inference-serving]] 的「吞吐账」占位——
  iteration-level scheduling/槽位-迭代账/与 PagedAttention 正交/三本账相乘，
  推理系统三本账（显存·延迟·吞吐）至此在概念层补齐；
  08-07 反哺再把预训练侧补上一处——把 07-16 Chinchilla 伴读接进 [[scaling-laws]]（该页此前把「20:1」写成事实、无任何伴读反链），
  抬成「约束优化+边际收益相等」骨架，D≈有效信息代理量与 RAG 的 k≈有效证据同构、三种「最优」分层、诊断表落地，
  为待推的【预训练数据配比】pick 垫好 D 轴概念层，新增链接支持该薄弱点仍活跃）

## hermes 每日推送规则

1. **优先消费 `picks.md`**：有 pending 条目就取第一条伴读推送，标记为 pushed
2. **队列空时自选**，形式不限：论文、书籍章节、经典文章、或直接用你自己的
   知识讲透一个概念/片段——只要命中薄弱点，不必依赖搜索。
   主题式讲解优于整篇转述，例如"从 MLE 到 DPO：目标函数的同源推导"这类切面
3. **不去重**：薄弱点还在就继续推类似内容，但要换材料、换角度、递进深度。
   近期推送历史见 `companion-log.md`，用它来变化角度，而不是回避主题
4. 每次推送写明命中哪条主线/薄弱点（一句话）；伴读全文存入
   `wiki/notes/`（一天一篇），`companion-log.md` 记一行索引
