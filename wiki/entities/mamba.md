---
title: Mamba SSM
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, architecture, deeplearning, optimization]
sources: [raw/papers/2312.00752-Mamba-Linear-Time-Sequence-Modeling.pdf]
---

# Mamba SSM

Mamba 是一种基于选择性状态空间模型（Selective State Space Model）的序列建模架构，由 Tri Dao 和 Albert Gu 提出。Mamba 实现了线性时间复杂度的序列建模，在推理效率上显著优于基于 [[transformer-architecture]] 的注意力机制。[[raw/papers/2312.00752-Mamba-Linear-Time-Sequence-Modeling.pdf]]

## 核心动机

Transformer 的 Self-Attention 机制计算复杂度为 O(N²)，限制了其在长序列上的应用。Mamba 旨在保持 Transformer 级别的建模能力，同时实现 O(N) 的推理复杂度。

## State Space Model (SSM) 基础

SSM 将序列建模视为连续系统：

$$h'(t) = Ah(t) + Bx(t)$$
$$y(t) = Ch(t) + Dx(t)$$

通过离散化后可以在序列数据上高效计算。传统 SSM（如 S4）的参数 A、B、C 是静态的，不随输入变化。

## 选择性机制（Selective Mechanism）

Mamba 的关键创新是使 SSM 参数**依赖于输入**：

- **选择性扫描**：输入依赖的 B、C 参数使模型可以选择性地记忆或遗忘信息
- **硬件感知算法**：通过扫描而非卷积的方式计算，优化 GPU 利用率
- **输入依赖的步长**：允许模型自适应地控制信息更新速率

## 模型规格

- **Mamba-1**：基础版本，1.3B/2.8B 参数
- **Mamba-2**：结构化状态空间对偶（SSD）框架，与注意力机制建立理论联系
- 支持无限上下文长度（理论上）
- 推理时 O(N) 时间和 O(1) 状态空间复杂度

## 性能表现

Mamba 在多个领域展现出竞争力：

- 语言建模：在 Pile 基准上与同规模 Transformer 持平
- 长序列建模：在信息检索和基因组学任务上优于 Transformer
- 推理效率：推理吞吐量显著高于 Attention-based 模型

## 混合架构

实际应用中，Mamba 常与 [[transformer-architecture]] 结合使用：

- Jamba 将 Mamba 层与 Attention 层交替堆叠
- Griffin 结合 Gated Linear Recurrences 与 Local Attention

## 局限性

- 在需要精确 recall 的任务上不如 Attention
- 长上下文训练的稳定性有待改进
- 生态和工具链不如 Transformer 成熟

## 影响

Mamba 开辟了超越 Transformer 的序列建模新方向，激发了学术界对线性时间序列模型的广泛研究。其 selective scan 设计与 [[deepseek]] 等团队的高效推理优化方向相呼应。
