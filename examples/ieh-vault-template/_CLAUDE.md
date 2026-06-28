---
title: IEH Runtime Manual
type: maintenance
ai-first: true
sources: []
---

# IEH Runtime Manual

## For future Claude
Read this file first when any Claude-family, Codex, Hermes, or Desktop runtime
opens this vault. Operate conservatively: preserve sources, write AI-first notes,
prefer reviewable proposals, and keep the stage model clean.

## Vault identity

- Vault name: Intellect Evolution Hub (IEH).
- Vault path: set by the user.
- Project repository: `obsidian-second-brain`.
- Remote repository: set by the user.
- This template is the starting structure. User-specific content arrives through
  manifest-aware ingest.

## Startup order

1. Read `CRITICAL_FACTS.md`.
2. Read `SOUL.md`.
3. Read this file.
4. Read `SCHEMA.md`.
5. Read `index.md`.
6. Read `wiki/hot.md`.
7. If needed, read `wiki/index.md`.
8. If still insufficient, run `compound_vault.py query`.

## Durable stage model

```text
raw/ -> source-summaries/ -> concepts|entities|comparisons -> queries/ -> mocs/
```

Use:

- `raw/` for original material plus compact source notes. For PDFs, keep the
  original under `raw/papers/` and do not duplicate full extracted text into
  markdown.
- `source-summaries/` for Chinese-first bilingual one-source reading scaffolds.
- `concepts/` for reusable ideas, methods, mechanisms, definitions.
- `entities/` for people, labs, tools, papers, projects, datasets.
- `comparisons/` for method and concept comparisons.
- `queries/` for learning questions and research-direction maps.
- `mocs/` for navigational maps.
- `maintenance/` for vault-wide rules and workflows.

## Runtime layer

Runtime files are generated or tool-facing:

- `wiki/hot.md`
- `wiki/index.md`
- `wiki/log.md`
- `wiki/meta/`
- `.vault-meta/`
- `.agents/`
- `.codex/`
- `AGENTS.md`
- `DESKTOP-ADAPTERS.md`

Use runtime files for retrieval and operation. Do not cite generated reports as
durable sources when a raw source exists.
IEH does not use legacy `wiki/entities`, `wiki/concepts`, or `wiki/resources`
as durable knowledge folders.

## Writing rules

- Every durable Markdown note needs frontmatter.
- Every durable note needs `ai-first: true`.
- Every durable note needs a `## For future Claude` section near the top.
- Filenames should use stable English kebab-case slugs.
- Never invent missing source details.
- Never pretend a PDF was read if extraction failed.
- Never turn a single source claim into domain consensus without saying it is
  single-source and low confidence.

## Query behavior

When answering:

1. Use `wiki/hot.md` first.
2. Use `wiki/index.md` second.
3. Use query retrieval for substantive questions.
4. Open the best source-summary, concept, query, or entity pages.
5. Answer with current confidence level.
6. If coverage is weak, propose or create a query page rather than overclaiming.

Useful command from the vault root after desktop install:

```bash
python3 .codex/scripts/compound_vault.py --vault . query "<question>" --refresh --top-k 8 --rerank auto
```

Useful command from the repository root:

```bash
python3 scripts/compound_vault.py --vault /path/to/vault query "<question>" --refresh --top-k 8 --rerank auto
```

## Ingest rule

For PDFs and attached source files, call manifest-aware ingest before manually
writing stage-model notes:

```bash
python3 scripts/compound_vault.py --vault /path/to/vault ingest /path/to/source.pdf
```

If a runtime already created stage files without manifest provenance, run:

```bash
python3 scripts/compound_vault.py --vault /path/to/vault manifest-repair --json
```
