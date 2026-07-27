---
title: DPR — 密集段落检索
created: 2026-05-10
updated: 2026-07-27
type: concept
tags: [retrieval, embedding, efficiency]
sources: [raw/papers/2004.04906-Dense-Passage-Retrieval-for-Open-Domain-Question-Answering.html]
---

# DPR — 密集段落检索

使用双 BERT 编码器将问题和段落编码为稠密向量，通过向量相似度进行语义匹配的检索方法。[[raw/papers/2004.04906-Dense-Passage-Retrieval-for-Open-Domain-Question-Answering.html]]

## 核心架构

### 双编码器（Dual Encoder）

```
Question → BERT_Q → q_vector
Passage  → BERT_P → p_vector
Similarity = dot(q_vector, p_vector)
```

两个编码器独立工作：
- **Question Encoder**：将问题编码为向量
- **Passage Encoder**：将候选段落编码为向量

### 为什么用双编码器而非交叉编码器

| 架构 | 优势 | 劣势 |
|------|------|------|
| 双编码器 | 可以预计算所有段落向量，检索时只需编码 query | 交互不够深入 |
| 交叉编码器 | Question 和 Passage 深度交互 | 每次检索都需要对所有候选段落编码 |

DPR 选择双编码器，因为检索场景需要快速匹配大量候选。

## 失败模式：单向量瓶颈不是「交互不够深入」，而是一次不可逆的过早聚合

上表把双编码器的代价写成「交互不够深入」，像是深度不足、加大模型即可缓解。
把这一栏拆到底会发现，它其实是一种**接口约束**，不是能力约束（详见
[[2026-07-24-late-interaction-muvera]]）。DPR 的效率来自一份「提前结算」：
passage 在离线阶段就被 `BERT_P` 压成一个固定向量，而**编码 passage 时它并不知道
未来的 query 会问什么**——所以只能把实体、时间、地区、指标、趋势、否定等异质信息
预先揉进同一个点（「先见自己，后见对方」）。压缩一旦完成，检索器只能看整体方向，
无法再追问「query 里的这个 token，究竟由 passage 里的哪个 token 支持」。

这条瓶颈的后果是**局部硬约束退化成可补偿的一项特征**。点积天然允许补偿：
query 换掉主体（「苹果公司」→「微软公司」）时，实体维少掉的分，可以被话题、
句式、领域相似度补回来，于是「A 公司营收」召回「B 公司营收」。这正是
[[text-embedding]] 里记的实体 mismatch，也是「过早聚合抹掉决定性少数信号」这一
更一般病灶在**编码端**的实例（评测端的同构版本见 [[benchmark-evaluation]] 的
「聚合掩盖关键切片」）。

要纠正一个常见误解：**这不是 mean-pooling 独有的 bug**。即使换成 `[CLS]` 或更
聪明的 learned pooling，只要最终接口仍是「一个 passage 一个向量」、最终相关性仍
主要由一个可补偿的标量决定，局部信号就没有被单独审计的资格。更强的 pooling 能
缓解，却取消不了这项信息瓶颈——区别是「能不能学到实体敏感」与「结构是否迫使它
单独结算」。

## 一根轴看清 DPR 的位置：交互被安排在链条哪一步

把 DPR 和它的后继放到同一根轴上，轴不是「稀疏还是稠密」，而是
*query 与 document 的细粒度交互发生在哪一步*：

| 方法 | 交互发生处 | 擅长保留 | 主要账单 |
|------|-----------|---------|---------|
| DPR（dense bi-encoder） | 编码后单次点积 | 整体语义 | 局部约束被过早聚合，不可逆 |
| [[sparse-retrieval]]（SPLADE） | 稀疏点积/倒排 | exact match + 扩展 | 词表绑定、索引膨胀 |
| [[colbert-retrieval]]（late interaction） | 检索时逐 token MaxSim | 实体/局部证据 | 存储与 m×n 匹配 |
| Cross-encoder | Transformer 内部全交互 | 关系/组合语义 | 无法全库逐篇跑 |

DPR 把交互推到最早（编码完即结算），换来「一篇文档一个点、可预计算、ANN 秒级召回」；
ColBERT 把交互推到检索时（保留 token 向量、MaxSim 让 query 每个检查项各找证据），
用存储换回实体级精度；MUVERA 再用 FDE 把这套多向量打分「保相似度地编译」回单向量
内积，让现成 MIPS 索引重新可用（见 [[colbert-retrieval]]）。所以选检索架构的真问题
不是「用哪种 embedding」，而是「愿意让 query 和 document 在哪一步、以多细的粒度见面，
为此付哪一笔账」。工程上二者常串成一条管线：DPR/dense 先粗召回，再交 ColBERT 或
cross-encoder 精排，把「不可逆的过早聚合」的损失在重排环节补回来。

## 训练过程

### 正负样本构造

- **正样本**：包含答案的段落
- **负样本**：
  - 同文档中其他段落（In-batch negatives）
  - BM25 检索到的但不包含答案的段落（Hard negatives）
  - 来自其他问题的黄金段落（跨问题负样本）

### 损失函数

```
L = -log exp(sim(q, p+)) / Σ exp(sim(q, pi))
```

NCE（Noise Contrastive Estimation）风格的损失函数。

## 与传统方法的对比

| 方法 | 检索类型 | 典型性能 |
|------|---------|---------|
| TF-IDF | 词频匹配 | 基线 |
| BM25 | 词频 + 文档长度归一化 | 强基线 |
| DPR | 语义匹配 | 显著优于 BM25 |

论文报告的具体数据：
- **Top-5 准确率**：DPR 65.2% vs. BM25 42.9%（Natural Questions open setting）
- **Top-20 检索准确率**：DPR 比 BM25 高 9%–19%（跨多个 QA 数据集）
- **端到端 QA**：DPR + reader 达到 41.5% EM，显著超过 ORQA 的 33.3%
- 训练仅需少量问题-段落对（无需额外预训练如 ICT）

## 应用

DPR 是 [[retrieval-augmented-generation]] 的核心检索组件，被广泛应用于：
- 开放域问答
- 企业知识库搜索
- [[tool-use]] 中的知识检索

## 相关概念

- [[retrieval-augmented-generation]] — DPR 是 RAG 的典型检索器
- [[text-embedding]] — DPR 使用 BERT 进行文本向量化
- [[colbert-retrieval]] — DPR 的改进版本，把交互从「编码后」推迟到「检索时」的 Late Interaction
- [[sparse-retrieval]] — 稀疏路：把实体 exact-match 留在独立词表维，另一种「拒绝过早聚合」的修法
- [[benchmark-evaluation]] — 「过早聚合抹掉少数信号」病灶的评测端同构版本
- [[self-rag]] — 结合检索和生成的方法
- [[in-context-learning]] — DPR 通过 few-shot 示例训练双编码器

## 伴读回流

- [[2026-07-24-late-interaction-muvera]] — 单向量信息瓶颈、late interaction 的「交互推迟到哪一步」轴、MUVERA/FDE 保相似度编译（本页「失败模式」与「交互轴」两节的来源）
