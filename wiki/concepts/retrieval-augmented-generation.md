---
title: RAG — 检索增强生成
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [retrieval, generation, agent]
sources: [raw/papers/2005.11401-Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.md]
---

# RAG — 检索增强生成

将信息检索与文本生成结合，先从外部知识库检索相关文档，再基于检索结果生成回答，解决 LLM 知识滞后和幻觉问题。[[raw/papers/2005.11401-Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.html]]

## 核心流程

```
用户问题 → 检索器(Retriever) → 相关文档 → 生成器(Generator) → 回答
```

### 两个核心组件

1. **检索器（Retriever）**：将用户查询映射到知识库中的相关文档
2. **生成器（Generator）**：基于检索到的文档生成最终回答

## RAG 的优势

| 问题 | 纯 LLM | RAG |
|------|--------|-----|
| 知识过时 | 无法获取新知识 | 实时检索最新信息 |
| 幻觉 | 可能编造事实 | 基于检索结果，更可靠 |
| 私有数据 | 无法访问 | 检索企业知识库 |
| 可追溯性 | 无法验证来源 | 可以标注来源文档 |
| 更新成本 | 需重新训练 | 更新知识库即可 |

## 检索方法

### 稀疏检索
- BM25、TF-IDF
- 基于词频匹配
- 适合精确匹配场景

### 稠密检索
- [[dense-passage-retrieval]] — 双编码器架构
- [[text-embedding]] — 文本向量化
- 适合语义匹配场景

### 混合检索
- 结合稀疏和稠密检索
- 通常效果最好

## 优化方向

| 优化方向 | 方法 |
|---------|------|
| 检索质量 | 查询改写、hyde、multi-query |
| 上下文长度 | 文档分块策略、重排序 |
| 生成质量 | 增强提示、引用生成 |
| 反馈循环 | [[self-rag]]、Adaptive RAG |

## 相关概念

- [[dense-passage-retrieval]] — RAG 的核心检索方法
- [[self-rag]] — 自我反思的 RAG
- [[graph-rag]] — 基于知识图谱的 RAG
- [[colbert-retrieval]] — Late Interaction 检索方法
- [[text-embedding]] — 文本向量化的基础
