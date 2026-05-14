---
title: Self-RAG — 自我反思检索增强生成
created: 2026-05-10
updated: 2026-05-10
type: concept
tags: [retrieval, generation, agent]
sources: [raw/papers/2310.11511-Self-RAG-Learning-to-Retrieve-Generate-and-Critique-through-Self-Reflection.md]
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

在多个基准测试上，Self-RAG 显著优于标准 RAG 和纯 LLM：
- 提升事实准确性
- 减少幻觉
- 在不需要检索的场景中更高效
- 更好的引用质量

## 相关概念

- [[retrieval-augmented-generation]] — Self-RAG 的基础框架
- [[react-agent]] — 类似的反思循环思想
- [[graph-rag]] — 另一种 RAG 改进方向
- [[dense-passage-retrieval]] — Self-RAG 中使用的检索方法
