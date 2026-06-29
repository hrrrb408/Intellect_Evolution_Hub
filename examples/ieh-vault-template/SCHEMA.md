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

- `raw/`: original source files plus compact source notes. PDF full text is not duplicated into markdown.
- `source-summaries/`: Chinese-first bilingual one-source reading notes.
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
IEH does not use `wiki/entities/`, `wiki/concepts`, or `wiki/resources/` as
knowledge folders. Those are legacy/generic compatibility paths only.

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
- Put compact source notes under `raw/articles/<domain>/<subdomain>/`.
  For PDFs, do not duplicate the full extracted text into git-tracked markdown.
- Put local Markdown/course-note images under the matching article folder,
  for example `raw/articles/engineering/algorithms/assets/figures/...`, and
  rewrite the note to reference `assets/figures/...`.
- Use `raw/assets/` only for standalone screenshots, web captures, and loose
  uploaded images that do not belong to one source note.
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
- User-facing durable notes must be Chinese-first bilingual. This applies to
  `index.md`, `log.md`, `source-summaries/`, `concepts/`, `entities/`,
  `comparisons/`, `queries/`, and `mocs/`.
- Use `中文 / English` for titles and section headings whenever English is
  present.
- English terms should have Chinese counterparts, usually
  `中文（English）`; full English sentences need a nearby Chinese explanation.
- Processed notes should explain in Chinese, while preserving important English
  method names, metrics, datasets, and source excerpts.
- Processed notes should teach, not only summarize.
- Do not invent missing source details.
- Runtime files under `wiki/`, `.vault-meta/`, `.codex/`, and `.agents/` may
  remain machine-friendly and are not the user's main reading surface.

## Query page standard

A useful query page includes:

- short answer or learning judgment;
- learning order;
- concepts and sources to connect;
- common confusions;
- self-check questions;
- mastery criteria;
- related pages and remaining gaps.
