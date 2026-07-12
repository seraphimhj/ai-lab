---
title: Qwen 系列
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, open-source, llm, multimodal]
sources: [raw/papers/2309.16609-Qwen-Technical-Report.pdf]
---

# Qwen 系列

Qwen（通义千问）是 [[alibaba-qwen]] 发布的开源大语言模型系列。Qwen 以强大的中文能力、多语言支持和丰富的模型生态著称，是中文 AI 社区最重要的开源基座模型之一。

## Qwen 1.0（2023 年 8 月）

Qwen 的首个版本即展现了出色的综合能力。[[raw/papers/2309.16609-Qwen-Technical-Report.pdf]]

- 参数规模：1.8B / 7B / 14B / 72B
- 训练数据：3T+ Token 多语言语料
- 支持中、英、日、韩等多种语言
- 原生支持工具调用和代码执行

## 核心架构特性

- 基于 [[transformer-architecture]] 的 Decoder-only 架构
- 使用 RoPE 位置编码
- SwiGLU 激活函数
- RMSNorm 归一化
- 支持外推到 32K 上下文（通过 YaRN 等技术）

## 模型生态

Qwen 系列构建了丰富的模型生态：

- **Qwen Base**：基础预训练模型
- **Qwen Chat**：通过 SFT + RLHF 对齐的对话模型
- **Qwen-VL**：视觉语言多模态模型
- **Qwen-Audio**：语音理解模型
- **Qwen-Coder**：代码专项模型
- **Qwen-Math**：数学专项模型
- **Qwen-Embedding**：文本嵌入模型（GTE 系列）

## 多语言能力

Qwen 系列在多语言基准上表现优异，尤其在中文任务上具有明显优势。训练数据覆盖了高质量的中英文语料，以及日、韩、法、德等语言数据。

## 性能特点

- 在中文理解和生成任务上达到同规模最佳
- 代码能力突出，在 HumanEval 等基准上表现优异
- 工具调用能力强大，支持 Function Calling
- 长上下文理解能力通过 YaRN 等技术扩展

## 与其他模型对比

- 相比 [[llama]] 系列，Qwen 在中文能力上更具优势
- 相比 [[deepseek]] 系列，Qwen 的模型生态更加完整
- 相比 [[yi-model]]，Qwen 的社区活跃度和工具链更成熟
- 相比 [[glm]] 系列，Qwen 的国际化和多模态布局更广泛
