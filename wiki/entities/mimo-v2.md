---
title: MiMo-V2
created: 2026-05-05
updated: 2026-05-05
type: entity
tags: [model, architecture, open-source, multimodal]
sources: [raw/transcripts/luo-fuli-interview-zhangxiaojun-2026.md, raw/articles/attention-algorithm-innovation-2025.md]
---

# MiMo-V2

小米大模型团队（[[luo-fuli]] 负责）研发的模型系列，包含 Flash、Pro、Omni、TTS 四个模型。

## 模型家族

| 模型 | 定位 | 特点 |
|------|------|------|
| Flash | 性价比 | 100-150 TPS，极速推理 |
| Pro | 旗舰 | 1T 总参，对标 Claude Opus 4.6 |
| Omni | 全模态 | 音视频联合理解，原生多模态训练 |
| TTS | 语音合成 | 离散音频建模，强泛化力 |

## 核心技术决策

### Hybrid Attention + MTP（而非 MLA）[[raw/articles/attention-algorithm-innovation-2025.md]]
- **选择原因**：MLA 已达 compute/memory bound 完美临界点，无法叠加 MTP
- Hybrid Attention 在计算上留有大量富余，可用 MTP 填补加速
- Flash/Pro 推理速度远超 MLA 架构模型（如 GLM-5、Kimi K2）
- 采用 **3:1 比例**（3 层 [[linear-attention]] + 1 层 Full Attention），与 Kimi Linear、Qwen3-Next 一致[[raw/articles/attention-algorithm-innovation-2025.md]]
- 已知弱点：Multi-Hop Reasoning（多跳推理）会掉点[[raw/articles/attention-algorithm-innovation-2025.md]]
- 详见 [[hybrid-attention]] 和 [[hybrid-vs-sparse-attention]]

### 1M 上下文窗口
- 设计之初就为 Long Context 效率和推理效率优化
- 更小 KV Cache 支持多级缓存，有利于节省推理成本

### MTP（Multi-Token Prediction）
- 预训练阶段加 MTP 提升基座能力
- 推理时利用 MTP 加速，降低单 token 生成成本
- 不会带来幻觉（预测准才采纳）

## 与竞品对比

- 架构选择与 DeepSeek V3/R1（MLA）、GLM-5、Kimi K2 不同
- 推理速度和成本是核心优势
- Agent 场景下表现超预期

## 定价策略变化

- Flash：极致性价比（输入百万 token 1.01 美金）
- Pro：按价值定价而非推理成本定价，因后训练带来溢价

## 相关概念

- [[agent-paradigm-shift]] — MiMo 快速转向 Agent 后训练范式
- [[hybrid-attention]] — MiMo 采用的混合注意力架构
- [[hybrid-vs-sparse-attention]] — Hybrid Linear vs Sparse Attention 对比
- [[linear-attention]] — Linear Attention 技术详解
- [[yang-songlin]] — Linear Attention 核心研究者
- [[luo-fuli]] — 团队负责人
