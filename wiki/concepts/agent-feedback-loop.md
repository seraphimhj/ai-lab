---
title: Agent 反馈循环设计
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [agent, agentic, framework, architecture]
sources: [raw/articles/designing-for-agents-2025.md]
---

# Agent 反馈循环设计

> 为 AI Agent 构建可观测的反馈机制，实现产品驱动的持续迭代。来源：Teddy Riker (Ramp) 的 "Designing for Agents"。[[raw/articles/designing-for-agents-2025.md]]

## 问题背景

当产品通过 MCP/API 暴露给 AI Agent 后，传统的可观测性手段面临挑战。Ramp 的 MCP 集成暴露了一个核心问题：**能看到工具调用量，但看不到聊天上下文。**[[raw/articles/designing-for-agents-2025.md]]

这意味着你知道 Agent 调用了你的工具，但不知道：
- Agent 为什么调用它？
- 调用是否达到了预期效果？
- Agent 遇到了什么困难？

## 三大解决方案

### 1. Rationale 参数

每个 MCP/CLI 工具调用都要求 Agent 提供一个 `rationale` 参数，解释**为什么**发起这个调用。[[raw/articles/designing-for-agents-2025.md]]

**实现方式：** 在工具 schema 中添加必填的 rationale 字段：

```json
{
  "name": "create-expense-report",
  "parameters": {
    "rationale": {
      "type": "string",
      "description": "Explain why you are making this call"
    }
  }
}
```

**价值：** rationale 数据为产品团队提供了丰富的意图信号，可以直接驱动产品决策。

### 2. 反馈工具

提供一个独立的反馈工具，让 Agent 主动报告：
- 哪些操作失败了
- 尝试了什么替代方案
- 期望的结果是什么[[raw/articles/designing-for-agents-2025.md]]

**与人类反馈的对比：** Agent 给出的反馈比人类用户更具体、更一致。人类用户可能只会说"不好用"，而 Agent 会精确描述："我调用了 X 工具，期望得到 Y 结果，实际得到了 Z，这是因为 W 格式不兼容。"

### 3. Context Seeding

在工具参数中添加字段，捕获后续可能有用的上下文信息。[[raw/articles/designing-for-agents-2025.md]]

这是一种前瞻性设计 — 不仅记录"发生了什么"，还为"接下来可能需要什么"预留信息通道。

## 从反馈到产品迭代

反馈循环的终极目标是**驱动产品改进**。[[raw/articles/designing-for-agents-2025.md]]

**实际案例：** Ramp 通过分析 rationale 模式，发现大量 Agent 调用的理由是 "generating incident reports"（生成事故报告）。这个信号直接推动 Ramp 构建了专用的 incident report 工具，大幅提升了该场景的效率。

**反馈驱动迭代的流程：**

1. 收集 rationale 和反馈数据
2. 识别高频模式（如特定使用场景、反复失败的操作）
3. 针对高频模式构建专用工具或优化现有接口
4. 验证改进效果，形成闭环

## 与其他概念的关系

- [[agent-product-design]] — 反馈循环是 Agent 产品设计三大原则之一
- [[claude-code-harness]] — Claude Code 的运行桥接层同样需要可观测性来理解 Agent 的执行状态
- [[agent-context-gap]] — 反馈工具也是发现上下文缺口的重要途径

## 关键原则

> 不要只监控工具调用量。要理解 Agent 的意图、困难和期望。Agent 是比人类更精确的产品反馈来源。[[raw/articles/designing-for-agents-2025.md]]
