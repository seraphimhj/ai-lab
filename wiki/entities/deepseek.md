---
title: DeepSeek 系列
created: 2026-05-10
updated: 2026-05-10
type: entity
tags: [model, open-source, llm, reasoning]
sources: [raw/papers/2401.02954-DeepSeek-LLM-Scaling-Open-Source-Language-Models-with-Longte.md, raw/papers/2405.04434-DeepSeek-V2-A-Strong-Economical-and-Efficient-Mixture-of-Exp.md, raw/papers/2412.19437-DeepSeek-V3-Technical-Report.md, raw/papers/2501.12948-DeepSeek-R1-Incentivizing-Reasoning-Capability-in-LLMs-via-R.md]
---

# DeepSeek 系列

DeepSeek 是深度求索公司（DeepSeek AI）发布的一系列开源大语言模型，以高性价比和创新架构著称。从 DeepSeek LLM 到 DeepSeek-V3 和 R1，该系列在推理能力和训练效率上持续突破。

## DeepSeek LLM（2024 年 1 月）

DeepSeek LLM 是系列首个基础模型，探索了长上下文场景下的 scaling 策略。[[raw/papers/2401.02954-DeepSeek-LLM-Scaling-Open-Source-Language-Models-with-Longte.html]]

- 参数规模：7B / 67B
- 训练数据：2T Token
- 支持长上下文（128K）
- 强调代码和数学能力

## DeepSeek-V2（2024 年 5 月）

DeepSeek-V2 引入了 MLA（Multi-head Latent Attention）和 DeepSeekMoE 架构，大幅降低了推理成本。[[raw/papers/2405.04434-DeepSeek-V2-A-Strong-Economical-and-Efficient-Mixture-of-Exp.html]]

- 参数规模：236B 总参数，21B 激活参数
- MLA 替代标准 MHA，减少 KV Cache 开销
- DeepSeekMoE 实现细粒度专家路由
- 训练成本仅为 LLaMA 2 70B 的 1/5

## DeepSeek-V3（2024 年 12 月）

DeepSeek-V3 进一步优化了 MoE 架构和训练效率。[[raw/papers/2412.19437-DeepSeek-V3-Technical-Report.html]]

- 671B 总参数，37B 激活参数
- Multi-Token Prediction (MTP) 辅助训练
- FP8 混合精度训练
- 无辅助损失的负载均衡策略

## DeepSeek-R1（2025 年 1 月）

DeepSeek-R1 是系列中最重要的突破，通过纯 RL 训练激发了模型的 Chain-of-Thought 推理能力，无需 SFT 即可获得强推理性能。[[raw/papers/2501.12948-DeepSeek-R1-Incentivizing-Reasoning-Capability-in-LLMs-via-R.html]]

- 基于 GRPO（Group Relative Policy Optimization）强化学习
- 自动涌现 Aha Moment（顿悟时刻）
- 推理能力可媲美 OpenAI o1
- 开源了 R1-Zero 和 R1 两个版本

## 与其他模型对比

- [[llama]] 系列是 DeepSeek 在开源领域的主要竞争者
- [[qwen]] 系列在中文能力上与 DeepSeek 形成互补
- [[mixtral]] 的 MoE 路由策略与 DeepSeekMoE 有异曲同工之妙

## 架构创新

- **MLA**：通过低秩压缩 KV 投影，显著减少显存占用
- **DeepSeekMoE**：细粒度专家路由 + 共享专家机制
- **GRPO**：无需 Critic Model 的组级相对策略优化
- **MTP**：多 Token 预测提升训练效率和推理能力

## 影响与意义

DeepSeek 系列证明了在有限资源下通过架构创新可以实现接近甚至超越闭源模型的性能，对开源 AI 生态产生了重大影响。DeepSeek-R1 的推理能力突破直接推动了全球 AI 行业对推理模型的关注。
