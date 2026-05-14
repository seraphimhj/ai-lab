---
title: Long-Context Extension
created: 2026-05-14
updated: 2026-05-14
type: concept
tags: [optimization, architecture, inference, llm]
sources: [raw/papers/2309.00071-YaRN-Efficient-Context-Window-Extension-of-Large-Language-Mo.html, raw/papers/2309.12307-LongLoRA-Efficient-Fine-tuning-of-Long-Context-Large-Languag.html, raw/papers/2310.01889-Ring-Attention-with-Blockwise-Transformers-for-Near-Infinite.html]
confidence: high
---

# Long-Context Extension

长上下文扩展是将 LLM 的有效上下文窗口从预训练时的固定长度（如 4K/8K）扩展到数十万甚至数百万 token 的技术族群。

## 挑战

[[transformer-architecture]] 的自注意力机制导致两个核心瓶颈：
1. **显存占用**：注意力矩阵 O(L²) 空间复杂度
2. **位置编码外推**：RoPE 等位置编码在超出训练长度后性能骤降

## 技术路线

### 位置编码插值

#### YaRN（Yet another RoPE extensioN）

将 RoPE 频率分成三组进行差异化处理：[[raw/papers/2309.00071-YaRN-Efficient-Context-Window-Extension-of-Large-Language-Mo.html]]

- **高频维度**（局部信息）：保持不变，无需插值
- **低频维度**（全局位置）：线性插值，压缩位置表示
- **中频维度**：NTK-by-parts 混合插值

优势：仅需原始上下文 0.1% 的数据微调 ~400 步即可将 LLaMA 2 从 4K 扩展到 64K/128K。

#### Dynamic NTK

在推理时动态调整 NTK 基数，无需微调即可一定程度外推。

### 高效微调

#### LongLoRA

结合 [[lora]] 的参数高效方法扩展上下文：[[raw/papers/2309.12307-LongLoRA-Efficient-Fine-tuning-of-Long-Context-Large-Languag.html]]

- **S²-Attn（Shifted Sparse Attention）**：训练时将序列分组做局部注意力，组间通过 shift 保持信息流通
- 推理时使用完整注意力（无近似损失）
- 将 LLaMA 2 7B 从 4K 扩展到 100K，训练成本大幅降低

### 分布式长序列

#### Ring Attention

通过多设备环形通信实现近无限上下文：[[raw/papers/2310.01889-Ring-Attention-with-Blockwise-Transformers-for-Near-Infinite.html]]

核心机制：
1. 将序列按 block 分布到 N 台设备
2. 每台设备持有一个 Query block，Key-Value block 在设备间环形传递
3. 通信完全被 blockwise attention 计算掩盖（zero overhead）
4. **上下文长度随设备数线性增长**

实测：TPUv4-1024 上可训练 100M+ token 序列，比 memory-efficient Transformer 长 500×。

## 与其他技术的关系

| 技术 | 解决问题 | 互补性 |
|-----|---------|--------|
| [[flash-attention]] | 单设备注意力加速 | Ring Attention 建立在 blockwise attention 之上 |
| [[hybrid-attention]] | KV Cache 压缩 | Linear 层减少长文本 KV Cache 量 |
| [[sparse-attention]] | 计算量减少 | Top-K 选择性注意力 |
| [[lora]] | 参数高效微调 | LongLoRA 的基础 |

## 各模型长上下文能力

| 模型 | 上下文长度 | 扩展方法 |
|-----|-----------|---------|
| [[llama]] 3.1 | 128K | Rope scaling + 长文本续训 |
| [[yi-model]] | 200K | 位置编码优化 |
| [[deepseek]] V3 | 128K | YaRN + 渐进式扩展 |
| [[qwen]] 2.5 | 128K | YaRN + 长文本 SFT |
| Claude 3.5 | 200K | 未公开 |

## 开放问题

- "Needle in a Haystack" 测试表明：长度扩展 ≠ 长度利用，中间位置信息容易被忽略
- 更长上下文的高效训练数据构造仍是瓶颈
- 实际应用中 RAG vs 长上下文的 trade-off 尚无定论
