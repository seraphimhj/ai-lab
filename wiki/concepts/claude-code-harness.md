---
title: Claude Code Harness 架构
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [agent, architecture, framework]
sources: [raw/articles/claude-code-harness-architecture-2026.md]
---

# Claude Code Harness 架构

Harness 是 [[claude-code]] 的核心编排层，设计本质是：**把多入口、多模式、多运行位置，收敛成一套统一的 agent turn 执行模型**。

## 三层架构

### 第一层：入口与分流

负责接住用户不同的使用方式：
- 命令行（CLI）
- 交互界面（TUI/REPL）
- SDK 调用
- Assistant 模式
- 远端链接

入口经 `main.tsx` 做参数解析、模式判断和路由分发。

### 第二层：Harness 会话编排（核心）

标准化处理层，将三种不同形态的请求统一为 turn 契约：
- 交互会话
- 无界面会话（headless）
- 远端接入

同时接入：
- 工具能力
- 扩展接入（MCP / plugins / skills）
- 状态与持久化

在执行前就把一次会话需要的**输入、能力和状态**组织完整。

### 第三层：Runtime 与支撑层

- **本地路径** → 进入本地 Runtime 执行完整 [[agent-loop-taor]]
- **远端路径** → 转入远端会话宿主（remote / bridge / server）

## 设计要点

- 「下限可控、上限可拓」的基础框架
- 入口无关性：无论从哪里来，都走同一套 turn 模型
- 关注恢复能力、权限模型、上下文压缩和长会话稳定性

## 相关概念

- [[agent-loop-taor]] — Harness 之下的执行循环
- [[claude-code-state-management]] — 状态管理支撑
- [[claude-code-memory-system]] — 记忆系统支撑
