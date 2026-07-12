---
title: LLaMA 系列
created: 2026-05-10
updated: 2026-05-10
type: entity
tags: [model, open-source, llm, deeplearning]
sources: [raw/papers/2302.13971-LLaMA-Open-and-Efficient-Foundation-Language-Models.md, raw/papers/2307.09288-LLaMA-2-Open-Foundation-Fine-Tuned-Chat-Models.md, raw/papers/2407.21783-Llama-3-Herd-of-Models.md]
---

# LLaMA 系列

LLaMA（Large Language Model Meta AI）是 [[meta-ai]] 发布的开源基础语言模型系列。从 LLaMA 1 到 LLaMA 3，该系列推动了开源大语言模型的快速发展，成为开源社区最重要的基座模型之一。

## LLaMA 1（2023 年 2 月）

LLaMA 1 的核心理念是证明**用更少的计算量训练更小的模型**可以达到大模型的效果。[[raw/papers/2302.13971-LLaMA-Open-and-Efficient-Foundation-Language-Models.html]]

- 参数规模：7B / 13B / 33B / 65B
- 训练数据：1T-1.4T Token
- 关键改进：使用更多 Token 训练（而非增大参数量）
- RMSNorm 替代 LayerNorm、SwiGLU 激活函数、旋转位置编码（RoPE）

## LLaMA 2（2023 年 7 月）

LLaMA 2 在 LLaMA 1 基础上进行了全面升级。[[raw/papers/2307.09288-LLaMA-2-Open-Foundation-Fine-Tuned-Chat-Models.html]]

- 参数规模：7B / 13B / 70B（及对应的 Chat 版本）
- 训练数据：2T Token
- 上下文窗口：4K → 4K（Base）/ 4K（Chat）
- 引入了 RLHF 对齐的 Chat 模型
- 发布了预训练和微调的完整配方

## LLaMA 3（2024 年 7 月）

LLaMA 3 进一步扩大了规模并提升了性能。[[raw/papers/2407.21783-Llama-3-Herd-of-Models.html]]

- 参数规模：8B / 70B / 405B
- 训练数据：15T+ Token
- 上下文窗口：8K → 128K（405B 版本）
- 引入 Grouped Query Attention (GQA)
- 多语言能力大幅提升

## 技术亮点

- **Scaling 策略**：更多 Token + 更小模型 = 更高效
- **开源生态**：催生了 Vicuna、Alpaca、WizardLM 等大量衍生模型
- **对齐方案**：LLaMA 2 的 RLHF 流程成为开源对齐的标准参考

## 社区影响

LLaMA 系列对开源 AI 社区产生了深远影响。LLaMA 2 的商业友好许可使得企业可以基于 LLaMA 构建产品，直接挑战了 [[openai]] 的商业模型垄断地位。

## 相关模型

- [[deepseek]] 系列在开源路线上与 LLaMA 形成竞争
- [[qwen]] 系列在中文能力上与 LLaMA 形成互补
