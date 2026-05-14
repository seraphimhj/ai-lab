---
title: RLHF — 基于人类反馈的强化学习
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [training, alignment, reinforcement-learning]
sources: [raw/papers/1909.08593-Fine-Tuning-Language-Models-from-Human-Preferences.md, raw/papers/2203.02155-Training-language-models-to-follow-instructions-with-human-f.md, raw/papers/2204.05862-Training-a-Helpful-and-Harmless-Assistant-with-Reinforcement.md]
---

# RLHF — 基于人类反馈的强化学习

通过人类偏好反馈训练奖励模型，再用强化学习优化语言模型，使其输出更符合人类期望。[[raw/papers/1909.08593-Fine-Tuning-Language-Models-from-Human-Preferences.html]]

## 核心流程

RLHF 训练分为三个阶段：

### 阶段一：监督微调（SFT）

在有标注的指令-回答对上微调预训练模型，使其具备基本的指令遵循能力。

### 阶段二：训练奖励模型（RM）

1. 收集人类偏好数据：对同一 prompt 的多个回答进行排序
2. 训练一个 Reward Model 预测人类偏好
3. 损失函数基于 Bradley-Terry 排序模型：
   ```
   L = -log σ(r(x, y_w) - r(x, y_l))
   ```
   其中 y_w 是人类偏好的回答，y_l 是较差的回答

### 阶段三：强化学习优化（PPO）

- 使用 PPO（Proximal Policy Optimization）优化策略模型
- 目标：最大化 RM 给出的奖励
- 加入 KL 散度惩罚，防止模型偏离 SFT 模型过远
- 避免奖励黑客（reward hacking）问题

## 关键变体

| 变体 | 核心思想 | 代表工作 |
|------|---------|---------|
| InstructGPT | 三阶段 RLHF 流程 | OpenAI |
| ChatGPT | 基于 InstructGPT 的对话模型 | OpenAI |
| HH-RLHF | 同时优化 helpful & harmless | Anthropic |

## 局限性

- **成本高**：需要大量高质量人类标注数据
- **奖励黑客**：模型可能学会欺骗奖励模型
- **分布偏移**：RL 优化过程中模型输出分布可能偏移
- **标注一致性**：不同标注员的偏好可能不一致

## 相关概念

- [[dpo]] — RLHF 的替代方案，无需训练 RM
- [[constitutional-ai]] — 用 AI 反馈替代部分人类反馈
- [[instruction-tuning]] — RLHF 的前置步骤 SFT
