---
title: Phi 系列
created: 2026-05-10
updated: 2026-05-10
type: entity
tags: [model, open-source, llm, training]
sources: [raw/papers/2309.05463-Textbooks-Are-All-You-Need-II-phi-15-technical-report.md]
---

# Phi 系列

Phi 是 [[microsoft-research]] 发布的小型语言模型系列，核心理念是**用高质量训练数据弥补模型规模不足**。Phi 系列证明了精心筛选的合成数据可以让极小模型达到远超预期的性能。[[raw/papers/2309.05463-Textbooks-Are-All-You-Need-II-phi-15-technical-report.html]]

## 核心理念："Textbooks Are All You Need"

Phi 系列的命名和设计理念源于一个关键洞察：教科书质量的数据比大规模网页爬取数据更有效。高质量、结构化的数据可以显著提升小模型的学习效率。

## 模型版本

### Phi-1（2023 年 6 月）

- 参数量：1.3B
- 专注代码生成任务
- 使用合成教科书数据训练
- 在 HumanEval 上达到 50.6%（超越 GPT-3.5）

### Phi-1.5（2023 年 9 月）

- 参数量：1.3B
- 从代码扩展到通用语言任务
- 在逻辑推理和数学上表现突出

### Phi-2（2023 年 12 月）

- 参数量：2.7B
- 在多项基准上接近 LLaMA 2 7B 和 Mistral 7B
- 100K 上下文窗口支持

### Phi-3（2024 年 4 月）

- 参数量：3.8B / 4.2B / 14B（Mini/Small/Medium）
- 在同规模模型中达到 SOTA 性能
- 支持长上下文（128K）
- 针对手机和边缘设备优化

## 数据策略

Phi 系列的数据策略是其核心优势：

- **教科书质量数据**：结构化、逻辑清晰的合成数据
- **GPT-4 生成的高质量数据**：利用大模型生成小模型训练数据
- **数据筛选**：严格的质量过滤和去重
- **合成推理数据**：专门为提升推理能力设计的数据集

## 性能表现

Phi 系列在同规模模型中表现卓越：

- Phi-2（2.7B）接近 LLaMA 2 7B 水平
- Phi-3 Mini（3.8B）超越 Mistral 7B
- 在数学和代码任务上尤为突出

## 技术架构

- 基于 [[transformer-architecture]] 的 Decoder-only 架构
- 使用密集的注意力机制（非 MoE）
- 支持长上下文的位置编码

## 影响

Phi 系列推动了 AI 社区对"数据质量 > 数据数量"理念的重视，为小模型高效训练提供了重要的方法论参考。其数据合成策略也被 [[deepseek]] 等团队借鉴。
