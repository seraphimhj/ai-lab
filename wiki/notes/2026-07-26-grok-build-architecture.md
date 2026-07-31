# Grok Build 源码架构深度审查

> **日期**: 2026-07-26  
> **源码**: https://github.com/xai-org/grok-build.git (Apache 2.0)  
> **审查范围**: 全量 Rust 源码 (~50+ crates)，重点关注 agent loop、工具协议、上下文管理、并发/子代理、权限安全、可扩展性与工程取舍  

---

## 一、项目概况

Grok Build (`grok`) 是 SpaceXAI 的终端 AI 编程 Agent。它以全屏 TUI 运行，可理解代码库、编辑文件、执行 Shell 命令、搜索网络并管理长时间运行的任务。支持交互式 TUI、headless 模式（脚本/CI）和 ACP（Agent Client Protocol）编辑器嵌入。项目以 Rust 编写，从 SpaceXAI monorepo 定期同步出。

**核心技术栈**：Rust, Tokio async runtime, Ratatui (TUI), ACP (Agent Client Protocol), MCP (Model Context Protocol), nono (kernel sandbox), Rhai (workflow scripting)

---

## 二、整体架构概览

### 2.1 仓库布局 (README.md L97-L106)

```
crates/codegen/
├── xai-grok-pager-bin       # 二进制入口 (composition root)
├── xai-grok-pager            # TUI: 滚动、输入、弹窗、渲染
├── xai-grok-shell            # Agent 运行时 + leader/stdio/headless 入口
├── xai-grok-shell-base       # Shell 基础工具（grok_home, env 等）
├── xai-grok-agent            # Agent 构建器、定义解析、system prompt 组装
├── xai-grok-tools            # 工具实现 (terminal, file edit, search, ...)
├── xai-grok-tools-api        # 工具 API 类型
├── xai-grok-workspace        # 宿主机文件系统、VCS、执行、checkpoint
├── xai-grok-workspace-types  # Workspace 类型定义
├── xai-grok-workspace-client # Workspace 客户端
├── xai-grok-sandbox          # OS 级沙箱 (nono: Landlock/Seatbelt)
├── xai-grok-config           # 配置加载/解析
├── xai-grok-mcp              # MCP 集成
├── xai-grok-memory           # 跨会话记忆
├── xai-grok-subagent-resolution # 子代理解析
├── xai-grok-hooks            # 钩子系统
├── xai-grok-markdown         # Markdown 渲染
├── xai-grok-auth             # 认证
├── xai-grok-models           # 模型管理
├── xai-workflow              # 工作流引擎 (Rhai 脚本)
├── xai-chat-state            # 对话状态管理
└── xai-agent-lifecycle       # Agent 生命周期
```

### 2.2 架构分层

```
┌─────────────────────────────────────────────────────┐
│                    UI Layer (TUI/ACP)                │
│     xai-grok-pager, xai-ratatui-*                   │
├─────────────────────────────────────────────────────┤
│                  Agent Runtime (Shell)               │
│     xai-grok-shell (SessionActor, Leader, MvpAgent)  │
├─────────────────────────────────────────────────────┤
│              Agent Builder + Prompt Layer            │
│     xai-grok-agent (Agent, AgentBuilder, Prompt)     │
├─────────────────────────────────────────────────────┤
│              Tools + Workspace Layer                 │
│  xai-grok-tools, xai-grok-workspace, xai-grok-sandbox│
├─────────────────────────────────────────────────────┤
│     Protocol Layer (ACP/MCP/Leader IPC)              │
│  xai-grok-mcp, xai-acp-lib, leader/*               │
├─────────────────────────────────────────────────────┤
│     Infrastructure (auth, config, memory, hooks)    │
│  xai-grok-auth, xai-grok-config, xai-grok-memory    │
└─────────────────────────────────────────────────────┘
```

---

## 三、Agent Loop：事件驱动的会话调度器

### 3.1 核心循环架构

