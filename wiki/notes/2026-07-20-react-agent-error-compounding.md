#+title: 伴读：Agent 的多步闭环——误差如何在 ReAct 循环里复合
#+date: [2026-07-20 Mon 09:02]
#+filetags: :reading:agent:react:context-engineering:evaluation:
#+identifier: 20260720T090222
#+source: Yao et al., ReAct: Synergizing Reasoning and Acting in Language Models (arXiv:2210.03629, ICLR 2023)

* 命中点

本次命中 *端到端闭环·偏差传导* 与 *Agent / 工具使用 / 上下文工程主线*：重点不是再介绍一遍 ReAct，而是追踪一次小偏差怎样经过 `Thought -> Action -> Observation -> Context` 回灌，最后变成任务失败，以及 context engineering 应在哪些接口截断它。

* 全局地图

** 一句话摘要

Agent 的危险不只是“每一步都可能错”，而是 *错误会改变下一步看到的世界*；长任务成功率近似指数下降只是第一层，更深一层是错误让后续条件分布变坏、形成相关且自激的闭环，而有效的上下文工程就是在回灌之前做校验、保真、压缩、记账与恢复。

** 结构地图

#+begin_example
目标 G
  |
  v
Thought_t ------> Action_t ------> Tool / Environment
  ^                  |                    |
  |                  |                    v
  +---- Context_t <--+------------- Observation_t
           |
           +-- 历史轨迹、状态摘要、工具返回、错误信息
           |
           +-- 下一轮再次进入模型

三条失败路径：

独立失误：       某一步错了，但没有污染后续
状态污染：       错误 action 改变环境，后续基于错误状态继续
信念污染：       错误 thought/observation 写入 context，被后续当成事实

五道拦截器：

Action schema -> 执行前验证 -> Observation 保真 -> 状态账本 -> 失败恢复
#+end_example

** 段落分类（Agent 判断，可覆盖）

- [骨] 从单步预测到闭环策略：模型的输出会成为下一步输入
- [骨] 为什么 `p^H` 会出现，以及它不等于“误差独立”
- [骨] ReAct 四个接口分别在哪里注入偏差
- [肌] 一个“查论文并写结论”的逐步失控案例
- [骨] ReAct 论文自己的失败分析：接地减少幻觉，却增加搜索与循环错误
- [骨] context engineering 不是“塞更多上下文”，而是控制回灌通道
- [肌] 一套可落地的 Agent 可靠性账本与评测指标
- [骨] 最强反对：反馈也能纠错，为什么一定会复合？

* 逐段伴读

** 第一段：[骨] 单步模型在做预测，Agent 在运行一个反馈系统

*** 原文锚点

#+begin_quote
At time step t, an agent receives an observation o_t from the environment and takes an action a_t following some policy pi(a_t | c_t), where c_t is the context to the agent.

在时间步 t，Agent 从环境接收观察 o_t，并依照策略 pi(a_t | c_t) 采取动作 a_t；其中 c_t 是 Agent 当时拥有的上下文。
#+end_quote

单步问答可以粗略画成：

#+begin_example
输入 x -> 模型 -> 输出 y
#+end_example

输出错了，损失通常就停在这次预测里。Agent 则是：

#+begin_example
context_t -> 模型 -> action_t -> 环境 -> observation_t -> context_(t+1)
#+end_example

这里发生了性质变化：`action_t` 不只是答案，它会选择下一条数据、修改外部状态，甚至决定后面还有没有机会看到正确证据。`observation_t` 也不只是工具返回，它会被包装、截断、摘要，再进入下一轮推理。

因此，Agent 的基本对象不是某一步的正确率，而是整条 *trajectory（轨迹）* 的状态演化。首次出现的术语：*closed loop（闭环）*，指系统输出通过环境反馈重新成为系统输入；它与一次性前向预测的关键区别，是错误可以改变未来输入分布。

*** 结构标注

核心换框：评估对象从 `P(单步输出正确)` 变成 `P(整条轨迹完成目标)`，并且每一步都在改写下一步的条件。

*** 碰撞

你真正应该问的不是“模型这一步答对了吗”，而是：*这一步如果错了，错误有没有获得写权限？* 它能否写入环境、长期记忆、状态摘要或下一轮 prompt，决定了它只是局部噪声，还是会繁殖的状态污染。

