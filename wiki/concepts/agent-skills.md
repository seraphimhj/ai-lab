---
title: Agent Skills（可复用工作流程）
created: 2026-05-14
updated: 2026-05-14
type: concept
tags: [agentic, tutorial]
sources: [raw/articles/llm-agent-core-principles-2026.md]
---

# Agent Skills（可复用工作流程）

## 定义

Skills 是将常用操作流程沉淀成文档，让 Agent 按文档执行的可复用工作模式。本质上是把人类的专业操作手册编码为 LLM 可理解的文本指令。

## 典型结构（以 Anthropic PDF Skill 为例）

```
skills/pdf/
├── SKILL.md        # 核心：何时触发 + 操作指南
├── reference.md    # 详细参考文档
├── forms.md        # 表单填写专项指南
└── scripts/        # 预写好的 Python 脚本
    ├── extract_form_field_info.py
    ├── fill_fillable_fields.py
    ├── convert_pdf_to_images.py
    └── ...
```

SKILL.md 开头通过 YAML frontmatter 定义触发条件：

```yaml
---
name: pdf
description: Use this skill whenever the user wants to do anything with PDF files.
---
```

## 渐进式披露（Progressive Disclosure）

Skills 的核心设计模式，解决上下文窗口有限的问题：

1. **启动时**：只加载 Skill 名称 + 一句话简介（节省 token）
2. **匹配时**：模型发现任务与某个 Skill 相关，才加载完整内容
3. **按需深入**：只加载当前任务需要的子文档和脚本

这与传统 RAG 的区别在于：Skills 是精心编写和结构化的操作文档，而非被动的文本片段检索。

## 与其他模式的区别

| 模式 | 特点 |
|------|------|
| System Prompt | 全局生效，常驻上下文 |
| Function Calling | 定义工具接口，模型按需调用 |
| Skills | 完整操作手册，按需加载到上下文 |
| RAG | 检索文档片段，补充背景知识 |

## 在 Agent 架构中的位置

Skills 位于 Agent 循环的知识层：

- LLM 遇到特定类型任务 → 触发对应 Skill
- Skill 内容加载到上下文 → 模型按指南执行
- 可包含预写脚本，模型通过 Tool Use 调用

## 与相关概念的关系

- [[context-engineering]]：Skills 是上下文工程的重要手段——按需加载操作文档
- [[react-agent]]：Agent 循环中通过 Skills 获取执行指导
- [[tool-use]]：Skills 中可能包含可调用的脚本工具
- [[claude-code]]：Claude Code 使用 Skills 系统管理各类操作能力
