#+title: 伴读：SPLADE 的 MLM head 到底怎么给一个词打分
#+date: [2026-07-19 Sun 09:02]
#+filetags: :reading:rag:retrieval:splade:
#+identifier: 20260719T090214
#+source: Formal et al., SPLADE v2 (arXiv:2109.10086)；DistilSPLADE

* 命中点

本次命中 *RAG / 检索 / Embedding 主线*，直接回答你对 07-15 伴读的追问：不再停在“SPLADE 把语义投回 30K 词表”，而是逐层拆开 *一个词项的检索权重究竟怎样从 MLM logit 算出来*。

* 全局地图

** 一句话摘要

SPLADE 让每个输入位置都对整张词表产生一组未归一化 logit，再依次经过 `ReLU -> log(1+x) -> 跨位置 max`，把“某个位置曾强烈点亮词项 i”变成整段文本在词项 i 上的非负权重；排序损失决定点亮什么，FLOPS 正则决定别点亮太多。

** 结构地图

#+begin_example
输入 token 序列
      |
      v
BERT：每个位置得到上下文化表示 h_j
      |
      v
MLM head：每个位置 j 输出 30,522 个 logits s_ij
      |
      +-- ReLU：负 logit -> 0
      +-- log(1+x)：压缩正 logit
      +-- max over j：每个词项只留最强位置
      v
整段文本的 30,522 维非负向量 w_i
      |
      +-- ranking loss：相关 query/doc 的共享词项权重大
      +-- FLOPS regularizer：大部分维度保持 0
      v
query/document 稀疏点积 -> 倒排索引检索
#+end_example

** 段落分类（Agent 判断，可覆盖）

- [骨] MLM head 输出的不是“输入 token 的一个分数”，而是每个位置对全词表的一排分数
- [骨] 从隐藏状态到词表 logit 的具体投影
- [骨] `ReLU -> log1p -> max` 三步各自在解决什么
- [肌] 一个带数字的手算例子
- [骨] 为什么这些 logit 不是 MLM 概率
- [骨] FLOPS 正则怎样让 30K 维真正稀疏
- [肌] 反向传播如何把“完形填空头”改造成“检索词项头”
- [骨] 工程上怎样解释和调试一个 SPLADE 权重

* 逐段伴读

** 第一段：[骨] 先纠正问题的主语：不是“给输入 token 打一个分”

*** 原文锚点

论文的核心表示可以写成：

#+begin_example
w_i = max_j log(1 + ReLU(s_ij))
#+end_example

其中：

- `j` 是 *输入位置*，例如句子中第 3 个 WordPiece；
- `i` 是 *词表词项*，例如词表中的 `heart`、`myocardial` 或 `banana`；
- `s_ij` 是位置 `j` 对词项 `i` 的原始 MLM logit；
- `w_i` 才是整段文本最终在词项 `i` 上的检索权重。

所以，MLM head 不是给每个输入 token 吐一个标量，而是给 *每个位置吐一条约 30K 维向量*：

#+begin_example
                 vocabulary dimension i
               heart  myocardial  attack  banana  ...
position j=1     ...      ...       ...     ...
position j=2     ...      ...       ...     ...
position j=3     ...      ...       ...     ...
#+end_example

若输入长度为 `L`，中间张量大致是 `L x |V|`；随后沿 `L` 个位置聚合，才得到长度为 `|V|` 的文本向量。

*** 结构标注

核心概念澄清：SPLADE 的基本打分对象是“*位置 j 对候选词项 i*”这对关系，不是输入 token 本身。

*** 注疏

把它想成一场有 `L` 位证人的听证会：每个位置都可以为 30K 个候选词作证；最终每个词项只采纳最有力的那位证人。这里“证人”是上下文化位置，不必与候选词字面相同。

*** 碰撞

如果输入里根本没有 `myocardial`，它凭什么得到分数？

因为位置表示 `h_j` 已看过整段上下文。输入中的 `heart attack` 可以让某个位置的上下文化表示落到接近词表向量 `myocardial` 的方向，于是该词得到正 logit。这就是 expansion（扩展），不是查同义词表。

** 第二段：[骨] logit 是怎样从 BERT 隐状态里出来的

*** 机制拆解

对位置 `j`，BERT 先产生上下文化隐藏状态 `h_j`。BERT 类 MLM head 通常先做一层变换，再投影到词表：

#+begin_example
z_j    = LayerNorm(GELU(W h_j + b))
s_ij   = e_i^T z_j + b_i
#+end_example

这里：

