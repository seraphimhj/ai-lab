---
title: Self-RAG — 自我反思检索增强生成
created: 2026-05-10
updated: 2026-08-16
type: concept
tags: [retrieval, generation, agent]
sources: [raw/papers/2310.11511-Self-RAG-Learning-to-Retrieve-Generate-and-Critique-through-Self-Reflection.html, raw/papers/2401.15884-Corrective-Retrieval-Augmented-Generation.html]
---

# Self-RAG — 自我反思检索增强生成

通过在生成过程中引入反思标记（Reflection Tokens），让模型自主决定何时检索、何时使用检索结果、以及生成内容是否需要修正。[[raw/papers/2310.11511-Self-RAG-Learning-to-Retrieve-Generate-and-Critique-through-Self-Reflection.html]]

## 核心问题

标准 [[retrieval-augmented-generation]] 的局限：
- **过度检索**：简单问题也检索，浪费资源
- **检索噪声**：检索结果可能不相关，干扰生成
- **无自我判断**：无法评估生成质量

## Self-RAG 的解决方案

### 四种反思标记

| 标记 | 含义 | 作用 |
|------|------|------|
| Retrieve | 是否需要检索 | 自主决定是否调用检索器 |
| IsRel | 检索文档是否相关 | 过滤不相关文档 |
| IsSup | 生成是否被检索支持 | 检测幻觉 |
| IsUse | 检索是否有用 | 判断检索的实际价值 |

### 生成流程

```
Input → [Retrieve?] 
  → Yes → Retrieve → [IsRel?] → [IsUse?] → Generate → [IsSup?]
  → No → Generate → [IsSup?]
```

模型在每个关键决策点生成对应的反思标记，实现自适应检索和生成。

## 训练方法

### 三阶段训练

1. **反思标记预测**：训练模型生成反思标记
2. **批评任务**：训练模型评估生成质量
3. **生成微调**：结合反思能力进行端到端微调

### 训练数据构造

- 使用强检索器获取正/负文档
- 用语言模型生成 critique
- 标注生成内容是否被文档支持

## 效果

Self-RAG（7B 和 13B 参数）在六个任务上的表现：
- 显著优于 retrieval-augmented ChatGPT（在 4 个任务上）
- 超过 Llama2-chat 和 Alpaca（在所有任务上）
- 在 Open-domain QA、推理和事实验证任务上全面领先
- 长文本生成的事实准确性和引用精度显著提升
- 推理时可通过 reflection token 概率的加权线性和进行 segment-level beam search，实现可定制化解码

## CRAG — 纠正式检索增强生成

CRAG（Corrective Retrieval Augmented Generation）[[raw/papers/2401.15884-Corrective-Retrieval-Augmented-Generation.html]] 是另一种改进 RAG 鲁棒性的方法：

### 核心机制

1. **检索评估器**：轻量级模型评估检索文档质量，返回置信度
2. **三种触发动作**：
   - 置信度高 → 直接使用检索结果
   - 置信度低 → 触发大规模 web 搜索补充
   - 中间状态 → decompose-then-recompose 过滤无关信息
3. **信息萃取**：分解检索文档，选择性聚焦关键信息

### 特点

- Plug-and-play，可与各种 RAG 方法无缝结合
- 在短文本和长文本生成任务上均有显著提升

## 换一根轴：不是「多一个评分器」，而是把检索改成可决策的动作（07-26 伴读反哺）

上面按「反思标记 / 三态触发」把 Self-RAG、CRAG 讲成两套改鲁棒性的机制清单。[[2026-07-26-self-rag-crag-agentic-retrieval]] 伴读换了一根更本质的轴：**真正变的不是多挂了一个打分器，而是控制流**——检索从一次性的生成前预处理，变成可以跳过、重做、降权、验证的动作。分水岭因此不在「有没有评分」，而在**评价结果会不会改变下一步动作**：只让模型多写一段「自我反思」而控制流照旧，不算纠错，只是把黑箱又叠了一层。

### 病灶重述：召回是候选生成，不是事实认证

标准 RAG 把 retriever 当「事实供应器」，但它只回答了一件事：*哪些文本在表示空间里最像这个 query*。它没承诺文档真的支持模型即将写出的那句话。于是要把两个此前容易混用的指标拆开：

```text
retrieval relevance:  文档和问题相关吗?     ← SPLADE/ColBERT/MUVERA 优化的是这个
claim support:        文档能推出这句回答吗?  ← 召回率再高也不保证
```

一篇乔布斯传记与「乔布斯哪年出生」高度相关，但若截取段落里没有出生年份，它对该 claim 就是「相关但不支持」。**检索错误不是普通噪声——一旦进入上下文，它会获得证据的外观**，把模型原本的「不知道」升级成「拿着错证据自信地说」。Recall@k 治的是候选缺失，治不了证据误用。

### 核心新洞见：Self-RAG 与 CRAG 是两处不同的保险丝，不是替代关系

按「拦哪一类故障、故障在链条哪一环」重排，两者覆盖的是不同故障面：

```text
query → retriever
          │
          ├─ CRAG evaluator ──── 拦「坏证据进入上下文」（生成前、外置质检站）
          │
        generator
          │
          └─ Self-RAG ISSUP ──── 拦「答案越过证据边界」（生成中、内生控制变量）
          │
        answer
```

