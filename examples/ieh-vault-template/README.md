---
title: IEH Vault Template
type: maintenance
ai-first: true
sources: []
---

# IEH Vault Template

## For future Claude
This directory is a clean, distributable Intellect Evolution Hub vault template.
It mirrors the compound/stage-model vault structure used by this project, but it
does not include private sources, personal notes, generated runtime caches, or
machine-specific paths.

## How to instantiate

From the `obsidian-second-brain` repository root:

```bash
cp -R examples/ieh-vault-template /path/to/NewVault
python3 scripts/compound_vault.py --vault /path/to/NewVault init
python3 scripts/install_desktop.py /path/to/NewVault --json
python3 scripts/compound_vault.py --vault /path/to/NewVault health --json
```

Then open `/path/to/NewVault` in Obsidian.

## What is included

- Stage-model directories: `raw/`, `source-summaries/`, `concepts/`,
  `entities/`, `comparisons/`, `queries/`, `mocs/`, `maintenance/`.
- Runtime directories: `wiki/`, `wiki/meta/`, `.vault-meta/`.
- Obsidian starter config under `.obsidian/`.
- Routing defaults under `.vault-meta/singularity-routes.json`.
- Runtime manuals: `_CLAUDE.md`, `AGENTS.md`, `CODEX-DESKTOP.md`,
  `CLAUDE-DESKTOP.md`, `HERMES.md`, `DESKTOP-ADAPTERS.md`.

## What is not included

- Private notes.
- Ingested source files.
- PDF binaries.
- Generated chunk indexes.
- Codex Desktop installed `.codex/` and `.agents/` directories.
- Local `.git/` history.
- Obsidian workspace state.

## IEH conventions

- PDF originals live in `raw/papers/`; `raw/articles/` keeps compact source
  notes only, not full duplicated PDF text.
- Generated reading scaffolds are Chinese-first bilingual. Keep English method
  names, metrics, datasets, and source excerpts when they matter.
- `wiki/` is runtime space only: `hot.md`, `index.md`, `log.md`, and `meta/`.
  Do not put durable knowledge into legacy `wiki/entities` or `wiki/concepts`
  paths.

## First ingest

Use the manifest-aware ingest path:

```bash
python3 scripts/compound_vault.py --vault /path/to/NewVault ingest /path/to/source.pdf
```

After ingest:

```bash
python3 scripts/compound_vault.py --vault /path/to/NewVault query "What did this source add?" --refresh
python3 scripts/compound_vault.py --vault /path/to/NewVault health --json
```
