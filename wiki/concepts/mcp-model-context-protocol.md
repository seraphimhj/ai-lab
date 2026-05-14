---
title: MCP（Model Context Protocol）
created: 2026-05-14
updated: 2026-05-14
type: concept
tags: [framework, ecosystem, agentic]
sources: [raw/articles/llm-agent-core-principles-2026.md]
---

# MCP（Model Context Protocol）

## 定义

MCP 是 Anthropic 提出的开放标准协议，号称 AI 工具领域的「USB-C 标准」。它解决的核心问题：各家 LLM 的工具调用 API 格式不同（OpenAI 用 `parameters`，Anthropic 用 `input_schema`），同一个工具需要为不同平台反复适配。

## 核心思路

- **写一次，到处接入**：工具开发者按 MCP 标准实现一次，所有支持 MCP 的 AI 应用都能直接使用
- **底层仍是 Tool Use**：MCP 并不改变 LLM 工具调用的基本机制（模型输出 JSON → 外围程序执行），只是将工具描述和调用的接口标准化了
- **Client-Server 架构**：MCP Server 暴露工具能力，MCP Client（AI 应用）发现并调用

## 示例

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-server")

@mcp.tool()
def get_weather(city: str) -> str:
    """查询指定城市的当前天气"""
    return f"{city}：8°C，多云"

mcp.run()
```

## 在 Agent 架构中的位置

MCP 属于 Agent 工具层的标准化接口，位于 LLM 与外部工具之间：

- 上层：LLM 通过 Function Calling 表达调用意图
- 中层：MCP 提供标准化的工具描述和发现机制
- 下层：实际 API / 脚本 / 系统调用

## 与相关概念的关系

- [[tool-use]]：MCP 底层依赖 Tool Use / Function Calling 机制
- [[react-agent]]：ReAct 循环中的「工具」可通过 MCP 标准化接入
- [[claude-code]]：Claude Code 原生支持 MCP Server 接入
- [[claude-code-harness]]：Harness 扩展层通过 MCP/plugins 接入外部工具

## 影响

MCP 的意义在于生态统一——工具开发者不再需要为每个 AI 平台单独适配，降低了 Agent 生态的碎片化程度。2025-2026 年主流 AI 工具（Claude Code、Cursor、Windsurf 等）已陆续支持 MCP。