** 第二段：[骨] `p^H` 从哪里来：不是因为独立，而是因为一路都要活着

假设一个任务必须连续通过 H 个关键步骤。令：

#+begin_example
S_t = 已正确完成前 t 步
p_t = P(第 t 步正确 | 前 t-1 步都正确)
#+end_example

那么完整成功率按条件概率链式法则为：

#+begin_example
P(S_H) = p_1 * p_2 * ... * p_H
#+end_example

若为了估算，假设每一步在“轨迹尚未偏离”的条件下都有近似相同的可靠率 p，才得到：

#+begin_example
P(S_H) approx p^H
#+end_example

*这里不需要假设各步误差彼此独立。* 恰恰相反，Agent 的误差通常高度相关；`p^H` 只是恒定条件存活率下的近似。队列里“单步 LLM 的误差彼此独立”这句话需要纠正：无论单步调用还是多步调用，共享模型偏见、同一含糊指令和同一错误上下文都会制造相关误差。

看一笔直觉账：

#+begin_example
条件单步可靠率 p     10 步全对     20 步全对     50 步全对
0.99                  90.44%        81.79%        60.50%
0.98                  81.71%        66.76%        36.42%
0.95                  59.87%        35.85%         7.69%
0.90                  34.87%        12.16%         0.52%
#+end_example

更坏的情况是，第一次错误后，后续可靠率不是继续保持 p，而是降成 q：模型会基于错误实体继续搜索，基于错误摘要继续规划。此时某次偏离不是加一个固定损失，而是在改变后续全部 `p_t`。

*** 结构标注

数学骨架：指数下降来自“每个关键门都必须通过”的乘法；闭环复合则来自某一步会改变后续门的难度。

*** 点睛

*horizon（任务视界）* 不是工具调用次数本身，而是必须串行成立、且缺乏恢复余地的关键决策数。把 20 次机械分页读取合并成一次批量调用，未必改变任务语义，却能缩短有效 horizon；增加验证步骤虽然让轨迹更长，却可能提高每个关键门的条件可靠率并提供恢复路径。所以“步骤越少越好”也不完整，应该优化的是 *不可恢复的错误暴露面*。

** 第三段：[骨] ReAct 每一环怎样注入偏差

*** 1. Thought：信念与计划偏差

ReAct 论文将语言 thought 视为扩展动作空间中的一种动作：它不直接改变外部环境，却会更新 context，支持后续推理与行动。

#+begin_quote
A thought aims to compose useful information by reasoning over the current context, and update the context to support future reasoning or acting.

Thought 旨在对当前上下文进行推理、组织有用信息，并更新上下文，以支持未来的推理或行动。
#+end_quote

它可能错在：

- 把任务拆错，遗漏隐含约束；
- 过早锁定实体，把猜测写成事实；
- 从一次空搜索推出“资料不存在”；
- 在摘要里丢掉反例，只保留支持当前假设的证据。

Thought 的危险是 *信念污染*：它没有碰真实世界，却会成为后续模型可见的“既有结论”。语言流畅度会掩盖其证据等级。

*** 2. Action：接口与副作用偏差

Action 可能错在：

- 工具选错：该查数据库却调用网页搜索；
- 参数错：实体、时间范围、路径或 ID 错；
- 动作顺序错：先删除再验证，先提交再测试；
- 权限边界错：把只读任务变成有副作用的写操作。

Action 的危险是 *状态污染*。错误查询尚可重试；错误付款、删除、发信、merge 则可能不可逆。因此相同的模型正确率，在只读搜索 Agent 和生产运维 Agent 上代表完全不同的风险。

*** 3. Observation：外部世界进入上下文时的测量偏差

工具返回并不等于事实直接进入模型。中间还会经历：序列化、截断、排序、去重、HTML 清洗、错误码解释和摘要。偏差可能来自：

- 搜索结果相关但不支持结论；
- 工具返回空值，wrapper 却没有区分“无结果”和“调用失败”；
- 长结果被截掉，恰好丢失限定条件；
- 网页中的恶意指令被误当成系统指令；
- 多个来源冲突，却被摘要成单一确定说法。

