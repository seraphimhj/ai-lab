---
title: AI 范式转移：从 Chat 到 Agent
created: 2026-05-05
updated: 2026-05-05
type: concept
tags: [agent, llm, timeline, architecture]
sources: [raw/transcripts/luo-fuli-interview-zhangxiaojun-2026.md]
---

# AI 范式转移：从 Chat 到 Agent

2026 年大模型竞争的第二幕：从 Pre-train 主导的 Chat 时代，转向 Post-train 主导的 Agent 时代。

## 核心变化

### Chat 时代
- 以 Pre-train 为核心
- 短上下文（4K → 128K）
- 模型即产品
- RL 以 Rollout 推理引擎为中心
- 评估：SWE-Bench、LeetCode Bench 等 Benchmark

### Agent 时代
- 以 Post-train 为核心，RL scaling for Agent
- 长上下文（1M → 10M）
- 模型 + Agent 框架 = 产品
- RL 以 Agent 为核心（更复杂系统）
- 评估：端到端任务完成率，工业级可用性
- 卡的投入：研究:预训练:后训练 = 3:1:1

## 关键信号

- [[claude-code]] + Claude Opus 4.6 展示了 Agent 范式的正确路径
- OpenClaw 开源让全球开发者参与 Agent 框架进化
- Code 的强泛化性从每个范式都"戳中了那个点"
- Agent 框架能弥补模型短板，激发中层模型上限

## 入场条件

- 1T+ 参数基座模型
- Long Context 高效架构
- 敏捷的 Post-train 团队
- 足够的算力（研究卡是训练卡的 3-5 倍）

## 罗福莉的判断

> "上一个时代的成功并不意味着下一个时代的领先，现在基本上大家在同一水平线。"

国内具备 1T+ 基座的公司（Kimi、MiMo 等），距 Claude Opus 4.6 水平约 **两三个月** 代差。

## 相关概念

- [[luo-fuli]] — 提出此判断
- [[mimo-v2]] — 快速转向 Agent 范式的模型
- [[agent-loop-taor]] — Agent 执行循环
- [[claude-code]] — Agent 范式的标杆产品
