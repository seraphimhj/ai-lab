# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-05-05] create | Wiki initialized
- Domain: AI/ML (LLM, Agent, Deep Learning, RAG, AI Engineering)
- Wiki path: ~/workspace/ai-lab/wiki
- Structure created with SCHEMA.md, index.md, log.md
- Subdirectories: raw/{articles,papers,transcripts,assets}, entities, concepts, comparisons, queries, _archive

## [2026-05-05] ingest | 7张图搞懂Claude Code的Harness架构设计
- Source: 微信公众号「诗与沅方」(FloraCat), 2026-04-03
- Raw: raw/articles/claude-code-harness-architecture-2026.md
- Created entities: claude-code
- Created concepts: claude-code-harness, agent-loop-taor, claude-code-memory-system, claude-code-state-management
- Key takeaways: Claude Code 采用 Harness 三层架构统一多入口、TAOR 循环执行、LLM 驱动的文件级记忆选择（非传统 RAG）

## [2026-05-05] ingest | 独家对话罗福莉：AI范式已然巨变！（张小珺访谈）
- Source: 微信公众号「语言即世界language is world」+ 小宇宙播客（张小珺 × 罗福莉）, 2026-04-24
- Audio: raw/assets/luo-fuli-interview-2026.m4a (200MB, 217min)
- Raw transcript: raw/transcripts/luo-fuli-interview-zhangxiaojun-2026.md
- Created entities: luo-fuli, mimo-v2
- Created concepts: agent-paradigm-shift
- Created comparisons: openclaw-vs-claude-code
- Updated entities: claude-code (补充 OpenClaw 对比链接)
- Key takeaways: Chat→Agent 范式转移、1T 模型入场券、卡比例 3:5:1→3:1:1、RL scaling for Agent、Hybrid Attention+MTP vs MLA、平权组织有利于创新、两年内可能 AGI

## [2026-05-05] ingest | 下一代Attention算法改进的猜想（张小珺 × 杨松琳）
- Source: 微信公众号「语言即世界language is world」, 2025-11-10
- Raw: raw/articles/attention-algorithm-innovation-2025.md
- Created entities: yang-songlin
- Created concepts: linear-attention, hybrid-attention, sparse-attention
- Created comparisons: hybrid-vs-sparse-attention
- Updated entities: mimo-v2（补充 Hybrid Attention 3:1 比例、多跳推理弱点、交叉链接）
- Key takeaways: Linear Attention 发展脉络（RetNet→GLA→Delta Net→KDA）、Hybrid 3:1 共识、Sparse vs Linear 核心区别（FLOPs vs KV Cache）、中国因算力有限倒逼算法创新、下一突破点在 Attention

## [2026-05-05] ingest | 为 Agent 设计产品【译】
- Source: Teddy Riker (Ramp), 译者 宝玉 (公众号 宝玉AI), 2025
- Original: https://x.com/teddy_riker/status/2047312986696454584
- Raw: raw/articles/designing-for-agents-2025.md
- Created concepts: agent-product-design, agent-feedback-loop, agent-context-gap
- Key takeaways: 80/20 法则翻转（80% 交互通过 Agent）、三代交互模型演进（UI→Agent→Agent-to-Agent）、教会智能体成功（运行时交付规范）、反馈循环（rationale+反馈工具+context seeding）、上下文缺口（索要上下文而非索要答案）

## [2026-05-10] create | 批量创建 24 个实体页（16 模型 + 8 机构）
- Created model entities: transformer-architecture, bert, gpt-3, gpt-4, llama, deepseek, qwen, mistral-7b, mixtral, gemma, yi-model, mamba, palm, phi, glm, clip
- Created org entities: openai, google-deepmind, anthropic, meta-ai, microsoft-research, alibaba-qwen, baidu, nvidia-research
- Each page: frontmatter (title/created/updated/type/tags/sources), 中文正文, 2+ wikilinks, 50-150 行
- Updated index.md: 新增实体分类（模型/机构/人物），更新页面计数
- Preserved existing pages: claude-code, luo-fuli, yang-songlin, mimo-v2

## [2026-05-10] ingest | LLM 论文批量入库（72 篇 arxiv 摘要）
|- Raw directory: raw/papers/ (72 files, ~150KB total)
|- 经典 LLM 论文: Attention, BERT, GPT-3, Scaling Laws, CLIP, Chinchilla, PaLM, InstructGPT, CoT, CAI, FlashAttention, LoRA, LLaMA 1/2, GPT-4, DPO, GPTQ, AWQ, Mamba, ReAct, Tree of Thoughts, Toolformer 等
|- 近一年论文: DeepSeek-V2/V3/R1, Llama 3, Mistral 7B, Mixtral, Gemma, Yi, Qwen, GLM, FlashAttention-3, Jamba, Griffin, Mamba-2, YaRN, LongLoRA, Ring Attention 等
|- RAG 论文: RAG 原论文, REALM, Self-RAG, CRAG, Adaptive-RAG, GraphRAG, DPR, ColBERT, SPLADE, BGE M3, MTEB 等
|- Embedding 论文: Sentence-BERT, E5, GTE, NV-Embed v1/v2, MTEB, Qwen3-Embedding, Jina v5 等
|- 清理了约 34 篇错误 arxiv ID 指向的非 LLM 论文

## [2026-05-10] create | 批量创建 20 个概念页 + 5 个对比页
|- 概念页 (concepts/):
  - 训练与对齐: rlhf, dpo, constitutional-ai, instruction-tuning, lora
  - 推理与提示: chain-of-thought, tree-of-thoughts, in-context-learning
  - 效率优化: flash-attention, model-quantization, mixture-of-experts, scaling-laws
  - RAG/检索: retrieval-augmented-generation, dense-passage-retrieval, colbert-retrieval, self-rag, graph-rag
  - Agent/工具: react-agent, tool-use
  - Embedding: text-embedding
|- 对比页 (comparisons/):
  - embedding-models-2025: MTEB 排名对比（Qwen3-Embedding-8B 75.22 #1, Harrier 74.3, Jina v5 71.7）
  - open-source-llm-comparison: LLaMA/Qwen/DeepSeek/Mistral/Gemma/Yi/Phi 全面对比
  - rlhf-vs-dpo: 对齐方法对比
  - rag-approaches: 6 种 RAG 架构对比
  - quantization-methods: GPTQ/AWQ/SparseGPT/GGUF 对比
|- Updated index.md: 分类重组，总计 66 页（28 entities + 31 concepts + 7 comparisons）
|- Preserved existing pages: 11 concepts, 2 comparisons

## [2026-05-14] ingest | LLM 与 Agent 核心原理全面解析
- Source: 微信公众号文章, https://mp.weixin.qq.com/s/i3yKCZCUtDkTrk4hFZz7NQ
- Raw: raw/articles/llm-agent-core-principles-2026.md
- Created concepts: mcp-model-context-protocol, context-engineering, agent-skills
- Updated concepts: chain-of-thought（推理模型演进+思考强度参数范式）, react-agent（Agent = LLM+Tool+Loop 简化理解）
- Updated index.md: +3 concepts, page count 66→69
- Key takeaways: MCP 标准化工具接口、上下文工程是 Agent 工程的核心、推理模型从双模型走向单模型+思考强度参数、Skills 渐进式披露设计

## [2026-05-14] ingest | raw/papers/ 全量论文入库（70+ 篇 → wiki 充实）
- Source: raw/papers/ 目录 70+ 篇 arxiv 论文 HTML/PDF
- Created concepts (4):
  - test-time-compute: 推理时计算缩放（2408.03314 Snell et al.）
  - long-context-extension: 长上下文扩展技术（YaRN/LongLoRA/Ring Attention）
  - code-generation: 代码生成模型（StarCoder 2305.06161）
  - sparse-retrieval: 学习型稀疏检索（SPLADE 2109.10086）
- Updated entities (3):
  - gpt-3: 增加 Scaling Laws 验证、InstructGPT/RLHF 后续、交叉链接
  - llama: 充实 LLaMA 2 对齐细节、LLaMA 3 多模态/工具使用/128K 上下文
  - deepseek: 充实 V2 MLA KV Cache 压缩数据、V3 训练成本/FP8/MTP、R1 GRPO 细节/Aha Moment/蒸馏版本
- Updated concepts (7):
  - flash-attention: 补充 Ring Attention 关联、长上下文基础设施角色
  - retrieval-augmented-generation: 增加 REALM/RETRO 历史演进、稀疏检索分支
  - text-embedding: 充实 BGE-M3/NV-Embed/Qwen3-Embedding/Jina v5 详情
  - scaling-laws: 增加 test-time-compute 交叉链接
  - rlhf: 充实摘要 RLHF/InstructGPT/HH-RLHF/GRPO 变体细节
  - constitutional-ai: 增加 Red Teaming 论文关联
  - lora: 增加 LongLoRA 论文引用和长上下文链接
- Updated index.md: +4 concepts（test-time-compute, long-context-extension, sparse-retrieval, code-generation）, page count 69→73
- 论文覆盖情况：
  - 直接创建新页面：4 篇
  - 充实已有实体页：~15 篇（GPT-3/LLaMA 1-3/DeepSeek LLM/V2/V3/R1 等）
  - 充实已有概念页：~30 篇（FlashAttention 1-3, GPTQ/AWQ/SparseGPT, LoRA, RAG/REALM/RETRO, Scaling Laws/Chinchilla, RLHF 系列, Embedding 系列, SPLADE, YaRN/LongLoRA/Ring Attention, StarCoder 等）
  - 已通过已有页面覆盖（无需新页面）：~25 篇（Attention Is All You Need→transformer-architecture, BERT→bert, ReAct→react-agent, CoT→chain-of-thought, ToT→tree-of-thoughts, Toolformer→tool-use, Self-Instruct→instruction-tuning, DPO→dpo, Mixtral→mixtral, Mistral→mistral-7b, PaLM→palm, GLM→glm, Gemma→gemma, Yi→yi-model, Phi→phi, CLIP→clip, Mamba→mamba, GraphRAG→graph-rag, Self-RAG→self-rag, DPR→dense-passage-retrieval, ColBERT→colbert-retrieval, MoE→mixture-of-experts 等）

