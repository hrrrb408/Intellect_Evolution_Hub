---
description: Plan or apply IEH/SINGULARITY stage-model source fusion.
category: meta
triggers_en: ["fusion proposals", "source fusion", "stage model fusion", "create concept query moc"]
argument-hint: "[source-note-path] [--apply]"
allowed-tools: Bash, Read
---

# /obsidian-fusion

Create a reviewable fusion plan for a raw source note.

Default mode is a dry-run. It writes:

- `wiki/meta/fusion-proposals-latest.json`
- `wiki/meta/fusion-proposals-latest.md`

With `--apply`, it only creates missing stage-model scaffolds and appends MOC
links. It does not overwrite existing durable notes.

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
- With `--apply`, existing notes are never overwritten.
- The command may create missing `concepts/`, `entities/`, `queries/`, and
  `mocs/` scaffolds, then refresh generated index/hot/chunks.