Agent 的主循环实现在 `run_session()` 函数中（`session/acp_session_impl/run_loop.rs:120-2241`）。采用单线程 Tokio `LocalSet` + `tokio::select!` 事件驱动模型：

```rust
// run_loop.rs:259 — 核心事件循环
loop {
    tokio::select! {
        biased;
        // 1. 空闲 flush 计时器 (记忆持久化)
        // 2. Dream 检查计时器 (记忆整合)
        // 3. 模型切换 (LazinessDetector 重置)
        // 4. ChatStateActor 事件 (对话重置、图片预算)
        // 5. SessionEvent 接收 (通知、replay flush)
        // 6. Completion 接收 (turn 完成信号)
        // 7. Command 接收 (用户输入/控制命令)
    }
}
```

**设计要点**：
- **单线程 per-session**：每个 `SessionActor` 运行在独立的 `tokio::runtime::Runtime`（`current_thread`），避免跨线程同步开销（`session/acp_session_impl/spawn.rs:39-42`）
- **biased select**：优先级明确的偏斜选择，计时器 > 事件 > 命令
- **串行化所有状态变更**：避免了传统多线程 Agent 中的锁竞争问题

### 3.2 SessionActor 状态模型

`SessionActor` 是会话运行时的核心状态容器，聚合了以下关键组件：

| 组件 | 用途 |
|------|------|
| `agent: RefCell<Agent>` | 当前 Agent 定义 + 渲染后的 system prompt |
| `chat_state_handle` | 对话历史和 token 计数 |
| `tool_context: ToolContext` | 工具执行上下文 (cwd, 环境变量) |
| `mcp_state` | MCP 服务器连接状态 |
| `permission_manager` | 权限决策管理器 |
| `workflow_manager` | 工作流管理器 |
| `memory` | 跨会话记忆后端 |
| `models_manager` | 模型切换/选择 |

### 3.3 Turn 生命周期

```
用户输入 → handle_prompt()
  ├── prompt_build.rs     # 构建 user message（模版、rules、AGENTS.md）
  ├── turn.rs             # 采样循环 (sampling loop)
  │    ├── 工具定义注入 → model API 调用
  │    ├── 响应解析 → tool_calls 提取
  │    ├── 并行/串行工具分发 (tool_dispatch.rs)
  │    ├── 工具结果注入 → 重新采样
  │    └── 无工具调用 → 文本响应 (turn 结束)
  ├── turn_end.rs         # Turn 完成清理
  │    ├── 计划清理 (Plan 中的 in_progress → completed)
  │    ├── goal 策略更新
  │    └── 遗留 interjection 刷新
  └── completion 信号发送 → run_loop 继续
```

关键入口函数在 `turn.rs` 中，每个 turn 支持：
- **多轮工具调用**：模型可以连续发出多批 tool_calls，每批执行完后将结果反馈给模型继续推理
- **Structured Output**：通过 `StructuredOutput` 伪工具实现 schema 约束输出（`turn.rs:7,10`），最多重试 3 次
- **并行工具执行**：同批内无文件冲突的工具并发执行（`tool_dispatch.rs:41-59` 通过文件路径锁实现串行化冲突工具）

### 3.4 Leader-Follower IPC 架构

`leader/mod.rs:1-33` 实现了单机单 Leader 多 Client 架构：

```
Leader Process (MvpAgent)
    │ IPC (Unix socket ~/.grok/leader.sock)
    ├── TUI Client (stdio)
    ├── IDE Extension (stdio)
    └── Headless CLI (websocket)
```

- Leader 持有共享的 Agent 状态，所有 Client 通过 Unix socket 通信
- 支持 Leader 版本检测和自动升级（新版本客户端可驱逐旧版本 Leader）
- Zombie Leader 检测（30 秒不可达即驱逐）

---

## 四、工具协议设计

### 4.1 工具类型系统

工具定义核心类型位于 `xai-grok-tools/src/types/`:

