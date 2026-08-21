# 当前主线（Current Focus）

> 供 hermes 每日选片、Claude 挖掘薄弱点、每周分诊使用。每周日复盘时更新。
> 最后更新：2026-08-20

## 主线方向（推送内容优先落在这三个圈内）

1. **RAG / 检索 / Embedding**
2. **Agent / 工具使用 / 上下文工程**
3. **模型评估**

## 薄弱点（选片时优先补这些，可跨主线）

> 每条带「最后确认」日期：当反馈或新增 [[链接]] 表明它仍是薄弱点时由挖掘刷新；
> 超过 3 周无任何支持，healthcheck 会提醒降权或移除——薄弱点也有半衰期。

- **统一数学框架**（最后确认：2026-08-15）：用一个框架理解各种 loss 和训练目标
  （MLE、对比学习、RLHF/DPO 的目标函数同源关系），而不是逐个记方法
  （07-30/07-31 伴读 + 新建 [[probability-calibration]] 把 proper scoring rule 的
  excess risk=KL(q||p) 与 MLE/NLL/交叉熵首次系统同源，并把训练端 KL 锚[[dpo]]
  与评测端 KL 尺接成同一散度的两副面孔；08-04 反哺再把这副「锚 vs 尺」的双面性
  正式写进 [[dpo]] 概念页本身——KL 不在 DPO 里消失而是被折进损失、β=锚绳松紧；
  08-05 反哺补上第三副面孔——把此前无任何概念页反链的 07-13 [[2026-07-13-infonce-vs-kl]]
  接进 [[dpo]]，KL 在蒸馏/构造端当「目标」（InfoNCE=one-hot KL、蒸馏=软分布 KL，主动最小化），
  与「锚」「尺」凑成同一散度沿闭环三工位的三副面孔，直接为待推的【交叉·KL 三副面孔】pick
  垫好概念层；08-13 反哺再把这副 log-loss/KL 骨架从评测端扩到奖励建模端——[[rlhf]] 的 Bradley-Terry
  偏好损失 −log σ(r_w−r_l) 本质是一条 proper scoring rule（σ(Δr)=RM 诚实报告的偏好概率、与
  [[probability-calibration]] 的 log loss 同形），并点明奖励黑客=RM 训得太诚实、只对标注者偏好分布诚实而非
  业务真相，同一副骨架再跨「后训练奖励建模」一站；08-15 反哺再把 KL 三副面孔的合成从 [[dpo]] 补齐到评测锚点页
  [[probability-calibration]] 本身——该页此前只写「锚+尺」两副面孔、且从未反链 07-13 [[2026-07-13-infonce-vs-kl]]，
  现补上「目标」（蒸馏/构造端 InfoNCE=one-hot KL、KD=软分布 KL 主动最小化）那一副，把同一个 KL(q‖p) 在闭环三工位换岗
  写进本就统摄 MLE/NLL/CE/KL/properness 的这页、并为 pending 的【交叉·KL 三副面孔】pick 从校准侧垫好概念层，新增链接支持该薄弱点仍活跃）
