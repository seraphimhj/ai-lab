---
title: ReAct — 推理与行动结合
created: 2026-05-10
updated: 2026-07-30
type: concept
tags: [agent, reasoning, tool-use]
sources: [raw/papers/2210.03629-ReAct-Synergizing-Reasoning-and-Acting-in-Language-Models.html, raw/articles/llm-agent-core-principles-2026.html]
---

# ReAct — 推理与行动结合

将语言模型的推理（Reasoning）与外部行动（Acting）交替进行，通过思考和行动的循环来解决需要外部信息的复杂任务。[[raw/papers/2210.03629-ReAct-Synergizing-Reasoning-and-Acting-in-Language-Models.html]]

## 核心思想

### 纯推理的局限

- [[chain-of-thought]] 只有推理，无法获取外部信息
- 模型的内部知识有限，无法处理实时或私有数据
- 无法与外部世界交互

### ReAct 循环

```
Thought（思考）→ Action（行动）→ Observation（观察）→ Thought → ...
```

模型先思考下一步该做什么，然后执行行动（如搜索、计算），观察结果，再继续推理。

## 格式示例

```
Question: 2023 年诺贝尔物理学奖得主是谁？他所在机构的排名是什么？

Thought 1: 我需要查找 2023 年诺贝尔物理学奖得主。
Action 1: Search[2023 Nobel Prize Physics winner]
Observation 1: Pierre Agostini, Ferenc Krausz, Anne L'Huillier

Thought 2: Pierre Agostini 在哪个机构？
Action 2: Search[Pierre Agostini affiliation]
Observation 2: Ohio State University

Thought 3: 我需要查找 Ohio State University 的排名。
Action 3: Search[Ohio State University ranking 2023]
Observation 3: #49 in US News

Thought 4: 现在可以回答了。
Answer: 2023 年诺贝尔物理学奖得主包括 Pierre Agostini，他所在的 Ohio State University 在 2023 年 US News 排名第 49。
```

## 优势

| 对比 | CoT（纯推理） | ReAct |
|------|-------------|-------|
| 外部信息 | 无法获取 | 通过 Action 获取 |
| 可解释性 | 中等 | 高（Thought 是显式的） |
| 错误恢复 | 无法自我纠正 | 可以根据 Observation 调整 |
| 任务范围 | 知识内任务 | 知识外 + 工具任务 |

## 简化理解：Agent = LLM + 工具 + 循环

Agent 的核心思路可以用极简伪代码表达：

```python
while 任务未完成:
    模型根据当前上下文思考下一步该做什么
    if 模型认为需要使用某个工具:
        执行工具，把结果追加到上下文
    elif 模型认为任务完成了:
        输出最终结果，退出循环
```

- LLM 是大脑，工具是手脚，循环是驱动力
- 循环副作用：上下文不断增长 → 上下文窗口大小至关重要
- Agent 工程的核心是上下文工程：如何高效组织和填充上下文窗口

## 论文实验数据

Yao et al. (2022) 在四个基准上评测 ReAct：
- **HotpotQA**：ReAct + CoT 组合方法超越纯 CoT，解决了幻觉和错误传播问题
- **Fever 事实验证**：ReAct 通过 Wikipedia API 交互生成可解释的推理轨迹
- **ALFWorld**：1-2 shot ReAct 比 imitation/RL 方法（训练 10³–10⁵ 样本）高 34% 绝对成功率
- **WebShop**：ReAct 比 RL 方法高 10% 绝对成功率

关键发现：推理和行动的组合相比单独使用（纯 Reasoning 或纯 Acting）带来系统性优势。

## 误差在闭环里如何复合

单步问答里一次预测错了，损失通常停在那一步；Agent 不同——`action_t` 会选择下一条数据、改写外部状态，`observation_t` 会被截断、摘要后再喂回下一轮，于是**错误会改变下一步看到的世界**。评估对象因此从「单步正确率」升级成「整条 trajectory 能否完成目标」。[[2026-07-20-react-agent-error-compounding]]

### 为什么长任务成功率近似指数衰减

设任务须连续通过 H 个关键门，令 p 为「轨迹尚未偏离」条件下每步的可靠率，则 P(成功) ≈ p^H。关键在于：**这不需要假设各步误差独立**——恰恰相反，共享的模型偏见、同一句含糊指令、同一段错误上下文会制造高度相关的误差。更坏的是首次出错后可靠率会从 p 跌到更低的 q（模型基于错误实体继续搜、基于错误摘要继续规划）。所以该优化的不是「步数越少越好」，而是**不可恢复的错误暴露面**（有效 horizon = 必须串行成立、且无独立校验或恢复路径的关键门数）。

