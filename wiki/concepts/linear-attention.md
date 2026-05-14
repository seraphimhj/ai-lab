---
title: 线性注意力机制
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [architecture, deeplearning, optimization, inference]
sources: [raw/articles/attention-algorithm-innovation-2025.md]
---

# 线性注意力机制（Linear Attention）

通过去掉 Softmax 归一化，将注意力计算从 O(L²) 降至 O(L) 的注意力变体。[[raw/articles/attention-algorithm-innovation-2025.md]]

## 核心原理

### Softmax Attention（标准注意力）
```
Q × K → L×L 矩阵 → Softmax → ×V
```
- 复杂度：O(L²)
- 需要存储完整 KV Cache
- 表达力强，是当前主流

### Linear Attention
```
去掉 Softmax → 可写成 RNN 推理形式 → 每步 O(1) → 整体 O(L)
```
- 复杂度：O(L)
- **省 KV Cache**：推理时仅需维护一个固定大小的隐藏状态
- 解码速度快，可加大 Batch Size

## 关键劣势

纯 Linear Attention 不 Work：
- RNN 状态恒定，无法像 Softmax 那样动态调整注意力分配
- 长文本场景有缺陷，信息可能被错误遗忘或保留

## 发展脉络[[raw/articles/attention-algorithm-innovation-2025.md]]

| 阶段 | 方法 | 关键改进 |
|------|------|----------|
| 2020 | 最早 Linear Attention | 去掉 Softmax，效果不好 |
| 2023 | RetNet | 加输入无关的 Decay（0.99 遗忘率） |
| 2024 | Gated Linear Attention | 加门控机制，Decay 变成输入相关 |
| 2024 | Delta Net | 用 Delta Rule 替代 Hebbian Rule，有减法操作（定向删除） |
| 2024 | Gated Delta Net | 合并门控 + Delta Rule，但受限于效率用粗粒度 Decay |
| 2025 | KDA (Kimi Delta Attention) | 细粒度 Decay，每个维度独立衰减率 |

### Decay 机制演进逻辑

1. **无 Decay** → 长距离信息爆炸
2. **输入无关 Decay (RetNet)** → 固定遗忘率，不够灵活
3. **输入相关 Decay (Gated LA)** → 门控决定遗忘，更灵活
4. **有减法 (Delta Net)** → 不仅能"减弱"，还能"删除"旧信息
5. **细粒度 Decay (KDA)** → 每个维度独立衰减率，精确控制

## 工业应用

纯 Linear Attention 很少单独使用，通常作为 [[hybrid-attention]] 的组成部分：
- 大部分层用 Linear Attention（省 KV Cache）
- 少量层用 Full/Sparse Attention（保表达力）

## 相关链接

- [[yang-songlin]] — Linear Attention 核心研究者
- [[hybrid-attention]] — 工业级混合架构
- [[sparse-attention]] — 另一条效率路线
- [[hybrid-vs-sparse-attention]] — 路线对比
