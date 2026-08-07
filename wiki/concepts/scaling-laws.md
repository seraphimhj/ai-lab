---
title: 缩放定律
created: 2026-05-10
updated: 2026-08-07
type: concept
tags: [scaling, training, fundamentals]
sources: [raw/papers/2001.08361-Scaling-Laws-Neural-Language-Models.html, raw/papers/2203.15556-Chinchilla-Training-Compute-Optimal-LLMs.html, raw/papers/2304.01373-Pythia-A-Suite-for-Analyzing-Large-Language-Models-Across-Tr.html]
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

### 换一根轴：Chinchilla 的骨架是一道约束优化题，不是「20:1」这个数字 [[2026-07-16-chinchilla-scaling-laws]]

上面那张表容易被误读成「记住 20 tokens/参数就行」。07-16 伴读把整篇论文还原成它真正问的问题——**不是「模型该多大」，而是「固定算力 C 这一笔钱，下一单位该买一个参数、还是让已有参数多看一个 token」**。参数 N 与数据 D 不是两个独立旋钮，而是争夺同一预算的两种资源，被 `C ≈ 6ND` 这条硬约束锁死：固定 C，N 翻倍则 D 必须减半，不存在「同时免费拥有更多参数和更多数据」。

- **损失拆成三张可比较的账单**：`L(N,D) = E + A/N^α + B/D^β`——不可约损失 E（世界本来就难预测）+ 容量不足项（模型装不下）+ 训练不足项（模型没学够）。两个幂指数都 < 1，意味着资源翻很多倍、损失只按幂律缓慢下降，**边际收益递减**是 scaling 的底色。
- **最优点不是「两项误差相等」，而是「边际收益相等」**：把 `D = C/(6N)` 代回，最优 `N* ∝ C^(β/(α+β))`、`D* ∝ C^(α/(α+β))`。经济学意义上，最后一单位算力投给参数所减的损失 = 投给数据所减的损失。所以 scaling law 首先是一张**预算分配表**，不是模型排行榜。
- **Gopher→Chinchilla 不是「小模型逆袭」，是预算重分配**：同一量级算力，Gopher 把钱压在参数上（280B/300B，D/N≈1.07），Chinchilla 缩到 70B、把释放的算力用于多看 4× token（D/N=20），于是更小却更强、且推理时只需携带约 1/4 参数。

**最该带走的边界**：20:1 是特定数据分布、特定架构下的经验工作点，不是自然常数。至少五件事会移动它，对应一张诊断表——

```text
观察                          诊断              下一笔预算
参数增大仍显著降 loss          容量不足          倾向增加 N
延长训练仍显著降 loss          训练不足          倾向增加 D
新数据收益低、重复收益饱和      有效数据不足       提升质量/多样性（不是堆量）
训练已足但 serving 太贵         生命周期目标错位   缩小 N、增加训练 token
离线 loss 好但下游/线上差       数据分布或评测错位  查数据混合与评测污染
```

**交叉·D 只是「有效信息」的代理量**：这条论证结构与 [[retrieval-augmented-generation|RAG]] 同构——预训练把「有效训练信息」用易计数的 token 数 D 代理、RAG 把「有效检索证据」用召回条数 k 代理；一旦质量下降/重复增加，D 继续涨而「有效 D」增长变慢。于是三种「最优」必须分开：训练算力最优（Chinchilla 直接回答）、推理成本最优、全生命周期最优（训练+存储+推理+数据）——后者要接到 [[llm-inference-serving|推理系统三本账]]，Chinchilla 只顺手改善它、没替你解掉。这也正是**数据环节向目标函数与评测环节传导偏差**的位置：若语料有效多样性被高估、benchmark 又与语料污染重叠，评测会把错误配置伪装成进步（[[benchmark-evaluation]]）。

## 超越 Chinchilla

后续研究发现了更复杂的关系：

- **Over-training**：数据量超过 Chinchilla 最优比例，可以训练出同性能但更小的模型（[[llama]] 系列策略）
- **Emergent Abilities**：某些能力在规模超过阈值后突然出现（[[palm]] 在 540B 规模首次系统观察）
- **Data Quality > Quantity**：高质量数据比纯数量更重要（[[phi]] 系列 "Textbooks Are All You Need" 极端验证）
- [[mixture-of-experts]]：引入新的缩放维度（专家数 vs 激活参数）
- **Pythia**：EleutherAI 提供 70M-12B 共 16 个检查点的完整训练动态，用于研究 Scaling Laws 的微观机制（记忆/遗忘/偏差涌现）[[raw/papers/2304.01373-Pythia-A-Suite-for-Analyzing-Large-Language-Models-Across-Tr.html]]

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
- [[llm-inference-serving]] — 全生命周期最优要接到推理三本账（训练算力最优只顺手改善它）
- [[benchmark-evaluation]] — 数据环节的错误配置会经语料污染在评测端被伪装成进步
- [[retrieval-augmented-generation]] — 「token 数 D≈有效信息」与「召回 k≈有效证据」是同一种代理量近似
