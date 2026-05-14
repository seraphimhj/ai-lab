     1|---
     2|title: RAG 方法对比
     3|created: 2026-05-10
     4|updated: 2026-05-10
     5|type: comparison
     6|tags: [comparison, rag, retrieval, agent, knowledge]
     7|sources: [raw/papers/2005.11401-Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.md, raw/papers/2310.11511-Self-RAG-Learning-to-Retrieve-Generate-and-Critique-through-Self-Reflection.md, raw/papers/2401.15884-Corrective-Retrieval-Augmented-Generation.md, raw/papers/2403.14403-Adaptive-RAG-Learning-to-Adapt-Retrieval-Augmented-Large-Language-Models-through.md, raw/papers/2404.16130-From-Local-to-Global-A-Graph-RAG-Approach-to-Query-Focused-Summarization.md]
     8|---
     9|
    10|# RAG 方法对比
    11|
    12|从基础 Naive RAG 到最新的 Agentic RAG，六种主流 RAG 架构的全面对比。[[raw/papers/2005.11401-Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.html]]
    13|
    14|## 架构概览
    15|
    16|### Naive RAG
    17|
    18|```
    19|Query → 检索器 (Embedding + Vector DB) → LLM 生成答案
    20|```
    21|
    22|最基础的检索增强生成。[[raw/papers/2005.11401-Retrieval-Augmented-Generation-for-Knowledge-Intensive-NLP-Tasks.html]]
    23|
    24|### Self-RAG
    25|
    26|```
    27|Query → [反思] 需要检索吗？→ [检索] → [反思] 检索结果相关吗？→ [生成+引用] → [反思] 有幻觉吗？
    28|```
    29|
    30|模型在生成过程中自主判断是否需要检索，并对每步进行自我反思。[[raw/papers/2310.11511-Self-RAG-Learning-to-Retrieve-Generate-and-Critique-through-Self-Reflection.html]]
    31|
    32|### CRAG (Corrective RAG)
    33|
    34|```
    35|Query → 检索 → [轻量级置信度评分] → ✅正确 → 使用 / ❌错误 → 纠正(搜索/Web) / ⚠️模糊 → 分解查询重试
    36|```
    37|
    38|对检索结果进行置信度评估，不信任时触发纠正机制。[[raw/papers/2401.15884-Corrective-Retrieval-Augmented-Generation.html]]
    39|
    40|### Adaptive-RAG
    41|
    42|```
    43|Query → [动态路由] → 无需检索直接生成 / 单次检索 / 多步检索
    44|         ↑
    45|    查询复杂度评估 (分类器)
    46|```
    47|
    48|根据查询复杂度自适应选择策略，简单问题直接回答，复杂问题多步检索。[[raw/papers/2403.14403-Adaptive-RAG-Learning-to-Adapt-Retrieval-Augmented-Large-Language-Models-through.html]]
    49|
    50|### GraphRAG
    51|
    52|```
    53|文档 → 实体/关系抽取 → 知识图谱 → 社区检测 → 社区摘要 → 全局查询 + 局部检索
    54|```
    55|
    56|利用知识图谱结构建模实体关系，擅长全局性、聚合性问题的回答。[[raw/papers/2404.16130-From-Local-to-Global-A-Graph-RAG-Approach-to-Query-Focused-Summarization.html]]
    57|
    58|### Agentic RAG
    59|
    60|```
    61|Query → Agent (规划/工具调用/多步推理) → [检索] → [重写] → [多源融合] → [验证] → 答案
    62|```
    63|
    64|以 Agent 为核心，自主决定检索策略、工具使用和多步推理。
    65|
    66|## 核心维度对比
    67|
    68|| 维度 | Naive RAG | Self-RAG | CRAG | Adaptive-RAG | GraphRAG | Agentic RAG |
    69||------|-----------|----------|------|--------------|----------|-------------|
    70|| **检索决策** | 总是检索 | 模型自主判断 | 总是检索 + 纠正 | 动态路由 | 图谱遍历 | Agent 决策 |
    71|| **反思能力** | ❌ | ✅ 多步反思 | ✅ 置信度纠正 | ✅ 适应 | ❌ | ✅ 全面 |
    72|| **全局推理** | ❌ | ❌ | ❌ | ❌ | ✅ 社区摘要 | ✅ |
    73|| **多步检索** | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ |
    74|| **实现复杂度** | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
    75|| **延迟** | 低 | 中 | 中 | 中 | 高 | 高 |
    76|| **适用场景** | 简单 QA | 通用 | 事实性 QA | 混合查询 | 全局分析 | 复杂任务 |
    77|
    78|## 各方法最佳场景
    79|
    80|| 场景 | 推荐 | 理由 |
    81||------|------|------|
    82|| 简单文档问答 | Naive RAG | 实现最简单，延迟最低 |
    83|| 需要引用来源 | Self-RAG | 自动生成引用标注 |
    84|| 检索质量不稳定 | CRAG | 自动纠正低质量检索 |
    85|| 查询复杂度差异大 | Adaptive-RAG | 简单查询不走检索 |
    86|| 全局趋势分析 | GraphRAG | 知识图谱聚合能力 |
    87|| 复杂研究任务 | Agentic RAG | 多工具协作，灵活应对 |
    88|
    89|## 演进趋势
    90|
    91|Naive RAG → Self-RAG/CRAG/Adaptive (反思+自适应) → GraphRAG (结构化知识) → Agentic RAG (自主决策)
    92|
    93|当前主流趋势是 **Agentic RAG + GraphRAG** 结合，兼具灵活性（Agent）和结构化推理（图谱）。
    94|
    95|## 相关链接
    96|
    97|- [[rag]] — RAG 基础概念
    98|- [[graph-rag]] — GraphRAG 详解
    99|- [[dense-passage-retrieval]] — 检索基础
   100|- [[embedding-models-2025]] — Embedding 模型选型
   101|- [[agent-paradigm-shift]] — Agent 范式
   102|