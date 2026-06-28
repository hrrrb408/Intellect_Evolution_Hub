---
description: Repair Compound Vault manifest provenance for existing IEH/SINGULARITY stage-model sources.
category: meta
triggers_en: ["repair manifest", "manifest repair", "fix source provenance", "repair compound manifest"]
argument-hint: "[--apply] [--repair-distributed] [--json]"
allowed-tools: Bash, Read
---

# /obsidian-manifest-repair

Repair `.vault-meta/compound-manifest.json` when raw/source-summary stage files
already exist but were created outside the manifest-aware ingest entrypoint.

Default mode is a dry-run. It reports stage sources under:

- `raw/papers/`
- `raw/articles/`
- `source-summaries/`

that are not represented in the Compound Vault manifest.

It can also backfill `distributed.entities` and `distributed.concepts` from
existing processed IEH pages when those pages were created by a runtime but the
manifest was not updated.

Use `--apply` only after reviewing the proposed repairs.

## Procedure

```bash
SCRIPT=""
for candidate in \
  scripts/compound_vault.py \
  .codex/scripts/compound_vault.py \
  .gemini/scripts/compound_vault.py \
  .opencode/scripts/compound_vault.py \
  "$HOME/.claude/skills/obsidian-second-brain/scripts/compound_vault.py"; do
  if [ -f "$candidate" ]; then
    SCRIPT="$candidate"
    break
  fi
done
if [ -z "$SCRIPT" ]; then
  echo "compound_vault.py not found. Run from the skill checkout or install a built platform dist into the vault." >&2
  exit 2
fi
python3 "$SCRIPT" manifest-repair $ARGUMENTS
```

## Safety rules

- Without `--apply`, no manifest changes are written.
- With `--apply`, the command only adds missing manifest entries.
- With `--repair-distributed --apply`, the command also adds reverse links from
  already-existing processed pages into the matching manifest source entries.
- It never deletes existing manifest entries.
- It never rewrites raw sources or durable notes.
- After repair, run health and confirm `Manifest untracked stage sources: 0`
  and `Manifest missing distributed links: 0`.

## When to use

Run this after an AI runtime manually creates IEH stage-model files from a
source without first calling `/obsidian-compound-ingest`.

The normal ingest path remains:

```bash
python3 "$SCRIPT" ingest "/path/to/source.pdf"
python3 "$SCRIPT" fusion "<raw-source-note>" --apply
python3 "$SCRIPT" health --json
```
