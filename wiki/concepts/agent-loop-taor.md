---
title: Agent Loop (TAOR)
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [agent, architecture, reasoning, inference]
sources: [raw/articles/claude-code-harness-architecture-2026.md]
---

# Agent Loop (TAOR)

[[claude-code]] 的核心执行循环，采用 **TAOR 模式**：Think-Act-Observe-Repeat。

## 设计哲学

「将智能下沉给模型，释放智能自主权」—— 架构编排尽可能简单，让模型主导意图生成和决策。

## 执行步骤

单次 turn 的稳定步骤：

1. **预处理上下文** — 装配本轮所需的上下文信息
2. **流式采样 thinking** — 模型生成思考和意图
3. **执行工具** — 按模型意图调用外部工具
4. **拼接 toolResult** — 将工具执行结果补回上下文
5. **判断是否回流** — 决定是否进入下一轮循环

## 核心特征

- 不是简单的问答回合，而是**可持续推进任务的执行循环**
- 模型负责生成意图，工具负责与外部世界交互
- 系统将结果补回上下文，决定是否继续
- 支撑 [[claude-code]] 的复杂长任务能力

## 与其他 Agent Loop 模式对比

- **ReAct** (Reason-Act) — 更早的 Agent 循环范式
- **Plan-Execute** — 先规划再执行的分步模式
- **TAOR** — Claude Code 的实现，强调 Observe 环节和持续 Repeat

## 相关概念

- [[claude-code-harness]] — 上层编排，决定 Agent Loop 如何被调用
- [[claude-code-memory-system]] — 为 Loop 提供记忆上下文
