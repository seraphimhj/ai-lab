---
source_url: https://mp.weixin.qq.com/s/i3yKCZCUtDkTrk4hFZz7NQ
ingested: 2026-05-14
sha256: 634cba01cd5ec7763af6d749d937b60ddbd1ed7704d739df7a605eab77bd4952
---

# LLM 与 Agent 核心原理全面解析

> AI 写代码的效果取决于两件事：**LLM 模型本身的能力** + **围绕模型的 Agent 工程实现**。两者都强才有最好效果。

---

## 一、LLM 本质：概率预测

**核心原理：根据已有文本，预测下一个 token 出现的概率。**

- **Token**：模型处理文本的最小单位（1 英文单词 ≈ 1 token，1 汉字 ≈ 1-2 token）
- 预测后拼到输入后面，继续预测下一个，如此反复生成完整文本
- ChatGPT 逐字出现并非打字机效果，而是真实工作方式

### 关键参数：温度（Temperature）

| 温度值 | 行为 | 适用场景 |
|--------|------|----------|
| 0（最低） | 每次选概率最大的字，最确定 | 编程等精确工作 |
| 高值 | 更愿选概率低的字，有创意但不可控 | 创意类工作 |

### 关键概念：上下文窗口（Context Window）

- 上下文 = 输入问题 + 对话历史 + 系统背景设定
- 模型每次生成回答依据整个上下文内容
- 超出窗口的内容被压缩或丢弃 → "失忆"
- **主流窗口大小：128K ~ 1M token**（几万到几十万字）
- **最佳实践：一个上下文窗口只聚焦一个问题，新问题重新开窗口**

---

## 二、Base vs Instruct 模型

| 版本 | 行为 | 示例 |
|------|------|------|
| Base | 文本补全（续写） | 输入"中国的首都是" → 接着写"北京，位于华北平原…" |
| Instruct | 理解为指令并回答 | 输入"中国的首都是" → 回答"中国的首都是北京" |

**Instruct 模型的制作过程：**
1. Base 模型基础上，用「指令-回答」数据对进行 **Fine-tuning**
2. 通过 **RLHF**（人类反馈强化学习）优化：生成多个回答 → 人类打分排序 → 模型调整

> 平时用的 ChatGPT、Gemini 等 AI 助手全是 Instruct 模型。

---

## 三、思维链（Chain of Thought, CoT）

**让模型先写推理过程再给答案，准确率大幅提高。**

- 每一步中间结果成为后续推理输入，更靠谱
- 推理模型（o1/o3、DeepSeek R1、Claude extended thinking）进一步加入**自我反思**：先给答案 → 回头检查 → 修正

### 2025 年新范式：单一模型 + 思考强度参数

```
旧模式：对话模型（gpt-4o） vs 推理模型（gpt-o1），中途不能换
新模式：同一模型 + reasoning_effort / effort / thinkingLevel 参数
```

- 强度调高 → 多花时间推演；强度调低 → 直接给答案省 token
- 好处：一套代码覆盖所有场景，复杂度大幅降低

---

## 四、System Prompt：设置「人设」

> System Prompt 就是一切工具调用、任务执行、操作流程的起点。

**两个核心价值：**
1. **定义模型行为方式**（角色、风格、偏好）
2. **设置不可轻易绕过的规则**（安全策略）

- 对话开始前给模型的指令，拼到上下文最前面
- 用户看不到，但模型每次生成都读到
- 模型训练时学会对 system 标签内容赋予更高服从权重
- ChatGPT「自定义指令」本质上追加到 System Prompt 里

---

## 五、Function Calling / Tool Use

> LLM 只能输出文本。Function Calling 给"超级大脑"装上了手脚。

**完整工作流程：**

```
工具描述写入 System Prompt → 用户提问 → 模型输出工具调用 JSON →
程序调用真实 API → 结果塞回上下文 → 模型生成最终回答
```

**关键点：模型本身不调用 API，只输出 JSON 表达"调用意图"，外围程序执行。**

考验的是模型的**指令遵从能力**：能否只输出合法 JSON，不夹带废话。

---

## 六、MCP：Model Context Protocol

> MCP = AI 工具领域的"USB-C 标准"

**解决的问题：** 各家 API 格式不同（OpenAI 用 `parameters`，Anthropic 用 `input_schema`），同一工具需反复适配。

**MCP 示例代码：**

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-server")

@mcp.tool()
def get_weather(city: str) -> str:
    """查询指定城市的当前天气"""
    return f"{city}：8°C，多云"

mcp.run()
```

- 写一次，所有支持 MCP 的 AI 工具都能接入
- **底层仍是 Tool Use 那一套**，只是接口标准化了

---

## 七、Agent：LLM + 工具 + 循环

> Agent 的核心思路：把 LLM + Tool Use 放进一个循环里。

```python
while 任务未完成:
    模型根据当前上下文思考下一步该做什么
    if 模型认为需要使用某个工具:
        执行工具，把结果追加到上下文
    elif 模型认为任务完成了:
        输出最终结果，退出循环
```

学术名称：**ReAct（Reasoning + Acting）**——思考 → 行动 → 观察结果 → 再思考

**循环副作用：** 上下文不断增长 → 上下文窗口大小至关重要

> LLM 是大脑，工具是手脚，循环是驱动力，结合起来就是 Agent。

---

## 八、Skills：可复用工作流程

> Skills = 把常用操作流程沉淀成文档，Agent 按文档执行。

**Anthropic PDF Skill 示例结构：**

```
skills/pdf/
├── SKILL.md        # 核心：何时触发 + 操作指南
├── reference.md    # 详细参考文档
├── forms.md        # 表单填写专项指南
└── scripts/        # 预写好的 Python 脚本
    ├── extract_form_field_info.py
    ├── fill_fillable_fields.py
    ├── convert_pdf_to_images.py
    └── ...
```

**SKILL.md 开头定义触发条件：**

```yaml
---
name: pdf
description: Use this skill whenever the user wants to do anything with PDF files.
---
```

**渐进式披露（Progressive Disclosure）：**
- 启动时只加载 Skill 名称 + 一句话简介（省 token）
- 模型发现任务相关时才加载完整内容
- 核心原理不变，通过按需加载大幅降低 token 消耗

---

## 九、核心洞察：一切都是上下文

> 不管是思维链、Tool Use、Agent 循环、MCP 工具描述还是 Skills 文档，**最终都要塞进上下文窗口里，交给同一个概率模型去一个字一个字地往外蹦**。

| 概念 | 本质 |
|------|------|
| 思维链 | 模型在上下文里写给自己看的草稿 |
| MCP / Tool Use | 上下文里塞工具描述，模型输出调用请求，结果追加回上下文 |
| Agent 循环 | 不断往上下文里追加思考和工具结果 |
| Skills | 把操作手册文本加载到上下文里 |

**上下文里塞什么、怎么塞、塞多少 → 直接决定 Agent 表现。**

---

## 十、回答开篇问题

**为什么 Claude Code + Claude 模型效果最好？**

- Claude Code 是 Agent 层面工具，Claude 是 LLM 模型
- Claude Code 敢给模型塞更多上下文，获取充分信息后再执行
- Cursor 等通过 API 调用有成本限制，塞更少上下文尽快给答案
- **Agent 工程做的好，能让模型发挥更充分**

> 随着模型能力提升，围绕模型构建的工程优化价值水涨船高——这正是 AI 时代的机会所在。
