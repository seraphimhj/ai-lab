---
title: RAG — 检索增强生成
created: 2026-05-10
updated: 2026-07-29
type: concept
tags: [retrieval, generation, agent]
sources: [raw/papers/2005.11401-Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.html, raw/papers/2002.08909-REALM-Retrieval-Augmented-Language-Model-Pre-Training.html, raw/papers/2112.04426-Improving-language-models-by-retrieving-from-trillions-of-to.html]
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

## 历史演进

### REALM（2020）— 检索增强预训练

首次证明检索器可以与语言模型端到端联合训练。通过 MLM 作为学习信号，反向传播穿过百万级文档检索步骤。在 Open-QA 上超越纯参数化模型 4-16%。[[raw/papers/2002.08909-REALM-Retrieval-Augmented-Language-Model-Pre-Training.html]]

### RAG（2020）— 经典框架

Meta AI 提出的 RAG 框架将 DPR 检索器和 BART 生成器结合，引入 RAG-Sequence 和 RAG-Token 两种生成模式。[[raw/papers/2005.11401-Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.html]]

### RETRO（2022）— 大规模检索增强

DeepMind 的 RETRO 从 2T token 数据库中检索，用 chunked cross-attention 融合检索结果，25× 少参数即可匹配 GPT-3 性能。[[raw/papers/2112.04426-Improving-language-models-by-retrieving-from-trillions-of-to.html]]

## 检索方法

### 稀疏检索
- BM25、TF-IDF — 基于词频匹配
- [[sparse-retrieval]] — SPLADE 等学习型稀疏方法
- 适合精确匹配场景

### 稠密检索
- [[dense-passage-retrieval]] — 双编码器架构
- [[text-embedding]] — 文本向量化
- 适合语义匹配场景

### 混合检索
- 结合稀疏和稠密检索（Hybrid Retrieval）
- 通过 RRF 或线性加权融合
- 通常效果最好

## 一根轴看清检索方法：query-doc 交互推迟到链条哪一步

上面把检索器按「稀疏 / 稠密 / 混合」分类，是按表示形态分的；但真正决定一个检索器
召回什么、漏什么的，是另一根更本质的轴——**query 与 doc 的交互被安排在流水线的哪一步算完**。
从「编码时就把交互算尽」到「检索时才逐 token 交互」排成一条谱，恰好把散落的方法串成一条线，
也解释了它们各自的强项与死角。[[2026-07-24-late-interaction-muvera]]

| 交互发生在 | 代表方法 | doc 侧存什么 | 强项 | 死角（漏什么） |
|-----------|---------|-------------|------|---------------|
| 编码时（最早） | [[dense-passage-retrieval|DPR]] 单向量 | 1 个向量 | 语义泛化、存储/检索最省 | 专名/型号被 mean-pool 淹没，实体 mismatch |
| 编码时·保词表维 | [[sparse-retrieval\|SPLADE]]、BM25 | 稀疏词表权重 | 精确匹配、实体命中落在独立维 | 纯词面同义/改写覆盖弱 |
| 检索时·逐 token | [[colbert-retrieval\|ColBERT]] MaxSim | 每 token 一个向量 | token 级精度，兼顾语义与实体 | 存储/延迟贵，需 MUVERA 之类压回 MIPS |
| 检索后·全交互 | cross-encoder 重排 | 不预存，联合前向 | 精度上限最高 | 只能对 top-k 重排，跑不了全库 |

**为什么这根轴比「稀疏/稠密」更有解释力**：交互越早算完，doc 编码时越是「不知道未来会来什么 query」，
只能把异质信息预先揉进固定表示——这是一次**不可逆的过早聚合**，低频高信息的 token（那个具体实体）
在求和/池化里被多数语义票淹没。交互推迟得越晚，doc 侧保留的信号维度越多、被话题相似度补偿掉的越少，
代价是存储与检索开销上升。所以选检索器不是「谁效果好」，而是**能容忍多大的存储/延迟预算，去把交互往后推几步**；
Hybrid 与多阶段（召回→重排）本质就是在这条谱上做混搭：用早交互的方法广撒网、用晚交互的方法在小集合上补精度。

这条「拒绝过早聚合、把维度拆开单独看」的思路不止用于召回——在评测端它对应
逐子集看 worst-group 而非只看 mean，是同一病灶在链条两端的同构修法（见 [[benchmark-evaluation]]、[[text-embedding]]）。

## 优化方向

| 优化方向 | 方法 |
|---------|------|
| 检索质量 | 查询改写、hyde、multi-query |
| 上下文长度 | 文档分块策略、重排序 |
| 生成质量 | 增强提示、引用生成 |
| 反馈循环 | [[self-rag]]、Adaptive RAG |

## 相关概念

- [[dense-passage-retrieval]] — RAG 的核心检索方法
- [[sparse-retrieval]] — 学习型稀疏检索（SPLADE）
- [[self-rag]] — 自我反思的 RAG
- [[graph-rag]] — 基于知识图谱的 RAG
- [[colbert-retrieval]] — Late Interaction 检索方法
- [[text-embedding]] — 文本向量化的基础
- [[long-context-extension]] — 长上下文 vs RAG 的 trade-off
