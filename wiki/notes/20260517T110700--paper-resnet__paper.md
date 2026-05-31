---
title: 学增量，不重造
subtitle: Deep Residual Learning for Image Recognition — 让深网络走得通的那一刀让权
date: 2026-05-17 Sun 11:07
tags: [paper, deep-learning, computer-vision, architecture]
identifier: 20260517T110700
source: https://arxiv.org/abs/1512.03385
authors: Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun (MSRA)
venue: CVPR 2016 (Best Paper Award), arXiv 1512.03385
---

> *原文 PDF*：[1512.03385-Deep-Residual-Learning-for-Image-Recognition.pdf](file:///Users/nolanhuang/paper_agent/wiki/raw/papers/1512.03385-Deep-Residual-Learning-for-Image-Recognition.pdf)

## 问题

2014 年底，一个刚跟着 VGG 风潮调通了 19 层网络的 CV 工程师，回家把网络堆到 56 层。他的预期很朴素——*VGG 是 19 层，那 56 层应该更准*。第二天看 training curve：56 层的训练误差比 20 层还高。

不是验证集，是*训练集*。这意味着不是过拟合——过拟合至少训练集上是赢的。是*更深的网络连训练数据都拟合不了*。他以为代码写错了，反复对，反复跑，发现没错。再换 BN，换初始化（Xavier、He init 都试过），还是一样。56 层 plain net 就是被 20 层吊打。

这件事在当时全场都看见了：网络一过 30 层，性能开始往下掉。圈里管它叫 *degradation problem*——退化问题。

之前的研究者怎么处理？两条路。一条是 *谨慎堆深*：VGG 顶到 19 层就停手，再深就靠工程花活（更小的 kernel、更猛的 dropout、更细的初始化）。Highway Network（2015）走第二条——给每层加一个 *learned gate*，让网络自己学"这一层要不要让信息穿过去"，但 gate 的参数本身要学，深层依然吃力，120 层就到顶了。两条路都默认了同一件事：*深度的代价是优化困难，必须由人手设计来抵消*。

何凯明他们看到了别人没看到的入口：*degradation 不是优化能力的物理上限，是优化目标摆错了位置*。如果 56 层最优解就是"把 36 层都做成 identity，剩下 20 层等价于 20 层 plain net"，那让一堆非线性层学出 identity 比想象的难得多——它们要靠几十个权重精准协同凑出 *y=x*。但如果换个目标，让这些层只需要学*它和 identity 的差*，把 weights 全压到 0 就完成 identity 了。差*（Residual）*比 *本体（Mapping）* 好学。

## 翻译

锚点继续在那个 56 层的工程师身上。他听了何凯明的提议，回去把网络改了一处——*每两层后面加一根从输入直连过来的线*。

这根线就是论文的命脉。在那个 56 层的工程师眼里，它长这样：

```
       x
       |  +---------+
       v  |         |
   +-------+        |
   | weight|        |
   |  +    |        | <- shortcut
   |  ReLU |        |  (identity)
   |  +    |        |
   | weight|        |
   +-------+        |
       |   <--------+
       v
       +
       |
       v
     ReLU
       |
       v
       y
```

读法：两层 weight 算出 *F(x)*，shortcut 把原 *x* 直接搬过来，加在一起，再过一次 ReLU 出 *y*。整层做的事是 *y = F(x) + x*，而不是 *y = H(x)*。

这一改动看着小到像没改——*shortcut 不带任何参数*，只是一根加法线。但它把网络的优化任务从"学映射 H"换成了"学增量 F = H − x"。

*这时候你看*——如果 56 层最优解里有 36 层应该做成 identity，那 36 个 *F* 块只需要把权重推到接近 0，shortcut 自动把 *x* 送过去就完事了。不需要让 weight 精确凑出 identity，只需要让它们*躺平*。优化器最擅长把一堆参数推向 0——L2 正则就是干这个的。

*那剩下 20 层呢？*——剩下 20 层学到的也不是"完整的特征变换"，而是"在已经能正确分类的基础上还差什么"。这是 *残差学习* 的精髓：不是让深层从头雕一个新答案，是让深层在浅层答案上*打补丁*。

*实验数字（在那只工程师天天跑的 ImageNet 上）*：

- *34 层 plain net*：top-1 error 28.5%。
- *34 层 ResNet*：top-1 error 25.0%（−3.5%）。同样深度，多一根 shortcut 线，绝对降 3.5 个点。
- *152 层 ResNet*（论文当家选手）：top-5 error 4.49%（single model），ensemble 3.57%。比 ImageNet 的人类标注误差（5%）还低。
- *CIFAR-10 上的极限*：1202 层 ResNet 训得通，training error 收敛——证明这个方法的天花板远不止 152 层。

*然后是那个最让人"哇"的副发现*——他们去测每层的*响应强度*（layer activation 的标准差）。plain net 的层与层之间响应水平差不多，每层都在"用力做事"。ResNet 的层响应*显著更小*，越深的层越接近 0。

这意味着什么？*ResNet 的多数层确实在学一个接近 identity 的映射*——*F* 趋近 0。深层不是在重新雕一遍 *x*，而是在 *x* 上做小额修正。这个数据正好佐证了"残差比本体好学"的猜想——网络自己用行动告诉作者：*你设的目标，确实是优化器能轻松拿到的位置*。

*最后一个工程要点：bottleneck*。152 层如果每层都用 *3×3+3×3* 块，参数会爆炸。论文用 *1×1 → 3×3 → 1×1* 三明治结构（先压通道再放回来），让 152 层的总参数量比 VGG-19 还少。这不是发明，是*让深度的代价不发散到工程上*的关键 trick——没有 bottleneck，152 层只能停留在 paper 里。

## 核心概念

挑三个外行卡住后面就跟不上的概念。

*1. Residual learning（残差学习）* — 不学 *H(x)*，学 *F(x) = H(x) − x*。

回到那个 56 层网络：原来要它学的是"输入猫的图，输出猫的特征向量"，整段路自己走。现在改成"输入猫的图，输出'比浅层提取的猫特征还差什么'，再加上浅层结果"。如果浅层已经认得是猫了，深层要学的就是细化那一点点（毛色、姿态、品种），而不是从头识别。少了它，56 层 plain net 的 36 层"应该做 identity 的层"必须自己凑出 *y=x*——优化器搞不定。

*2. Identity shortcut（恒等捷径）* — 一根不带任何参数、把 *x* 直接送到下两层之后的加法线。

它的特殊在于*零参数*。Highway Network 也搞 shortcut，但带 gate（要学"开多大"），结果 gate 参数把深层的优化负担又抬回来了。ResNet 的 shortcut 是"白送"——*F(x) + x* 里那个 *x* 不算账。零参数意味着零优化阻力，意味着不论深网堆多少层，*identity 永远是默认的、免费的、可达的状态*。少了它（哪怕换成 1×1 conv 当 shortcut），深度往上推时退化又会出现——论文 Table 3 比较过。

*3. Pre-activation 与 BN 位置（设计 trick）* — 这条不是组件，是让整个机制 work 的设计选择。

*F* 块内部的顺序是 weight → BN → ReLU → weight → BN，加法之后再 ReLU。这个顺序保证 shortcut 路径上是"干净的 identity"——加法前 *x* 没被 BN/ReLU 污染。如果 shortcut 路径上插一个 ReLU，*x* 的负值就被砍掉一半，identity 就破了，深层学起来又会卡。这个细节是后续 ResNet v2（He et al. 2016b）专门讨论的——*shortcut 要纯，纯到一点非线性都不能加*。少了它，论文里 152 层的稳定收敛就垮了。

## 洞见

*让深网络走得通的那一刀，不是发明了新结构，是把"默认值"换成了 identity*。

之前的网络默认每层都"做事"——一旦实际任务里某些层应该不做事（identity），优化器要拉着一堆权重精准凑出 *y=x*，难。ResNet 把默认改成"不做事"，需要做事的层在 *F* 里自己长出来，*F=0* 就等于让权。

这是一个 *目标重设* 的洞见，不是 *容量提升* 的洞见。同样的参数、同样的数据、同样的优化器——只换了"网络该学什么"的定义，56 层就从训不动变成训得通，152 层变成新基线。

带得走的东西：*遇到优化卡住，别先想"加容量、加数据、换 optimizer"，先问"我让模型学的目标，是不是把它最容易达到的状态摆在了反方向？"*。如果"什么都不做"是个合理候选答案，那它应该是默认值，不是要努力学出来的特殊点。

## 博导审稿

*选题眼光*：strong。Degradation problem 是 2015 年视觉圈里大家都看见、但没人敢正面打的硬骨头——多数人绕道走，靠 BN、Highway 这种"补丁"消解。何凯明他们正面拆问题：*为什么深就该卡？* 拆到"目标摆错位置"这个层面，干净利落。这种问题 ten years later 看，是真缺口，不是人造缺口。

*方法成熟度*：一刀干净。Shortcut 是零参数 identity，没有 gate、没有 weighting、没有 attention——*能不带参数就不带参数*这件事被做到了极致。这是巧劲，不是蛮力。比起 Highway Network 多 30% 参数才能搞通 100+ 层，ResNet 是用"减法"赢的——减掉了 gate，反而走得更远。

但有个未被讨论的*根本预设*：*假设最优解结构里 identity 层占比不小*。论文 motivation 反复说"如果最优是 identity，残差学起来更容易"——可万一最优解里 identity 层占比很小呢？比如某些任务（speech、video temporal）里每一层都需要做实质变换，identity 不是好的默认值。这种情况下 ResNet 的归纳偏置反而是包袱。这就是为什么后来 Transformer 在 NLP 上独立做出 residual+LayerNorm 后，*shortcut 这件事变成了通用配方，但 identity-as-default 的强度被 LayerNorm/Pre-LN 等机制反复重新校准*——大家在悄悄修正这个 "identity 是好默认值" 的假设。

另一个隐忧是 *响应越来越小* 这个副发现的两面性——它说明 *F* 确实在学小修正，但也说明深层在做的事越来越"不那么必要"。这意味着 ResNet 的"深"，部分是冗余的，*1000 层和 100 层在做的事可能高度重叠*。后来 Stochastic Depth、DropPath、Layer Pruning 都在挖这个洞——证实了博导的怀疑：*ResNet 的深度有水分*。

*实验诚意*：足。ImageNet 上 18/34/50/101/152 层都跑了 plain vs residual 对照，ablation 详实。CIFAR 跑到 1202 层证明天花板远未到。bottleneck vs basic block 的参数量对比也给出了。Baseline（VGG-19、GoogLeNet-22）公道。

*写作功力*：能给本科生看懂，又能让审稿人挑不出毛病。Figure 1 的 plain net 退化曲线是全文文眼——一张图就让人理解了 motivation。

*判决*：*strong accept*。是少数几篇"读完之后整个领域的默认起点都被改写"的论文——之后所有视觉网络（DenseNet、ResNeXt、EfficientNet 直到 ConvNeXt），所有 NLP 网络（Transformer 全家），都默认带 residual。它不是 incremental，是 redefinition。CVPR 2016 Best Paper，名实相符。

## 启发

接 AlexNet 的「让权链」继续往下走，三视角连看：

*1. 让权链的第二刀更精细——让的是"网络架构里的默认假设"*

AlexNet 让的是"特征要不要人手设计"——粗粒度，整段流水线作废。ResNet 让的是"每一层默认在做什么"——细粒度，单层级别上把"做事"的负担反过来安排。从让权链的角度看，这是一次*更深的让*：连每一层应不应该做事，都让出去给优化器决定。

*顺着这条线往下，下一刀在哪？*
- Transformer 让的是"信息流的拓扑由谁决定"——RNN/CNN 都是人手设计的拓扑（顺序传递 / 局部聚合），attention 让"谁连谁"自己学。
- ViT 让的是"图像该不该被当成 2D 网格"——直接当 token 序列，让模型自己发现 2D 结构。
- Mamba/SSM 让的是"信息混合机制要不要人定"——softmax-attention 还是人手设计的机制，SSM 把混合也变成可学。

ResNet 在这条链里的位置是 *第一个把"层与层关系"让权的工作*。它告诉后人：*让权可以做到层内级别*。

*2. 投资视角：押"让默认值"的人*

AlexNet 那篇启发里说押"让特征工程让出去"的赛道（金融因子、法律条款、医药描述符）。ResNet 把粒度细化了——*在已经端到端的领域里，找哪些"默认假设"还是人手设计的*，那是下一个 ResNet 时刻。

具体抓手：
- *评估指标的默认假设*：一堆 RAG、agent 公司还在用人手设计的 evaluation harness（precision@k、ROUGE、人工标注）。把"评估什么"也让出去（让模型自己长出 reward model）的公司，是潜在 ResNet 时刻——比如 Anthropic 的 Constitutional AI、OpenAI 的 RLHF→RLAIF 演进。
- *推理框架的默认结构*：现在的 agent 框架默认 plan→tool→observation→reflect 这个 loop 是人定的——LangChain、AutoGen 都在卖这套手雕的循环。把循环结构也让出去（让模型自己学"该不该 plan、该不该 reflect"）的方向，是 OpenAI o1/o3、DeepSeek R1 这条线在做的事。卖死循环的公司是 plain net，卖让循环长出来的环境的公司是 ResNet。
- *判断器*：这家公司在卖"更精细的人手默认值"还是"让默认值自己浮现的环境"？前者越复杂越死路，后者越简单越值钱。ResNet 之所以横扫，是因为它的核心改动只有"加一根线"——*简单到能让权的方案，比复杂到无法让权的方案，长跑赢*。

*3. RAG/大模型视角：当前栈里哪些"默认值"在等 ResNet 时刻？*

ResNet 的关键不是"加深"，是"把 identity 设为默认值"。把这个视角搬到 RAG 栈：

- *Chunking 是默认值*：现在所有 RAG 默认要切 chunk，长度超 512 就切。ResNet 视角下应该问：如果"不切 chunk"是更合理的默认值呢？Late chunking、layout-aware、hierarchical retrieval 都在做这件事——*让"切不切、切多大"自己浮现*，而不是写死。
- *Retrieval-augment 是默认值*：现在 RAG 默认每个 query 都走一次检索。ResNet 视角应该问：如果"不检索"是更合理的默认值呢？Self-RAG、Active Retrieval 让模型自己决定要不要检索——*让"检索动作"变成可学的而非默认的*。
- *Top-k 是默认值*：默认取前 k 个 chunk 拼进 prompt。ResNet 视角应该问：如果"不取或取所有"是更合理的默认呢？长上下文模型让 k 趋向无穷，selective context 让 k 趋向 0，两边都在重定义这个默认值。

*共同模式*：当前 RAG 栈的每一处"必须做"，都在等一个把它降为"可选默认"的工作。哪个先被降下来，哪条线就出 ResNet 时刻。

*4. 反转视角：能让"做事"不能让"路径"，再追一刀*

AlexNet 的反转里说"能让路径不能让指南针"。ResNet 给这个加了细化：*能让"该不该做事"，但不能让"做完之后往哪走"*。Shortcut 让深层可以选择不做事，但*shortcut 自己的拓扑（哪两层之间连）是人定的*——论文里写死了"每两层连一根"。

后来 DenseNet 把这个让出去了（每层和之前所有层都连），但代价是参数爆炸；NAS 又把"该连不该连"让给搜索算法。这条让权也在持续——*下一个能想清楚"shortcut 拓扑该怎么自动浮现"的工作*，会是又一刀。

判断器：你的系统里，*"哪些组件该跳过、哪些该用"* 这件事是人定的吗？如果是，那就是下一个 shortcut 让权的位置。
