---
source_url: https://mp.weixin.qq.com/s/9IpWaz8yXHViW_MBNkOZfQ
original_url: https://x.com/teddy_riker/status/2047312986696454584
ingested: 2026-05-05
sha256: b03237d35ce0e8f411ff66cfce8a9883b71060137f6a01995b147181aa1c7722
---

# 为 Agent 设计产品【译】

- **原标题:** Designing for Agents
- **作者:** Teddy Riker (Ramp)
- **译者:** 宝玉 (公众号 宝玉AI)
- **来源:** https://mp.weixin.qq.com/s/9IpWaz8yXHViW_MBNkOZfQ

## 核心论点

UI 没有死，但 80/20 法则已经翻转：80% 的人机交互将通过 AI Agent 完成。

三种交互模型正在演进：

1. **User → UI → Database**（传统模式）
2. **User → User's AI Agent → Database**（当前浪潮）
3. **User → User's AI Agent → Software's AI Agent → Database**（新兴模式）

**案例：Salesforce Headless 360** — 将整个平台暴露为 API/MCP/CLI，无需浏览器。

**数据：** Ramp 的 MCP 周活跃用户在 3 个月内增长了 10 倍。

## 教会 AI 智能体如何成功

**Notion MCP 示例：** `notion-create-pages` 工具在写入前要求先获取 `notion://docs/enhanced-markdown-spec` 资源 — "先读规范，再动笔"。

**Slack MCP 对比：** 不强制 Slack 特定格式，导致格式化错误。

**关键教训：** 不要让 Agent 猜测。在它们需要时，准确提供所需的规范。

- 旧世界：API 文档中的规范 → 开发者阅读 → 编写适配器
- 新世界：规范在运行时交付给 Agent，恰好在需要时

## 建立反馈循环

**Ramp MCP 可观测性问题：** 能看到工具调用量，但看不到聊天上下文。

三个解决方案：

1. **Rationale 参数：** 每个 MCP/CLI 调用要求 Agent 解释为什么
2. **反馈工具：** 独立工具让 Agent 报告什么失败了 / 尝试了什么
3. **Context Seeding：** 添加参数捕获后续有用的上下文

**反馈循环 → 产品改进：** rationale 模式揭示新功能信号（例如 "generating incident reports" → 构建专用工具）。

Agent 给出的反馈比人类用户更具体、更一致。

## 留意上下文缺口

**示例：Diego 的 AI 首席幕僚 vs 费用管理系统 Agent**

- AI 首席幕僚知道：日历、邮件（酒店/航班确认）、Slack 线程（晚餐上下文）、收据
- 费用系统知道：交易数据、公司政策、GL 科目、历史分类

- **糟糕的设计：** "这是一笔交易，从 150 个 GL code 中选择"（传统 API 思维）
- **好的设计：** "这是客户餐、团队餐还是个人费用？" — 索要上下文，而非索要答案

每个 Agent 贡献它最了解的内容 → 对 Diego 和他的会计师都有更好的结果。

> "过去，界面夹在 Diego 和他的费用系统之间。现在，界面夹在他的智能体和你的智能体之间。"
