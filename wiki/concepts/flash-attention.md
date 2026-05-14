---
title: FlashAttention — 高效注意力计算
created: 2026-05-10
updated: 2026-05-14
type: concept
tags: [efficiency, optimization, architecture]
sources: [raw/papers/2205.14135-FlashAttention-1.html, raw/papers/2307.08691-FlashAttention-2.html, raw/papers/2407.08608-FlashAttention-3-Fast-and-Accurate-Attention-with-Asynchrony.html]
---

# FlashAttention — 高效注意力计算

通过 IO-aware 分块计算和硬件优化，在不牺牲精度的前提下大幅加速 Attention 计算。已成为大模型训练和推理的事实标准。

## 问题背景

标准 Attention 计算有两个瓶颈：
1. **内存瓶颈**：需要存储 L×L 的注意力矩阵（L 为序列长度）
2. **IO 瓶颈**：大量 HBM（显存）到 SRAM（缓存）的读写

## 核心技术

### FlashAttention 1（2022）[[raw/papers/2205.14135-FlashAttention-1.html]]

- **分块计算（Tiling）**：将 Q、K、V 分块加载到 SRAM 中计算
- **在线 Softmax**：分块计算时递归更新 Softmax 的分母
- **反向传播重计算**：不存储注意力矩阵，反向传播时重新计算
- 效果：2-4× 加速，减少内存峰值

### FlashAttention 2（2023）[[raw/papers/2307.08691-FlashAttention-2.html]]

- 优化工作分配：减少非矩阵乘法的 FLOPs
- **并行化**：在不同维度（序列、头、batch）上并行
- 效果：比 FlashAttention 1 再快 2×

### FlashAttention 3（2024）[[raw/papers/2407.08608-FlashAttention-3-Fast-and-Accurate-Attention-with-Asynchrony.html]]

- 针对 Hopper GPU (H100) 的异步执行
- **流水线**：将 FP8 量化、矩阵乘法、Softmax 重叠执行
- 利用 FP8 Tensor Core
- 效果：比 FlashAttention 2 再快 1.5-2×

## 复杂度对比

| 方法 | 时间复杂度 | 内存复杂度 | 是否精确 |
|------|-----------|-----------|---------|
| 标准 Attention | O(L²d) | O(L²) | 精确 |
| Sparse Attention | O(L√L d) | O(L√L) | 近似 |
| FlashAttention | O(L²d) | O(L) | 精确 |
| [[linear-attention]] | O(Ld²) | O(L) | 近似 |

## 影响与地位

FlashAttention 是现代 LLM 训练的基石：
- 几乎所有主流模型（[[llama]]、[[deepseek]]、[[qwen]]）都使用 FlashAttention
- 使得长序列训练成为可能，是 [[long-context-extension]] 的基础设施
- 催生了更多 IO-aware 算法的研究
- Ring Attention 将 FlashAttention 的 blockwise 思想扩展到多设备分布式长序列训练

## 相关概念

- [[linear-attention]] — 另一种降低注意力复杂度的方向
- [[sparse-attention]] — 稀疏注意力方法
- [[hybrid-attention]] — 结合多种注意力机制
- [[mixture-of-experts]] — 与 FlashAttention 配合提升整体效率
