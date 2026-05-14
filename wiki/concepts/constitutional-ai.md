---
title: Constitutional AI — 宪法式 AI
created: 2026-05-10
updated: 2026-05-14
type: concept
tags: [alignment, training, safety]
sources: [raw/papers/2212.08073-Constitutional-AI-Harmlessness-from-AI-Feedback.html, raw/papers/2209.07858-Red-Teaming-Language-Models-to-Reduce-Harms-Methods-Scaling.html]
---

# Constitutional AI — 宪法式 AI

Anthropic 提出的一种对齐方法，用一组明确的原则（"宪法"）来指导 AI 自我改进，减少对人类标注的依赖。[[raw/papers/2212.08073-Constitutional-AI-Harmlessness-from-AI-Feedback.html]]

## 核心思想

不直接用人类标注有害/无害，而是让 AI 根据一组**预先定义的原则**来：
1. 批评和修正自己的回答
2. 生成 AI 反馈用于训练

## 训练流程

### 阶段一：监督学习（SL）

1. **生成有毒回答**：用有害 prompt 让模型生成回答
2. **自我批评**：给模型一条宪法原则，要求它批评自己的回答
3. **修正回答**：根据批评结果生成无害的回答
4. **SFT 微调**：用 (prompt, 修正后回答) 对微调模型

### 阶段二：AI 反馈 RL（RLAIF）

1. 用宪法原则让 AI 对两个回答进行偏好排序
2. 用这些 AI 生成的偏好数据训练 [[rlhf]] 的奖励模型
3. 用 PPO 优化，但**无需人类标注**

## 宪法原则示例

- "请选择最无害、最符合伦理的回答"
- "请选择最不具有歧视性的回答"
- "请选择最能帮助用户的回答"

原则可以来自人类编写的准则、UN 人权宣言等。

## 优势

- **减少人类标注**：用 AI 反馈替代大量人类偏好标注
- **可审计性**：宪法原则是明确可检查的
- **可扩展性**：易于添加新原则来覆盖新场景
- **灵活性**：不同应用可以定义不同的"宪法"

## 局限性

- 宪法原则的质量直接影响效果
- AI 自我批评可能不够深入
- 仍需少量人类标注来评估和验证

## 与 Red Teaming 的关系

[[anthropic]] 同期发表的 Red Teaming 研究 [[raw/papers/2209.07858-Red-Teaming-Language-Models-to-Reduce-Harms-Methods-Scaling.html]] 证明了 AI 辅助红队测试可以发现大量人类未曾想到的攻击方式。CAI 的自我批评机制可视为一种内化的红队测试。

## 相关概念

- [[rlhf]] — CAI 后半段仍使用 RLHF 流程
- [[dpo]] — 另一种减少 RLHF 复杂度的方法
- [[instruction-tuning]] — 对齐训练的基础