```rust
// definition.rs — 模型 API 的 Tool 定义
pub struct ToolDefinition {
    pub kind: ToolType,          // Function
    pub function: FunctionTool,  // { name, description, parameters }
}

// tool.rs — 工具分类枚举
pub enum ToolNamespace {
    GrokBuild, GrokBuildConcise, GrokBuildHashline,
    Codex, OpenCode, MCP,
}

pub enum ToolKind {  // 31 种工具分类
    Read, Edit, Delete, ListDir, Write, Move, Search,
    Lsp, Execute, Plan, WebSearch, WebFetch,
    BackgroundTaskAction, WaitTasksAction, KillTaskAction,
    List, Skill, MemorySearch, MemoryGet, Task,
    EnterPlan, ExitPlan, AskUser, ImageGen, VideoGen,
    ImageToVideo, ReferenceToVideo, DeployApp,
    SearchTool, UseTool, Monitor, GoalUpdate, Workflow, Other,
}
```

### 4.2 多工具集并存策略

Grok Build 的一个独特设计是**同时支持多套工具集**（namespace），来源包括：

| 工具集 | 来源 | 说明 |
|--------|------|------|
| `GrokBuild` | 自研 | 原生工具实现（bash, read_file, search_replace, grep, ...） |
| `GrokBuildConcise` | 自研 | 精简版工具描述，减少 token 消耗 |
| `GrokBuildHashline` | 自研 | 基于 hash-line 的编辑方式 |
| `Codex` | openai/codex | 从 Codex CLI 移植（read_file, list_dir, apply_patch, grep） |
| `OpenCode` | sst/opencode | 从 OpenCode 移植（read, write, edit, bash, grep, glob, skill, todo） |
| `MCP` | MCP 协议 | 外部 MCP 服务器提供的工具 |

**设计原则**：
- 工具注册通过 `ToolBridge` 统一管理（`xai-grok-agent/src/agent.rs:36`）
- `AgentBuilder` 通过 `with_tools()` / `with_disallowed_tools()` 控制工具可见性（`builder.rs:321-327`）
- 兼容模式扫描 `.claude/` / `.cursor/` 目录自动发现外部规则和工具（`builder.rs:108-110` 的 `CompatConfig`）
- 第三方工具集（Codex, OpenCode）的移植在 `THIRD_PARTY_NOTICES.md` 中声明

### 4.3 工具提醒 (Reminders)

工具执行后自动注入系统提醒（`types/tool.rs:125-139`）：

```rust
pub trait Reminder {
    fn requires_expr(&self) -> Expr<ToolRequirement>;
    async fn collect_reminders(&self, resources: SharedResources, tool_output: &ToolOutput)
        -> Vec<String>;
}
```

- **Per-tool reminders**：read_file 空文件提醒、offset 越界提醒
- **Cross-cutting reminders**：技能发现提醒 (`SkillDiscoveryReminder`)
- 提醒内容作为 `system-reminder` 注入下一轮对话

### 4.4 Backend-hosted Tools

部分工具（web_search, x_search）可以作为**服务端原生工具**发送，由 agentic sampler 在服务端执行（`agent.rs:43-49` 的 `hosted_tools`）。这种设计：
- 减少本地执行延迟
- 避免将搜索结果作为长文本消耗 context window
- 通过 `backend_search_enabled` + `supports_backend_search` 双重开关控制

---

## 五、上下文管理

### 5.1 Compaction 策略

`xai-grok-agent/src/compaction.rs` 定义了会话级 CompactionPolicy：

```rust
pub struct CompactionPolicy {
    pub auto_compact_threshold_percent: u32,  // 默认 85%
    pub compact_model: Option<String>,        // 可选专用 compaction 模型
    pub memory_flush_enabled: bool,           // compaction 前是否刷新记忆
    pub wall_clock_budget_secs: u64,          // 超时保护 (默认 300s)
    pub two_pass_enabled: bool,               // 两阶段 compaction
}
```

