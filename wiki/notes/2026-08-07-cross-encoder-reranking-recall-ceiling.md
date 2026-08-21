# 伴读：Cross-Encoder 为什么更准，却不能直接替代召回？

> 本次命中：*RAG / 检索 / Embedding + 端到端闭环*；补的是“召回与精排如何分工，以及前一阶段的漏检为什么会成为后一阶段无法突破的性能上限”。

材料锚点：Reimers & Gurevych, *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*（EMNLP 2019），并把 bi-encoder / cross-encoder 放回现代 RAG 的 retrieve-then-rerank 管线里重读。

## 全局地图

### 一句话摘要

Cross-encoder 更准，是因为它让 query 与 document 的 token 在打分前充分交互；它不能替代大规模召回，是因为这种交互必须对每个 query-document 对重新计算，而 reranker 再强，也无法找回召回阶段从未交给它的文档。

### 结构地图

```text
离线阶段
  document d
      |
      v
  bi-encoder ----> doc vector ----> ANN index

在线阶段
  query q
      |
      v
  query vector ---- ANN search ----> top-K candidates
                                       |
                                  recall ceiling
                                       |
                                       v
                 [q; d1] [q; d2] ... [q; dK]
                       \    |          /
                        cross-encoder
                              |
                              v
                         reranked top-N
                              |
                              v
                           generator

两种交互时机：
  bi-encoder   : 先各自压缩，后用一个相似度交互
  cross-encoder: 先逐 token 交互，最后才压成相关性分数
```

### 段落分类概览（Agent 判断）

- `[骨]` 同一个“相关性模型”，为什么会分成 bi-encoder 与 cross-encoder
- `[骨]` cross-encoder 的精度从哪里来，计算债又从哪里来
- `[肌]` 一个多约束查询如何暴露单向量相似度的盲点
- `[骨]` 召回上限：reranker 只能重排它看见的候选
- `[骨]` 训练与评测如何让两阶段系统真正闭环
- `[筋]` 从“选更强模型”过渡到“分配有限计算”

---

## 一、[骨] 分界不在模型名字，而在 query 和 document 何时见面

先抓住两个术语。

- *Bi-Encoder（双编码器）*：query 与 document 分别编码成向量，再用点积或余弦相似度打分。文档向量可以离线计算并建索引。
- *Cross-Encoder（交叉编码器）*：把 query 与 document 作为一个联合输入，让 Transformer 的 self-attention 在两者 token 之间直接交互，最后输出一个相关性分数；它通常不产出可独立索引的文档向量。

两者都可以使用 BERT 类骨干，真正的差别是信息路径：

```text
Bi-Encoder
q -- Encoder --> u --+
                      +--> sim(u, v) --> score
 d -- Encoder --> v --+

Cross-Encoder
[CLS] q [SEP] d [SEP]
          |
          v
joint Transformer interactions
          |
          v
        score
```

bi-encoder 在见到对方之前，必须先把各自全部信息压进固定维向量。它回答的是：

> “只看各自摘要后，这两个对象是否接近？”

cross-encoder 不要求 query 或 document 先形成独立摘要。它可以在每一层注意力里追问：

> “query 的这个词，应该与 document 的哪个词对齐？这个约束是否被满足？否定词修饰了谁？”

### 原文锚点

Sentence-BERT 论文描述原始 BERT 配对计算的核心句是：

> “It requires that both sentences are fed into the network, which causes a massive computational overhead.”
>
> “它要求把两个句子同时送入网络，因此造成巨大的计算开销。”

### 直译层（信）

“同时送入”不是数据格式上的小区别，而是说：文档 d 的表示依赖当前 query q。换一个 query，就必须重新计算这个 q-d 对。

### 意译层（达）

cross-encoder 的强项与弱点来自同一件事：它拒绝提前把文档压成一个可复用的答案。正因不提前压缩，它保住了细粒度匹配；也正因不能复用，它无法廉价地扫描百万级语料。

### 结构标注

这是全文骨架：*表示能否复用*与*交互是否充分*是一组直接 trade-off，不是两个无关的工程参数。

### 碰撞问题

