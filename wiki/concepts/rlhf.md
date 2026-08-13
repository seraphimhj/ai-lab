---
title: RLHF — 基于人类反馈的强化学习
created: 2026-05-10
updated: 2026-08-13
type: concept
tags: [training, alignment, reinforcement-learning]
sources: [raw/papers/1909.08593-Fine-Tuning-Language-Models-from-Human-Preferences.html, raw/papers/2009.01325-Learning-to-summarize-from-human-feedback.html, raw/papers/2203.02155-Training-language-models-to-follow-instructions-with-human-f.html, raw/papers/2204.05862-Training-a-Helpful-and-Harmless-Assistant-with-Reinforcement.html]
---

# RLHF — 基于人类反馈的强化学习

通过人类偏好反馈训练奖励模型，再用强化学习优化语言模型，使其输出更符合人类期望。[[raw/papers/1909.08593-Fine-Tuning-Language-Models-from-Human-Preferences.html]]

## 核心流程

RLHF 训练分为三个阶段：

### 阶段一：监督微调（SFT）

在有标注的指令-回答对上微调预训练模型，使其具备基本的指令遵循能力。

### 阶段二：训练奖励模型（RM）

1. 收集人类偏好数据：对同一 prompt 的多个回答进行排序
2. 训练一个 Reward Model 预测人类偏好
3. 损失函数基于 Bradley-Terry 排序模型：
   ```
   L = -log σ(r(x, y_w) - r(x, y_l))
   ```
   其中 y_w 是人类偏好的回答，y_l 是较差的回答

### 阶段三：强化学习优化（PPO）

- 使用 PPO（Proximal Policy Optimization）优化策略模型
- 目标：最大化 RM 给出的奖励
- 加入 KL 散度惩罚，防止模型偏离 SFT 模型过远
- 避免奖励黑客（reward hacking）问题

## 关键变体

| 变体 | 核心思想 | 代表工作 |
|------|---------|---------|
| 摘要 RLHF | 首次大规模验证 RLHF 对文本生成质量的提升 | OpenAI [[raw/papers/2009.01325-Learning-to-summarize-from-human-feedback.html]] |
| InstructGPT | 三阶段 RLHF 用于指令遵循，让 1.3B 模型超越 175B [[raw/papers/2203.02155-Training-language-models-to-follow-instructions-with-human-f.html]] | OpenAI |
| HH-RLHF | 同时优化 helpful & harmless 双目标 [[raw/papers/2204.05862-Training-a-Helpful-and-Harmless-Assistant-with-Reinforcement.html]] | Anthropic |
| [[dpo]] | 把 RM 训练与 PPO 折叠成一次二分类，离线拟合成对偏好 | Rafailov 2023 |
| KTO | 只用单条 desirable/undesirable 标签、无需成对，损失厌恶式加权 | ContextualAI |
| GRPO | 无需 Critic Model 的组级 RL，[[deepseek]] R1 使用 | DeepSeek |

## 局限性

- **成本高**：需要大量高质量人类标注数据
- **奖励黑客**：模型可能学会欺骗奖励模型
- **分布偏移**：RL 优化过程中模型输出分布可能偏移
- **标注一致性**：不同标注员的偏好可能不一致

## 换一根轴：祖先不是三段流水线，而是「奖励减漂移」——DPO / KTO / GRPO 一张家谱

> 反哺自 07-18 伴读 [[2026-07-18-dpo-kto-grpo-family]]。上面「核心流程」把 RLHF 讲成
> SFT→RM→PPO 三段式，容易让人把 PPO 当成 RLHF 的本质、把 DPO/KTO/GRPO 当成三个按年份替代旧
> 方法的新算法。换一个更稳的抽象，这层误读就散了。

RLHF 的真正共同祖先不是那条流水线，而是一道目标：

```text
max  E[y~π(·|x)] r(x,y)  −  β · KL( π(·|x) ‖ π_ref(·|x) )
     └── 奖励项：生成更高奖励的回答      └── 漂移项：别为钻奖励空子离参考模型太远
```

第一项要「奖励」，第二项要「减漂移」。PPO 只是求解这道题的一个优化器；后来的方法再花哨，都可
以只追问三件事——**奖励信号从哪来、KL 锚拴在哪、数据何时产生**。这三根轴彼此正交，DPO/KTO/GRPO
不过是在三根轴上各挪了位置：

| 方法 | reward 从哪来 | KL 锚在哪里 | 数据何时产生 |
|------|--------------|-------------|-------------|
| [[dpo]] | 成对人工/模型偏好（chosen>rejected） | 隐式：`log π_θ − log π_ref` 折进损失 | 离线 |
| KTO | 单条 desirable/undesirable 标签 | 隐式对数比 + 一个分布参考点 | 离线 |
| GRPO | 规则验证器或 reward model 的标量分 | 显式：目标里外挂 KL 惩罚 | 在线采样 |

一张更准的家谱是「按数据闭环分叉」，不是「按名字排先后」：

```text
                带 KL 正则的奖励最大化（= 奖励减漂移）
                              |
             +----------------+----------------+
             |                                 |
      离线偏好拟合                         在线策略优化
             |                                 |
       +-----+-----+                         GRPO
       |           |                   (PPO 家族，去掉 critic：
    paired      unpaired               组内均值当基线，省一套价值网络)
     DPO          KTO
```

