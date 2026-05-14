---
title: Agent 产品设计
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [agent, agentic, framework, platform, architecture]
sources: [raw/articles/designing-for-agents-2025.md]
---

# Agent 产品设计

> 为 AI Agent 设计产品和 API 的核心原则与实践框架。来源：Teddy Riker (Ramp) 的 "Designing for Agents"。[[raw/articles/designing-for-agents-2025.md]]

## 核心趋势：80/20 法则的翻转

UI 并没有消亡，但人机交互的主导方式正在发生根本变化：80% 的交互将通过 AI Agent 完成，而非直接通过图形界面。[[raw/articles/designing-for-agents-2025.md]]

**Ramp 的实证数据：** MCP 周活跃用户在 3 个月内增长 10 倍，验证了 Agent-driven 交互的爆发式增长。[[raw/articles/designing-for-agents-2025.md]]

## 三代交互模型演进

交互模式经历了三个阶段的演进：

| 代际 | 模式 | 说明 |
|------|------|------|
| 第一代 | User → UI → Database | 传统 GUI 交互，用户直接操作界面 |
| 第二代 | User → Agent → Database | 当前浪潮，用户的 AI Agent 直接调用 API |
| 第三代 | User → Agent → Agent → Database | 新兴模式，两个 Agent 协作完成任务 |

第三代模型意味着产品方也需要构建自己的 AI Agent，与用户的 Agent 进行协商和协作。这要求产品设计从"为人设计界面"转向"为 Agent 设计接口"。

**Salesforce Headless 360** 是这一趋势的典型案例：将整个平台暴露为 API/MCP/CLI，完全不需要浏览器。[[raw/articles/designing-for-agents-2025.md]]

## 三大设计原则

Teddy Riker 提出了 Agent 产品设计的三大核心原则：

1. **教会智能体如何成功** — 提供 Agent 所需的规范，让它们在正确的时机获得正确的信息。详见 [[agent-feedback-loop]] 和 [[agent-context-gap]]
2. **建立反馈循环** — 通过 rationale 参数、反馈工具、context seeding 实现可观测性和持续改进。详见 [[agent-feedback-loop]]
3. **留意上下文缺口** — 不同 Agent 掌握不同上下文，设计接口时应索要上下文而非索要答案。详见 [[agent-context-gap]]

## 与传统 API 设计的区别

| 维度 | 传统 API 设计 | Agent 产品设计 |
|------|-------------|---------------|
| 规范传递 | 开发者阅读文档后编写适配器 | 运行时动态交付给 Agent |
| 错误处理 | 返回错误码，开发者调试 | 提供反馈工具，Agent 自行报告 |
| 接口设计 | 暴露完整数据，由调用方决定 | 索要上下文，由 Agent 间协商 |
| 反馈来源 | 人类用户反馈（模糊、不一致） | Agent 反馈（具体、一致、结构化） |

## 与其他架构的关系

- [[claude-code-harness]] — Claude Code 的 Harness 架构展示了类似的"为 Agent 设计入口"思想，通过三层架构统一多入口
- [[agent-paradigm-shift]] — Chat→Agent 范式转移是 Agent 产品设计兴起的大背景
- [[agent-loop-taor]] — Think-Act-Observe-Repeat 执行循环模式是 Agent 产品接口设计的参考框架

## 关键洞察

> "过去，界面夹在用户和他的费用系统之间。现在，界面夹在他的智能体和你的智能体之间。"[[raw/articles/designing-for-agents-2025.md]]

这意味着产品设计者需要重新思考"用户"是谁 — 未来的主要"用户"可能不是人类，而是另一个 AI Agent。