当你说“cross-encoder 比 embedding 模型更懂相关性”时，代价究竟是模型参数更多，还是每个新 query 都让所有 document 表示失效、必须重新做成对计算？后者才是系统级关键。

---

## 二、[骨] 更准的来源：相关性不是两个摘要的距离，而是条件化判断

考虑查询：

```text
q = “支持 CUDA 12、显存低于 16GB、可离线部署的 reranker”
```

文档 A：

```text
“该模型支持 CUDA 12，可离线部署，INT8 后占用 11GB 显存。”
```

文档 B：

```text
“该模型支持 CUDA 12，效果优秀；24GB 显卡可流畅运行。”
```

两篇文档都与“CUDA、部署、reranker、显存”处于相近主题。bi-encoder 必须把所有约束压成一个向量，再用单个相似度汇总：

```text
score_bi(q, d) = sim(E_q(q), E_d(d))
```

这里的瓶颈不只是“向量维度有限”，而是最终相似度通常是一次整体聚合。三个条件中满足两个的 B，可能因总体语义更相似而超过真正满足全部条件的 A。

cross-encoder 则近似学习：

```text
score_cross(q, d) = f([q; d])
```

因为 `f` 直接看到成对文本，它更容易表达：

```text
支持 CUDA 12?       A=yes, B=yes
低于 16GB?          A=yes, B=no
可离线部署?          A=yes, B=unclear
所有硬约束都满足?     A=yes, B=no
```

注意，这不是说 cross-encoder 天然会做符号逻辑；而是它的结构允许每个 query token 对 document token 进行条件化匹配。bi-encoder 的独立编码则必须在不知道未来查询的情况下，预先决定文档里哪些细节值得保留。

### 点睛层（雅）

这里的 *cross* 不是“跨模态”的“跨”，而是两侧 token 在编码过程中发生交叉注意力式的信息交换。它强调的是联合编码，不是模型属于某个名为 Cross 的家族。

### 结构标注

这段解释精度收益：cross-encoder 把“相关性”从静态几何距离改回“给定这个 query，document 是否满足这些具体要求”的条件判断。

### 注疏：与 Late Interaction 是同一根轴上的不同落点

ColBERT 的 late interaction 不是另一个世界的方法，而是 bi-encoder 与 cross-encoder 之间的折中：

```text
交互更早、更充分、更贵
Cross-Encoder
      |
      |  joint token interactions through Transformer layers
      |
Late Interaction / ColBERT
      |  独立编码，但保留 token vectors，检索时做 MaxSim
      |
Bi-Encoder
      |  独立编码，每侧压成 single vector，只做一次 sim
      v
交互更晚、更受限、更便宜
```

它们都在回答同一个问题：*你愿意在多早的时候丢掉细粒度信息，以换取多大的可索引性？*

---

## 三、[肌] 计算债：为什么不能让 cross-encoder 扫全库

Sentence-BERT 用一个极端但清楚的数字说明问题：在 10,000 个句子里寻找最相似句对，cross-encoder 式逐对比较约需 5,000 万次推理，论文估计约 65 小时；把句子先独立编码后，向量相似度计算则可降到秒级。

对 RAG 查询，复杂度的形状是：

```text
语料文档数 = N
候选数     = K, 且 K << N

Cross-Encoder 全库扫描：N 次昂贵联合前向 / query
两阶段系统：
  1. ANN / lexical retrieval 找 K 个候选
  2. Cross-Encoder 做 K 次联合前向 / query
```

假设知识库有 1,000,000 篇文档，reranker 每个 query 只处理 100 篇：

```text
全库逐对计算 : 1,000,000 pairs
候选后精排   :       100 pairs
缩减倍数     :    10,000 x
```

真实延迟还受序列长度、batching、GPU 和模型大小影响，但数量级差异已经说明架构为何必须分层。

更重要的是，document embedding 可以离线计算：

```text
文档更新时：付一次编码成本
用户查询时：只编码 query + ANN 搜索
```

cross-encoder 的 document 表示依赖当前 query，无法以同样方式预计算完整相关性。

