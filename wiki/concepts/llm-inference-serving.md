---
title: LLM 推理服务优化——显存/延迟/吞吐三本账
created: 2026-07-24
updated: 2026-07-24
type: concept
tags: [inference, optimization, infra, llm]
sources: []
---

# LLM 推理服务优化——显存/延迟/吞吐三本账

自回归 decode 的根问题不是「模型算得慢」，而是**串行依赖 + 每步硬件利用率低**：第 t+1 个 token 的输入含第 t 个 token，t 没落地 t+1 就不能开始；每步只处理少量 token，却要把整套权重和不断增长的 KV cache 搬过计算单元，于是单 token decode 通常是 **memory-bound**——算力在等数据搬运。理解任何一项推理优化，先问它动的是哪一本账。

## 三本账的分工

不同优化改善不同指标，别用同一把尺子衡量：

```text
账目        典型手段                           主要改善指标
显存账      GQA/MQA、KV 量化、PagedAttention   同显存容纳更多有效 token → 更大 batch
延迟账      speculative decoding、Medusa       减少一个请求需要的串行大模型轮次
吞吐账      continuous / iteration-level batching  一张卡同时服务更多不等长请求、少空转
```

这三本账争夺同一批 GPU 计算与显存资源，必须在**真实并发分布**下一起评测——局部资源利用率最高，不等于线上目标最优。

## 显存账：KV cache 与 PagedAttention

**为什么 KV cache 既省计算又成瓶颈**：它是「用空间换计算」的经典交换——不缓存则每步重算历史 K/V，缓存则只算新 token 但必须持续保存并读取全部历史状态。KV 大小由**层数 × KV head 数 × head dim × 精度**决定，不是只看参数量；GQA/MQA 正是在推理侧大幅减 KV 的架构设计（Llama 2 70B 用 8 个 KV head，每 token 约 320 KiB；无 GQA 的 OPT-13B 每 token 高达 800 KB）。

**PagedAttention**（Kwon et al., SOSP 2023, arXiv:2309.06180）解决的不是「有效 KV 太大」，而是 **allocator/layout 的浪费**：旧式为每个请求按最大长度预分配一整块连续空间，profiling 显示只有 20.4%–38.2% 真正装有效 token，其余是 reservation（预留）/ internal（尾部永不用）/ external（空闲但不连续）三类碎片。解法与操作系统分页同形——把 KV 切成固定 token 数的逻辑块、允许物理非连续、用 block table 映射：

```text
逻辑 KV：  [L0] [L1] [L2] [L3]     ← 请求看到的连续上下文
             ↓ block table
物理显存： [P7] [P1] [P8] [P3]     ← 任意空闲块可复用
```

按需增长、消灭外部碎片、压低内部碎片、允许前缀/beam 共享（copy-on-write）。它主要改善**吞吐**（更大 batch 摊薄权重搬运），不保证 batch=1 单请求每 token 延迟同比下降，也不改变自回归的串行依赖。详见 [[2026-07-14-kv-cache-paged-attention]]。

## 延迟账：投机解码

自回归每步串行等上一个 token，投机解码用便宜的 draft 模型 q 先猜 k 个候选，大模型 p 在**一次前向里并行核验**：候选序列已给定，p 可像短 prefill 一样并行给每个位置打分。「验证比生成便宜」不是每 token 的 FLOPs 更少，而是 k 个位置合进一次调用、更易并行、摊薄权重读取与 kernel launch——它甚至增加总 FLOPs，却降低 wall-clock latency（**牺牲算力效率换延迟效率**）。

- **无损性**：随机采样时以 `accept(x)=min(1, p(x)/q(x))` 接受，拒绝后从残差分布 `max(0,p−q)` 归一化重采，产出 token 严格服从 p——经典投机解码是无损调度，不是量化式近似压缩。
- **接受率 α 是加速比总闸门**：每轮平均推进 `(1−α^{k+1})/(1−α)` 个 token；α 越低、k 越大边际存活率越低，别看到「一次验 k 个」就声称 k 倍加速。
- **Medusa** 去掉独立 draft 模型，在主干 hidden state 上挂多个 decoding head + tree attention，用「更远位置条件更弱」换掉「调度两个模型」的成本。

会更慢的场景：draft 与目标不一致（高温/跨语言/稀有标识符拉低 α）、draft 太贵、k 太大、高并发已填满 GPU（增每请求计算损总吞吐）。详见 [[2026-07-23-speculative-decoding-latency]]。

## 吞吐账：continuous batching

生产 serving 的真问题是「一张卡同时服务几百条不等长请求怎么不空转」。static batching 要等整个 batch 里最慢的那条解码完，GPU 大量空泡；**continuous / iteration-level batching** 改成每条序列一解码到 EOS 就立刻退场、新请求即时补进 batch 维度，把利用率拉满。它和 PagedAttention 是一套：**前者填满 batch 维、后者填满显存维**。（本页此账待专题伴读笔记补全后回填细节。）

## 判断框架

看到任何推理优化，依次问：

```text
它减少的是：A 有效状态本身？(GQA/量化)  B 无效分配与碎片？(PagedAttention)
           C 重复计算/存储？(prefix caching)  D 权重搬运摊销？(continuous batching)
           E 串行轮次？(speculative decoding)
它改善的是：首 token 延迟 / 每 token 延迟(ITL) / 吞吐 / 每 token 成本 / 质量不回退
```

## 相关概念

- [[flash-attention]] — attention kernel 的 IO-aware 优化，与本页的显存/搬运账互补
- [[model-quantization]] — 从「有效状态」一端减 KV/权重，另一条降本路径
- [[mixture-of-experts]] — 参数量与每-token 计算量解耦，推理侧另一根账（routing/负载均衡）
- [[scaling-laws]] — 训练侧的算力分配账，与推理侧成本账对照

## 伴读来源

- [[2026-07-14-kv-cache-paged-attention]] — 显存账：memory-bound、KV 显存核算、PagedAttention 分页解法
- [[2026-07-23-speculative-decoding-latency]] — 延迟账：接受率、无损采样、Medusa、何时更慢
