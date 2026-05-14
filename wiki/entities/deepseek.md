---
title: DeepSeek 系列
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, open-source, llm, reasoning]
sources: [raw/papers/2401.02954-DeepSeek-LLM-Scaling-Open-Source-Language-Models-with-Longte.html, raw/papers/2405.04434-DeepSeek-V2-A-Strong-Economical-and-Efficient-Mixture-of-Exp.html, raw/papers/2412.19437-DeepSeek-V3-Technical-Report.html, raw/papers/2501.12948-DeepSeek-R1-Incentivizing-Reasoning-Capability-in-LLMs-via-R.html]
---

# DeepSeek 系列

DeepSeek 是深度求索公司（DeepSeek AI）发布的一系列开源大语言模型，以高性价比和创新架构著称。从 DeepSeek LLM 到 DeepSeek-V3 和 R1，该系列在推理能力和训练效率上持续突破。

## DeepSeek LLM（2024 年 1 月）

DeepSeek LLM 是系列首个基础模型，探索了长上下文场景下的 scaling 策略。[[raw/papers/2401.02954-DeepSeek-LLM-Scaling-Open-Source-Language-Models-with-Longte.html]]

- 参数规模：7B / 67B
- 训练数据：2T Token
- 提出了改进的 [[scaling-laws]]：在数据和参数之外引入上下文长度维度
- 支持长上下文（128K via [[long-context-extension]]）
- 强调代码和数学能力

## DeepSeek-V2（2024 年 5 月）

DeepSeek-V2 引入了 MLA（Multi-head Latent Attention）和 DeepSeekMoE 架构，大幅降低了推理成本。[[raw/papers/2405.04434-DeepSeek-V2-A-Strong-Economical-and-Efficient-Mixture-of-Exp.html]]

- 参数规模：236B 总参数，21B 激活参数
- **MLA**：将 KV 投影压缩到低秩隐空间（d_c = 512），KV Cache 减少 93.3%
- **DeepSeekMoE**：160 个路由专家（每 token 选 6 个）+ 2 个共享专家
- 训练成本仅为同等性能模型的 42.5%
- 在 MMLU/HumanEval/GSM8K 等基准上超越 [[mixtral]] 8x22B

## DeepSeek-V3（2024 年 12 月）

DeepSeek-V3 进一步优化了 MoE 架构和训练效率，以极低成本达到顶级性能。[[raw/papers/2412.19437-DeepSeek-V3-Technical-Report.html]]

- 671B 总参数，37B 激活参数（256 路由专家，每 token 选 8 个）
- **Multi-Token Prediction (MTP)**：同时预测多个未来 token，加速训练和推理
- **FP8 混合精度训练**：前向传播使用 FP8，减少通信开销
- **无辅助损失的负载均衡**：通过 bias 调整路由概率，避免辅助损失干扰主梯度
- 训练成本：仅 278.8 万 H800 GPU 小时（约$557 万），性能接近 Claude 3.5 Sonnet
- 上下文：预训练 4K → 渐进扩展至 128K（YaRN）

## DeepSeek-R1（2025 年 1 月）

DeepSeek-R1 是系列中最重要的突破——通过纯 RL 训练激发了模型的 Chain-of-Thought 推理能力。[[raw/papers/2501.12948-DeepSeek-R1-Incentivizing-Reasoning-Capability-in-LLMs-via-R.html]]

- **R1-Zero**：无 SFT 冷启动，仅用 RL（GRPO）训练即自动涌现推理链
  - 自动出现"Aha Moment"（自我纠错行为）
  - 思考 token 长度随训练自动增长
- **R1**：在 R1-Zero 基础上加入少量 SFT 冷启动 + 多阶段 RL
  - 推理能力可媲美 OpenAI o1-preview
  - AIME 2024 数学竞赛准确率 79.8%（超越 o1-mini）
- **GRPO**：Group Relative Policy Optimization，不需要 Critic Model，以组内相对奖励做归一化
- 开源蒸馏版本：1.5B/7B/8B/14B/32B/70B（基于 Qwen/LLaMA 底座）
- 核心贡献：证明 RL 可以直接涌现推理能力，不依赖人类标注的思考过程

## 架构创新总结

| 创新 | 首次引入 | 核心思想 |
|-----|---------|---------|
| MLA | V2 | 低秩压缩 KV，显存省 93% |
| DeepSeekMoE | V2 | 细粒度路由 + 共享专家 |
| 无辅助损失均衡 | V3 | Bias 动态调整，避免梯度干扰 |
| MTP | V3 | 多 token 预测，并行推理加速 |
| GRPO | R1 | 无 Critic RL，组级相对奖励 |

## 与其他模型对比

- [[llama]] 系列是 DeepSeek 在开源领域的主要竞争者
- [[qwen]] 系列在中文能力上与 DeepSeek 形成互补
- [[mixtral]] 的 MoE 路由策略与 DeepSeekMoE 有异曲同工之妙
- 与 [[test-time-compute]] 相关：R1 通过增加推理时的思考 token 量来提升性能

## 影响与意义

DeepSeek 系列证明了在有限资源下通过架构创新可以实现接近甚至超越闭源模型的性能。DeepSeek-R1 的推理能力突破直接推动了全球 AI 行业对推理模型（reasoning models）的关注，其 GRPO 训练范式成为后续推理模型的标准方法。V3 的极低训练成本更是引发了"AI 是否真需要天量算力"的行业讨论。
