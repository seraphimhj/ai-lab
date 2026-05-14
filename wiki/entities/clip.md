---
title: CLIP
created: 2026-05-10
updated: 2026-05-14
type: entity
tags: [model, architecture, cv, multimodal]
sources: [raw/papers/2103.00020-Learning-Transferable-Visual-Models-From-Natural-Language-Su.html]
---

# CLIP

CLIP（Contrastive Language-Image Pre-training）是 [[openai]] 于 2021 年提出的多模态模型，通过自然语言监督学习视觉表示。CLIP 在零样本图像分类上达到了与有监督模型竞争的性能，开创了多模态学习的新范式。[[raw/papers/2103.00020-Learning-Transferable-Visual-Models-From-Natural-Language-Su.html]]

## 核心思想

CLIP 的关键创新在于**使用自然语言作为监督信号**，而非传统的固定类别标签。通过预测一批图像-文本配对中哪些是正确匹配的（对比目标而非精确文本预测），CLIP 在 **4 亿（image, text）** 配对数据（WIT 数据集，WebImageText）上学习了视觉和语言的联合多模态嵌入空间。论文证明这种对比学习方法比 captioning 预测方法效率高 4x 以上。

## 训练方法

### 对比学习

CLIP 使用对称交叉熵损失（symmetric cross entropy loss）进行训练，本质是 InfoNCE / multi-class N-pair loss：

1. 从数据集中采样一批 N 个 (图像, 文本) 配对
2. 图像编码器提取图像特征
3. 文本编码器提取文本特征
4. 计算所有 N×N 图像-文本对的余弦相似度
5. 最大化 N 个正确配对的相似度，最小化 N²-N 个错误配对的相似度
6. 温度参数 τ 作为可学习标量在训练中直接优化

训练简化设计：不使用非线性投影层（仅用线性投影映射到共享嵌入空间），不初始化 ImageNet 预训练权重，从头训练。

### 编码器架构

- **图像编码器**：ViT (Vision Transformer) 或 ResNet
- **文本编码器**：12 层 Transformer
- 两个编码器的输出投影到共享的嵌入空间

## 模型规模

- ViT-B/32：约 150M 参数
- ViT-B/16：约 150M 参数
- ViT-L/14：约 430M 参数
- ViT-L/14@336px：约 430M 参数（高分辨率版本）

## 性能表现

### 零样本分类

CLIP 的零样本分类能力是其最大亮点：

- ImageNet 上达到 76.2%（零样本）
- 在 30+ 数据集上平均零样本性能与有监督 ResNet-50 持平
- 在分布外数据上表现显著优于传统模型

### 鲁棒性

CLIP 在多种分布偏移下表现出更强的鲁棒性：

- 自然分布偏移（如素描、卡通风格的分类）
- 跨域迁移能力
- 对噪声和干扰的抵抗能力

## 局限性

- 在细粒度分类（如区分车型）上表现较弱
- 对抽象概念和计数任务能力有限
- 零样本性能在复杂任务上仍有差距
- 训练数据中的社会偏见会被继承

## 后续影响

CLIP 对多模态 AI 产生了深远影响：

- 开创了视觉-语言联合学习范式
- 催生了 Stable Diffusion、DALL·E 等文生图模型
- 为 [[gpt-4]] 等多模态模型奠定了技术基础
- CLIP 的嵌入空间被广泛用于图像检索和相似性搜索
- 与 [[transformer-architecture]] 中的 ViT 结合成为视觉编码标配
- 论文的 WIT 数据集构建方法影响了后续大规模多模态数据策略
