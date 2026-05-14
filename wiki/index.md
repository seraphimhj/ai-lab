# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: 2026-05-14 | Total pages: 69 (28 entities + 34 concepts + 7 comparisons)

## Entities

### 模型

- [[transformer-architecture]] — Transformer 架构，Self-Attention 机制，现代 LLM 基座
- [[bert]] — BERT 双向预训练语言模型，开创"预训练+微调"范式
- [[gpt-3]] — OpenAI 175B 自回归模型，验证 Scaling Law 与 In-Context Learning
- [[gpt-4]] — OpenAI 多模态大模型，人类水平专业基准表现
- [[llama]] — Meta AI 开源基础语言模型系列（LLaMA 1/2/3）
- [[deepseek]] — 深度求索开源系列，MLA + MoE + GRPO，R1 推理突破
- [[qwen]] — 阿里通义千问开源系列，中文能力突出，生态丰富
- [[mistral-7b]] — Mistral AI 7B 高效模型，SWA + GQA 架构
- [[mixtral]] — Mistral AI MoE 架构模型，8 专家稀疏路由
- [[gemma]] — Google DeepMind 开源轻量模型，基于 Gemini 技术
- [[yi-model]] — 零一万物开源模型，200K 超长上下文
- [[mamba]] — 选择性状态空间模型，O(N) 线性序列建模
- [[palm]] — Google PaLM 540B，Pathways 系统首次大规模验证
- [[phi]] — Microsoft 小型高效模型系列，"Textbooks Are All You Need"
- [[glm]] — 清华/智谱 GLM/ChatGLM 双语模型，自回归空白填充
- [[clip]] — OpenAI 视觉-语言对比学习模型，多模态学习奠基
- [[claude-code]] — Anthropic 通用终端 Agent，企业级 Agent 架构标杆
- [[mimo-v2]] — 小米模型系列（Flash/Pro/Omni/TTS），Hybrid Attention + MTP 架构

### 机构

- [[openai]] — GPT 系列 / ChatGPT / CLIP，AI 产业化核心推动者
- [[google-deepmind]] — PaLM / Gemini / Gemma / AlphaFold，基础研究领导者
- [[anthropic]] — Claude 系列 / Constitutional AI，AI 安全优先
- [[meta-ai]] — LLaMA 系列 / PyTorch / ReAct，开源 AI 生态推动者
- [[microsoft-research]] — Phi 系列 / LoRA / DeepSpeed，投资+自研双轨策略
- [[alibaba-qwen]] — Qwen 系列 / GTE 嵌入模型，中文开源 AI 领军
- [[baidu]] — ERNIE / 文心一言 / PaddlePaddle，知识增强预训练先驱
- [[nvidia-research]] — GPU/CUDA/TensorRT，AI 计算基础设施

### 人物

- [[luo-fuli]] — 小米大模型团队负责人，MiMo-V2 系列主导者
- [[yang-songlin]] — MIT CSAIL PhD，Linear Attention 研究者，Flash Linear Attention 作者

## Concepts

### Agent 设计
- [[agent-loop-taor]] — Think-Act-Observe-Repeat 执行循环模式
- [[agent-paradigm-shift]] — 2026 AI 范式转移：Pre-train(Chat) → Post-train(Agent)
- [[agent-product-design]] — Agent 产品设计三原则：教会智能体成功、反馈循环、上下文缺口
- [[agent-feedback-loop]] — Agent 反馈循环设计：rationale 参数、反馈工具、context seeding
- [[agent-context-gap]] — 多 Agent 上下文缺口：索要上下文而非索要答案

### Claude Code 系列
- [[claude-code-harness]] — 入口适配 + 会话编排 + 运行桥接三层架构
- [[claude-code-memory-system]] — 策略约束 + 指令注入 + 分层记忆召回
- [[claude-code-state-management]] — 会话运行态 + 全局会话态 + 持久化层

### 训练与对齐
- [[rlhf]] — RLHF 基于人类反馈的强化学习，三阶段偏好优化
- [[dpo]] — Direct Preference Optimization，简化 RLHF 无需奖励模型
- [[constitutional-ai]] — Anthropic 宪法式 AI，AI 自我对齐减少人工标注
- [[instruction-tuning]] — 指令微调，从 Self-Instruct 到大规模多任务
- [[lora]] — LoRA 低秩适配，参数高效微调范式

### 推理与提示
- [[chain-of-thought]] — CoT 思维链提示，显著提升 LLM 逻辑推理
- [[tree-of-thoughts]] — 树状思维搜索，增强复杂问题求解
- [[in-context-learning]] — In-Context Learning，GPT-3 验证的大规模少样本能力

### 效率优化
- [[flash-attention]] — FlashAttention 1/2/3，IO-aware 精确注意力加速
- [[model-quantization]] — 模型量化 (GPTQ/AWQ/SparseGPT)，推理加速显存优化
- [[mixture-of-experts]] — MoE 稀疏专家混合，参数量/计算量解耦
- [[scaling-laws]] — 缩放定律 (Kaplan + Chinchilla)，指导模型规模与数据量关系
- [[linear-attention]] — 线性注意力机制：O(L) 复杂度 vs O(L²) Softmax Attention
- [[hybrid-attention]] — 混合注意力架构：Linear 层省 KV Cache + Full 层保表达力
- [[sparse-attention]] — 稀疏注意力机制：DeepSeek 路线，Indexer 选 Top-K Token

### RAG / 检索增强
- [[retrieval-augmented-generation]] — RAG 检索增强生成，外部知识注入 LLM
- [[dense-passage-retrieval]] — DPR 密集段落检索，双编码器检索范式
- [[colbert-retrieval]] — ColBERT Late Interaction，token 级细粒度匹配
- [[self-rag]] — Self-RAG 自主判断检索需求，按需 RAG
- [[graph-rag]] — GraphRAG 知识图谱增强 RAG，支持全局问题回答

### Agent / 工具
- [[react-agent]] — ReAct 推理+行动协同范式，Agent 基础
- [[tool-use]] — LLM 工具使用，Toolformer 自主学会调用 API
- [[mcp-model-context-protocol]] — MCP 协议，AI 工具领域的「USB-C 标准」
- [[agent-skills]] — 可复用工作流程，渐进式披露按需加载
- [[context-engineering]] — 上下文工程，一切高级能力的本质都在上下文填充

### Embedding
- [[text-embedding]] — 文本嵌入/向量化，Sentence-BERT → E5 → MTEB 标准化评测

## Comparisons

- [[embedding-models-2025]] — 2025-2026 Embedding 大模型 MTEB 排名对比（Qwen3-Embedding 75.22 #1）
- [[open-source-llm-comparison]] — 2024-2025 开源 LLM 全面对比（LLaMA/Qwen/DeepSeek/Mistral/Gemma）
- [[rlhf-vs-dpo]] — RLHF vs DPO 对齐方法对比，流程/效率/效果多维分析
- [[rag-approaches]] — 6 种 RAG 架构对比（Naive → Agentic RAG）
- [[quantization-methods]] — 量化方法对比（GPTQ/AWQ/SparseGPT/GGUF）
- [[openclaw-vs-claude-code]] — 开源 vs 闭源 Agent 框架对比
- [[hybrid-vs-sparse-attention]] — Hybrid Linear vs Sparse Attention 效率路线对比

## Queries