以上三段在支持第一节的论证：bi-encoder 的价值不只是“稍快”，而是把在线计算从“随全库 N 线性增长”改造成“索引搜索 + 随候选 K 增长”。

---

## 四、[骨] 召回上限：精排能改顺序，不能复活缺席者

设某个查询真正需要的证据集合是 R，召回阶段给 reranker 的候选集合是 C_K。

候选召回率是：

```text
Recall@K = |R intersect C_K| / |R|
```

reranker 无论多强，输出都只能来自 C_K。若关键文档 `d*` 不在候选里：

```text
d* not in C_K
=> reranker cannot score d*
=> d* cannot enter top-N
=> generator cannot read d*
```

所以两阶段系统有一个硬上限：

```text
最终 evidence recall@N <= 候选 evidence recall@K
```

这是集合约束，不取决于 reranker 多聪明。

### 一个容易误判的离线实验

你可能观察到：

```text
reranker 加入前 MRR = 0.42
reranker 加入后 MRR = 0.68
```

然后得出“瓶颈已经从召回转移到生成”。但如果 candidate recall@100 只有 0.75，意味着至少约四分之一的目标证据根本没参加这场比赛。0.68 的排序提升可能已经接近候选上限，却不表示端到端系统足够好。

正确的诊断顺序是：

```text
1. 目标证据有没有进入 candidate set?       recall@K
2. 进入后有没有被排到 generator 可见位置?   recall@N / MRR / nDCG
3. 看见后 generator 有没有使用?             answer faithfulness / citation
```

### 最强反驳

“把 K 一直调大，不就能提高召回上限吗？”

部分成立，但不是免费午餐：

```text
K 增大
  + 候选召回通常上升
  - reranker 计算近似线性上升
  - 难负例与近重复文档增多
  - 若送入 generator 的 N 也上升，上下文噪声与成本增加
```

因此 K 不是一个越大越好的常数，而是系统在漏检成本、精排预算和尾延迟之间的决策变量。

### 压力测试

如果 relevant document 已经在 top-100，reranker 却把它从第 40 位排到第 80 位，问题不是召回；如果它从未进入 top-100，换再强的 reranker 也修不了。两种故障必须先分层，不能统称为“RAG 效果不好”。

### 结构标注

这是全文最重要的端到端约束：*下游模型的能力，只能作用于上游保留下来的信息。*

---

## 五、[骨] 训练闭环：召回器找“可能对的”，精排器学“细微差别”

两阶段系统不应把两个模型独立优化后简单拼接。它们看到的数据分布不同。

召回器面对的是：

```text
1 positive vs millions of mostly obvious negatives
```

它的首要职责是高覆盖地缩小搜索空间。训练常用对比目标：

```text
L_retriever
= -log exp(s(q,d+))
       / [exp(s(q,d+)) + sum_j exp(s(q,d_j-))]
```

reranker 面对的则是召回器已经挑出的 top-K：

```text
1 positive vs K highly confusing negatives
```

这些 negative 往往主题相同、实体相近、只差一个约束，正适合 cross-encoder 学细粒度判断。

### 为什么随机负例不够

若训练 reranker 时的负例是随机文档：

```text
q: “Python asyncio timeout 如何取消任务”
negative: “法国葡萄酒产区介绍”
```

模型只需识别主题就能获胜。但线上真正的错误候选更像：

```text
negative 1: asyncio timeout，但没有取消 pending task
negative 2: 取消 task，但示例针对 thread 而非 coroutine
negative 3: API 已被新版本弃用
```

因此有价值的 hard negatives 应来自实际召回器，尤其是“retriever 高分但人工判断不相关”的候选。这样训练分布才与部署分布相接。

### 偏差如何反向传导

闭环如下：

```text
retriever 当前偏好
      |
      v
产生 top-K 与 hard negatives
      |
      v
训练 reranker 的判别边界
      |
      v
决定哪些结果被用户看见/点击
      |
      v
新日志再训练 retriever 与 reranker
```

若初始 retriever 系统性漏掉某类文档，那类文档既进不了 reranker，也很难成为线上反馈中的正例。上游召回偏差会通过数据采样被固化。

