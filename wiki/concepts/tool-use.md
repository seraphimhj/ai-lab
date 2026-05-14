---
title: 工具使用
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [agent, tool-use, capabilities]
sources: [raw/papers/2302.04761-Toolformer-Language-Models-Can-Teach-Themselves-to-Use-Tools.md]
---

# 工具使用

让大语言模型学会调用外部工具（搜索、计算器、代码执行、API 等）来扩展其能力边界。[[raw/papers/2302.04761-Toolformer-Language-Models-Can-Teach-Themselves-to-Use-Tools.html]]

## 为什么需要工具

语言模型的能力受限于训练数据：
- **时效性**：训练截止日期后的事件无法获知
- **精确性**：数学计算容易出错
- **私有数据**：无法访问企业内部数据
- **交互性**：无法操作外部系统

工具使用突破了这些限制。

## Toolformer 的方法[[raw/papers/2302.04761-Toolformer-Language-Models-Can-Teach-Themselves-to-Tools.html]]

### 自监督学习工具调用

1. **候选 API 插入**：在训练数据中自动插入 API 调用
2. **执行与过滤**：执行 API 调用，保留能提高预测质量的调用
3. **微调**：用过滤后的数据微调模型

### 支持的工具类型

| 工具 | API 格式 | 用途 |
|------|---------|------|
| 搜索引擎 | Search(query) | 获取实时信息 |
| 计算器 | Calculator(expr) | 精确数学计算 |
| 日历 | Calendar(day) | 日期计算 |
| 机器翻译 | Translate(text, lang) | 多语言翻译 |
| QA 系统 | QA(question) | 知识库查询 |

## 工具使用框架

### Function Calling

现代 LLM API 的标准方式：
```json
{
  "name": "get_weather",
  "description": "获取指定城市的天气",
  "parameters": {
    "city": {"type": "string"},
    "date": {"type": "string"}
  }
}
```

模型输出结构化的函数调用，系统执行后返回结果。

### [[react-agent]] 范式

在 ReAct 框架中，工具使用是 Action 的一种：
- Thought → Action (tool call) → Observation → ...

## 挑战

- **幻觉调用**：编造不存在的 API
- **参数错误**：参数格式或值不正确
- **过度依赖**：简单问题也调用工具
- **多工具编排**：多个工具的组合使用复杂

## 相关概念

- [[react-agent]] — 推理+行动框架
- [[retrieval-augmented-generation]] — 检索作为最重要的工具
- [[tree-of-thoughts]] — 工具使用可以融入思维树搜索
