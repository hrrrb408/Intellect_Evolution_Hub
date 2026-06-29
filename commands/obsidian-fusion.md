---
description: Plan or apply IEH/SINGULARITY stage-model source fusion.
category: meta
triggers_en: ["fusion proposals", "source fusion", "stage model fusion", "create concept query moc"]
argument-hint: "[source-note-path] [--apply] [--upgrade-scaffolds]"
allowed-tools: Bash, Read
---

# /obsidian-fusion

Create a reviewable fusion plan for a raw source note.

Default mode is a dry-run. It writes:

- `wiki/meta/fusion-proposals-latest.json`
- `wiki/meta/fusion-proposals-latest.md`
- `wiki/meta/fusion-drafts-latest.json`
- `wiki/meta/fusion-drafts-latest.md`

With `--apply`, it creates missing stage-model pages from reviewable Chinese-first
drafts and appends MOC links. It does not overwrite existing durable notes.

With `--apply --upgrade-scaffolds`, it may replace existing low-confidence fusion
scaffolds. Human-written notes are still preserved.

## IEH bilingual rule

For IEH/SINGULARITY stage-model vaults, created or upgraded user-facing pages
must be Chinese-first bilingual. This applies to `source-summaries/`,
`concepts/`, `entities/`, `comparisons/`, `queries/`, and `mocs/`.

- Headings use `中文 / English`.
- Technical terms use `中文（English）`.
- Full English sentences need a nearby Chinese explanation.
- Runtime reports under `wiki/meta/` may remain machine-friendly.

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
python3 "$SCRIPT" fusion $ARGUMENTS
```

## Safety rules

- Without `--apply`, no durable stage pages are modified.
- With `--apply`, missing `source-summaries/`, `concepts/`, `entities/`,
  `queries/`, and `mocs/` pages are created from reviewable drafts.
- Existing notes are never overwritten unless they are detected as old fusion
  scaffolds and `--upgrade-scaffolds` is explicitly set.
- The command refreshes generated index/hot/chunks after writing durable pages.
