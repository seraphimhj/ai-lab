---
title: SWE-agent — 软件工程 Agent
created: 2026-05-15
updated: 2026-05-15
type: concept
tags: [agentic, tool, llm, benchmark]
sources: [raw/papers/2405.15793-SWE-agent-Agent-Computer-Interfaces-Enable-Automated-Softwar.pdf]
confidence: high
---

# SWE-agent — 软件工程 Agent

SWE-agent 是 Princeton 团队提出的软件工程 Agent 系统，核心创新在于 **Agent-Computer Interface (ACI)** 概念——为 LM Agent 专门设计的计算机交互界面，类比人类工程师使用 IDE 而非裸终端。[[raw/papers/2405.15793-SWE-agent-Agent-Computer-Interfaces-Enable-Automated-Softwar.pdf]]

## 核心思想

人类程序员受益于 IDE（VSCode、PyCharm 等）的高效界面，但 LM Agent 通常只能通过原始 Linux Shell 与计算机交互。SWE-agent 提出：**LM Agent 是一类新的终端用户，需要专门为其设计的交互界面（ACI）**。

## Agent-Computer Interface (ACI)

ACI 提供一组 LM 友好的命令，替代复杂的 Shell 操作：

| ACI 命令 | 功能 | 对比 Shell |
|----------|------|-----------|
| File Viewer | 浏览文件（带行号、滚动） | cat / less |
| File Editor | 编辑文件（带验证反馈） | sed / vim |
| Code Search | 搜索代码符号 | grep / find |
| Navigate Repo | 目录导航 | cd / ls |

### 关键设计原则

1. **简化动作空间**：少量简单命令代替 Shell 的无限命令空间
2. **防护栏**：防止常见错误（如无效编辑）
3. **结构化反馈**：每次操作后给出简洁、具体的环境反馈
4. **错误恢复**：编辑失败时自动回滚并给出提示

## 性能表现

| 基准 | SWE-agent (GPT-4 Turbo) | 此前 SOTA | 提升 |
|------|------------------------|-----------|------|
| SWE-bench (2,294 issues) | 12.47% pass@1 | 3.8% (RAG) | 3.3× |
| HumanEvalFix | 87.7% | - | SOTA |
| SWE-bench Lite (300) | +10.7pp vs Shell baseline | - | - |

- Claude 3 Opus 作为底座 LM 可解决 10.5% 的 SWE-bench 任务
- ACI 设计对性能影响显著：比纯 Shell 交互多解决 10.7 个百分点

## 与 [[claude-code]] 的关系

SWE-agent 和 [[claude-code]] 代表了编程 Agent 的两种路线：
- **SWE-agent**：学术研究导向，强调 ACI 设计对 Agent 性能的影响
- **Claude Code**：产品导向，[[claude-code-harness]] 三层架构 + [[agent-loop-taor]] 执行循环

两者共同验证了：**接口设计（不修改模型权重）可以大幅提升 Agent 能力**。

## 贡献

1. 提出 ACI 概念——Agent 专用界面设计
2. 证明专用界面 > 通用 Shell（无需修改 LM 权重）
3. 开源系统 + SWE-bench 评测标准推动了 Coding Agent 领域发展

## 相关概念

- [[react-agent]] — SWE-agent 采用类似的 Think-Act-Observe 循环
- [[tool-use]] — ACI 本质是为 Agent 设计的 Tool 集合
- [[code-generation]] — SWE-agent 的核心能力基础
- [[claude-code]] — 产品级编程 Agent 的代表
