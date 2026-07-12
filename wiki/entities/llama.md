---
title: LLaMA 系列
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, open-source, llm, deeplearning]
sources: [raw/papers/2302.13971-LLaMA-Open-and-Efficient-Foundation-Language-Models.html, raw/papers/2307.09288-LLaMA-2-Open-Foundation-Fine-Tuned-Chat-Models.html, raw/papers/2407.21783-Llama-3-Herd-of-Models.pdf]
---

# LLaMA 系列

LLaMA（Large Language Model Meta AI）是 [[meta-ai]] 发布的开源基础语言模型系列。从 LLaMA 1 到 LLaMA 3，该系列推动了开源大语言模型的快速发展，成为开源社区最重要的基座模型之一。

## LLaMA 1（2023 年 2 月）

LLaMA 1 的核心理念是证明**用更少的计算量训练更小的模型**可以达到大模型的效果，呼应了 [[scaling-laws]] 中 Chinchilla 的发现。[[raw/papers/2302.13971-LLaMA-Open-and-Efficient-Foundation-Language-Models.html]]

- 参数规模：7B / 13B / 33B / 65B
- 训练数据：1T-1.4T Token（仅公开数据）
- 关键改进：使用更多 Token 训练（而非增大参数量）
- 架构改进：RMSNorm 替代 LayerNorm、SwiGLU 激活函数、旋转位置编码（RoPE）
- LLaMA 13B 在多数基准上超越 GPT-3 175B

## LLaMA 2（2023 年 7 月）

LLaMA 2 在 LLaMA 1 基础上进行了全面升级，首次提供商业友好许可。[[raw/papers/2307.09288-LLaMA-2-Open-Foundation-Fine-Tuned-Chat-Models.html]]

- 参数规模：7B / 13B / 70B（及对应的 Chat 版本）
- 训练数据：2T Token（比 LLaMA 1 增加 40%）
- 上下文窗口：4K
- 70B 版本使用 Grouped Query Attention（GQA）提升推理效率
- [[rlhf]] 对齐流程：SFT → Rejection Sampling + PPO 迭代优化
- 安全训练：Red Teaming + Safety RLHF + Context Distillation
- 详细公开了训练和对齐全流程

## LLaMA 3 / 3.1（2024 年 7 月）

LLaMA 3 代表了开源模型的最大规模尝试。[[raw/papers/2407.21783-Llama-3-Herd-of-Models.pdf]]

- 参数规模：8B / 70B / 405B
- 训练数据：15T+ Token（多语言，高质量数据策整）
- 上下文窗口：8K → 128K（通过渐进式 [[long-context-extension]]）
- 全面使用 Grouped Query Attention (GQA)
- 词汇表扩大到 128K（tiktoken tokenizer）
- 多模态能力：支持图像、视频、语音输入
- 工具使用：内置 Code Interpreter、Search、数学工具
- 405B 版本在多项基准上接近 [[gpt-4]] 水平

## 技术亮点

- **Scaling 策略**：LLaMA 1 证明 token-optimal training 的价值；LLaMA 3 则回归大力出奇迹路线
- **开源生态**：催生了 Vicuna、Alpaca、WizardLM、CodeLlama 等大量衍生模型
- **对齐方案**：LLaMA 2 的 RLHF 流程成为开源对齐的标准参考
- **架构演进**：从标准 MHA(1)→GQA(2/3)，保持架构简洁

## 社区影响

LLaMA 系列对开源 AI 社区产生了深远影响。LLaMA 2 的商业友好许可使得企业可以基于 LLaMA 构建产品，直接挑战了 [[openai]] 的商业模型垄断地位。LLaMA 3 405B 证明开源模型可以达到闭源模型水平。

## 相关模型

- [[deepseek]] 系列在开源路线上与 LLaMA 形成竞争，架构创新更激进
- [[qwen]] 系列在中文能力上与 LLaMA 形成互补
- [[mistral-7b]] / [[mixtral]] 走高效路线与 LLaMA 小模型竞争
