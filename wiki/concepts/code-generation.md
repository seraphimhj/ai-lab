---
title: Code Generation
created: 2026-05-14
updated: 2026-05-14
type: concept
tags: [model, llm, training, benchmark]
sources: [raw/papers/2305.06161-StarCoder-may-the-source-be-with-you.html]
confidence: high
---

# Code Generation

代码生成是 LLM 的核心应用场景之一，专门的代码模型通过在高质量代码语料上训练，实现代码补全、生成、翻译和修复。

## 代表模型

### StarCoder（BigCode, 2023）

由 BigCode 开源社区训练的 15.5B 参数代码模型：[[raw/papers/2305.06161-StarCoder-may-the-source-be-with-you.html]]

- **训练数据**：The Stack v1.2（1T tokens，80+ 编程语言 + GitHub Issues + Git Commits）
- **上下文长度**：8K tokens（Multi-Query Attention + Fill-in-the-Middle）
- **架构**：标准 [[transformer-architecture]] Decoder-only + MQA
- **许可**：OpenRAIL-M，允许商用
- **表现**：在 HumanEval 上达 40.8%（超越原始 Codex），Python 表现尤为突出

### 其他代码模型

| 模型 | 参数量 | 开源 | 特点 |
|-----|--------|------|------|
| Codex (OpenAI) | 12B | ❌ | GPT-3 微调，GitHub Copilot 底座 |
| StarCoder 2 | 3/7/15B | ✅ | The Stack v2，更多语言 |
| CodeLlama | 7/13/34B | ✅ | [[llama]] 2 续训，支持 Infilling |
| DeepSeek-Coder | 1.3/6.7/33B | ✅ | 2T token 代码语料，FIM 支持 |
| Qwen-Coder | 1.5/7/14B | ✅ | [[qwen]] 系列代码特化 |

## 关键技术

### Fill-in-the-Middle (FIM)

训练时随机将代码片段拆为 prefix-middle-suffix，要求模型在给定前后文的情况下生成中间部分。对 IDE 代码补全场景至关重要。

### Repository-Level Context

将整个仓库结构作为上下文输入，使模型理解跨文件依赖。StarCoder 在训练中特别加入了 Git Commits 数据以学习代码修改模式。

### Multi-Query Attention

StarCoder 使用 MQA（所有 head 共享 K、V）减少 KV Cache，使 8K 长上下文推理更高效。

## 评测基准

- **HumanEval**：164 道 Python 编程题，评估功能正确性（pass@k）
- **MBPP**：974 道 Python 入门题
- **MultiPL-E**：多语言代码生成评估
- **DS-1000**：数据科学库调用能力
- **SWE-bench**：真实 GitHub Issue 修复能力

## 与 Agent 的结合

代码生成能力是 [[react-agent]] 和 [[tool-use]] 的基础。[[claude-code]] 等编程 Agent 的核心能力即为在 Agent Loop 中持续生成、执行和修正代码。

## 训练数据去毒

StarCoder 项目对数据做了大量治理：PII 检测/过滤、Opt-out 机制（开发者可要求移除自己的代码）、恶意代码检测，为开源代码模型树立了数据伦理标杆。
