---
title: ReAct — 推理与行动结合
created: 2026-05-10
updated: 2026-05-14
type: concept
tags: [agent, reasoning, tool-use]
sources: [raw/papers/2210.03629-ReAct-Synergizing-Reasoning-and-Acting-in-Language-Models.md, raw/articles/llm-agent-core-principles-2026.md]
---

# ReAct — 推理与行动结合

将语言模型的推理（Reasoning）与外部行动（Acting）交替进行，通过思考和行动的循环来解决需要外部信息的复杂任务。[[raw/papers/2210.03629-ReAct-Synergizing-Reasoning-and-Acting-in-Language-Models.html]]

## 核心思想

### 纯推理的局限

- [[chain-of-thought]] 只有推理，无法获取外部信息
- 模型的内部知识有限，无法处理实时或私有数据
- 无法与外部世界交互

### ReAct 循环

```
Thought（思考）→ Action（行动）→ Observation（观察）→ Thought → ...
```

模型先思考下一步该做什么，然后执行行动（如搜索、计算），观察结果，再继续推理。

## 格式示例

```
Question: 2023 年诺贝尔物理学奖得主是谁？他所在机构的排名是什么？

Thought 1: 我需要查找 2023 年诺贝尔物理学奖得主。
Action 1: Search[2023 Nobel Prize Physics winner]
Observation 1: Pierre Agostini, Ferenc Krausz, Anne L'Huillier

Thought 2: Pierre Agostini 在哪个机构？
Action 2: Search[Pierre Agostini affiliation]
Observation 2: Ohio State University

Thought 3: 我需要查找 Ohio State University 的排名。
Action 3: Search[Ohio State University ranking 2023]
Observation 3: #49 in US News

Thought 4: 现在可以回答了。
Answer: 2023 年诺贝尔物理学奖得主包括 Pierre Agostini，他所在的 Ohio State University 在 2023 年 US News 排名第 49。
```

## 优势

| 对比 | CoT（纯推理） | ReAct |
|------|-------------|-------|
| 外部信息 | 无法获取 | 通过 Action 获取 |
| 可解释性 | 中等 | 高（Thought 是显式的） |
| 错误恢复 | 无法自我纠正 | 可以根据 Observation 调整 |
| 任务范围 | 知识内任务 | 知识外 + 工具任务 |

## 简化理解：Agent = LLM + 工具 + 循环

Agent 的核心思路可以用极简伪代码表达：

```python
while 任务未完成:
    模型根据当前上下文思考下一步该做什么
    if 模型认为需要使用某个工具:
        执行工具，把结果追加到上下文
    elif 模型认为任务完成了:
        输出最终结果，退出循环
```

- LLM 是大脑，工具是手脚，循环是驱动力
- 循环副作用：上下文不断增长 → 上下文窗口大小至关重要
- Agent 工程的核心是上下文工程：如何高效组织和填充上下文窗口

## 局限性

- 行动空间需要预先定义
- 多步推理时错误可能累积
- 行动次数受限（API 调用成本）
- 循环中上下文不断增长，受窗口大小约束

## 相关概念

- [[chain-of-thought]] — ReAct 中 Thought 部分的基础
- [[tool-use]] — ReAct 中 Action 的具体实现
- [[retrieval-augmented-generation]] — 一种常见的 Action 类型
- [[agent-paradigm-shift]] — ReAct 是 Agent 范式的重要里程碑
- [[context-engineering]] — Agent 循环本质是不断往上下文追加内容
- [[mcp-model-context-protocol]] — Agent 工具层的标准化接口
- [[agent-skills]] — Agent 的可复用操作文档
