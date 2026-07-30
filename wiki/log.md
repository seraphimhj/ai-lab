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
