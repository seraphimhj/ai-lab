---
title: 混合注意力架构
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [architecture, deeplearning, optimization, inference]
sources: [raw/articles/attention-algorithm-innovation-2025.md]
---

# 混合注意力架构（Hybrid Attention）

将 [[linear-attention]] 与 Full/Sparse Attention 按层混合的架构设计，兼顾推理效率与表达力。[[raw/articles/attention-algorithm-innovation-2025.md]]

## 核心思路

- **Linear Attention 层**（多数）：省 KV Cache、加速解码、支持大 Batch Size
- **Full/Sparse Attention 层**（少数）：保持强表达力，支持复杂推理

## 比例共识

行业逐步收敛到 **3:1** 比例（3 层 Linear + 1 层 Full）：
- [[mimo-v2]] 采用此比例
- Kimi Linear (KDA) 采用此比例
- Qwen3-Next (Gated Delta Net) 采用此比例

Minimax M1 曾尝试 **7:1**（过于激进），M2 已回退 Full Attention。

## 已知弱点

**Multi-Hop Reasoning（多跳推理）会掉点**[[raw/articles/attention-algorithm-innovation-2025.md]]
- 多跳推理需要跨多层传递精确信息
- Linear 层的信息压缩可能丢失关键细节
- Full Attention 层间隔过远时会加剧此问题

## 代表模型

| 模型 | Linear 层类型 | Full 层类型 | 比例 |
|------|--------------|-------------|------|
| Kimi Linear | KDA | Full Attention | 3:1 |
| Qwen3-Next | Gated Delta Net | Full Attention | 3:1 |
| [[mimo-v2]] | Linear | Sliding Window | 3:1 |
| Minimax M1 | Lightning Attention | Full Attention | 7:1（已弃用） |

## 未来演进

最佳方案可能是将 Hybrid 中的 Full Attention 层换成 [[sparse-attention]]，兼顾效率与表达力。[[raw/articles/attention-algorithm-innovation-2025.md]]

## 相关链接

- [[linear-attention]] — Linear 层的技术基础
- [[sparse-attention]] — Full 层的潜在替代方案
- [[hybrid-vs-sparse-attention]] — 路线对比
- [[yang-songlin]] — 核心研究者
- [[mimo-v2]] — 代表模型