## [2026-05-15] ingest | raw/papers/ 全量论文入库 — 补全轮
- 新建概念页 (1):
  - swe-agent: 软件工程 Agent + ACI 界面设计（2405.15793）
- 充实实体页 (11):
  - gpt-4: 补充 RLHF/MMLU/Scaling Law 数据
  - mistral-7b: 完整架构参数表、SWA/GQA 细节
  - mixtral: 架构参数、47B/13B 参数说明、DPO 对齐
  - palm: 6T token/780B/6144 TPU v4、不连续涌现/CoT 发现
  - phi: phi-1.5 训练参数、数据策略细节
  - glm: INT4 量化/4×RTX3090 推理、超越 GPT-3 175B
  - clip: 400M WIT 数据集、对比学习效率 4x、ImageNet 76.2%
  - mamba: sources 格式修正 + 交叉链接
  - gemma: 完整架构参数（2B/7B）、6T token
  - yi-model: 3.1T token、<10K 微调指令、34B RTX4090 部署
  - qwen: sources 格式修正 + 交叉链接
- 充实概念页 (13):
  - dense-passage-retrieval: DPR Top-5 65.2% vs BM25 42.9%
  - colbert-retrieval: 170× speedup、14000× fewer FLOPs
  - chain-of-thought: PaLM 540B GSM8K 57% vs standard 18%、涌现 ~100B+
  - tree-of-thoughts: 双过程理论设计哲学
  - instruction-tuning: Flan-PaLM +9.4%、MMLU 75.2%
  - react-agent: ALFWorld +34%、WebShop +10%
  - tool-use: Toolformer 6.7B 超 GPT-3 + 新增 HuggingGPT 四阶段框架
  - self-rag: Self-RAG 7B/13B 超 ChatGPT + 新增 CRAG 纠正式 RAG
  - graph-rag: 百万 token 级数据集、map-reduce 模式
  - in-context-learning: GPT-3 175B 参数背景
  - mixture-of-experts: Mixtral 47B/13B、超 GPT-3.5/LLaMA-70B
  - linear-attention: 新增 Griffin 门控线性循环 + 局部注意力
  - hybrid-attention: 新增 Jamba Transformer-Mamba MoE 混合（52B/12B active, 256K ctx）
- 补充更新:
  - scaling-laws: 新增 Pythia 训练动态分析套件
  - rag-approaches: sources 格式修正 .md → .html
- Updated index.md: +1 concept（swe-agent）, page count 73→74
- 论文覆盖统计：raw/papers/ 全部 70+ 篇论文均已映射到 wiki 页面

## [2026-07-23] update | mining 反哺：伴读笔记回流概念层
- react-agent: 新增「误差在闭环里如何复合」章节（p^H 的相关误差来源、四类污染注入点、context engineering 五接口拦截、observability/diagnosability/recoverability 三判据），反向链接 [[2026-07-20-react-agent-error-compounding]]；顺手去掉重复的「论文实验数据」块；updated 2026-05-14 → 2026-07-23
- text-embedding: 新增「失败模式：实体 mismatch」章节（mean-pooling 淹没低频高信息 token、semantic similarity vs retrieval relevance、稀疏 exact-match / late interaction / entity-aware 难负例三条修法），反向链接 [[2026-07-22-embedding-entity-mismatch]]、交叉链 [[sparse-retrieval]] [[colbert-retrieval]]；updated → 2026-07-23
- picks: 补 1 条至 5 条 pending——「推理系统的第三本账·吞吐 / continuous batching」，凑齐推理系统三本账（显存 07-14 / 延迟 07-23 / 吞吐）
- current-focus: 刷新三条薄弱点「最后确认」（统一数学框架→07-18、端到端闭环→07-20、retrieval 以外→07-23），推理系统条目补「吞吐/batching」

## [2026-07-24] update | mining 反哺 + 新建推理服务概念页
- colbert-retrieval（反哺）: 新增「交互推迟到哪一步」统一轴 + 实体 mismatch 手算 + MUVERA/FDE 保相似度编译 + 延迟物化同构章节，反向链接 [[2026-07-24-late-interaction-muvera]]、补交叉链 [[sparse-retrieval]]；updated 2026-05-14 → 2026-07-24
- llm-inference-serving（新建）: 合并 07-14 KV cache/PagedAttention 与 07-23 投机解码两篇伴读笔记为「显存/延迟/吞吐三本账」概念页，含 PagedAttention 分页解法、投机解码接受率 α 闸门、判断框架，反向链接 [[2026-07-14-kv-cache-paged-attention]] [[2026-07-23-speculative-decoding-latency]]，交叉链 [[flash-attention]] [[model-quantization]] [[mixture-of-experts]] [[scaling-laws]]
- Updated index.md: +1 concept（llm-inference-serving，效率优化区）, page count 74→75（39→40 concepts）
- picks: 补 1 条至 5 条 pending——「MoE：参数量/计算量解耦的两笔账」（连接度信号 mixture-of-experts/scaling-laws 活跃，把推理账抬到架构容量层）
- current-focus: 刷新「retrieval 以外」最后确认 07-23 → 07-24（新建 inference-serving 页 + MoE pick 支持推理系统/预训练 gap 仍活跃），条目补 MoE 容量账并挂 [[llm-inference-serving]]

## [2026-07-25] update | mining 反哺 + 新建模型评估概念页
- benchmark-evaluation（新建）: 把三篇评测伴读（07-17 benchmark 失效三态 / 07-21 让权指南针·LLM-as-judge / 07-25 聚合抹掉少数信号）聚成「模型评估」主线首个概念页——benchmark 作为有限样本估计器、独立性/非适应性/代表性三支柱对应 contamination/Goodhart/drift、聚合掩盖关键切片、LLM-as-judge 共盲/迎合/自证三失效、评测身份证八问 + 四层评测栈、评测偏差经选模反向注入端到端闭环；反向链接 [[2026-07-17-benchmark-failure-distribution]] [[2026-07-21-path-and-compass]] [[2026-07-25-aggregation-erases-minority-signals]]，交叉链 [[text-embedding]] [[colbert-retrieval]] [[sparse-retrieval]] [[rlhf]] [[constitutional-ai]] [[scaling-laws]]
- text-embedding（反哺·硬性）: 在实体 mismatch 段后新增「更一般的病灶：过早聚合与可聚合性四问」——把 mismatch 还原为聚合病灶的编码端实例、点积的补偿性、可交换/可补偿/同质/线性效用四问、Goodhart 前置版与有损摘要类比，反向链接 [[2026-07-25-aggregation-erases-minority-signals]]、交叉链 [[benchmark-evaluation]]；updated 2026-07-23 → 2026-07-25
- Updated index.md: +1 concept（benchmark-evaluation，新增「模型评估」区）, page count 75→76（40→41 concepts）
- picks: 补 1 条至 5 条 pending——「LLM-as-judge 的系统性偏置与去偏」（递进 07-21/07-25，落到评委那本偏置账，pairs with 新建 benchmark-evaluation 页）
- current-focus: 刷新「端到端闭环」最后确认 07-20 → 07-25（07-25 伴读打通编码端/评测端聚合病灶 + 评测偏差反向注入数据环，已聚成 benchmark-evaluation 页）

## [2026-07-26] update | mining 反哺：聚合病灶接上检索端
- sparse-retrieval（反哺·硬性）: 新增「从『过早聚合』看稀疏检索：给否决型信号留独立账目」章节——把 SPLADE 词表维还原为「拒绝在编码端过早聚合」（实体命中落在独立维、不必先并进整体语义方向、不被话题相似度补偿），点明这是它在「精确匹配」栏对 dense 占优的机制根因；并加限定「推迟聚合≠永不聚合」（SPLADE 总分仍求和，硬约束需 lexical filter/entity linker 兜底）；把稀疏词表维 / ColBERT MaxSim / 评测端 slice 串成同一病灶三处同构修法。反向链接 [[2026-07-25-aggregation-erases-minority-signals]]，交叉链 [[dense-passage-retrieval]] [[colbert-retrieval]] [[benchmark-evaluation]] [[text-embedding]]；updated 2026-05-14 → 2026-07-26
- current-focus: 刷新「端到端闭环」最后确认 07-25 → 07-26（07-26 反哺把聚合病灶从编码端/评测端接到检索端，SPLADE 词表维/ColBERT MaxSim 是召回环的同构修法，新增链接支持该薄弱点仍活跃）
- picks: 队列已满 5 条 pending（Self-RAG/CRAG、上下文工程四拦截、吞吐 continuous batching、MoE 两笔账、LLM-as-judge 去偏），序列完整、无需微调，不动

## [2026-07-27] update | mining 反哺：过早聚合病灶接回 dense 编码端本身
- dense-passage-retrieval（反哺·硬性）: 新增「失败模式：单向量瓶颈不是『交互不够深入』而是一次不可逆的过早聚合」+「一根轴看清 DPR 的位置：交互被安排在链条哪一步」两节——把原表里含糊的「交互不够深入」拆成接口约束（passage 编码时不知未来 query、只能预揉异质信息进一个点、局部硬约束退化成可补偿特征），点明这是实体 mismatch 的编码端根因、且非 mean-pooling 独有（[CLS]/learned pooling 同受信息瓶颈）；用「交互发生在哪一步」轴把 dense/[[sparse-retrieval]]/[[colbert-retrieval]]/cross-encoder 串成同一病灶的四处修法，接上 MUVERA 保相似度编译与 dense→ColBERT 精排管线。反向链接 [[2026-07-24-late-interaction-muvera]]，交叉链 [[text-embedding]] [[benchmark-evaluation]]；顺手删去重复的 [[in-context-learning]] 关系行；updated 2026-05-14 → 2026-07-27
- current-focus: 刷新「端到端闭环」最后确认 07-26 → 07-27（07-27 反哺把「过早聚合抹掉少数信号」从检索端接回 dense 编码端本身，DPR 单向量瓶颈=编码端过早聚合，新增链接支持该薄弱点仍活跃）
- picks: 队列已满 5 条 pending（Self-RAG/CRAG、上下文工程四拦截、吞吐 continuous batching、MoE 两笔账、LLM-as-judge 去偏），序列完整、上周内已有交叉 pick（07-25 实体mismatch×benchmark），无需微调，不动

