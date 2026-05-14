---
title: DPO — Direct Preference Optimization
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [training, alignment, optimization]
sources: []
---

# DPO — Direct Preference Optimization

将 [[rlhf]] 中的奖励模型训练和强化学习优化合并为一个简单的分类问题，直接从偏好数据优化策略模型。

## 核心动机

传统 RLHF 流程复杂：
1. 需要训练单独的 Reward Model
2. 需要运行 PPO 强化学习
3. 超参数多，训练不稳定

DPO 的关键洞察：RLHF 的最优解可以用解析形式表达，从而**跳过 RM 训练**。

## 数学原理

### RLHF 目标

给定偏好数据 (x, y_w, y_l)，RLHF 目标是最大化：
```
r_φ(x, y_w) - r_φ(x, y_l)
```
同时满足 KL 约束。

### DPO 的闭式解

通过将奖励函数表示为参考策略的函数：
```
r(x, y) = β log π(y|x) / π_ref(y|x) + β log Z(x)
```

可以直接将损失函数写为策略模型的目标：
```
L_DPO = -E[log σ(β log π_θ(y_w|x)/π_ref(y_w|x) - β log π_θ(y_l|x)/π_ref(y_l|x))]
```

**无需训练 RM，直接用偏好对优化 LLM。**

## 优势

| 对比维度 | RLHF | DPO |
|---------|------|-----|
| 奖励模型 | 需要单独训练 | 不需要 |
| 训练稳定性 | 依赖 PPO 调参 | 简单分类损失 |
| 计算开销 | 高（多个模型） | 低（单模型） |
| 实现复杂度 | 高 | 低 |

## 局限性

- 对噪声偏好数据敏感
- 在线探索能力弱（不像 PLOA 或强化学习可以在线采样）
- 长文本生成场景效果可能不如 RLHF

## 相关概念

- [[rlhf]] — DPO 所简化的原始方法
- [[constitutional-ai]] — 另一种减少人类标注的方案
- [[instruction-tuning]] — 偏好学习的基础
