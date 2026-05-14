---
title: Yi 模型
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, open-source, llm, deeplearning]
sources: [raw/papers/2403.04652-Yi-Open-Foundation-Models-by-01AI.html]
---

# Yi 模型

Yi 是零一万物（01.AI）发布的一系列开源基础语言模型，由李开复团队开发。Yi 模型基于 6B 和 34B 预训练语言模型，扩展出 chat 模型、200K 长上下文模型、depth-upscaled 模型和视觉语言模型。Yi 系列的核心竞争力来自其**数据工程质量**，使用 3.1T Token 的高工程化语料从零训练，达到接近 GPT-3.5 的基准分数和人类偏好。[[raw/papers/2403.04652-Yi-Open-Foundation-Models-by-01AI.html]]

## 模型设计哲学

Yi 的设计核心关注以下维度：

1. **模型规模选择**：34B 在 RTX 4090 (24G) 上 INT4 量化后可推理，兼顾推理能力和部署成本
2. **数据量补偿**：34B 小于 Chinchilla 最优的 70B，因此增加训练数据至 3.1T Token（过训练 regime）以补偿计算量
3. **数据质量优先**：预训练和微调均采用质量优先策略
4. **微调数据精细化**：仅使用 <10K 条人工精选指令（每条由 ML 工程师逐一验证），对标 LIMA 方法论

## 模型规格

- **Yi-6B**：60 亿参数
- **Yi-34B**：340 亿参数
- 上下文窗口：4K（基础版）→ 200K（长上下文版，通过轻量级持续预训练扩展）
- 基于 [[transformer-architecture]] 的 Decoder-only 架构

## 数据工程

Yi 的预训练数据清洗系统特点：

- **多维过滤管线**：语言、启发式文本特征、困惑度、语义、主题、安全
- **级联去重**：段落级、MinHash、精确匹配三级去重
- 移除率远高于 CCNet、RefinedWeb、RedPajama 等现有管线
- 预训练语料：3.1T Token（英文 + 中文）

## 核心特性

### 长上下文能力

Yi 系列的一个突出特点是其 200K Token 的超长上下文窗口：

- 通过轻量级持续预训练扩展上下文
- 在 needle-in-a-haystack 检索任务上表现出色
- 无论序列长度和信息位置如何，均可成功检索

### Depth Upscaling

通过对预训练 checkpoint 进行深度扩展（增加层数）并持续预训练，进一步提升性能。

### 视觉语言

- 将 chat 语言模型与 vision transformer encoder 结合
- 训练模型将视觉表示对齐到语言模型的语义空间

## 性能表现

Yi-34B 在发布时在多项基准上表现优异：

- 在 MMLU、CommonSenseQA、PIQA 等多项基准上性能接近 GPT-3.5
- Yi Chat 在 AlpacaEval 和 Chatbot Arena 等人类偏好平台上表现强劲
- 在中文任务上具有显著优势
- 200K 上下文版本在长文本检索和推理任务上表现出色

## 版本变体

- **Yi-6B/34B Base**：基础预训练模型
- **Yi-6B/34B Chat**：通过 SFT + RLHF 对齐的对话模型（<10K 指令微调）
- **Yi-VL**：视觉语言多模态模型
- **Yi-Coder**：代码专项模型

## 架构设计

Yi 采用经典 [[transformer-architecture]] Decoder 架构，关键设计选择包括：

- RMSNorm 归一化
- RoPE 位置编码
- SwiGLU 激活函数
- FlashAttention 加速训练
- GQA（Grouped-Query Attention）

## 与同类模型对比

- 相比 [[qwen]] 系列，Yi 在长上下文处理上有独特优势（200K vs 32K）
- 相比 [[llama]] 系列，Yi 在中文任务上表现更强
- Yi-34B 以约一半参数量达到接近 LLaMA 2 70B 的性能（得益于 3.1T Token 过训练）
- 与 [[phi]] 系列类似，Yi 也强调数据质量对模型性能的决定性作用

## 生态影响

Yi 模型的开源为中文 AI 社区提供了更多选择，其长上下文能力和数据工程方法论推动了社区对超长上下文技术和数据质量的研究关注。
