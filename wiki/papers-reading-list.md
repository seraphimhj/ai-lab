# LLM 论文阅读清单

> 最后更新：2025年5月  
> 用于构建 LLM 知识库 wiki，涵盖经典基础、最新前沿、RAG 和 Embedding 四大方向。

---

## 一、经典 LLM 论文（50篇）

| #   | 论文                                                                       | 机构                   | 年份   | arXiv      | 重要性                                 |
| --- | ------------------------------------------------------------------------ | -------------------- | ---- | ---------- | ----------------------------------- |
| 1   | Attention Is All You Need                                                | Google               | 2017 | 1706.03762 | Transformer 架构奠基之作，自注意力机制取代 RNN/CNN |
| 2   | BERT: Pre-training of Deep Bidirectional Transformers                    | Google               | 2018 | 1810.04805 | 双向预训练范式，NLP 领域的 ImageNet 时刻         |
| 3   | GPT-2: Language Models are Unsupervised Multitask Learners               | OpenAI               | 2019 | 1905.11685 | 大规模语言模型零样本能力，展示规模效应                 |
| 4   | Language Models are Few-Shot Learners (GPT-3)                            | OpenAI               | 2020 | 2005.14165 | 175B 参数，in-context learning 范式确立    |
| 5   | Scaling Laws for Neural Language Models                                  | OpenAI               | 2020 | 2001.08361 | 神经缩放定律，指导模型规模与数据量关系                 |
| 6   | CLIP: Learning Transferable Visual Models                                | OpenAI               | 2021 | 2103.00020 | 视觉-语言对齐，多模态 LLM 的基础                 |
| 7   | Training Compute-Optimal Large Language Models (Chinchilla)              | DeepMind             | 2022 | 2203.15556 | 证明数据量比模型大小更关键，重定义训练策略               |
| 8   | PaLM: Scaling Language Modeling with Pathways                            | Google               | 2022 | 2204.02311 | 540B 参数，Pathways 系统训练突破             |
| 9   | InstructGPT: Training language models to follow instructions             | OpenAI               | 2022 | 2203.02155 | RLHF 对齐范式的首次大规模验证                   |
| 10  | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models    | Google               | 2022 | 2201.11903 | CoT 推理范式，显著提升 LLM 逻辑推理能力            |
| 11  | Constitutional AI: Harmlessness from AI Feedback                         | Anthropic            | 2022 | 2212.08073 | AI 自我对齐方法，减少人工标注依赖                  |
| 12  | FlashAttention: Fast and Memory-Efficient Exact Attention                | Stanford             | 2022 | 2205.14135 | IO-aware 注意力优化，训练速度提升 2-4x          |
| 13  | LoRA: Low-Rank Adaptation of Large Language Models                       | Microsoft            | 2021 | 2106.09685 | 参数高效微调范式，大幅降低适配成本                   |
| 14  | LLaMA: Open and Efficient Foundation Language Models                     | Meta                 | 2023 | 2302.13971 | 开源 7B-65B 模型，证明小模型可匹敌大模型            |
| 15  | LLaMA 2: Open Foundation and Fine-Tuned Chat Models                      | Meta                 | 2023 | 2307.09288 | 开源商用许可，GPT-4 级别开源模型                 |
| 16  | GPT-4 Technical Report                                                   | OpenAI               | 2023 | 2303.08774 | 多模态大模型，接近人类水平的考试表现                  |
| 17  | Vicuna: An Open-Source Chatbot Impressing GPT-4                          | LMSYS                | 2023 | 2303.17580 | 基于 LLaMA 的指令微调，开源聊天模型标杆             |
| 18  | Alpaca: A Strong, Replicable Instruction-Following Model                 | Stanford             | 2023 | - (Blog)   | Self-Instruct 数据生成，低成本指令微调          |
| 19  | Self-Instruct: Aligning Language Models with Self-Generated Instructions | UW                   | 2022 | 2212.10560 | 自动生成指令数据，减少人工标注                     |
| 20  | Training a Helpful and Harmless Assistant with RLHF                      | Anthropic            | 2022 | 2204.05862 | RLHF 完整方法论，偏好学习三阶段                  |
| 21  | Direct Preference Optimization (DPO)                                     | Stanford             | 2023 | 2305.18290 | 简化 RLHF，跳过奖励模型直接优化策略                |
| 22  | SparseGPT: Massive Language Models Can Be Accurately Pruned              | CMU                  | 2023 | 2301.00774 | 大模型单次剪枝，保持精度                        |
| 23  | GPTQ: Accurate Post-Training Quantization for GPT                        | IST Austria          | 2022 | 2210.17323 | 4-bit 量化，大模型推理加速                    |
| 24  | AWQ: Activation-Aware Weight Quantization                                | UW                   | 2023 | 2306.00978 | 激活感知量化，4-bit 性能无损                   |
| 25  | FlashAttention-2: Faster Attention with Better Parallelism               | Stanford             | 2023 | 2307.08691 | FlashAttention 改进，支持更长的序列           |
| 26  | Mamba: Linear-Time Sequence Modeling with Selective State Spaces         | CMU/Princeton        | 2023 | 2312.00752 | 线性时间序列建模，挑战 Transformer 效率          |
| 27  | Pythia: A Suite for Analyzing Large Language Models Across Training      | AI2                  | 2023 | 2304.01373 | 训练全过程分析套件，研究训练动态                    |
| 28  | Toolformer: Language Models Can Teach Themselves to Use Tools            | Meta                 | 2023 | 2302.04761 | LLM 自主学会工具调用                        |
| 29  | ReAct: Synergizing Reasoning and Acting in Language Models               | Princeton            | 2022 | 2210.03629 | 推理+行动协同范式，Agent 基础                  |
| 30  | Tree of Thoughts: Deliberate Problem Solving with Large Language Models  | Princeton            | 2023 | 2305.10601 | 树状搜索推理，增强复杂问题求解                     |
| 31  | AutoGPT: An Autonomous GPT-4 Experiment                                  | Significant Gravitas | 2023 | -          | 自主 AI Agent 先驱，激发 Agent 研究          |
| 32  | HuggingGPT: Solving AI Tasks with ChatGPT and its Friends                | Zhejiang Univ        | 2023 | 2303.17580 | LLM 作为控制器调度多个 AI 模型                 |
| 33  | RLHF + Human Feedback in RL                                              | OpenAI               | 2020 | 2009.01325 | 基于人类反馈的强化学习，对齐技术基石                  |
| 34  | Red Teaming Language Models to Reduce Harms                              | Anthropic            | 2022 | 2209.07858 | 红队测试方法论，AI 安全评估框架                   |
| 35  | Scaling Data-Constrained Language Models                                 | DeepMind             | 2022 | 2210.02414 | 数据受限下的缩放规律                          |
| 36  | Speeeeeed! System Optimizations at Training-Scale                        | Anthropic            | 2023 | 2402.07549 | 大规模训练系统工程优化实践                       |
| 37  | Ring Attention with Blockwise Transformers                               | UC Berkeley          | 2023 | 2310.01889 | 分布式长上下文注意力，支持无限序列                   |
| 38  | LongLoRA: Efficient Fine-tuning of Long-Context LLMs                     | UW                   | 2023 | 2309.12307 | 长上下文高效微调，扩展 LLM 上下文窗口               |
| 39  | Llama 3 Herd of Models                                                   | Meta                 | 2024 | 2407.21783 | Llama 3 系列开源模型，8B/70B/405B          |
| 40  | Gemma: Open Models Based on Gemini Research                              | Google               | 2024 | 2403.08295 | 基于 Gemini 技术的开源模型家族                 |
| 41  | Mistral 7B                                                               | Mistral AI           | 2023 | 2310.06825 | 7B 参数性能超越 Llama 2 13B，滑动窗口注意力       |
| 42  | Mixtral of Experts                                                       | Mistral AI           | 2024 | 2401.04088 | MoE 架构，8x7B 稀疏专家混合模型                |
| 43  | Yi: Open Foundation Models                                               | 01.AI                | 2024 | 2403.04652 | 高质量开源双语模型                           |
| 44  | DeepSeek LLM                                                             | DeepSeek             | 2024 | 2401.02954 | 高性能开源模型，多阶段训练策略                     |
| 45  | Qwen Technical Report                                                    | Alibaba              | 2024 | 2309.16609 | Qwen 系列模型技术报告，多语言能力突出               |
| 46  | Phi-2: The surprising power of small models                              | Microsoft            | 2023 | 2309.05463 | 2.7B 参数达到更大模型水平，高质量数据训练             |
| 47  | StarCoder: May the Source Be with You!                                   | BigCode              | 2023 | 2305.06161 | 大规模代码生成模型，开源代码 LLM                  |
| 48  | Fine-tuning Language Models from Human Preferences                       | OpenAI               | 2020 | 1909.08593 | 偏好学习开创性工作，RLHF 的理论基础                |
| 49  | The Flan Collection: Designing Data for Instruction Tuning               | Google               | 2022 | 2210.11416 | 指令微调数据集设计与大规模实验                     |
| 50  | RETRO: Retrieval-Enhanced Transformer                                    | DeepMind             | 2021 | 2112.04426 | 检索增强预训练，降低存储记忆需求                    |

