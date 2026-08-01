---
title: Mixture of Experts — 稀疏专家混合
created: 2026-05-10
updated: 2026-08-01
type: concept
tags: [architecture, efficiency, scaling]
sources: [raw/papers/2401.04088-Mixtral-of-Experts.html]
---

# Mixture of Experts — 稀疏专家混合

通过让模型包含多个"专家"子网络，但每次推理只激活其中少量专家，实现大模型容量与高效计算的平衡。[[raw/papers/2401.04088-Mixtral-of-Experts.html]]

## 核心思想

### 稠密模型 vs. MoE

| 特性 | 稠密模型 | MoE 模型 |
|------|---------|---------|
| 参数总量 | 全部参与计算 | 总量大，但每次只激活一部分 |
| 计算量 | 与参数量成正比 | 与激活参数量成正比 |
| 推理速度 | 慢 | 快（仅激活部分专家） |
| 模型容量 | 受限于计算预算 | 可以更大 |

## 架构设计

### Router（路由器）

- 一个轻量级门控网络
- 输入 token → 输出各专家的权重分布
- 选择 top-k 个专家（通常 k=1 或 k=2）

### Forward Pass

```
y = Σ G(x)_i × E_i(x)    # G: router, E: expert
```
其中只有 top-k 个 G(x)_i 非零。

### 典型配置（Mixtral 8×7B）

- 8 个专家，每层 8 个 feedforward block
- 每个 token 在每层由 router 选择 2 个专家处理并加性组合输出
- 总参数量：~47B，每 token 仅用 **13B 激活参数**
- 上下文长度：**32k tokens**
- 效果：超越或匹配 Llama 2 70B 和 GPT-3.5（所有评估基准）
- 在数学、代码生成和多语言基准上大幅超越 Llama 2 70B
- Mixtral 8×7B–Instruct 版本超越 GPT-3.5 Turbo、Claude-2.1、Gemini Pro（人类评估）
- 开源许可：Apache 2.0

## 训练挑战

### 负载均衡

Router 容易倾向于只使用少数专家，导致：
- 未使用的专家退化
- 负载不均

**解决方案**：
- 辅助损失（auxiliary loss）：鼓励均匀分配
- 噪声 Top-k：在路由中加入噪声增加探索

### Expert Dropout

某些专家可能变成"僵尸"专家，需要监控和调整。

## 发展脉络

| 模型 | 专家数 | Top-k | 总参数 |
|------|--------|-------|--------|
| Switch Transformer | 128-256 | 1 | 1.6T |
| GLaM | 64 | 1 | 1.2T |
| Mixtral 8×7B | 8 | 2 | 47B |
| DeepSeek-V2 | 160 | 6 | 236B |
| DeepSeek-V3 | 256 | 8 | 671B |

## 解耦的边界：一条收益、两笔账（07-29 反哺）

来自伴读 [[2026-07-29-moe-capacity-compute-routing]]。上面那张「稠密 vs MoE」表把 MoE 写成一个几乎无代价的胜利（「推理速度：快」），这一节把那句话拆开——**MoE 不是让同样的计算变便宜，而是把 dense 模型里被捆在一起的三个量拆开，让你能单独调它们；但没有让任何一个消失。**

### 先把「参数量」这个词拆成两个

Dense 模型里「参数多」同时意味着容量大、算得多、显存占得多——三件事绑成一个数字。MoE 把这个数字裂成两个必须分开报的量：

```text
N_total  = 全部专家参数    -> 决定「记多少」（容量）与「占多少显存」（权重驻留）
N_active = 每 token 激活参数 -> 决定「单 token 前向算多少 FLOPs」
```

Mixtral 的 46.7B / 12.9B 不是「13B 模型只占 13B 显存」，而是「46.7B 的容量、每 token 只走其中一段路径」。**「MoE 推理快」这句话只对 N_active 成立，对显存和延迟都不成立**——所以上表「推理速度：快」应读作「每-token FLOPs 低」，而非端到端更快。

### 账一（训练）：稀疏只有可调度时才转化为有效容量

