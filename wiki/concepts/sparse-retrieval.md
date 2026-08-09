---
title: Sparse Retrieval
created: 2026-05-14
updated: 2026-08-09
type: concept
tags: [retrieval, embedding, nlp, rag]
sources: [raw/papers/2109.10086-SPLADE-v2-Sparse-Lexical-and-Expansion-Model-for-Information-Retrieval.html]
confidence: high
---

# Sparse Retrieval

稀疏检索是信息检索的经典范式，通过词汇级别的精确匹配实现文档召回。现代学习型稀疏检索（Learned Sparse Retrieval）结合了传统 BM25 的可解释性与神经网络的语义扩展能力。

## 从 BM25 到学习型稀疏检索

### 传统稀疏检索（BM25）

基于词频-逆文档频率（TF-IDF）的经典方法：
- 依赖精确词汇匹配
- 无法处理同义词/释义（vocabulary mismatch 问题）
- 但高度可解释、推理快速、无需 GPU

### 学习型稀疏检索（SPLADE）

SPLADE（SParse Lexical AnD Expansion model）用 [[bert]] 的 MLM head 为文档每个 token 生成词汇表上的稀疏权重：[[raw/papers/2109.10086-SPLADE-v2-Sparse-Lexical-and-Expansion-Model-for-Information-Retrieval.html]]

核心机制：
1. 文档通过 BERT 编码，每个 token 在 MLM head 输出 30K 维词汇表的 logits
2. 使用 max pooling + log-saturation 聚合为单一稀疏向量
3. 该向量自动实现**词汇扩展**（expansion）：文档中没出现的相关词也会获得非零权重

例如：文档"The cat sat on the mat"可能扩展出"feline", "kitten", "pet"等语义相关词。

### SPLADE v2 改进

- **蒸馏训练**：从 Cross-Encoder 教师模型学习
- **正则化**：FLOPS 正则化控制稀疏度，平衡效果与效率
- **效果**：在 MS MARCO 上超越 BM25 ~10 个点，接近 [[dense-passage-retrieval]] 水平

## SPLADE 的打分机制：一个词项权重的完整来历

上面说 SPLADE「用 MLM head 为每个 token 生成词表权重」，但真正的打分对象不是输入 token，而是**「位置 j × 词表项 i」这对关系** [[2026-07-15-splade-learned-sparse-retrieval]]：MLM head 对每个输入位置 j 都吐一整排约 30K 维 logit `s_ij`（位置 j 的上下文状态与词表向量 e_i 做点积的匹配分），一段长 L 的文本先得到一个 `L×|V|` 张量，再沿位置聚合成 `|V|` 维文本向量 [[2026-07-19-splade-mlm-head-term-scoring]]：

```text
w_i = max_j  log(1 + ReLU(s_ij))
```

三个算子各管一件事、缺一不可：
- **ReLU**：把负 logit 精确砍成 0，既是稀疏门、又保证权重非负（稀疏点积里共享词只加分，不会「两个负数相乘反而加分」）；
- **log(1+x)**：单调压缩正激活，边际增益递减（0→1 重要、20→21 微不足道），防少数超大 logit 垄断点积；
- **跨位置 max**：同一词项可能被多处点亮，只留最强证据——`w_i` 非零意味着「整段中至少一处强烈支持词项 i」，梯度也主要经获胜位置 `argmax_j` 回传，学习信号比 sum pooling 更集中。

**扩展（expansion）不由这三闸创造**：文档没出现 `myocardial` 却能得分，是因为 `heart attack` 的上下文让某位置表示落到接近 `myocardial` 词表向量的方向——扩展早在 `s_ij` 的词表投影里就发生了，三闸只决定哪些联想活下来、活下来权重多大。

### 关键边界：SPLADE 权重不是概率

标准 MLM 对同一位置的整张词表做 softmax，强迫所有词竞争总和为 1 的概率质量；SPLADE 在表示层直接对 `log(1+ReLU(s_ij))` 取值，**没有 softmax**，各维不必求和为 1，一篇心梗文档可以同时强烈点亮 heart / attack / myocardial / treatment。所以 `w_i` 不是「词 i 出现的概率」、不是「遮住位置 j 后的校准概率」，而是检索训练后的**词项重要性权重（term importance weight）**——形状更接近多标签分类而非完形填空。把 SPLADE 权重当置信度来读，是最常见的误用。