**核心新洞见——DPO/KTO 与 GRPO 改的根本不是同一件事，所以「谁更先进」是个坏问题。**

- **DPO/KTO 重写的是「反馈→损失」这个接口**：从成对偏好降到单条二元标签，是在换你必须采集
  什么数据。KTO 不是「DPO 删掉 rejected」——删掉配对后，DPO 里本会自动消去的提示相关常数 C(x)
  不再消失，必须另造一个分布参考点，反馈更便宜、信用分配更粗。
- **GRPO 重写的是「在线 RL 里优势怎么估」**：它保留「采样→奖励→更新」的在线闭环，只把 PPO 的
  learned critic 换成 group-relative baseline——同一提示采 G 个答案，用组内均值当基线、组内标准化
  得相对优势 `A_i=(r_i−mean)/std`。省掉一套价值网络，代价是把压力转给采样质量与奖励设计（同组
  全对或全错、std≈0 时几乎没有学习信号）。这跟 [[dpo]] 的 KL 折叠是**正交**的两步棋。

于是选型的第一顺位不是损失函数，而是**反馈系统与数据闭环**：反馈是成对比较 / 单条标签 / 可自动
验证的标量？能否承受在线生成的算力与分布漂移？任务要探索新策略还是离线数据已覆盖目标行为？

两处交叉值得记一笔：① GRPO 的组内标准化与信息检索的 **query-level normalization** 同形——不同
query 的原始分不可直比，先在每个 query 的候选集内做相对排序（呼应 [[sparse-retrieval]] 的
per-query 归一化）；② 这张家谱把 07-18 note 的终局问题留给了 [[benchmark-evaluation]]——当 reward
model / 验证器 / LLM-judge 本身也随训练迭代时，π_ref 还是够稳的「锚」吗，还是已进入奖励·策略·
评测者三者共漂、而现有 KL 只约束了其中一条边的系统？可验证奖励（RLVR）为何能退回「几乎不让权」，
另有一条 pick 在 `queries/picks.md` 待推。

## 奖励模型也是一台概率报告器：Bradley-Terry 的「诚实」诚实拟合的是谁

> 反哺自 07-31 伴读 [[2026-07-31-proper-scoring-rules-honest-probabilities]]。把上面「局限性」里
> 那条孤零零的**奖励黑客**接到一个更硬的机制上——它不是 RM 训坏的意外，而是 RM 训得**太诚实**的必然。

阶段二那条 Bradley-Terry 损失 `L=-log σ(r(x,y_w)−r(x,y_l))` 本质上是一条**适当评分规则**
（proper scoring rule）：把「这一对里 w 是否胜出」当成二分类，σ(Δr) 就是 RM 报告的偏好概率，
这条 NLL 与 [[probability-calibration]] 里的 log loss 同形，同一套「如实报告 `p=q` 才是唯一期望
最优」的激励结构在逼 RM 诚实地报出它相信的偏好概率。到这一层，RM 是一台被 proper scoring 校准
过、越练越诚实的概率报告器。

危险恰恰在「诚实」二字的对象上。properness 只保证 `p` 追向**被评分的标签分布**——这里就是
**标注者群体的偏好分布**，而不是「什么才是更好的回答」这个业务真相：

```text
Bradley-Terry / log loss  proper
      +--> RM 的偏好概率诚实追向「标注者爱选哪个」
      -X-> 标注者爱选的 = 真正更好的（长度/格式/位置/谄媚偏置全在污染这个 q）
```

于是「奖励黑客」换一个说法就散了它的偶然性：**RM 越是一台校准良好的概率报告器，它越忠实地把
「标注者爱看什么」而非「什么是对的」编码进奖励**，policy 再把这些系统性偏置当作真目标去最大化。
阶段三那个 KL 锚只拦得住**策略漂移**（别离 π_ref 太远），拦不住这层更深的「诚实地测量了错的
对象」——它约束的是 π 到 π_ref 的距离，不是 r 到真相的距离。这正是 [[probability-calibration]]
的终局问题落在对齐上的形状：当「真相」本身由反馈过程生成，properness 到底该相对于谁来定义？
可验证奖励（RLVR）之所以能抗 reward hacking，正是把 `q` 从「标注者偏好」换成「验证器判定的
0/1」这个不被口味污染的分布（另有 pick 待推）。

## 相关概念

- [[dpo]] — 家谱里「离线·成对偏好」这一支：把 RM+PPO 折叠成一次二分类
- [[probability-calibration]] — RM 的 Bradley-Terry 是一条 proper scoring rule；奖励黑客=它诚实拟合了标注者偏好分布而非真相
- [[constitutional-ai]] — 用 AI 反馈替代部分人类反馈
- [[instruction-tuning]] — RLHF 的前置步骤 SFT
- [[benchmark-evaluation]] — 家谱的终局问题落点：reward/policy/judge 共漂时 KL 只锚住一条边
- [[2026-07-18-dpo-kto-grpo-family]] — 反哺来源（三轴家谱：reward 从哪来 / KL 锚在哪 / 数据何时产生）
- [[2026-07-31-proper-scoring-rules-honest-probabilities]] — 反哺来源（Bradley-Terry=proper scoring rule，奖励黑客=RM 诚实拟合标注者偏好分布而非真相）
