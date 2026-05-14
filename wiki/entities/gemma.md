---
title: Gemma 系列
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, open-source, llm, deeplearning]
sources: [raw/papers/2403.08295-Gemma-Open-Models-Based-on-Gemini-Research-and-Technology.html]
---

# Gemma 系列

Gemma 是 [[google-deepmind]] 发布的开源轻量级语言模型系列，基于 Gemini 研究和技术构建。Gemma 提供了 2B 和 7B 两个规模，在 18 个文本任务中的 11 个上超越了同规模开源模型，旨在为资源受限场景提供高质量的模型选择。[[raw/papers/2403.08295-Gemma-Open-Models-Based-on-Gemini-Research-and-Technology.html]]

## 模型规格

### Gemma 1.0 架构参数

| 参数 | Gemma 2B | Gemma 7B |
|------|----------|----------|
| d_model | 2048 | 3072 |
| Layers | 18 | 28 |
| Feedforward hidden dims | 32768 | 49152 |
| Num heads | 8 | 16 |
| Num KV heads | 1 (MQA) | 16 (MHA) |
| Head size | 256 | 256 |
| Vocab size | 256128 | 256128 |
| 上下文长度 | 8192 | 8192 |
| 训练数据量 | 最高 6T Token | 最高 6T Token |

### Gemma 2.0

- 参数规模扩展至 2B / 9B / 27B
- 引入 Knowledge Distillation
- 支持更长上下文
- 性能大幅提升

## 架构特性

- **Gemma 2B**：使用 Multi-Query Attention (MQA)，1 个 KV head
- **Gemma 7B**：使用标准 Multi-Head Attention (MHA)，16 个 KV heads
- GeGLU 激活函数
- RoPE 位置编码
- RMSNorm 归一化（Pre-norm + Post-norm 双归一化）
- 基于 [[transformer-architecture]] 的 Decoder-only 架构
- 词表大小 256K（使用 SentencePiece tokenizer，与 Gemini 共享）

## 训练特点

- 使用与 Gemini 相同的架构、数据和训练方法
- 训练数据量高达 6T Token 文本（主要为英文网页文档、代码和数学内容）
- 训练基础设施：Google TPU（TPUv5e）
- 严格的过滤和去重流程
- 同时发布 pretrained 和 fine-tuned checkpoints

## 性能表现

Gemma 在同规模模型中表现优异：

- Gemma 7B 在 18 个基准中的 11 个上超越 [[mistral-7b]]、LLaMA 2 7B/13B、Falcon 等同规模开源模型
- 覆盖领域：问答、常识推理、数学与科学、编码
- 提供了全面的安全性和责任评估

## 开源许可

Gemma 采用 Gemma Terms of Use（自定义许可证），允许商业和非商业使用。Google 认为负责任地发布 LLM 对于改善前沿模型安全性和推动创新至关重要。

## 安全与对齐

Google DeepMind 在 Gemma 的开发中特别注重安全性：

- 预训练数据过滤（个人信息、有害内容）
- RLHF 对齐的 fine-tuned 版本
- 红队测试
- 同时发布 raw pretrained 和 fine-tuned checkpoints 以支持 instruction-tuning 研究

## 生态

Gemma 与 Google 的 AI 生态深度集成，支持 TensorFlow、JAX、PyTorch 等多个框架，并提供了针对 CPU 和移动设备优化的 2B 版本。其与 [[palm]] 系列的技术传承关系使其成为 Google 开源 AI 战略的核心组成部分。
