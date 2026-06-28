---
title: IEH Agent Guide
type: maintenance
ai-first: true
sources: []
---

# IEH Agent Guide

## For future Claude
This file is a generic agent handoff for a clean IEH vault template. After
running `scripts/install_desktop.py`, the generated `AGENTS.md` may replace or
extend this file with platform-specific instructions.

## Required behavior

- Read `CRITICAL_FACTS.md`, `SOUL.md`, `_CLAUDE.md`, and `SCHEMA.md`.
- Preserve raw sources.
- Use manifest-aware ingest before manual synthesis.
- Write durable notes into the stage model.
- Use query retrieval before answering substantive vault questions.
- Run health after meaningful writes.

## Preferred commands

From the vault root after desktop install:

```bash
python3 .codex/scripts/compound_vault.py --vault . ingest /path/to/source.pdf
python3 .codex/scripts/compound_vault.py --vault . query "<question>" --refresh --top-k 8 --rerank auto
python3 .codex/scripts/compound_vault.py --vault . health --json
```

From the repository root:

```bash
python3 scripts/compound_vault.py --vault /path/to/vault ingest /path/to/source.pdf
python3 scripts/compound_vault.py --vault /path/to/vault query "<question>" --refresh --top-k 8 --rerank auto
python3 scripts/compound_vault.py --vault /path/to/vault health --json
```
