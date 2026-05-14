---
title: 量化方法对比
created: 2026-05-10
updated: 2026-05-10
type: comparison
tags: [comparison, quantization, compression, deployment, inference]
sources: [raw/papers/2210.17323-GPTQ-Accurate-Post-Training-Quantization-for-Generative-Pre-Trained-Transformers.md, raw/papers/2301.00774-AWQ-Activation-aware-Weight-Quantization-for-LLM-Compression-and-Acceleration.md, raw/papers/2306.00978-AWQ-Activation-aware-Weight-Quantization-for-LLM-Compression.md]
---

# 量化方法对比

将 LLM 从 FP16 压缩到 INT4/INT8 以降低显存占用和推理延迟的四种主流后训练量化（PTQ）方法。

## 核心原理

量化将模型权重从高精度（FP16/BF16）映射到低精度（INT8/INT4），核心挑战是在精度损失最小化的同时最大化压缩比。

## 方法对比

| 维度 | GPTQ | AWQ | SparseGPT | GGUF |
|------|------|-----|-----------|------|
| **量化粒度** | Per-channel | Per-group | Per-channel + 稀疏 | Per-group |
| **核心思想** | 基于 Hessian 的二阶信息 | 保护高激活权重通道 | 权重稀疏化 + 量化 | 多种量化策略可选 |
| **支持精度** | INT3/4/8 | INT3/4/8 | INT3/4 | INT2/3/4/5/8 |
| **校准数据量** | ~128 条 | ~128 条 | ~128 条 | 无需校准 |
| **GPU 推理** | ✅ (ExLlama, vLLM) | ✅ (vLLM, AutoAWQ) | ⚠️ 有限 | ❌ 主要 CPU |
| **CPU 推理** | ❌ | ❌ | ❌ | ✅ (llama.cpp) |
| **精度损失 (INT4)** | 低 | 最低 | 低 | 中等 |
| **压缩比 (INT4)** | ~4x | ~4x | ~4x | ~4x |
| **量化速度** | 慢（逐层优化） | 快 | 中 | 即时（无需校准） |
| **开源模型可用性** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 方法详解

### GPTQ

基于近似二阶信息（Hessian 矩阵逆的近似），逐层优化量化误差。[[raw/papers/2210.17323-GPTQ-Accurate-Post-Training-Quantization-for-Generative-Pre-Trained-Transformers.html]]

- 量化时需要 GPU，速度较慢（几分钟到几十分钟）
- INT4 量化下精度损失极小
- 生态成熟，HuggingFace 上有大量 GPTQ 格式模型

### AWQ (Activation-aware Weight Quantization)

观察到一个关键发现：仅 1% 的显著权重通道（salient channels）对模型输出影响巨大。AWQ 保护这些通道不被过度量化。[[raw/papers/2301.00774-AWQ-Activation-aware-Weight-Quantization-for-LLM-Compression-and-Acceleration.html]]

- 量化速度比 GPTQ 快
- 同等精度下 AWQ 通常优于 GPTQ
- 适合 GPU 部署（vLLM 原生支持）

### SparseGPT

将权重分为重要权重和可剪枝权重，先做结构化稀疏剪枝再量化。[[raw/papers/2306.00978-AWQ-Activation-aware-Weight-Quantization-for-LLM-Compression.html]]

- 同时实现稀疏化和量化
- 理论精度损失最小
- 但实际部署生态不如 GPTQ/AWQ 成熟

### GGUF

llama.cpp 项目的量化格式，支持多种量化策略（Q4_K_M, Q5_K_S, Q8_0 等）。

- 无需校准数据，即时量化
- 主要用于 CPU 推理，支持消费级硬件
- 不同子格式（K-quant）在速度/精度间取舍
- 最广泛的模型可用性

## 常用 GGUF 子格式

| 格式 | 位数 | 特点 |
|------|------|------|
| Q8_0 | 8-bit | 几乎无精度损失 |
| Q5_K_M | ~5-bit | 精度与速度平衡 |
| **Q4_K_M** | ~4-bit | **最推荐的默认选择** |
| Q3_K_M | ~3-bit | 更激进压缩，精度有损 |
| Q2_K | ~2-bit | 极限压缩，质量下降明显 |

## 选型建议

| 场景 | 推荐 |
|------|------|
| GPU 服务端推理 | AWQ (最佳精度) / GPTQ (最广泛) |
| CPU / Mac 推理 | GGUF Q4_K_M |
| 边缘设备 | GGUF Q3_K_M / Q4_K_S |
| 最低精度损失 | AWQ INT4 / GGUF Q8_0 |
| 快速量化无需校准 | GGUF |

## 相关链接

- [[gptq]] — GPTQ 详解
- [[awq]] — AWQ 详解
- [[gguf]] — GGUF 格式与 llama.cpp
- [[llm-inference-optimization]] — 推理优化总览
- [[kv-cache]] — KV Cache 量化