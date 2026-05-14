---
title: Anthropic
created: 2026-05-10
updated: 2026-05-10
type: entity
tags: [company, lab, llm, alignment]
sources: []
---

# Anthropic

Anthropic 是由 Dario Amodei 和 Daniela Amodei 等前 OpenAI 成员于 2021 年创立的 AI 安全公司。Anthropic 以"AI 安全"为核心使命，致力于构建可靠、可解释、可控的 AI 系统。其 Claude 系列模型是 [[openai]] GPT 系列的主要竞争者。

## 核心产品

### Claude 系列

- Claude 1/2/3/3.5/4：持续迭代的大语言模型系列
- Claude 3 Opus/Sonnet/Haiku：三级定位策略
- 支持 200K Token 超长上下文
- 多模态能力（图像理解）
- Claude 3.5 Sonnet 在多项基准上超越 GPT-4o

### Agent 产品

- [[claude-code]]：基于终端的 AI Coding Agent
- Claude Artifacts：交互式内容创作
- Claude for Enterprise：企业级 AI 解决方案

## 关键技术贡献

### Constitutional AI (CAI)

Anthropic 提出的 Constitutional AI 是 AI 对齐领域的重要创新。[[raw/papers/2212.08073-Constitutional-AI-Harmlessness-from-AI-Feedback.html]]

- 使用一组原则（宪法）指导 AI 行为
- AI 自我批评和修正（RL from AI Feedback）
- 减少对大量人工标注的依赖
- 显著提升模型的安全性和有用性

### RLHF 研究

Anthropic 在 RLHF（Reinforcement Learning from Human Feedback）领域做出了奠基性贡献，其研究揭示了 RLHF 的能力和局限。

### AI 安全研究

- 可解释性研究（Sparse Autoencoders、Circuit Analysis）
- Red Teaming 方法论
- 诚实性研究
- 长期风险和超级智能对齐

## RSP（Responsible Scaling Policy）

Anthropic 提出了负责任扩展政策（RSP），将 AI 安全级别与模型能力挂钩：

- ASL-1/2/3：不同安全等级
- 设定能力阈值，达到阈值前必须完成安全评估
- 推动行业对 AI 治理的标准化

## 商业模式

- Claude Pro / Team / Enterprise 订阅
- API 按量付费
- 与 AWS、Google Cloud 等云平台合作
- 亚马逊是其主要投资方

## 行业影响

Anthropic 的 AI 安全理念对整个行业产生了深远影响。其 Constitutional AI 方法被多家公司借鉴，安全优先的价值观也推动了行业对 AI 治理的重视。
