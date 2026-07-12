---
title: 2025-2026 Embedding 大模型全面对比
created: 2026-05-10
updated: 2026-05-10
type: comparison
tags: [comparison, embedding, mteb, retrieval, open-source, commercial-api]
sources: [raw/papers/2506.05176-Qwen3-Embedding-Advancing-Text-Embedding-and-Reranking-Through-Foundation-Models.html, raw/papers/2602.15547-jina-embeddings-v5-text-Task-Targeted-Embedding-Distillation.html, raw/papers/2405.17428-NV-Embed-Improved-Techniques-for-Training-LLMs-as-Generalist-Embedding-Models.html, raw/papers/2308.03281-Towards-General-Text-Embeddings-with-Multi-stage-Contrastive-Learning.pdf, raw/papers/2402.03216-M3-Embedding-Multi-Linguality-Multi-Functionality-Multi-Granularity-Text-Embeddi.html, raw/papers/1908.10084-Sentence-BERT-Sentence-Embeddings-using-Siamese-BERT-Networks.html]
---

# 2025-2026 Embedding 大模型全面对比

基于最新 MTEB (Massive Text Embedding Benchmark) 排名，按参数量分档梳理当前主流 Embedding 模型。[[raw/papers/2210.07316-MTEB-Massive-Text-Embedding-Benchmark.html]]

## 📊 总览表

### ≥8B 大参数量模型

| 模型 | 参数量 | 类型 | MTEB Eng v2 | MTEB 多语言 | 维度 | 上下文 | 备注 |
|------|--------|------|-------------|-------------|------|--------|------|
| **Qwen3-Embedding-8B** | 8B | 开源 | **75.22** | **70.58 (#1)** | 4096 | 32K | 综合最强，多语言冠军 |
| **microsoft/harrier-oss-v1-27b** | 27B | 开源 | 74.3 | — | — | — | 微软旗舰，推理成本高 |
| **Octen-Embedding-8B** | 8B | 开源 | — | — | — | — | RTEB #1 (0.8045) |

### 1B–8B 中参数量模型

| 模型 | 参数量 | 类型 | MTEB Eng v2 | MTEB 多语言 | 维度 | 上下文 | 备注 |
|------|--------|------|-------------|-------------|------|--------|------|
| **Qwen3-Embedding-4B** | 4B | 开源 | **74.60** | — | 2560 | 32K | 性价比极高 |
| **gte-Qwen2-7B-instruct** | 7.6B | 开源 | 70.72 | — | 3584 | 32K | Google 出品 |
| **NV-Embed-v2** | 7.8B | 开源 | 69.81 | — | 4096 | 128K | 超长上下文 |

### <1B 轻量模型

| 模型 | 参数量 | 类型 | MTEB Eng v2 | MTEB 多语言 | 维度 | 上下文 | 备注 |
|------|--------|------|-------------|-------------|------|--------|------|
| **jina-embeddings-v5-text-small** | 677M | 开源 | 71.7 | 67.7 | 1024 | 8K | 小模型中英文最强 |
| **Qwen3-Embedding-0.6B** | 0.6B | 开源 | 70.70 | — | 1024 | 32K | 超小体积高性能 |
| **stella_en_1.5B_v5** | 1.5B | 开源 | 69.43 | — | 2048 | 32K | 均衡之选 |
| **BGE M3** | 0.57B | 开源 | — | — | 1024 | 8K | 经典多功能模型 |

### 商业 API 模型

| 模型 | 提供商 | MTEB Eng v2 | 维度 | 上下文 | 备注 |
|------|--------|-------------|------|--------|------|
| **gemini-embedding-exp** | Google | 73.3 | 3072 | — | 闭源最强之一 |
| **text-embedding-3-large** | OpenAI | 66.5 | 3072 | 8K | 生态最成熟 |
| **Voyage 3/4** | Voyage AI | ~72+ | 1024 | 32K | 检索专精 |
| **embed v4** | Cohere | ~71+ | 1024 | 128K | 多语言支持好 |

## 🔑 关键发现

### Qwen3-Embedding 系列统治榜单

Qwen3-Embedding 三尺寸（0.6B / 4B / 8B）覆盖全场景，8B 版本拿下 MTEB Eng v2 **75.22** 和多语言 **70.58** 双榜第一。[[raw/papers/2506.05176-Qwen3-Embedding-Advancing-Text-Embedding-and-Reranking-Through-Foundation-Models.html]]

核心训练技术：
- **多阶段对比学习**：从弱监督预训练到指令微调
- **MRL (Matryoshka Representation Learning)**：支持灵活维度截断
- **长上下文训练**：32K context window

### 轻量模型亮点

jina-embeddings-v5-text-small 以仅 677M 参数达到 71.7 MTEB 分数，通过 Task-Targeted Embedding Distillation 实现。[[raw/papers/2602.15547-jina-embeddings-v5-text-Task-Targeted-Embedding-Distillation.html]]

### 开源 vs API 趋势

2025-2026 年开源 Embedding 模型全面超越商业 API。Qwen3-Embedding-8B (75.22) vs OpenAI text-embedding-3-large (66.5) 差距近 **9 分**。

## 选型建议

| 场景 | 推荐 |
|------|------|
| 多语言通用 | Qwen3-Embedding-8B |
| 高性价比英文 | Qwen3-Embedding-4B |
| 边缘部署 | jina-embeddings-v5-text-small / Qwen3-Embedding-0.6B |
| 超长文档 | NV-Embed-v2 (128K) |
| 快速集成、无需部署 | gemini-embedding-exp |

## 相关链接

- [[text-embedding]] — MTEB 基准详解
- [[text-embedding]] — BGE 系列模型
- [[text-embedding]] — Embedding 模型鼻祖
- [[rag-approaches]] — Embedding 在 RAG 中的应用
- [[dense-passage-retrieval]] — 密集检索基础
