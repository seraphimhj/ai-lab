---
title: DPO — Direct Preference Optimization
created: 2026-05-10
updated: 2026-08-04
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

## 换一根轴：KL 在 DPO 里是「锚」，和评测端那把「尺」是同一个散度

> 反哺自 07-31 伴读 [[2026-07-31-proper-scoring-rules-honest-probabilities]]：它把 log loss 的
> 超额风险推成 KL(q‖p)，正好和 DPO 里的 KL 约束凑成同一个数学对象在闭环两端的两副面孔。

上面「数学原理」把 KL 只当成 RLHF 目标里一句「同时满足 KL 约束」，容易读成一条可有可无的
护栏。实际上 KL 是 DPO 闭式解**能成立的前提**，它并没有在 DPO 里消失，而是被折进了损失：

- **DPO 没有去掉 KL 锚，只是把它内生化。** RLHF 的最优策略是
  `π*(y|x) ∝ π_ref(y|x)·exp(r(x,y)/β)`——这个解本身就带着参考策略 π_ref 这个锚点。DPO 把奖励
  反解成 `r = β·log(π_θ/π_ref) + βlog Z`，于是损失里的 `log(π_θ/π_ref)` 这一项**就是**对 π_ref
  的 KL 约束的显式化身。不是「先优化奖励、再加 KL 惩罚」，而是「奖励的定义里已经写死了以 π_ref 为
  基准」。撤掉 π_ref（令其为均匀分布），DPO 就退化成对偏好对做无约束的最大似然，会把策略推到远离
  预训练分布的地方。
- **β 是锚绳的松紧，不是学习率。** β 大 = KL 锚拉得紧 = 策略被按在 π_ref 附近、保守；β 小 = 放长
  锚绳 = 允许为迎合偏好大幅漂移，也更容易被噪声偏好（见「局限性」）带偏。DPO 的「过优化」表现为
  β 太小时策略钻偏好数据空子、离 π_ref 越来越远——这正是 KL 锚失效的样子。

而真正值得记住的新洞见是**同一个 KL 在端到端闭环里换岗**：

```text
KL(q‖p) 的两副面孔
  训练端（DPO/RLHF）：KL 是「锚」——把策略拴在 π_ref 上，越小越保守（约束项，被动约束）
  评测端（proper score）：KL 是「尺」——log loss 相对诚实报告多付的超额风险（度量项，被动度量）
        └─ 见 [[probability-calibration]]：excess risk = KL(q‖p)，只有 p=q 时为 0
```

一个当「约束」拴住优化、一个当「刻度」度量诚实，方向性（谁锚向谁）和角色都不同，却共享
「分布失配要付代价」这同一副骨架。看清这点，就不必把 DPO 的 KL 约束、蒸馏里的 KL、评测里的 KL
当成三件事分开背——它们是一个散度在闭环三个工位上的三种用法（这条线索另有一条交叉 pick 在
`queries/picks.md` 待推）。

## 相关概念

- [[rlhf]] — DPO 所简化的原始方法
- [[constitutional-ai]] — 另一种减少人类标注的方案
- [[instruction-tuning]] — 偏好学习的基础
- [[probability-calibration]] — 评测端的 KL：同一散度当「尺」而非「锚」
- [[2026-07-31-proper-scoring-rules-honest-probabilities]] — 反哺来源（proper score 的 excess risk=KL）
