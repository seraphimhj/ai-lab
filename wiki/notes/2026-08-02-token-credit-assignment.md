# 一条梯度看懂 SFT、DPO、PPO 与 GRPO：奖励到底该算到哪个 token 头上？

> 本次命中：**统一数学框架 + retrieval 以外·后训练 + 端到端闭环**；重点补上此前“方法家谱”背后的共同骨架：许多后训练方法都在更新 token 的 log-probability，真正不同的是——**谁给每个 token 分配多大的学习权重**。

## 全局地图

### 一句话摘要

SFT、DPO、PPO/GRPO 看似使用不同 loss，梯度却大多能读成同一句话：**提高某些已采样 token 的概率、降低另一些 token 的概率；方法之间最关键的差别，是权重从哪里来，以及一条序列的总奖励如何被分摊到各 token。**

### 结构地图

```text
prompt x
   |
   v
模型逐 token 生成 y_1 ... y_T
   |
   v
得到监督信号
   |
   +-- 标准答案 ----------------> SFT
   +-- chosen / rejected --------> DPO
   +-- reward / verifier --------> PPO, GRPO
   |
   v
把信号变成权重 w_t
   |
   v
更新每一步 log pi(y_t | x, y_<t)

共同骨架：loss gradient = - sum_t w_t * gradient log pi_t
                                   |
                                   v
真正的难题：w_t 应该给谁、给多少？
```

### 段落分类（Agent 判断）

- `[骨]` 自回归序列概率把整段学习还原为 token log-probability 之和
- `[骨]` 一条统一梯度：方法差别主要藏在权重 `w_t`
- `[肌]` SFT、DPO、PPO、GRPO 分别如何产生权重
- `[骨]` 序列级奖励广播给所有 token，会制造 credit assignment 问题
- `[骨]` 训练目标、采样和评测必须闭环检查，不能只看 loss 名字

---

## 一、先把“整条回答的概率”拆开

### `[骨]` 模型从来不是一次生成整段，而是连续做 T 次分类

对 prompt `x` 和回答 `y = (y_1, ..., y_T)`，自回归模型写成：

```text
pi(y | x) = product_t pi(y_t | x, y_<t)
```

取对数后：

```text
log pi(y | x) = sum_t log pi(y_t | x, y_<t)
```

这一步极重要：序列级的概率乘积，被变成 token 级 log-probability 的求和。于是，不管最终信号来自标准答案、偏好对，还是奖励模型，参数更新最终都要落到某些 `log pi(y_t | ...)` 上。

把最常见的更新抽象成：

```text
gradient loss = - sum_t w_t * gradient log pi(y_t | x, y_<t)
```

- `w_t > 0`：提高这个 token 在当前上下文中的概率；
- `w_t < 0`：压低它的概率；
- `|w_t|` 越大：这一步承担的学习力度越大；
- `w_t = 0`：这个 token 不从该样本获得更新。

严格说，各算法还会有 KL、value loss、entropy、clipping 等附加项；但如果你只想先抓住 policy 更新的主干，这个式子足够有穿透力。

**结构标注：全文的数学骨架。** loss 的名字会变，落到模型参数上的基本动作仍是“带权调整 token 的 log-probability”。

### 碰撞问题 1

你过去看到“序列奖励是 1”时，是否会自然理解成“整条序列都做对了”？

真正需要警惕的是：**序列得 1，只说明某个最终判据通过了；它并没有告诉我们，序列里的每一个 token 都同样有功。**

---

## 二、SFT：最简单，也最强硬的权重分配

### `[肌]` 标准答案中的每个 token，默认都被当成正例

SFT 的负对数似然为：

```text
L_SFT = - sum_t log pi(y*_t | x, y*_<t)
```

与统一式对照：

```text
w_t = 1    for every target token
```

它的隐含判断非常强：数据集里的目标回答不仅“整体可接受”，而且在 teacher forcing 给定正确前缀时，**每一个实际出现的 token 都值得提高概率**。

这也是 SFT 稳定的原因：

- 不需要模型自己探索；
- 不需要估计 reward；
- 每个位置都有稠密监督；
- 梯度方差低。

但它的局限与优点来自同一处。若答案包含多余套话、偶然措辞，甚至一处局部错误，SFT 仍会把它们当成权重为 1 的正例。SFT 学的是“模仿这条轨迹”，不是“只保留这条轨迹中真正导致成功的部分”。

一个经常被忽略的变化是 loss mask：如果只对 assistant answer 计 loss，而不对 system/user prompt 计 loss，本质上就是把不该学习的位置设为 `w_t = 0`。这已经是最朴素的 credit assignment。