### 四类污染注入点

| 接口 | 改写的东西 | 危险 |
|------|-----------|------|
| Thought | 信念 | 把猜测写成「已确认」，语言流畅度掩盖证据等级 |
| Action | 世界 | 错误的写/删/付款/merge 不可逆 |
| Observation | 测量 | 截断丢限定条件、空值与失败码不分、外部文本被当指令 |
| Context | 记忆 | 摘要把「未验证」压成事实、重复轨迹被当证据增强 |

四者不是纯串行管线，而是每轮都回灌的耦合系统。

### context engineering = 治理回灌通道，而非塞更多 token

有效的上下文工程分布在回路每个接口，核心是限制**错误信息的写权限**、并保留可信恢复锚点：动作前把自由文本压成 typed schema + 参数/副作用校验；观察入上下文前区分 `empty/timeout/permission_denied/parse_error` 并让外部文本按不可信数据隔离；历史压缩时用分栏账本拆开 Goal / Facts(带 source) / Hypotheses / Plan / Failures；循环中挂 loop detector、按错误类型分配重试预算、checkpoint 重规划而非续喂脏轨迹；提交前做可执行断言（数字能否定位到 source span、实体 ID 是否全程一致）而非「请再检查一遍」这种同分布反思。

闭环收敛还是发散，取决于三个变量：**observability**（错误是否在反馈里留下可辨信号）、**diagnosability**（能否区分无结果/工具故障/参数错/假设错）、**recoverability**（识别后有无回退换路）。三者弱时，多加一轮反思只是给错误更多自我解释的机会——尤其当 evaluator、反思器、执行器同源、共享同一盲点时，「自检」可能只是相关错误的多数投票。

### Context 压缩：闭环里的第四处「过早聚合」

上表 Context 行的危险——「摘要把『未验证』压成事实、重复轨迹被当证据增强」——不是 Agent 特有的新病，而是一个更一般病灶在回路里的复发：**过早聚合把决定性的少数信号抹掉**。它在编码端表现为单向量把低频实体淹进整句语义、在评测端表现为总体均值把关键切片压成一个数（[[2026-07-25-aggregation-erases-minority-signals]]）；到了 Agent，history compaction 就是同一个动作的第四处发作——把一长段异质轨迹（目标、带 source 的事实、未验证假设、失败码、一次越权动作的记录）聚合成一段流畅摘要时，被丢掉的正是「谁贡献了这条信息、它的证据等级如何」。

```text
病灶发作点          被聚合掉的少数信号
编码端单向量        低频高信息 token（专名/型号）→ 被高频语义补偿
评测端单指标        关键切片（安全/长尾/高损失组）→ 被多数样本稀释
Agent context 压缩  单条未验证假设 / 失败码 / 越权动作 → 被摘要成「已确认事实」
```

这解释了为什么「多塞点 token 让模型再想想」救不了长任务：问题不在窗口不够大，而在压缩把「未验证」和「已确认」聚合进了同一层，硬约束（这一步到底核实过没有）退化成可被流畅叙述补偿的一项特征——和点积里实体维被话题相似度补偿是同一种可补偿性。所以修法也同构：**拒绝过早聚合、按风险再聚合**——分栏账本把 Goal / Facts(带 source) / Hypotheses / Failures 拆开存（对应检索端保留 token 向量 / 词表维、评测端保留 per-slice），让「未验证」始终占一个不被摘要抹平的独立账目；checkpoint 重规划而非续喂脏轨迹，就是「先暴露失败切片、再有意识地二次聚合」在时间维上的版本。

## 局限性

- 行动空间需要预先定义
- 多步推理时错误可能累积
- 行动次数受限（API 调用成本）
- 循环中上下文不断增长，受窗口大小约束

## 相关概念

- [[chain-of-thought]] — ReAct 中 Thought 部分的基础
- [[tool-use]] — ReAct 中 Action 的具体实现
- [[retrieval-augmented-generation]] — 一种常见的 Action 类型
- [[agent-paradigm-shift]] — ReAct 是 Agent 范式的重要里程碑
- [[context-engineering]] — Agent 循环本质是不断往上下文追加内容
- [[mcp-model-context-protocol]] — Agent 工具层的标准化接口
- [[agent-skills]] — Agent 的可复用操作文档

## 伴读来源

- [[2026-07-20-react-agent-error-compounding]] — 误差沿闭环复合、有效 horizon、四类污染注入点、context engineering 治理回灌通道
- [[2026-07-25-aggregation-erases-minority-signals]] — context 压缩是回路里第四处「过早聚合」，与编码端/评测端同构、分栏账本对应保留切片
