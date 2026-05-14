---
title: 指令微调
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [training, alignment, nlp]
sources: [raw/papers/2212.10560-Self-Instruct-Aligning-Language-Models-with-Self-Generated-I.md, raw/papers/2210.11416-Scaling-Instruction-Finetuned-Language-Models.md]
---

# 指令微调

通过在指令-回答对上微调预训练语言模型，使其能够理解并执行人类指令。[[raw/papers/2212.10560-Self-Instruct-Aligning-Language-Models-with-Self-Generated-I.html]]

## 核心思想

预训练模型（如 [[transformer-architecture]]）学会了语言的统计规律，但不会"听指令"。指令微调通过监督学习教会模型：
- 理解各种指令格式
- 以适当的格式输出回答
- 遵循约束条件

## 数据来源

### 人工标注

- FLAN Collection：覆盖 1800+ NLP 任务
- Alpaca：52K 指令数据（由 GPT 生成）
- Open-Orca：大规模指令数据集

### 自生成方法（Self-Instruct）

Self-Instruct 提出用 LLM 自己生成指令数据[[raw/papers/2212.10560-Self-Instruct-Aligning-Language-Models-with-Self-Generated-I.html]]：
1. 用种子任务（175 条人工编写）作为 few-shot 示例
2. 让 LLM 生成新指令、输入和输出
3. 过滤低质量和重复数据
4. 用生成数据微调模型

### 扩展方法

- Evol-Instruct：通过逐步演化指令增加复杂度
- WizardLM：基于 Evol-Instruct 的高质量数据集

## 训练策略

| 策略 | 说明 |
|------|------|
| 全量 SFT | 更新所有参数，效果最好但成本高 |
| [[lora]] | 低秩微调，参数效率高 |
| 混合数据 | 混合多种任务类型提升泛化能力 |

## 规模效应

Flan-T5 和 Flan-PaLM 的研究表明[[raw/papers/2210.11416-Scaling-Instruction-Finetuned-Language-Models.html]]：
- 指令微调的效果随模型规模和任务数量增加而提升
- 任务数量从 9 增加到 1836 时，性能持续提升
- 指令微调的增益在大模型上更显著

## 相关概念

- [[rlhf]] — 指令微调后的进一步对齐
- [[lora]] — 高效的指令微调方法
- [[chain-of-thought]] — 指令微调中的推理增强
- [[in-context-learning]] — 无需微调的替代方案
