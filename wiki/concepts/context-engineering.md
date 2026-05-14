---
title: 上下文工程（Context Engineering）
created: 2026-05-14
updated: 2026-05-14
type: concept
tags: [agentic, reasoning, tutorial]
sources: [raw/articles/llm-agent-core-principles-2026.md]
confidence: medium
---

# 上下文工程（Context Engineering）

## 核心洞察

> 不管是思维链、Tool Use、Agent 循环、MCP 工具描述还是 Skills 文档，**最终都要塞进上下文窗口里，交给同一个概率模型去一个字一个字地往外蹦**。

LLM 所有高级能力（推理、工具调用、Agent 循环）的本质，都是在上下文中塞入不同类型的信息：

| 概念 | 在上下文中的本质 |
|------|------------------|
| 思维链 | 模型在上下文里写给自己看的草稿 |
| MCP / Tool Use | 上下文里塞工具描述，模型输出调用请求，结果追加回上下文 |
| Agent 循环 | 不断往上下文里追加思考和工具结果 |
| Skills | 把操作手册文本加载到上下文里 |

## 关键公式

**上下文里塞什么、怎么塞、塞多少 → 直接决定 Agent 表现。**

这揭示了一个重要事实：所谓「Agent 工程」，本质上是**上下文工程**——如何高效地组织和填充 LLM 的上下文窗口。

## 上下文窗口的约束

- 上下文 = 输入问题 + 对话历史 + 系统背景设定（System Prompt）
- 主流窗口大小：128K ~ 1M token
- 超出窗口的内容被压缩或丢弃（「失忆」）
- **最佳实践**：一个上下文窗口只聚焦一个问题，新问题重新开窗口

## Agent 工程的差异

以 Claude Code 为例，它比 Cursor 等 API 调用方式效果更好的关键原因：

- Claude Code 敢给模型塞更多上下文，获取充分信息后再执行
- API 调用受成本限制，倾向于塞更少上下文尽快给答案
- **同样能力的模型，上下文填充策略不同 → 效果差距巨大**

## 与相关概念的关系

- [[chain-of-thought]]：CoT 是上下文工程的典型案例——让模型在上下文中写推理草稿
- [[react-agent]]：ReAct 循环中每一步都在往上下文追加内容
- [[tool-use]]：工具描述和调用结果都占用上下文空间
- [[agent-skills]]：Skills 文档需要按需加载到上下文中（渐进式披露）

## 开放问题

- 随着上下文窗口增长（1M+ token），上下文工程的最佳实践是否需要重新定义？
- 长上下文下的「中间信息丢失」（Lost in the Middle）问题如何缓解？
- 上下文压缩 vs 精确填充的 trade-off 如何量化？