这正是 [[2026-07-27-context-engineering-error-firebreaks|故障域设计]]那根轴在检索环的复现：可靠性不来自组件不犯错，而来自**在误差跨环传播之前放保险丝**——直接接住 [[react-agent]] 的 07-20 误差复合诊断（单步误差独立、闭环误差复合），把「误差从哪注入」翻到「在哪一环拦下、拦的是哪一类」。CRAG 的 evaluator 与 reranker 也不同：reranker 在候选池内问「谁更好」，evaluator 问「这批还能不能用」——Incorrect 分支允许承认候选池整体失效、换知识源，这是从 ranking 到 control 的一步。

### 四类判断为什么不能压成一个 confidence

Retrieve / ISREL / ISSUP / ISUSE 各问不同的事、各对应不同的补救动作（跳过检索 / 换文档 / 补证据改写 claim / 重组答案）。把它们加权求和成一个总分，就会丢掉故障位置——「文档相关=是、事实支持=是、回答有用=否」（只讲了正确的原理史却没回答「怎么修」）这种组合会被一个平均分抹平。这与 [[2026-07-25-aggregation-erases-minority-signals|过早聚合抹掉少数信号]]同构：**别只报一个总分，用评分维度定位错误发生在哪一环**。CRAG 的 Ambiguous 三态同理——不把中间分硬切成对/错，让「不确定」拥有一种不能被忽略的表示（≈ 类型系统里的 `Option`/`Result`，不允许不确定悄悄伪装成确定值）。

### 一句话把定义抬一层

Agentic RAG 的本质不是「多调几次搜索」，而是**让检索质量影响控制流**——检索被降格为一个带质检与回退路径的可决策动作，评分只有真正改变后续动作时才有价值。

## 交叉：同一副「便宜提议 + 核验」骨架，为什么投机解码是无损的、而 Self-RAG 不是（07-23 × 07-26 反哺）

把上面的控制流再抬一层，会撞见另一个子系统里一模一样的形状。[[2026-07-23-speculative-decoding-latency|投机解码]]的结构是：便宜的 draft 模型先串行猜 k 个候选，昂贵的 target 模型在一次前向里并行核验、接受最长正确前缀、在首个拒绝处纠正。Self-RAG/CRAG 的结构是：便宜的 retriever 先提出候选证据，一个 verifier（CRAG evaluator / Self-RAG ISSUP）核验它能不能支持即将写出的 claim、不合格就丢弃/补检/改写。**两者是同一副「让一个不可靠但便宜的提议器跑在前面，用一个核验器兜住质量」骨架**——提议器只决定速度与覆盖面，核验器才决定最终保证。这正是本页「保险丝」框架与 [[llm-inference-serving]] 延迟账的合流：一个把保险丝放在 decode 轮次上（拦「draft 猜错」），一个放在证据边界上（拦「答案越过证据」）。

但把两者并排，最有信息量的是它们**不**同构的那一处——核验器的性质天差地别：

```text
              提议器(便宜/不可靠)     核验器            最终保证
投机解码       draft 模型猜 token      target 一次并行验  精确：拒绝采样从残差
                                                        max(0,p−q) 重采，输出
                                                        严格服从 p —— 无损
Self-RAG/CRAG  retriever 召回证据      ISSUP/evaluator   概率：核验器自己是个
                                       打分              会错的学习判据，无硬保证
```

投机解码的核验器是一条**可证明正确**的接受-拒绝规则（呼应 [[dpo]]/[[probability-calibration]] 那副 KL 骨架：接受率 α 本质是 draft 分布 q 与 target 分布 p 的失配代价，失配越大存活前缀越短），所以它能把「便宜提议」的全部风险都吸收掉、输出分布一个 bit 都不偏。Self-RAG 的核验器却是它自己训练出来的一个 ISSUP 判据——它会漏判、会被表面相关性骗，于是「证据支持」这件事没有硬保证，只是把幻觉概率压低。**这条分界线正是本库反复出现的那个问题**：核验器一旦从「可执行的精确规则」退化成「一个会被优化的学习判据」，就回到 [[benchmark-evaluation]] 的 Goodhart 脊——谁来核验核验器？（也正是 pending 的【RLVR/GRPO】pick 的题眼：可验证域里 verifier 是 0/1 硬事实、退回投机解码那一侧的「精确核验」，开放生成里 verifier 是 judge、落在 Self-RAG 这一侧的「概率核验」。）一句话收口：**propose-verify 是通用的可靠性模式，但你拿到的是无损保证还是概率保证，全看那个核验器是「规则」还是「模型」。**

## 相关概念

- [[llm-inference-serving]] — 投机解码是同一副 propose-verify 骨架在推理延迟账上的落点（精确核验器一端）
- [[retrieval-augmented-generation]] — Self-RAG 的基础框架
- [[react-agent]] — 类似的反思循环思想；07-20 误差复合是本页「保险丝」框架的上游诊断
- [[context-engineering]] — 故障域设计/错误保险丝那根轴，Self-RAG/CRAG 是它在检索环的两处落点
- [[graph-rag]] — 另一种 RAG 改进方向
- [[dense-passage-retrieval]] — Self-RAG 中使用的检索方法
- [[colbert-retrieval]] — 可作为 Self-RAG 检索器的替代方案
