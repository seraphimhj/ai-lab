---
title: Tree of Thoughts — 树状思维
created: 2026-05-10
updated: 2026-05-14
type: concept
tags: [reasoning, prompting, inference]
sources: [raw/papers/2305.10601-Tree-of-Thoughts-Deliberate-Problem-Solving-with-Large-Langu.html]
---

# Tree of Thoughts — 树状思维

将 [[chain-of-thought]] 从线性推理链扩展为树状搜索结构，允许模型探索多条推理路径并回溯，提升复杂问题求解能力。[[raw/papers/2305.10601-Tree-of-Thoughts-Deliberate-Problem-Solving-with-Large-Langu.html]]

## 核心思想

### 从链到树

| 方法 | 结构 | 探索能力 |
|------|------|---------|
| 标准 I/O | 单步 | 无探索 |
| Chain-of-Thought | 线性链 | 单路径 |
| Tree of Thoughts | 树 | 多路径 + 回溯 |

### 关键类比

将 LLM 推理类比为搜索问题：
- **状态**：中间推理步骤
- **动作**：生成下一个推理步骤
- **目标**：找到正确的解决方案

## 算法框架

### ToT 的四个组件

1. **Thought Decomposition**：将问题分解为中间步骤
2. **Thought Generation**：为每个状态生成多个候选后续步骤（k 个）
3. **State Evaluation**：评估每个候选步骤的质量/可能性
4. **Search Algorithm**：选择搜索策略

### 搜索策略

| 策略 | 方法 | 适用场景 |
|------|------|---------|
| BFS | 广度优先，评估每层所有节点 | 每层步骤少 |
| DFS | 深度优先，回溯错误路径 | 解空间深 |
| Beam Search | 保留 top-b 个候选 | 平衡宽度和深度 |

## 设计哲学

ToT 的设计灵感来自认知科学的"双过程理论"：
- **System 1**：快速、自动——对应 LLM 的标准自回归生成
- **System 2**：缓慢、深思——对应 ToT 的搜索与评估

以及 Newell & Simon (1950s) 将问题求解视为"组合问题空间中的搜索"。ToT 用 LLM 本身作为启发式评估函数（而非程序化或学习到的启发式），是前所未有的做法。

## 实际效果

在三个任务上展示了显著提升：
- **24点游戏**：从 4% → 74%
- **创意写作**：评分显著优于 CoT
- **Mini Crosswords**：从 18.9% → 43.3%

## 局限性

- 每个节点需要多次 LLM 调用，成本高
- 需要精心设计评估函数
- 推理延迟大幅增加
- 不适用于简单任务

## 相关概念

- [[chain-of-thought]] — ToT 的基础
- [[in-context-learning]] — 思维链和树状思维都属于 ICL 范畴
- [[react-agent]] — 另一种结构化推理方法
