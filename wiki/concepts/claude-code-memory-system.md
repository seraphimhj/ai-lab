---
title: Claude Code 记忆系统
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [agent, rag, memory, architecture]
sources: [raw/articles/claude-code-harness-architecture-2026.md]
---

# Claude Code 记忆系统

[[claude-code]] 的记忆管理采用「**策略约束 + 指令注入 + 分层记忆召回**」的组合式上下文系统。

## 三层机制

### 策略层

企业或组织下发的开关与限制，约束系统能做什么。

### 指令层

包括：
- `CLAUDE.md` — 项目级规则
- 用户级规则文件
- 告诉模型**如何工作**

### 记忆层

按作用域分层：
- **当前会话沉淀** — 会话内的临时记忆
- **项目与团队范围记忆** — 跨会话共享
- **Agent 专属记忆** — 面向特定 Agent
- **动态记忆（nested memory）** — 按路径触发补充，非检索

## 记忆加载链路

```
记忆文件 → 相关性筛选 → 附件注入 → 进入下一轮 turn
```

## 记忆筛选机制（关键设计）

与典型的 RAG 语义检索路线不同，Claude Code 采用 **LLM 驱动的文件级记忆选择**：

- **候选集** — 来自磁盘记忆文件
- **选择依据** — 文件名、描述、query 语义匹配
- **选择器** — 模型（不是 embedding similarity）
- **结果粒度** — 挑文件，不是查向量库 top-k chunk

## 设计总结

「按作用域分层、按时机写入、按相关性召回、按预算约束展示」

让用户感知到系统**越来越懂上下文**，而非"强行回忆"。

## 与传统 RAG 的差异

| 维度 | Claude Code | 传统 RAG |
|------|------------|----------|
| 检索方式 | LLM 驱动选择 | Embedding similarity |
| 粒度 | 文件级 | Chunk 级 |
| 向量库 | 不使用 | 依赖向量数据库 |
| 动态记忆 | 路径触发 | 通常无此机制 |

## 相关概念

- [[claude-code-harness]] — 记忆系统在 Harness 编排中接入
- [[agent-loop-taor]] — 记忆为每个 turn 提供上下文