### 5.2 两阶段 Compaction (Two-Pass)

`session/compaction.rs` 实现了创新的两阶段压缩：

1. **Pass 1 (Prefire)**：当 token 使用量接近阈值前（default_lead = 10%），在后台异步生成历史前缀的摘要 NOTE₁
2. **Pass 2 (Tail)**：实际 compaction 时，将 NOTE₁ + 最近尾部拼接，再用模型生成最终摘要

**Prefire 失效检测**（`compaction.rs:48-65`）：
```rust
fn fingerprint_prefix(items: &[ConversationItem]) -> u64 {
    // 对 item 类型 + 文本内容做 hash
    // 如果 prefix 被编辑/rewind/branch，指纹变化，NOTE₁ 失效
}
```

### 5.3 ChatStateActor

对话状态由独立的 `ChatStateActor` 管理：
- 维护 `ConversationItem` 数组（System, User, Assistant, ToolResult, Reasoning）
- 跟踪 prompt_index、token 计数
- 发送事件（`ConversationReset`, `ImageBudget`, `PromptIndexChanged`, `TokensUpdated`）
- 支持图片预算管理和 eviction

### 5.4 记忆系统

`xai-grok-memory` crate 提供跨会话记忆：
- **Idle flush**：空闲时自动将对话摘要持久化到记忆存储
- **Dream consolidation**：定期后台运行记忆整合
- **Session end hook**：会话结束时的记忆保存
- `memory_search` / `memory_get` 工具供 Agent 检索历史知识

---

## 六、并发与子代理

### 6.1 SubagentCoordinator

子代理协调器在 `xai-grok-tools/src/implementations/grok_build/task/coordinator.rs`：

```rust
pub struct SubagentCoordinator<Runner: ChildRunner> {
    // 管理 pending/active/completed 子代理
    // 处理 spawn / await / cancel / inspect 操作
    // 支持 foreground budget 和 buffer_completions
}
```

**核心设计**（`agent/mvp_agent/subagent_coordinator.rs:148-184`）：
- `ShellChildRunner` 实现 `ChildRunner` trait，在 shell 进程内运行子代理
- 子代理作为新的 `SessionActor` 创建，拥有独立的会话上下文
- `LocalRef<MvpAgent>` 非 Send 引用，`spawn_local` 在同一 LocalSet 中运行

### 6.2 子代理生成流程

```
父会话 task 工具调用
  → ChannelBackend 发送 Spawn 事件
  → SubagentCoordinator 接收
  → ShellChildRunner::run()
    → try_build_subagent_spawn_context()  # 构建生成上下文
    → 继承父会话的:
        - MCP 连接池 (parent_mcp_pool)
        - Client hooks (client_hooks)
        - 工具定义 (parent_tool_definitions)
    → run_shell_child()  # 创建新 SessionActor
    → 返回 SubagentResult
```

### 6.3 并行工具执行

在 `tool_dispatch.rs:41-59` 中，工具调用通过 `lock_path_for_args()` 判断文件冲突：
- 相同文件路径的编辑操作 → 串行执行（共享 Mutex）
- 不同文件的操作 → 完全并发执行
- `target_directory`（list_dir）不参与文件锁

---

## 七、权限安全与沙箱

### 7.1 权限系统

`xai-grok-workspace/src/permission/` 实现了多层权限架构：

| 层级 | 文件 | 功能 |
|------|------|------|
| 规则解析 | `rules.rs` | 解析 `--allow Bash(git *)` 等规则语法 |
| 策略编译 | `policy.rs` | `CompiledPolicy` 匹配引擎 |
| 自动模式 | `auto_mode.rs` | 启发式 + LLM 分类器自动决策 |
| 权限管理 | `manager.rs` | `PermissionManager` 集中决策 |
| Shell 访问 | `shell_access.rs` | 受保护编辑权限 |
| 执行风险 | `exec_risk.rs` | 命令风险评估 |

