---
title: 模型评估——benchmark 作为估计器与它的三种失效
created: 2026-07-25
updated: 2026-08-12
type: concept
tags: [benchmark, alignment, llm]
sources: []
---

# 模型评估——benchmark 作为估计器与它的三种失效

一个 benchmark 分数不是「模型能力」本身，而是**在特定样本、特定评分规则下对某个目标分布风险的一次有限样本估计**。把它当估计器看，评测的所有坑就都能归到「这台估计器在什么条件下失真」这一个问题上，而不必逐个背名词。

## 骨架：benchmark 是一台估计器

线上真正关心的是目标分布 `P_online` 上的风险 `R_online(f) = E_(x,y~P_online)[L(f(x),y)]`；但线上总体无法完整观察，于是从评测分布 `P_eval` 采有限样本算 `R_hat_eval(f) = (1/n) Σ L(f(x_i), y_i)`，再拿它推断 `R_online`。这一步推断暗中依赖三个条件，三个条件各对应一种失效：

```text
独立性  评测题没进过训练/微调/prompt 开发/选模    破裂 → contamination（数据污染）
非适应性 没在同一批题上反复试到把噪声也调进来       破裂 → Goodhart / benchmark overfitting
代表性  P_eval 与今天的 P_online 足够接近          破裂 → distribution drift（分布漂移）
```

三项任一破裂，分数仍可上升，但它对真实能力的估计已经失真。[[2026-07-17-benchmark-failure-distribution]]

## 三种失效

| 失效 | 攻击的假设 | 表现 | 优先查的证据 |
|------|-----------|------|-------------|
| **contamination** | 评测与训练之间的防火墙 | 公开榜暴涨、私有题不涨 | 去重、时间切分、近重复与模板重合、检索库是否存答案 |
| **Goodhart / 过拟合** | 「测量不改变被测系统」 | 同一验证集越调越高、新留出集不涨 | 调参次数、选模历史、winner's curse、隐藏 holdout |
| **distribution drift** | 「过去采的题仍代表今天的世界」 | 离线稳定、线上逐月下降 | 分时段切片、流量构成、任务与工具变化 |

- **contamination** 不一定是逐字背诵：近重复、模板污染、开发污染（团队反复看错误样本改 prompt）、检索污染都算。「输出不一字不差」不能证明没污染——它把测量对象从「样本外泛化」悄悄换成了「训练暴露 + 记忆迁移 + 泛化的混合物」。
- **Goodhart** 不需要偷看答案：测试集不进梯度 ≠ 没被优化。团队每天照同一 dashboard 决定保留哪个实验，dashboard 就是一种稀疏、延迟的人类梯度；`winner's curse` 让胜出配置混入对有限样本噪声的幸运适配。
- **drift** 对 LLM 常是系统自己制造的（`performative prediction`）：模型上线 → 用户学会提问、失败用户离开 → 日志分布改变 → 下一轮训练又用这些日志。离线与线上「打架」时先别裁决信谁，先问两边的 `estimand`（待估量）是否同一个总体、时间窗口与损失函数。

## 聚合掩盖分布：总分为何测不到关键切片

总体准确率 `overall = Σ_g p_g · accuracy_g` 的权重 `p_g` 来自**测试集的样本占比**，不是业务价值。关键组只占 10%、掉 10 个点，只让总分掉 1 个点——于是「模型没在线上突然变差，而是离线平均从未测量你真正关心的风险」。[[2026-07-25-aggregation-erases-minority-signals]]

```text
模型   普通样本(90%)   关键切片(10%)   总体
A         96%             55%          91.9%
B         94%             75%          92.1%   ← 榜单只说「B 高 0.2 个点」
```

B 用普通样本 2 个点换来关键切片 20 个点，是风险结构的改变，总分却把它压成 0.2。这与 [[text-embedding]] 编码端的实体 mismatch **同构**：都是「过早聚合把决定性的少数信号抹平」，只是一个在编码端（整句压成一个点）、一个在评测端（整集压成一个数）。修法也同构——拒绝过早聚合、按业务风险再聚合：per-slice 指标 / macro average / worst-group / CVaR / cost weighting，对应检索端的 MaxSim / exact-match / entity-aware 难负例（见 [[colbert-retrieval]] [[sparse-retrieval]]）。