## [2026-07-28] update | mining 反哺：把上下文工程翻到「写权限」那一面
- context-engineering（反哺·硬性）: 该页此前从 2026-05-14 起未更新、无任何伴读反向链接，且近三日反哺全落在检索端（text-embedding/sparse/dense），本日转向 Agent 主线补链。新增「换个方向看：不是『塞多少』，而是『谁有写权限』」一节——把原页「本质都是往窗口塞信息」的填充量直觉翻面：多步闭环里决定成败的不是 token 数量而是错误信息能否拿到写权限，早期小偏差沿 [[react-agent]] 闭环自激放大；据此把上下文工程落成分布在五个接口的「写权限闸门」表（动作前 typed schema / 观察入窗前失败语义+不可信隔离 / 压缩时分栏账本 / 循环中 loop detector+重试预算 / 提交前可执行断言），并把原页开放问题里的「压缩 vs 精确填充 trade-off」重述为「压缩会不会把未验证压成已确认」、点出 observability/diagnosability/recoverability 三变量决定闭环收敛还是发散。反向链接 [[2026-07-20-react-agent-error-compounding]]；updated 2026-05-14 → 2026-07-28
- picks: 队列已满 5 条 pending（Self-RAG/CRAG、上下文工程四拦截、吞吐 continuous batching、MoE 两笔账、LLM-as-judge 去偏），序列完整、上周内已有交叉 pick（07-25 实体mismatch×benchmark），且本日 companion-log 无新反馈，无需微调，不动
- current-focus: 无明确反馈证据，薄弱点定义不动；「端到端闭环」07-27 刚确认、本日反哺属同一偏差传导轴的 Agent 侧补链，不重复刷新日期
- healthcheck: companion-log 静默 3 天（07-25 后无新条目、hermes 07-26/07-27 未推送 notes），已报 ERROR——反馈通道疑似停摆，本轮选片仅靠连接度替补信号，已提醒用户查 hermes cron

## [2026-07-29] update | mining 反哺：给 RAG umbrella 页补「交互推迟到哪一步」统一轴
- retrieval-augmented-generation（反哺·硬性）: 该页自 2026-05-14 起未更新、无任何伴读反向链接，且「检索方法」段一直是「稀疏/稠密/混合」的平铺菜单。近三日反哺已把「过早聚合/交互推迟到哪一步」这根轴分别接进 dense/sparse/colbert/text-embedding 四个下游页，本日把它上提到 RAG 伞页本身——新增「一根轴看清检索方法：query-doc 交互推迟到链条哪一步」一节，用一张谱表（DPR 单向量→SPLADE 词表维→ColBERT 逐 token MaxSim→cross-encoder 全交互）把散落的检索器按「交互在流水线哪一步算完」排成一条线，点明交互越早=doc 编码越是不可逆的过早聚合（低频实体被池化淹没）、越晚=保留信号维度越多但存储/延迟越贵，于是选检索器=用预算把交互往后推几步、Hybrid/多阶段是这条谱上的混搭；末尾接回「拒绝过早聚合」在评测端的同构修法（worst-group vs mean）。反向链接 [[2026-07-24-late-interaction-muvera]]，交叉链 [[dense-passage-retrieval]] [[sparse-retrieval]] [[colbert-retrieval]] [[text-embedding]] [[benchmark-evaluation]]；updated 2026-05-14 → 2026-07-29
- picks: 队列已满 5 条 pending（Self-RAG/CRAG、上下文工程四拦截、吞吐 continuous batching、MoE 两笔账、LLM-as-judge 去偏），序列完整、上周内已有交叉 pick（07-25 实体mismatch×benchmark），且 companion-log 自 07-25 起无新反馈/无新推送，无需微调，不动
- current-focus: 无明确反馈证据，薄弱点定义不动；本日反哺属「端到端闭环·过早聚合」同一轴的召回端补链（07-27 刚确认），不重复刷新日期
- healthcheck: companion-log 静默升至 4 天（ERROR）、hermes 自 07-25 后未推送任何 notes、picks 队列 5 条全无消费——本地 hermes agent 疑似连续 4 天停摆，反馈闭环中断，已再次提醒查 hermes cron status

## [2026-07-30] update | mining 反哺：把「过早聚合」病灶接进 Agent 记忆环
- react-agent（反哺·硬性）: 该页此前只从 07-20 note 讲了「误差沿闭环复合」，未与近一周 RAG/评测端系统梳理的「过早聚合抹掉少数信号」轴打通，且 07-25 那篇高价值交叉 note 尚未链入任何 Agent 页。本日在 context engineering 段后新增「Context 压缩：闭环里的第四处『过早聚合』」小节——把上表 Context 行的危险（摘要把未验证压成事实）还原为编码端单向量/评测端单指标同一病灶的第四处发作：history compaction 聚合一长段异质轨迹时丢掉的正是「谁贡献了、证据等级如何」，未验证假设/失败码/越权动作记录=这一环的少数信号；给出三处发作点对照表，点明「多塞 token 救不了长任务」是因为压缩把未验证与已确认聚合进同一层、硬约束退化成可被流畅叙述补偿的一项特征（同点积里实体维被话题相似度补偿）；修法同构——分栏账本(Goal/Facts带source/Hypotheses/Failures)对应检索端保留 token 向量/词表维、评测端 per-slice，checkpoint 重规划=时间维上的「先暴露失败切片再二次聚合」。反向链接 [[2026-07-25-aggregation-erases-minority-signals]]，并补建该页缺失的「伴读来源」段（列 07-20 / 07-25）；updated 2026-07-23 → 2026-07-30
- current-focus: 刷新「端到端闭环」最后确认 07-27 → 07-30（新增 react-agent×07-25 链接把「过早聚合」病灶从编码/评测/检索三端扩到 Agent 记忆环第四处，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 07-30
- picks: 队列已满 5 条 pending（Self-RAG/CRAG、上下文工程四拦截、吞吐 continuous batching、MoE 两笔账、LLM-as-judge 去偏），序列完整、上周内已有交叉 pick（07-25 实体mismatch×benchmark），本日反哺本身即一次概念交叉（Agent 记忆×聚合病灶），无需微调，不动
- healthcheck: companion-log 静默升至 5 天（ERROR）、hermes 自 07-25 后未推送任何 notes、picks 队列 5 条全无消费——本地 hermes agent 疑似连续 5 天停摆，9:00 伴读推送与反馈回收均中断，已通知用户查 hermes cron status

## [2026-07-31] create+update | mining 反哺：概率评测独立成页，把「统一数学框架」接进 proper scoring rule
- **create** concepts/probability-calibration.md: 07-30 calibration-vs-ranking 与 07-31 proper-scoring-rules 两篇同主题伴读笔记攒到 ≥2 篇、却无对应概念页（benchmark-evaluation 只讲「估计器失效/judge」，缺「分数语义」维），按 OS ⑥ 新建。骨架=区分/校准/决策效用三分（排序好-X->概率准-X->决策好、AUC 单调不变只测排序）；proper scoring rule 的激励相容 + Brier/log 的 excess risk 分解（(p-q)^2 与 KL(q||p)）把 MLE/NLL/交叉熵/KL/properness 收成同一对象的五个名字；ECE 分箱与「过早聚合掩盖子群」同构；校准≠决策效用（阈值来自代价）；proper 不保证目标分布对（端到端闭环边界、reward overoptimization）；temperature scaling 只改刻度不改排序。反向链接 [[2026-07-30-calibration-vs-ranking]] [[2026-07-31-proper-scoring-rules-honest-probabilities]]，交叉链 [[benchmark-evaluation]] [[dpo]] [[rlhf]] [[text-embedding]] [[scaling-laws]]；已入 index.md「模型评估」段
- **update** concepts/benchmark-evaluation.md（反哺·硬性）: 该页把 benchmark 当估计器却从未区分「估的是排序分数还是概率」。新增「分数是排序还是概率：估计器之前先问『在估计什么量』」一节——点明同一批输出兼作排序/概率/决策三道互不蕴含的题、单调变换下 AUC 不变而概率含义已坏、要评概率须用 proper scoring rule（excess risk=KL/平方距离，顺带收进 MLE/NLL/交叉熵/KL），并把 ECE 整体平均接回本页原有「聚合掩盖切片」坑；正文指向新页 [[probability-calibration]]。反向链接 [[2026-07-30-calibration-vs-ranking]] [[2026-07-31-proper-scoring-rules-honest-probabilities]]；updated 2026-07-25 → 2026-07-31
- current-focus: 刷新「统一数学框架」最后确认 07-18 → 07-31（07-30/07-31 两篇 + 今日新建页把 proper scoring rule 的 excess risk=KL 与 MLE/NLL/交叉熵 同源关系首次系统落进知识层、且把训练端 KL 锚[[dpo]]与评测端 KL 尺接成同一散度，新增链接明确支持该薄弱点仍活跃）；「端到端闭环」07-31 note 的「目标分布错了优化越成功越学错」是同一轴新节点，刷新 07-30 → 07-31；同步顶部「最后更新」→ 07-31
- picks: 队列 pending 仅剩 1 条（hermes 07-26~07-29 消费 4 条、07-30/07-31 队列见底转自选），补足至 5——新增 ①temperature/Platt scaling 校准修法（模型评估，直承 07-30/07-31 两篇「下一步线索」）②RLVR/GRPO 可验证奖励躲开 reward hacking（后训练，递进 07-18 DPO 家谱、换「奖励可验证性」轴）③预训练数据配比 mixture/dedup/质量过滤（预训练，补 07-16 Chinchilla 只算 N/D 数量、未及 D 的构成）④【交叉·KL 三副面孔】训练锚×评测尺×蒸馏（统一数学框架，串 07-18/07-31/07-13 三篇）
- healthcheck: Errors 0、companion-log 已补齐至 07-31（前几日日志记的 hermes 停摆已恢复、notes/ 有 07-30·07-31 两篇），反馈通道恢复正常；无 companion-log 静默报警。适应度榜 top=react-agent/context-engineering/sparse-retrieval（Agent+检索方向活跃），bottom=bert/vit 旧 paper note（notes/ 归 hermes，不动）

