---
title: 模型量化
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [efficiency, optimization, deployment]
sources: [raw/papers/2210.17323-GPTQ-Accurate-Post-Training-Quantization-for-Generative-Pre.html, raw/papers/2301.00774-SparseGPT-Massive-Language-Models-Can-Be-Accurately-Pruned-i.html, raw/papers/2306.00978-AWQ-Activation-aware-Weight-Quantization-for-LLM-Compression.html]
---

# 模型量化

将模型权重从高精度浮点数（FP16/BF16）转换为低精度表示（INT8/INT4），以减少模型大小和加速推理。

## 基本原理

量化将连续的浮点值映射到离散的量化点：
```
w_quant = round(w / scale) × scale
```
- **scale**：缩放因子
- 量化粒度可以是 per-tensor、per-channel 或 per-group

## 量化位宽与效果

| 位宽 | 模型大小（相对 FP16） | 精度损失 | 推理加速 |
|------|---------------------|---------|---------|
| FP16/BF16 | 1× | 无 | 基线 |
| INT8 | 0.5× | 极小 | 1.5-2× |
| INT4 | 0.25× | 小 | 2-4× |
| INT3 | ~0.2× | 中等 | 3-5× |
| INT2 | ~0.15× | 较大 | 4-6× |

## 主要方法

### GPTQ[[raw/papers/2210.17323-GPTQ-Accurate-Post-Training-Quantization-for-Generative-Pre.html]]

- 基于近似二阶信息（Hessian）的逐层量化
- OBS（Optimal Brain Surgeon）框架
- 支持 INT4/INT3 量化
- 权重聚类 + 懒更新优化

### AWQ[[raw/papers/2306.00978-AWQ-Activation-aware-Weight-Quantization-for-LLM-Compression.html]]

- **Activation-aware**：保护对激活值影响大的权重通道
- 核心洞察：仅 1% 的权重通道对量化敏感
- 保护敏感通道不进行激进量化
- 比 GPTQ 在同等精度下更快

### SparseGPT[[raw/papers/2301.00774-SparseGPT-Massive-Language-Models-Can-Be-Accurately-Pruned-i.html]]

- 将量化和稀疏化（剪枝）结合
- 基于 Hessian 的权重剪枝 + 量化
- 可以同时实现 50% 稀疏 + 4-bit 量化

## 量化类型

| 类型 | 训练需求 | 效果 | 适用场景 |
|------|---------|------|---------|
| PTQ（训练后量化） | 无需训练 | 好 | 快速部署 |
| QAT（量化感知训练） | 需要微调 | 最好 | 精度敏感 |
| 混合精度 | 部分层量化 | 平衡 | 大模型 |

## 实践建议

- INT4 量化通常是最优性价比选择
- 使用 AWQ 保护重要通道
- 结合 [[lora]]（QLoRA）可以在量化后微调恢复精度

## 相关概念

- [[lora]] — QLoRA 结合量化与低秩微调
- [[mixture-of-experts]] — 稀疏化降低计算量
- [[flash-attention]] — 量化与高效注意力配合使用
