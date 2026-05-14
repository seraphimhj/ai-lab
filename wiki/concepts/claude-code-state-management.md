---
title: Claude Code 状态管理
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [agent, architecture]
sources: [raw/articles/claude-code-harness-architecture-2026.md]
---

# Claude Code 状态管理

[[claude-code]] 采用「**会话运行态 + 全局会话态 + 持久化层**」分层协同管理架构。

## 三层状态

### AppState（会话运行态）

当前会话的实时状态，包括：
- REPL/TUI 任务状态
- MCP 连接
- 插件状态
- 权限状态
- 通知
- 远端连接

服务于交互体验和当前 turn 的运行过程。

### bootstrap/state（全局会话态）

当前会话的全局运行信息：
- 项目位置
- 会话标识
- 成本与预算
- 模型与功能开关
- 通道与遥测

是整个 runtime 的**公共配置底座**。

### sessionStorage（持久化层）

将会话记录和恢复信息写入磁盘：
- 对话轨迹
- 续接数据
- 历史快照

供 resume、历史读取和会话恢复使用。

## 串联机制

**ToolUseContext** 将三层状态串起来：
- 把当前会话状态暴露给 query、tools、tasks
- 把 turn 内上下文带进 [[agent-loop-taor]]

## 相关概念

- [[claude-code-harness]] — 状态管理在 Harness 编排中接入
- [[agent-loop-taor]] — Agent Loop 依赖状态管理提供上下文