## [2026-08-01] update | mining 反哺：把 MoE 伴读接进概念页，拆开「参数量」这个词
- mixture-of-experts（反哺·硬性）: 该页自 2026-05-14 起未更新、无任何伴读反向链接，且「稠密 vs MoE」表把 MoE 写成几乎无代价的胜利（「推理速度：快」）。据 07-29 伴读新增「解耦的边界：一条收益、两笔账」一节——把「参数多」拆成 N_total（容量/权重驻留）与 N_active（每-token FLOPs），点明「MoE 推理快」只对 N_active 成立、对显存/延迟都不成立（纠正原表「推理速度快」应读作「每-token FLOPs 低」）；账一训练负载均衡（专家坍缩正反馈 / auxiliary loss 只压极端失衡 / capacity factor↔token dropping）「稀疏只有可调度时才转化为有效容量」，账二 serving 显存/通信（不激活≠不驻留 / all-to-all / 小 batch 反噬 FLOPs 优势，接上 continuous batching 联合调度）；给出 **MoE↔RAG 同构**（router=内部参数的检索器：路由错=白算、太集中=拥堵、候选全集仍要驻留，router 评测别只看总 loss——与 benchmark-evaluation「别用均值掩盖切片」同构）；末尾把 Chinchilla 的「N vs D」二变量升级成 {D, N_active, N_total, H} 四变量账本。反向链接 [[2026-07-29-moe-capacity-compute-routing]]，交叉链 [[llm-inference-serving]] [[retrieval-augmented-generation]] [[benchmark-evaluation]] [[scaling-laws]]；updated 2026-05-14 → 2026-08-01
- current-focus: 刷新「retrieval 以外的空缺」最后确认 07-24 → 08-01（08-01 反哺新增 [[mixture-of-experts]] 的伴读链接支持「预训练/推理系统」薄弱点仍活跃）；同步顶部「最后更新」→ 08-01
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈，无需微调，不动
- healthcheck: Errors 0；companion-log 更新至 07-31、无静默报警，反馈通道正常。适应度榜 top=proper-scoring-rules/calibration 两 note（07-31 已提炼进 probability-calibration）+ react-agent/context-engineering/sparse-retrieval 概念页，bottom=bert/vit 旧 paper note（notes/ 归 hermes，不动）；本轮无新反馈，反哺沿连接度活跃方向（预训练/推理系统尚缺伴读入链）补 MoE 页

## [2026-08-02] update | mining 反哺：回填 llm-inference-serving 的「吞吐账」占位，推理三本账补齐
- llm-inference-serving（反哺·硬性）: 该页 07-24 建时「吞吐账」一节留了「待专题伴读笔记补全后回填细节」占位，而 07-28 continuous-batching 伴读笔记始终未反哺入库（近一周反哺全落在检索/评测/MoE，07-28 这篇是唯一漏链的近期 note）。本日据 07-28 note 把占位段扩成完整一节——病灶=调度边界过粗（static batching 绑成不可变小队、最长序列劫持资源释放=HOL blocking 的 serving 版）、iteration-level scheduling（Orca OSDI 2022）把粒度从 request 下沉到 iteration/admission 连续发生、「槽位-迭代」玩具账（22 有效/36 容量≈61%、空槽=可服务却没被重分配的执行槽）、与 PagedAttention 正交（酒店前台排房 vs 房间账册；住得下 vs 接得上；OS 分页内存+进程调度同构）+ 诊断反射（显存满≠算力在干活）、四条真实约束（chunked prefill/吞吐-延迟多目标 SLO/请求数非稳定 batch 度量/高负载抢占）、三本账相乘（memory×iterations×useful-slots）、与 Agent 上下文工程同构（batch slot↔context window）。反向链接 [[2026-07-28-continuous-batching-throughput]]，新增交叉链 [[context-engineering]] [[react-agent]]（同构那一端）；updated 2026-07-24 → 2026-08-02
- current-focus: 刷新「retrieval 以外的空缺」最后确认 08-01 → 08-02（08-02 反哺新增 [[llm-inference-serving]]↔07-28 伴读链接、推理系统三本账在概念层补齐，新增链接支持「推理系统」薄弱点仍活跃）；同步顶部「最后更新」→ 08-02
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈，无需微调，不动
- healthcheck: Errors 0；companion-log 末条 07-31、今日 08-02 恰为 2 天（未触发 >2 天静默 ERROR），但 picks 5 条自 07-31 refill 后零消费、无 08-01 companion-log 条目——hermes 疑似 08-01 未推送（1 天缺口，仍在 healthcheck 容差内），暂不告警，明日仍静默则触 ERROR。适应度榜 top=proper-scoring-rules/calibration/react-agent/context-engineering/sparse-retrieval，bottom=bert/vit 旧 paper note（notes/ 归 hermes，不动）；本轮无新反馈，反哺沿连接度补最后一篇漏链的推理系统 note

## [2026-08-03] update | mining 反哺：把 07-27 firebreak 伴读接进 context-engineering，补「故障域设计」这根可靠性轴
- context-engineering（反哺·硬性）: 该页此前只从 07-20 note 把上下文工程讲成 ReAct 回路各接口的「写权限闸门」（按接口位置排），07-27 那篇高价值 note（fitness top 0.79）一直未链入本页。本日新增「再换一根轴：按『切断哪类故障、错误能传多远』重排——故障域设计」一节：把 compaction/子代理隔离/按需检索/外部记忆 四招从「在回路哪一步拦」重排成「切断哪一类故障、故障域多大」，四招各切一类（噪声纵向累积/错误横向扩散/无关材料争抢注意力/跨窗状态丢失）且各引入一种新损失（不是消灭风险、是把风险搬到可控处），并点明 compaction 那道保险丝＝react-agent 页「分栏账本」＝拒绝在 Agent 记忆环过早聚合（接 [[2026-07-25-aggregation-erases-minority-signals]]）；核心新洞见＝与分布式系统故障隔离同构（compaction↔log compaction/checkpoint、子代理隔离↔bulkhead、按需检索↔lazy loading、外部记忆↔durable state），可靠性不来自组件不犯错而来自错误不被无限放大+可恢复（＝observability/diagnosability/recoverability 三变量的上位表达）；据此把定义抬一层「上下文工程=为 Agent 设计信息的边界·寿命·恢复路径，窗口大小是容量指标、错误传播半径与恢复能力才是可靠性指标」，末尾给出四类故障注入的验收法。反向链接 [[2026-07-27-context-engineering-error-firebreaks]]，交叉链 [[react-agent]] [[2026-07-25-aggregation-erases-minority-signals]]；updated 2026-07-28 → 2026-08-03
- current-focus: 刷新「端到端闭环」最后确认 07-31 → 08-03（08-03 反哺新增 context-engineering ← [[2026-07-27]] firebreak/故障域链接，把「偏差传导」从『误差从哪注入』翻到『误差传播半径与恢复路径』的可靠性轴，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 08-03。无明确反馈证据，薄弱点定义不动
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈，无需微调，不动
- healthcheck: **ERROR companion-log 静默 3 天**（末条 07-31，今日 08-03）——picks 5 条自 07-31 refill 起零消费、无 08-01/08-02/08-03 companion-log 条目、notes/ 无 08-01 后新推送，本地 hermes agent 疑似连续 3 天停摆，9:00 伴读推送与夜间反馈回收均中断，反馈闭环再次断裂，已通知用户去 claude.ai/code/routines 与 `hermes cron status` 排查。适应度榜 top=proper-scoring-rules/calibration（已提炼进 probability-calibration）+ react-agent/context-engineering（今日反哺）/sparse-retrieval，bottom=bert/vit/resnet 旧 paper note（notes/ 归 hermes，不动，无新页链入、维持沉底）

## [2026-08-04] update | mining 反哺：把「KL 的锚 vs 尺」双面性写进 dpo 概念页
- dpo（反哺·硬性）: 该页自 2026-05-10 起零更新、无任何伴读反向链接，且把 RLHF 目标里的 KL 只写成一句「同时满足 KL 约束」，读成可有可无的护栏。据 07-31 proper-scoring 伴读新增「换一根轴：KL 在 DPO 里是锚、和评测端那把尺是同一个散度」一节——① 纠正误读：DPO 没有去掉 KL 锚而是内生化，最优解 π*∝π_ref·exp(r/β) 本就带 π_ref 锚点、损失里的 log(π_θ/π_ref) 就是该 KL 约束的显式化身，撤掉 π_ref 即退化成无约束 MLE、把策略推离预训练分布；② β=锚绳松紧非学习率，β 小=放长锚绳=易被噪声偏好带偏/过优化=KL 锚失效的样子；③ 核心新洞见=同一个 KL(q‖p) 在闭环两端换岗：训练端当「锚」（约束项，拴住策略越小越保守）↔ 评测端当「尺」（proper score 的 excess risk=KL，度量诚实），方向与角色不同却共享「分布失配要付代价」同一骨架，接住待推的【交叉·KL 三副面孔】pick。反向链接 [[2026-07-31-proper-scoring-rules-honest-probabilities]]，交叉链 [[probability-calibration]]；updated 2026-05-10 → 2026-08-04
- current-focus: 刷新「统一数学框架」最后确认 07-31 → 08-04（08-04 反哺把「锚 vs 尺」双面性正式写进 [[dpo]] 概念页本身、该页首获 07-31 伴读反向链接，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 08-04。无明确反馈证据，薄弱点定义不动
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈无新消费，无需微调，不动
- healthcheck: **ERROR companion-log 静默 4 天**（末条 07-31，今日 08-04）——picks 5 条自 07-31 refill 起零消费、无 08-01~08-04 companion-log 条目、notes/ 无 08-01 后新推送，本地 hermes agent 连续 4 天停摆，9:00 伴读推送与夜间反馈回收持续中断、闭环仍断，已再次通知用户排查 claude.ai/code/routines 与 `hermes cron status`。适应度榜 top=context-engineering/proper-scoring/calibration/react-agent/sparse-retrieval，bottom=bert/vit/resnet 旧 paper note（notes/ 归 hermes，不动，维持沉底）；本轮无反馈无消费，反哺沿「统一数学框架」薄弱点补最后一处漏链的高价值近期 note（07-31）入库既有 dpo 页