专家坍缩是一个正反馈：`略好 → 分到更多 token → 学得更快 → 更好 → 更多 token`，结果少数专家挤爆、多数闲置，N_total 名义很大、有效容量退化成几个专家。auxiliary load-balancing loss（`L_aux ∝ Σ f_i·P_i`，f=实际流量、P=router 概率质量）惩罚的是「流量与概率同时集中」，只压极端失衡、不规定专家学什么；capacity factor 则给每个专家设槽位上限，太小则热门专家溢出、token 被丢（token dropping）伤质量，太大则空槽浪费算力。**关键纠偏**：轮询也能均衡，但那牺牲了 MoE 的价值（内容条件化计算）——难的是「让 router 有选择性，又不让选择性演化成拥堵」。

### 账二（推理）：不激活 ≠ 不驻留

低延迟 serving 需要所有可能被选中的专家权重都驻留在 GPU 上，于是出现「每-token FLOPs 低、总权重显存仍很高」的组合。专家放不下一张卡时跨设备布局，router 按内容路由触发 **all-to-all**（每台设备都可能向每台设备发 token 激活）。由此一个反直觉：**大 batch 时专家收到足够 token、通信被摊薄，MoE 的 FLOPs 优势才兑现；小 batch / 低并发时每个专家只收到零星 token，kernel 与通信开销盖过省下的矩阵乘法，理论优势未必变成延迟优势**——这正是它和 [[llm-inference-serving]] 里 continuous batching 接上的地方：更大的并发池让专家 batch 更饱满，但并发升高又加重通信/显存，需联合调度。

### 一个同构：MoE 的 router 就是内部参数的检索器

```text
MoE：先路由到少数专家，再执行参数计算
RAG：先检索少数文档，再执行上下文计算
```

二者都用「选择少数资源」扩大可用容量，也共享同一族失败模式：**路由/检索错了，后面算得再准也白算；路由太集中则热门资源拥堵；候选全集虽不参与本次计算，却仍要被存储和索引**（专家权重驻留 ↔ 文档索引常驻）。差别只是 MoE 路由的是内部参数、[[retrieval-augmented-generation|RAG]] 路由的是外部知识。这个同构给出一条评测提醒：router 不该只看最终 loss，还要单独看**选择质量、负载分布、失败切片**——与 [[benchmark-evaluation]] 「别用整体均值掩盖关键子集」同构。

### 它怎么改写 Chinchilla 的账本

Dense scaling 里 `训练算力 ∝ N·D`，N 是单一数字；MoE 里 N 裂开后账本变成：训练 FLOPs 主要跟 `N_active·D` 走、权重显存/检查点跟 `N_total` 走、通信开销跟专家布局/top-k/batch 走、模型质量四者共同决定。于是最优分配从 07-16 [[scaling-laws|Chinchilla]] 的「N vs D」二变量问题升级成 `{D, N_active, N_total, 路由/通信可承受度 H}` 四变量问题。**别把它简化成「把 Chinchilla 的 N 换成 N_active」**——那会漏掉总容量对 loss 的贡献，也漏掉路由与通信。

## 相关概念

- [[scaling-laws]] — MoE 提供了新的缩放维度
- [[model-quantization]] — 与 MoE 配合进一步压缩
- [[flash-attention]] — MoE 模型训练依赖高效注意力
- [[linear-attention]] — MoE + Linear Attention 可以进一步降低推理成本
- [[instruction-tuning]] — Mixtral-Instruct 使用 SFT + DPO 进行指令微调
- [[llm-inference-serving]] — MoE serving 的显存/通信账与 continuous batching 联合调度
- [[retrieval-augmented-generation]] — router 路由参数 ↔ RAG 检索文档，同构的「选择少数资源」及其失败模式
- [[benchmark-evaluation]] — router 评测别只看总 loss，要看负载分布与失败切片

## 伴读来源

- [[2026-07-29-moe-capacity-compute-routing]] — 一条收益两笔账、N_total/N_active 解耦、MoE↔RAG 同构、四变量 scaling 账本
