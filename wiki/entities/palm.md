---
title: PaLM
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, architecture, llm, deeplearning]
sources: [raw/papers/2204.02311-PaLM-Scaling-Language-Modeling-with-Pathways.html]
---

# PaLM

PaLM（Pathways Language Model）是 Google 于 2022 年发布的 540B 参数密集激活 Transformer 语言模型，使用 Google 自研的 Pathways 系统在 6144 块 TPU v4 上训练。PaLM 540B 在数百个语言理解和生成基准上实现了 SOTA 的 few-shot 性能，并在多步推理任务上超越了微调 SOTA，在 BIG-bench 上超越了平均人类表现。[[raw/papers/2204.02311-PaLM-Scaling-Language-Modeling-with-Pathways.html]]

## Pathways 系统

Pathways 是 Google 的下一代 ML 计算系统，支持：

- 跨多个 TPU v4 Pod 的高效大规模训练
- 6144 块 TPU v4 芯片的并行协调
- 高效的资源利用和容错机制

PaLM 是 Pathways 系统的首个大规模应用验证。

## 模型规格

| 配置 | PaLM 8B | PaLM 62B | PaLM 540B |
|------|---------|----------|-----------|
| 参数量 | 80 亿 | 620 亿 | 5400 亿 |

三个规模均基于 [[transformer-architecture]] 的 Decoder-only 架构，核心设计选择：

- SwiGLU 激活函数
- 并行 Transformer blocks（Attention 和 FFN 并行计算而非串行）
- 无偏置（no bias）的 Attention 和 FFN 层
- RoPE 位置编码
- 共享的输入输出嵌入
- Multi-Query Attention（KV heads 共享）

## 核心发现

### Scaling Breakthroughs

PaLM 的训练揭示了规模化带来的**不连续能力涌现**（discontinuous improvements）：

- 在 BIG-bench 的大量任务上，性能随模型规模呈阶跃式增长
- 多步推理能力（如 chain-of-thought）在 540B 时显著涌现
- 超越了 BIG-bench 上的平均人类表现
- 在语言理解、推理、代码生成、多语言翻译上均实现重大突破

### Few-Shot Learning

PaLM 540B 的 few-shot 性能在许多任务上超越了经过微调的 SOTA 模型，证明了 scaling 的持续回报。

## 性能亮点

| 任务 | PaLM 540B 表现 |
|------|---------------|
| BIG-bench | 优于平均人类表现 |
| GSM8K | 58%（8-shot chain-of-thought） |
| 多步推理 | 超越微调 SOTA |
| 代码生成 | 显著超越前代模型 |
| 多语言翻译 | 100+ 语言支持 |

## 训练细节

- 训练数据：780B Token 多语言语料（英文为主，含多语言网页、书籍、代码等）
- 训练硬件：6144 块 TPU v4（跨 2 个 TPU v4 Pod）
- 训练效率：达到硬件 FLOPs 利用率 46.2%（540B 模型），高于此前报告的大规模训练效率
- 数据混合：社交媒体对话、过滤网页、书籍、GitHub 代码、Wikipedia、新闻

## 后续影响

PaLM 的技术成果直接影响了 [[google-deepmind]] 后续的 Gemini 和 [[gemma]] 系列模型。其 Pathways 系统为大规模分布式训练提供了重要参考，并行 Transformer 设计也被后续模型广泛采用。PaLM 的 chain-of-thought 推理能力发现对 [[gpt-4]] 等后续模型的提示工程产生了重大影响。
