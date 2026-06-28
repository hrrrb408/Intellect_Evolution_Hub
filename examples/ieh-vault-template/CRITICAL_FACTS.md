---
title: IEH Critical Facts
type: identity
ai-first: true
sources: []
---

# IEH Critical Facts

## For future Claude
Read this file first for compact orientation. It is intentionally short and
high priority.

## Facts

- This vault is an Intellect Evolution Hub template instance.
- The user must set the real vault path.
- The durable stage model is:
  `raw/ -> source-summaries/ -> concepts|entities|comparisons -> queries/ -> mocs/`.
- Runtime retrieval order is:
  `wiki/hot.md -> wiki/index.md -> BM25 chunks/query -> durable notes`.
- Processed pages should be written for future learning and retrieval.
- Do not overwrite human-written durable notes.
- Do not auto-resolve contradictions.
- Run health after meaningful ingest or structural changes.

## Fast commands

From the vault root after desktop install:

```bash
python3 .codex/scripts/compound_vault.py --vault . query "<question>" --refresh --top-k 8 --rerank auto
python3 .codex/scripts/compound_vault.py --vault . health --json
```

From the repo root:

```bash
python3 scripts/compound_vault.py --vault /path/to/vault query "<question>" --refresh --top-k 8 --rerank auto
python3 scripts/compound_vault.py --vault /path/to/vault health --json
```