**权限规则语法示例**（`rules.rs`）：
```
--allow '*'                    # 允许所有
--allow 'Bash(git *)'          # 允许 git 命令
--allow 'Bash(touch *)'         # 允许 touch 命令
--allow 'MCP(server:tool)'      # 允许 MCP 工具
--allow 'WebFetch(*.example.com)' # 允许特定域名
```

**Auto Mode 分类器**（`auto_mode.rs`）：
- **快速路径 (Heuristic)**：模式匹配已知安全操作
- **LLM 路径**：对未知操作发送轻量分类请求
- `access_requires_user_interaction()` 判断是否需要人工介入

### 7.2 沙箱机制

`xai-grok-sandbox/src/lib.rs` 基于 `nono` crate 实现 OS 级沙箱：

**Profile 类型**（`profiles.rs`）：
- `Off`：关闭沙箱
- `Workspace`：限制到工作区
- `Devbox`：开发容器（bwrap 实现）
- `Custom(name)`：自定义配置

**沙箱层次**：
1. **进程级**：通过 `nono` 的 Landlock (Linux) / Seatbelt (macOS) 限制文件访问
   - `apply()` 方法不可逆（`lib.rs:162`）
   - 失败时优雅降级，记录日志但继续运行
2. **子进程级**：通过 seccomp 过滤子进程网络（`child_net.rs`）
3. **bwrap 模式**（Linux）：通过 bubblewrap 重新执行进程
   - `deny_write` 路径以只读挂载
   - `deny_read` 路径以不可读占位符覆盖
4. **Hook write-deny**：直接钩子写入保护

**网络策略**（`network_policy.rs`）：
- 进程级网络保持开放（Agent 需要 LLM API）
- 子进程网络可选择性阻断
- 网站级策略：`WebsitePolicy { allow, deny }`

### 7.3 YOLO 模式与 Always-Approve Pin

- YOLO 模式：自动批准所有权限请求
- Always-Approve Pin：通过 `requirements.toml` 强制禁用 YOLO（`spawn.rs:9-32`）
- Pin 激活时，CLI 的 catch-all `--allow` 规则被丢弃，仅保留 scoped 规则

---

## 八、可扩展性与插件架构

### 8.1 ACP (Agent Client Protocol)

`xai-acp-lib` 实现标准化的 Agent-Client 协议，支持：
- 工具调用和结果传输
- 会话更新和通知
- 权限请求流程
- 客户端能力协商（文件系统、终端、MCP 等）

### 8.2 MCP (Model Context Protocol)

`xai-grok-mcp` crate 提供：
- MCP 服务器生命周期管理（启动、健康检查、自动重启）
- 工具发现和注册
- 渐进式初始化（`McpInitStrategy::Progressive`）vs 阻塞式（`Blocking`）
- MCP 工具结果截断（session-scoped `max_output_bytes`）
- Liveness watcher 监控服务器状态

### 8.3 Workflow 引擎

`xai-workflow/src/engine.rs` 基于 Rhai 脚本的工作流引擎：

- **确定性执行**：禁用 `timestamp()` 和 `sleep()`，确保 resume 可重放
- **Journal 机制**：记录每次 host call 的输入/输出，支持断点续传
- **并行调度**：`MAX_PARALLEL` 控制最大并发 agent 调用
- **预算控制**：`max_ops`（默认 1 亿）防止无限循环
- **暂停/取消**：`PauseKind` 支持暂停和取消信号

### 8.4 插件系统

`xai-grok-agent/src/plugins/`：
- **插件发现**：扫描 `~/.grok/plugins/` 和 marketplace
- **Git 安装**：从 Git 仓库安装插件
- **Manifest 解析**：插件元数据（工具、hooks、技能）
- **信任机制**：插件信任验证（`trust.rs`）
- **Marketplace 集成**：`xai-grok-plugin-marketplace`

