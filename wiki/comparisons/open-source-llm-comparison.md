     1|---
     2|title: 2024-2025 开源 LLM 对比
     3|created: 2026-05-10
     4|updated: 2026-05-10
     5|type: comparison
     6|tags: [comparison, llm, open-source, llama, qwen, deepseek, mistral]
     7|sources: [raw/papers/2412.19437-DeepSeek-V3-Technical-Report.md, raw/papers/2501.12948-DeepSeek-R1-Incentivizing-Reasoning-Capability-in-LLMs-via-R.md, raw/papers/2405.04434-DeepSeek-V2-A-Strong-Economical-and-Efficient-Mixture-of-Exp.md, raw/papers/2309.16609-Qwen-Technical-Report.md, raw/papers/2401.04088-Mixtral-of-Experts.md, raw/papers/2310.06825-Mistral-7B.md, raw/papers/2403.08295-Gemma-Open-Models-Based-on-Gemini-Research-and-Technology.md, raw/papers/2403.04652-Yi-Open-Foundation-Models-by-01AI.md, raw/papers/2309.05463-Textbooks-Are-All-You-Need-II-phi-15-technical-report.md, raw/papers/2406.12793-ChatGLM-A-Family-of-Large-Language-Models-from-GLM-130B-to-G.md]
     8|---
     9|
    10|# 2024-2025 开源 LLM 对比
    11|
    12|主流开源大语言模型按尺寸分档对比，覆盖推理、代码、数学、多语言等核心能力。
    13|
    14|## 按尺寸分档
    15|
    16|### ≤7B 轻量级
    17|
    18|| 模型 | 参数量 | 架构 | 推理 | 代码 | 数学 | 多语言 | 上下文 |
    19||------|--------|------|------|------|------|--------|--------|
    20|| **Qwen2.5-7B** | 7B | Dense | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 128K |
    21|| **Mistral-7B** | 7B | Dense | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 32K |
    22|| **Gemma 2 9B** | 9B | Dense | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 8K |
    23|| **Phi-4** | 14B | Dense | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 16K |
    24|| **Yi-1.5-9B** | 9B | Dense | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 4K |
    25|
    26|### 14B–32B 中量级
    27|
    28|| 模型 | 参数量 | 架构 | 推理 | 代码 | 数学 | 多语言 | 上下文 |
    29||------|--------|------|------|------|------|--------|--------|
    30|| **Qwen2.5-32B** | 32B | Dense | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 128K |
    31|| **DeepSeek-V2-Lite** | 16B | MoE (2/160) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 128K |
    32|| **Mixtral 8x22B** | 141B | MoE (8/39) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 64K |
    33|
    34|### ≥65B 大参数
    35|
    36|| 模型 | 参数量 | 架构 | 推理 | 代码 | 数学 | 多语言 | 上下文 |
    37||------|--------|------|------|------|------|--------|--------|
    38|| **DeepSeek-V3** | 671B | MoE (37/256) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 128K |
    39|| **DeepSeek-R1** | 671B | MoE (37/256) | ⭐⭐⭐⭐⭐+ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐+ | ⭐⭐⭐⭐ | 128K |
    40|| **LLaMA 3.1 405B** | 405B | Dense | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 128K |
    41|| **Qwen2.5-72B** | 72B | Dense | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 128K |
    42|
    43|## 核心差异分析
    44|
    45|### MoE vs Dense
    46|
    47|| 维度 | Dense (LLaMA, Qwen2.5) | MoE (DeepSeek, Mixtral) |
    48||------|------------------------|-------------------------|
    49|| 推理速度 | 参数量越大越慢 | 激活参数少，速度快 |
    50|| 训练成本 | 高 | 训练大但激活少 |
    51|| 部署显存 | 需全部加载 | 可部分加载 |
    52|| 效果上限 | 高 | 更高（参数空间大） |
    53|
    54|DeepSeek-V3 采用 671B 总参数但仅激活 37B，以 8B 级推理成本达到 405B Dense 级效果。[[raw/papers/2412.19437-DeepSeek-V3-Technical-Report.html]]
    55|
    56|### 推理能力突破
    57|
    58|DeepSeek-R1 通过 RL 强化推理链，在数学和代码上超越 GPT-4o 级别。[[raw/papers/2501.12948-DeepSeek-R1-Incentivizing-Reasoning-Capability-in-LLMs-via-R.html]]
    59|
    60|### 多语言能力
    61|
    62|Qwen 系列在中文和跨语言任务上领先，LLaMA 英文最强，Mistral 欧洲语言优势明显。
    63|
    64|## 选型建议
    65|
    66|| 场景 | 推荐 |
    67||------|------|
    68|| 本地部署轻量 | Qwen2.5-7B |
    69|| 性价比推理 | DeepSeek-V3 (MoE) |
    70|| 深度推理 | DeepSeek-R1 |
    71|| 纯英文任务 | LLaMA 3.1 / Gemma |
    72|| 代码生成 | Phi-4 / Qwen2.5-32B |
    73|| 中文场景 | Qwen2.5 系列 |
    74|
    75|## 相关链接
    76|
    77|- [[deepseek-v3]] — DeepSeek V3 技术详解
    78|- [[deepseek-r1]] — DeepSeek R1 推理模型
    79|- [[llama]] — LLaMA 系列演进
    80|- [[qwen]] — Qwen 系列详解
    81|- [[mixture-of-experts]] — MoE 架构原理
    82|