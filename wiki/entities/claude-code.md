---
title: Claude Code
created: 2026-05-05
updated: 2026-05-05
type: entity
tags: [company, open-source, agent, llm]
sources: [raw/articles/claude-code-harness-architecture-2026.md]
---

# Claude Code

Anthropic 推出的 AI Coding Agent，基于终端运行，不仅是编码工具，更是一个**通用的终端 Agent**：能循环思考、调度工具、治理权限、恢复上下文、稳定长会话。

## 核心能力

- 循环思考与工具调度
- 权限治理
- 上下文恢复
- 长会话稳定性
- 远端协作与会话资产管理

## 架构模块

- [[claude-code-harness]] — 入口适配 + 会话编排 + 运行桥接
- [[agent-loop-taor]] — Think-Act-Observe-Repeat 执行循环
- [[claude-code-state-management]] — 分层状态管理（会话态 / 全局态 / 持久化）
- [[claude-code-memory-system]] — 策略约束 + 指令注入 + 分层记忆召回
- 工具系统 — 能力定义 → 装配 → 执行三层供给链（内建工具 + MCP + plugins）

## 演进方向

从源码中可见，Claude Code 正在向**Agent 工作平台**演进，涵盖主动协作、长时记忆、远端运行与会话资产管理能力。Anthropic 内部也在探索将 Coding Agent 外溢到更多行业场景。

## 设计哲学

「将智能下沉给模型，释放智能自主权」—— 架构编排足够简单，让模型主导意图生成，工具负责与外部世界交互。

## 与 OpenClaw 对比

- 详见 [[openclaw-vs-claude-code]] 对比页
- Claude Code 架构设计成熟，但闭源、黑盒，无法改造
- OpenClaw 开源、可改造，社区迭代快，但稳定性略逊
- 两者互相吸纳设计，未来趋于融合

## 关键文件

- `main.tsx` — 入口路由分发
- CLAUDE.md — 项目级指令配置
- `bootstrap/state` — 全局会话态管理
