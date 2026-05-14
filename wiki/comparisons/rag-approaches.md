---
title: RAG 方法对比
created: 2026-05-10
updated: 2026-05-15
type: comparison
tags: [comparison, rag, retrieval, agent, knowledge]
sources: [raw/papers/2005.11401-Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.html, raw/papers/2310.11511-Self-RAG-Learning-to-Retrieve-Generate-and-Critique-through-Self-Reflection.html, raw/papers/2401.15884-Corrective-Retrieval-Augmented-Generation.html, raw/papers/2403.14403-Adaptive-RAG-Learning-to-Adapt-Retrieval-Augmented-Large-Language-Models-through.pdf, raw/papers/2404.16130-From-Local-to-Global-A-Graph-RAG-Approach-to-Query-Focused-Summarization.html]
---

# RAG 方法对比

从基础 Naive RAG 到最新的 Agentic RAG，六种主流 RAG 架构的全面对比。[[raw/papers/2005.11401-Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.html]]

## 架构概览

### Naive RAG

```
Query → 检索器 (Embedding + Vector DB) → LLM 生成答案
```

最基础的检索增强生成。[[raw/papers/2005.11401-Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.html]]

### Self-RAG

```
Query → [反思] 需要检索吗？→ [检索] → [反思] 检索结果相关吗？→ [生成+引用] → [反思] 有幻觉吗？
```

模型在生成过程中自主判断是否需要检索，并对每步进行自我反思。[[raw/papers/2310.11511-Self-RAG-Learning-to-Retrieve-Generate-and-Critique-through-Self-Reflection.html]]

### CRAG (Corrective RAG)

```
Query → 检索 → [轻量级置信度评分] → ✅正确 → 使用 / ❌错误 → 纠正(搜索/Web) / ⚠️模糊 → 分解查询重试
```

对检索结果进行置信度评估，不信任时触发纠正机制。[[raw/papers/2401.15884-Corrective-Retrieval-Augmented-Generation.html]]

### Adaptive-RAG

```
Query → [动态路由] → 无需检索直接生成 / 单次检索 / 多步检索
         ↑
    查询复杂度评估 (分类器)
```

根据查询复杂度自适应选择策略，简单问题直接回答，复杂问题多步检索。[[raw/papers/2403.14403-Adaptive-RAG-Learning-to-Adapt-Retrieval-Augmented-Large-Language-Models-through.pdf]]

### GraphRAG

```
文档 → 实体/关系抽取 → 知识图谱 → 社区检测 → 社区摘要 → 全局查询 + 局部检索
```

利用知识图谱结构建模实体关系，擅长全局性、聚合性问题的回答。[[raw/papers/2404.16130-From-Local-to-Global-A-Graph-RAG-Approach-to-Query-Focused-Summarization.html]]

### Agentic RAG

```
Query → Agent (规划/工具调用/多步推理) → [检索] → [重写] → [多源融合] → [验证] → 答案
```

以 Agent 为核心，自主决定检索策略、工具使用和多步推理。

## 核心维度对比

| 维度 | Naive RAG | Self-RAG | CRAG | Adaptive-RAG | GraphRAG | Agentic RAG |
|------|-----------|----------|------|--------------|----------|-------------|
| **检索决策** | 总是检索 | 模型自主判断 | 总是检索 + 纠正 | 动态路由 | 图谱遍历 | Agent 决策 |
| **反思能力** | ❌ | ✅ 多步反思 | ✅ 置信度纠正 | ✅ 适应 | ❌ | ✅ 全面 |
| **全局推理** | ❌ | ❌ | ❌ | ❌ | ✅ 社区摘要 | ✅ |
| **多步检索** | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |
| **实现复杂度** | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **延迟** | 低 | 中 | 中 | 中 | 高 | 高 |
| **适用场景** | 简单 QA | 通用 | 事实性 QA | 混合查询 | 全局分析 | 复杂任务 |

## 各方法最佳场景

| 场景 | 推荐 | 理由 |
|------|------|------|
| 简单文档问答 | Naive RAG | 实现最简单，延迟最低 |
| 需要引用来源 | Self-RAG | 自动生成引用标注 |
| 检索质量不稳定 | CRAG | 自动纠正低质量检索 |
| 查询复杂度差异大 | Adaptive-RAG | 简单查询不走检索 |
| 全局趋势分析 | GraphRAG | 知识图谱聚合能力 |
| 复杂研究任务 | Agentic RAG | 多工具协作，灵活应对 |

## 演进趋势

Naive RAG → Self-RAG/CRAG/Adaptive (反思+自适应) → GraphRAG (结构化知识) → Agentic RAG (自主决策)

当前主流趋势是 **Agentic RAG + GraphRAG** 结合，兼具灵活性（Agent）和结构化推理（图谱）。

## 相关链接

- [[retrieval-augmented-generation]] — RAG 基础概念
- [[graph-rag]] — GraphRAG 详解
- [[dense-passage-retrieval]] — 检索基础
- [[embedding-models-2025]] — Embedding 模型选型
- [[agent-paradigm-shift]] — Agent 范式