- **端到端闭环**（最后确认：2026-08-19）：数据 → 采样 → 目标函数 → 评测 → 线上分布，
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
  稀疏 exact-match 因无此学习目标错位而能当身份锚兜底（＝三处修法的词表层第一处）；
  08-09 反哺再把同一根「训练分布↔使用分布错位」轴推进一层——[[sparse-retrieval]] 首链 [[2026-07-19-splade-mlm-head-term-scoring]]/[[2026-07-15-splade-learned-sparse-retrieval]]，
  拆开 SPLADE 打分链（w_i=max_j log(1+ReLU(s_ij)) 三闸、权重非概率、FLOPS 正则造稀疏），并点出效率轴上的孪生错位——FLOPS 训练代理≠真实 P99 延迟，与相关性轴的 semantic-similarity↔retrieval-relevance 错位同骨架（皆 reward-hacking 形）；
  08-12 反哺再把这几处散落的错位收成一根显式脊——[[benchmark-evaluation]]（自 07-31 零更新的评测枢纽页）新增「Goodhart 不是评测专属」一节，
  把 Goodhart/reward overoptimization/SPLADE FLOPS 错位/语料污染抽象成同一副「真目标 T 昂贵不可观测→各站改优化可测代理 S→压力足够则 S↑/T↓」骨架在闭环四站（数据·预训练/后训练/检索/评测）的四身衣服，
  点明评测端只是最后一站读数、危险在于它把前几站错位聚合成一个上线决策写回数据环，防御在四站同构＝周期性回锚 T（隐藏 holdout/gold reward/真实 P99/下游离线集），
  首链 [[2026-07-18-dpo-kto-grpo-family]]/[[2026-07-19-splade-mlm-head-term-scoring]] 两处训练站代理错位；
  08-16 反哺再把「便宜提议+核验」这副可靠性骨架跨子系统接通——[[self-rag]] 首链 07-23 投机解码，
  点明 Self-RAG/CRAG 的 retriever→verifier 与投机解码的 draft→target 是同一副 propose-verify 骨架、
  分界只在核验器是「精确规则」（投机解码拒绝采样无损）还是「会被优化的学习判据」（ISSUP 只压概率、退回 [[benchmark-evaluation]] 的谁核验核验器），
  self-rag↔[[llm-inference-serving]] 两个此前未交叉的子系统首次接通；
  08-17 反哺再把 compaction 这道保险丝从「抽象手段」落到生产实现——[[context-engineering]] 首链 07-26 Grok Build 审查，
  据两阶段 compaction（prefire 异步预烧 + fingerprint 失效）补出全页新洞见：这道保险丝本身是一段有状态、会过期的缓存，
  预烧摘要 NOTE₁ 的最危险失效不是「摘错」而是「摘的是一段被 rewind 掉的历史」＝external-memory 那行「过期错误被永久化」在 compaction 内部复发，
  指纹失效＝把 durable-state 的失效规则搬进 compaction，同一副「拒绝把未验证聚合成已确认」骨架再添一层；
  08-18 反哺再把 08-16 建起的 propose-verify 骨架从「投机解码×Self-RAG 两子系统」扩到第三个子系统·检索精排——[[colbert-retrieval]] 首链 07-23 投机解码，
  点明 MUVERA 的 `FDE 粗召回→MaxSim 重排` 与 draft→target、retriever→verifier 同为「便宜有损提议器 + 昂贵精确核验器」，
  并补出该骨架的第二根轴（自 08-16「核验器是规则还是模型→无损 vs 概率」之外）：**核验器能否回到源头**——投机解码拒绝即从 target 残差重采（提议器只封顶速度）、MaxSim 只能在已召回 Top-K 内重排回不到全库（提议器封顶 recall@K 天花板），
  这正解释了 colbert 页早写下却未挂骨架的「MUVERA 成败看 recall@K 非代理分数误差」，并点明 CRAG 网络补检三态＝检索侧唯一的回源头通道，llm-inference-serving↔colbert 两子系统经此首次交叉；
  08-19 反哺再把这副 propose-verify 骨架补上检索级联最上游一站——[[sparse-retrieval]] 首链 07-23 投机解码/07-24 late-interaction，点明 SPLADE/BM25＝级联里最常见的第一级提议器，且因核验器回不到全库，提议器漏检永久丢失、其 recall 天花板＝整条链精度上限；
  由此把本页原本含糊的「混合检索＝两全其美」重接成骨架必需——稀疏（漏检来自 vocabulary mismatch）与 dense（漏检来自 semantic↔relevance 错位）是两台盲区正交的提议器，RRF 并联＝在 propose 阶段把召回天花板一次性顶够高（因核验器无法回源头挽回）；
  08-20 反哺再把这副 propose-verify 骨架推到它的边界一格——[[mixture-of-experts]] 首链 07-23 投机解码，点明 MoE 的 router 是一个 top-k 提议器却**在推理链上根本没有下游核验器**（token 被路由/加权合并直接成层输出，推理时既测不出也挽不回错路由），
  由此把 08-16/08-18 立起的两根轴推到极限并补出第三层「核验器的有无决定防御压在推理侧还是训练侧」——投机解码把风险交给推理时的精确核验、MoE 把风险交给训练时的负载均衡（auxiliary loss/capacity factor 不是修某次坏路由而是训练时压低系统性坍缩概率），
  这正解释了本页 07-29 终局问题「路由错了算检索失败/容量不足/目标错配」之难＝核验器缺席的结构后果，llm-inference-serving/self-rag/colbert↔mixture-of-experts 经此把 propose-verify 骨架接到预训练架构侧，新增链接支持该薄弱点仍活跃）