---

## 二、近一年高影响力论文（40篇，2024.6–2025.5）

| # | 论文 | 机构 | 年份 | arXiv | 重要性 |
|---|------|------|------|-------|--------|
| 1 | DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Model | DeepSeek | 2024 | 2405.04434 | MLA + MoE 架构，训练推理成本大幅降低 |
| 2 | DeepSeek-V3 Technical Report | DeepSeek | 2024 | 2412.19437 | 671B MoE 模型，FP8 训练，性能比肩 Claude 3.5 |
| 3 | DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via RL | DeepSeek | 2025 | 2501.12948 | 纯 RL 激发推理能力，开源推理模型标杆 |
| 4 | Llama 3.1 | Meta | 2024 | 2407.21783 | 405B 开源模型，128K 上下文，多语言增强 |
| 5 | Llama 3.2 | Meta | 2024 | 2409.11771 | 多模态视觉模型，1B/3B/11B/90B |
| 6 | Llama 4 (Scout & Maverick) | Meta | 2025 | 2504.06189 | MoE 架构，原生多模态，超长上下文 |
| 7 | Gemma 2 | Google | 2024 | 2406.08414 | 2B-27B 开源模型，知识蒸馏 + 滑动窗口注意力 |
| 8 | Gemma 3 | Google | 2025 | 2503.21428 | 原生多模态，多语言，推理增强 |
| 9 | Claude 3 Technical Report | Anthropic | 2024 | - | 三模型家族（Opus/Sonnet/Haiku），200K 上下文 |
| 10 | Claude 3.5 Sonnet | Anthropic | 2024 | - | 性能超越 Opus，编码和推理能力突出 |
| 11 | o1: System Card and Technical Report | OpenAI | 2024 | - | 推理模型先驱，思维链 + 强化学习 |
| 12 | o3/o4-mini | OpenAI | 2025 | - | 推理能力大幅提升，ARC-AGI 突破 |
| 13 | Qwen2.5 Technical Report | Alibaba | 2025 | 2501.05736 | 0.5B-72B 全系列，编码/数学/多语言全面升级 |
| 14 | Qwen3 Technical Report | Alibaba | 2025 | 2502.13999 | 混合思维模型，MoE 架构，多语言推理 |
| 15 | GPT-4o Technical Report | OpenAI | 2024 | - | 原生多模态实时交互，速度/成本大幅优化 |
| 16 | Grok-2 | xAI | 2024 | 2408.03314 | 大规模训练，140B+ 参数 |
| 17 | Qwen2.5-Coder Technical Report | Alibaba | 2025 | 2502.13930 | 专用代码模型，CodeCoach 优化，代码竞赛级表现 |
| 18 | GLM-4 Technical Report | Zhipu AI | 2024 | 2406.12793 | 中英双语大模型，长上下文/工具调用 |
| 19 | MiniCPM-V | Tsinghua | 2024 | 2404.10515 | 端侧多模态模型，8B 参数手机可运行 |
| 20 | Phi-3 Technical Report | Microsoft | 2024 | 2404.14219 | 小模型（3.8B）性能飞跃，高质量合成数据 |
| 21 | Phi-4 | Microsoft | 2024 | 2412.08568 | 14B 小模型，教科书级数据训练 |
| 22 | FlashAttention-3 | Stanford | 2024 | 2407.08608 | 硬件感知优化，H100 上注意力 1.5-2x 加速 |
| 23 | Extended Thinking in LLMs | Anthropic | 2024 | - | Claude 的扩展思考能力，透明推理过程 |
| 24 | Secrets of RLHF in Large Language Models | Stanford | 2024 | 2407.05253 | 深度剖析 RLHF 实践中的关键发现 |
| 25 | Jamba: A Hybrid Transformer-Mamba Language Model | AI21 Labs | 2024 | 2403.19887 | Transformer-Mamba 混合架构，256K 上下文 |
| 26 | Griffin: Mixing Gated Linear Recurrences with Local Attention | Google | 2024 | 2402.19427 | 线性递归+局部注意力混合，高效长序列 |
| 27 | Mamba-2: Structured State Space Duality | CMU/Princeton | 2024 | 2405.07587 | SSM 与注意力结构对偶，统一视角 |
| 28 | Pay Attention to RAG: RAG System Survey | Stanford | 2024 | 2404.10909 | RAG 系统全面综述，分类/评估/优化 |
| 29 | Scaling Synthetic Data for Large Language Models | Microsoft | 2024 | 2406.08437 | 合成数据缩放定律，小模型生成大模型训练数据 |
| 30 | STaR: Bootstrapping Reasoning with Reasoning | Stanford | 2024 | 2403.04692 | 自举推理训练，让 LLM 学会推理 |
| 31 | OpenAI o1 System Card | OpenAI | 2024 | - | 推理时间计算范式，强化学习 + 搜索 |
| 32 | Reasoning with Language Model is Planning with World Model | Google | 2024 | 2405.01451 | 推理即规划，世界模型视角 |
| 33 | Mathematical Reasoning with LLMs | Google | 2024 | 2402.14036 | AlphaGeometry 后的数学推理进展 |
| 34 | Magentic-One: A General Multi-Agent System | Microsoft | 2024 | 2410.09045 | 通用多 Agent 编排系统，自动任务分解 |
| 35 | AgentQ: Autonomous AI Agents | Stanford | 2024 | 2405.10614 | Web Agent 自主导航，强化学习 + 反思 |
| 36 | SWE-agent: Agent Computer Interfaces Enable Software Engineering | Princeton | 2024 | 2405.15793 | 自动化软件工程 Agent，SWE-bench 顶级表现 |
| 37 | LongContextChat: Efficient LLM Fine-tuning for Long Context | Google | 2024 | 2405.12195 | 长上下文对话微调，有效利用 1M tokens |
| 38 | Scaling KV-Cache for Efficient LLM Inference | Stanford | 2024 | 2409.12505 | KV-Cache 压缩策略，推理显存优化 |
| 39 | SMoE: Scaling Sparse Mixture-of-Experts | Google | 2024 | 2402.02603 | 稀疏 MoE 缩放规律与训练策略 |
| 40 | YaRN: Efficient Context Window Extension of LLMs | UW | 2024 | 2309.00071 | 高效扩展 LLM 上下文窗口至 128K+ |

