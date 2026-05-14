---
title: Chain-of-Thought — 思维链提示
created: 2026-05-10
updated: 2026-05-14
type: concept
tags: [reasoning, prompting, inference]
sources: [raw/papers/2201.11903-Chain-of-Thought-Prompting-Elicits-Reasoning-in-Large-Langua.html, raw/articles/llm-agent-core-principles-2026.html]
---

# Chain-of-Thought — 思维链提示

通过在提示中展示逐步推理过程，引导大语言模型进行中间推理步骤，从而解决复杂问题。[[raw/papers/2201.11903-Chain-of-Thought-Prompting-Elicits-Reasoning-in-Large-Langua.html]]

## 核心思想

直接让模型输出答案 vs. 让模型先"思考"再输出答案：
- **标准提示**：Q → A（可能对复杂问题出错）
- **CoT 提示**：Q → 推理步骤 1 → 推理步骤 2 → ... → A（准确率显著提升）

## 两种形式

### Few-Shot CoT

在 prompt 中给出包含推理过程的示例：
```
Q: 罗杰有 5 个网球。他又买了 2 罐，每罐 3 个球。他现在有多少个球？
A: 罗杰开始有 5 个球。2 罐 × 3 个 = 6 个球。5 + 6 = 11。答案是 11。

Q: [新问题]
A:
```

### Zero-Shot CoT

只需在问题后加上 "Let's think step by step"：
```
Q: [问题]
A: Let's think step by step.
```

## 为什么有效

- 将复杂问题分解为多个简单子问题
- 每一步推理利用模型的中间计算能力
- 提供更多的计算步骤（compute in the forward pass）
- 类似于人类解题时的"草稿纸"过程

## 适用场景

- 数学推理
- 逻辑推理
- 多步规划
- 需要复合计算的任务

## 推理模型的演进

推理模型（o1/o3、DeepSeek R1、Claude extended thinking）在 CoT 基础上加入**自我反思**：先给答案 → 回头检查 → 修正。

### 2025 年新范式：单一模型 + 思考强度参数

旧模式中对话模型（gpt-4o）与推理模型（gpt-o1）是分离的，中途不能切换。新模式使用同一模型 + reasoning_effort / effort / thinkingLevel 参数：

- 强度调高 → 多花时间推演（类似深度推理模式）
- 强度调低 → 直接给答案省 token（类似快速对话模式）
- 好处：一套代码覆盖所有场景，复杂度大幅降低

## 论文关键数据

Wei et al. (2022) 在三个大模型（LaMDA 137B、PaLM 540B、GPT-3 175B）上测试：
- **GSM8K 数学题**：PaLM 540B + 8 个 CoT exemplars 达到 57% 准确率，超过 fine-tuned GPT-3 with verifier（55%）和 standard prompting（18%）
- **涌现效应**：CoT 仅在足够大的模型中有效（~100B+ 参数），小模型几乎无增益
- 覆盖算术、常识和符号推理三大类任务

## 论文关键数据

Wei et al. (2022) 在三个大模型（LaMDA 137B、PaLM 540B、GPT-3 175B）上测试：
- **GSM8K 数学题**：PaLM 540B + 8 个 CoT exemplars 达到 57% 准确率，超过 fine-tuned GPT-3 with verifier（55%）和 standard prompting（18%）
- **涌现效应**：CoT 仅在足够大的模型中有效（~100B+ 参数），小模型几乎无增益
- 覆盖算术、常识和符号推理三大类任务

## 局限性

- 对小模型效果有限（通常需要 >100B 参数）
- 推理链越长，错误累积风险越高
- 不是所有任务都受益于 CoT（简单任务反而可能变差）

## 相关概念

- [[tree-of-thoughts]] — CoT 的树状扩展，支持回溯
- [[in-context-learning]] — CoT 是 ICL 的一种特殊形式
- [[scaling-laws]] — 推理能力与模型规模的关系
- [[react-agent]] — 将推理与行动结合的 Agent 范式
- [[context-engineering]] — CoT 的本质是在上下文中写推理草稿