- **retrieval 以外的空缺**（最后确认：2026-08-10）：大模型预训练（数据配比、scaling、MoE 容量账）、
  后训练（对齐方法演进）、推理系统（serving、KV cache、投机解码、吞吐/batching——已聚成 [[llm-inference-serving]]）
  （08-01 反哺把 07-29 MoE 伴读接进 [[mixture-of-experts]]——N_total/N_active 解耦、两笔账、
  router=内部参数检索器的 MoE↔RAG 同构、Chinchilla 四变量账本；
  08-02 反哺把 07-28 continuous batching 伴读回填进 [[llm-inference-serving]] 的「吞吐账」占位——
  iteration-level scheduling/槽位-迭代账/与 PagedAttention 正交/三本账相乘，
  推理系统三本账（显存·延迟·吞吐）至此在概念层补齐；
  08-07 反哺再把预训练侧补上一处——把 07-16 Chinchilla 伴读接进 [[scaling-laws]]（该页此前把「20:1」写成事实、无任何伴读反链），
  抬成「约束优化+边际收益相等」骨架，D≈有效信息代理量与 RAG 的 k≈有效证据同构、三种「最优」分层、诊断表落地，
  为待推的【预训练数据配比】pick 垫好 D 轴概念层；
  08-10 反哺再把后训练·对齐方法演进补上一处——把 07-18 DPO/KTO/GRPO 家谱伴读接进 [[rlhf]]（该页自 05-14 零更新、无任何伴读反链），
  抬成「共同祖先=奖励减漂移、DPO/KTO/GRPO 在 reward 来源/KL 锚/数据何时产生 三根正交轴上各挪位」的家谱骨架，
  点明 DPO/KTO 改「反馈→损失」接口、GRPO 改「在线 RL 优势估计（组内基线替 critic）」是正交两步、选型首选数据闭环而非损失函数，
  并把终局问题（reward/policy/judge 共漂、KL 只锚一条边）交叉链到 [[benchmark-evaluation]]，新增链接支持该薄弱点仍活跃）

## hermes 每日推送规则

0. **先过一篇一反馈门禁**：读取 `companion-log.md` 最近一篇已推送文章所在日期段；
   只有该段已经记录用户明确“已读”，或针对该篇留下评论、追问、理解反馈，才允许继续。
   未通过时不消费 picks、不自选、不生成 note、不推送后续文章。不得用“无反馈”、
   wiki 连接度或时间流逝替代用户反馈。
1. **优先消费 `picks.md`**：门禁通过后，有 pending 条目就取第一条伴读推送，标记为 pushed
2. **队列空时自选**，门禁通过后形式不限：论文、书籍章节、经典文章、或直接用你自己的
   知识讲透一个概念/片段——只要命中薄弱点，不必依赖搜索。
   主题式讲解优于整篇转述，例如"从 MLE 到 DPO：目标函数的同源推导"这类切面
3. **不去重，但必须逐篇解锁**：薄弱点还在就继续推类似内容，但要换材料、换角度、递进深度。
   近期推送历史见 `companion-log.md`，用它来变化角度，而不是回避主题
4. 每次推送写明命中哪条主线/薄弱点（一句话）；伴读全文存入
   `wiki/notes/`（一天一篇），`companion-log.md` 记一行索引
