---
title: 文本嵌入/向量化
created: 2026-05-10
updated: 2026-07-25
type: concept
tags: [embedding, representation, retrieval]
sources: [raw/papers/1908.10084-Sentence-BERT-Sentence-Embeddings-using-Siamese-BERT-Networks.html, raw/papers/2212.03533-Text-Embeddings-by-Weakly-Supervised-Contrastive-Pre-training.html, raw/papers/2210.07316-MTEB-Massive-Text-Embedding-Benchmark.html, raw/papers/2402.03216-M3-Embedding-Multi-Linguality-Multi-Functionality-Multi-Granularity-Text-Embeddi.html, raw/papers/2405.17428-NV-Embed-Improved-Techniques-for-Training-LLMs-as-Generalist-Embedding-Models.html, raw/papers/2407.15831-NV-Retriever-Improving-text-embedding-models-with-effective-hard-negative-mining.html, raw/papers/2506.05176-Qwen3-Embedding-Advancing-Text-Embedding-and-Reranking-Through-Foundation-Models.html, raw/papers/2602.15547-jina-embeddings-v5-text-Task-Targeted-Embedding-Distillation.html]
---

# 文本嵌入/向量化

将文本映射到稠密向量空间的过程，使语义相似的文本在向量空间中距离较近。是信息检索、聚类、相似度计算等任务的基础。

## 基本概念

### 什么是 Embedding

```
"今天天气真好" → [0.12, -0.34, 0.56, ..., 0.78]  (768维向量)
"阳光明媚"     → [0.15, -0.31, 0.52, ..., 0.75]  (相似向量)
"明天要下雨"   → [0.89, 0.12, -0.45, ..., 0.23]  (不相似向量)
```

文本 → 固定维度向量，语义相似度 ≈ 向量相似度。

### 核心任务

- **语义相似度**：两段文本有多相似
- **语义搜索**：找到与 query 语义最匹配的文档
- **聚类**：将相似文本分组
- **重排序**：对候选文档按相关性排序

## 主要方法演进

### Sentence-BERT（2019）[[raw/papers/1908.10084-Sentence-BERT-Sentence-Embeddings-using-Siamese-BERT-Networks.html]]

- 使用 Siamese BERT 网络生成句子级嵌入
- 对比学习目标：相似句子对拉近，不相似句子对推远
- 比标准 BERT 快 10×，效果好 10-20%

### E5 / Instructor（2022-2023）

- **E5**：弱监督对比预训练[[raw/papers/2212.03533-Text-Embeddings-by-Weakly-Supervised-Contrastive-Pre-training.html]]
- **Instructor**：指令增强的嵌入（根据任务生成不同嵌入）
- **BGE**：通用嵌入模型，中文表现优秀

### 现代 Embedding 模型

| 模型 | 特点 |
|------|------|
| OpenAI text-embedding-3 | 大规模商用，支持降维 |
| BGE-M3 | 开源，Dense+Sparse+ColBERT 三合一 [[raw/papers/2402.03216-M3-Embedding-Multi-Linguality-Multi-Functionality-Multi-Granularity-Text-Embeddi.html]] |
| GTE 系列 | [[alibaba-qwen]] 出品，多语言长文本 |
| NV-Embed v1/v2 | LLM-based embedding，effective hard negative mining [[raw/papers/2405.17428-NV-Embed-Improved-Techniques-for-Training-LLMs-as-Generalist-Embedding-Models.html]] |
| NV-Retriever | 正负样本挖掘优化，提升检索精度 [[raw/papers/2407.15831-NV-Retriever-Improving-text-embedding-models-with-effective-hard-negative-mining.html]] |
| Qwen3-Embedding | 基于 Qwen3 基座，MTEB 75.22 登顶 [[raw/papers/2506.05176-Qwen3-Embedding-Advancing-Text-Embedding-and-Reranking-Through-Foundation-Models.html]] |
| Jina Embeddings v5 | Task-Targeted Distillation，任务自适应嵌入 [[raw/papers/2602.15547-jina-embeddings-v5-text-Task-Targeted-Embedding-Distillation.html]] |

### BGE-M3（2024）[[raw/papers/2402.03216-M3-Embedding-Multi-Linguality-Multi-Functionality-Multi-Granularity-Text-Embeddi.html]]

M3 = Multi-Linguality + Multi-Functionality + Multi-Granularity：
- **多语言**：100+ 语言统一向量空间
- **多功能**：单模型同时输出 Dense / Sparse / ColBERT 三种表示
- **多粒度**：支持 8192 token 长文本
- 训练创新：Self-Knowledge Distillation（三种表示互为教师）

