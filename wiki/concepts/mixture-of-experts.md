---
title: Mixture of Experts — 稀疏专家混合
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [architecture, efficiency, scaling]
sources: [raw/papers/2401.04088-Mixtral-of-Experts.md]
---

# Mixture of Experts — 稀疏专家混合

通过让模型包含多个"专家"子网络，但每次推理只激活其中少量专家，实现大模型容量与高效计算的平衡。[[raw/papers/2401.04088-Mixtral-of-Experts.html]]

## 核心思想

### 稠密模型 vs. MoE

| 特性 | 稠密模型 | MoE 模型 |
|------|---------|---------|
| 参数总量 | 全部参与计算 | 总量大，但每次只激活一部分 |
| 计算量 | 与参数量成正比 | 与激活参数量成正比 |
| 推理速度 | 慢 | 快（仅激活部分专家） |
| 模型容量 | 受限于计算预算 | 可以更大 |

## 架构设计

### Router（路由器）

- 一个轻量级门控网络
- 输入 token → 输出各专家的权重分布
- 选择 top-k 个专家（通常 k=1 或 k=2）

### Forward Pass

```
y = Σ G(x)_i × E_i(x)    # G: router, E: expert
```
其中只有 top-k 个 G(x)_i 非零。

### 典型配置（Mixtral 8×7B）

- 8 个专家，每个 7B 参数
- 总参数量：~47B
- 每个激活 2 个专家，实际计算量 ≈ 13B
- 效果接近 LLaMA 70B，但推理速度快数倍

## 训练挑战

### 负载均衡

Router 容易倾向于只使用少数专家，导致：
- 未使用的专家退化
- 负载不均

**解决方案**：
- 辅助损失（auxiliary loss）：鼓励均匀分配
- 噪声 Top-k：在路由中加入噪声增加探索

### Expert Dropout

某些专家可能变成"僵尸"专家，需要监控和调整。

## 发展脉络

| 模型 | 专家数 | Top-k | 总参数 |
|------|--------|-------|--------|
| Switch Transformer | 128-256 | 1 | 1.6T |
| GLaM | 64 | 1 | 1.2T |
| Mixtral 8×7B | 8 | 2 | 47B |
| DeepSeek-V2 | 160 | 6 | 236B |
| DeepSeek-V3 | 256 | 8 | 671B |

## 相关概念

- [[scaling-laws]] — MoE 提供了新的缩放维度
- [[model-quantization]] — 与 MoE 配合进一步压缩
- [[flash-attention]] — MoE 模型训练依赖高效注意力
- [[linear-attention]] — MoE + Linear Attention 可以进一步降低推理成本