**结构标注：第一个实例。** SFT 不是没有 credit assignment，而是采用“目标区间内人人同功”的最简单分配。

---

## 三、DPO：比较两条序列，但更新仍落到 token 上

### `[肌]` DPO 先比较“相对参考模型，这两条回答谁被抬高得更多”

对 chosen 回答 `y+`、rejected 回答 `y-`，DPO 的核心 margin 可写成：

```text
m = beta * [
      log pi_theta(y+|x) - log pi_ref(y+|x)
    - log pi_theta(y-|x) + log pi_ref(y-|x)
]

L_DPO = -log sigmoid(m)
```

首次出现的几个词：

- `reference policy`（参考策略）：通常是 SFT 模型，用来限制新策略偏离原行为太远；
- `beta`：控制相对参考模型的偏离尺度；
- `margin`（间隔）：chosen 相对 rejected 被提升了多少。

因为每个序列的 `log pi(y|x)` 仍是 token log-probability 之和，所以 DPO 的一次更新可以读成：

```text
chosen 的 token： 统一向上推
rejected 的 token：统一向下压
力度：由当前 margin 是否已足够大决定
```

如果模型已经明显偏爱 chosen，`sigmoid` 进入饱和区，样本权重变小；如果模型还偏爱 rejected，这对样本会得到更大的纠偏力度。

这里要精确一点：同一条序列中的 token 会共享一个由 pair margin 产生的标量系数，但每个 token 的 `gradient log pi_t` 并不相同，所以参数变化并非机械地平均分给 token。可是，**偏好标签本身没有告诉 DPO：chosen 究竟好在哪几个 token，rejected 又坏在哪几个 token。**

例如：

```text
chosen:  前 180 个 token 普通，最后给出正确结论
rejected: 前 180 个 token 普通，最后一个符号写反
```

纯序列级 DPO 会提高 chosen 整条轨迹、压低 rejected 整条轨迹。两条回答共有的大量合理推理，也被卷入更新。若数据中的 chosen/rejected 差异很大，这种“整段归因”会更粗。

**结构标注：第二个实例。** DPO 改变的是权重来源——从“标准答案存在”变成“成对偏好 margin”；它没有自动解决 token 级归因。

### 碰撞问题 2

DPO 常被说成“比 RL 简单、稳定”。但如果偏好只由回答最后一句决定，整条 chosen 序列都被奖励，这究竟是合理泛化，还是误把相关 token 当成因果 token？

答案取决于数据：如果 chosen 的整体写法都更好，序列级归因可能够用；如果差异只集中在局部，token/process-level 标签会更精准。

---

## 四、REINFORCE / PPO：让采样结果决定权重

### `[骨]` Policy gradient 的核心不是“奖励越大越好”，而是“比预期更好才上调”

最基础的 policy-gradient 形式是：

```text
gradient J = E[ sum_t A_t * gradient log pi(y_t | s_t) ]
```

其中：

- `state s_t`：prompt 加已生成前缀；
- `action`：当前采样的 token；
- `return`：从当前步往后得到的累计奖励；
- `advantage A_t`（优势）：这个动作的结果比基线预期好多少。

若只用最终序列奖励 `R`，最朴素的 REINFORCE 会近似成：

```text
A_t = R - baseline
```

于是同一序列中的所有 token 常共享同一个最终奖励信号。`baseline` 不改变期望梯度，却会显著降低方差：不是“得正分就提高”，而是“比同类情境下预期更好才提高”。

PPO 在这根主干上加了两道护栏：

1. 用 importance ratio 衡量新旧策略对已采样 token 的概率变化；
2. 用 clipping 阻止单批数据把策略推得过远。

概念化地写：

```text
ratio_t = pi_new(y_t|s_t) / pi_old(y_t|s_t)

objective_t = min(
  ratio_t * A_t,
  clip(ratio_t, 1-eps, 1+eps) * A_t
)
```

`A_t` 决定方向，`ratio/clipping` 限制步幅。RLHF 里通常还会对偏离参考模型加入 KL 代价。所以 PPO 不是换掉了“加权 log-probability”骨架，而是在**权重估计与更新幅度**上增加控制系统。

**结构标注：第三个实例。** PPO 的复杂主要来自 on-policy 采样、advantage/value 估计和受约束更新，而不是来自一种完全不同的学习原理。

---

## 五、GRPO：去掉 value model，不等于去掉 baseline

### `[肌]` 同一题采一组回答，用组内相对成绩构造 advantage

GRPO 的直觉可写成：对同一 prompt 采样一组回答，得到奖励 `r_1 ... r_G`，再标准化：

```text
A_i = (r_i - mean(r_1...r_G)) / (std(r_1...r_G) + epsilon)
```

