---
title: 杨松琳
created: 2026-05-05
updated: 2026-05-05
type: entity
tags: [person, lab, open-source, deeplearning]
sources: [raw/articles/attention-algorithm-innovation-2025.md]
---

# 杨松琳

MIT CSAIL PhD，研究方向为高效注意力机制/线性注意力，被称为"Linear Attention之母"。[[raw/articles/attention-algorithm-innovation-2025.md]]

## 背景

- MIT CSAIL 在读博士生
- 研究方向：高效注意力机制（Efficient Attention）、[[linear-attention]]

## 核心贡献

### Flash Linear Attention (FLA)
- 开源线性注意力计算库，被广泛采用
- 提供高效的 Linear Attention 实现基准

### 算法研究脉络
从 RetNet 获得启发，逐步推进 [[linear-attention]] 的发展：
1. RetNet → Gated Linear Attention → Delta Net → Gated Delta Net → KDA
2. 每一步都在 Decay 机制上做改进：从输入无关 → 输入相关 → 粗粒度 → 细粒度

### 工业合作
- 参与 Kimi Linear (KDA) 开发 — [[hybrid-attention]] 的代表实现
- 参与 Qwen3-Next 部分工作 — 采用 Gated Delta Net 的 [[hybrid-attention]]

## 观点

- 中国在算法创新上领先，因为算力有限倒逼 Efficiency 创新
- 硬件亲和是关键：算法必须能高效矩阵乘法
- 下一个架构突破点在 Attention（FFN 已被 MoE "雕"好）
- 最佳方案可能是 [[hybrid-vs-sparse-attention]] 中 Hybrid 的 Full 层换成 Sparse Attention

## 相关链接

- [[linear-attention]] — 核心研究领域
- [[hybrid-attention]] — 工业级应用架构
- [[sparse-attention]] — 对比路线
- [[hybrid-vs-sparse-attention]] — 路线对比