### 8.5 Hook 系统

`xai-grok-hooks` 提供事件驱动的扩展点：
- `SessionStart`, `SessionEnd`, `PromptSubmitted`, `PreToolUse`, `PostToolUse` 等事件
- 非阻塞分发（`dispatch_non_blocking`）
- Hook 注册表（`HookRegistry`）
- 执行结果通过 `XaiSessionUpdate` 通知上报

### 8.6 外部会话兼容

`xai-grok-workspace/src/foreign_sessions/`：
- **Claude 会话导入**：读取 `.claude/projects/` 下的对话历史
- **Codex 会话导入**：读取 Codex CLI 的会话数据库
- **能力适配**：将外部会话转换为 Grok Build 可用的格式

### 8.7 Skill 系统

`xai-grok-tools/src/implementations/skills/`：
- 从文件系统发现 SKILL.md 文件
- 支持 `.grok/skills/`, `.claude/skills/`, `.cursor/skills/`
- 自动注入到 system prompt 的 `<available_skills>` 块
- 支持 announced/pending 状态管理

---

## 九、工程取舍与设计决策

### 9.1 Rust 选择

- **零成本抽象**：工具 trait、async 零开销
- **内存安全**：避免 GC 暂停，适合长时间运行的 Agent 进程
- **编译时保证**：`!Send` 类型强制单线程 LocalSet（如 `ShellChildRunner`）
- **跨平台**：macOS/Linux 一等支持，Windows best-effort

### 9.2 单线程 per-Session

**优势**：
- 消除所有锁竞争，状态变更天然串行
- `RefCell` 代替 `Mutex`/`RwLock`，零开销
- 调试简单，调用栈清晰

**代价**：
- 单个会话严重依赖 I/O 并发时受限于单线程
- 工具执行必须 async（不能阻塞 event loop）
- 子代理需要独立运行时

### 9.3 多工具集并存

**设计理由**：
- 兼容 Claude Code、Codex CLI、OpenCode 生态（`.claude/`, `.cursor/` 目录）
- 不同工具集适应不同场景（concise 减少 token，hashline 支持大文件编辑）
- 厂商锁定防范：用户可以切换到不同的工具集

**代价**：
- 维护成本高（多套工具需要同步更新）
- 工具语义映射复杂（不同工具集参数名不同，如 file_path vs target_file）
- 模型需要理解不同工具集的差异

### 9.4 Generated Cargo.toml

根 `Cargo.toml` 由 monorepo 工具生成，标记为只读（`README.md:109-112`）。这反映了 xAI 内部 monorepo 架构的工程约束。

### 9.5 逐渐式沙箱

沙箱采用分阶段、可降级的设计（`lib.rs:222-231`）：
- 如果 `nono` 不支持当前平台，优雅降级并记录日志
- 如果 `bwrap` 不可用，跳过但继续运行
- 仅在不安全的降级可能导致安全问题时 fail-closed（如 hook write-deny）

### 9.6 Prompt 渲染分离

`xai-grok-agent/src/prompt/context.rs` 将系统提示拆分为多个可组合的部分：
- `<user_info>`：OS, Shell, 工作目录, 日期
- `<rules>`：项目规则、用户规则
- `<git_status>`：Git 状态
- `<project_context>`：项目文件树
- `<available_skills>`：发现的技能
- `<available_tools>`：工具列表
- `<system-reminder>`：动态注入的提醒

每个部分可单独开关，通过 `AgentDefinition` / `AgentBuilder` 控制。

### 9.7 使用 Record

`crates/codegen/xai-grok-tools/THIRD_PARTY_NOTICES.md` 声明了对 openai/codex 和 sst/opencode 工具实现的移植，遵循 Apache 2.0 §4(b) 变更声明。

---

## 十、可复用的 Coding Agent 设计原则

### 原则 1：事件驱动的单线程 Actor 模型

> **源码参考**: `run_loop.rs:120-259`, `spawn.rs:39-42`

