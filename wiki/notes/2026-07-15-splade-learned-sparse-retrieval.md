# 伴读：SPLADE——把“查询扩展”学进 30K 维词表

> 本次命中：**RAG / 检索 / Embedding 主线**；直接回应你对 SPLADE 的请求，并递进前天的 InfoNCE/dense 讨论：dense 与 sparse 的关键分界，不是“有没有语义”，而是**语义最后被放进什么坐标系、交给什么索引检索**。

材料：Formal et al., *SPLADE v2: Sparse Lexical and Expansion Model for Information Retrieval*, arXiv:2109.10086。

## 全局地图

### 一句话摘要

SPLADE 用 BERT 理解上下文，却不把整段压成一个不可读的稠密向量；它把理解结果“翻译”回 30,522 维 WordPiece 词表，只激活少数词及其权重，于是既能学习语义扩展，又能继续使用倒排索引做精确匹配。

### 结构地图

```text
传统 BM25
原文词项 -> 词频/IDF 权重 -> 稀疏词表向量 -> 倒排索引
   |
   | vocabulary mismatch：query 与 document 意思相近但用词不同
   v
SPLADE
上下文 token -> BERT -> MLM head 对整张词表打分
                         |
                         +-- 原词重加权
                         +-- 激活未出现但语义相关的词（扩展）
                         v
                 稀疏词表向量 -> 倒排索引

Dense retriever（对照）
整段文本 -> encoder -> 低维稠密隐空间 -> ANN 向量索引
```

### 段落分类概览（Agent 判断，可覆盖）

- `[骨]` dense / sparse 真正的分界：坐标系与检索器
- `[骨]` SPLADE 如何把上下文投回词表
- `[肌]` 一个查询扩展的直觉例子
- `[骨]` 为什么“稀疏”必须进入训练目标
- `[骨]` SPLADE v2 的三项改进
- `[肌]` 论文结果与边界
- `[骨]` 在 RAG 中何时选 SPLADE、dense 或 hybrid

## 第一段 `[骨]`：先拆掉一个误区——sparse 不等于“没有语义”

最容易把检索方法分成：

```text
sparse = 关键词匹配、没有语义
 dense = embedding、有语义
```

这条分法对 BM25 尚可，对 SPLADE 已经失效。SPLADE 同样用预训练 Transformer 理解上下文；它与 dense retriever 的真正区别，是**最终表示的坐标轴**。

```text
Dense：
文本 -> [0.12, -0.37, 0.08, ...]
        每一维是模型学出的潜在方向，人通常说不清其含义

SPLADE：
文本 -> {"retrieval": 2.1, "search": 1.4, "document": 0.8, ...}
        每一维直接对应 BERT 词表中的一个 WordPiece
```

Dense 把语义压进几百到几千个**潜在坐标**，再用 ANN（approximate nearest-neighbor，近似最近邻）找几何上接近的向量。SPLADE 把语义展开到 30,522 个**词汇坐标**，但只保留少数非零项，再用倒排索引找共享词项。

论文原文把目标说得很清楚：

> **Original:** “learning sparse representations for documents and queries, that could inherit from the desirable properties of bag-of-words models such as the exact matching of terms and the efficiency of inverted indexes.”
>
> **直译（信）：** 学习文档和查询的稀疏表示，使其能够继承词袋模型的理想性质，例如词项精确匹配和倒排索引的效率。
>
> **意译（达）：** 保留 BERT 的理解力，但让检索引擎最终仍看到“哪些词、各有多重要”，而不是一团只能做向量距离的隐空间坐标。

**结构标注：核心概念换轴。** sparse / dense 不是语义能力的二分，而是“语义落在哪套基底上”的二分。

### 碰撞 1

如果一个词表维度是由神经网络根据上下文激活的，它仍然算“关键词检索”吗？

更准确的说法是：**SPLADE 做的是 learned lexical retrieval（学习式词汇检索）**。匹配发生在词汇坐标上，但哪些词该出现、权重多大，是模型从数据中学出来的。

## 第二段 `[骨]`：SPLADE 的核心动作——让每个位置对整张词表“联想”

给定一段文本，BERT 先为第 i 个输入 token 产生上下文表示 hi。然后复用 masked language model head（MLM head，掩码语言模型预测头），对词表中每个词 j 计算一个分数：

```text
wij = MLM-logit(hi, vocabulary-term j)
```

这一步可以理解为：**站在当前上下文位置，词表里的每个词有多可能、或多相关？**

