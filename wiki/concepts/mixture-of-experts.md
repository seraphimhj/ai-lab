---
title: Mixture of Experts — 稀疏专家混合
created: 2026-05-10
updated: 2026-05-14
type: concept
tags: [architecture, efficiency, scaling]
sources: [raw/papers/2401.04088-Mixtral-of-Experts.html]
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

- 8 个专家，每层 8 个 feedforward block
- 每个 token 在每层由 router 选择 2 个专家处理并加性组合输出
- 总参数量：~47B，每 token 仅用 **13B 激活参数**
- 上下文长度：**32k tokens**
- 效果：超越或匹配 Llama 2 70B 和 GPT-3.5（所有评估基准）
- 在数学、代码生成和多语言基准上大幅超越 Llama 2 70B
- Mixtral 8×7B–Instruct 版本超越 GPT-3.5 Turbo、Claude-2.1、Gemini Pro（人类评估）
- 开源许可：Apache 2.0

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
- [[instruction-tuning]] — Mixtral-Instruct 使用 SFT + DPO 进行指令微调
