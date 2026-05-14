---
title: GPT-3
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, architecture, nlp, llm]
sources: [raw/papers/2005.14165-Language-Models-are-Few-Shot-Learners.html]
---

# GPT-3

GPT-3 是 [[openai]] 于 2020 年发布的自回归语言模型，拥有 1750 亿参数，是此前最大非稀疏语言模型的 10 倍。GPT-3 证明了扩大模型规模可以显著提升 in-context learning 能力，无需梯度更新即可在多种任务上表现优异。[[raw/papers/2005.14165-Language-Models-are-Few-Shot-Learners.html]]

## 模型变体

| 名称 | 参数量 | 层数 | 隐藏维度 | 注意力头数 |
|------|--------|------|----------|------------|
| GPT-3 Small | 125M | 12 | 768 | 12 |
| GPT-3 Medium | 350M | 24 | 1024 | 16 |
| GPT-3 Large | 760M | 24 | 1536 | 16 |
| GPT-3 XL | 1.3B | 24 | 2048 | 20 |
| GPT-3 2.7B | 2.7B | 32 | 2560 | 20 |
| GPT-3 6.7B | 6.7B | 32 | 4096 | 32 |
| GPT-3 13B | 13B | 40 | 5140 | 40 |
| GPT-3 175B | 175B | 96 | 12288 | 96 |

## In-Context Learning

GPT-3 的核心发现是 **Scaling Law**：随着模型规模增长，few-shot 性能持续提升。模型可以通过任务描述和少量示例（zero-shot、one-shot、few-shot）直接完成新任务，无需微调。

## 训练数据

GPT-3 的训练数据来自多个来源的混合语料，总计约 3000 亿 Token：

- WebText2：过滤后的网页文本
- Books1/Books2：书籍语料
- Wikipedia：英文维基百科
- Common Crawl：大规模网页爬取数据

## 性能表现

- 在多项 NLP 任务上接近或达到微调 SOTA 水平
- 在翻译、问答、完形填空等任务上表现突出
- 能完成需要实时推理的任务，如解乱词、3 位数算术
- 生成的新闻文章人类评估者难以区分真伪

## 局限性与争议

- 训练数据中的偏见会被放大
- 在某些数据集上存在方法学问题
- 部分任务上 few-shot 学习仍有困难
- 高昂的计算成本限制了可复现性

## Scaling Laws 验证

GPT-3 的不同规模变体系统验证了 [[scaling-laws]]：模型性能随参数量呈幂律关系平滑提升。这一发现为后续 Chinchilla 等研究（更优数据/参数比例）奠定了经验基础。[[raw/papers/2001.08361-Scaling-Laws-Neural-Language-Models.html]]

## 后续影响

GPT-3 奠定了 [[gpt-4]] 的技术基础，其 [[in-context-learning]] 能力直接催生了 ChatGPT 的产品化。175B 参数的规模也推动了 [[llama]] 等开源模型在类似规模上的追赶。InstructGPT 后续通过 [[rlhf]] 将 GPT-3 对齐到人类偏好，形成了预训练→SFT→RLHF 的三阶段训练范式。[[raw/papers/2203.02155-Training-language-models-to-follow-instructions-with-human-f.html]]
