---
title: Self-RAG — 自我反思检索增强生成
created: 2026-05-10
updated: 2026-05-14
type: concept
tags: [retrieval, generation, agent]
sources: [raw/papers/2310.11511-Self-RAG-Learning-to-Retrieve-Generate-and-Critique-through-Self-Reflection.html, raw/papers/2401.15884-Corrective-Retrieval-Augmented-Generation.html]
---

# Self-RAG — 自我反思检索增强生成

通过在生成过程中引入反思标记（Reflection Tokens），让模型自主决定何时检索、何时使用检索结果、以及生成内容是否需要修正。[[raw/papers/2310.11511-Self-RAG-Learning-to-Retrieve-Generate-and-Critique-through-Self-Reflection.html]]

## 核心问题

标准 [[retrieval-augmented-generation]] 的局限：
- **过度检索**：简单问题也检索，浪费资源
- **检索噪声**：检索结果可能不相关，干扰生成
- **无自我判断**：无法评估生成质量

## Self-RAG 的解决方案

### 四种反思标记

| 标记 | 含义 | 作用 |
|------|------|------|
| Retrieve | 是否需要检索 | 自主决定是否调用检索器 |
| IsRel | 检索文档是否相关 | 过滤不相关文档 |
| IsSup | 生成是否被检索支持 | 检测幻觉 |
| IsUse | 检索是否有用 | 判断检索的实际价值 |

### 生成流程

```
Input → [Retrieve?] 
  → Yes → Retrieve → [IsRel?] → [IsUse?] → Generate → [IsSup?]
  → No → Generate → [IsSup?]
```

模型在每个关键决策点生成对应的反思标记，实现自适应检索和生成。

## 训练方法

### 三阶段训练

1. **反思标记预测**：训练模型生成反思标记
2. **批评任务**：训练模型评估生成质量
3. **生成微调**：结合反思能力进行端到端微调

### 训练数据构造

- 使用强检索器获取正/负文档
- 用语言模型生成 critique
- 标注生成内容是否被文档支持

## 效果

Self-RAG（7B 和 13B 参数）在六个任务上的表现：
- 显著优于 retrieval-augmented ChatGPT（在 4 个任务上）
- 超过 Llama2-chat 和 Alpaca（在所有任务上）
- 在 Open-domain QA、推理和事实验证任务上全面领先
- 长文本生成的事实准确性和引用精度显著提升
- 推理时可通过 reflection token 概率的加权线性和进行 segment-level beam search，实现可定制化解码

## CRAG — 纠正式检索增强生成

CRAG（Corrective Retrieval Augmented Generation）[[raw/papers/2401.15884-Corrective-Retrieval-Augmented-Generation.html]] 是另一种改进 RAG 鲁棒性的方法：

### 核心机制

1. **检索评估器**：轻量级模型评估检索文档质量，返回置信度
2. **三种触发动作**：
   - 置信度高 → 直接使用检索结果
   - 置信度低 → 触发大规模 web 搜索补充
   - 中间状态 → decompose-then-recompose 过滤无关信息
3. **信息萃取**：分解检索文档，选择性聚焦关键信息

### 特点

- Plug-and-play，可与各种 RAG 方法无缝结合
- 在短文本和长文本生成任务上均有显著提升

## 相关概念

- [[retrieval-augmented-generation]] — Self-RAG 的基础框架
- [[react-agent]] — 类似的反思循环思想
- [[graph-rag]] — 另一种 RAG 改进方向
- [[dense-passage-retrieval]] — Self-RAG 中使用的检索方法
- [[colbert-retrieval]] — 可作为 Self-RAG 检索器的替代方案
