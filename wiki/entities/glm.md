---
title: GLM / ChatGLM
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, open-source, llm, nlp]
sources: [raw/papers/2210.02414-GLM-130B-An-Open-Bilingual-Pre-trained-Model.html, raw/papers/2406.12793-ChatGLM-A-Family-of-Large-Language-Models-from-GLM-130B-to-G.html]
---

# GLM / ChatGLM

GLM（General Language Model）是清华大学和智谱 AI 联合开发的双语预训练语言模型系列。GLM 系列从学术研究出发，逐步发展为完整的产品生态，是中国大模型领域的重要力量。

## GLM-130B（2022 年 10 月）

GLM-130B 是系列的首个大规模模型，是当时唯一开源的、性能至少达到 GPT-3 (davinci) 水平的 100B 级别模型。[[raw/papers/2210.02414-GLM-130B-An-Open-Bilingual-Pre-trained-Model.html]]

- 参数量：1300 亿（130B）
- 双语支持：中英文
- 基于 [[transformer-architecture]] 的自回归空白填充（autoregressive blank infilling）架构
- 使用 3D 并行（数据/流水线/张量并行）训练
- 在 INT4 量化下几乎无性能损失——100B 级别模型中首个实现此特性
- 量化后可在 4×RTX 3090 (24G) 或 8×RTX 2080 Ti (11G) 上推理——100B 级别模型的最低硬件门槛
- 在多项英语基准上显著超越 GPT-3 175B (davinci)，而 OPT-175B 和 BLOOM-176B 未能达到此性能
- 在中文基准上持续大幅超越 ERNIE TITAN 3.0 260B（当时最大中文模型）
- 训练过程中面临大量 loss spike 和训练发散等工程挑战

## ChatGLM 系列

ChatGLM 将 GLM 演化为面向对话和应用的模型系列。[[raw/papers/2406.12793-ChatGLM-A-Family-of-Large-Language-Models-from-GLM-130B-to-G.html]]

### ChatGLM-6B

- 参数量：62 亿
- 单卡消费级 GPU 可运行
- 中英文双语对话能力
- 在中文社区广泛部署

### ChatGLM2 / ChatGLM3

- 性能持续提升
- 支持工具调用和代码执行
- 更长的上下文窗口（32K）
- Agent 能力增强

### GLM-4

- 参数规模大幅扩展
- 多模态能力
- 更强的推理和工具使用能力

## 架构特色

GLM 系列采用独特的**自回归空白填充**预训练目标：

- 结合了 BERT 的双向理解和 GPT 的自回归生成
- 通过 Mask 策略同时建模 Span 和 Document 级别
- 在理解和生成任务上均有竞争力
- 使用 Post-LayerNorm（与 Pre-LN 的主流方案不同）

## 训练技术

- Post-LayerNorm + 嵌入层梯度收缩（训练稳定性）
- 使用 DeepSpeed ZeRO 优化大规模训练
- INT4/INT8 量化支持（无需 post-training quantization）
- Multi-task Instruction Pre-training (MIP)
- FlashAttention 加速
- 支持 FP16 和 FP32 混合精度训练

## 产品与生态

智谱 AI 围绕 GLM 系列构建了完整的产品线：

- ChatGLM 在线对话产品
- API 平台和开发者工具
- 行业定制解决方案
- GLM-4 的多模态产品矩阵

## 社区影响

ChatGLM-6B 的开源极大推动了中文 AI 社区的发展，其低门槛部署和中文优化使其成为中国最受欢迎的开源模型之一。相比 [[qwen]] 和 [[llama]]，ChatGLM 在中文场景的适配上更加深入。GLM-130B 作为首个开源 100B 模型挑战者，为后续 [[palm]] 等大模型的开源化树立了先例。
