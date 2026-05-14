---
title: Mistral 7B
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, open-source, llm, deeplearning]
sources: [raw/papers/2310.06825-Mistral-7B.html]
---

# Mistral 7B

Mistral 7B 是法国 AI 公司 Mistral AI 发布的 7B 参数开源语言模型。尽管参数量仅 73 亿，Mistral 7B 在多项基准上超越了 LLaMA 2 13B，成为小模型高效训练的标杆。[[raw/papers/2310.06825-Mistral-7B.html]]

## 核心架构创新

### Sliding Window Attention (SWA)

Mistral 7B 引入了滑动窗口注意力机制，每个 Token 仅关注固定窗口内的 Token（默认 4096）。SWA 实现了线性推理复杂度，同时通过信息传播保持全局上下文感知。

### Grouped-Query Attention (GQA)

使用 GQA 替代标准 MHA，减少 KV Cache 的内存占用。GQA 在 MHA 和 MQA 之间取得平衡，兼顾性能和效率。

### Rolling Buffer Cache

结合 SWA 的滚动缓存机制，允许在有限显存下处理任意长度的序列。

## 训练配置

| 参数 | 值 |
|------|-----|
| dim | 4096 |
| n_layers | 32 |
| head_dim | 128 |
| hidden_dim | 14336 |
| n_heads | 32 |
| n_kv_heads | 8 |
| window_size | 4096 |
| context_len | 8192 |
| vocab_size | 32000 |

- 参数量：7.3B
- 上下文窗口：8K（有效窗口 4096）
- 词表大小：32K (BPE tokenizer)
- 开源许可：Apache 2.0

## 性能表现

Mistral 7B 在所有评估基准上超越了 LLaMA 1 13B 和 LLaMA 2 13B：

- MMLU：62.5%
- HumanEval：31.2%
- GSM8K：52.2%
- 在推理、数学和代码任务上表现尤为突出

## 版本变体

- **Mistral 7B Base**：基础预训练模型
- **Mistral 7B Instruct**：通过 SFT 对齐的指令模型
- **Mistral 7B GPTQ**：量化版本，适配消费级 GPU

## 开源策略

Mistral 7B 采用 Apache 2.0 许可证，完全开放权重，允许商业使用。这一策略使其迅速成为开源社区最受欢迎的小模型之一。

## 后续影响

Mistral 7B 的成功催生了 [[mixtral]] MoE 架构模型，也推动了社区对小模型高效架构的研究。其 SWA 和 GQA 设计被后续许多模型采纳。基于 [[transformer-architecture]] 的高效设计使其成为开源社区最广泛使用的基座模型之一。

## 与其他小模型对比

- 相比 [[phi]] 系列，Mistral 更注重通用能力而非数据质量策略
- 相比 [[gemma]] 系列，Mistral 的开源许可更加宽松
- Mistral 的 SWA 设计启发了 [[deepseek]] 的注意力优化方向