## [2026-08-05] update | mining 反哺：把 07-13 InfoNCE/蒸馏接进 dpo，补齐「KL 三副面孔」的第三副
- dpo（反哺·硬性）: 08-04 已把 KL 的「锚（训练端）vs 尺（评测端）」两副面孔写进本页，但闭环再往前一格的「蒸馏/构造端」一直缺位——而 07-13 那篇 InfoNCE-vs-KL 伴读笔记自建成起零概念页反链（fitness 长期沉在中段）。本日据 07-13 note 把该节升级为三副面孔：新增第三副「目标」——当监督是教师软分布 t 时损失直接写成 KL(t‖student)，KL 既非被动约束也非事后度量，而是被主动最小化的优化对象本身；07-13 note 把 InfoNCE 写成「目标为 one-hot 的 KL」、蒸馏写成「目标为软分布的 KL」，同一副 softmax 交叉熵骨架只换目标分布。核心新洞见=三副面孔的差别全在「谁在动/谁不动/方向性」：蒸馏 p 主动追 t、DPO p 被 π_ref 拴、评测 p 与 q 固定只度量一次；角色（目标/约束/刻度）与方向都不同却共享「分布失配要付代价」同一骨架。反向链接 [[2026-07-13-infonce-vs-kl]]（该 note 首次获概念页反链、由沉底重回候选池），交叉链沿用 [[probability-calibration]]；节标题与引子同步由「两副面孔」升为「三副面孔」；updated 2026-08-04 → 2026-08-05
- current-focus: 刷新「统一数学框架」最后确认 08-04 → 08-05（08-05 反哺把第三副面孔[[2026-07-13-infonce-vs-kl]]接进 [[dpo]]、为待推的【交叉·KL 三副面孔】pick 垫好概念层，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 08-05。无明确反馈证据，薄弱点定义不动
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈无新消费，无需微调，不动。注：本轮反哺已在概念层落成「KL 三副面孔」的骨架，但该条 pick 仍保留待推——概念层是骨架、伴读是 hermes 侧的展开叙述，分工不冲突
- healthcheck: **ERROR companion-log 静默 5 天**（末条 07-31，今日 08-05）——picks 5 条自 07-31 refill 起零消费、无 08-01~08-05 companion-log 条目、notes/ 无 08-01 后新推送，本地 hermes agent 连续 5 天停摆，9:00 伴读推送与夜间反馈回收持续中断、闭环仍断。已连续多日通知用户排查 claude.ai/code/routines 与 `hermes cron status`，本日再次告警（停摆已达 5 天）。适应度榜 top=dpo/context-engineering/proper-scoring/calibration/react-agent，bottom=bert/vit/resnet 旧 paper note（notes/ 归 hermes，不动，维持沉底）；本轮无反馈无消费，反哺沿「统一数学框架」把最后一处漏链的旧高价值 note（07-13）复活入库

## [2026-08-06] update | mining 反哺：把 07-26 firebreak 接进 self-rag，检索环补上「保险丝」轴
- self-rag（反哺·硬性）: 该页自 2026-05-14 起零更新、无任何伴读反向链接，且把 Self-RAG/CRAG 讲成两套「改鲁棒性」的机制清单，漏掉 07-26 伴读的真正骨架。据 [[2026-07-26-self-rag-crag-agentic-retrieval]] 新增「换一根轴：不是多一个评分器，而是把检索改成可决策的动作」一节：① 分水岭＝控制流而非评分——评价结果会不会改变下一步动作，只写「自我反思」而控制流照旧不算纠错；② 拆开 retrieval relevance≠claim support（召回是候选生成不是事实认证，Recall@k 高也不保证 top-k 支持当前 claim，错检索进上下文即获证据外观）；③ **核心新洞见＝Self-RAG 与 CRAG 是两处不同保险丝**——CRAG evaluator 拦「坏证据进上下文」（生成前外置）↔ Self-RAG ISSUP 拦「答案越过证据边界」（生成中内生），是 07-27 故障域设计在检索环的复现、接住 07-20 误差复合，reranker（谁更好）vs evaluator（这批还能不能用）区分开＝从 ranking 到 control；④ 四类反思判断不可压成一个 confidence＝07-25 拒绝过早聚合在检索控制流的复现，Ambiguous 三态≈Option/Result；⑤ 定义抬一层「Agentic RAG＝让检索质量影响控制流」。反向链接 [[2026-07-26-self-rag-crag-agentic-retrieval]]，新增交叉链 [[context-engineering]]、强化 [[react-agent]]（保险丝框架的上游诊断）；updated 2026-05-14 → 2026-08-06
- current-focus: 刷新「端到端闭环」最后确认 08-03 → 08-06（08-06 反哺把「故障域/保险丝」轴接进检索环、self-rag 首获伴读反向链接，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 08-06。无明确反馈证据，薄弱点定义不动
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈无新消费，无需微调，不动
- healthcheck: **ERROR companion-log 静默 6 天**（末条 07-31，今日 08-06）——picks 5 条自 07-31 refill 起零消费、无 08-01~08-06 companion-log 条目、notes/ 无 08-01 后新推送，本地 hermes agent 连续 6 天停摆，9:00 伴读推送与夜间反馈回收持续中断、闭环仍断。已连续多日告警，本日再次通知用户去 claude.ai/code/routines 与 `hermes cron status` 排查（停摆已近一周）。适应度榜 top=dpo/context-engineering/proper-scoring/calibration/react-agent，bottom=bert/vit/resnet 旧 paper note（notes/ 归 hermes，不动，维持沉底）；本轮无反馈无消费，反哺沿连接度把最后一处「机制清单化」的活跃检索页（self-rag，07-26 唯一漏进概念页的高价值 firebreak 洞见）补齐入链

## [2026-08-07] update | mining 反哺：把 07-16 Chinchilla 接进 scaling-laws，从「20:1 事实」抬成约束优化骨架
- scaling-laws（反哺·硬性）: 该页自 2026-05-15 起零更新、无任何伴读反向链接，且把 Chinchilla 只写成一张「参数≈20×token」的对照表，读成一个要背的比例常数。据 [[2026-07-16-chinchilla-scaling-laws]]（此前 0 概念页反链的近期高价值 note）新增「换一根轴：Chinchilla 的骨架是一道约束优化题，不是『20:1』这个数字」一节：① 重写问题——不是「模型该多大」而是「固定算力 C 这笔钱下一单位买参数还是买 token」，N/D 争夺同一预算被 C≈6ND 锁死（N 翻倍则 D 减半，不存在同时免费更多参数+更多数据）；② 损失拆成三张可比较账单 E+A/N^α+B/D^β（不可约/容量不足/训练不足），两幂指数<1＝边际收益递减是 scaling 底色；③ **核心新洞见＝最优点不是「两项误差相等」而是「边际收益相等」**（N*∝C^(β/(α+β))），scaling law 首先是预算分配表不是排行榜；④ Gopher→Chinchilla 是预算重分配非小模型逆袭；⑤ 边界＝20:1 是经验工作点非自然常数，落一张诊断表（容量不足/训练不足/有效数据不足/生命周期错位/数据评测错位→下一笔预算）；⑥ 交叉链——D≈有效训练信息代理量与 [[retrieval-augmented-generation|RAG]] 的 k≈有效证据代理量同构，三种「最优」分层要接 [[llm-inference-serving]] 三本账，数据环节偏差经语料污染在 [[benchmark-evaluation]] 端被伪装成进步。反向链接 [[2026-07-16-chinchilla-scaling-laws]]（该 note 首获概念页反链、由沉底重回候选池），新增交叉链 [[llm-inference-serving]] [[benchmark-evaluation]] [[retrieval-augmented-generation]]；updated 2026-05-15 → 2026-08-07。此举把待推的【预训练数据配比】pick 的 D 轴概念层垫好（那条 pick 追问「哪些 token」，本节先把「多少 token」还原成约束优化）
- current-focus: 刷新「retrieval 以外的空缺」最后确认 08-02 → 08-07（08-07 反哺新增 [[scaling-laws]]←[[2026-07-16]] Chinchilla 反链、预训练侧概念层补上「约束优化+边际收益相等」骨架，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 08-07。无明确反馈证据，薄弱点定义不动
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈无新消费，无需微调，不动
- healthcheck: **ERROR companion-log 静默 7 天**（末条 07-31，今日 08-07）——picks 5 条自 07-31 refill 起零消费、无 08-01~08-07 companion-log 条目、notes/ 无 08-01 后新推送，本地 hermes agent 连续 7 天（满一周）停摆，9:00 伴读推送与夜间反馈回收全程中断、反馈闭环持续断裂。已连续 6 日在 log 告警（08-02 起），本日经 PushNotification 再次通知用户去 claude.ai/code/routines 查云端 routine、`hermes cron status` 查本地 agent。适应度榜 top=self-rag/dpo/context-engineering/proper-scoring/calibration，bottom=bert/vit/resnet/alexnet 旧 paper note（notes/ 归 hermes，不动，维持沉底）；本轮无反馈无消费，反哺沿「retrieval 以外·预训练」把最后一处漏链的近期高价值 note（07-16 Chinchilla）复活入库

