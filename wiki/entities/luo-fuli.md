---
title: 罗福莉
created: 2026-05-05
updated: 2026-05-05
type: entity
tags: [person, lab]
sources: [raw/transcripts/luo-fuli-interview-zhangxiaojun-2026.md]
---

# 罗福莉

小米大模型团队负责人，主导研发 [[mimo-v2]] 系列模型。曾供职阿里达摩院、DeepSeek。

## 职业经历

- 阿里达摩院 — 早期大模型研究
- DeepSeek — 参与预训练和 R1 相关工作，亲历 R1 的"奇袭"诞生
- 小米 — 大模型团队负责人，带领团队从零训练 1T 参数模型

## 关键技术判断（2026年）

- **Anthropic 路径正确**，Agent + Post-train 是当下共识方向
- **1T 模型是入场券**：实现接近 Claude Opus 4.6 水平的必要条件
- **RL scaling for Agent** 是核心赛点
- **卡的比例巨变**：Chat 时代 3:5:1 → Agent 时代 3:1:1（研究:预训练:后训练）
- **两年内可能实现 AGI**
- **Agent 自学习**即将发生：模型先吸收所有人智能，再靠自己产生更强智能

## 核心观点

### Agent 框架
- OpenClaw 是"划时代的 Agent 框架"，弥补了很多模型短板
- 一套复杂 Agent 框架设计能弥补非常多模型能力短板
- 顶尖模型应与顶尖 Agent 框架共同进步

### 模型架构
- 选择 Hybrid Attention + MTP 而非 MLA，更适合 Agent 长上下文推理
- MLA 在计算和访存已达完美临界点，无法叠加 MTP 加速

### 组织管理
- **平权有利于创新**：没有职级、没有小组、没有 deadline
- 环境比经验更重要
- 靠热爱驱动，不靠管理
- 让预训练的人做后训练是很好的补充（diversity）

## 相关实体

- [[mimo-v2]] — 主导研发的模型系列
- [[claude-code]] — 对其架构有深度分析
- [[agent-loop-taor]] — Agent 执行循环
