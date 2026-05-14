---
title: LoRA — 低秩微调
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [training, efficiency, fine-tuning]
sources: [raw/papers/2106.09685-LoRA-Low-Rank-Adaptation-of-Large-Language-Models.md]
---

# LoRA — 低秩微调

在冻结预训练模型参数的同时，通过注入可训练的低秩矩阵来实现高效微调。[[raw/papers/2106.09685-LoRA-Low-Rank-Adaptation-of-Large-Language-Models.html]]

## 核心原理

### 低秩假设

模型微调时的权重更新矩阵 ΔW 具有低秩特性（intrinsic dimensionality 很低）：
```
W_new = W_0 + ΔW = W_0 + B × A
```
其中 W_0 冻结，A ∈ R^(r×k)，B ∈ R^(d×r)，r << min(d, k)。

### 训练方式

- **冻结**原始权重 W_0
- 只训练低秩矩阵 A 和 B
- 推理时可以合并：W_new = W_0 + BA，无额外推理延迟

## 关键设计选择

| 设计选择 | 说明 |
|---------|------|
| 秩 r | 通常 4-64，越大表达能力越强但参数越多 |
| 应用层 | 通常只对 Attention 的 Q/K/V/O 投影加 LoRA |
| 初始化 | A 用高斯随机初始化，B 用零初始化 |
| Alpha 缩放 | ΔW = (α/r) × BA，控制更新幅度 |

## 参数效率

以 7B 模型为例：
- 全量微调：~7B 可训练参数
- LoRA (r=16)：仅 ~4-10M 可训练参数（减少 99.8%+）

## 变体与扩展

| 变体 | 核心改进 |
|------|---------|
| QLoRA | 将基模型量化到 4-bit，LoRA 权重保持 bf16 |
| LoRA+ | 对 A 和 B 使用不同学习率 |
| DoRA | 将权重分解为幅度和方向，LoRA 只调整方向 |
| LongLoRA | 扩展 LoRA 支持长上下文微调 |

## 应用场景

- [[instruction-tuning]] 的高效实现
- 多任务适配（每个任务一个 LoRA adapter）
- 领域定制（医疗、法律等领域微调）

## 相关概念

- [[instruction-tuning]] — LoRA 常用于指令微调
- [[model-quantization]] — QLoRA 结合量化和 LoRA
- [[scaling-laws]] — 指导 LoRA 超参数选择
