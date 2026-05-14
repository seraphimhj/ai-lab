---
title: Test-Time Compute Scaling
created: 2026-05-14
updated: 2026-05-14
type: concept
tags: [optimization, inference, reasoning, llm]
sources: [raw/papers/2408.03314-Scaling-LLM-Test-Time-Compute-Optimally-can-be-More-Effectiv.html]
confidence: high
---

# Test-Time Compute Scaling

Test-Time Compute（推理时计算缩放）是一种通过在推理阶段投入更多计算量来提升模型输出质量的策略，代表了从"更大模型"到"更聪明推理"的范式转移。

## 核心思想

传统 [[scaling-laws]] 关注预训练阶段的计算资源分配（模型参数 × 数据量），而 Test-Time Compute 则探索另一个维度：固定模型大小，在推理时投入额外计算来改善输出。核心问题是：**在推理计算预算固定的情况下，如何最优分配以最大化性能？** [[raw/papers/2408.03314-Scaling-LLM-Test-Time-Compute-Optimally-can-be-More-Effectiv.html]]

## 两种缩放机制

### 1. Verifier 搜索（输出层修改）

使用 Process Reward Model（PRM）对推理过程每一步进行验证：
- **Best-of-N 采样**：最简单形式，生成 N 个候选答案，用 verifier 选最优
- **Tree Search**：使用 PRM 在解题步骤空间做树搜索，比 Best-of-N 高效
- **Beam Search / Lookahead**：更精细的搜索算法

### 2. Proposal Distribution 修改（输入层修改）

迭代地修改模型的提案分布：
- **Sequential Revision**：让模型自我批评并修正答案
- **STaR / ReST^EM**：通过 RL 微调改善提案质量

## Compute-Optimal 策略

关键发现：**不同难度的问题适合不同的推理策略**。

| 问题难度 | 最优策略 | 原因 |
|---------|---------|------|
| 简单/中等 | Sequential Revision | 初始答案方向正确，只需细化 |
| 困难 | Parallel Sampling + PRM Search | 需要探索不同解题思路 |
| 极难 | 增加预训练规模 | 推理时计算收益有限 |

采用"自适应计算最优"策略（根据问题难度动态选择），可以在仅用 **1/4 计算量** 的情况下超越 Best-of-N 基线。

## 与预训练计算的对比

在 FLOPs-matched 评估中：
- 小模型 + 额外推理计算 **可以超越 14× 大模型**（在模型已有一定成功率的问题上）
- 当推理 token 量 << 预训练 token 量时，推理计算扩展更划算
- 极难问题仍需更大预训练模型，推理计算无法完全替代

## 与其他概念的关系

- [[chain-of-thought]] 和 [[tree-of-thoughts]] 是 Test-Time Compute 的具体实例
- DeepSeek-R1 的 [[rlhf]] 训练出的长推理链即为隐式 Test-Time Compute
- 与 [[scaling-laws]] 互补：预训练缩放 vs 推理缩放是两个正交维度

## 影响

这一研究暗示未来方向：**更少 FLOPs 花在预训练，更多 FLOPs 花在推理**。这正是 OpenAI o1、DeepSeek-R1 等推理模型的理论基础——通过 longer thinking 获得 better answers。