Observation 的危险是 *测量污染*：环境本身可能没错，但 Agent 看见的是经过通道变形后的环境。

*** 4. Context：历史管理偏差

Context 不只是 token 容器，而是 Agent 的工作状态。它可能错在：

- 旧观察挤占窗口，新证据被截断；
- 摘要把“尚未验证”压成“已确认”；
- 重试产生重复轨迹，模型误以为重复等于证据增强；
- 工具返回、模型推断、用户要求没有来源标签；
- 错误被不断复制，形成上下文中的多数意见。

*** 结构标注

误差分层：Thought 改信念，Action 改世界，Observation 改测量，Context 改记忆。四者不是一条纯串行管线，而是每轮都回灌的耦合系统。

** 第四段：[肌] 一次小实体错误，怎样长成“有引用的错误结论”

任务：查一篇论文的方法是否在某数据集上优于基线，并写一句带来源的结论。

#+begin_example
Step 1 Thought:
  记错论文简称，把 Method-A 当成 Method-B。

Step 2 Action:
  search[Method-B benchmark]

Step 3 Observation:
  返回一篇确实讨论 Method-B 的二手文章；相关，但不是目标论文。

Step 4 Thought:
  “已找到目标方法的评测。”
  注意：此处把“搜索命中”升级成“身份已验证”。

Step 5 Action:
  抽取表格中的最好数字。

Step 6 Observation:
  表格脚注说明该数字来自不同数据划分，但脚注在截断时丢失。

Step 7 Thought:
  将数字与目标论文基线直接比较。

Step 8 Action:
  生成结论，并附上二手文章 URL。
#+end_example

最终文本可能同时满足三个表面标准：有方法名、有数字、有 URL；却错了三次：实体错、评测协议错、来源层级错。后面的每一步在局部上都“合理”，因为第一步已经改变了它们看到的条件。

这揭示了一个常被忽略的事实：*最终答案验证不能替代中间状态验证*。末尾检查 URL 是否存在，抓不到“URL 指向了另一个方法”；检查数字是否出现在页面，抓不到“数据划分不可比”。

以上案例支持第三段：闭环错误不是每一步随机抖一下，而是早期偏差给后续建立了一条内部自洽、外部错误的轨道。

** 第五段：[骨] ReAct 的实证教训：工具接地消灭一种错，也引入另一种错

论文在 HotpotQA 上人工检查了 ReAct 与 CoT 的成功和失败轨迹。其表 2 报告：在被抽样分析的失败案例中，CoT 的主要失败类型是 hallucination，占 56%；ReAct 的 hallucination 为 0%，但 ReAct 失败中 reasoning error 占 47%，search result error 占 23%。这些百分比来自论文特定抽样分析，不应外推成所有 Agent 的通用故障率。

#+begin_quote
Non-informative search, which counts for 23% of the error cases, derails the model reasoning and gives it a hard time to recover and reformulate thoughts.

无信息量的搜索占错误案例的 23%；它会使模型的推理脱轨，并让模型很难恢复或重新组织思路。
#+end_quote

作者还指出 ReAct 的一种特有高频错误：模型重复先前的 thought 和 action，无法跳出循环。

这组结果比“ReAct 减少幻觉”更重要：

#+begin_example
纯 CoT：  世界主要由模型内部生成
          -> 灵活，但事实可能凭空长出来

ReAct：   世界部分由工具观察约束
          -> 更接地，但搜索质量、接口状态和循环控制成为新瓶颈
#+end_example

论文还显示，ReAct 并非在所有指标上单独最佳：在 PaLM-540B prompting 设置下，HotpotQA 的 ReAct EM 为 27.4，CoT 为 29.4；组合策略达到更高结果。原论文用“ReAct 超步数则退回 CoT-SC”或“CoT 自一致性不足则转 ReAct”的启发式做路由。教训不是永远使用更多工具，而是 *根据不确定性的来源切换推理模式*：缺事实时查外部，检索反复无信息时不要无限查。

*** 结构标注

证据段：闭环反馈既是纠错通道，也是新误差源。ReAct 把故障从“无依据地编”部分转移到了“搜错、读错、循环与恢复失败”。

*** 旁逸