- `z_j` 是为词表预测加工后的上下文向量；
- `e_i` 是词表中第 `i` 个 WordPiece 的输出向量，常与输入 embedding 权重绑定；
- 点积 `e_i^T z_j` 衡量当前位置的上下文状态与词项 `i` 的方向有多匹配；
- `b_i` 是该词项的偏置；
- `s_ij` 是 logit（未归一化分数），可正可负。

首次出现的术语：*weight tying（权重绑定）*，指输入 token embedding 与输出词表分类器共享参数。这样“读入某个词”和“预测某个词”使用同一套词汇坐标。

07-15 那句“把语义投回词表”，现在可以展开成：

#+begin_example
上下文语义 h_j
  -> MLM transform 得到 z_j
  -> 分别与每个词表向量 e_i 做点积
  -> 得到词表坐标上的 30K 个 logits
#+end_example

*** 结构标注

机制骨架：30K 维不是凭空生成的；每一维都是上下文状态与一个可命名词表向量的匹配分数。

*** 点睛

“MLM head 复用完形填空能力”是好直觉，但不要读成“模型真的把每个位置遮住又预测一次”。SPLADE 前向时通常直接取各位置的隐藏状态过 MLM head；它借的是预训练得到的词表投影和语言先验，不需要逐位置构造 `[MASK]` 输入。

** 第三段：[骨] 三道闸门：ReLU、log1p、max

*** 第一闸：ReLU 只保留正证据

#+begin_example
r_ij = ReLU(s_ij) = max(0, s_ij)
#+end_example

负 logit 被精确砍成 0，最终可以不进入倒排表。它还保证检索权重非负，使稀疏点积更接近传统词项匹配：共享词只加分，不发生“两个负数相乘反而加分”。

但 ReLU *本身不保证足够稀疏*。若 30K 个 logits 中有一大批为正，仍会激活很多词；真正把大量 logit 推到 0 以下的是训练中的稀疏正则。

*** 第二闸：`log(1+x)` 压缩强证据

#+begin_example
u_ij = log(1 + r_ij)
#+end_example

它是单调函数，不改变同一位置上正分的大小顺序，却让边际增益递减：

#+begin_example
原始正 logit：  0.6    1.1    3.0    5.0
log(1+x)：       0.470  0.742  1.386  1.792
#+end_example

从 0 到 1 的提升很重要，从 20 到 21 的提升就很小。这样可防止少数超大 logit 垄断点积，也让权重尺度更适合检索。

*** 第三闸：跨位置 max 只留最强证据

#+begin_example
w_i = max over positions j of u_ij
#+end_example

同一个词项可能被多个位置点亮。max pooling 问的是：“整段中，哪里最强烈地支持词项 i？”只要任一位置点亮它，文本向量中的 `w_i` 就非零。

与原版 SPLADE 的 sum pooling 对照：

#+begin_example
sum pooling：多处弱证据可以累积；重复出现也会抬高权重
max pooling：只留最强证据；更像 presence + strongest support
#+end_example

*** 结构标注

核心算子：ReLU 决定“进不进索引”，log1p 决定“强分怎样压缩”，max 决定“多个位置怎样合成整段权重”。

*** 碰撞

这三步里，哪一步创造了 expansion？都不是。扩展早在 `s_ij` 的词表投影中已经发生；三道闸门只决定哪些联想能活下来，以及活下来后权重多大。

** 第四段：[肌] 手算一次：`heart attack treatment`

下面数字只用于展示算子，不代表某个真实 checkpoint 的输出。假设我们只观察三个输入位置和四个词表维度：

#+begin_example
原始 logits s_ij

input position     heart   myocardial   treatment   banana
heart               4.2       1.1          0.2       -1.3
attack              2.7       3.0          0.6       -0.8
treatment           0.5       0.9          5.0       -0.4
#+end_example

经过 ReLU，`banana` 一列全部变成 0；再做 `log(1+x)`：

#+begin_example
变换后 u_ij

input position     heart   myocardial   treatment   banana
heart              1.649      0.742         0.182      0
attack             1.308      1.386         0.470      0
treatment          0.405      0.642         1.792      0
#+end_example

最后逐列取 max：

#+begin_example
w_heart       = 1.649   <- 由位置 heart 胜出
w_myocardial  = 1.386   <- 由位置 attack 胜出，原文没出现却被扩展
w_treatment   = 1.792   <- 由位置 treatment 胜出
w_banana      = 0       <- 不进入稀疏表示
#+end_example

最终文本表示可写成：

#+begin_example
{treatment: 1.792, heart: 1.649, myocardial: 1.386}
#+end_example

以上手算段在支持第三段：所谓“一个词的 SPLADE 分数”，就是它在所有上下文位置上的最强正 logit，经压缩后的值。