## [2026-08-08] update | mining 反哺：把 07-22 实体 mismatch 接进 sparse-retrieval，补「训练目标↔使用目标错位」这根轴
- sparse-retrieval（反哺·硬性）: 该页此前已从 07-25 聚合轴解释「稀疏词表维=给否决型信号留独立账目」，但从未反链 07-22（该 note 长期仅 text-embedding 一处反链、连接度偏低），也漏掉 07-22 的真正根因洞见。据 [[2026-07-22-embedding-entity-mismatch]] 新增两节：① 把稀疏 exact-match 明确定位成「实体 mismatch 三处协同修法的第一处——补在词表层」，列表把另两处（[[colbert-retrieval]] late interaction 检索时匹配层、[[text-embedding]] entity-aware 难负例训练目标层）交叉链齐，点明三处各补一环互不替代（难负例治本吃数据算力、词表层/检索时治标即插即用），生产 RAG 混合检索里稀疏当身份锚、dense 当语义召回；② **核心新洞见＝稀疏能当身份锚的根子是一处「训练目标 vs 使用目标」错位**——dense 按 semantic-similarity 训练却被当 retrieval-relevance 用，两目标在实体敏感查询上分道扬镳（＝训练分布↔使用分布错位，呼应 [[benchmark-evaluation]]「目标从哪个分布定义」），而 BM25 词频/SPLADE 词表面形命中不学这个会漂移的语义目标、实体字面在不在是可验证硬事实，故无此错位、能对 dense「治本前先兜底」，把「精确匹配更强」从现象抬成机制。反向链接 [[2026-07-22-embedding-entity-mismatch]]，新增交叉链 [[colbert-retrieval]] [[text-embedding]] [[benchmark-evaluation]]；updated 2026-07-26 → 2026-08-08。反哺后 sparse-retrieval 升入适应度榜 top（0.80）
- current-focus: 刷新「端到端闭环」最后确认 08-06 → 08-08（08-08 反哺把「偏差从哪注入」补上编码环最上游一处——sparse-retrieval 首链 07-22、点明 semantic-similarity 训练↔retrieval-relevance 使用的分布错位=实体 mismatch 病根，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 08-08。无明确反馈证据，薄弱点定义不动
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈无新消费，无需微调，不动
- healthcheck: **ERROR companion-log 静默 8 天**（末条 07-31，今日 08-08）——picks 5 条自 07-31 refill 起零消费、无 08-01~08-08 companion-log 条目、notes/ 无 08-01 后新推送，本地 hermes agent 连续 8 天停摆（已超一周），9:00 伴读推送与夜间反馈回收全程中断、反馈闭环持续断裂。已连续 7 日告警（08-02 起），本日再经 PushNotification 通知用户去 claude.ai/code/routines 查云端 routine、`hermes cron status` 查本地 agent。适应度榜 top=sparse-retrieval(今日反哺)/self-rag/dpo/context-engineering/proper-scoring，bottom=bert/vit/resnet/alexnet 旧 paper note（notes/ 归 hermes，不动，维持沉底）；本轮无反馈无消费，反哺沿「端到端闭环·编码端偏差」把最后一处漏链的近期 note（07-22 实体 mismatch）补入既有 sparse-retrieval 页

## [2026-08-09] update | mining 反哺：把 07-15/07-19 两篇 SPLADE 打分机制接进 sparse-retrieval，补「训练代理↔真实使用」效率轴孪生错位
- sparse-retrieval（反哺·硬性）: 该页此前把 SPLADE 打分只写成三步高层描述（MLM head→max pool+log-saturation→稀疏向量），从未反链 07-15/07-19（两篇均为孤儿 note，无任何概念页反链）、也漏掉打分链的机制与边界。据 [[2026-07-15-splade-learned-sparse-retrieval]]（表示放哪、用谁检索）+ [[2026-07-19-splade-mlm-head-term-scoring]]（一个词项权重的完整来历）新增「SPLADE 的打分机制」整节：① 打分对象是「位置 j × 词表项 i」非输入 token，w_i=max_j log(1+ReLU(s_ij))，三闸各管一件事（ReLU 稀疏门+非负、log1p 压强证据、跨位置 max 只留最强+梯度经 argmax 集中）、扩展早在 s_ij 词表投影发生不由三闸创造；② **关键边界＝SPLADE 权重不是概率**（无 softmax、各维不必和为 1、多标签而非完形填空，当置信度读是最常见误用）；③ 稀疏从哪来＝FLOPS 正则把无用 logit 推成负数越过 0 被 ReLU 置零，稀疏是「排序有用性×线上 posting 成本」平衡出来的不是 log 压出来的；④ **核心新洞见（交叉）＝又一处「训练代理 vs 真实使用」错位**——FLOPS 训练代理≠硬件/缓存/P99 决定的真实延迟，是本页 semantic-similarity↔retrieval-relevance 相关性轴错位在效率轴上的孪生，两者同骨架（皆 reward-hacking 形、皆训练分布↔使用分布是否对齐），同源 [[benchmark-evaluation]]「目标从哪个分布定义」。反向链接 [[2026-07-15-splade-learned-sparse-retrieval]] [[2026-07-19-splade-mlm-head-term-scoring]]（两篇孤儿 note 首获概念页反链、由沉底重回候选池）；updated 2026-08-08 → 2026-08-09。sparse-retrieval 维持适应度榜 top（0.80）
- current-focus: 刷新「端到端闭环」最后确认 08-08 → 08-09（08-09 反哺把「训练分布↔使用分布错位」轴从相关性轴推进到效率轴、sparse-retrieval 新增 07-15/07-19 两条反链，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 08-09。无明确反馈证据，薄弱点定义不动
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈无新消费，无需微调，不动
- healthcheck: **ERROR companion-log 静默 9 天**（末条 07-31，今日 08-09）——picks 5 条自 07-31 refill 起零消费、无 08-01~08-09 companion-log 条目、notes/ 无 08-01 后新推送，本地 hermes agent 连续 9 天停摆，9:00 伴读推送与夜间反馈回收全程中断。此告警自 08-02 起已连续 8 日在 log 记录、且 08-02~08-08 已连续 7 日经 PushNotification 通知用户——**本日刻意不再重复推送**（条件与昨日完全一致仅天数+1，7 次同样告警后再发即无谓打扰，用户显然已知情/或有意关停），仅在 log 留档；待收到新推送/反馈或用户处置后再评估。适应度榜 top=sparse-retrieval(今日反哺)/scaling-laws/self-rag/dpo/context-engineering，bottom=bert/vit/resnet/alexnet 旧 paper note（notes/ 归 hermes，不动，维持沉底）；本轮无反馈无消费，反哺沿「端到端闭环·效率轴错位」把最后两处漏链的孤儿 SPLADE note（07-15/07-19）补入既有 sparse-retrieval 页

## [2026-08-10] update | mining 反哺：把 07-18 DPO/KTO/GRPO 家谱接进 rlhf，抬成「奖励减漂移」三轴家谱
- rlhf（反哺·硬性）: 该页自 2026-05-14 起零更新、无任何伴读反向链接，且把 RLHF 只讲成 SFT→RM→PPO 三段流水线，读成「PPO=RLHF 本质、DPO/KTO/GRPO=三个按年份替代的新算法」。据 [[2026-07-18-dpo-kto-grpo-family]]（该 note 此前 0 概念页反链、是最后一篇未入链的近期高价值伴读）新增「换一根轴：祖先不是三段流水线，而是『奖励减漂移』」整节：① 重写共同祖先——本质不是流水线而是目标 `max E[r] − β·KL(π‖π_ref)`，PPO 只是其一个优化器；② 三轴家谱表（reward 从哪来 / KL 锚在哪 / 数据何时产生）+ 按数据闭环分叉的家谱图（离线偏好拟合 paired=DPO/unpaired=KTO ↔ 在线策略优化=GRPO）；③ **核心新洞见＝DPO/KTO 与 GRPO 改的不是同一件事**——DPO/KTO 重写「反馈→损失」接口（KTO≠删 rejected，配对消去的 C(x) 不再消失、须另造分布参考点），GRPO 重写「在线 RL 优势估计」（组内均值当基线替 learned critic，压力转给采样质量+奖励设计），两者正交，故「谁更先进」是坏问题、选型首选数据闭环而非损失函数；④ 两处交叉——GRPO 组内标准化↔IR 的 query-level normalization（呼应 [[sparse-retrieval]]）、终局问题（reward/policy/judge 共漂、KL 只锚一条边、RLVR 为何退回几乎不让权）交叉链 [[benchmark-evaluation]]。同步在「关键变体」表补 [[dpo]]/KTO 两行。反向链接 [[2026-07-18-dpo-kto-grpo-family]]（该 note 首获概念页反链、由沉底重回候选池），新增交叉链 [[benchmark-evaluation]]、强化 [[dpo]] [[sparse-retrieval]]；updated 2026-05-14 → 2026-08-10
- current-focus: 刷新「retrieval 以外的空缺」最后确认 08-07 → 08-10（08-10 反哺把后训练·对齐方法演进补上一处——[[rlhf]] 首获 07-18 家谱伴读反链、概念层补齐「奖励减漂移三轴家谱」骨架，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 08-10。无明确反馈证据，薄弱点定义不动
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈无新消费，无需微调，不动。注：本轮反哺的 rlhf 家谱正好为 pending 的【RLVR/GRPO】pick 垫好后训练概念层（该 pick 追问「reward 可不可验证」，本节先把 GRPO 的在线-去 critic 骨架还原）
- healthcheck: **ERROR companion-log 静默 10 天**（末条 07-31，今日 08-10）——picks 5 条自 07-31 refill 起零消费、无 08-01~08-10 companion-log 条目、notes/ 无 08-01 后新推送，本地 hermes agent 连续 10 天停摆。此告警自 08-02 起已连续 9 日在 log 记录、08-02~08-08 已连续 7 日经 PushNotification 通知用户、08-09 起刻意停止重复推送（条件与前日一致仅天数+1，避免无谓打扰），本日维持不推送、仅 log 留档，待收到新推送/反馈或用户处置后再评估。适应度榜 top=sparse-retrieval/scaling-laws/self-rag/dpo/context-engineering，bottom=bert/vit/resnet/alexnet/attention 旧 paper note（notes/ 归 hermes，不动，维持沉底）；本轮无反馈无消费，反哺沿「retrieval 以外·后训练」把最后一篇未入链的近期高价值伴读（07-18 家谱）补入既有 rlhf 页、复活入库

