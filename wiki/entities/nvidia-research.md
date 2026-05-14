---
title: NVIDIA Research
created: 2026-05-10
updated: 2026-05-10
type: entity
tags: [company, lab, inference, framework, infra]
sources: []
---

# NVIDIA Research

NVIDIA Research 是 NVIDIA 的研究部门，在 AI 计算、图形学和高性能计算领域具有全球领导地位。作为 AI 时代"卖铲子"的核心公司，NVIDIA 的硬件和软件生态是大语言模型训练和推理的基础设施。

## 核心硬件

### GPU 系列

- **A100**（2020）：Ampere 架构，AI 训练的主力 GPU
- **H100**（2022）：Hopper 架构，引入 Transformer Engine
- **B200/GB200**（2024）：Blackwell 架构，大幅提升推理性能
- **L40S/L40**：推理优化的 GPU

### 系统级产品

- **DGX**：AI 超级计算机
- **NVLink / NVSwitch**：GPU 间高速互联
- **Grace Hopper**：CPU+GPU 超级芯片

## 关键软件与框架

### CUDA

CUDA 是 NVIDIA 的并行计算平台，是现代 AI 的基石：

- 2006 年发布，开创了 GPU 通用计算的先河
- 支持几乎所有主流深度学习框架
- 持续演进的版本和功能（CUDA 12+）

### AI 软件栈

- **TensorRT**：高性能推理优化器
- **TensorRT-LLM**：大语言模型推理优化库
- **Triton**：开源的 GPU 编程语言
- **Cutlass**：线性代数优化库

## 研究贡献

### NV-Embed

NV-Embed 是 NVIDIA Research 发布的文本嵌入模型系列，在嵌入基准上表现优异。通过改进的训练策略和架构设计，NV-Embed 在 MTEB 等基准上达到了 SOTA 性能。

### NV-Retriever

NV-Retriever 是配套的检索模型，通过有效的 hard negative mining 策略提升了检索质量。

### FlashAttention

NVIDIA Research 对 FlashAttention 系列优化做出了重要贡献：

- FlashAttention-2/3：高效的 Attention 计算
- 减少内存访问，提升 GPU 利用率
- 是现代大模型训练的标准组件

## 加速计算生态

NVIDIA 构建了完整的 AI 加速计算生态：

- **NGC**：预训练模型和容器仓库
- **NIM**（NVIDIA Inference Microservices）：推理微服务
- **AI Enterprise**：企业级 AI 软件套件

## 行业影响

NVIDIA 的硬件和软件几乎支撑了整个 AI 行业。[[openai]]、[[google-deepmind]]、[[meta-ai]] 等公司的模型训练都严重依赖 NVIDIA GPU。其 CUDA 生态的护城河使得竞争对手难以撼动其市场地位。

## 挑战与竞争

- 自研芯片趋势（Google TPU、Amazon Trainium）
- 开源 AI 芯片（Groq、Cerebras 等）
- 地缘政治对供应链的影响
- 中国市场的替代需求（华为昇腾等）
