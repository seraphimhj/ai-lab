---
title: Agent 上下文缺口
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [agent, agentic, architecture, framework]
sources: [raw/articles/designing-for-agents-2025.md]
---

# Agent 上下文缺口

> 在多 Agent 协作场景中，不同 Agent 掌握不同上下文，产品设计需要弥合这一缺口。来源：Teddy Riker (Ramp) 的 "Designing for Agents"。[[raw/articles/designing-for-agents-2025.md]]

## 问题定义

在第三代交互模型（User → User's Agent → Software's Agent → Database）中，两个 Agent 各自掌握不同的信息上下文，形成**上下文缺口（Context Gap）**。[[raw/articles/designing-for-agents-2025.md]]

这种缺口是系统性的 — 每个 Agent 天然只能访问自己所属系统内的数据，但完整的决策往往需要跨系统的上下文。

## 案例：Diego 的报销场景[[raw/articles/designing-for-agents-2025.md]]

Diego 需要报销一笔晚餐费用。场景中涉及两个 Agent：

**Diego 的 AI 首席幕僚（User's Agent）掌握：**
- 📅 日历信息 — 知道当晚有客户会议
- 📧 邮件 — 有酒店和航班的确认信息
- 💬 Slack 线程 — 知道晚餐的上下文（客户聚餐、团队建设还是个人消费）
- 🧾 收据 — 持有消费凭证

**费用管理系统 Agent（Software's Agent）掌握：**
- 💳 交易数据 — 金额、商户、时间
- 📋 公司政策 — 报销规则、限额
- 🏷️ GL 科目 — 150 个总账科目代码
- 📊 历史分类 — 过往类似交易的分类记录

## 糟糕的设计 vs 好的设计

### ❌ 糟糕的设计（传统 API 思维）

> "Here's a transaction, pick from 150 GL codes."

将内部数据结构直接暴露给调用方，要求对方做出精确的底层决策。这对人类开发者来说尚且困难，对缺乏领域知识的 Agent 来说更是不可能完成的任务。

### ✅ 好的设计（Agent 产品思维）

> "Is this a client meal, team meal, or personal expense?"

**索要上下文，而非索要答案。**[[raw/articles/designing-for-agents-2025.md]]

好的设计遵循以下原则：

1. **问你知道对方能回答的问题** — Diego 的 Agent 知道晚餐是客户餐，但不知道对应的 GL code
2. **暴露语义接口，而非数据接口** — "客户餐/团队餐/个人费用" 是语义概念，"GL-4721/GL-8830/GL-1105" 是内部编码
3. **让每个 Agent 贡献它最了解的内容** — User's Agent 贡献业务上下文，Software's Agent 贡献规则映射
4. **在 Agent 之间协商，而非在一端做全部决策**

## 设计原则总结

| 原则 | 说明 | 反模式 |
|------|------|--------|
| 索要上下文而非答案 | 问"这是什么类型的费用"而非"选哪个 GL code" | 暴露内部编码让 Agent 选择 |
| 语义接口优于数据接口 | 用业务语言而非系统编码定义参数 | 直接暴露数据库 schema |
| 分工协作 | 每个 Agent 贡献其专长领域的信息 | 要求一个 Agent 掌握所有上下文 |
| 渐进式细化 | 先获取高层上下文，再逐步精化 | 一次性要求完整精确输入 |

## 与其他概念的关系

- [[agent-product-design]] — 上下文缺口管理是 Agent 产品设计三大原则之一
- [[agent-feedback-loop]] — 反馈工具可以辅助发现上下文缺口的位置和模式
- [[claude-code-memory-system]] — Claude Code 的分层记忆召回机制本质上也是在解决上下文缺口问题

## 核心引用

> "过去，界面夹在 Diego 和他的费用系统之间。现在，界面夹在他的智能体和你的智能体之间。"[[raw/articles/designing-for-agents-2025.md]]

这句话揭示了 Agent 时代的核心设计挑战：你的"用户"现在是另一个 Agent，而你需要设计的是两个 Agent 之间的协商协议。