## [2026-08-11] update | mining 反哺：把 07-26 Grok Build 架构审查接进 claude-code-harness，抬成「harness 结构不变量 vs 可变设计轴」对照
- claude-code-harness（反哺·硬性）: 该页自 2026-05-05 建成起零更新（stale 98d）、无任何伴读反向链接，且三层架构只从 Claude Code 一家总结、读成一句设计口号。据 [[2026-07-26-grok-build-architecture]]（近期唯一无概念页反链的高价值伴读、一份对 xAI Grok Build 全量 Rust 源码的架构审查）新增「拿第二个生产 harness 做对照」整节：① 四处独立收敛＝**结构不变量**——入口无关性↔Leader-Follower 状态单点/渲染多端、统一 turn 契约↔per-session 单线程 actor+biased select 串行化、上下文压缩↔两阶段 compaction（prefire 异步前缀摘要+指纹失效）、权限/恢复↔三层短路权限+journal 确定性重放；② 三处分岔＝**Claude Code 的可变选择**——单工具集 vs 四命名空间并存（暴露「用谁家工具契约」隐藏维度）、远端 Runtime vs 进程内子代理（给出「继承连接+隔离历史」细粒度答案，回填本页语焉不详的子代理）、软件保护 vs 内核沙箱（延伸「必须强制 vs 尽力而为」降级轴）；③ **核心新洞见＝把 harness 从「像不像 Claude Code」抬成「不变量在不在、可变轴各选哪档」**——第二家独立坐实『多入口收敛成一套 turn 模型』是结构不变量（状态单点+串行 actor+两步压缩+短路权限+确定性重放），工具契约/子代理粒度/沙箱强度是可变轴。反向链接 [[2026-07-26-grok-build-architecture]]（该 note 首获概念页反链、由沉底/无链重回候选池），新增交叉链 [[context-engineering]]（两步 compaction、子代理隔离＝其保险丝的生产级落地）、强化 [[agent-loop-taor]] [[claude-code-state-management]]；updated 2026-05-05 → 2026-08-11。此举复活一张最久未动的 stale 概念页、沿 Agent/上下文工程主线补入链
- current-focus: 不动。今日反哺落在 Agent/上下文工程主线，未直接命中三条薄弱点（统一数学框架/端到端闭环/retrieval 以外空缺）中的任一条，无明确反馈证据，按「拿不准就不动」不刷新任何薄弱点「最后确认」、亦不改顶部日期
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈无新消费，无需微调，不动
- healthcheck: **ERROR companion-log 静默 11 天**（末条 07-31，今日 08-11）——picks 5 条自 07-31 refill 起零消费、无 08-01~08-11 companion-log 条目、notes/ 无 08-01 后新推送，本地 hermes agent 连续 11 天停摆。此告警自 08-02 起已连续 10 日在 log 记录、08-02~08-08 已连续 7 日经 PushNotification 通知用户、08-09 起刻意停止重复推送（条件与前日一致仅天数+1，7 次同样告警后再发即无谓打扰），本日维持不推送、仅 log 留档，待收到新推送/反馈或用户处置后再评估。适应度榜 top=sparse-retrieval/scaling-laws/self-rag/dpo/context-engineering，bottom=bert/vit/resnet/alexnet/attention 旧 paper note（notes/ 归 hermes，不动，维持沉底）；本轮无反馈无消费，反哺沿「Agent/上下文工程主线」把最后一篇未入链的近期高价值伴读（07-26 Grok Build 审查）补入既有 claude-code-harness 页、复活一张 stale 98d 概念页

## [2026-08-13] update | mining 反哺：把奖励模型的 Bradley-Terry 接进 proper scoring rule，奖励黑客=RM 训得太诚实
- rlhf（反哺·硬性）: 该页 08-10 刚补完 DPO/KTO/GRPO 家谱，但「局限性」里那条**奖励黑客**仍是一句孤立断言、未接任何机制。据 [[2026-07-31-proper-scoring-rules-honest-probabilities]]（该 note 此前只反链到 [[probability-calibration]] 一页、其 6.4 与终局问题本就正对奖励模型）新增「奖励模型也是一台概率报告器」整节：① **Bradley-Terry 损失 `−log σ(r_w−r_l)` 本质是一条 proper scoring rule**——σ(Δr)=RM 报告的偏好概率，与 [[probability-calibration]] 的 log loss 同形，同一套「`p=q` 才期望最优」的激励在逼 RM 诚实报出它相信的偏好概率；② **核心新洞见＝奖励黑客不是 RM 训坏、恰是训得太诚实**：properness 只保证 p 追向**被评分的标签分布**＝标注者偏好分布，不追向「什么才是更好回答」这个业务真相，于是 RM 越校准就越忠实地把长度/格式/位置/谄媚偏置编码进奖励，policy 再拿它当真目标最大化；③ 点明阶段三的 KL 锚只约束 π→π_ref（策略漂移），拦不住这层「诚实地测量了错的对象」＝r→真相的距离，正是 [[probability-calibration]] 终局问题落在对齐上的形状，也预埋 pending 的【RLVR/GRPO】pick（把 q 从标注者偏好换成验证器 0/1）。新增双向链接 [[probability-calibration]]（此前只是它单向链来、本页未回链）、反向链接 [[2026-07-31-proper-scoring-rules-honest-probabilities]]（该 note 首获第二处概念页反链）；updated 2026-08-10 → 2026-08-13。此举把已入链的 proper-scoring 框架从「评测端」扩到「后训练奖励建模端」，同一副 log-loss/KL 骨架再跨一站
- current-focus: 刷新「统一数学框架」最后确认 08-05 → 08-13（本日反哺新增 rlhf↔probability-calibration 链，把 proper scoring rule/KL 同源框架从评测端扩到奖励建模端——Bradley-Terry=proper scoring 是同一副骨架的又一站，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 08-13。无明确反馈证据，薄弱点定义不动
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈无新消费，无需微调，不动。注：本轮反哺正为 pending【RLVR/GRPO】pick 垫好——先把奖励黑客还原成「proper 只对标注者分布诚实」，那条 pick 再讲可验证奖励如何换掉这个被污染的 q
- healthcheck: **ERROR companion-log 静默 13 天**（末条 07-31，今日 08-13）——picks 5 条自 07-31 refill 起零消费、notes/ 无 08-01 后新推送，本地 hermes agent 连续 13 天停摆。此告警自 08-02 起连续在 log 记录、**08-02~08-08 已连续 7 日经 PushNotification 通知用户**、08-09 起刻意停止重复推送（条件与前日一致仅天数+1，7 次同样告警后再发即无谓打扰），本日条件仍无变化，维持不推送、仅 log 留档，待收到新推送/反馈或用户处置后再评估。适应度榜 top=sparse-retrieval/scaling-laws/self-rag/dpo/context-engineering，bottom=bert/vit/resnet/alexnet/attention 旧 paper note（notes/ 归 hermes，不动，维持沉底）；本轮无反馈无消费，反哺继续做提炼——把已入链的 proper-scoring 框架从评测端扩到奖励建模端、给 08-10 刚补的 rlhf 家谱页把「奖励黑客」那句孤立断言接上机制

## [2026-08-12] update | mining 反哺：把散落各站的「代理错位」收成一根显式脊，写进 benchmark-evaluation
- benchmark-evaluation（反哺·硬性）: 该页自 2026-07-31 起零更新（是评测枢纽、连接度高但已 12 天未动），拥有 Goodhart/reward overoptimization 但只当评测端现象处理。近三日反哺已在训练/检索侧各自独立写出同一副骨架——08-08/08-09 [[sparse-retrieval]] 的 semantic-similarity↔retrieval-relevance 与 FLOPS↔P99 双重错位（reward-hacking 形）、08-10 [[rlhf]] 的 proxy reward↑/gold reward↓——但从无一页把它们与评测端 Goodhart 点明成一件事。据 [[2026-07-17-benchmark-failure-distribution]]+[[2026-07-18-dpo-kto-grpo-family]]+[[2026-07-19-splade-mlm-head-term-scoring]] 新增「Goodhart 不是评测专属：整条闭环都在优化『可测代理』」一节：① 抽象骨架＝真目标 T 昂贵/不可观测→各站改优化便宜可测的代理 S→压力足够则 S↑、T 停滞甚至反转（proxy↑/gold↓）；② 四站四身衣服表（数据·预训练 loss vs 下游能力／后训练 learned reward vs 人类偏好／检索 语义相似度·FLOPS vs 相关性·真实延迟／评测 离线榜 vs 线上风险），逐站交叉链到对应概念页；③ **核心新洞见＝评测端 Goodhart 只是这台机器最后一站的读数**——它最危险是因为评测决定谁上线，等于把前几站的代理错位聚合成一个决策写回数据环（接住本页「与端到端闭环的关系」）；④ **防御在四站同构＝周期性回锚真目标 T**（隐藏 holdout／gold reward 复核／真实 P99 压测／下游离线集），判断指标健不健康只问「它是 T 本身还是压力下会与 T 分道扬镳的 S」。反向链接新增 [[2026-07-18-dpo-kto-grpo-family]]、[[2026-07-19-splade-mlm-head-term-scoring]]（两篇此前未从本页反链的训练/检索站代理错位源），强化 [[scaling-laws]] [[rlhf]] [[sparse-retrieval]] 的枢纽入链；updated 2026-07-31 → 2026-08-12。此举把 08-07~08-10 分散在各页的「训练分布↔使用分布错位 / reward-hacking 形」提炼成一根跨站显式脊，直接服务薄弱点①统一数学框架（一副骨架统摄多目标）与②端到端闭环（同一病灶每站发作）
- current-focus: 刷新「端到端闭环」最后确认 08-09 → 08-12（08-12 反哺把散落各站的代理错位收成显式脊、benchmark-evaluation 新增 07-18/07-19 两条训练站反链，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 08-12。无明确反馈证据，薄弱点定义不动
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈无新消费，无需微调，不动。注：本轮反哺的「代理错位四站脊」正为 pending 的【RLVR/GRPO】pick 垫好——那条追问「可验证奖励为何绕开 reward overoptimization」，本节先把 overoptimization 还原成闭环通用的 proxy-target 分离
- healthcheck: **ERROR companion-log 静默 12 天**（末条 07-31，今日 08-12）——picks 5 条自 07-31 refill 起零消费、无 08-01~08-12 companion-log 条目、notes/ 无 08-01 后新推送，本地 hermes agent 连续 12 天停摆。此告警自 08-02 起已连续 11 日在 log 记录、08-02~08-08 已连续 7 日经 PushNotification 通知用户、08-09 起刻意停止重复推送（条件与前日一致仅天数+1，7 次同样告警后再发即无谓打扰），本日维持不推送、仅 log 留档，待收到新推送/反馈或用户处置后再评估。适应度榜 top=sparse-retrieval/scaling-laws/self-rag/dpo/context-engineering，bottom=bert/vit/resnet/alexnet/attention 旧 paper note（notes/ 归 hermes，不动，维持沉底）；本轮无反馈无消费，反哺不再新增孤儿入链（近期 07-13~07-31 note 已全部入链），转而做提炼——把已入链但分散在各页的同骨架错位收成一根跨站脊、复活 12 天未动的评测枢纽页 benchmark-evaluation