例如原文出现 `car`，在合适上下文里，MLM head 可能同时给这些词正分：

```text
car         高分  <- 原词重加权
vehicle     高分  <- 语义扩展
automobile  中分  <- 语义扩展
engine      中分  <- 相关概念
banana      负分  <- ReLU 后归零
```

SPLADE 对负分做 ReLU，再用 `log(1 + x)` 压缩过大的正分，最后沿输入位置聚合。v2 的默认做法是 max pooling：

```text
w_j = max over input positions i of log(1 + ReLU(w_ij))
```

于是整段文本得到一个 30,522 维向量 w；其中绝大多数维度为 0，少数维度对应被保留的词项及权重。

首次出现的两个关键术语：

- **Expansion（扩展）**：激活原文中没出现、但可弥合 query-document 用词差异的词。
- **Term weighting（词项加权）**：重新判断原文已有词在当前上下文中有多重要。

SPLADE 把两件事放进同一个算子：MLM head 既能“补词”，也能“调权”。

**结构标注：机制骨架。** BERT 负责理解，MLM head 负责把理解结果投影回可索引的词表。

### 点睛：这里不是把 MLM 的概率直接当检索概率

MLM 预训练原本回答“遮住的位置最可能是什么词”；SPLADE 借用它的词表投影层和语言先验，再通过检索排序目标端到端微调。最终分数应理解为**检索词项权重**，不是严格校准的补词概率。

## 第三段 `[肌]`：它如何解决 vocabulary mismatch？

假设查询与文档分别是：

```text
query:    treatment for a heart attack
文档原文: managing myocardial infarction
```

BM25 看到的共享实词可能很少：`heart attack` 与 `myocardial infarction` 字面不重合。

SPLADE 可以在两侧产生扩展：

```text
query representation:
{heart, attack, treatment, myocardial, infarction, ...}

文档 representation:
{managing, myocardial, infarction, heart, attack, treatment, ...}
```

两者仍然通过词表维度的点积打分：

```text
score(q, d) = sum over vocabulary j of w_qj * w_dj
```

只要某个词在 query 和 document 两个稀疏向量中都非零，它就贡献分数。倒排索引只需为非零词项保存 posting list（倒排表）。

注意：上例只是解释机制的示意，不代表具体 checkpoint 必然给出这些词或权重。真实扩展由训练数据、模型初始化、正负样本与稀疏正则共同决定。

**以上一段在支持第二段：** 查询扩展不是预先写好的同义词表，而是上下文化、任务驱动的词表激活。

## 第四段 `[骨]`：为什么不能让模型尽情扩展？

如果只优化相关性，最安全的策略可能是给每段文本激活大量相关词。召回或许上升，但每个词的 posting list 变长、每个 query 激活词变多，倒排索引会逐渐失去速度优势。

```text
扩展太少 -> vocabulary mismatch 仍在 -> 漏召回
扩展太多 -> posting lists 爆炸      -> 延迟和索引体积上升
```

所以 SPLADE 的完整目标不是单一 ranking loss，而是：

```text
L_total = L_rank
        + lambda_q * L_sparse(query)
        + lambda_d * L_sparse(document)
```

`L_rank` 在论文中是你已经见过的 in-batch contrastive loss：给定 query，让正文档在正样本、hard negative 和 batch negatives 中取得更高 softmax 概率。也就是说，它与 7 月 13 日那篇 InfoNCE 伴读属于同一骨架。

稀疏侧使用 FLOPS regularizer。它不只惩罚“非零项总数”，还近似惩罚一个词在 batch 中被普遍激活的程度；高频激活会被平方放大：

```text
L_FLOPS = sum over term j of (average activation of term j)^2
```

直觉是：

```text
只做 L1：少开几个词就行，可能大家都挤到同一批热门词
FLOPS：  还要避免热门维度形成超长 posting lists
```

这比“向量有多稀疏”更接近真正的线上成本，因为倒排检索慢不慢，还取决于非零项是否集中在少数高 document-frequency 词上。

论文还给 query 与 document 分别设置 `lambda_q`、`lambda_d`。原因是二者成本结构不对称：文档表示可离线编码和建索引，而查询每次在线到来；query 激活更多词，就要在线访问更多 posting lists。

**结构标注：效率不是部署后的补丁，而是训练目标的一部分。** SPLADE 学的不只是“相关性表示”，而是“在倒排引擎预算下的相关性表示”。

### 碰撞 2