### 稀疏从哪来：FLOPS 正则在改 logit 的符号

ReLU 只能把「已经是负」的 logit 置零；真正把大量维度推过 0 的是训练里的稀疏正则。SPLADE 在排序损失外加 FLOPS 正则（batch 内每词项平均激活的平方和），尤其惩罚「热门词到处亮」（posting list 太长、检索时扫描贵）：

```text
L = L_rank + λ_q·L_FLOPS(query) + λ_d·L_FLOPS(document)
```

于是训练是拉锯——排序损失想多点亮词以提高 query/doc 重叠，FLOPS 正则把无用的 `s_ij` 推成负数、越过 0 后被 ReLU 精确置零、倒排索引彻底不存它。**稀疏度是「排序有用性 × 线上 posting 成本」两股力平衡出来的，不是 log 压出来的**（log(1+x) 对任何正数仍为正，只压幅度不造零；精确的零来自 ReLU 与稀疏正则）。

### 又一处「训练代理 vs 真实使用」错位

FLOPS 正则把「少扫 posting list」写进训练，但线上真正决定延迟的是硬件、压缩格式、缓存命中与 P99——**训练代理目标（低 FLOPS）与真实执行成本（低延迟）并不恒等**。这正是本页下一节那处「semantic-similarity 训练目标 vs retrieval-relevance 使用目标」错位在**效率轴**上的孪生：一处落在相关性轴（dense 按语义相似训练、当检索相关用，于是认错实体），一处落在效率轴（按 FLOPS 训练、当真实延迟用，于是可能「FLOPS 看着低、检索却不快」，形同 reward hacking）。两者共享同一副骨架——**一旦用代理目标训练，就得防它和真实目标分道扬镳**，与 [[benchmark-evaluation]]「你的目标是从哪个分布定义的」同源。这也把稀疏检索的效率账，从「怎么调稀疏度」抬成「训练分布↔使用分布是否对齐」的可靠性问题。

## 稀疏 vs 密集检索

| 维度 | 稀疏检索 (SPLADE) | 密集检索 ([[dense-passage-retrieval]]) |
|-----|-------------------|-------|
| 表示维度 | ~30K（词汇表大小） | 768/1024 |
| 索引 | 倒排索引 | ANN 索引 (HNSW/IVF) |
| 可解释性 | 高（可看到哪些词被匹配） | 低 |
| 精确匹配 | 强 | 弱（实体名等） |
| 语义匹配 | 中等（通过扩展） | 强 |
| 推理速度 | 快（Lucene 优化） | 中等 |
| 零样本泛化 | 中等 | 较弱 |

## 在 RAG 中的应用

在 [[retrieval-augmented-generation]] 系统中，最佳实践是稀疏+密集**混合检索**（Hybrid Retrieval）：
- 稀疏分支（BM25/SPLADE）处理关键词精确匹配
- 密集分支（DPR/E5/BGE）处理语义相似度
- 通过 RRF（Reciprocal Rank Fusion）或线性加权融合结果

这正是 [[colbert-retrieval]] 之外的另一种"两全其美"方案。

## 从「过早聚合」看稀疏检索：给否决型信号留独立账目

把 SPLADE/BM25 放到「过早聚合」这条轴上，会得到一个比"精确匹配强"更结构化的解释 [[2026-07-25-aggregation-erases-minority-signals]]：

[[dense-passage-retrieval|Dense 单向量]]在**检索前**就把整句压成一个点，实体名这类低频高信息 token 的贡献被话题语义淹没，而点积又允许"实体维少掉的分被话题维补回来"——于是"苹果营收"召回"微软营收"。SPLADE 的词表维相当于**给否决型信号留一个独立账目**：实体的字面命中落在它自己的一维上，不必先并进整体语义方向，因此不容易被话题相似度补偿掉。这也是它在上表"精确匹配"一栏对 dense 占优的机制根因——不是"匹配更准"，而是**把聚合推迟、让实体维单独结算**。

