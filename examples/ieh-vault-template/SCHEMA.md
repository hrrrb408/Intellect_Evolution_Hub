---
title: IEH Schema
type: maintenance
ai-first: true
sources: []
---

# IEH Schema

## For future Claude
This vault uses the Intellect Evolution Hub stage model plus the
obsidian-second-brain compound runtime. Keep knowledge files and runtime files
separate.

## Core model

The durable knowledge flow is:

```text
raw/ -> source-summaries/ -> concepts|entities|comparisons -> queries/ -> mocs/
```

## Knowledge layer

- `raw/`: original source files or near-original extractions.
- `source-summaries/`: one-source reading notes.
- `concepts/`: reusable ideas, methods, mechanisms, definitions.
- `entities/`: people, labs, organizations, tools, papers, projects, datasets.
- `comparisons/`: method and framework comparison pages.
- `queries/`: learning questions, research questions, and decision questions.
- `mocs/`: maps of content for active domains and subdomains.
- `maintenance/`: vault-wide workflows and operating rules.
- `index.md`: short human-written front door.
- `log.md`: human-readable operation log.

## Runtime layer

- `wiki/hot.md`: recent working set.
- `wiki/index.md`: generated vault map.
- `wiki/log.md`: compound runtime log.
- `wiki/meta/`: generated reports, query results, drafts, proposals.
- `.vault-meta/`: manifest, routing, mode, chunks, BM25 index.
- `.agents/`: Codex Desktop skill install output.
- `.codex/`: Codex Desktop scripts and references.
- `AGENTS.md`: Codex and agent routing.
- `DESKTOP-ADAPTERS.md`: desktop handoff guide.

Do not treat generated runtime reports as final durable knowledge.

## Domain taxonomy

Domains express primary use case:

- `engineering`: software, systems, AI engineering, tooling.
- `science`: basic science and mechanism research.
- `business`: products, strategy, marketing, organizations.
- `finance`: investing, markets, macro, accounting, quant.
- `medicine`: clinical medicine, pharmacology, public health.
- `society`: law, policy, education, history, institutions.
- `life`: career, productivity, personal health, relationships, decisions.
- `exam-prep`: exams, interviews, certificates, course review.

## Routing rules

- Preserve source material first.
- Put original PDFs under `raw/papers/<domain>/<subdomain>/`.
- Put text extraction or near-original markdown under
  `raw/articles/<domain>/<subdomain>/`.
- Put single-source summaries under
  `source-summaries/<domain>/<subdomain>/`.
- Put reusable synthesis under `concepts/`, `entities/`, `comparisons/`,
  `queries/`, or `mocs/`.
- Update the relevant MOC whenever durable processed pages are added.

## Writing rules

- Every durable Markdown note needs frontmatter.
- Every durable note needs `ai-first: true`.
- Every durable note needs a `## For future Claude` section.
- Filenames use stable English kebab-case slugs.
- Raw material may keep original language.
- Processed notes should teach, not only summarize.
- Do not invent missing source details.

## Query page standard

A useful query page includes:

- short answer or learning judgment;
- learning order;
- concepts and sources to connect;
- common confusions;
- self-check questions;
- mastery criteria;
- related pages and remaining gaps.