这里的论证结构和控制论是同一个形状。开放环系统只执行预定动作；闭环系统用反馈修正偏差，但如果传感器有偏、反馈延迟或控制增益过大，反馈本身会造成振荡。Agent 的重复搜索循环，就像控制器看见滞后的误差信号后不断过度修正。问题从来不是“要不要反馈”，而是“反馈是否可观测、可信、带延迟，以及系统有没有阻尼”。

** 第六段：[骨] Context engineering 到底在链条哪一环拦截

把 context engineering 理解为“写更好的 system prompt”太窄。它真正管理的是：*什么信息以什么结构、证据等级和生命周期进入下一轮决策*。

*** 拦截器 1：动作之前——把自由文本压成可验证意图

#+begin_example
模型意图 -> typed schema -> 参数校验 -> 权限/副作用检查 -> 执行
#+end_example

要点：

- 工具调用使用类型化 schema、枚举和必填字段；
- 写操作先 dry-run，危险动作要求独立确认条件；
- 参数中携带实体 ID，而不只携带易混的名字；
- 对不可逆动作设置事务、幂等键或补偿动作。

它拦的是 Thought 到 Action 的翻译误差。

*** 拦截器 2：观察进入上下文之前——保留原始证据与失败语义

- 明确区分 `empty_result`、`timeout`、`permission_denied`、`parse_error`；
- 原始输出与摘要并存，摘要必须指回证据片段；
- 给来源、时间、查询参数和截断状态加元数据；
- 外部文本按不可信数据隔离，不能获得指令权限。

它拦的是 Observation 的测量误差与来源漂白。

*** 拦截器 3：历史压缩时——分开事实、推断、计划与未决项

不要让一段自然语言摘要承担所有状态。使用分栏账本：

#+begin_example
Goal:        用户原始目标与验收条件
Facts:       已由工具证实的事实 + source id
Hypotheses:  尚待验证的推断
Plan:        当前计划与下一动作
Done:        已完成步骤及产物
Open:        未决问题
Failures:    失败动作、错误码、已尝试次数
#+end_example

它拦的是 Context 压缩后“猜测升格为事实”。

*** 拦截器 4：循环过程中——让进展可测量

- 每轮记录状态是否产生新信息；
- 相同 action + 参数重复时触发 loop detector；
- 设置按错误类型分配的重试预算，而非统一 `max_steps`；
- 连续无信息观察后，强制改写查询、切换工具或回退；
- 对长任务设置 checkpoint，从最近可信状态重规划，而非把整条脏轨迹继续喂回去。

它拦的是错误的自我复制。

*** 拦截器 5：提交结果之前——按验收条件检查，而非让模型泛泛反思

“请检查你的答案”往往只会生成另一段同分布语言。更可靠的是可执行断言：

#+begin_example
- 声称的每个数字是否能定位到 source span？
- 方法实体 ID 是否从头到尾一致？
- 比较双方的数据集、split、metric 是否相同？
- 产物是否真实存在，哈希/测试是否通过？
- 是否仍有未解决的工具错误被摘要掩盖？
#+end_example

它拦的是“内部自洽被误当成外部正确”。

*** 结构标注

工程答案：context engineering 分布在回路每个接口；核心不是增加 token，而是限制错误信息的写权限，并为恢复保留可信锚点。

** 第七段：[肌] 怎么评测：不要只看最终成功率

只报 task success rate 会告诉你系统坏了，却不告诉你坏在哪。建议至少同时记录：

#+begin_example
1. Task success
   最终验收条件是否全部满足

2. Critical-step reliability
   关键决策在“此前状态可信”条件下的正确率

3. Recovery rate
   发生可检测错误后，回到可信轨迹的比例

4. Error amplification factor
   一次上游错误平均污染多少个后续状态/动作

5. Loop rate and wasted actions
   重复调用率、无新增信息步骤数

6. Grounding precision
   带引用断言中，来源真正支持断言的比例

7. Side-effect safety
   未授权或不可逆错误动作的发生率

8. Effective horizon
   必须串行正确、且没有独立校验或恢复路径的关键门数量
#+end_example

一个系统可能在单步 tool-call accuracy 上更高，却因恢复率低而整任务更差；也可能多做两步验证，使表面 horizon 增长，却把有效 horizon 降低。评测必须把“首次犯错”和“犯错后失控”分开。

