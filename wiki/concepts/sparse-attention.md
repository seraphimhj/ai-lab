---
title: 稀疏注意力机制
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [architecture, deeplearning, optimization, inference]
sources: [raw/articles/attention-algorithm-innovation-2025.md]
---

# 稀疏注意力机制（Sparse Attention）

通过选择性计算部分 Token 的注意力来降低计算量的注意力变体，DeepSeek 为代表路线。[[raw/articles/attention-algorithm-innovation-2025.md]]

## 核心思路

- 每一层都是 Sparse Attention，无 Full Attention 层
- 用 **Indexer**（蒸馏训练）选择 Top-K Token 参与注意力计算
- 选择的 Token 数远小于序列长度，从而减少计算量

## 技术实现

### Indexer 机制
- 通过蒸馏训练一个 Indexer 网络
- Indexer 为每个 Query 选择最相关的 Top-K Key
- 只对选中的 Token 计算注意力，跳过其余

### 训练策略
- Indexer 需要与主模型联合训练
- 蒸馏目标：模拟 Full Attention 的行为

## 优缺点[[raw/articles/attention-algorithm-innovation-2025.md]]

| 维度 | Sparse Attention |
|------|-----------------|
| 计算 | ✅ 省 FLOPs（只计算 Top-K） |
| KV Cache | ❌ 不省（仍需存储完整 KV） |
| 长文本 | ⚠️ 长度上去后需要 KV Cache 压缩 |
| Retrieval | ✅ 比 [[linear-attention]] 的 Retrieval 能力更强 |
| 表达力 | ✅ 保留 Full Attention 的表达力 |

## 与 Linear Attention 的关键区别

- Sparse Attention **省 FLOPs 但不省 KV Cache**
- [[linear-attention]] **省 KV Cache 但表达力受限**
- 两者互补，最佳方案可能是结合使用（见 [[hybrid-vs-sparse-attention]]）

## 代表模型

- **DeepSeek V3/R1**：Sparse Attention 的主要实践者
- DeepSeek MLA (Multi-head Latent Attention) 是另一条路线

## 相关链接

- [[linear-attention]] — 对比路线
- [[hybrid-attention]] — 混合方案
- [[hybrid-vs-sparse-attention]] — 详细对比
