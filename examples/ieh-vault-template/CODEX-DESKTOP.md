---
title: Codex Desktop Runtime Manual
type: maintenance
ai-first: true
sources: []
---

# Codex Desktop Runtime Manual

## For future Claude
Codex Desktop should treat this vault as the source of truth and use the
compound vault runtime for ingest, retrieval, health, and repair.

## Install adapter files

From the repository root:

```bash
python3 scripts/install_desktop.py /path/to/vault --json
python3 scripts/install_desktop.py /path/to/vault --check --json
```

This installs:

- `AGENTS.md`
- `.agents/skills/`
- `.codex/scripts/compound_vault.py`
- `.codex/references/`
- `DESKTOP-ADAPTERS.md`

## Startup order

1. Read `CRITICAL_FACTS.md`.
2. Read `SOUL.md`.
3. Read `_CLAUDE.md`.
4. Read `AGENTS.md`.
5. Read `SCHEMA.md`.
6. Read `wiki/hot.md`.

## Ingest rule

For PDFs and attached source files, Codex Desktop must call the manifest-aware
`ingest` command before manually writing durable stage-model notes.

```bash
python3 .codex/scripts/compound_vault.py --vault . ingest /path/to/source.pdf
```

Manual stage-model synthesis is allowed only after ingest.

## Write policy

- Preserve raw sources.
- Keep processed pages in the IEH stage model.
- Do not overwrite human-written durable notes.
- Use proposals and drafts before applying structural changes.
- Refresh index and chunks after writes.
- Run health before reporting a workflow complete.
