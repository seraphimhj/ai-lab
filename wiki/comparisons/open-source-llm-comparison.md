---
title: 2024-2025 开源 LLM 对比
created: 2026-05-10
updated: 2026-05-10
type: comparison
tags: [comparison, llm, open-source, llama, qwen, deepseek, mistral]
sources: [raw/papers/2412.19437-DeepSeek-V3-Technical-Report.html, raw/papers/2501.12948-DeepSeek-R1-Incentivizing-Reasoning-Capability-in-LLMs-via-R.html, raw/papers/2405.04434-DeepSeek-V2-A-Strong-Economical-and-Efficient-Mixture-of-Exp.html, raw/papers/2309.16609-Qwen-Technical-Report.pdf, raw/papers/2401.04088-Mixtral-of-Experts.html, raw/papers/2310.06825-Mistral-7B.html, raw/papers/2403.08295-Gemma-Open-Models-Based-on-Gemini-Research-and-Technology.html, raw/papers/2403.04652-Yi-Open-Foundation-Models-by-01AI.html, raw/papers/2309.05463-Textbooks-Are-All-You-Need-II-phi-15-technical-report.html, raw/papers/2406.12793-ChatGLM-A-Family-of-Large-Language-Models-from-GLM-130B-to-G.html]
---

# 2024-2025 开源 LLM 对比

主流开源大语言模型按尺寸分档对比，覆盖推理、代码、数学、多语言等核心能力。

## 按尺寸分档

### ≤7B 轻量级

| 模型 | 参数量 | 架构 | 推理 | 代码 | 数学 | 多语言 | 上下文 |
|------|--------|------|------|------|------|--------|--------|
| **Qwen2.5-7B** | 7B | Dense | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 128K |
| **Mistral-7B** | 7B | Dense | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 32K |
| **Gemma 2 9B** | 9B | Dense | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 8K |
| **Phi-4** | 14B | Dense | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 16K |
| **Yi-1.5-9B** | 9B | Dense | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 4K |

### 14B–32B 中量级

| 模型 | 参数量 | 架构 | 推理 | 代码 | 数学 | 多语言 | 上下文 |
|------|--------|------|------|------|------|--------|--------|
| **Qwen2.5-32B** | 32B | Dense | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 128K |
| **DeepSeek-V2-Lite** | 16B | MoE (2/160) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 128K |
| **Mixtral 8x22B** | 141B | MoE (8/39) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 64K |

### ≥65B 大参数

| 模型 | 参数量 | 架构 | 推理 | 代码 | 数学 | 多语言 | 上下文 |
|------|--------|------|------|------|------|--------|--------|
| **DeepSeek-V3** | 671B | MoE (37/256) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 128K |
| **DeepSeek-R1** | 671B | MoE (37/256) | ⭐⭐⭐⭐⭐+ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐+ | ⭐⭐⭐⭐ | 128K |
| **LLaMA 3.1 405B** | 405B | Dense | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 128K |
| **Qwen2.5-72B** | 72B | Dense | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 128K |

## 核心差异分析

### MoE vs Dense

| 维度 | Dense (LLaMA, Qwen2.5) | MoE (DeepSeek, Mixtral) |
|------|------------------------|-------------------------|
| 推理速度 | 参数量越大越慢 | 激活参数少，速度快 |
| 训练成本 | 高 | 训练大但激活少 |
| 部署显存 | 需全部加载 | 可部分加载 |
| 效果上限 | 高 | 更高（参数空间大） |

DeepSeek-V3 采用 671B 总参数但仅激活 37B，以 8B 级推理成本达到 405B Dense 级效果。[[raw/papers/2412.19437-DeepSeek-V3-Technical-Report.html]]

### 推理能力突破

DeepSeek-R1 通过 RL 强化推理链，在数学和代码上超越 GPT-4o 级别。[[raw/papers/2501.12948-DeepSeek-R1-Incentivizing-Reasoning-Capability-in-LLMs-via-R.html]]

### 多语言能力

Qwen 系列在中文和跨语言任务上领先，LLaMA 英文最强，Mistral 欧洲语言优势明显。

## 选型建议

| 场景 | 推荐 |
|------|------|
| 本地部署轻量 | Qwen2.5-7B |
| 性价比推理 | DeepSeek-V3 (MoE) |
| 深度推理 | DeepSeek-R1 |
| 纯英文任务 | LLaMA 3.1 / Gemma |
| 代码生成 | Phi-4 / Qwen2.5-32B |
| 中文场景 | Qwen2.5 系列 |

## 相关链接

- [[deepseek]] — DeepSeek V3 技术详解
- [[deepseek]] — DeepSeek R1 推理模型
- [[llama]] — LLaMA 系列演进
- [[qwen]] — Qwen 系列详解
- [[mixture-of-experts]] — MoE 架构原理