这使得：

- 高于同组平均的回答被上调；
- 低于同组平均的回答被下调；
- 题目整体偏难或偏易的影响被部分抵消；
- 不必单独训练一个 value model 来预测 baseline。

所以“GRPO 没有 critic”不应被理解为“GRPO 不需要基线”。它把学习出来的 value baseline，换成了**同 prompt 多次采样形成的经验组基线**。

与统一式对照，GRPO 的关键变化是：

```text
w_t ~= group-relative advantage * policy-ratio control
```

若奖励只在回答结束时给出，某条回答内部通常仍有粗粒度广播：同一回答中的 token 共享这个组相对优势。它解决了“不同 prompt 的 reward 尺度难比”和“value model 成本高”的一部分问题，却没有凭空获得局部推理步骤的因果归因。

还有一个边界条件：若组内所有回答奖励都一样，`std` 接近 0，组内就几乎没有可用于排序的学习信号。**采样多样性、reward 能否拉开差距、组大小**，因此不是外围工程参数，而是直接决定梯度是否存在的数据环节。

**结构标注：第四个实例。** GRPO 重写的是 baseline 的来源，不是 policy-gradient 的底层语法。

---

## 六、真正的薄弱点：最终奖励该不该广播给整条链？

### `[骨]` Credit assignment 是“谁导致了结果”，不是“谁出现在结果之前”

设模型解一道题：

```text
1. 选对公式
2. 代入数值
3. 中间算术写错
4. 后面忠实沿用错误
5. 最终答案错误，reward = 0
```

如果把 `reward = 0` 或负 advantage 广播给所有 token，第一步那个正确公式也受到压制。反过来，模型若推理错误但碰巧猜中最终答案，所有步骤都可能被奖励。

这就是 temporal credit assignment（时间信用分配）：**一个延迟出现的结果，要如何归因给此前的一长串决策？**

```text
最终奖励
   |
   +-- 粗粒度：整条序列共享 -------- 简单、便宜、方差可能较大
   |
   +-- token/value 估计 ------------ 更细，但依赖 critic 准确性
   |
   +-- process reward -------------- 标步骤对错，但标注昂贵
   |
   +-- verifier 定位首错点 -------- 更可执行，但只适用于可验证任务
   |
   +-- 对比式局部改写 -------------- 控制变量强，但数据构造复杂
```

这里出现一个与 07-25“拒绝过早聚合”完全同构的结构：

```text
检索：整句过早压成一个向量 -> 实体信号被淹没
评测：整集过早压成一个均值 -> 失败子集被淹没
后训练：整条轨迹过早压成一个 reward -> 关键步骤被淹没
```

三处问题都不是“聚合一定错”，而是：**聚合以后，哪个维度再也恢复不出来？** 序列只剩一个分数后，你无法仅从这个分数反推出究竟哪个 token 应受奖惩。

### 一条逆光注疏：既然归因这么粗，为什么 sequence-level reward 仍有效？

最强反驳是：语言中的 token 高度耦合，局部步骤很难独立定义；只要对大量样本取期望，真正有助于成功的模式会更常出现在高奖励轨迹中，policy gradient 仍能统计地找出方向。

这确实成立，也是序列级 RL 能工作的原因。但它依赖三个条件：

1. 探索能产生足够多样的轨迹；
2. reward 与真实目标相关，而非可博弈 proxy；
3. 数据量足以让偶然相关逐渐抵消。

一旦 reward 稀疏、任务 horizon 很长、采样模式单一，或者 judge 有系统性偏置，粗归因就会把错误方向稳定地放大。

**结构标注：核心矛盾。** 细粒度归因更准却更贵、更可能引入错误标注；粗粒度归因便宜，却把统计相关当作局部信用。

### 碰撞问题 3

如果 verifier 只检查最终答案，而模型学会省略推理、直接猜答案，reward 上升是否等于推理能力上升？

这不是纯评测问题。因为 verifier 进入训练后，**它能看见什么，就定义了模型有动力学什么。**

---

## 七、把四种方法放回同一张表

| 方法 | 信号从哪来 | 典型权重形状 | baseline / 锚 | 主要盲点 |
|---|---|---|---|---|
| SFT | 目标序列 | 目标 token 通常全为 `+1` | 数据分布本身 | 好坏 token 一起模仿 |
| DPO | chosen/rejected pair | chosen 上调、rejected 下调，力度取决于 margin | reference policy | 偏好通常只到序列级 |
| PPO | 在线采样 reward | advantage 决定方向，clip 限步幅 | value baseline + old/ref policy | critic 误差、训练复杂、归因仍可能粗 |
| GRPO | 同 prompt 组内 reward | 组相对 advantage | group mean/std + ref policy | 依赖组内多样性；无分差就无信号 |

