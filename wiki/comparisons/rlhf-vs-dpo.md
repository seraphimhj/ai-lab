---
title: RLHF vs DPO 对齐方法对比
created: 2026-05-10
updated: 2026-05-10
type: comparison
tags: [comparison, alignment, rlhf, dpo, training, safety]
sources: [raw/papers/2203.02155-Training-language-models-to-follow-instructions-with-human-f.html, raw/papers/2204.05862-Training-a-Helpful-and-Harmless-Assistant-with-Reinforcement.html]
---

# RLHF vs DPO 对齐方法对比

将预训练 LLM 对齐人类偏好（helpful, harmless, honest）的两种主流方法。[[raw/papers/2203.02155-Training-language-models-to-follow-instructions-with-human-f.html]]

## 流程对比

### RLHF (Reinforcement Learning from Human Feedback)

```
预训练模型 → SFT (监督微调) → 训练 Reward Model → PPO 强化学习 → 对齐模型
                ↑                    ↑                    ↑
            人类标注偏好         人类排序数据           Reward Model 打分
```

三阶段流程：SFT → RM → PPO。

### DPO (Direct Preference Optimization)

```
预训练模型 → SFT → DPO (直接用偏好数据优化) → 对齐模型
                        ↑
                   人类排序数据 (无需 RM)
```

两阶段流程：SFT → DPO，隐式消除 Reward Model。

## 核心维度对比

| 维度 | RLHF | DPO |
|------|------|-----|
| **训练阶段数** | 3 (SFT + RM + PPO) | 2 (SFT + DPO) |
| **Reward Model** | ✅ 需要单独训练 | ❌ 不需要（隐式推导） |
| **样本效率** | 中等（RM + PLO 各需数据） | 高（偏好数据直接用） |
| **训练稳定性** | ❌ PPO 超参敏感，易不稳定 | ✅ 更稳定，本质是分类损失 |
| **计算开销** | 高（4 个模型同时在线） | 低（仅需 policy 模型） |
| **实现复杂度** | 高（需要 PPO 训练基础设施） | 低（几行代码改动） |
| **效果上限** | ⭐⭐⭐⭐⭐（理论上限更高） | ⭐⭐⭐⭐（多数场景够用） |
| **控制粒度** | 高（可精细调 reward） | 中（受限于偏好数据质量） |
| **代表应用** | InstructGPT, Claude, ChatGPT | Zephyr, Tülu, many open models |

## 数学本质

DPO 的核心洞察：RLHF 的最优 policy 可用闭式解表示，无需显式训练 RM。

$$\pi_\theta(y|x) = \frac{1}{Z(x)} \pi_{\text{ref}}(y|x) \exp\left(\frac{1}{\beta} r(x,y)\right)$$

DPO 将此公式代入 Bradley-Terry 偏好模型，得到直接优化目标：

$$\mathcal{L}_{\text{DPO}} = -\mathbb{E}\left[\log \sigma\left(\beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right)\right]$$

## 各自优势与局限

### RLHF 优势
- 可针对不同维度训练独立 Reward Model（helpfulness / safety）
- 支持在线学习，可实时收集反馈
- 理论框架成熟，可控性强

### RLHF 局限
- PPO 训练不稳定，超参调优成本高
- Reward Model 可能被 policy hack（reward hacking）
- 工程复杂度高

### DPO 优势
- 实现简单，无需 PPO 训练循环
- 训练更稳定，适合资源有限的团队
- 偏好数据直接利用，样本效率高

### DPO 局限
- 离线方法，无法在线收集反馈
- 偏好数据质量直接影响效果
- 对极端偏好的建模能力有限

## 进展与变体

| 方法 | 改进方向 |
|------|----------|
| **IPO** | 解决 DPO 的 over-optimization 问题 |
| **KTO** | 只需好坏信号，无需成对偏好 |
| **ORPO** | 合并 SFT 和对齐为单阶段 |
| **SimPO** | 用 response 长度作为隐式 reward |
| **GRPO** | DeepSeek-R1 使用的组相对策略优化 |

## 相关链接

- [[rlhf]] — RLHF 详解
- [[dpo]] — DPO 详解
- [[constitutional-ai]] — Anthropic 的对齐方法
- [[deepseek]] — GRPO 应用的代表模型
- [[gpt-3]] — RLHF 首个大规模应用