每个会话作为一个独立 Actor，运行在单线程 Tokio runtime 中。所有状态变更通过 `tokio::select!` 串行化处理，消除锁竞争。这种模型特别适合 Agent 应用——Agent 的状态更新天然是顺序的（一轮对话结束后才进入下一轮），不需要多线程并发修改状态。

**复用建议**：
- 如果你的 Agent 需要管理多个会话，为每个会话分配独立的单线程 runtime
- 使用 biased select 明确优先级：计时器 > 内部事件 > 外部命令

### 原则 2：多工具集分离策略

> **源码参考**: `types/tool.rs:33-46`, `builder.rs:321-327`

将工具按来源/用途划分为多个 Namespace，每个 Namespace 独立维护。Agent 可以根据场景（交互式/headless/IDE 嵌入）选择不同的工具集组合。这解决了"一套工具无法适应所有场景"的问题。

**复用建议**：
- 为工具定义 namespace 枚举
- 支持 per-agent 的工具白名单/黑名单
- 考虑提供"精简版"工具描述以减少 token 消耗

### 原则 3：两阶段上下文压缩 (Two-Pass Compaction)

> **源码参考**: `compaction.rs:31-33, 38-65`

在上下文接近阈值前，后台异步生成历史前缀摘要（Pass 1）；实际压缩时将前缀摘要 + 尾部拼接再生成最终摘要（Pass 2）。通过内容指纹检测前缀是否被编辑（如 rewind），失效时自动丢弃缓存。

**复用建议**：
- Pass 1 的 prefire lead（默认 10%）可以根据模型速度/上下文大小调节
- 指纹机制可以用简单 hash 替代，关键是检测内容变化
- 为 compaction 设置 wall-clock budget 防止 reasoning 模型跑飞

### 原则 4：分层权限决策

> **源码参考**: `permission/auto_mode.rs`, `permission/rules.rs`, `permission/policy.rs`

权限决策分为三层：
1. **规则层**：用户显式配置的 allow/deny 规则
2. **分类器层**：启发式 + LLM 自动分类
3. **交互层**：用户实时确认

每层可以短路后续决策，从快到慢、从自动到人工。

**复用建议**：
- 规则层支持 glob 模式匹配
- 分类器层可以先用简单启发式（已知安全命令），不可判定时回退 LLM
- 交互层支持"总是批准"选项（会话级/命令级）

### 原则 5：工具执行的文件冲突感知并发

> **源码参考**: `tool_dispatch.rs:41-59`

同一批次中的工具调用，通过分析目标文件路径判断是否存在写冲突：相同文件串行执行，不同文件并发执行。这在不引入复杂事务机制的前提下最大化并行度。

**复用建议**：
- 通过 `file_path` / `path` / `target_file` 参数提取目标文件
- 不参与文件锁定的操作（如 list_dir、search）完全并发
- 这种"乐观并发"策略在 Agent 场景中足够实用

### 原则 6：Leader-Follower 进程架构

> **源码参考**: `leader/mod.rs:1-33`

单机单 Leader 多 Client 架构，通过 Unix socket 通信。Leader 持有共享的 Agent 状态，多个客户端（TUI、IDE、headless）复用同一个状态。

**复用建议**：
- Leader 进程管理所有会话状态
- Client 进程负责 UI 渲染（每个 Client 模式可以完全不同：TUI vs IDE plugin vs Web）
- 支持 Leader 版本检测和自动升级（新版本 Client 可驱逐旧版本 Leader）

### 原则 7：Agent 定义的外部化

> **源码参考**: `xai-grok-agent/src/config.rs` (AgentDefinition), `builder.rs`

Agent 通过 `AgentDefinition` 定义文件配置（如 `agents/code-reviewer.md`），而不是硬编码。支持：
- 工具白名单/黑名单
- 自定义 system prompt
- permission mode
- skills 列表
- 模式预设（plan mode, auto mode 等）