修法不是只换 loss，而是主动打破闭环：

- 合并 BM25、dense、规则检索等多路候选，提高训练候选多样性；
- 从未命中 slice 中人工或程序化补正例；
- 用 teacher cross-encoder 蒸馏 retriever，但同时保留独立召回评测；
- 按实体、时间、语言、长文档、多跳查询分层监控 recall@K。

### 结构标注

这是“端到端闭环”的训练版：部署时的 candidate distribution 应进入训练设计，否则 reranker 学会的只是实验室里的排序题。

---

## 六、[筋] 真正的问题不是选谁，而是把计算花在哪些 pair 上

作者从 BERT 成对计算的昂贵，走向 Sentence-BERT 的可复用向量。现代 retrieve-then-rerank 又把部分成对计算请回来，但只花在最值得判断的 K 个候选上。

所以两阶段系统不是妥协式拼装，而是计算资源分配：

```text
便宜模型看全库：追求别漏
昂贵模型看小集：追求别排错
生成模型看更小集：追求读懂并忠实回答
```

昨天的 hybrid retrieval 解决“哪些候选有资格进场”；今天的 cross-encoder 解决“进场后谁真正满足 query”。二者之间的接口不是一个 top-K 文件，而是一条性能上限。

---

## 全文复盘

### 理解轨迹

```text
“cross-encoder 更准，所以直接替代 embedding 检索”
                       |
                       v
更准来自联合编码：query-token 与 document-token 充分交互
                       |
                       v
同一原因导致不可复用：每个 q-d pair 都要重新前向
                       |
                       v
bi-encoder 扫全库，cross-encoder 只精排 top-K
                       |
                       v
reranker 的输出集合被 candidate set 硬性限制
                       |
                       v
先诊断 recall@K，再诊断 rerank，再诊断 generation
                       |
                       v
训练 hard negatives 必须来自真实候选分布
```

### 你应该带走的三个判断

1. *结构判断*：bi-encoder 与 cross-encoder 的根本差异，是交互发生在压缩之前还是之后。
2. *系统判断*：reranker 提高的是候选集内部的排序质量，不直接提高候选集外的覆盖。
3. *闭环判断*：召回器生成的候选分布同时决定 reranker 的推理上限与训练难度。

### 读后一句话（不可跳过）

读完后，请你最想对这套两阶段架构说的一句话留在这里。不要复述“一个快、一个准”；试着判断：*你的系统当前更可能在候选进入前丢信息，还是在候选进入后排错？你凭什么证据这么判断？*

### 终局问题

如果每个 query 的难度不同——有的 top-10 已经足够，有的 top-500 仍漏证据——固定 K 是否本身就是一种过早聚合？系统能否根据召回分数间隔、多路一致性或 query 类型，动态决定“还要不要继续找”和“值得给 reranker 多少计算预算”？

### 术语表

| English | 中文 | 本文含义 | 出现位置 |
|---|---|---|---|
| Bi-Encoder | 双编码器 | 独立编码 query/document，产生可索引向量 | 第一节 |
| Cross-Encoder | 交叉编码器 | 联合编码 q-d pair，输出相关性分数 | 第一、二节 |
| Joint Encoding | 联合编码 | 两侧 token 在编码层中直接交互 | 第一节 |
| Candidate Set | 候选集 | 召回阶段交给 reranker 的 top-K 文档 | 第三、四节 |
| Recall Ceiling | 召回上限 | 下游输出受候选集合覆盖率硬约束 | 第四节 |
| Hard Negative | 难负例 | 与 query 很像但不满足真实相关条件的负样本 | 第五节 |
| Retrieve-then-Rerank | 先召回后精排 | 便宜全库搜索与昂贵局部判断的组合 | 全文 |

### 下一步线索

沿终局问题继续推进，最直接的切面不是再读一篇“更强 reranker”，而是研究 *adaptive retrieval / dynamic top-k*：先看“置信度能否决定是否继续检索”，再把它与 Self-RAG 的 reflection token 对照。前者动态分配搜索预算，后者动态决定是否需要外部证据；二者都在把固定管线改成可决策动作。
