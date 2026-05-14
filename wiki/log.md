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
