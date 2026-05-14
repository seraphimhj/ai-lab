---
title: GPT-4
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, architecture, llm, multimodal]
sources: [raw/papers/2303.08774-GPT-4-Technical-Report.html]
---

# GPT-4

GPT-4 是 [[openai]] 于 2023 年发布的大规模多模态模型，能够同时接受图像和文本输入并生成文本输出。GPT-4 在多项专业和学术基准上达到人类水平表现，包括在模拟律师资格考试中排名前 10%。[[raw/papers/2303.08774-GPT-4-Technical-Report.html]]

## 核心特性

### 多模态能力

GPT-4 是首个原生支持图像输入的 GPT 系列模型，能够理解图像内容并与文本交互。这使得模型可以处理包含图表、截图、照片等视觉信息的问题。

### 预训练与对齐

- 基于 [[transformer-architecture]] 架构进行预训练
- 后训练对齐过程显著提升了事实性和行为一致性
- 建立了跨规模的性能可预测性基础设施

### 性能可预测性

GPT-4 的一个重要技术成果是：可以在仅使用 GPT-4 千分之一到万分之一计算量的模型上准确预测 GPT-4 的最终 loss。论文使用幂律拟合公式 L(C) = aC^b + c 进行预测，结果与实际训练高度吻合。在 HumanEval 代码生成任务上也成功预测了性能。

## 基准表现

| 基准 | GPT-4 表现 | GPT-3.5 对比 |
|------|-----------|-------------|
| 律师资格考试 (Bar Exam) | 前 10%（~298 分） | 后 10% |
| SAT 数学 | 700/800（93%） | — |
| GRE Quantitative | 163/170（80%） | — |
| AP Biology | 5/5（满分） | — |
| MMLU（57 学科） | 86.4%（英文 SOTA） | — |
| MMLU 多语言 | 超越 24/26 语言的英文 SOTA | — |
| Codeforces 评级 | ~ Elo 392 | — |

## 对齐与安全

GPT-4 使用 RLHF（Reinforcement Learning from Human Feedback）进行后训练对齐，通过 Red Team 测试和 model-assisted safety pipeline 减少有害输出。报告特别详述了在 bias、disinformation、over-reliance、privacy、cybersecurity 等方面的风险分析和缓解策略。

## 影响

GPT-4 的发布标志着大语言模型进入多模态时代，直接推动了 [[claude-code]] 等 AI Agent 产品的发展。其预测性 scaling 方法论为后续 [[palm]] 等大模型的训练规划提供了范式参考。GPT-4 相较 [[gpt-3]] 的巨大跃升也验证了规模化的持续回报。

## 局限性

- 仍存在事实性错误（幻觉问题）
- 未公开具体模型参数和架构细节
- 多模态能力限于图像输入
- 推理成本高昂