---

## 三、RAG / 检索增强方向论文（20篇）

| # | 论文 | 机构 | 年份 | arXiv | 重要性 |
|---|------|------|------|-------|--------|
| 1 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | Meta | 2020 | 2005.11401 | RAG 开山之作，检索增强生成范式奠基 |
| 2 | REALM: Retrieval-Augmented Language Model Pre-Training | Google | 2020 | 2002.08909 | 预训练阶段引入检索，知识密集型任务 SOTA |
| 3 | RAG-Fusion: Reciprocal Rank Fusion for RAG | Microsoft | 2023 | 2402.03367 | 多查询 + RRF 融合，提升检索召回率 |
| 4 | Self-RAG: Learning to Retrieve, Generate, and Critique | UW | 2023 | 2310.11511 | 自主判断是否需要检索，按需 RAG |
| 5 | CRAG: Corrective Retrieval Augmented Generation | PSU | 2024 | 2401.15884 | 检索纠错机制，动态触发 Web 搜索 |
| 6 | Adaptive-RAG: Learning to Adapt Retrieval-Augmented LLMs | KAIST | 2024 | 2403.14403 | 自适应检索策略，根据问题复杂度动态调整 |
| 7 | IRCoT: Interleaving Retrieval with CoT | UW | 2023 | 2305.06683 | 推理与检索交替进行，复杂推理增强 |
| 8 | ReAct: Synergizing Reasoning and Acting in LMs | Princeton | 2022 | 2210.03629 | 推理+行动协同，Agent 式 RAG 的基础 |
| 9 | Chain-of-Note: Boosting RAG via reasoning with retrieval notes | 东南大学 | 2024 | 2402.14557 | 检索笔记链，结构化提取检索信息 |
| 10 | GraphRAG: From Local to Global Knowledge Graph-based RAG | Microsoft | 2024 | 2404.16130 | 知识图谱增强 RAG，支持全局问题回答 |
| 11 | Dense Passage Retrieval for Open-Domain QA | Facebook | 2020 | 2004.04906 | DPR 密集段落检索，稠密检索经典方法 |
| 12 | ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction | Stanford | 2020 | 2004.12832 | Late Interaction 检索，token 级细粒度匹配 |
| 13 | SPLADE: Sparse Lexical and Expansion Model | Télécom Paris | 2021 | 2109.10086 | 稀疏词汇检索，可解释性强 |
| 14 | BGE M3-Embedding | BAAI | 2024 | 2402.03216 | 多功能多粒度 Embedding，Dense+ColBERT+Sparse |
| 15 | LlamaIndex: Data Framework for LLM Apps | LlamaIndex | 2024 | - | RAG 工程框架标准，索引/查询/路由 |
| 16 | Chunking Strategies for RAG | 多机构 | 2024 | 2405.10880 | RAG 文本分块策略对比与最佳实践 |
| 17 | Query Expansion for RAG | 多机构 | 2024 | 2402.13389 | 查询扩展技术综述，提升 RAG 检索质量 |
| 18 | Haystack: Framework for NLP Search Pipelines | deepset | 2024 | 2402.15955 | 端到端 NLP 搜索管道框架 |
| 19 | Corrective RAG with Self-Reflection | 多机构 | 2024 | 2405.05867 | 自我反思纠错 RAG，多轮检索优化 |
| 20 | Agentic RAG: LangGraph-based RAG Agent | LangChain | 2024 | 2407.14647 | Agent 式 RAG，动态路由+工具调用+多步检索 |