## 让权指南针：LLM-as-judge 把评测从「打分」变成「闭环控制」

AlexNet 与 Transformer 都让模型自学**路径**（特征形成 / 信息路由），却仍由人固定**指南针**——而指南针不止一个 loss，而是 `标签定义 + 数据分布 + loss + 评测指标 + 选择/发布规则`。**模型路径越自由，指南针越重要**：搜索能力越强，越擅长找目标函数的漏洞。[[2026-07-21-path-and-compass]]

LLM-as-judge / RLAIF 第一次大规模让一个**会学习、有偏好、可被迎合**的模型进入评价闭环。三个失效机制：

- **共盲**：选手与评委来自相似预训练/对齐，误差相关——评委一致不等于真，可能只是同一把歪尺测十次。
- **迎合**：优化器发现评委口味（位置偏置、冗长偏置、自我偏好），策略模型学到的是「更像高分答案」而非「更正确」——语言评测版的 Goodhart，`reward model overoptimization` 里 proxy reward 升、gold reward 反降。
- **自证**：评委偏爱的格式被更多生成 → 训练数据更同质 → 新模型更像评委 → 评委更认可 → 表面分持续涨。评测从「测量仪器」变成「生态选择压力」。

对策不是退回全人工，而是把评委关进约束：能执行验证的别用 LLM 猜（代码跑测试、数学做校验、检索核对引用）；rubric 拆成可观测维度不让文风补偿事实错误；反事实扰动（换 A/B 顺序、压篇幅、隐身份）测评委是否看错东西；保留异质锚点让误差来源不相关；judge 当模型版本管理（换 judge = 换量尺，趋势线不能未经桥接直接续）；留一块优化看不见的审计集。

## Goodhart 不是评测专属：整条闭环都在优化「可测代理」

把上面三种失效里的 Goodhart 抽象一层，它其实不是评测独有的病，而是**闭环每一站都在犯的同一个结构错误**：真正的目标 `T` 昂贵或不可直接观测，于是各站都改优化一个便宜、可测的代理 `S`；只要施加足够优化压力，`S` 会一路升、`T` 却停滞甚至反转（proxy↑ / gold↓）。同一副骨架在闭环四个位置换了四身衣服：

```text
站位          真目标 T              被优化的代理 S         错位 / reward-hacking 形
数据·预训练    下游能力              固定语料上的 loss       语料污染让 loss 降却非泛化（20:1 是经验工作点非常数）
训练·后训练    人类真实偏好          learned reward model    proxy reward↑ / gold reward↓ ＝ reward overoptimization
训练·检索      检索相关性、真实延迟   语义相似度、FLOPS       semantic-similarity↔retrieval-relevance、FLOPS↔P99 双重错位
评测          线上风险 R_online     离线榜单 R_hat_eval     Goodhart / contamination / drift（本页三失效）
```

对应概念页各自把这一站拆开了：数据·预训练见 [[scaling-laws]]、后训练见 [[rlhf]]（家谱见 [[2026-07-18-dpo-kto-grpo-family]]）、检索见 [[sparse-retrieval]]（打分链的 FLOPS 代理错位见 [[2026-07-19-splade-mlm-head-term-scoring]]）。于是「评测端的 Goodhart」只是这台机器在**最后一站**的读数——它之所以最危险，是因为评测决定谁上线，等于把前几站的代理错位**聚合成一个决策**再写回数据环（见下文「与端到端闭环的关系」）。

也因此**防御手段在四站同构**：都不是「换一个更聪明的代理」，而是**周期性回锚真目标 T**——隐藏 holdout / gold reward 复核 / 真实 P99 压测 / 下游任务离线集，各自是同一句「别让 S 独自当家」在本站的落法。判断一个指标健不健康，就问一句：它是 `T` 本身，还是一个在足够压力下会与 `T` 分道扬镳的 `S`？

## 一张「评测身份证」

