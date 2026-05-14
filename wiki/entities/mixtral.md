---
title: Mixtral MoE
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, open-source, llm, architecture]
sources: [raw/papers/2401.04088-Mixtral-of-Experts.html]
---

# Mixtral MoE

Mixtral 是 Mistral AI 发布的 Mixture-of-Experts (MoE) 语言模型，采用 8 个专家的稀疏路由架构。Mixtral 8x7B 总参数量 46.7B，但每个 Token 仅激活 12.9B 参数，以接近 7B 模型的推理成本达到接近 LLaMA 2 70B 的性能。[[raw/papers/2401.04088-Mixtral-of-Experts.html]]

## MoE 架构

### 稀疏专家路由

Mixtral 的核心创新在于将 Transformer 的 FFN 层替换为 8 个专家 FFN 的集合。对于每个 Token，一个 Router 网络选择 Top-2 专家进行计算，加权求和输出。

### 负载均衡

为保证各专家被均匀使用，Mixtral 引入了负载均衡损失项，防止 Router 将所有 Token 路由到少数专家。

## 模型规格

| 参数 | 值 |
|------|-----|
| dim | 4096 |
| n_layers | 32 |
| head_dim | 128 |
| hidden_dim | 14336 |
| n_heads | 32 |
| n_kv_heads | 8 |
| context_len | 32768 |
| vocab_size | 32000 |
| num_experts | 8 |
| top_k_experts | 2 |

- **总参数**：46.7B（论文原文：each token has access to 47B parameters）
- **激活参数**：12.9B（论文原文：only uses 13B active parameters during inference）
- **专家数量**：8 个
- **Top-K 路由**：2
- **上下文窗口**：32K
- **架构特性**：继承 [[mistral-7b]] 的 GQA

## 性能表现

Mixtral 8x7B 在多项基准上接近或超越 GPT-3.5 和 LLaMA 2 70B：

- MMLU：70.6%
- HumanEval：40.2%
- GSM8K：74.4%
- 在多语言和代码任务上表现优异

## 版本变体

- **Mixtral 8x7B Base**：基础预训练模型（Apache 2.0 许可）
- **Mixtral 8x7B Instruct**：SFT + DPO（Direct Preference Optimization）对齐的指令模型，超越 GPT-3.5 Turbo、Claude-2.1、Gemini Pro 和 LLaMA 2 70B Chat
- **Mixtral 8x22B**：更大规模版本，性能接近 GPT-4

## 技术对比

与 [[deepseek]] 的 DeepSeekMoE 相比，Mixtral 使用更粗粒度的专家路由（每个 FFN 层独立路由 vs 共享专家机制），但训练流程更加简洁。

## 影响

Mixtral 的成功证明了 MoE 架构在大语言模型中的实用性，推动了 MoE 从学术研究走向工程实践。其开源策略也加速了 MoE 在开源社区的普及。基于 [[transformer-architecture]] 的 sparse MoE 设计启发了 [[deepseek]] 等团队的后续工作。
