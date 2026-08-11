---
title: Claude Code Harness 架构
created: 2026-05-05
updated: 2026-08-11
type: concept
tags: [agent, architecture, framework]
sources: [raw/articles/claude-code-harness-architecture-2026.md]
---

# Claude Code Harness 架构

Harness 是 [[claude-code]] 的核心编排层，设计本质是：**把多入口、多模式、多运行位置，收敛成一套统一的 agent turn 执行模型**。

## 三层架构

### 第一层：入口与分流

负责接住用户不同的使用方式：
- 命令行（CLI）
- 交互界面（TUI/REPL）
- SDK 调用
- Assistant 模式
- 远端链接

入口经 `main.tsx` 做参数解析、模式判断和路由分发。

### 第二层：Harness 会话编排（核心）

标准化处理层，将三种不同形态的请求统一为 turn 契约：
- 交互会话
- 无界面会话（headless）
- 远端接入

同时接入：
- 工具能力
- 扩展接入（MCP / plugins / skills）
- 状态与持久化

在执行前就把一次会话需要的**输入、能力和状态**组织完整。

### 第三层：Runtime 与支撑层

- **本地路径** → 进入本地 Runtime 执行完整 [[agent-loop-taor]]
- **远端路径** → 转入远端会话宿主（remote / bridge / server）

## 设计要点

- 「下限可控、上限可拓」的基础框架
- 入口无关性：无论从哪里来，都走同一套 turn 模型
- 关注恢复能力、权限模型、上下文压缩和长会话稳定性

## 拿第二个生产 harness 做对照：什么是结构不变量，什么只是本家选择

上面这套三层描述是从 Claude Code 一家总结出来的，容易把「多入口收敛成统一 turn 模型」当成一句设计口号。把一份对独立第二实现的全量源码审查摆进来，这句口号能被证伪或坐实——Grok Build（xAI 的终端 coding agent，全 Rust）在没有共享代码的前提下，几乎逐条复现了本页的三层骨架，于是「哪些是 harness 的结构不变量、哪些只是 Claude Code 的一种选法」第一次能分开看。[[2026-07-26-grok-build-architecture]]

**四处独立收敛＝结构不变量**（两家形态不同却都必须有）：

| 本页设计要点 | Grok Build 的对应实现 | 抽出的不变量 |
|------|------|------|
| 入口无关性：多入口走同一 turn 模型 | Leader-Follower：单 Leader 进程持有 Agent 状态，TUI / IDE / headless 三种 Client 经 Unix socket 复用同一状态 | 「入口无关」不是路由技巧，而是**状态单点、渲染多端**——UI 差异被挤到 Client 层，turn 模型只有一份 |
| 统一 turn 契约 | per-session 单线程 Tokio actor + `biased tokio::select!`，所有状态变更串行化（计时器 > 事件 > 命令） | turn 模型的本体是**一个把并发挤成串行的 actor**，锁竞争问题被「一会话一单线程」从设计上消掉 |
| 上下文压缩 / 长会话稳定性 | 两阶段 compaction：接近阈值前后台异步生成前缀摘要（prefire），实际压缩时拼「前缀摘要＋尾部」再总结；用内容指纹检测前缀被 rewind/编辑即失效 | 长会话稳定性靠**把压缩拆成可预算、可失效的两步**，而非一次性截断——与 [[context-engineering]] 的 compaction 保险丝同形，此处是它的一个生产级落地 |
| 权限模型 / 恢复能力 | 三层权限（显式 allow/deny 规则 → 启发式＋LLM 分类器 → 人工确认，每层可短路）；workflow 引擎 journal＋禁用 `timestamp/sleep` 保证 resume 可重放 | 权限是**从快到慢、自动到人工的短路链**；恢复能力＝**确定性重放**，靠记录每次 host call 的输入输出而非快照整个进程 |

**三处分岔＝Claude Code 的选择而非 harness 的必然**（Grok Build 走了另一条，说明这几处是可变设计轴，不是唯一解）：

- **单工具集 vs 多命名空间并存**：Grok Build 同时挂 `GrokBuild / Codex / OpenCode / MCP` 四套工具集，扫 `.claude/`、`.cursor/` 目录自动发现外部规则——把「工具集」变成一根可切换的兼容轴（代价是多套语义映射的维护成本）。这暴露出本页三层里**「工具能力」接入其实还有一根「用谁家的工具契约」的隐藏维度**。
- **进程内子代理 vs 远端会话宿主**：本页把远端路径单列为第三层 Runtime；Grok Build 的子代理是同一 LocalSet 内 `spawn_local` 的新 `SessionActor`，**继承父会话的 MCP 连接池 / hooks / 工具定义、但隔离对话历史**——给出「隔离什么、继承什么」的更细粒度答案（连接与策略继承、状态与历史隔离），可回填本页语焉不详的「子代理」。
- **软件保护 vs 内核沙箱**：Grok Build 用 `nono`（Landlock/Seatbelt）做 OS 级隔离并可优雅降级，只在关键边界（hook write-deny）fail-closed——把本页一句带过的「权限模型」延伸出一层**「安全措施分必须强制 vs 尽力而为」的降级策略轴**。

一句话收束：本页「把多入口/多模式/多位置收敛成一套 turn 模型」被第二家独立坐实为**结构不变量**（状态单点＋串行 actor＋两步压缩＋短路权限＋确定性重放），而工具契约、子代理隔离粒度、沙箱强度是**可变设计轴**——读 harness 设计时该问的不是「像不像 Claude Code」，而是「这几根不变量在不在、那几根可变轴各自选了哪一档」。子代理的「继承连接、隔离历史」也正是 [[context-engineering]] 里「子代理隔离」保险丝的实现级注解，[[agent-loop-taor]] 的采样循环在两家都对应那个串行 actor 的内层。

## 相关概念

- [[agent-loop-taor]] — Harness 之下的执行循环（＝Grok Build 里串行 actor 的内层采样循环）
- [[claude-code-state-management]] — 状态管理支撑（对应「状态单点」不变量）
- [[claude-code-memory-system]] — 记忆系统支撑
- [[context-engineering]] — 两步 compaction、子代理隔离是其保险丝的生产级落地
