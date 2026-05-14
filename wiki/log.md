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
