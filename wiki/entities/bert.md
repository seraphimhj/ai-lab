---
title: BERT
created: 2026-05-10
updated: 2026-05-10
type: entity
tags: [model, architecture, nlp, deeplearning]
sources: [raw/papers/1810.04805-BERT-Pre-training-Deep-Bidirectional-Transformers.html]
---

# BERT

BERT（Bidirectional Encoder Representations from Transformers）是 Google 于 2018 年提出的预训练语言模型，开创了双向预训练的范式。与此前仅使用单向上下文的模型不同，BERT 通过联合调节左右上下文，在所有 Transformer 层中实现深度双向表示。[[raw/papers/1810.04805-BERT-Pre-training-Deep-Bidirectional-Transformers.html]]

## 预训练任务

### Masked Language Model (MLM)

随机遮蔽输入中 15% 的 Token，要求模型根据上下文预测被遮蔽的内容。其中 80% 替换为 `[MASK]`，10% 替换为随机 Token，10% 保持不变。

### Next Sentence Prediction (NSP)

判断两个句子是否为原文中连续出现的上下句，使模型学习句子间的关系。

## 模型规模

- **BERT-Base**：12 层，768 隐藏维度，12 个 Attention Head，1.1 亿参数
- **BERT-Large**：24 层，1024 隐藏维度，16 个 Attention Head，3.4 亿参数

## 核心创新

BERT 的核心贡献在于证明了基于 [[transformer-architecture]] 的双向 Encoder 在预训练后，仅需增加一个简单的输出层即可在多种 NLP 任务上达到 SOTA，无需大量任务特定架构修改。

## 下游任务表现

BERT 在 11 个 NLP 基准上刷新了记录：

- GLUE 评分提升至 80.5%（+7.7%）
- SQuAD v1.1 Test F1 达到 93.2
- SQuAD v2.0 Test F1 达到 83.1

## 影响与遗产

BERT 开启了 "预训练 + 微调" 的 NLP 范式，深刻影响了后续所有预训练语言模型的设计。其 MLM 预训练策略被 [[roberta]]、[[albert]] 等后续模型继承和改进。BERT 也证明了 [[openai]] 此前 GPT 系列采用的单向预训练并非最优选择，双向上下文建模至关重要。

## 局限性

- 预训练与微调之间的 MLM 遮蔽不匹配
- NSP 任务的有效性受到后续研究质疑
- 与自回归模型相比，生成能力较弱
