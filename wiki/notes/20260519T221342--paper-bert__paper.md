---
title: 补全胜续写
subtitle: BERT — Pre-training of Deep Bidirectional Transformers for Language Understanding
date: 2026-05-19 Tue 22:13
tags: [paper, deep-learning, nlp, transformer, pretraining, representation-learning]
identifier: 20260519T221342
source: /Users/nolanhuang/paper_agent/wiki/raw/papers/1810.04805-BERT-Pre-training-Deep-Bidirectional-Transformers.pdf
authors: Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova
venue: NAACL 2019 (Google AI Language)
list_ref: wiki/papers-reading-list.md §一 第 2 篇
---

> *原文 PDF*：[1810.04805-BERT-Pre-training-Deep-Bidirectional-Transformers.pdf](file:///Users/nolanhuang/paper_agent/wiki/raw/papers/1810.04805-BERT-Pre-training-Deep-Bidirectional-Transformers.pdf)

* 问题

你用一句话考一个语言模型：「I cannot ___ with that statement」。它给你的答案是 *say*。语义上能说通，但你心里清楚——正确答案是 *agree*。

为什么？因为这个空填什么，必须同时看到左边的 「I cannot」 和右边的 「with that statement」。「cannot ... with」 这一对左右钳口锁住 *agree*。只看左半边的模型永远到不了那里——它只能从「I cannot」这点信号往外猜，分布散得到处都是。

2018 年 NLP 圈面对的就是这个困境。当时的预训练范式（ELMo、OpenAI GPT）都假设语言模型必须从左到右读：每个词只能根据它前面的词来预测自己。这是 *标准语言模型* 的定义——条件概率 p(w_t | w_1, ..., w_{t-1})。这个定义在数学上很干净，但在做下游任务时荒唐：你做问答（SQuAD），系统看到一个候选答案 token，理论上它最该参考的是「问题里那个特定词」和「答案后面那句解释」，可标准 LM 强迫它只能往左看。

ELMo 想了个折中：训练两个独立的单向 LM（一个左到右、一个右到左），把两个表示拼起来。但这是 *浅层拼接*——两个模型在每一层都是各看各的，到最后一层才碰头。OpenAI GPT 干脆只用左到右的 Transformer decoder。两条路都被同一个戒律捆住：标准 LM 不能双向，否则每个词在多层叠加里会绕一圈看到自己——这是个让人头大的死锁。

Devlin 他们看到的入口很直白：既然戒律是「不能让词看到自己」，那就别用语言模型这个目标。换成完形填空——把 15% 的词盖掉，让模型靠剩下 85% 来填空。这个目标天然是双向的，因为剩下的 85% 既包括左也包括右；这个目标也天然解开了死锁，因为被盖掉的词在输入端就消失了，它在多层叠加里压根没法看到自己。换一个目标，整套架构的桎梏就解了。

* 翻译

这一节带你看「I cannot [MASK] with that statement」这个具体例子怎么走完 BERT 的全流程，方法长什么样、为什么这么长。

** 锚点：BERT 是一台「填空机」加一个「插头」

把 BERT 看成两个零件焊在一起：

- 一个 *深度双向 Transformer 编码器*——12 层（BASE）或 24 层（LARGE）的 self-attention 堆叠，每个位置都能看见整句所有位置（不像 GPT 只能看左边）。
- 一个 *任务无关的输入格式*——在句首插一个 `[CLS]`、句间插一个 `[SEP]`、对每个位置加上 segment embedding（标记你属于句子 A 还是句子 B）。

预训练时，这台机器做两件事：把随机盖住的词填回来（MLM）；判断两个句子是不是连续的（NSP）。下游用时，你把它当作一个 *特征提取器*，外面只接一个极简输出层（一个 `[CLS] -> 分类标签` 的线性层，或者一个 `每个 token -> 标签` 的线性层），整体 fine-tune 几个 epoch 就完事。

整个论文的核心断言：*预训练时学到的双向表示，比下游任务从头训练任何复杂结构都强*。所以下游不需要为每个任务设计特殊架构——所有 NLP 任务塌缩成同一个模板：输入装进 BERT，输出接一个线性层。

** 第一步：把句子变成 BERT 看得懂的输入

我们的句子 `I cannot [MASK] with that statement`，先经过 WordPiece 分词成大约这样：`[CLS] i can not [MASK] with that statement [SEP]`。

每个 token 的输入向量是 *三个 embedding 相加*：

- Token embedding：词本身的查找向量
- Segment embedding：标记「我是句子 A」还是「我是句子 B」（这里全是 A）
- Position embedding：第几个位置（学到的，不是 sin/cos）

三个加起来，喂进 12 层 Transformer encoder。每一层每个位置都做一次 self-attention，所有位置互看。这点和原始 Transformer encoder 一模一样——*BERT 在架构上没有任何创新，它的革命全在「预训练目标」上*。

** 第二步：MLM 怎么训练

预训练时，对输入的 15% token 做手脚：

- 80% 的概率换成 `[MASK]`：「I cannot [MASK] with that statement」
- 10% 的概率换成 *随机词*：「I cannot apple with that statement」
- 10% 的概率 *保持原词不变*：「I cannot agree with that statement」

只有这 15% 被选中的位置参与 loss 计算——预测原词，cross entropy。其他 85% 不计 loss。

为什么 80/10/10 这种古怪比例？这是 BERT 最容易被忽视的设计选择。如果 100% 都换 `[MASK]`，模型就会偷懒：它知道「凡是没看见原词的位置一定是要预测的位置」，所以只在 `[MASK]` 处下功夫，其他位置的表示训得很糟。但 fine-tune 时输入里压根没有 `[MASK]`——*预训练和下游分布不对齐，模型会懵*。10% 替随机词逼模型对每个位置都保持警觉（你看到的词可能是错的）；10% 保留原词逼模型对每个位置都做出预测（不能仅凭「这是 `[MASK]`」就触发输出）。这样训出来的表示对所有位置一视同仁，下游没有 `[MASK]` 也能用。

** 第三步：NSP 怎么训练

输入两个句子，让 `[CLS]` 那一位的最终输出预测「B 是不是 A 的下一句」。50% 时间 B 真是下一句，50% 时间 B 是从语料里随机挑的。这是一个二分类问题。

NSP 的目的是让 `[CLS]` 学到 *句对关系*——为问答（QA）和自然语言推理（NLI）这类需要句间关系的任务做准备。

** 第四步：fine-tune 时换插头

预训练完，BERT 是一坨「会填空、会判断句对」的参数。下游怎么用？换个插头：

- *句子分类（情感、entailment）*：拿 `[CLS]` 那一位的输出，接一个 `H -> K` 线性层（K 是类别数），整体 fine-tune
- *token 级标注（NER）*：每个 token 位置接一个线性层
- *问答（SQuAD）*：引入两个向量 S（start）、E（end），每个 passage token 算 `S·T_i` 和 `E·T_i`，softmax 出起止位置

*所有任务用同一个预训练 checkpoint 初始化*——这是 BERT 最迷人的工程美学。

** 数据：差距到底有多大

| 任务 | 之前的 SOTA | BERT_BASE | BERT_LARGE |
|------|-------------|-----------|------------|
| GLUE 平均 | 75.1（OpenAI GPT） | 79.6 | *82.1*（+7.0 绝对值） |
| MNLI-m 准确率 | 82.1 | 84.6 | *86.7*（+4.6） |
| SQuAD v1.1 F1 | 91.7（集成） | 88.5 | *93.2*（单模型超集成） |
| SQuAD v2.0 F1 | 78.0 | - | *83.1*（+5.1） |

参数量：BERT_BASE 110M、BERT_LARGE 340M。BASE 故意做成和 OpenAI GPT 同等大小（12 层 768 隐藏维 12 头），目的是 *证明同等参数下双向碾压单向*——不是靠堆参数赢的。

** 反直觉副发现：双向不只是「多一倍信息」，是质变

直觉上你会想：双向 = 单向 × 2，最多线性提升。Table 5 的 ablation 给出反例：

- BERT_BASE（双向 + NSP）：MNLI 84.4 / SQuAD F1 88.5
- 同架构换成 LTR（左到右、丢 NSP，等于 GPT 复刻）：MNLI 82.1 / SQuAD F1 *77.8*

SQuAD 上掉了 *10.7 F1*。在 LTR 顶上加一个 BiLSTM 也只能补回 7 个点（到 84.9），仍远低于双向的 88.5。这不是「多一倍信息」能解释的——这是 *单向架构在 token 级任务上的根本性限制*。SQuAD 要预测答案 span 的边界，每个候选 token 必须同时看到「问题」（在它左边）和「答案后续解释」（在它右边）。你不可能靠左到右编码出一个能感知右侧上下文的 token 表示——除非你绕一大圈让 token 也看见自己（死锁）。

更反直觉的是 Section 5.2：BERT_LARGE 在 MRPC（只有 *3,600 个标注样本*）上仍能稳定超过 BERT_BASE。当时学界普遍认为「极大模型只对大数据集有意义，小数据集上反而过拟合」——BERT 第一次砸实「只要预训练充分，模型大对小数据集也是收益」。这是后来 GPT-3 in-context learning 和整个 scaling law 故事的早期前哨。

* 核心概念

回到 `I cannot [MASK] with that statement` 这个例子，下面三个零件每解开一个，例子就更清晰一层。

** MLM：把 LM 的死锁换成完形填空

*一句话*：随机盖住 15% 的词让模型填回来，是让深度双向预训练成为可能的*目标函数变换*。

*回到例子*：在标准 LM 里，「agree」这个词在第 N 层的表示，理论上可以通过多层 attention 绕回来「偷看」自己——所以必须用 mask 矩阵切断右向连接。但一旦切断，你就只能看到左半边「I cannot」。MLM 的诀窍是 *从输入端就把这个词替换掉*——模型在第 0 层看到的是 `[MASK]`，根本没机会偷看 agree。代价是只有 15% 位置参与 loss（训练效率低），收益是每一层每个位置都可以自由地双向看，没有死锁。

*为什么重要*：这是 BERT 唯一真正的创新。所有「双向预训练」的可能性都建立在「换一个目标函数」这一招上。如果你死守 LM 目标，永远走不到双向。

** 80/10/10 替换：缓解预训练-微调分布错位的设计 trick

*一句话*：被选中的 15% 里，只有 80% 真换 `[MASK]`、10% 换随机词、10% 保留原词，目的是让模型在每个位置都保持「这词可能是要预测的、可能是错的、可能是对的」三态警觉。

*回到例子*：fine-tune 时你给 BERT 的输入是 `I cannot agree with that statement`（无 `[MASK]`），它要给情感分类做特征。如果预训练时模型学的是「只对 `[MASK]` 那一位下功夫」，那 fine-tune 时所有位置都没有 `[MASK]`，模型会发现自己处在一个完全陌生的输入分布里，表示崩塌。10% 的「换随机词」和 10% 的「保留原词」是给模型打的*疫苗*——预训练时它已经见过没有 `[MASK]` 的输入了，下游切换时不应激。

*为什么重要*：很多人复述 BERT 时会跳过这个细节，但这是 MLM 能 *实际工作* 而非「理论上工作」的关键。论文 Appendix C.2 的 ablation 显示，纯 100% 替换或纯保留都会显著掉点。这是论文里少有的「我们试出来的 hack」类设计——优雅程度不及 MLM 主体，但缺了它整套范式不 work。

** 统一输入格式：[CLS] + [SEP] + Segment——一架结构通吃所有任务

*一句话*：通过在输入里硬编码三个特殊 token / embedding 类型，BERT 把所有 NLP 任务塌缩成「输入装进同一个编码器，输出接极简线性层」的统一模板。

*回到例子*：我们这个例子在 GLUE 情感分类里走的是「单句模式」：`[CLS] I cannot agree with that statement [SEP]`，最后取 `[CLS]` 那一位输出做分类。如果改做 entailment，输入变成 `[CLS] I cannot agree [SEP] You disagree [SEP]`，segment embedding 第一段全 A、第二段全 B，仍然取 `[CLS]` 做二分类。如果改做 SQuAD，输入是 `[CLS] question [SEP] passage [SEP]`，取 passage 部分 token 做 span 预测。*同一个编码器、同一套预训练参数、同一个 fine-tune 流程*。

*为什么重要*：在 BERT 之前，每个 NLP 任务都有自己的「明星架构」——QA 用 BiDAF、entailment 用 ESIM、NER 用 BiLSTM-CRF。Table 1-7 的所有 SOTA 名字都是任务专属架构。BERT 的统一格式让这些架构*成为多余*。这是 NLP 工程的一次大幅 *坍缩*——从「N 个任务 × N 个架构」到「1 个预训练 + N 个线性头」。从这一刻起，「研究新架构」在 NLP 圈不再是主流——主流变成「研究更好的预训练目标」。后来 GPT 路线把这个范式再压一格：不仅架构统一，*连下游 fine-tune 都不需要*，prompt 即可。

* 洞见

*在「理解」类任务上，预训练目标的双向性比模型架构本身更重要*。

整篇论文从头到尾的 ablation 都在说同一件事：把 GPT 的架构原封不动搬过来（BASE 和 GPT 同尺寸），只是把训练目标从单向 LM 换成 MLM，所有 GLUE 任务全面碾压。这意味着 *表示的好坏取决于训练时让模型看到的「上下文范围」*——架构只是承载这个上下文范围的容器。

由此带走两条能动手的认知：

1. *做表示学习时，先想「我让模型看到什么」，再想「用什么模型看」*。架构选择是次要的；目标函数划定的「可见域」决定上限。
2. *任务专属架构的红利会随预训练深化而消失*。BERT 出现前 NLP 的 BiDAF / ESIM / BiLSTM-CRF 全是为了「在没有好预训练时多榨一点性能」。一旦预训练够好，这些架构就是冗余。在搜推领域同理：当用户行为序列预训练做透了，下游精排的复杂网络结构往往也会随之坍缩。

* 博导审稿

*选题眼光*：真缺口，不是人造缺口。2018 年所有人都在用单向 LM 做预训练，没人系统挑战过「为什么必须单向」这个隐含戒律。Devlin 看穿这是 *目标函数定义* 的人为限制（不是 Transformer 架构的限制），换个目标就解锁——这是研究品味的体现。Strong yes。

*方法成熟度*：MLM 是巧劲、NSP 是蛮力。MLM 漂亮在它把「不能看自己」从架构层面（mask 矩阵）转移到了输入层面（直接替换），优雅程度高。NSP 就比较潦草——直觉上「学句对关系」很合理，但论文用的是 *50/50 随机配对* 这种粗糙信号，后来 RoBERTa（2019）和 ALBERT（2019）双双证明 NSP 没用甚至有害。换言之：*这篇论文的两个预训练目标，一个革命、一个噪音*。论文写作时把它们并列呈现是不诚实的——更准确的判断应该是「MLM 单独就够了」，但作者没有做这个 ablation（"BERT_BASE without NSP" vs "BERT_BASE" 的对照在 Table 5 有，但论文倾向解读为「NSP 有用」）。学生在做研究时要警惕「成功的方法里夹带的失败组件」。

*未被讨论的根本预设*：BERT 假定「下游任务以理解为主」，所以双向编码器是普世答案。但 *自回归生成任务被默默排除*——你不能用 BERT 写文章，因为 MLM 训练根本不会让模型学习「按顺序生成下一个词」这个能力。论文一个字都没提这个限制。事后看，这个被掩盖的限制决定了 BERT 路线的天花板：当通用智能要求「一个模型既能理解又能生成」时，GPT 路线（自回归）赢了，BERT 路线收敛到 encoder-only 的特征提取器角色。换句话说：*BERT 在 2018 年的「全胜」是建立在「NLP = 理解任务」这个错误预设之上*。学生做研究要随时反问：我的方法的「域外」在哪里？我假设了什么样的任务分布？

*实验诚意*：充分。GLUE / SQuAD v1.1 / SQuAD v2.0 / SWAG / NER 五个 benchmark 全覆盖，ablation 包括「去 NSP / 去双向 / 加 BiLSTM 兜底」三组对照、「12 层 vs 24 层 vs 不同隐藏维」尺寸 sweep、feature-based vs fine-tuning 两条路线对比。诚意十足，没有挑数据集。

*写作功力*：清晰、克制、不卖弄。Section 3 把架构和预训练任务讲得让二年级 PhD 也能复现。Figure 1（pre-training / fine-tuning 双面板）是教科书级的论文图——一图说清整套范式。

*判决*：*Strong accept*。这是 NLP 史上少有的「换个目标函数，整个学科范式坍缩」级别的工作。它的问题（NSP 是噪音、生成任务被回避）不削弱核心贡献，只说明任何范式革命都不可能一次性把所有问题解清楚。

* 启发

落到我手头的搜索推荐工作上，三条能动手的：

** 迁移：用户行为序列上的 MLM 预训练

把用户的点击/曝光/购买序列当 token 序列，做 BERT 风格的 MLM 预训练——随机盖掉 15% 的行为 item，让模型靠左右上下文的行为填回来。这比 GPT 风格「预测下一个点击」更贴搜推任务的真实形态：召回/精排不是「续写用户未来」，是「理解用户当前 query 的意图分布」，本质是双向理解任务。

具体怎么接：
- token 词表 = item ID（或语义聚类 ID）+ 特殊 token `[CLS]` `[SEP]` `[MASK]`
- segment embedding 区分「query 序列」 vs 「user 行为序列」（双 segment 预训练）
- 下游粗排 / 精排：取 `[CLS]` 输出做 user-query 兼容性打分，或者拿 `T_i` 做 item-level 排序特征
- MLM 和 *搜推业务里已经在做的 item-CTR 预测* 是正交的——前者训表示，后者训打分头

这个思路 KuaiBERT / SASRec / BERT4Rec 都做过，但工业落地时往往因为「预训练 vs fine-tune 的 [MASK] 错位」掉性能。BERT 的 *80/10/10 trick* 是解药——可惜很多搜推 BERT 复刻者把这步省了。

** 混搭：[CLS] + [SUMMARY] 做粗精排一致率的桥

我现在在做粗精排 Top N 一致率指标。粗排用极简模型（双塔），精排用复杂模型（交叉特征 + Transformer）。两者表示空间不一致，是一致率掉的根因。

借 [CLS] 的思路：在精排 Transformer 里加一个 *与 [CLS] 同质的 [SUMMARY] token*，预训练时让它聚合整个 user-context 上下文。粗排的 user 塔不再独立训，而是 *蒸馏自精排的 [SUMMARY] 表示*——粗排塔的输出向量直接对齐精排 [SUMMARY] 向量（MSE 或 InfoNCE）。这样粗排和精排共享同一个表示空间锚点，Top N 召回对齐率应该能拉。

待验证：[SUMMARY] 蒸馏目标 vs 直接 logit 蒸馏，哪个对一致率更友好。

** 反转：警惕 NSP 类「直觉合理但 ablation 证伪」的辅助任务

我在搜推系统里见过太多「直觉上应该有用、但 ablation 一做就证伪」的辅助 loss——多任务里的次要任务、对比学习里的负样本构造、点击/转化双塔 loss 平衡。BERT 的 NSP 是这个失败模式的鼻祖：*作者自己都没做严格 ablation 验证 NSP 是否真有用*，结果一年后被两个独立工作（RoBERTa、ALBERT）双重证伪。

提醒自己：每加一个辅助任务，都要做「去掉它会怎样」的对照，且这个对照必须 *和加它时一样投入的算力*——不能拿一个少训 50% 的版本说「去掉就掉点」。NSP 当年没掉点是因为它没贡献也没害（中性 noise），但论文写法让人误以为它必要。我在自己的项目里也容易掉进同样的陷阱：「加了某个 loss 模型 work 了」≠「这个 loss 是 work 的原因」。

* 串联

把这篇放进我已读的 CV/DL 奠基序列里，五篇连起来是一条清晰的范式坍缩线：

| 年份 | 论文 | 它做掉了什么 |
|------|------|-------------|
| 2012 | AlexNet | 证明深度 CNN + GPU 在视觉上 work |
| 2015 | ResNet | 解决「再深就训不动」的优化问题，深度本身可堆 |
| 2017 | Transformer | 用注意力替代 RNN，序列建模摆脱时间步串行 |
| 2018 | *BERT*（本篇） | 证明双向预训练 + 极简 fine-tune 头能通吃 NLP 任务 |
| 2020 | ViT | 把 Transformer 搬到视觉，证明「数据足够，先验可舍」 |

BERT 在这条线上是 *NLP 的第一次大坍缩*——从「N 个任务 × N 个架构」收敛到「1 个预训练 + N 个线性头」。ViT 两年后做的是 *视觉的同款坍缩*——从「卷积 + 池化 + 局部先验」收敛到「token + Transformer + 数据规模」。两者的范式同构性是惊人的：都把「架构创新」让位给「目标函数 + 数据规模」。

这条线的下一步——也就是我接下来该精读的方向——是 *把双向理解和自回归生成统一在一个目标函数下*：T5（text-to-text 统一）或 GPT-3（in-context learning 替代 fine-tune）。BERT 范式天花板就在那两篇论文出现的位置。
