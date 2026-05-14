---
title: 文本嵌入/向量化
created: 2026-05-10
updated: 2026-05-14
type: concept
tags: [embedding, representation, retrieval]
sources: [raw/papers/1908.10084-Sentence-BERT-Sentence-Embeddings-using-Siamese-BERT-Networks.html, raw/papers/2212.03533-Text-Embeddings-by-Weakly-Supervised-Contrastive-Pre-training.html, raw/papers/2210.07316-MTEB-Massive-Text-Embedding-Benchmark.html, raw/papers/2402.03216-M3-Embedding-Multi-Linguality-Multi-Functionality-Multi-Granularity-Text-Embeddi.html, raw/papers/2405.17428-NV-Embed-Improved-Techniques-for-Training-LLMs-as-Generalist-Embedding-Models.html, raw/papers/2506.05176-Qwen3-Embedding-Advancing-Text-Embedding-and-Reranking-Through-Foundation-Models.html, raw/papers/2602.15547-jina-embeddings-v5-text-Task-Targeted-Embedding-Distillation.html]
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

## 相关概念

- [[dense-passage-retrieval]] — Embedding 在检索中的应用
- [[colbert-retrieval]] — Token 级别的交互式嵌入
- [[retrieval-augmented-generation]] — Embedding 是 RAG 的基础
- [[model-quantization]] — Embedding 模型的部署优化
