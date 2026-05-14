---
title: 缩放定律
created: 2026-05-10
updated: 2026-05-14
type: concept
tags: [scaling, training, fundamentals]
sources: [raw/papers/2001.08361-Scaling-Laws-Neural-Language-Models.html, raw/papers/2203.15556-Chinchilla-Training-Compute-Optimal-LLMs.html]
---

# 缩放定律

描述语言模型性能如何随模型规模（参数量）、数据量和计算量增长的定量规律。是大模型时代的理论基础。[[raw/papers/2001.08361-Scaling-Laws-Neural-Language-Models.html]]

## Kaplan Scaling Laws（2020）[[raw/papers/2001.08361-Scaling-Laws-Neural-Language-Models.html]]

OpenAI 首次系统性发现：

### 三条核心定律

1. **参数缩放**：性能 ∝ N^α，α ≈ 0.076
2. **数据缩放**：性能 ∝ D^α，α ≈ 0.095
3. **计算缩放**：性能 ∝ C^α，α ≈ 0.050

性能（交叉熵 loss）与三者呈幂律关系：
```
L(N) = (N_c / N)^α_N + L_∞
L(D) = (D_c / D)^α_D + L_∞
L(C) = (C_c / C)^α_C + L_∞
```

### 关键结论

- 模型越大，越能从更多数据中受益
- 短期看，增加参数最有效
- 幂律关系在多个数量级内成立

## Chinchilla Scaling Laws（2022）[[raw/papers/2203.15556-Chinchilla-Training-Compute-Optimal-LLMs.html]]

DeepMind 修正了 Kaplan 的结论：

### 关键发现

- 之前的大模型**参数过大、数据太少**
- 计算最优的比例：**参数量 ≈ 20 × token 数**
- 例如：70B 参数的模型需要约 1.4T tokens

### 影响与意义

| 模型 | 参数量 | 训练 tokens | Chinchilla 最优？ |
|------|--------|------------|-----------------|
| GPT-3 (175B) | 175B | 300B | ❌ 数据不足 |
| Chinchilla (70B) | 70B | 1.4T | ✅ |
| LLaMA (65B) | 65B | 1.4T | ✅ |
| GPT-4 | 未知 | 未知 | - |

## 超越 Chinchilla

后续研究发现了更复杂的关系：

- **Over-training**：数据量超过 Chinchilla 最优比例，可以训练出同性能但更小的模型（LLaMA 系列策略）
- **Emergent Abilities**：某些能力在规模超过阈值后突然出现
- **Data Quality > Quantity**：高质量数据比纯数量更重要
- [[mixture-of-experts]]：引入新的缩放维度（专家数 vs 激活参数）

## 实践指导

1. 确定计算预算 C
2. 根据 Chinchilla 比例分配 N 和 D
3. 优先保证数据质量
4. 考虑 over-training 策略降低推理成本

## 相关概念

- [[mixture-of-experts]] — 新的缩放维度（稀疏参数）
- [[test-time-compute]] — 推理时计算缩放，与预训练缩放互补
- [[instruction-tuning]] — 缩放定律在指令微调阶段的体现
- [[model-quantization]] — 推理阶段的缩放优化
