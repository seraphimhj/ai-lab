# LLM 论文阅读清单

> 最后更新：2026年5月（重新整理：分门别类，类目内按演进路线从旧到新排序）  
> 用于构建 LLM 知识库 wiki，覆盖架构、训练、推理、对齐、长上下文、模型谱系、推理模型、多模态、Agent、RAG、Embedding、评测共 12 大方向。  
> 论文若跨多个方向，按"主家"放一处，需要时在其他方向用 `→ §X` 引用。

---

## 目录

- [一、基础架构与位置编码](#一基础架构与位置编码)
- [二、预训练与缩放定律](#二预训练与缩放定律)
- [三、指令微调与对齐](#三指令微调与对齐)
- [四、参数高效微调（PEFT）](#四参数高效微调peft)
- [五、推理加速与量化](#五推理加速与量化)
- [六、长上下文与新架构（含 SSM/线性注意力）](#六长上下文与新架构)
- [七、稀疏专家（MoE）](#七稀疏专家moe)
- [八、旗舰模型谱系](#八旗舰模型谱系)
- [九、推理模型与 Reasoning RL](#九推理模型与-reasoning-rl)
- [十、多模态 VLM 与生成](#十多模态-vlm-与生成)
- [十一、代码 LLM](#十一代码-llm)
- [十二、Agent 与工具使用](#十二agent-与工具使用)
- [十三、RAG / 检索增强](#十三rag--检索增强)
- [十四、Embedding 与 Reranker](#十四embedding-与-reranker)
- [十五、评测基准](#十五评测基准)

---

## 一、基础架构与位置编码

> Transformer 之后的架构主线 + 位置编码主线。

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | Attention Is All You Need | Google | 2017 | 1706.03762 | Transformer 奠基，自注意力替代 RNN/CNN |
| 2 | BERT: Pre-training of Deep Bidirectional Transformers | Google | 2018 | 1810.04805 | 双向预训练，NLP 的 ImageNet 时刻 |
| 3 | T5: Unified Text-to-Text Transformer | Google | 2019 | 1910.10683 | text-to-text 统一框架 |
| 4 | An Image is Worth 16x16 Words (ViT) | Google | 2020 | 2010.11929 | 视觉 Transformer 奠基 |
| 5 | RoFormer: Rotary Position Embedding (RoPE) | Zhuiyi | 2021 | 2104.09864 | RoPE 位置编码，主流 LLM 标配 |
| 6 | ALiBi: Train Short, Test Long | UW | 2021 | 2108.12409 | 线性偏置位置编码，长度外推 |
| 7 | Differential Transformer | Microsoft | 2024 | 2410.05258 | 差分注意力消除噪声，长上下文显著改进 |

---

## 二、预训练与缩放定律

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | GPT-2: Language Models are Unsupervised Multitask Learners | OpenAI | 2019 | 1905.11685 | 大模型零样本能力，规模效应 |
| 2 | Scaling Laws for Neural Language Models | OpenAI | 2020 | 2001.08361 | Kaplan 缩放定律奠基 |
| 3 | GPT-3: Language Models are Few-Shot Learners | OpenAI | 2020 | 2005.14165 | 175B + in-context learning 范式 |
| 4 | Chinchilla: Training Compute-Optimal LLMs | DeepMind | 2022 | 2203.15556 | 数据量 ≥ 模型大小，重定义训练策略 |
| 5 | Emergent Abilities of LLMs | Google/Stanford | 2022 | 2206.07682 | "涌现能力"概念奠基 |
| 6 | Scaling Data-Constrained LMs | DeepMind | 2022 | 2210.02414 | 数据受限下的缩放规律 |
| 7 | Pythia: A Suite for Analyzing LLMs Across Training | AI2 | 2023 | 2304.01373 | 训练全过程动态分析 |
| 8 | Speeeeeed! System Optimizations at Training-Scale | Anthropic | 2023 | 2402.07549 | 大规模训练系统工程 |
| 9 | Scaling Synthetic Data for LLMs | Microsoft | 2024 | 2406.08437 | 合成数据缩放规律 |
| 10 | Test-Time Compute Scaling Laws | Google | 2024 | 2408.03314 | 推理时计算缩放，重塑训练-推理平衡 |
| 11 | The Bitter Lesson of LLM RL Scaling | OpenAI/DeepMind | 2025 | - | RL 训练规模化的工程理论总结 |

---

## 三、指令微调与对齐

> 监督微调（SFT） → RLHF → AI 反馈/宪法 → DPO → 后训练 recipe。

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | Fine-tuning LMs from Human Preferences | OpenAI | 2019 | 1909.08593 | 偏好学习开创性工作，RLHF 理论基础 |
| 2 | Learning to Summarize from Human Feedback | OpenAI | 2020 | 2009.01325 | 基于人类反馈的 RL 实践 |
| 3 | InstructGPT: Training LMs to Follow Instructions | OpenAI | 2022 | 2203.02155 | RLHF 对齐范式首次大规模验证 |
| 4 | Training a Helpful and Harmless Assistant with RLHF | Anthropic | 2022 | 2204.05862 | RLHF 完整三阶段方法论 |
| 5 | Red Teaming Language Models to Reduce Harms | Anthropic | 2022 | 2209.07858 | 红队测试方法论 |
| 6 | The Flan Collection | Google | 2022 | 2210.11416 | 指令微调数据集设计 |
| 7 | Self-Instruct: Self-Generated Instructions | UW | 2022 | 2212.10560 | 自动生成指令数据 |
| 8 | Constitutional AI: Harmlessness from AI Feedback | Anthropic | 2022 | 2212.08073 | RLAIF 自我对齐 |
| 9 | Alpaca: Strong Replicable Instruction-Following | Stanford | 2023 | - (Blog) | Self-Instruct + LLaMA，低成本指令微调 |
| 10 | Vicuna: Open-Source Chatbot | LMSYS | 2023 | 2303.17580 | 基于 LLaMA 的指令微调标杆 |
| 11 | DPO: Direct Preference Optimization | Stanford | 2023 | 2305.18290 | 简化 RLHF，跳过奖励模型 |
| 12 | Secrets of RLHF in Large Language Models | Stanford | 2024 | 2407.05253 | RLHF 实践关键发现 |
| 13 | Tülu 3: Open Post-Training Recipe | AI2 | 2024 | 2411.15124 | SFT+DPO+RLVR 完整开源 recipe |

---

## 四、参数高效微调（PEFT）

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | LoRA: Low-Rank Adaptation | Microsoft | 2021 | 2106.09685 | 低秩适配，PEFT 事实标准 |
| 2 | QLoRA: Efficient Finetuning of Quantized LLMs | UW | 2023 | 2305.14314 | 4-bit 量化 + LoRA，单卡微调 65B |
| 3 | LongLoRA: Long-Context LLM Fine-tuning | UW | 2023 | 2309.12307 | 长上下文高效微调 |

---

## 五、推理加速与量化

> 训练侧 IO 优化 + 推理侧量化/剪枝/KV-Cache。

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | FlashAttention | Stanford | 2022 | 2205.14135 | IO-aware 注意力，2-4x 加速 |
| 2 | GPTQ: Post-Training Quantization for GPT | IST Austria | 2022 | 2210.17323 | 4-bit 量化，大模型推理加速 |
| 3 | SparseGPT: Massive LLMs Can Be Pruned | CMU | 2023 | 2301.00774 | 大模型单次剪枝 |
| 4 | AWQ: Activation-Aware Weight Quantization | UW | 2023 | 2306.00978 | 激活感知量化，4-bit 性能无损 |
| 5 | FlashAttention-2: Better Parallelism | Stanford | 2023 | 2307.08691 | 改进 FlashAttention，长序列支持 |
| 6 | vLLM (PagedAttention) | UC Berkeley | 2023 | 2309.06180 | KV-Cache 分页管理，推理引擎工业标准 |
| 7 | FlashAttention-3: Hardware-Aware on H100 | Stanford | 2024 | 2407.08608 | H100 上 1.5-2x 注意力加速 |
| 8 | Scaling KV-Cache for Efficient LLM Inference | Stanford | 2024 | 2409.12505 | KV-Cache 压缩，推理显存优化 |

---

## 六、长上下文与新架构

> 含 SSM、线性递归、Sparse Attention、长上下文外推。

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | RETRO: Retrieval-Enhanced Transformer | DeepMind | 2021 | 2112.04426 | 检索增强预训练（RAG 早期形态） |
| 2 | YaRN: Efficient Context Window Extension | UW | 2023 | 2309.00071 | 高效扩展至 128K+ |
| 3 | Ring Attention with Blockwise Transformers | UC Berkeley | 2023 | 2310.01889 | 分布式长上下文注意力 |
| 4 | Mamba: Selective State Space Models | CMU/Princeton | 2023 | 2312.00752 | 线性时间序列建模，挑战 Transformer |
| 5 | Griffin: Gated Linear Recurrences + Local Attention | Google | 2024 | 2402.19427 | 线性递归+局部注意力混合 |
| 6 | Jamba: Hybrid Transformer-Mamba | AI21 Labs | 2024 | 2403.19887 | 混合架构 256K 上下文 |
| 7 | LongContextChat | Google | 2024 | 2405.12195 | 长上下文对话微调，1M tokens |
| 8 | Mamba-2: Structured State Space Duality | CMU/Princeton | 2024 | 2405.07587 | SSM 与注意力结构对偶 |
| 9 | Titans: Learning to Memorize at Test Time | Google | 2025 | 2501.00663 | 神经记忆模块 + 测试时学习 |
| 10 | MiniMax-01 / Lightning Attention | MiniMax | 2025 | 2501.08313 | 4M 上下文工程化 |
| 11 | Native Sparse Attention (NSA) | DeepSeek | 2025 | 2502.11089 | 原生稀疏注意力，长上下文训推统一 |
| 12 | MoBA: Mixture of Block Attention | Moonshot | 2025 | 2502.13189 | Kimi 长上下文核心，块级 MoE 注意力 |

---

## 七、稀疏专家（MoE）

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | GShard: Scaling Giant Models with Conditional Computation | Google | 2020 | 2006.16668 | MoE 工程化先驱，自动分片 |
| 2 | Switch Transformer | Google | 2021 | 2101.03961 | 万亿参数 MoE 奠基 |
| 3 | Mixtral of Experts | Mistral AI | 2024 | 2401.04088 | 8x7B 稀疏专家开源 |
| 4 | DeepSeekMoE | DeepSeek | 2024 | 2401.06066 | 细粒度专家 + 共享专家 |
| 5 | SMoE: Scaling Sparse MoE | Google | 2024 | 2402.02603 | 稀疏 MoE 缩放规律 |
| 6 | DeepSeek-V2 (MLA + MoE) | DeepSeek | 2024 | 2405.04434 | MLA + MoE，训练推理成本骤降 |
| 7 | DeepSeek-V3 | DeepSeek | 2024 | 2412.19437 | 671B MoE + FP8 训练 |

---

## 八、旗舰模型谱系

> 按机构分组，每组内严格按时间从旧到新。

### 8.1 OpenAI 系

| # | 模型 | 年份 | arXiv | 主要贡献 |
|---|------|------|-------|---------|
| 1 | GPT-2 | 2019 | 1905.11685 | 见 §二 |
| 2 | GPT-3 | 2020 | 2005.14165 | 见 §二 |
| 3 | GPT-4 Technical Report | 2023 | 2303.08774 | 多模态大模型，接近人类考试水平 |
| 4 | GPT-4V(ision) System Card | 2023 | - | 多模态 GPT-4 |
| 5 | GPT-4o Technical Report | 2024 | - | 端到端多模态实时交互 |
| 6 | o1 System Card | 2024 | - | 推理模型时代开启 |
| 7 | o3 / o4-mini | 2025 | - | ARC-AGI 突破 |
| 8 | GPT-5 System Card | 2025 | - | 统一推理与对话路由，多模态原生 |

### 8.2 Anthropic 系（Claude）

| # | 模型 | 年份 | arXiv | 主要贡献 |
|---|------|------|-------|---------|
| 1 | Claude 3 Technical Report | 2024 | - | Opus/Sonnet/Haiku 三模型，200K 上下文 |
| 2 | Claude 3.5 Sonnet | 2024 | - | 编码与推理代际跃升 |
| 3 | Extended Thinking | 2024 | - | 透明推理过程 |
| 4 | Claude 3.7 Sonnet | 2025 | - | 首个混合推理模型，可控思考预算 |
| 5 | Claude 4 (Opus / Sonnet) | 2025 | - | 编码与 Agent 能力代际跃升，SWE-Bench 突破 |

### 8.3 Google / DeepMind 系

| # | 模型 | 年份 | arXiv | 主要贡献 |
|---|------|------|-------|---------|
| 1 | PaLM: Scaling LM with Pathways | 2022 | 2204.02311 | 540B Pathways 训练突破 |
| 2 | Gemini 1.0 / 1.5 Pro | 2023-24 | 2312.11805 / 2403.05530 | 原生多模态 + 1M 上下文 |
| 3 | Gemma | 2024 | 2403.08295 | 基于 Gemini 的开源家族 |
| 4 | Gemma 2 | 2024 | 2406.08414 | 知识蒸馏 + 滑动窗口注意力 |
| 5 | Gemma 3 | 2025 | 2503.21428 | 原生多模态 + 推理增强 |
| 6 | Gemini 2.5 Pro | 2025 | 2507.06261 | 1M+ 上下文，原生多模态推理 |

### 8.4 Meta 系（LLaMA）

| # | 模型 | 年份 | arXiv | 主要贡献 |
|---|------|------|-------|---------|
| 1 | LLaMA | 2023 | 2302.13971 | 开源 7B-65B 奠基 |
| 2 | LLaMA 2 | 2023 | 2307.09288 | 开源商用许可 |
| 3 | Llama 3 Herd | 2024 | 2407.21783 | 8B/70B/405B |
| 4 | Llama 3.1 | 2024 | 2407.21783 | 405B + 128K 上下文 |
| 5 | Llama 3.2 (含 Vision) | 2024 | 2409.11771 | 1B/3B/11B/90B + 多模态 |
| 6 | Llama 4 (Behemoth/Maverick/Scout) | 2025 | 2504.06189 | MoE 旗舰，原生多模态，10M 上下文 |

### 8.5 中国开源旗舰

| # | 模型 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | Qwen Technical Report | Alibaba | 2024 | 2309.16609 | Qwen 1 系列 |
| 2 | DeepSeek LLM | DeepSeek | 2024 | 2401.02954 | 多阶段训练策略 |
| 3 | Yi: Open Foundation Models | 01.AI | 2024 | 2403.04652 | 高质量双语开源 |
| 4 | MiniCPM-V | Tsinghua | 2024 | 2404.10515 | 端侧多模态，手机可运行 |
| 5 | GLM-4 Technical Report | Zhipu AI | 2024 | 2406.12793 | 中英双语 + 工具调用 |
| 6 | Hunyuan-Large / Hunyuan-T1 | Tencent | 2024-25 | 2411.02265 | 389B MoE 中文旗舰 |
| 7 | Qwen2.5 | Alibaba | 2025 | 2501.05736 | 0.5B-72B 全系列 |
| 8 | DeepSeek-R1 | DeepSeek | 2025 | 2501.12948 | → §九 推理模型 |
| 9 | Kimi K1.5 | Moonshot | 2025 | 2501.12599 | → §九 推理模型 |
| 10 | Qwen2.5-Coder | Alibaba | 2025 | 2502.13930 | → §十一 代码 LLM |
| 11 | Qwen3 | Alibaba | 2025 | 2502.13999 | 混合思维模型，MoE |
| 12 | QwQ-32B / QwQ-Max | Alibaba | 2025 | - | 中等规模强推理开源 |
| 13 | Qwen3 / Qwen3-Max | Alibaba | 2025 | 2505.09388 | Dense+MoE 全谱系，1T MoE |
| 14 | Kimi K2: Open Agentic Intelligence | Moonshot | 2025 | 2507.20534 | 1T MoE 开源 Agent 模型 |
| 15 | DeepSeek-V3.1 / V3.2 | DeepSeek | 2025 | 2509.18786 | 混合推理 + Sparse Attention |
| 16 | DeepSeek-R1.5 / R2 | DeepSeek | 2025 | - | 推理长度可控 + 工具调用 |

### 8.6 其他开源（Mistral / Microsoft Phi / NVIDIA / AI2 / xAI / 端侧）

| # | 模型 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | Phi-2 | Microsoft | 2023 | 2309.05463 | 2.7B 高质量数据训练 |
| 2 | Mistral 7B | Mistral AI | 2023 | 2310.06825 | 7B 超越 Llama 2 13B |
| 3 | Phi-3 | Microsoft | 2024 | 2404.14219 | 3.8B 小模型飞跃 |
| 4 | Nemotron-4 340B | NVIDIA | 2024 | 2406.11704 | 合成数据训练旗舰 |
| 5 | Grok-2 | xAI | 2024 | 2408.03314 | 140B+ 大规模训练 |
| 6 | Phi-4 | Microsoft | 2024 | 2412.08568 | 14B 教科书级数据 |
| 7 | OLMo 2 | AI2 | 2024 | 2501.00656 | 完全开源（数据+权重+代码） |
| 8 | SmolLM2 / SmolLM3 | HuggingFace | 2025 | 2502.02737 | 端侧小模型最佳实践 |
| 9 | Phi-4-mini / Phi-4-multimodal | Microsoft | 2025 | 2503.01743 | 端侧多模态小模型 |
| 10 | Mistral Small 3 / Medium 3 | Mistral AI | 2025 | - | 中小模型新版，性能/成本平衡 |

---

## 九、推理模型与 Reasoning RL

> Prompt 时代（CoT 系列）→ 推理时缩放（o1）→ 纯 RL 激发（R1/K1.5）→ 简化复刻（s1/rStar）→ 工业 RL 系统。

### 9.1 Prompt-time 推理方法

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | Chain-of-Thought Prompting | Google | 2022 | 2201.11903 | CoT 推理范式奠基 |
| 2 | Self-Consistency Improves CoT | Google | 2022 | 2203.11171 | 投票一致性，CoT 标配 |
| 3 | STaR: Self-Taught Reasoner | Stanford | 2022 | 2203.14465 | 自举推理训练 |
| 4 | ReAct: Reasoning + Acting | Princeton | 2022 | 2210.03629 | 推理+行动协同（也是 Agent 基石） |
| 5 | Reflexion: Verbal RL for Reasoning | Northeastern | 2023 | 2303.11366 | 自我反思 + 语言反馈 |
| 6 | Self-Refine: Iterative Self-Feedback | CMU | 2023 | 2303.17651 | 自我精炼范式 |
| 7 | Tree of Thoughts | Princeton | 2023 | 2305.10601 | 树状搜索推理 |
| 8 | Let's Verify Step by Step (PRM) | OpenAI | 2023 | 2305.20050 | 过程奖励模型 |

### 9.2 RL-based 推理与推理时缩放

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | DeepSeekMath / GRPO | DeepSeek | 2024 | 2402.03300 | GRPO 算法，R1 系列基础 |
| 2 | Mathematical Reasoning with LLMs | Google | 2024 | 2402.14036 | AlphaGeometry 后的数学推理 |
| 3 | STaR Bootstrapping Reasoning with Reasoning | Stanford | 2024 | 2403.04692 | 自举推理训练演进 |
| 4 | Reasoning is Planning with World Model | Google | 2024 | 2405.01451 | 推理即规划视角 |
| 5 | OpenAI o1 System Card | OpenAI | 2024 | - | 推理模型时代开启 |
| 6 | Process Reward Models in Math Reasoning | Tsinghua/OpenAI | 2024 | 2410.08146 | 数学 PRM 系统综述 |
| 7 | DeepSeek-R1: Reasoning via RL | DeepSeek | 2025 | 2501.12948 | 纯 RL 激发推理，开源标杆 |
| 8 | rStar-Math: Self-Evolved Deep Thinking | Microsoft | 2025 | 2501.04519 | 小模型 + MCTS + 自进化 |
| 9 | Kimi K1.5: Long-CoT RL | Moonshot | 2025 | 2501.12599 | 128K 思维链 RL |
| 10 | s1: Simple Test-Time Scaling | Stanford | 2025 | 2501.19393 | 1K 数据 + budget forcing 复刻 o1 |
| 11 | DAPO: Open-Source LLM RL System at Scale | ByteDance | 2025 | 2503.14476 | GRPO 改进，工业级开源 |
| 12 | RLVR Survey: Verifiable Rewards | 多机构 | 2025 | 2509.02547 | 可验证奖励 RL 全景综述 |

---

## 十、多模态 VLM 与生成

> 视觉-语言对齐 → 指令式 VLM → 原生多模态 → 视频/图像生成 → 统一自回归。

### 10.1 视觉-语言对齐与早期 VLM

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | CLIP: Learning Transferable Visual Models | OpenAI | 2021 | 2103.00020 | 视觉-语言对齐奠基 |
| 2 | Flamingo | DeepMind | 2022 | 2204.14198 | 少样本 VLM 范式奠基 |
| 3 | Whisper | OpenAI | 2022 | 2212.04356 | 多语种 ASR 奠基 |
| 4 | BLIP-2 (Q-Former) | Salesforce | 2023 | 2301.12597 | Q-Former 桥接，工业 VLM 基座 |
| 5 | LLaVA: Visual Instruction Tuning | Wisconsin | 2023 | 2304.08485 | 视觉指令微调开源标杆 |
| 6 | MiniGPT-4 | KAUST | 2023 | 2304.10592 | 早期开源 VLM |
| 7 | Video-LLaMA / Video-ChatGPT | NTU/MBZUAI | 2023 | 2306.02858 / 2306.05424 | 视频理解 VLM 早期代表 |
| 8 | Qwen-VL | Alibaba | 2023 | 2308.12966 | 中文 VLM 系列起点 |
| 9 | LLaVA-1.5 / LLaVA-NeXT | Wisconsin | 2023-24 | 2310.03744 | LLaVA 改进系列 |
| 10 | InternVL | Shanghai AI Lab | 2023 | 2312.14238 | 视觉编码器规模化 |

### 10.2 原生多模态与开源旗舰

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | Idefics 2 / Idefics 3 | HuggingFace | 2024 | 2405.02246 | 开源 VLM 工程范式 |
| 2 | NVLM: Open Frontier-Class VLMs | NVIDIA | 2024 | 2409.11402 | 开源 VLM 旗舰 |
| 3 | Qwen2-VL / Qwen2.5-VL | Alibaba | 2024-25 | 2409.12191 | 原生分辨率，中文最强开源 VLM |
| 4 | Molmo and PixMo | AI2 | 2024 | 2409.17146 | 完全开源 + 高质量人工数据 |
| 5 | Pixtral 12B / Pixtral Large | Mistral | 2024 | 2410.07073 | 开源多模态旗舰 |
| 6 | InternVL 2.5 / InternVL3 | Shanghai AI Lab | 2024-25 | 2504.10479 | 开源 VLM 旗舰 |

### 10.3 图像/视频生成

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | Sora Technical Report | OpenAI | 2024 | - | 文生视频里程碑 |
| 2 | Stable Diffusion 3 / FLUX.1 | Stability/BFL | 2024 | 2403.03206 | DiT 架构图像生成新旗舰 |
| 3 | Emu3: Next-Token Prediction is All You Need | BAAI | 2024 | 2409.18869 | 统一自回归多模态生成 |
| 4 | Veo 3 / Veo 4 | Google | 2025 | - | 长时序高保真视频生成 |

---

## 十一、代码 LLM

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | Codex / HumanEval | OpenAI | 2021 | 2107.03374 | 代码 LLM 与 HumanEval 评测奠基 |
| 2 | StarCoder: May the Source Be with You | BigCode | 2023 | 2305.06161 | 大规模开源代码 LLM |
| 3 | Qwen2.5-Coder | Alibaba | 2025 | 2502.13930 | 代码竞赛级表现，开源旗舰 |

> Devin / SWE-agent 等代码 Agent 见 §十二。

---

## 十二、Agent 与工具使用

> 工具调用 → 单 Agent 推理-行动循环 → 多 Agent 协作 → SWE Agent → 通用 Computer Use Agent。

### 12.1 工具调用与单 Agent 范式

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | ReAct: Reasoning + Acting | Princeton | 2022 | 2210.03629 | Agent 范式奠基（→ §九） |
| 2 | Toolformer: LMs Teach Themselves to Use Tools | Meta | 2023 | 2302.04761 | LLM 自主工具调用首次系统化 |
| 3 | HuggingGPT | Zhejiang Univ | 2023 | 2303.17580 | LLM 调度多个 AI 模型 |
| 4 | AutoGPT | Significant Gravitas | 2023 | - | 自主 AI Agent 先驱 |

### 12.2 多 Agent 协作 / 模拟

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | CAMEL: Communicative Agents | KAUST | 2023 | 2303.17760 | 角色扮演式 Agent 协作 |
| 2 | Generative Agents | Stanford | 2023 | 2304.03442 | 25 Agent 小镇社会模拟 |
| 3 | Voyager: Embodied Agent in Minecraft | NVIDIA/Caltech | 2023 | 2305.16291 | 开放世界终身学习 |
| 4 | MetaGPT: Multi-Agent SOP | DeepWisdom | 2023 | 2308.00352 | 多 Agent SOP 协作框架 |
| 5 | AutoGen | Microsoft | 2023 | 2308.08155 | 多 Agent 对话框架事实标准 |
| 6 | Magentic-One: Generalist Multi-Agent | Microsoft | 2024 | 2411.04468 | 通用多 Agent 编排 |

### 12.3 软件工程 Agent

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | SWE-Bench | Princeton | 2023 | 2310.06770 | 真实 GitHub Issues 评测金标准 |
| 2 | SWE-agent (ACI) | Princeton | 2024 | 2405.15793 | Agent Computer Interface 设计 |
| 3 | Devin Technical Report | Cognition | 2024 | - | 首个商业化 SWE Agent |
| 4 | OpenDevin / OpenHands | UIUC/CMU | 2024 | 2407.16741 | 开源通用 SWE Agent 平台 |

### 12.4 Web / 通用 Computer Use Agent

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | GAIA: General AI Assistants Benchmark | Meta/HuggingFace | 2023 | 2311.12983 | 通用 AI 助手评测 |
| 2 | Browser Use / WebVoyager / WebArena | 多机构 | 2024 | 2401.13649 | 浏览器 Agent 工程范式 |
| 3 | AgentQ: Autonomous Web Agent | Stanford | 2024 | 2405.10614 | RL + 反思的 Web Agent |
| 4 | Anthropic Computer Use | Anthropic | 2024 | - | Claude 操作计算机 |
| 5 | OpenAI Operator System Card | OpenAI | 2025 | - | OpenAI 浏览器 Agent |
| 6 | Manus AI Technical Overview | Monica | 2025 | - | 通用 Agent 产品化 |
| 7 | Agent S2: Generalist-Specialist Framework | Simular AI | 2025 | 2504.00906 | 通用-专家组合 Agent |

---

## 十三、RAG / 检索增强

> 经典稠密检索 → RAG 算法主线 → 上下文工程 → 图 RAG → Reranker → 框架 → 评测综述。

### 13.1 检索基础

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | DPR: Dense Passage Retrieval | Facebook | 2020 | 2004.04906 | 稠密检索经典 |
| 2 | ColBERT: Late Interaction | Stanford | 2020 | 2004.12832 | token 级细粒度匹配 |
| 3 | SPLADE: Sparse Lexical Expansion | Télécom Paris | 2021 | 2109.10086 | 稀疏可解释检索 |

### 13.2 RAG 算法主线（按时间）

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | REALM: Retrieval-Augmented Pre-Training | Google | 2020 | 2002.08909 | 预训练阶段引入检索 |
| 2 | RAG: Knowledge-Intensive NLP | Meta | 2020 | 2005.11401 | RAG 开山之作 |
| 3 | FiD: Fusion-in-Decoder | Facebook | 2020 | 2007.01282 | 工程基线 |
| 4 | RETRO: Retrieval-Enhanced Transformer | DeepMind | 2021 | 2112.04426 | （→ §六） |
| 5 | Atlas: Few-shot RAG LMs | Meta | 2022 | 2208.03299 | 检索增强少样本学习集大成 |
| 6 | HyDE: Zero-Shot Dense Retrieval | CMU | 2022 | 2212.10496 | 假设性文档 Embedding |
| 7 | IRCoT: Interleaving Retrieval with CoT | UW | 2023 | 2305.06683 | 推理与检索交替 |
| 8 | FLARE: Active RAG | CMU | 2023 | 2305.06983 | 前瞻式主动检索 |
| 9 | Self-RAG | UW | 2023 | 2310.11511 | 自主判断是否检索 |
| 10 | RA-DIT: Dual Instruction Tuning | Meta | 2023 | 2310.01352 | 检索器+生成器联合微调 |
| 11 | ChatQA | NVIDIA | 2024 | 2401.10225 | 对话式 RAG SOTA |
| 12 | CRAG: Corrective RAG | PSU | 2024 | 2401.15884 | 检索纠错，动态触发 Web |
| 13 | RAG-Fusion (RRF) | Microsoft | 2023 | 2402.03367 | 多查询 RRF 融合 |
| 14 | Chain-of-Note | 东南大学 | 2024 | 2402.14557 | 检索笔记链 |
| 15 | RAFT: Domain-Specific RAG Fine-tuning | UC Berkeley | 2024 | 2403.10131 | 干扰文档训练 |
| 16 | Adaptive-RAG | KAIST | 2024 | 2403.14403 | 自适应检索策略 |
| 17 | Corrective RAG with Self-Reflection | 多机构 | 2024 | 2405.05867 | 自反思纠错 |
| 18 | LongRAG | Waterloo | 2024 | 2406.15319 | 长上下文 LLM 重塑 RAG |
| 19 | Best Practices in RAG | 多机构 | 2024 | 2407.01219 | 各组件最佳实践对比 |
| 20 | Agentic RAG (LangGraph) | LangChain | 2024 | 2407.14647 | 动态路由+工具+多步检索 |
| 21 | RAG vs Long Context | Google DeepMind | 2024 | 2407.16833 | 长上下文 vs RAG，结论：互补 |

### 13.3 上下文工程：分块、改写、长程

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | Query Rewriting (Rewrite-Retrieve-Read) | Microsoft | 2023 | 2305.14283 | 查询改写范式 |
| 2 | Lost in the Middle | Stanford | 2023 | 2307.03172 | 中段信息丢失，排序基础 |
| 3 | RAPTOR: Recursive Tree Retrieval | Stanford | 2024 | 2401.18059 | 递归摘要树，分层检索 |
| 4 | Query Expansion for RAG | 多机构 | 2024 | 2402.13389 | 查询扩展综述 |
| 5 | Chunking Strategies for RAG | 多机构 | 2024 | 2405.10880 | 文本分块策略对比 |
| 6 | Late Chunking | Jina AI | 2024 | 2409.04701 | 先编码再分块，保留上下文 |
| 7 | Anthropic Contextual Retrieval | Anthropic | 2024 | - (Blog) | 上下文化分块 + BM25，召回错误降 49% |

### 13.4 知识图谱与图 RAG

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | MemGPT: LLMs as Operating Systems | UC Berkeley | 2023 | 2310.08560 | 内存分页范式，长期记忆 |
| 2 | GraphRAG: Local to Global KG-RAG | Microsoft | 2024 | 2404.16130 | 知识图谱增强 RAG |
| 3 | HippoRAG: Neurobiologically Inspired | OSU | 2024 | 2405.14831 | 海马体启发的图 RAG，多跳推理 |
| 4 | KAG: Knowledge-Augmented Generation | Ant Group | 2024 | 2409.13731 | 蚂蚁知识增强生成框架 |
| 5 | LightRAG | HKU | 2024 | 2410.05779 | 双层检索 + 增量索引 |
| 6 | PathRAG: Pruning Graph-based RAG | HKU | 2025 | 2502.14902 | 关系路径剪枝 |

### 13.5 Reranker / 重排序

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | RankGPT: ChatGPT as Re-Ranker | RUC | 2023 | 2304.09542 | LLM 作为重排序器开创 |
| 2 | BGE Reranker / v2 | BAAI | 2023-24 | 2402.03216 | 开源 Reranker 事实标准 |
| 3 | Cohere Rerank 3 / 3.5 | Cohere | 2024 | - | 商业 Reranker API 标杆 |
| 4 | Jina Reranker v2 | Jina AI | 2024 | - | 100+ 语言 Reranker |
| 5 | Qwen3-Reranker | Alibaba | 2025 | 2506.05176 | MTEB Reranking #1 |

### 13.6 RAG 工程框架

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | LlamaIndex Data Framework | LlamaIndex | 2024 | - | 索引/查询/路由工程标准 |
| 2 | Haystack: NLP Search Pipelines | deepset | 2024 | 2402.15955 | 端到端搜索管道 |

### 13.7 评测、综述与前沿

| # | 论文 | 机构 | 年份 | arXiv | 主要贡献 |
|---|------|------|------|-------|---------|
| 1 | RAGAS: Automated RAG Evaluation | Exploding Gradients | 2023 | 2309.15217 | RAG 评测事实标准 |
| 2 | ARES: Automated RAG Evaluation | Stanford | 2023 | 2311.09476 | 合成数据 + 评分模型 |
| 3 | RAG for AI-Generated Content Survey | 多机构 | 2024 | 2402.19473 | 跨模态 RAG 综述 |
| 4 | Pay Attention to RAG: Survey | Stanford | 2024 | 2404.10909 | RAG 系统全面综述 |
| 5 | TruLens / TruLens-Eval | TruEra | 2024 | - | RAG 三角评测框架 |
| 6 | A Survey on RAG Meeting LLMs | 多机构 | 2024 | 2405.06211 | 2024 全景综述 |

---

## 十四、Embedding 与 Reranker

> 早期对比学习 → BERT-based 监督训练 → LLM-based Embedding → 多模态/代码 Embedding。
> （Reranker 已并入 §13.5；本章只列 Embedding 模型论文。）

### 14.1 早期对比学习与 BERT-based

| # | 论文/模型 | 机构 | 年份 | arXiv | 主要贡献 |
|---|----------|------|------|-------|---------|
| 1 | Sentence-BERT | NLLP | 2019 | 1908.10084 | Sentence Transformers 奠基 |
| 2 | SimCSE | Princeton | 2021 | 2104.08821 | 对比学习句向量，dropout 正样本 |
| 3 | Contriever | Meta | 2021 | 2112.09118 | 无监督对比学习检索器 |
| 4 | GTR: Large Dual Encoders | Google | 2021 | 2112.07899 | 检索器规模化研究 |
| 5 | Matryoshka Representation Learning | UW/Google | 2022 | 2205.13147 | 嵌套表征，可变维度 Embedding |
| 6 | E5: Bidirectional Embeddings | Microsoft | 2022 | 2212.03533 | 弱监督对比学习，大规模预训练 |
| 7 | INSTRUCTOR: One Embedder, Any Task | HKU | 2022 | 2212.09741 | 指令式 Embedding 开创 |
| 8 | text-embedding-ada-002 / text-embedding-3 | OpenAI | 2022/24 | - | 商业 API 标杆 |
| 9 | Nomic Embed Text v1.5 | Nomic AI | 2024 | 2402.01613 | 137M 开源 + Matryoshka |

### 14.2 LLM-based Embedding（解码器改造为 Encoder）

| # | 论文/模型 | 机构 | 年份 | arXiv | 主要贡献 |
| 1 | RepLLaMA / RankLLaMA | Waterloo | 2023 | 2310.08319 | LLaMA 改造稠密检索器 + Reranker |
| 2 | E5-Mistral-7B-Instruct | Microsoft | 2024 | 2402.05672 | Mistral-7B 指令微调 Embedding |
| 3 | GritLM: Generative Representational Instruction Tuning | Contextual AI | 2024 | 2402.09906 | 生成与表征统一训练 |
| 4 | Echo Embeddings | UCSD | 2024 | 2402.15449 | 重复输入双向上下文，简化 LLM Embedding |
| 5 | LLM2Vec | McGill | 2024 | 2404.05961 | 解码器 LLM → Embedding 标准方案 |
| 6 | NV-Embed (v1) | NVIDIA | 2024 | 2407.15831 | LLM 作通用 Embedding 训练技术 |
| 7 | NV-Embed-v2 | NVIDIA | 2024 | 2405.17428 | 首个 MTEB 70+，Latent Attention Pooling |
| 8 | Promptriever | Cornell | 2024 | 2409.11136 | 可 prompt 的检索器 |
| 9 | NV-Retriever / NV-Embed-v3 | NVIDIA | 2025 | - | NV 系列后续，融合 reranker 训练 |

### 14.3 通用 Embedding 旗舰（中英/多语言）

| # | 论文/模型 | 机构 | 年份 | arXiv | 主要贡献 |
|---|----------|------|------|-------|---------|
| 1 | GTE-Qwen2-7B-instruct | Alibaba | 2024 | 2308.03281 | GTE 系列，中英文双榜 #1 |
| 2 | BGE M3-Embedding | BAAI | 2024 | 2402.03216 | Dense+ColBERT+Sparse 多功能多粒度 |
| 3 | Voyage AI Embeddings | Voyage AI | 2024 | 2402.11125 | 商业 Embedding API 标杆 |
| 4 | Cohere Embed v3 | Cohere | 2024 | 2402.09353 | 100+ 语言 |
| 5 | Stella Embedding | NovaSearch | 2024 | - | 中英文双榜常驻 Top |
| 6 | Gemini Embedding | Google | 2024 | 2407.19669 | Gemini 体系内 Embedding |
| 7 | Jina Embeddings v3 | Jina AI | 2024 | 2409.10173 | 8K 上下文 + 任务 LoRA 适配器 |
| 8 | BGE Multilingual Gemma2 | BAAI | 2024 | - | 基于 Gemma 2 9B 多语言 |
| 9 | Snowflake Arctic Embed v2.0 | Snowflake | 2024 | 2412.04506 | Apache-2.0 多语言企业级 |
| 10 | mxbai-embed-large-v1 / v2 | Mixedbread AI | 2024 | 2412.21154 | 二值量化友好 |
| 11 | Voyage 3 / 3 large / Code 3 | Voyage AI | 2024-25 | - | 商业旗舰系列，含代码专用 |
| 12 | GTE-ModernBERT | Alibaba | 2025 | - | 基于 ModernBERT，长上下文友好 |
| 13 | Cohere Embed v4 | Cohere | 2025 | - | 多模态（图文统一），128K 上下文 |
| 14 | Harrier (Gemma3-based) | Microsoft | 2025 | - | 27B MIT 开源，MTEB v2 74.3 |
| 15 | Octen-Embedding | Octen Team | 2025 | - | RTEB #1，垂直领域优化 |
| 16 | Qwen3-Embedding | Alibaba | 2025 | 2506.05176 | MTEB Eng v2 #1 (75.22)，多语言 #1 |
| 17 | Jina Embeddings v5 | Jina AI | 2026 | 2602.15547 | 第五代多语言，119+ 语言，32K 上下文 |

### 14.4 多模态与代码 Embedding

| # | 论文/模型 | 机构 | 年份 | arXiv | 主要贡献 |
|---|----------|------|------|-------|---------|
| 1 | SigLIP | Google | 2023 | 2303.15343 | CLIP 的 Sigmoid loss 改进 |
| 2 | CodeT5+ / CodeRankEmbed | Salesforce | 2023-24 | 2305.07922 | 代码 Embedding 专用 |
| 3 | E5-V: Universal Multimodal Embeddings | Beijing AI | 2024 | 2407.12580 | 基于 MLLM 的统一多模态 |
| 4 | SigLIP 2 | Google | 2025 | 2502.14786 | 多模态 Embedding 新标杆 |

---

## 十五、评测基准

| # | 评测 | 机构 | 年份 | arXiv | 覆盖能力 |
|---|------|------|------|-------|---------|
| 1 | MMLU: Multitask Language Understanding | UC Berkeley | 2020 | 2009.03300 | 通用知识评测事实标准 |
| 2 | HumanEval（含 Codex 论文） | OpenAI | 2021 | 2107.03374 | 代码生成 |
| 3 | MTEB: Massive Text Embedding Benchmark | HuggingFace | 2022 | 2210.07316 | Embedding 评测事实标准 |
| 4 | RAGAS | Exploding Gradients | 2023 | 2309.15217 | RAG 评测（也见 §13.7） |
| 5 | SWE-Bench | Princeton | 2023 | 2310.06770 | 软件工程 Agent（也见 §12.3） |
| 6 | GAIA | Meta/HuggingFace | 2023 | 2311.12983 | 通用 AI 助手（也见 §12.4） |
| 7 | MMTEB / MIEB | 多机构 | 2025 | 2502.13595 | MTEB 多语言 + 多模态扩展 |
| 8 | Agentic Benchmarks (BrowseComp / SWE-Bench Verified 等) | 多机构 | 2024-25 | - | Agent 三大事实基准合集 |

---

## 附录 A：MTEB 最新排名参考（2025年5月）

| 排名 | 模型 | MTEB Eng v2 | 多语言 | 参数量 |
|------|------|-------------|--------|--------|
| 1 | Qwen3-Embedding-8B | 75.22 | 70.58 | 8B |
| 2 | Qwen3-Embedding-4B | 74.60 | - | 4B |
| 3 | Harrier-oss-v1-27b | 74.3 | - | 27B |
| 4 | gte-Qwen2-7B-instruct | 70.72 | - | 7B |
| 5 | Qwen3-Embedding-0.6B | 70.70 | - | 0.6B |
| 6 | NV-Embed-v2 | 69.81 | - | ~7B |
| 7 | Jina-Embeddings-v5-text-small | 71.7 | 67.7 | 677M |
| - | Octen-Embedding-8B | - | RTEB #1 | 8B |

---

## 附录 B：本次重整说明（2026.5）

**结构变化**：
- 由原 7 大方向拆分整合为 **15 大方向**，类目内严格按时间从旧到新排序
- 旗舰模型（§八）按机构子分组（OpenAI / Anthropic / Google / Meta / 中国开源 / 其他开源）
- 推理模型（§九）拆为 Prompt-time 推理方法 + RL-based 推理两条线
- 多模态（§十）拆为对齐与早期 VLM、原生多模态、生成模型三条线
- Agent（§十二）拆为工具调用、多 Agent、SWE Agent、Computer Use Agent 四条演进线
- RAG（§十三）按"检索基础 → 算法主线 → 上下文工程 → 图 RAG → Reranker → 框架 → 评测"7 个子组
- Embedding（§十四）拆为对比学习经典、LLM-based、通用旗舰、多模态/代码 4 个子组
- 新增 §十一 代码 LLM、§十五 评测基准 两个独立分类

**编辑原则**：
- 同一论文不重复列出（如 ReAct、GRPO 等跨方向论文，主家放一处，他处用 `→ §X` 引用）
- 每行格式统一：`# | 论文 | 机构 | 年份 | arXiv | 主要贡献`
- 每个子表内严格按发表年份/版本时间从旧到新

**未补充**（如需可加）：
- 安全对齐（Sleeper Agents / Alignment Faking / Scalable Oversight）
- 工业训练系统（Megatron-LM / DeepSpeed / ZeRO / FSDP）
- 数据工程（FineWeb / DCLM / Common Crawl 工艺）