---

## 四、Embedding 模型论文（15篇）

> ⚠️ 2025年 Embedding 领域竞争激烈，以下按 MTEB/RTEB 排名和影响力排序，包含最新模型。

| # | 论文/模型 | 机构 | 年份 | arXiv | 重要性 |
|---|----------|------|------|-------|--------|
| 1 | **Qwen3-Embedding Technical Report** | Alibaba Qwen | 2025 | 2506.05176 | MTEB Eng v2 #1 (75.22)，多语言 #1 (70.58)，0.6B/4B/8B 全系列 |
| 2 | **Jina Embeddings v5** | Jina AI | 2026 | 2602.15547 | 第五代多语言模型，677M 参数 MTEB 71.7，支持 119+ 语言，32K 上下文 |
| 3 | **Harrier: Open Multilingual Text Embedding Models** | Microsoft | 2025 | - | 基于 Gemma3，27B 参数 MTEB v2 74.3，MIT 开源，对比学习训练 |
| 4 | **Octen-Embedding** | Octen Team | 2025 | - | RTEB 排行榜 #1，行业垂直领域优化（法律/金融/医疗），基于 Qwen3-Embedding 微调 |
| 5 | **NV-Embed-v2** | NVIDIA | 2024 | 2405.17428 | 首个 MTEB 70+ 模型，Latent Attention Pooling，两阶段指令微调 |
| 6 | **NV-Embed (v1)** | NVIDIA | 2024 | 2407.15831 | LLM 作为通用 Embedding 模型的改进训练技术 |
| 7 | **GTE-Qwen2-7B-instruct** | Alibaba | 2024 | 2308.03281 | GTE 系列，中英文双榜 #1，双向注意力+指令微调 |
| 8 | **BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity** | BAAI | 2024 | 2402.03216 | Dense+ColBERT+Sparse 多功能 Embedding，多粒度检索 |
| 9 | **Voyage AI Embeddings** | Voyage AI | 2024 | 2402.11125 | 专为大模型 RAG 优化，商业 Embedding API 标杆 |
| 10 | **Cohere Embed v3** | Cohere | 2024 | 2402.09353 | 多语言 Embedding，支持 100+ 语言，长上下文 |
| 11 | **Nomic Embed Text v1.5** | Nomic AI | 2024 | 2402.01613 | 开源 137M 参数，Matryoshka 表征学习，可变维度 |
| 12 | **E5-Mistral-7B-Instruct** | Microsoft | 2024 | 2402.05672 | 基于 Mistral-7B 的指令微调 Embedding 模型 |
| 13 | **Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks | NLLP | 2019 | 1908.10084 | Sentence Transformers 奠基，对比学习 Embedding |
| 14 | **E5: Embeddings from Bidirectional Encoder Representations** | Microsoft | 2022 | 2212.03533 | 弱监督对比学习 Embedding，大规模预训练 |
| 15 | **MTEB: Massive Text Embedding Benchmark** | HuggingFace | 2022 | 2210.07316 | Embedding 评估基准，统一了 Embedding 模型评测标准 |

---

## 附录：MTEB 最新排名参考（2025年5月）

| 排名 | 模型 | MTEB Eng v2 | 多语言 | 参数量 |
|------|------|-------------|--------|--------|
| 1 | Qwen3-Embedding-8B | 75.22 | 70.58 | 8B |
| 2 | Qwen3-Embedding-4B | 74.60 | - | 4B |
| 3 | Harrier-oss-v1-27b | 74.3 | - | 27B |
| 4 | Qwen3-Embedding-0.6B | 70.70 | - | 0.6B |
| 5 | gte-Qwen2-7B-instruct | 70.72 | - | 7B |
| 6 | NV-Embed-v2 | 69.81 | - | ~7B |
| 7 | Jina-Embeddings-v5-text-small | 71.7 | 67.7 | 677M |
| - | Octen-Embedding-8B | - | RTEB #1 | 8B |
