---
title: ColBERT — Late Interaction 检索
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [retrieval, embedding, efficiency]
sources: [raw/papers/2004.12832-ColBERT-Efficient-and-Effective-Passage-Search-via-Contextualized-Late-Interacti.md]
---

# ColBERT — Late Interaction 检索

一种介于双编码器和交叉编码器之间的检索方法，保留 Token 级别的细粒度交互，同时保持双编码器的检索效率。[[raw/papers/2004.12832-ColBERT-Efficient-and-Effective-Passage-Search-via-Contextualized-Late-Interacti.html]]

## 核心动机

### 双编码器的局限

[[dense-passage-retrieval]] 将整个段落压缩为单个向量：
- 丢失 Token 级别的细粒度信息
- 长文档中关键信息被稀释
- 对精确匹配不敏感

### 交叉编码器的局限

- Query 和 Passage 深度交互，效果好
- 但每个候选都需要完整编码，无法预计算

## Late Interaction 原理

### MaxSim 操作

ColBERT 的核心是 **MaxSim**（Maximum Similarity）：

```
Score(q, d) = Σ max_i sim(q_i, d_j)
```

对于 query 中的每个 token q_i，找到 document 中最相似的 token d_j，然后对所有 q_i 的最大相似度求和。

### 与其他方法的对比

| 方法 | 交互级别 | 预计算 | 效果 |
|------|---------|--------|------|
| DPR | 向量 × 向量 | ✅ | 中等 |
| ColBERT | Token × Token（延迟） | ✅ | 好 |
| Cross-Encoder | 完整交互 | ❌ | 最好 |

## 架构

### 编码阶段

```
Query → BERT → [q_1, q_2, ..., q_m]   (每个 token 一个向量)
Doc   → BERT → [d_1, d_2, ..., d_n]   (每个 token 一个向量)
```

向量维度通常为 128 维（比标准 BERT 的 768 维小很多）。

### 检索阶段

1. 用 ANN（近似最近邻）快速召回候选段落
2. 对候选段落计算 MaxSim 精确分数
3. 按分数排序返回

## 优势

- **细粒度匹配**：保留 token 级别的语义交互
- **可预计算**：文档的 token embedding 可以预先存储
- **延迟交互**：交互在检索阶段才发生，兼顾效果和效率
- **鲁棒性**：对查询改写和同义替换不敏感

## ColBERTv2 改进

- 使用 ResNet 风格的压缩层降低维度
- 引入 hard negative mining
- 支持多语言
- 检索延迟进一步降低

## 相关概念

- [[dense-passage-retrieval]] — ColBERT 的基础和对比对象
- [[text-embedding]] — ColBERT 使用的 token 级嵌入
- [[retrieval-augmented-generation]] — ColBERT 作为 RAG 检索器
- [[self-rag]] — 结合反思机制的检索增强
