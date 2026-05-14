# Wiki Schema

## Domain
AI/ML 知识库：涵盖大语言模型（LLM）、Agent、深度学习（Deep Learning）、RAG、AI 工程化及相关技术领域的研究笔记、概念整理和实体追踪。

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`)
- Every wiki page starts with YAML frontmatter (see below)
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** On pages that synthesize 3+ sources, append `[[raw/articles/source-file.md]]`
  at the end of paragraphs whose claims come from a specific source.
- 语言：正文使用中文，技术术语保留英文原文

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
# Optional quality signals:
confidence: high | medium | low
contested: true
contradictions: [other-page-slug]
---
```

### raw/ Frontmatter
```yaml
---
source_url: https://example.com/article
ingested: YYYY-MM-DD
sha256: <hex digest of the raw content below the frontmatter>
---
```

## Tag Taxonomy
- Models: model, architecture, benchmark, training, fine-tuning, quantization
- People/Orgs: person, company, lab, open-source, ecosystem
- Techniques: optimization, inference, alignment, data, embedding, retrieval, reasoning, agentic
- Domains: llm, agent, deeplearning, rag, nlp, cv, multimodal, reinforcement-learning
- Meta: comparison, timeline, controversy, prediction, tutorial, survey, paper-review
- Tools: framework, library, platform, infra

Rule: every tag on a page must appear in this taxonomy. If a new tag is needed, add it here first, then use it.

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines — break into sub-topics with cross-links
- **Archive a page** when its content is fully superseded — move to `_archive/`, remove from index
