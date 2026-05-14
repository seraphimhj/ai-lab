     1|---
     2|title: Mamba SSM
     3|created: 2026-05-10
     4|updated: 2026-05-10
     5|type: entity
     6|tags: [model, architecture, deeplearning, optimization]
     7|sources: [raw/papers/2312.00752-Mamba-Linear-Time-Sequence-Modeling.md]
     8|---
     9|
    10|# Mamba SSM
    11|
    12|Mamba 是一种基于选择性状态空间模型（Selective State Space Model）的序列建模架构，由 Tri Dao 和 Albert Gu 提出。Mamba 实现了线性时间复杂度的序列建模，在推理效率上显著优于基于 [[transformer-architecture]] 的注意力机制。[[raw/papers/2312.00752-Mamba-Linear-Time-Sequence-Modeling.html]]
    13|
    14|## 核心动机
    15|
    16|Transformer 的 Self-Attention 机制计算复杂度为 O(N²)，限制了其在长序列上的应用。Mamba 旨在保持 Transformer 级别的建模能力，同时实现 O(N) 的推理复杂度。
    17|
    18|## State Space Model (SSM) 基础
    19|
    20|SSM 将序列建模视为连续系统：
    21|
    22|$$h'(t) = Ah(t) + Bx(t)$$
    23|$$y(t) = Ch(t) + Dx(t)$$
    24|
    25|通过离散化后可以在序列数据上高效计算。传统 SSM（如 S4）的参数 A、B、C 是静态的，不随输入变化。
    26|
    27|## 选择性机制（Selective Mechanism）
    28|
    29|Mamba 的关键创新是使 SSM 参数**依赖于输入**：
    30|
    31|- **选择性扫描**：输入依赖的 B、C 参数使模型可以选择性地记忆或遗忘信息
    32|- **硬件感知算法**：通过扫描而非卷积的方式计算，优化 GPU 利用率
    33|- **输入依赖的步长**：允许模型自适应地控制信息更新速率
    34|
    35|## 模型规格
    36|
    37|- **Mamba-1**：基础版本，1.3B/2.8B 参数
    38|- **Mamba-2**：结构化状态空间对偶（SSD）框架，与注意力机制建立理论联系
    39|- 支持无限上下文长度（理论上）
    40|- 推理时 O(N) 时间和 O(1) 状态空间复杂度
    41|
    42|## 性能表现
    43|
    44|Mamba 在多个领域展现出竞争力：
    45|
    46|- 语言建模：在 Pile 基准上与同规模 Transformer 持平
    47|- 长序列建模：在信息检索和基因组学任务上优于 Transformer
    48|- 推理效率：推理吞吐量显著高于 Attention-based 模型
    49|
    50|## 混合架构
    51|
    52|实际应用中，Mamba 常与 [[transformer-architecture]] 结合使用：
    53|
    54|- [[jamba]] 将 Mamba 层与 Attention 层交替堆叠
    55|- [[griffin]] 结合 Gated Linear Recurrences 与 Local Attention
    56|
    57|## 局限性
    58|
    59|- 在需要精确 recall 的任务上不如 Attention
    60|- 长上下文训练的稳定性有待改进
    61|- 生态和工具链不如 Transformer 成熟
    62|
    63|## 影响
    64|
    65|Mamba 开辟了超越 Transformer 的序列建模新方向，激发了学术界对线性时间序列模型的广泛研究。
    66|