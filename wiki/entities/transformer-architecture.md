---
title: Transformer 架构
created: 2026-05-10
updated: 2026-05-10
type: entity
tags: [model, architecture, deeplearning, nlp]
sources: [raw/papers/1706.03762-Attention Is All You Need.html]
---

# Transformer 架构

Transformer 是 2017 年由 Google 团队提出的深度学习架构，完全基于 Self-Attention 机制，摒弃了 RNN 和 CNN 的递归与卷积结构。论文标题 "Attention Is All You Need" 准确概括了其核心思想。Transformer 奠定了现代大语言模型（LLM）的基础架构，几乎所有后续主流模型都基于它构建。[[raw/papers/1706.03762-Attention Is All You Need.html]]

## 核心组件

### Self-Attention

Self-Attention 是 Transformer 的核心机制，通过 Query、Key、Value 三个矩阵计算序列中每个 Token 与其他所有 Token 的关联权重。Scaled Dot-Product Attention 的计算公式为：

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

缩放因子 $\sqrt{d_k}$ 防止点积值过大导致 softmax 梯度消失。

### Multi-Head Attention

将 Q、K、V 分别投影到多个子空间，并行计算多组 Attention 后拼接。多头机制允许模型同时关注不同位置的不同表示子空间。

### Position-wise Feed-Forward

每个位置独立应用两层全连接网络，中间使用 ReLU 激活。公式为 $\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$。

### Positional Encoding

由于 Transformer 不含递归结构，需要通过 Positional Encoding 注入位置信息。原论文使用正弦/余弦函数生成位置编码。

### Layer Normalization & Residual Connection

每个子层（Attention + FFN）都使用残差连接和 Layer Normalization，有效缓解深层网络的训练难度。

## Encoder-Decoder 结构

原论文采用 Encoder-Decoder 架构用于机器翻译：

- **Encoder**：N 层堆叠，每层包含 Multi-Head Self-Attention + FFN
- **Decoder**：N 层堆叠，额外增加 Masked Self-Attention（防止看到未来 Token）和 Cross-Attention（关注 Encoder 输出）

## 影响与变体

- [[bert]] 采用纯 Encoder 结构，开创双向预训练范式
- [[gpt-3]] 采用纯 Decoder 结构，推动自回归语言模型发展
- [[claude-code]] 等现代 AI Agent 背后的基础模型均基于 Transformer 架构

## 训练效率

Transformer 的并行化能力远超 RNN：由于 Self-Attention 可以并行计算所有位置的注意力权重，训练时间从 RNN 的数周缩短到数天。原论文在 8 块 GPU 上仅需 3.5 天完成 WMT 英德翻译训练。
