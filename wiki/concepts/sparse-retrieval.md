---
title: Sparse Retrieval
created: 2026-05-14
updated: 2026-07-26
type: concept
tags: [retrieval, embedding, nlp, rag]
sources: [raw/papers/2109.10086-SPLADE-v2-Sparse-Lexical-and-Expansion-Model-for-Information-Retrieval.html]
confidence: high
---

# Sparse Retrieval

稀疏检索是信息检索的经典范式，通过词汇级别的精确匹配实现文档召回。现代学习型稀疏检索（Learned Sparse Retrieval）结合了传统 BM25 的可解释性与神经网络的语义扩展能力。

## 从 BM25 到学习型稀疏检索

### 传统稀疏检索（BM25）

基于词频-逆文档频率（TF-IDF）的经典方法：
- 依赖精确词汇匹配
- 无法处理同义词/释义（vocabulary mismatch 问题）
- 但高度可解释、推理快速、无需 GPU

### 学习型稀疏检索（SPLADE）

SPLADE（SParse Lexical AnD Expansion model）用 [[bert]] 的 MLM head 为文档每个 token 生成词汇表上的稀疏权重：[[raw/papers/2109.10086-SPLADE-v2-Sparse-Lexical-and-Expansion-Model-for-Information-Retrieval.html]]

核心机制：
1. 文档通过 BERT 编码，每个 token 在 MLM head 输出 30K 维词汇表的 logits
2. 使用 max pooling + log-saturation 聚合为单一稀疏向量
3. 该向量自动实现**词汇扩展**（expansion）：文档中没出现的相关词也会获得非零权重

例如：文档"The cat sat on the mat"可能扩展出"feline", "kitten", "pet"等语义相关词。

### SPLADE v2 改进

- **蒸馏训练**：从 Cross-Encoder 教师模型学习
- **正则化**：FLOPS 正则化控制稀疏度，平衡效果与效率
- **效果**：在 MS MARCO 上超越 BM25 ~10 个点，接近 [[dense-passage-retrieval]] 水平

## 稀疏 vs 密集检索

| 维度 | 稀疏检索 (SPLADE) | 密集检索 ([[dense-passage-retrieval]]) |
|-----|-------------------|-------|
| 表示维度 | ~30K（词汇表大小） | 768/1024 |
| 索引 | 倒排索引 | ANN 索引 (HNSW/IVF) |
| 可解释性 | 高（可看到哪些词被匹配） | 低 |
| 精确匹配 | 强 | 弱（实体名等） |
| 语义匹配 | 中等（通过扩展） | 强 |
| 推理速度 | 快（Lucene 优化） | 中等 |
| 零样本泛化 | 中等 | 较弱 |

## 在 RAG 中的应用

在 [[retrieval-augmented-generation]] 系统中，最佳实践是稀疏+密集**混合检索**（Hybrid Retrieval）：
- 稀疏分支（BM25/SPLADE）处理关键词精确匹配
- 密集分支（DPR/E5/BGE）处理语义相似度
- 通过 RRF（Reciprocal Rank Fusion）或线性加权融合结果

这正是 [[colbert-retrieval]] 之外的另一种"两全其美"方案。

## 从「过早聚合」看稀疏检索：给否决型信号留独立账目

把 SPLADE/BM25 放到「过早聚合」这条轴上，会得到一个比"精确匹配强"更结构化的解释 [[2026-07-25-aggregation-erases-minority-signals]]：

[[dense-passage-retrieval|Dense 单向量]]在**检索前**就把整句压成一个点，实体名这类低频高信息 token 的贡献被话题语义淹没，而点积又允许"实体维少掉的分被话题维补回来"——于是"苹果营收"召回"微软营收"。SPLADE 的词表维相当于**给否决型信号留一个独立账目**：实体的字面命中落在它自己的一维上，不必先并进整体语义方向，因此不容易被话题相似度补偿掉。这也是它在上表"精确匹配"一栏对 dense 占优的机制根因——不是"匹配更准"，而是**把聚合推迟、让实体维单独结算**。

但要点是：推迟聚合 ≠ 永不聚合。SPLADE 的最终相关性仍是所有词表维上的**求和**，若其他词项分数足够多，实体错配仍可能被补偿。真正需要"实体错即淘汰"的硬约束场景，还得在稀疏召回之外叠 lexical filter / entity linker / metadata 约束兜底——稀疏检索给了实体一个独立发言的维度，但没有把它升级成不可协商的一票。

这条"哪一步聚合、就决定哪种信号被抹掉"的轴，把稀疏检索、[[colbert-retrieval]] 的 MaxSim（逐 token 独立验收）与评测端的 worst-group / slice 指标串成同一病灶（[[benchmark-evaluation]]）的三处同构修法：编码/检索端保留局部维度、评测端保留数据切片，最后都按真实业务风险而非样本频率再聚合。

## 与 [[text-embedding]] 的关系

现代 embedding 模型如 BGE-M3 已内置多路检索能力：Dense + Sparse + ColBERT 三合一，模糊了稀疏/密集的边界。Qwen3-Embedding 同样支持稀疏向量输出。