### NV-Embed（2024）[[raw/papers/2405.17428-NV-Embed-Improved-Techniques-for-Training-LLMs-as-Generalist-Embedding-Models.html]]

基于 LLM（Mistral 7B）作为 embedding 骨干：
- Latent Attention Layer 代替平均池化
- 两阶段对比学习：Instruct→Hard Negative
- MTEB 56 任务上首个 LLM-based 模型超越所有专用模型

## 评估基准

MTEB（Massive Text Embedding Benchmark）[[raw/papers/2210.07316-MTEB-Massive-Text-Embedding-Benchmark.html]] 是当前最全面的 Embedding 评估基准：
- 覆盖 8 个任务类型
- 58 个数据集
- 多语言支持

## 关键技术

| 技术 | 说明 |
|------|------|
| 对比学习 | 基础训练范式 |
| Hard Negative Mining | 挖掘难负样本提升区分度 |
| Instruction Tuning | 指令条件嵌入 |
| Matryoshka Representation | 多粒度嵌入，支持降维 |

## 失败模式：实体 mismatch

Dense 单向量检索有一个系统性失败：查询「A 公司 2025 年营收」会把「B 公司 2025 年营收」排在「A 公司 2024 年营收」之前——**话题相似压过了身份差异**。[[2026-07-22-embedding-entity-mismatch]]

根因在编码链条的两步：mean-pooling 把整句压成一个点时，专名/型号/数字这类**低频但高信息**的 token 贡献被高频语义词淹没；cosine 相似度随之由话题语义主导，而非那个具体实体。更深一层，dense embedding 常被训练成逼近 **semantic similarity**（两段话在谈相近的事），却被系统拿来近似 **retrieval relevance**（这段话能否回答这个具体查询）——两者恰恰在实体敏感的查询上分道扬镳。

三条把身份信号补回来的修法，各在不同环节拦截：

| 修法 | 补在哪一环 | 机制 |
|------|-----------|------|
| 稀疏 exact-match（[[sparse-retrieval]] / BM25） | 词表层 | 保住专名的字面命中，在混合检索里当身份锚 |
| late interaction（[[colbert-retrieval]] MaxSim） | 检索时匹配层 | 保留每个 token 向量、逐 token 匹配，实体 token 不被过早 pooling 抹掉 |
| entity-aware 难负例 | 训练目标层 | 用「只换实体」的难负例逼模型学到「换个实体即负样本」，改写相似性边界 |

一句话：mismatch 的病根在「过早聚合把决定性的少数信号抹平」，三条修法的共性是「拒绝过早聚合、把实体维度单独保住」。

### 更一般的病灶：过早聚合与「可聚合性」四问

实体 mismatch 不是 embedding 独有的 bug，而是一种结构性病灶的编码端实例：**聚合保留一个总量，却丢弃贡献者的身份与分布**（`z = Σ w_i·x_i` 是多对一映射，从 `z` 无法还原谁强谁弱）。同一种病在评测端复现——总体准确率把关键切片淹进多数样本（详见 [[benchmark-evaluation]]）。点积天然允许**补偿**：实体维少掉的分可被话题、句式、领域相似度补回来，于是「必须满足的硬约束」退化成「可被其他相似性抵消的一项特征」。[[2026-07-25-aggregation-erases-minority-signals]]

判断一次聚合（mean-pooling 或任何 `[CLS]`/learned pooling）是否安全，问四件事——只要有一个否定，就该在聚合前保住结构：

```text
可交换   各项身份不重要，换位不改决策       实体「苹果↔微软」换位会改答案主体 → 否
可补偿   一项差可被另一项好抵消             实体错不该由话题像来补偿           → 否
近似同质 各项测量的是相近性质               实体/时间/否定承担不同语义角色      → 否
线性效用 总损失≈各项损失加权和             一个硬约束失败可令整段文档无关       → 否
```

这也是 Goodhart 定律的前置版本：通常说「指标成为目标后不再是好指标」，这里更早一步——**指标在被聚合出来的那一刻，可能就已不代表目标**。embedding 单向量和 benchmark 总分都是面向下游决策的「有损摘要」（像数据库优化器用 histogram 估行数会抹掉列间相关性）；真正的问题永远是：它丢掉的那一维相关性，恰不恰好是你的任务最在乎的那一条。

## 相关概念

- [[dense-passage-retrieval]] — Embedding 在检索中的应用
- [[colbert-retrieval]] — Token 级别的交互式嵌入
- [[benchmark-evaluation]] — 编码端 mismatch 与评测端聚合掩盖同构，都是过早聚合抹掉少数信号
- [[retrieval-augmented-generation]] — Embedding 是 RAG 的基础
- [[model-quantization]] — Embedding 模型的部署优化