** 第五段：[骨] 最容易犯的错：把 logit 当成 MLM 概率

*** 为什么不是概率

标准 MLM 会对同一位置的整张词表做 softmax：

#+begin_example
p(i | context at j) = exp(s_ij) / sum_k exp(s_kj)
#+end_example

softmax 强迫所有词竞争一份总和为 1 的概率质量。若 `heart` 概率上升，其他词的概率总和必须下降。

SPLADE 在表示层使用的是：

#+begin_example
log(1 + ReLU(s_ij))
#+end_example

这里 *没有 softmax*，各维度不需要总和为 1，多个相关词可以同时得到高权重。因此 `w_i` 不是：

- “词 i 出现在文档中的概率”；
- “把位置 j 遮住后词 i 的校准概率”；
- “文档陈述了词 i 的置信度”。

它是经过检索训练后的 *term importance weight（词项重要性权重）*。

*** 结构标注

边界澄清：MLM 初始化提供语言先验，但 SPLADE 输出是多标签式检索激活，不是单标签式补词概率分布。

*** 对手光

如果真的使用 softmax 概率，会怎样？它会制造不必要的零和竞争：一篇关于心肌梗死的文档完全可以同时强烈支持 `heart`、`attack`、`myocardial`、`infarction` 和 `treatment`。检索表示需要“一对多地点亮”，而标准补词概率要求“这个空最可能是哪一个词”。二者任务结构不同。

** 第六段：[骨] 30K 维为什么最终能稀疏：FLOPS 正则在改 logit 的符号

*** 两股相反的训练力

若只用排序损失，模型倾向多点亮一些词，以提高 query 与相关文档发生重叠的机会。SPLADE 因此加入稀疏正则：

#+begin_example
L_total = L_rank
        + lambda_q * L_FLOPS(query)
        + lambda_d * L_FLOPS(document)
#+end_example

FLOPS regularizer 的核心形状是：先计算一个 batch 中每个词项的平均激活，再平方求和。

#+begin_example
mean_i = average over batch examples of w_i
L_FLOPS = sum over vocabulary i of mean_i^2
#+end_example

它尤其惩罚“许多文本都在激活同一个词”的情况，因为这会让该词的 posting list 很长，检索时扫描代价高。

于是训练形成拉锯：

#+begin_example
ranking loss：  点亮能连接相关 query/document 的词
FLOPS penalty：别乱点；尤其别让热门词到处亮
#+end_example

ReLU 的关键作用这时才完整显现：正则不只是把正权重缩小，它会推动无用的 `s_ij` 穿过 0 变成负数；一旦越过 0，ReLU 便把该维精确置零，倒排索引可以彻底不存它。

*** 结构标注

训练闭环：激活公式提供可稀疏的门，排序目标选择有用维度，FLOPS 正则把线上 posting 成本反馈进训练。

*** 碰撞

“log 压缩使表示稀疏”对吗？不对。对任何正数，`log(1+x)` 仍为正；它只压缩幅度。精确的零来自 ReLU，而“多数值落到 ReLU 左边”主要来自稀疏正则与训练动态。

** 第七段：[肌] 梯度到底流向哪里

max pooling 还有一个不显眼但重要的后果：对每个词项 `i`，梯度主要通过获胜位置 `j*` 回传。

#+begin_example
j* = argmax_j log(1 + ReLU(s_ij))
#+end_example

以手算例子中的 `myocardial` 为例，位置 `attack` 的 3.0 胜过另外两个位置。若排序目标希望提高 `myocardial` 权重，更新会主要推动 `attack` 位置的上下文表示与 `myocardial` 的词表向量更匹配。

这解释了两点：

1. max pooling 让每个扩展词形成一个相对明确的“最强触发位置”；
2. 非获胜位置即使也给正分，通常不会从该词项的 max 路径得到梯度，学习信号比 sum pooling 更集中。

但不要把 `argmax` 位置当成因果解释。BERT 的 `h_j` 已混入全句上下文；“attack 位置触发 myocardial”只说明聚合层在此取最大，不说明模型只根据 `attack` 这个字作判断。

*** 结构标注

以上一段在补充机制：max 不只改变前向权重，也改变反向信用分配。

** 第八段：[骨] 一个权重的完整身份证

现在可以给任意 SPLADE 词项权重做六层追踪：

#+begin_example
1. 词表坐标：i 对应哪个 WordPiece？
2. 最强位置：哪个 j 产生最大 s_ij？
3. 原始 logit：s_ij 是正是负、离 0 多远？
4. 激活变换：ReLU 与 log1p 后剩多少？
5. 训练来源：ranking signal 为什么奖励这条重叠？
6. 成本约束：FLOPS 是否在压制它成为全局热门扩展？
#+end_example