如果两个模型 nDCG 相同，但一个平均每个 query 激活 20 个词，另一个激活 200 个词，它们是同一个质量的 retriever 吗？

离线榜单上可能是；在线系统里不是。SPLADE 强迫我们把检索目标写完整：

```text
质量 + 延迟 + 索引体积 + 吞吐
```

## 第五段 `[骨]`：SPLADE v2 改了什么？

论文的主线不是第一次提出 SPLADE，而是改进三个环节。

### 1. Sum pooling 改成 max pooling

原版把不同输入位置对同一词 j 的贡献相加；v2 取最大值。

```text
sum：多个位置反复联想到同一词，权重会累积
max：保留最强的那次语义证据
```

max 更像在问：“整段里，哪个位置最有力地支持激活这个检索词？”论文实验中，SPLADE-max 相比原 SPLADE 在 MS MARCO MRR@10 从 0.322 提到 0.340，在 TREC DL 2019 nDCG@10 从 0.665 提到 0.684。

### 2. SPLADE-doc：只扩展文档，不扩展查询

它让 query 保持原始词项，分数变成：

```text
score(q, d) = sum over terms j appearing in q of document_weight_j
```

这样 query 侧无需运行 BERT，所有昂贵编码都可离线完成；代价是 query 端不能主动扩展。它回答了一个工程问题：**如果在线延迟比极致效果更重要，语义扩展能否全部“烘焙”进文档索引？**

### 3. Hard negatives + cross-encoder distillation

DistilSPLADE-max 用 SPLADE 挖更难的负样本，再让 cross-encoder teacher 为正负文档打分，用 Margin-MSE 学 teacher 的分差。

这正好接回你之前的判断：

```text
InfoNCE / ranking loss：主要教“谁应该赢”
Margin-MSE distillation：进一步教“应该赢多少”
```

SPLADE v2 的提升不应全部归功于“稀疏表示”这个架构标签；负样本质量、教师信号和 pooling 同样关键。

**结构标注：论文贡献拆解。** 表示形式决定可用的索引，训练配方决定这个表示到底能有多好。

## 第六段 `[肌]`：结果说明了什么，又没说明什么？

论文 2021 年的主要结果：

| 模型 | MS MARCO MRR@10 | TREC DL 2019 nDCG@10 |
|---|---:|---:|
| BM25 | 0.184 | 0.506 |
| SPLADE | 0.322 | 0.665 |
| SPLADE-max | 0.340 | 0.684 |
| SPLADE-doc | 0.322 | 0.667 |
| DistilSPLADE-max | 0.368 | 0.729 |

在论文使用的 BEIR 子集上，DistilSPLADE-max 平均 nDCG@10 为 0.500；表中 ColBERT、BM25、TAS-B 分别为 0.455、0.440、0.435。它说明词汇坐标并未阻止模型获得强语义泛化，至少在当时这组零样本评测中表现很强。

但不要把表读成“SPLADE 永远胜过 dense”：

- 这是 2021 年模型和基线的时间切片，不覆盖后来的 dense / multi-vector 模型。
- ANN 与倒排索引的真实延迟都依赖实现、硬件、语料规模、过滤条件和目标 recall。
- 论文的 FLOPS 是代理指标，不等于生产引擎的实测 P95/P99 延迟。
- SPLADE 的词表可解释性强于 dense，但 WordPiece 碎片、错误扩展和领域偏差仍会让解释失真。

**结构标注：证据与边界。** 结果支持“learned sparse 可以兼得语义与倒排”，不支持“表示形式单独决定胜负”。

## 第七段 `[骨]`：在 RAG 中，dense、SPLADE、hybrid 各把语义放在哪一层？

```text
BM25
语义主要留给：用户措辞、文档措辞、人工同义词规则
索引看到：      原始词项
优势：          精确、便宜、成熟
风险：          vocabulary mismatch

SPLADE
语义主要放在：encoder + MLM head 产生的词汇扩展
索引看到：      学出来的词项与权重
优势：          语义扩展 + 倒排索引 + 可检查词项
风险：          索引膨胀、热门扩展词、领域错配

Dense
语义主要放在：encoder 的潜在几何空间
索引看到：      稠密向量
优势：          跨措辞匹配、整体语义压缩
风险：          精确实体/编号可能丢失，解释较弱，ANN 有近似误差

Hybrid
语义放在：      词汇空间和潜在空间两边
融合发生在：    分数级或排序级
优势：          两类召回信号互补
风险：          成本更高，融合权重与校准更复杂
```

