---
title: Yi 模型
created: 2026-05-10
updated: 2026-05-10
type: entity
tags: [model, open-source, llm, deeplearning]
sources: [raw/papers/2403.04652-Yi-Open-Foundation-Models-by-01AI.md]
---

# Yi 模型

Yi 是零一万物（01.AI）发布的一系列开源基础语言模型，由李开复团队开发。Yi 模型以强大的语言理解和长上下文能力著称。[[raw/papers/2403.04652-Yi-Open-Foundation-Models-by-01AI.html]]

## 模型规格

- **Yi-6B**：60 亿参数
- **Yi-34B**：340 亿参数
- 上下文窗口：4K（基础版）→ 200K（长上下文版）
- 基于 [[transformer-architecture]] 的 Decoder-only 架构

## 核心特性

### 长上下文能力

Yi 系列的一个突出特点是其 200K Token 的超长上下文窗口，通过位置编码外推和渐进式上下文扩展实现。在长文本理解任务上表现出色。

### 多语言支持

Yi 模型在训练数据中包含大量中文语料，在中文理解、生成和多语言任务上具有竞争力。

### 高质量训练数据

Yi 团队特别注重训练数据的质量控制，使用了严格的数据清洗和过滤流程，包括去重、质量评分和有害内容过滤。

## 性能表现

Yi-34B 在发布时在多项基准上表现优异：

- MMLU：76.3%
- 在中文任务上具有显著优势
- 200K 上下文版本在长文本检索和推理任务上表现出色

## 版本变体

- **Yi-6B/34B Base**：基础预训练模型
- **Yi-6B/34B Chat**：通过 SFT + RLHF 对齐的对话模型
- **Yi-VL**：视觉语言多模态模型
- **Yi-Coder**：代码专项模型

## 架构设计

Yi 采用标准的 Transformer Decoder 架构，关键设计选择包括：

- RMSNorm 归一化
- RoPE 位置编码
- SwiGLU 激活函数
- FlashAttention 加速训练

## 与同类模型对比

- 相比 [[qwen]] 系列，Yi 在长上下文处理上有独特优势
- 相比 [[llama]] 系列，Yi 在中文任务上表现更强
- Yi-34B 的性能接近 LLaMA 2 70B，但参数量仅为一半

## 生态影响

Yi 模型的开源为中文 AI 社区提供了更多选择，其长上下文能力推动了社区对超长上下文技术的研究和关注。
