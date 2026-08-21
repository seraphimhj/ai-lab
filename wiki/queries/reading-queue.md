# 伴读发送队列（Reading Queue）

> **用途：控制“一篇在途、逐篇反馈”。**
> Hermes 每天发送第一条未勾选文章；如果该文章尚未收到“已读”或评论，次日继续发送同一篇。
> 收到反馈后将该条勾选，下一次运行才发送后一篇。
> 队列未清空时，Hermes 不生成新文章，Claude 不补充 picks、不生成或反哺文章。

<!-- 格式：- [ ] 原始推送日期 | note 路径；确认后追加：| acknowledged YYYY-MM-DD -->

## 历史存量（按原始日期从旧到新）

- [ ] 2026-08-01 | wiki/notes/2026-08-01-llm-as-judge-systematic-bias.md
- [ ] 2026-08-02 | wiki/notes/2026-08-02-token-credit-assignment.md
- [ ] 2026-08-03 | wiki/notes/2026-08-03-doremi-data-mixture-objective.md
- [ ] 2026-08-04 | wiki/notes/2026-08-04-tau-bench-pass-k-agent-reliability.md
- [ ] 2026-08-05 | wiki/notes/2026-08-05-rag-evaluation-causal-decomposition.md
- [ ] 2026-08-06 | wiki/notes/2026-08-06-hybrid-retrieval-score-fusion.md
- [ ] 2026-08-07 | wiki/notes/2026-08-07-cross-encoder-reranking-recall-ceiling.md
- [ ] 2026-08-08 | wiki/notes/2026-08-08-counterfactual-offline-evaluation-ips.md
- [ ] 2026-08-09 | wiki/notes/2026-08-09-prefix-caching-shared-context.md
- [ ] 2026-08-10 | wiki/notes/2026-08-10-chunked-prefill-scheduling.md
- [ ] 2026-08-11 | wiki/notes/2026-08-11-hard-negatives-false-negatives.md
- [ ] 2026-08-12 | wiki/notes/2026-08-12-importance-sampling-hidden-objective.md
- [ ] 2026-08-13 | wiki/notes/2026-08-13-kl-regularization-trust-region.md
- [ ] 2026-08-14 | wiki/notes/2026-08-14-teacher-forcing-exposure-bias.md
- [ ] 2026-08-15 | wiki/notes/2026-08-15-scheduled-sampling-dagger-distribution-shift.md
- [ ] 2026-08-16 | wiki/notes/2026-08-16-dagger-to-rl-on-policy.md
- [ ] 2026-08-17 | wiki/notes/2026-08-17-ppo-clipping-stale-policy-data.md
- [ ] 2026-08-18 | wiki/notes/2026-08-18-gae-advantage-bias-variance.md
- [ ] 2026-08-19 | wiki/notes/2026-08-19-grpo-group-relative-baseline.md
- [ ] 2026-08-21 | wiki/notes/2026-08-21-grpo-length-bias-token-policy-gradient.md