一个实用选择框架：

1. **实体名、产品码、错误码、法律条款号非常关键**：先确保 lexical 通道，BM25 或 SPLADE 不宜缺席。
2. **query 与文档措辞差异大、自然语言改写多**：dense 或 SPLADE 都可能补 vocabulary mismatch。
3. **已有成熟倒排基础设施，希望保留过滤、posting-level 优化与可解释调试**：SPLADE 很有吸引力。
4. **语料频繁更新**：SPLADE 文档编码成本高于 BM25；要把重建或增量索引成本算进闭环。
5. **线上容错要求高**：hybrid 往往比押注单一路径稳，但必须用消融证明新增通道带来的 recall 值得额外成本。

## 旁逸：SPLADE 与可学习编译器是同一个形状

这里的结构像“先用高级表示理解，再编译到既有执行引擎的指令集”：

```text
BERT 上下文表示 = 高级中间表示
词表稀疏向量   = 倒排引擎可执行的指令
倒排索引       = 成熟执行后端
```

SPLADE 没有抛弃几十年优化过的 inverted index，而是学习如何把语义“编译”成它能执行的形式。这个视角也解释了它的局限：编译目标受词表限制，词表里难以表达的概念只能靠若干词项近似。

## 今日收束

把整篇压成一句可复用的话：

> **Dense 把语义压进不可命名的低维坐标，再做几何近邻；SPLADE 把语义展开回可命名的高维词表坐标，再做倒排匹配。两者都能学习语义，只是把语义放在不同层，并把执行交给不同检索器。**

以后看到“sparse embedding”时，先问四件事：

```text
1. 坐标轴是什么？词表维度，还是无名 latent dimension？
2. 非零项从哪来？原词、规则扩展，还是模型学习？
3. 稀疏如何约束？只看 L1，还是直接逼近 posting / FLOPS 成本？
4. 最终谁来检索？倒排索引、稀疏向量引擎，还是 ANN？
```

## 留给你的碰撞

假设 SPLADE 给一篇医学文档扩展出了 `heart attack`，但原文只有 `myocardial infarction`：这条可解释的词项究竟是**证据**，还是只是模型为了召回学出的**路由标签**？

如果生成模型后来引用该文档，我们能否把 SPLADE 的扩展词当成文档真的说过的话？不能。它适合解释“为什么被召回”，不等于解释“文档提供了什么事实”。

## 读后一句话（留给你）

读完后，你最想对作者说的一句话是什么？不要复述“SPLADE 是 learned sparse retrieval”，而是判断：**把语义投回固定词表，究竟是保住了可解释性，还是只把 latent space 换成了一套看起来更像人话的代理坐标？**

## 终局问题

当检索模型可以偷偷给文档添加原文没有的词时，RAG 的 provenance（来源可追溯性）应该从“命中了哪些词”退回到哪一层，才能避免把**召回理由**误当成**回答证据**？

## 术语表

| 英文 | 中文 | 本文含义 |
|---|---|---|
| learned sparse retrieval | 学习式稀疏检索 | 用模型学习词表维度上的稀疏权重 |
| vocabulary mismatch | 词汇错配 | query 与相关文档语义相近但字面词项不重合 |
| MLM head | 掩码语言模型预测头 | 把上下文表示投影到完整 WordPiece 词表 |
| expansion | 扩展 | 激活输入中未出现但有助匹配的词项 |
| term weighting | 词项加权 | 学习原有或扩展词项的检索重要性 |
| inverted index | 倒排索引 | 从词项映射到包含该词项的文档及权重 |
| posting list | 倒排表 | 某个词项对应的文档列表 |
| FLOPS regularizer | FLOPS 稀疏正则 | 近似惩罚检索计算，尤其抑制普遍激活的维度 |
| max pooling | 最大池化 | 对每个词表维度保留所有输入位置中的最强证据 |
| hard negative | 难负样本 | 与 query 很像但不相关、最能提供排序梯度的文档 |
| distillation | 知识蒸馏 | 用 cross-encoder 等教师的细粒度分数训练检索器 |

## 下一步线索

下一步只需继续追一个具体问题：读 *An Efficiency Study for SPLADE Models*（SIGIR 2022）中“regularization strength 如何形成 effectiveness-efficiency Pareto frontier”的部分。不要先看新模型名，重点检查：**训练时的 FLOPS 代理指标，是否真的预测了倒排引擎上的延迟、索引大小和吞吐？**