以上指标支持第六段：可靠 Agent 的优化目标不是零错误——这通常不现实——而是 *错误可检测、污染有边界、状态可回滚、任务可恢复*。

** 第八段：[骨] 压力测试：反馈明明能纠错，为什么说误差会复合？

最强反对是：闭环的意义正是根据 observation 修正错误。只要工具返回真实世界，Agent 不应比单步模型更脆弱，反而应越走越准。

这个反对成立一半。闭环有两种区域：

#+begin_example
负反馈区域：
  observation 能暴露偏差
  + agent 正确解释错误
  + 有可用恢复动作
  -> 误差收敛

正反馈区域：
  observation 含糊、截断或被误读
  + 错误被写入摘要
  + 后续行动只寻找支持它的证据
  -> 误差放大
#+end_example

所以关键变量不是“是否有工具”，而是三个条件：

1. *observability（可观测性）*：错误是否会在反馈中留下可辨认信号？
2. *diagnosability（可诊断性）*：系统能否区分搜索无结果、工具故障、参数错误和假设错误？
3. *recoverability（可恢复性）*：识别错误后，是否有回退、重试、换路或人工接管路径？

若三者都强，长 horizon 不必等于指数崩溃；系统可以在局部闭环中纠错。若三者弱，增加反思轮数只是让错误获得更多自我解释的机会。

*** 结构标注

论证收束：`p^H` 不是 Agent 的宿命，而是缺少检测与恢复时的基线；context engineering 的价值，是把“必须步步不错”改造成“允许局部犯错，但不能让错穿过边界”。

* 全文复盘

** 理解轨迹

#+begin_example
单步正确率
  -> 条件概率连乘解释长 horizon 衰减
  -> 纠正“必须独立才有 p^H”的误解
  -> 区分 Thought / Action / Observation / Context 四类污染
  -> 用 ReAct 论文看到：接地减少幻觉，也引入搜索与循环故障
  -> 将 context engineering 定位为回灌通道治理
  -> 从“避免犯错”升级为“检测、隔离、恢复”
#+end_example

** 读后一句话（不可跳过）

读完后，请只对作者说一句话：*ReAct 最需要补上的，不是更强的 reasoning，而是哪一种错误边界？为什么？*

这不是复述题。若你的答案能指出一个具体接口，并说出错误怎样穿过它，就已经从“理解 Agent 流程”走到了“能设计 Agent 可靠性”。

** 终局问题

如果一个 Agent 的 evaluator、反思器和执行器都来自同一个基础模型，它们共享同一种盲点，那么“多加一道自检”究竟是在增加独立证据，还是在制造相关错误的多数投票？你会在哪个接口引入真正异质的校验信号？

** 术语表

| 英文 | 中文 | 本文含义 | 位置 |
|-------+------+----------+------|
| closed loop | 闭环 | 输出经环境反馈重新成为输入 | 第一段 |
| trajectory | 轨迹 | Thought、Action、Observation 与状态的完整序列 | 第一段 |
| horizon | 任务视界 | 必须串行完成的决策跨度；本文更关心有效关键门数量 | 第二段 |
| error compounding | 误差复合 | 上游错误改变后续条件分布，使后续更易继续错 | 第二至四段 |
| grounding | 接地 / 证据锚定 | 用外部可核验观察约束模型内部生成 | 第五段 |
| observability | 可观测性 | 内部错误能否从外部反馈中被识别 | 第八段 |
| diagnosability | 可诊断性 | 能否定位错误类型与发生接口 | 第八段 |
| recoverability | 可恢复性 | 偏离后能否回到最近可信状态 | 第八段 |

** 下一步线索

沿本文的终局问题，下一步不要泛读 Agent 框架，而应直接看：

- Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning*，重点看“语言反思如何写回记忆”，追问反思是否提供了独立信号。
- Madaan et al., *Self-Refine: Iterative Refinement with Self-Feedback* 的方法与消融部分，重点比较“同模型自评”在什么任务上有效、什么情况下只是重写。
- 若转向工程实现，选一个真实 Agent trace，为每一条 context 项加 `source / confidence / lifecycle / write permission` 四个字段；这比再加一句“请仔细思考”更能检验今天的结论。
