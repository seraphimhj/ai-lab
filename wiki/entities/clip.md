---
title: CLIP
created: 2026-05-10
updated: 2026-05-10
type: entity
tags: [model, architecture, cv, multimodal]
sources: [raw/papers/2103.00020-Learning-Transferable-Visual-Models-From-Natural-Language-Su.md]
---

# CLIP

CLIP（Contrastive Language-Image Pre-training）是 [[openai]] 于 2021 年提出的多模态模型，通过自然语言监督学习视觉表示。CLIP 在零样本图像分类上达到了与有监督模型竞争的性能，开创了多模态学习的新范式。[[raw/papers/2103.00020-Learning-Transferable-Visual-Models-From-Natural-Language-Su.html]]

## 核心思想

CLIP 的关键创新在于**使用自然语言作为监督信号**，而非传统的固定类别标签。通过在 4 亿（图像，文本）配对数据上训练，CLIP 学习了视觉和语言的联合表示空间。

## 训练方法

### 对比学习

CLIP 使用 InfoNCE 对比损失函数进行训练：

1. 从数据集中采样一批 (图像, 文本) 配对
2. 图像编码器提取图像特征
3. 文本编码器提取文本特征
4. 计算所有图像-文本对的余弦相似度
5. 最大化正确配对的相似度，最小化错误配对的相似度

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