看任何榜单，先别看第一名，先找这几行小字——它们比总分更接近真相：

```text
1. Target       真正要改善的用户结果是什么？
2. Population    指标代表哪些用户/任务/语言/时间段？
3. Exposure      训练者/模型/检索库是否见过样本？
4. Adaptation    围绕这套指标做过多少轮选择？
5. Slices        哪些关键子群可能被平均数掩盖？
6. Cost          不同错误的业务/安全代价是否等权？
7. Freshness     上次刷新样本是什么时候？
8. Decision      什么结果触发上线/回滚/继续观察？
```

配套的是四层评测栈（互补而非替代）：训练内指标 → 固定离线集（便于比较、最易被适应性优化）→ 滚动隐藏集（查泛化与漂移）→ 线上 A/B 与人工审计（最贴近产品、最能发现自动 judge 漏了什么）。

## 分数是排序还是概率：估计器之前先问「在估计什么量」

前面把 benchmark 当成对风险 `R_online` 的有限样本估计器，但「估计器估的是哪种量」
本身就分叉：同一批输出既能当**排序分数**、也能当**概率**、还能当**决策依据**，三者是
互不蕴含的三道题。把分数做任意严格单调变换，排序（AUC）纹丝不动，概率含义却已改坏——
所以「AUC/accuracy 高」不能替概率质量背书。要评概率就得用**适当评分规则**（NLL、Brier）：
它们靠 excess risk 分解（log 的 `KL(q||p)`、Brier 的 `(p-q)^2`）让「诚实报告」成为唯一
最优，同时把 MLE/NLL/交叉熵/KL 收进同一框架；而 ECE 的分箱一旦整体平均，又会掉进本页
「聚合掩盖切片」的同一个坑（整体校准 ≠ 子群校准）。这条「分数语义」维度独立成页展开，
见 [[probability-calibration]]。[[2026-07-30-calibration-vs-ranking]]
[[2026-07-31-proper-scoring-rules-honest-probabilities]]

## 与端到端闭环的关系

评测不是链尾的「客观旁观」：它一旦决定哪个模型上线，就成了控制回路的一部分——评测偏差 → 选错模型 → 改变线上输出 → 改变用户行为与日志 → 改变下一轮训练数据 → 偏差被写回模型。这正是「端到端闭环·偏差传导」的评测版本，误差通过决策反向注入数据环节，而非停在报表最后一栏。

## 相关概念

- [[text-embedding]] — 编码端的实体 mismatch 与评测端聚合掩盖同构，都是过早聚合抹掉少数信号
- [[colbert-retrieval]] — late interaction 逐 token 保留局部信号，对应评测端 per-slice 拒绝过早聚合
- [[sparse-retrieval]] — 词表维 exact-match 保住少数信号
- [[rlhf]] — RLAIF / reward model overoptimization 是 judge 进入闭环的训练侧
- [[constitutional-ai]] — 从原则生成逐样本 AI 偏好的 RLAIF 范式
- [[probability-calibration]] — 分数语义维：区分/校准/决策效用三分与 proper scoring rule，本页缺席的「分数是排序还是概率」
- [[scaling-laws]] — 评测与 scaling 都要问「这个数在估计哪个分布上的什么量」

## 伴读来源

- [[2026-07-17-benchmark-failure-distribution]] — benchmark 作为估计器、contamination/Goodhart/drift 三支柱、四层评测栈
- [[2026-07-21-path-and-compass]] — 路径可学、指南针必须外置；LLM-as-judge 把评测升级为闭环控制、共盲/迎合/自证
- [[2026-07-25-aggregation-erases-minority-signals]] — 聚合抹平少数信号在编码端与评测端同构、可聚合性四问
- [[2026-07-18-dpo-kto-grpo-family]] — 训练站的代理错位：learned reward model 被优化到 proxy↑/gold↓（reward overoptimization），Goodhart 的后训练版本
- [[2026-07-19-splade-mlm-head-term-scoring]] — 检索站的代理错位：FLOPS 训练代理≠真实 P99 延迟，Goodhart 在效率轴的孪生
