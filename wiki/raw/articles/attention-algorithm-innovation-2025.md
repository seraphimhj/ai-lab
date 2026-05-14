---
source_url: https://mp.weixin.qq.com/s/USj6wbOI8CD0MTQCQ01hXQ
ingested: 2026-05-05
sha256: 10aaaad8e8675d41640a34d1841b67912e952e0b71294346f5aa673ed1e4b518
---
# 下一代Attention算法改进的猜想

**作者：** 张小珺 × 杨松琳（MIT CSAIL PhD）
**日期：** 2025-11-10
**来源：** 微信公众号「语言即世界language is world」
**URL：** https://mp.weixin.qq.com/s/USj6wbOI8CD0MTQCQ01hXQ

---

## 嘉宾介绍

杨松琳，MIT CSAIL PhD，研究方向为高效注意力机制/线性注意力。Flash Linear Attention (FLA) 开源库作者，被称为"Linear Attention之母"。参与 Kimi Linear (KDA) 和 Qwen3-Next 部分工作。

## Linear Attention 核心原理

### Softmax Attention
- Q×K → L×L 矩阵 → Softmax → ×V
- 复杂度 O(L²)
- 需要存储完整 KV Cache

### Linear Attention
- 去掉 Softmax → 可写成 RNN 推理形式 → 每步 O(1) → 整体 O(L)
- 关键优势：省 KV Cache、解码快、可加大 Batch Size
- 关键劣势：纯 Linear 不 Work（RNN 状态恒定，长文本有缺陷）

## Linear Attention 发展脉络

1. **2020年：最早 Linear Attention**，效果不好
2. **RetNet**：加输入无关的 Decay（0.99 遗忘率）
3. **Gated Linear Attention**：加门控机制，Decay 变成输入相关
4. **Delta Net**：用 Delta Rule 替代 Hebbian Rule，有减法操作（定向删除）
5. **Gated Delta Net**：合并门控 + Delta Rule，但受限于效率用粗粒度 Decay
6. **KDA (Kimi Delta Attention)**：细粒度 Decay，每个维度独立衰减率

## Hybrid Attention 架构

- 核心思路：部分层 Softmax Attention（保表达力）+ 大部分层 Linear Attention（省 KV Cache）
- 比例共识：3:1（3 层 Linear + 1 层 Full）
- Minimax M1 曾用 7:1（过于激进）
- 已知弱点：Multi-Hop Reasoning 多跳推理会掉点
- 代表：Kimi Linear, Qwen3-Next, MiMo-V2

## Sparse Attention（DeepSeek 路线）

- 每一层都是 Sparse Attention，无 Full Attention 层
- 用 Indexer（蒸馏训练）选择 Top-K Token
- 优点：省 FLOPs，Retrieval 能力更强
- 缺点：不省 KV Cache，长度上去后需要 KV Cache 压缩

## 未来方向

- 最佳结合：Hybrid 中的 Full Attention 层换成 Sparse Attention
- 中国算法创新领先：因算力有限，对 Efficiency 要求更高
- 硬件亲和是关键：算法必须能高效矩阵乘法
- 下一个架构突破点在 Attention（FFN 已被 MoE "雕"好）

## 各公司选择

- **DeepSeek**: Sparse Attention
- **Kimi**: Linear/Hybrid Attention (KDA)
- **Minimax**: M1 Linear → M2 回退 Full Attention（Lightning Attention 太弱 + 评估不充分）
- **Qwen**: Hybrid Attention (Gated Delta Net)
- **OpenAI**: Sliding Window Attention + Full Attention