最值得记的不是表格，而是这个阅读算法：以后遇到一个新 loss，先问四个问题。

```text
1. 被提高/压低的是哪个 log-probability？
2. 权重 w 从标签、偏好、reward，还是 verifier 来？
3. baseline 或 reference 是谁？它消方差还是限制漂移？
4. 信号粒度到 sequence、step，还是 token？
```

只要这四问能答出来，大多数“新后训练算法”就不再是一座新孤岛。

---

## 八、端到端闭环：不要只比较 loss，要检查五个接口

### `[骨]` 同一个目标函数，换采样与评测，也可能变成另一套系统

```text
数据 / prompt 分布
      |
      v
采样策略：温度、组大小、旧策略
      |
      v
信号：答案、偏好、reward、verifier
      |
      v
归因：sequence / step / token 权重
      |
      v
更新约束：reference、KL、clip
      |
      v
离线评测与线上行为
      |
      +-------------------- feedback --------------------+
```

逐环看偏差如何传：

- **数据**：若训练题型窄，权重再精确也只优化窄分布；
- **采样**：若组内答案几乎相同，GRPO 没有对比信号；
- **奖励**：若 judge 奖励冗长，advantage 会忠实地鼓励冗长；
- **归因**：若最终分数广播全序列，局部错误位置不可见；
- **约束**：KL/clip 太强学不动，太弱则 exploit reward；
- **评测**：若仍用同一个 reward model 验收，proxy hacking 会被误认成进步。

因此，“PPO 还是 GRPO”“DPO 还是 RL”往往问得太早。更先要问的是：**你的反馈信号能否区分好坏？能区分到什么粒度？错误权重一旦产生，会经采样闭环被放大多少次？**

**结构标注：闭环收束。** 目标函数只是链条中的一个变换器；它不能创造 reward 里没有的信息。

---

## 全文复盘

### 理解轨迹

```text
“每种后训练方法有一种新 loss”
              |
              v
序列 log-probability = token log-probability 之和
              |
              v
共同更新 = 带权调整 token log-probability
              |
              v
SFT / DPO / PPO / GRPO 的差别落到 w_t 的来源
              |
              v
看见 sequence reward 无法自动定位关键 token
              |
              v
把 credit assignment 接回数据、采样、评测闭环
```

### 读后一句话（不可跳过）

**读完之后，你最想对“最终答案对了，就奖励整条推理”这件事说的一句话是什么？**

不要复述本文。试着给出边界判断，例如：“在什么任务上我愿意接受这种粗归因；在什么任务上我一定要求过程验证？”

### 终局问题

如果过程奖励模型能逐步指出错误，它本身也可能把某一种“标准解题风格”误当成正确推理。**我们是在解决 credit assignment，还是把最终答案 judge 的偏置搬到了每一个步骤？**

### 术语表

| English | 中文 | 本文含义 | 位置 |
|---|---|---|---|
| log-probability | 对数概率 | 把序列概率乘积转成 token 分数之和 | 第一节 |
| credit assignment | 信用分配 / 归因 | 决定哪些动作应为最终结果受奖惩 | 第六节 |
| advantage | 优势 | 某动作结果相对基线好多少 | 第四节 |
| baseline | 基线 | 降低 policy-gradient 方差的参照 | 第四、五节 |
| reference policy | 参考策略 | 限制新策略偏离原模型的锚 | 第三、四节 |
| policy ratio | 策略概率比 | 新旧策略对同一采样动作的概率变化 | 第四节 |
| clipping | 截断 | 限制 PPO 单次策略更新幅度 | 第四节 |
| process reward | 过程奖励 | 对中间推理步骤而非只对结局评分 | 第六节 |
| reward hacking | 奖励投机 | 提高代理奖励但不提高真实质量 | 第八节 |

### 下一步线索

1. Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed., Chapter 13：重点看 policy-gradient theorem、REINFORCE with baseline，理解“baseline 为什么不改变期望梯度”。  
   http://incompleteideas.net/book/the-book-2nd.html
2. Schulman et al., *Proximal Policy Optimization Algorithms*：重点看 clipped surrogate objective，分清 advantage 决定方向、clip 限制步幅。  
   https://arxiv.org/abs/1707.06347
3. Rafailov et al., *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*：重点看 DPO objective 如何由隐式 reward 与 reference policy 推出。  
   https://arxiv.org/abs/2305.18290
4. Shao et al., *DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models*：重点看 GRPO 如何用 group-relative score 代替单独的 critic/value model。  
   https://arxiv.org/abs/2402.03300