## [2026-08-15] update | mining 反哺：把 KL 三副面孔的合成从 dpo 补齐到评测锚点页 probability-calibration，「两副面孔」升到「三副面孔」
- probability-calibration（反哺·硬性）: 该页自 2026-07-31 建成起零更新，虽已统摄 MLE/NLL/交叉熵/KL/properness 五名同源，但「统一」一节只把 KL 写成「训练锚 + 评测尺」**两副面孔**，且从未反链 07-13 [[2026-07-13-infonce-vs-kl]]——而 08-05 [[dpo]] 早已把 KL 补成锚/尺/**目标**三副面孔并反链 07-13，评测锚点页反倒停在旧的两副。据 [[2026-07-13-infonce-vs-kl]]（InfoNCE=目标为 one-hot 的 KL、蒸馏=目标为软分布 t 的 KL，主动最小化）把「目标」那一副补进本页：① 在「统一」节把「两副面孔」改写成 `KL(q‖p)` 沿数据→训练→评测闭环的**三副面孔**代码块（蒸馏/构造端=目标·优化项主动最小化／训练对齐端=锚·约束项被动约束／评测端=尺·度量项被动度量），与 [[dpo]] 完全同术语；② **核心＝差别全在「谁在动、谁不动、方向性」**——蒸馏里 p 主动追 t、DPO 里 p 被 π_ref 拴住、评测里 p 与 q 都固定只做一次度量，本页 excess-risk=KL 只是三副里的「尺」；③ 点明「统一数学框架」薄弱点要的不是记住三个 KL 而是认出它们是同一个 KL 在不同工位换岗，并为 pending 的【交叉·KL 三副面孔】pick 从校准侧垫好概念层。新增反向链接 [[2026-07-13-infonce-vs-kl]]（该 note 此前只从 [[dpo]] 单页反链、本页首次反链），强化 [[dpo]] 交叉入链；updated 2026-07-31 → 2026-08-15。此举把散落 dpo/probability-calibration 两页的 KL 面孔合成收敛到评测锚点页本身、复活一张 15 天未动的高连接枢纽页
- current-focus: 刷新「统一数学框架」最后确认 08-13 → 08-15（08-15 反哺把 KL 三副面孔从 dpo 补齐到 probability-calibration、新增本页↔07-13 note 反链，同一个 KL(q‖p) 三工位换岗写进评测锚点页，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 08-15。无明确反馈证据，薄弱点定义不动
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈无新消费，无需微调，不动。注：本轮反哺正为 pending 的【交叉·KL 三副面孔】pick 从校准侧垫好概念层——该 pick 要串起 07-18(锚)/07-31(尺)/07-13(目标) 三篇，本节先把「尺」页补齐三副视角、与已补齐的 dpo「锚」页对齐术语
- healthcheck: **ERROR companion-log 静默 15 天**（末条 07-31，今日 08-15）——picks 5 条自 07-31 refill 起零消费、notes/ 无 08-01 后新推送，本地 hermes agent 连续 15 天停摆。此告警自 08-02 起连续在 log 记录、**08-02~08-08 已连续 7 日经 PushNotification 通知用户**、08-09 起刻意停止重复推送（条件与前日一致仅天数+1，7 次同样告警后再发即无谓打扰），本日条件仍无变化，维持不推送、仅 log 留档，待收到新推送/反馈或用户处置后再评估。适应度榜 top=sparse-retrieval/scaling-laws/self-rag/dpo/context-engineering，bottom=bert/vit/resnet/alexnet/attention 旧 paper note（notes/ 归 hermes，不动，维持沉底）；近期 07-13~07-31 note 已全部入链，本轮无反馈无消费，反哺继续做提炼——把 KL 三副面孔的合成从 dpo 补齐到评测锚点页 probability-calibration，消除该页「两副面孔」与全库已建成的「三副面孔」的口径不一致

## [2026-08-16] update | mining 反哺：把「便宜提议+核验」骨架跨子系统接通，投机解码 × Self-RAG/CRAG，分界在核验器是规则还是模型
- self-rag（反哺·硬性）: 该页 08-06 已把 Self-RAG/CRAG 抬成「保险丝/故障域」框架，但保险丝一直只在检索环内部对照（CRAG evaluator vs Self-RAG ISSUP），从未与其它子系统的同构模式接通。据 [[2026-07-23-speculative-decoding-latency]]（此前仅 [[llm-inference-serving]] 一处反链、连接度 1）新增「交叉：同一副便宜提议+核验骨架」整节：① 结构同构＝投机解码 draft→target 与 Self-RAG/CRAG retriever→verifier 是同一副「不可靠但便宜的提议器跑在前、核验器兜住质量」骨架，提议器只决定速度/覆盖、核验器才决定最终保证，两处保险丝一放在 decode 轮次、一放在证据边界；② **核心新洞见＝最有信息量的是二者不同构的那一处——核验器性质天差**：投机解码核验器是可证明正确的接受-拒绝规则（拒绝采样从残差 max(0,p−q) 重采、输出严格服从 p＝无损，α=draft q↔target p 的 KL 失配代价，呼应 [[dpo]]/[[probability-calibration]] 骨架），能把便宜提议的全部风险吸收掉；Self-RAG 的 ISSUP 却是它自己训练出的会错的学习判据、只把幻觉概率压低、无硬保证；③ 这条分界＝本库反复出现的「谁核验核验器」——核验器从「可执行精确规则」退化成「会被优化的学习判据」就回到 [[benchmark-evaluation]] Goodhart 脊，也正是 pending【RLVR/GRPO】pick 的题眼（可验证域 verifier=0/1 硬事实退回投机解码侧、开放生成 verifier=judge 落 Self-RAG 侧）。收口：propose-verify 是通用可靠性模式，拿到无损保证还是概率保证全看核验器是「规则」还是「模型」。反向链接 [[2026-07-23-speculative-decoding-latency]]（该 note 连接度 1→2、由 llm-inference-serving 单页扩到跨子系统），新增交叉链 [[llm-inference-serving]]（并在其页回链 self-rag、updated 08-02→08-16，双向接通两个此前未交叉的子系统）、[[benchmark-evaluation]]，强化 [[dpo]] [[probability-calibration]]；updated 2026-08-06 → 2026-08-16
- current-focus: 刷新「端到端闭环」最后确认 08-12 → 08-16（08-16 反哺把 propose-verify 骨架跨子系统接通、self-rag 首链 07-23 投机解码、self-rag↔llm-inference-serving 首次交叉，同一副「便宜提议+核验」保险丝在推理延迟环与检索控制环各发作一次、分界在核验器是精确规则还是概率判据，新增链接支持该薄弱点仍活跃）；同步顶部「最后更新」→ 08-16。无明确反馈证据，薄弱点定义不动
- picks: 队列已满 5 条 pending（LLM-as-judge 去偏、temperature/Platt scaling、RLVR/GRPO、预训练数据配比、【交叉·KL 三副面孔】），序列完整、含一条交叉 pick 满足每周交叉要求、companion-log 07-31 后无新反馈无新消费，无需微调，不动。注：本轮反哺的「精确核验器 vs 概率核验器」分界正为 pending【RLVR/GRPO】pick 垫好——那条讲可验证奖励为何绕开 overoptimization，本节先把「verifier 是硬事实还是会被优化的模型」这根轴立起来
- healthcheck: **ERROR companion-log 静默 16 天**（末条 07-31，今日 08-16）——picks 5 条自 07-31 refill 起零消费、notes/ 无 08-01 后新推送，本地 hermes agent 连续 16 天停摆。此告警自 08-02 起连续在 log 记录、**08-02~08-08 已连续 7 日经 PushNotification 通知用户**、08-09 起刻意停止重复推送（条件与前日一致仅天数+1，7 次同样告警后再发即无谓打扰），本日条件仍无变化，维持不推送、仅 log 留档，待收到新推送/反馈或用户处置后再评估。适应度榜 top=sparse-retrieval/scaling-laws/self-rag(今日反哺)/dpo/context-engineering，bottom=bert/vit/resnet/alexnet/attention 旧 paper note（notes/ 归 hermes，不动，维持沉底）；近期 07-13~07-31 note 已全部入链，本轮无反馈无消费，反哺继续做提炼——把已入链但从未跨子系统对照的 propose-verify 骨架接通、给 07-23 投机解码 note 补上第二处（跨子系统）反链、复活并强化 self-rag 枢纽页