在真实系统调试时，至少同时打印：

- 原始文本及 WordPiece 切分；
- 最终 top weighted terms；
- 每个 term 的 argmax 输入位置；
- query/document 的共享激活词及点积贡献 `w_qi * w_di`；
- 文档频率或 posting-list 长度。

只看 top terms 会产生一种虚假的“可解释感”：一个词看起来像人话，不代表它是原文证据。更可靠的解释是：“这个词项贡献了多少召回分，它由哪个上下文位置触发，它是否在语料中泛滥。”

*** 结构标注

工程结论：SPLADE 的可解释性应落在“召回路由可审计”，不能上升为“文档事实可证明”。

* 旁逸：这更像多标签分类，而不是完形填空

标准 MLM 的形状是：一个空位，在 30K 个候选中选最可能的少数词。SPLADE 的形状更像多标签分类：一篇文本可以同时拥有很多检索标签，每个标签有独立强度。

#+begin_example
MLM：    这个位置最可能是哪一个词？       -> softmax，词间竞争
SPLADE：整篇文本应该挂上哪些检索词？     -> 非负多维激活，可同时点亮
#+end_example

它使用 MLM head 的参数结构，却在检索微调中改变了输出的制度：从“争夺一个概率蛋糕”变成“独立决定哪些路由开关值得打开”。

* 全文复盘

** 理解轨迹

#+begin_example
07-15：SPLADE 把语义投回 30K 维词表
  |
  v
今天第一步：每个输入位置都有一整排 30K logits
  |
  v
今天第二步：logit = 上下文状态与词表向量的匹配
  |
  v
今天第三步：ReLU -> log1p -> max 生成文本词项权重
  |
  +-- 排序损失决定哪些共享词有用
  +-- FLOPS 正则推动无用 logits 过零、真正消失
  v
最终边界：权重解释“为何召回”，不证明“原文说过”
#+end_example

最该带走的不是公式外形，而是这句：*SPLADE 的稀疏权重不是 MLM 概率；它是以 MLM 词表投影为初始化、由检索目标和效率正则共同塑造的非负路由分数。*

** 读后一句话

不可跳过的一问：读完后，你最想对“MLM head 给每个 token 打一个词义分数”这句话做什么修正？

一个达到 L2 的回答应包含判断，而非只复述步骤。例如：

“不是给输入 token 一个分，而是每个上下文位置对全词表打 logits；SPLADE 再把每个词项跨位置聚合成检索权重，而且这个权重不是概率。”

** 终局问题

SPLADE 用 FLOPS 正则把“少扫 posting lists”写进训练，但线上真正关心的是硬件、压缩格式、缓存命中和 P99 延迟；当训练代理目标与真实执行成本不一致时，模型会不会像 reward hacking 一样，学出“FLOPS 看起来低、实际检索却不快”的稀疏分布？

** 术语表

| 英文 | 中文 | 本文含义 | 出现位置 |
|-
| MLM head | 掩码语言模型预测头 | 把位置隐藏状态投影到完整词表的模块 | 第二段 |
| logit | 未归一化分数 | softmax 前的词表分数；SPLADE 直接对其做稀疏激活 | 第一、五段 |
| weight tying | 权重绑定 | 输入 embedding 与输出词表投影共享参数 | 第二段 |
| ReLU | 线性整流 | 将负 logit 精确置零，提供稀疏门 | 第三、六段 |
| log1p | `log(1+x)` 变换 | 压缩正激活的动态范围 | 第三段 |
| max pooling | 最大池化 | 每个词项跨输入位置只保留最强证据 | 第三、七段 |
| expansion | 词项扩展 | 激活原文未出现但有助匹配的词表项 | 第一段 |
| term weight | 词项权重 | 文本在某词表维度上的最终非负检索分数 | 第五段 |
| FLOPS regularizer | FLOPS 正则 | 通过惩罚 batch 平均激活来近似约束倒排计算成本 | 第六段 |
| posting list | 倒排表 | 某词项对应的文档及权重列表 | 第六、八段 |

** 下一步线索

下一步只追一个具体实验：打开一个可用的 SPLADE checkpoint，对同一文本导出 `(term, final weight, argmax input position, raw logit)`，再分别提高与降低 FLOPS 正则强度，观察三件事：非零词数、热门词 posting 长度、检索质量如何形成 Pareto frontier。材料可接 *An Efficiency Study for SPLADE Models*（SIGIR 2022）中正则强度与实际效率的实验部分。
