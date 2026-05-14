---
title: PaLM
created: 2026-05-10
updated: 2026-05-10
type: entity
tags: [model, architecture, llm, deeplearning]
sources: [raw/papers/2204.02311-PaLM-Scaling-Language-Modeling-with-Pathways.md]
---

# PaLM

PaLM（Pathways Language Model）是 Google 于 2022 年发布的大规模语言模型，使用 Google 自研的 Pathways 系统在 6144 块 TPU v4 上训练。PaLM 540B 是当时最大的密集语言模型之一，在多项任务上实现了突破性表现。[[raw/papers/2204.02311-PaLM-Scaling-Language-Modeling-with-Pathways.html]]

## Pathways 系统

Pathways 是 Google 的下一代 ML 计算系统，支持：

- 跨 Pod 级别的模型并行训练
- 稀疏激活的异构计算
- 高效的资源利用和容错机制

PaLM 是 Pathways 系统的首个大规模应用验证。

## 模型规格

- **PaLM 8B**：80 亿参数
- **PaLM 62B**：620 亿参数
- **PaLM 540B**：5400 亿参数
- 基于 [[transformer-architecture]] 的 Decoder-only 架构
- SwiGLU 激活函数
- 并行 Transformer blocks
- 无偏置的 Attention 和 FFN 层
- RoPE 位置编码
- 共享的输入输出嵌入

## 核心发现

### Scaling Breakthroughs

PaLM 的训练揭示了规模化带来的能力涌现：

- 在 BIG-bench 上达到接近人类水平的 100+ 项任务
- 在语言理解、推理、代码生成上实现重大突破
- 多语言翻译能力显著提升

### Few-Shot Learning

PaLM 的 few-shot 性能随着模型规模增长而持续提升，540B 模型在许多任务上超越了经过微调的 SOTA 模型。

## 性能亮点

| 任务 | PaLM 540B 表现 |
|------|---------------|
| BIG-bench | 优于平均人类表现 |
| GSM8K | 58%（few-shot） |
| MATH | 20%（few-shot） |
| 代码生成 | 显著超越前代模型 |
| 多语言 | 100+ 语言支持 |

## 训练细节

- 训练数据：780B Token 多语言语料
- 训练硬件：6144 块 TPU v4
- 训练时长：约 2 个月
- 利用 Chinchilla Scaling Laws 确定最优数据量

## 后续影响

PaLM 的技术成果直接影响了 [[google-deepmind]] 后续的 Gemini 和 [[gemma]] 系列模型。其 Pathways 系统也为大规模分布式训练提供了重要参考。
