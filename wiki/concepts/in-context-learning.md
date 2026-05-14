---
title: In-Context Learning — 上下文学习
created: 2026-05-10
updated: 2026-05-14
type: concept
tags: [reasoning, prompting, inference]
sources: [raw/papers/2005.14165-Language-Models-are-Few-Shot-Learners.html]
---

# In-Context Learning — 上下文学习

大语言模型无需更新参数，仅通过在输入 prompt 中提供示例或指令，就能学习并执行新任务的能力。[[raw/papers/2005.14165-Language-Models-are-Few-Shot-Learners.html]]

## GPT-3 的发现

GPT-3（175B 参数，Brown et al., 2020）首次系统性地展示了大模型的 in-context learning 能力[[raw/papers/2005.14165-Language-Models-are-Few-Shot-Learners.html]]：
- **Zero-shot**：只给任务描述，不给示例
- **One-shot**：给一个示例
- **Few-shot**：给多个示例

模型规模越大，ICL 能力越强——这是一种涌现能力。GPT-3 使用 dual-encoder 架构，在多种 NLP 任务上验证了无需微调即可通过提示达到有竞争力的性能。

## 形式分类

| 形式 | 描述 | 示例 |
|------|------|------|
| Zero-shot | 只描述任务 | "将以下文本翻译成英文：" |
| Few-shot | 给几个输入-输出示例 | 模板 + 3-10 个示例 |
| Instruction | 自然语言指令 | "请总结以下文章的要点" |
| Chain-of-Thought | 带推理过程的示例 | 逐步展示解题过程 |

## 为什么有效

ICL 的机制仍在研究中，主流假说包括：

1. **隐式梯度下降**：Transformer 的 attention 机制隐式地执行了梯度下降
2. **任务识别**：模型通过示例识别任务类型，然后应用预训练中学到的知识
3. **模式匹配**：模型匹配 prompt 中的模式并延续

## 实践技巧

- 示例顺序有影响（recency bias：最后出现的示例影响最大）
- 示例多样性比数量更重要
- 格式一致性很关键
- 混合正例和反例可以提升效果

## 与其他方法的对比

| 方法 | 参数更新 | 成本 | 适应能力 |
|------|---------|------|---------|
| ICL | 不更新 | 低（推理时） | 中 |
| [[instruction-tuning]] | 更新 | 高 | 高 |
| [[lora]] 微调 | 部分更新 | 中 | 高 |

## 相关概念

- [[chain-of-thought]] — ICL 中最成功的推理增强方法
- [[instruction-tuning]] — 将 ICL 能力固化到模型参数中
- [[scaling-laws]] — ICL 能力随模型规模增长的规律
- [[dense-passage-retrieval]] — ICL 的 few-shot 范式启发了检索增强方法
- [[react-agent]] — 在 ICL 框架下通过 few-shot 实现工具使用
- [[dense-passage-retrieval]] — ICL 的 few-shot 范式启发了检索增强方法
- [[react-agent]] — 在 ICL 框架下通过 few-shot 实现工具使用
