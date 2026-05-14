---
title: DPR — 密集段落检索
created: 2026-05-10
updated: 2026-05-14
type: concept
tags: [retrieval, embedding, efficiency]
sources: [raw/papers/2004.04906-Dense-Passage-Retrieval-for-Open-Domain-Question-Answering.html]
---

# DPR — 密集段落检索

使用双 BERT 编码器将问题和段落编码为稠密向量，通过向量相似度进行语义匹配的检索方法。[[raw/papers/2004.04906-Dense-Passage-Retrieval-for-Open-Domain-Question-Answering.html]]

## 核心架构

### 双编码器（Dual Encoder）

```
Question → BERT_Q → q_vector
Passage  → BERT_P → p_vector
Similarity = dot(q_vector, p_vector)
```

两个编码器独立工作：
- **Question Encoder**：将问题编码为向量
- **Passage Encoder**：将候选段落编码为向量

### 为什么用双编码器而非交叉编码器

| 架构 | 优势 | 劣势 |
|------|------|------|
| 双编码器 | 可以预计算所有段落向量，检索时只需编码 query | 交互不够深入 |
| 交叉编码器 | Question 和 Passage 深度交互 | 每次检索都需要对所有候选段落编码 |

DPR 选择双编码器，因为检索场景需要快速匹配大量候选。

## 训练过程

### 正负样本构造

- **正样本**：包含答案的段落
- **负样本**：
  - 同文档中其他段落（In-batch negatives）
  - BM25 检索到的但不包含答案的段落（Hard negatives）
  - 来自其他问题的黄金段落（跨问题负样本）

### 损失函数

```
L = -log exp(sim(q, p+)) / Σ exp(sim(q, pi))
```

NCE（Noise Contrastive Estimation）风格的损失函数。

## 与传统方法的对比

| 方法 | 检索类型 | 典型性能 |
|------|---------|---------|
| TF-IDF | 词频匹配 | 基线 |
| BM25 | 词频 + 文档长度归一化 | 强基线 |
| DPR | 语义匹配 | 显著优于 BM25 |

论文报告的具体数据：
- **Top-5 准确率**：DPR 65.2% vs. BM25 42.9%（Natural Questions open setting）
- **Top-20 检索准确率**：DPR 比 BM25 高 9%–19%（跨多个 QA 数据集）
- **端到端 QA**：DPR + reader 达到 41.5% EM，显著超过 ORQA 的 33.3%
- 训练仅需少量问题-段落对（无需额外预训练如 ICT）

## 应用

DPR 是 [[retrieval-augmented-generation]] 的核心检索组件，被广泛应用于：
- 开放域问答
- 企业知识库搜索
- [[tool-use]] 中的知识检索

## 相关概念

- [[retrieval-augmented-generation]] — DPR 是 RAG 的典型检索器
- [[text-embedding]] — DPR 使用 BERT 进行文本向量化
- [[colbert-retrieval]] — DPR 的改进版本，使用 Late Interaction
- [[self-rag]] — 结合检索和生成的方法
- [[in-context-learning]] — DPR 通过 few-shot 示例训练双编码器
- [[in-context-learning]] — DPR 通过 few-shot 示例训练双编码器
