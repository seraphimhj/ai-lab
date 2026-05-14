---
title: Gemma 系列
created: 2026-05-10
updated: 2026-05-10
type: entity
tags: [model, open-source, llm, deeplearning]
sources: [raw/papers/2403.08295-Gemma-Open-Models-Based-on-Gemini-Research-and-Technology.md]
---

# Gemma 系列

Gemma 是 [[google-deepmind]] 发布的开源轻量级语言模型系列，基于 Gemini 研究和技术构建。Gemma 提供了 2B 和 7B 两个规模，旨在为资源受限场景提供高质量的模型选择。[[raw/papers/2403.08295-Gemma-Open-Models-Based-on-Gemini-Research-and-Technology.html]]

## 模型规格

### Gemma 1.0

- **Gemma 2B**：20 亿参数
- **Gemma 7B**：70 亿参数
- 上下文窗口：8K
- 基于 [[transformer-architecture]] 的 Decoder-only 架构

### Gemma 2.0

- 参数规模扩展至 2B / 9B / 27B
- 引入 Knowledge Distillation
- 支持更长上下文
- 性能大幅提升

## 架构特性

- Multi-Query Attention (MQA) 或 Grouped-Query Attention (GQA)
- GeGLU 激活函数
- RoPE 位置编码
- RMSNorm 归一化
- 交替的局部和全局滑动窗口注意力

## 训练特点

- 基于 Gemini 架构和训练方法的改进
- 高质量的多语言训练数据
- 严格的过滤和去重流程
- 支持指令微调和对话对齐

## 性能表现

Gemma 在同规模模型中表现优异：

- Gemma 7B 超越 Mistral 7B 在多项基准上的表现
- Gemma 2B 在移动端和边缘设备上表现出色
- 在数学推理和代码生成上有显著优势

## 开源许可

Gemma 采用基于使用量的自定义许可证，允许商业和非商业使用，但对大规模分发有一定限制。

## 安全与对齐

Google DeepMind 在 Gemma 的开发中特别注重安全性，通过预训练数据过滤、RLHF 对齐和红队测试等多重机制确保模型输出的安全性。

## 生态

Gemma 与 Google 的 AI 生态深度集成，支持 TensorFlow、JAX、PyTorch 等多个框架，并提供了针对移动设备优化的版本。
