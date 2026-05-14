---
title: GraphRAG — 基于知识图谱的检索增强生成
created: 2026-05-10
updated: 2026-05-14
type: concept
tags: [retrieval, generation, knowledge-graph]
sources: [raw/papers/2404.16130-From-Local-to-Global-A-Graph-RAG-Approach-to-Query-Focused-Summarization.html]
---

# GraphRAG — 基于知识图谱的检索增强生成

将文档集合构建为知识图谱，利用图的结构信息进行社区检测和层次化摘要，解决全局性问题和跨文档推理。[[raw/papers/2404.16130-From-Local-to-Global-A-Graph-RAG-Approach-to-Query-Focused-Summarization.html]]

## 核心动机

标准 [[retrieval-augmented-generation]] 的局限：
- **局部性**：只检索局部文档片段，缺乏全局理解
- **跨文档推理弱**：难以综合多个文档的信息
- **主题理解不足**：无法回答"这个数据集的整体主题是什么"

## GraphRAG 流程

### 阶段一：索引构建

1. **文本分块**：将文档切分为段落
2. **实体/关系抽取**：用 LLM 从文本中提取实体和关系
3. **图构建**：将实体和关系构建为知识图谱
4. **社区检测**：使用 Leiden 算法检测图中的社区
5. **社区摘要**：为每个社区生成摘要
6. **层次化摘要**：从底层到顶层逐级生成摘要

### 阶段二：查询与生成

1. **实体识别**：从查询中识别相关实体
2. **局部搜索**：在图中搜索与实体相关的子图
3. **全局搜索**：遍历社区摘要，匹配查询意图
4. **回答生成**：基于搜索结果生成回答

## 局部 vs. 全局搜索

| 搜索类型 | 方法 | 适用问题 |
|---------|------|---------|
| 局部搜索 | 实体 + 邻居节点 | 具体事实性问题 |
| 全局搜索 | 社区摘要 + map-reduce | 总结性、全局性问题 |

## 与标准 RAG 对比

| 维度 | 标准 RAG | GraphRAG |
|------|---------|---------|
| 索引结构 | 向量数据库 | 知识图谱 |
| 检索粒度 | 文档片段 | 实体 + 社区 |
| 全局理解 | 弱 | 强（社区摘要） |
| 构建成本 | 低 | 高（需 LLM 抽取） |
| 可维护性 | 简单 | 复杂（图更新） |

## 论文关键数据

Microsoft Research (Edge et al., 2024) 在百万 token 规模数据集上的实验：
- 针对全局 sensemaking 问题，GraphRAG 在 **comprehensiveness**（全面性）和 **diversity**（多样性）上大幅超越朴素 RAG 基线
- 两阶段索引：先从源文档中用 LLM 提取实体知识图谱，再对紧密相关实体群组预生成社区摘要
- 查询时：每个社区摘要生成部分回答，然后汇总为最终回答（map-reduce 模式）
- 开源 Python 实现：https://aka.ms/graphrag

## 适用场景

- 大规模文档集合的全局理解
- 需要跨文档推理的任务
- 企业知识库的智能问答
- 研究论文的分析与总结

## 局限性

- 索引构建成本高（需要大量 LLM 调用）
- 图的更新和维护复杂
- 实体抽取质量影响整体效果
- 对短文档或简单问答场景 overkill

## 相关概念

- [[retrieval-augmented-generation]] — GraphRAG 的基础
- [[self-rag]] — 另一种 RAG 改进方向（反思机制）
- [[dense-passage-retrieval]] — GraphRAG 可以结合 DPR 进行混合检索
- [[text-embedding]] — 文本向量化的基础技术
- [[colbert-retrieval]] — 细粒度检索可作为局部搜索的补充
