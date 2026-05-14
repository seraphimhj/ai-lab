---
title: Hybrid Linear Attention vs Sparse Attention 对比
created: 2026-05-05
updated: 2026-05-05
type: comparison
tags: [architecture, comparison, optimization, inference, deeplearning]
sources: [raw/articles/attention-algorithm-innovation-2025.md]
---

# Hybrid Linear Attention vs Sparse Attention

两种降低注意力计算成本的主流路线对比。[[raw/articles/attention-algorithm-innovation-2025.md]]

## 核心区别

| 维度 | Hybrid Linear Attention | Sparse Attention |
|------|------------------------|-----------------|
| **核心方法** | 部分层用 [[linear-attention]]，少部分层用 Full Attention | 每层都用 [[sparse-attention]]，Indexer 选 Top-K Token |
| **FLOPs** | Linear 层省 FLOPs | 省 FLOPs（只计算 Top-K） |
| **KV Cache** | ✅ 大幅节省（Linear 层无需 KV Cache） | ❌ 不节省（仍需完整 KV） |
| **表达力** | ⚠️ Full 层保表达力，但比例有限 | ✅ 保留 Full Attention 表达力 |
| **多跳推理** | ❌ 弱点，Multi-Hop Reasoning 会掉点 | ✅ 比 Linear 强 |
| **Retrieval** | ⚠️ 中等 | ✅ 更强 |
| **长文本扩展** | ✅ KV Cache 小，易扩展 | ⚠️ 需要 KV Cache 压缩 |
| **Batch Size** | ✅ 可加大 | ❌ 受 KV Cache 限制 |

## 代表模型

### Hybrid Linear Attention 路线
- **Kimi Linear (KDA)**：[[linear-attention]] + Full Attention，3:1
- **Qwen3-Next**：Gated Delta Net + Full Attention，3:1
- **[[mimo-v2]]**：Linear + Sliding Window，3:1
- **Minimax M1**：Lightning Attention + Full，7:1（已弃用，M2 回退 Full）

### Sparse Attention 路线
- **DeepSeek V3/R1**：Indexer + Sparse Attention

### 其他路线
- **OpenAI**：Sliding Window Attention + Full Attention

## 各公司选择逻辑[[raw/articles/attention-algorithm-innovation-2025.md]]

| 公司 | 选择 | 理由 |
|------|------|------|
| DeepSeek | Sparse | 算力强，更关注 FLOPs 效率 |
| Kimi | Hybrid (KDA) | 追求长文本效率，需省 KV Cache |
| Minimax | M1 Hybrid → M2 Full | Lightning Attention 太弱 + 评估不充分 |
| Qwen | Hybrid (Gated Delta Net) | 平衡效率与表达力 |
| OpenAI | Sliding Window + Full | 算力充足，Sliding Window 足够 |

## 未来方向

最佳结合方案可能是：**Hybrid 架构中的 Full Attention 层换成 Sparse Attention**[[raw/articles/attention-algorithm-innovation-2025.md]]
- 用 Linear 层省 KV Cache
- 用 Sparse 层保表达力 + 省 FLOPs
- 兼顾两条路线的优势

## 相关链接

- [[linear-attention]] — Hybrid 中 Linear 层的技术基础
- [[sparse-attention]] — Sparse 路线详解
- [[hybrid-attention]] — Hybrid 路线详解
- [[yang-songlin]] — 核心研究者观点
- [[mimo-v2]] — Hybrid 路线代表模型