但要点是：推迟聚合 ≠ 永不聚合。SPLADE 的最终相关性仍是所有词表维上的**求和**，若其他词项分数足够多，实体错配仍可能被补偿。真正需要"实体错即淘汰"的硬约束场景，还得在稀疏召回之外叠 lexical filter / entity linker / metadata 约束兜底——稀疏检索给了实体一个独立发言的维度，但没有把它升级成不可协商的一票。

这条"哪一步聚合、就决定哪种信号被抹掉"的轴，把稀疏检索、[[colbert-retrieval]] 的 MaxSim（逐 token 独立验收）与评测端的 worst-group / slice 指标串成同一病灶（[[benchmark-evaluation]]）的三处同构修法：编码/检索端保留局部维度、评测端保留数据切片，最后都按真实业务风险而非样本频率再聚合。

## 稀疏检索是「实体 mismatch 三处修法」里的第一处

上一节从「过早聚合」解释了稀疏检索为何在实体上占优；换到「补哪一环」这根轴，稀疏 exact-match 是补回实体信号的**三处协同修法中的第一处——补在词表层**（[[2026-07-22-embedding-entity-mismatch]] 把这套修法拆全）：

| 修法 | 补在链条哪一环 | 机制 | 页面 |
|------|--------------|------|------|
| **稀疏 exact-match（本页 SPLADE/BM25）** | **词表层（召回前）** | 专名落在自己的一维、字面命中当身份锚，混合检索里给 dense 兜底 | 本页 |
| late interaction MaxSim | 检索时匹配层 | 保留每 token 向量、逐 token 验收，实体 token 不被 pooling 抹掉 | [[colbert-retrieval]] |
| entity-aware 难负例 | 训练目标层 | 「只换实体」的难负例逼模型学到「换个实体即负样本」，改写相似性边界 | [[text-embedding]] |

三处各补一环、互不替代：训练侧难负例改的是 dense 自身的相似性边界（治本但吃数据与算力），词表层与检索时两处是「不改 dense、外挂一个对实体更硬的通道」（治标但即插即用）。生产 RAG 常把词表层这一处与 dense 做混合检索（RRF/加权），正是让稀疏分支当**身份锚**、dense 分支当**语义召回**。

**为什么稀疏分支能当身份锚，根子在一处「训练目标 vs 使用目标」的错位**：dense embedding 通常被对比学习训练去逼近 **semantic similarity**（两段话在不在谈相近的事），却被系统当 **retrieval relevance**（这段话答不答得了这个具体查询）来用——两个目标恰在实体敏感的查询上分道扬镳，于是"营收下降"的话题相似度盖过"哪家公司"的身份差异。这本质是一次**训练分布与使用分布的错位**（呼应 [[benchmark-evaluation]]「你的目标是从哪个分布定义的」）。稀疏 exact-match 没有这道错位：BM25 的词频统计压根不学「语义相似」这个会漂移的目标、SPLADE 的命中也锚在词表面形上，实体的字面在不在文档里是个可验证的硬事实、不靠一个可能训偏的语义方向来代理——这才是它对 dense「治本前先兜底」的结构性理由，而非简单的"匹配更准"。

## 与 [[text-embedding]] 的关系

现代 embedding 模型如 BGE-M3 已内置多路检索能力：Dense + Sparse + ColBERT 三合一，模糊了稀疏/密集的边界。Qwen3-Embedding 同样支持稀疏向量输出。

## 伴读来源

- [[2026-07-15-splade-learned-sparse-retrieval]] — SPLADE 把语义投回 30K 维词表、继续用倒排索引检索（「表示放哪、用谁检索」这根分界轴）
- [[2026-07-19-splade-mlm-head-term-scoring]] — 一个词项权重的完整来历：`w_i=max_j log(1+ReLU(s_ij))` 三闸、为什么不是概率、FLOPS 正则如何造稀疏、FLOPS 代理↔真实延迟错位
- [[2026-07-22-embedding-entity-mismatch]] — 实体 mismatch 三处修法（词表层 exact-match / late interaction / entity-aware 难负例）、semantic-similarity 与 retrieval-relevance 的训练-使用目标错位
- [[2026-07-25-aggregation-erases-minority-signals]] — 「过早聚合抹掉少数信号」这根轴，稀疏词表维=给否决型信号留独立账目
