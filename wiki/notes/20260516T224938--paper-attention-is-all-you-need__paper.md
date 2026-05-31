---
title: 步步成桎，一望即通
subtitle: Attention Is All You Need
date: 2026-05-16 Sat 22:49
tags: [paper]
identifier: 20260516T224938
source: /Users/nolanhuang/paper_agent/wiki/raw/papers/1706.03762-Attention Is All You Need.pdf (arXiv 1706.03762)
authors: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin
venue: NeurIPS 2017 (Google Brain / Google Research / U. Toronto)
---

> *原文 PDF*：[1706.03762-Attention Is All You Need.pdf](file:///Users/nolanhuang/paper_agent/wiki/raw/papers/1706.03762-Attention%20Is%20All%20You%20Need.pdf)

# 问题

你在做机器翻译。给一句英文 *"The animal didn't cross the street because it was too tired"*，要翻成德文。德文代词得分阴阳中性，所以你必须告诉模型：这个 *it* 指的是 *animal*，不是 *street*。这俩词隔了七个位置。

2017 年大家公认的做法是 RNN（LSTM、GRU）。一个词一个词读进来，每读一个词更新一次隐藏状态。读到 *it* 时，*animal* 的信号已经被挤压、覆盖、衰减了七次——梯度过六道门就糊了，长距离依赖学不动是 RNN 的老毛病。更别提这七步只能严格串行：第一步没算完第二步动不了，GPU 闲一半，训长句子就是干等。卷积版本（ConvS2S, ByteNet）想救场，但要让首尾两端"看见对方"还是得堆很多层，路径长度只是从 *O(n)* 缩到 *O(log n)*，没本质区别。

作者看到的入口非常硬核：*为什么不让 it 直接看一眼 animal？* 不要任何中间步骤，不要 hidden state 接力，不要卷积窗口——任意两个位置一步对望。这个想法逼出了一个看似激进的赌注：把 recurrence 和 convolution *全部砍掉*，整个模型只剩 attention。论文标题 *Attention Is All You Need* 是字面意思——真的只用这一个东西。

# 翻译

在我们那个 *it / animal* 的句子上，方法像一场圆桌会议。

九个词（*The animal didn't cross the street because it was too tired*）每人坐自己的位置。每轮会议开始，每个人手里拿着三张牌：

- *query*（我想找什么）
- *key*（我擅长被谁找）
- *value*（我能给出什么内容）

*it* 举起 query：「我是个代词，我想找一个名词，最好是能解释为什么 *too tired*。」全场的 key 都被它扫一遍，相似度高的就权重高。*animal* 的 key 写着「我是名词、生物、能累」——匹配。*street* 的 key 写着「我是地点、无生命」——不匹配。于是 *it* 把 *animal* 的 value（"指代生物"这个语义）大份拿过来，把 *street* 的 value 几乎不要。一轮会开完，*it* 的表示里就含上了 *animal* 的语义。

整个过程一步完成。从 *it* 到 *animal* 的"路径长度"是 *1*，不管中间隔多少词。这就是论文表 1 那一行的含义：self-attention 的 maximum path length 是 *O(1)*，RNN 是 *O(n)*。距离不再是问题。

*那为什么是 8 张桌子并行（multi-head）？* 一张桌子只能聊一种关系。「指代」是一类，「主谓搭配」是另一类，「修饰」又是一类。如果只用一个头，softmax 平均下来这些信号互相打架，averaging 抹平细节。论文做了消融：1 头比 8 头差 0.9 BLEU，32 头反而又变差——8 是甜点。每个头被强制做不同的事，分工出现。后来可视化发现，确实有的头专门管短距离句法、有的头管长距离指代——分工是涌现的，不是设计的。

*那为什么要除一个 √dk？* 当 query 和 key 维度变大（论文里 dk=64），点积的量级也跟着涨。softmax 一旦输入过大就饱和——最大值那一项接近 1，其余近 0，梯度几乎消失。除以 √dk 把分布拉回温和区，让 softmax 还能学。这个设计在 1 年后所有人都开始用，省下无数次"为什么不收敛"的 debug。

*那位置呢？* 砍掉 RNN 之后冒出一个新坑：模型现在完全不知道词的顺序。把句子打乱再喂进去，attention 算出的结果一模一样——对它来说"猫吃鱼"和"鱼吃猫"等价。作者打的补丁是直接在词向量上加一个 sin/cos 函数生成的位置编码：每个维度用一种波长，波长从 2π 到 10000·2π 几何级数排列。作者的赌注是「这种编码能让模型学相对位置」（PE_{pos+k} 可以表达成 PE_pos 的线性函数），但消融表 row (E) 里他们顺手做了对比：sin/cos 和 *learned positional embedding* 效果几乎完全相同。这意味着——*位置编码这块作者自己也没想透*。这个口子被后来的 RoPE、ALiBi、相对位置编码反复挖，挖了七年还在挖。

*结果有多漂亮？* WMT'14 英德翻译，Transformer big 拿到 BLEU 28.4，比之前最好的 *集成模型* 还高 2 分以上；训练只用 8 张 P100、3.5 天。base model 用 12 小时跑完就已经超越所有已发表单模型。在英法翻译上 BLEU 41.8，训练成本不到上一届 SOTA 的四分之一。最有意思的是论文 6.3 节顺手做了英文句法分析（constituency parsing），啥都没改，4 层 Transformer 直接接近 SOTA——这其实是在悄悄说："这玩意儿不只是翻译模型，是个通用结构"。后来的故事大家都知道了。

# 核心概念

*Self-attention 的 QKV 三角色*。在 *it / animal* 的例子上：每个词同时扮演三个身份。query 是它"想问什么"，key 是它"被找时显示什么标签"，value 是它"被选中后交出什么内容"。三个角色由同一个词的 embedding 经三个不同线性层投出来——同源、异职。少了 QKV 这层抽象，attention 就是个"按相似度加权"，没有"提问→应答"的语义角色，方法的可解释性和扩展性立刻塌陷。后来 cross-attention（query 来自一边、key/value 来自另一边）能优雅成立，全靠这个三角色框架。

*Multi-head 不是 ensemble，是分工*。8 头并行常被误解成"多算几次取平均更稳"，但论文里 d_model=512 被切成 8 份每份 64 维——*总计算量没变*，只是表达空间被切开。重点不是冗余，是强迫不同子空间学不同的关系类型。在 *it* 的例子上：一个头可能专门做"指代-名词"匹配，另一个头做"主语-时态"匹配。少了多头，softmax 把所有关系压成一坨平均权重，就像让一个人同时听 8 段对话再总结——averaging inhibits this，论文原话。

*位置编码是"凑合的设计选择"，不是定理*。这是论文里最暴露作者*没想透*的一块。前面 self-attention 的 *O(1)* 路径长度论证得很硬，但到位置编码这里画风一转：选 sin/cos 是因为「我们 hypothesize 它能学相对位置」，并且「也许能外推到训练时没见过的长度」——两个 hypothesize 都没证明。对照实验（learned vs sinusoidal）效果一样，恰恰说明这个组件还有大量优化空间。后来 RoPE 把"相对位置"从加法改成旋转，ALiBi 干脆改成线性偏置——七年来位置编码被颠覆了三轮，根源就在这里。这是个示范：*论文里被作者一笔带过的设计选择，往往是后续工作最肥的矿。*

# 洞见

*序列性不是问题的本质，是工具的痕迹。*

RNN 时代我们以为"按顺序处理"是 sequence modeling 的天然属性——文字本来就有先后嘛。Transformer 戳破了这个幻觉：先后顺序只是数据的一个属性（位置编码就够了），它*不必*体现在计算图里。一旦把"顺序"从计算结构中剥离，并行性、长距离依赖、可扩展性同时解锁。

这个思路可以反复套用：每当你看到一个工作流被强制成串行，问一句——*这个序是数据本身要求的，还是被工具锁死的？* 多数时候是后者。把序还给数据、把并行还给计算，常常就是下一个 Transformer 时刻。

# 博导审稿

*选题眼光*：strong。「序列计算是必须的吗」是真问题不是人造缺口。RNN 的 *O(n)* 串行成本在序列长度爆炸的时代是结构性瓶颈，不是参数调一调能绕过去的。作者敢直接砍掉 recurrence 和 convolution——这种"把婴儿和洗澡水一起倒掉"的勇气，是好选题的标志。

*方法成熟度*：巧劲，但有三个未被作者讨论的根本预设，七年后回看每一个都是雷：

(1) *O(n²) 复杂度被脚注一笔带过*。论文 4 节末尾轻描淡写"我们 plan to investigate restricted attention"——这是个非常诚实的脚注，但读者很容易忽略。今天大模型的上下文长度战争（128K、1M、10M）其实是在还这笔账。FlashAttention、Ring Attention、稀疏 attention 全是在做的事就是*缓解*这个 *O(n²)*，没人真正解决。作者那时假设「序列长度 n 通常小于表示维度 d」——在 2017 的 NMT 任务上对，2024 之后全错。

(2) *位置编码的 hypothesize 没坐实*。前面已说，sin/cos 和 learned 等效说明这块没想透。后续 RoPE / ALiBi 都在挖这个坑。作者把"相对位置可由 PE 线性表达"当成动机，但模型实际是不是真用了这个性质，没有任何证据。

(3) *Encoder-Decoder 范式被默认接受*。论文整套架构是为机器翻译这种 sequence transduction 任务设计的——一边读、一边生成。但当任务退化到 *language modeling*（只生成不翻译），encoder 这半边其实是冗余的。GPT 系列直接砍掉 encoder 只留 decoder-only，反而成了主流。作者没质疑「sequence transduction = encoder-decoder」这个继承自 seq2seq 时代的预设。这不算失误（论文做的就是 NMT），但这是个隐性预设，外行读者容易把它当作 Transformer 的本质。

*实验诚意*：高。Table 3 的 ablation 该消的都消了——头数、key 维度、模型规模、dropout、label smoothing、位置编码方式，每行都有数。两个数据集（EN-DE / EN-FR）+ 一个迁移任务（constituency parsing）。FLOPs 估算公开。基本无水分。

*写作功力*：教科书级。5 页核心内容，配图清晰到工程师能照着 reproduce。Section 4 *Why Self-Attention* 用 path length / sequential ops / per-layer complexity 三个维度直接对位 RNN/CNN/Self-Attention，是把"为什么这么做"摆在桌上而不是塞进附录的范本。

*判决*：*strong accept*。21 世纪深度学习三大奠基论文之一（另两个是 AlexNet、ResNet）。这种论文的"评分"已经没意义——它已经是行业的语法。

# 启发

*反转*：作者赌"通用并行结构 > 任务特化结构"——七年后被 LLM 完全验证。但反过来：*作者埋的 O(n²) 雷，今天还在*。当工程师面对长上下文挑战时，与其继续优化 attention 常数，不如重新质疑"是否真需要每一对 token 都互看"——这是 Mamba / 状态空间模型在赌的方向。Transformer 的胜利让人忘了：它的 *O(1)* 路径长度是用 *O(n²)* 内存换来的，这笔账总有一天要还。