**复用建议**：
- Agent 定义应该是数据而不是代码
- 支持从文件加载和程序化构建两种方式
- Prompt 渲染与 Agent 定义分离，支持运行时切换

### 原则 8：MCP 渐进式集成

> **源码参考**: `sampler_turn.rs:112-127`

MCP 服务器初始化支持两种策略：
- `Blocking`：等待所有 MCP 服务器就绪后才开始首轮对话
- `Progressive`：不等待，首轮仅使用内置工具，后续轮次逐步加入 MCP 工具

**复用建议**：
- 交互式场景用 Progressive（减少启动延迟）
- headless/CI 场景用 Blocking（确保所有工具可用）
- 支持 MCP 服务器的自动重启和健康检查

### 原则 9：Sandbox 的优雅降级

> **源码参考**: `sandbox/lib.rs:222-231`, `sandbox/lib.rs:177-189`

沙箱采用可降级设计：在支持的平台（Linux/macOS）上使用 kernel 级隔离，不支持的平台降级到纯软件保护。降级时记录日志但不中断服务，仅在关键安全边界（如 hook write-deny）fail-closed。

**复用建议**：
- 区分"必须强制执行"和"尽力而为"的安全措施
- 为每个安全层级定义降级策略（fail-open vs fail-closed）
- 沙箱状态应该在进程启动时一次性设置（不可逆），避免运行时动态切换

### 原则 10：子代理的继承式上下文

> **源码参考**: `subagent_coordinator.rs:63-71`, `spawn.rs`

子代理从父会话继承关键上下文：
- MCP 连接池（避免重新建立连接）
- Client hooks（保持钩子链完整）
- 工具定义（子代理可用的工具集）

但子代理运行在独立的 SessionActor 中，拥有独立的会话历史和状态。

**复用建议**：
- 继承网络连接（MCP、数据库等）避免重复建立
- 继承钩子和权限策略保持一致性
- 隔离对话历史和 tool state 避免污染父会话

---

## 十一、关键源码路径索引

| 关注点 | 路径 |
|--------|------|
| Agent Loop | `crates/codegen/xai-grok-shell/src/session/acp_session_impl/run_loop.rs` |
| Turn 采样 | `crates/codegen/xai-grok-shell/src/session/acp_session_impl/turn.rs` |
| 工具定义 | `crates/codegen/xai-grok-tools/src/types/definition.rs` |
| 工具分类 | `crates/codegen/xai-grok-tools/src/types/tool.rs` |
| Agent 构建 | `crates/codegen/xai-grok-agent/src/builder.rs` |
| Prompt 上下文 | `crates/codegen/xai-grok-agent/src/prompt/context.rs` |
| Compaction | `crates/codegen/xai-grok-shell/src/session/compaction.rs` |
| 权限系统 | `crates/codegen/xai-grok-workspace/src/permission/mod.rs` |
| 沙箱 | `crates/codegen/xai-grok-sandbox/src/lib.rs` |
| 子代理协调 | `crates/codegen/xai-grok-shell/src/agent/mvp_agent/subagent_coordinator.rs` |
| Leader IPC | `crates/codegen/xai-grok-shell/src/leader/mod.rs` |
| Workflow 引擎 | `crates/codegen/xai-workflow/src/engine.rs` |
| MCP 集成 | `crates/codegen/xai-grok-shell/src/session/mcp_dispatcher.rs` |
| 工具实现 | `crates/codegen/xai-grok-tools/src/implementations/` |
| Session Actor | `crates/codegen/xai-grok-shell/src/session/acp_session.rs` |

---

> **总结**: Grok Build 的架构展示了生产级 coding agent 的核心设计模式：事件驱动的单线程 Actor 模型、多工具集分离策略、分层权限决策、两阶段上下文压缩、文件冲突感知的并行执行、以及可降级的沙箱机制。这些原则可直接应用于构建类似的 AI 编程代理系统。
