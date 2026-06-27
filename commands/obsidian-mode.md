---
description: Get, set, or preview Compound Vault methodology routing: generic, LYT, PARA, or Zettelkasten.
category: meta
triggers_en: ["set vault mode", "get vault mode", "route note by mode", "methodology mode"]
argument-hint: "get | set <mode> | route <type> <name>"
allowed-tools: Bash, Read
---

# /obsidian-mode

Manage the Compound Vault methodology mode. Modes affect where new source,
entity, concept, project, decision, question, session, and research notes are
filed.

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
python3 "$SCRIPT" mode $ARGUMENTS
```

## Examples

```bash
python3 "$SCRIPT" mode get
python3 "$SCRIPT" mode set para
python3 "$SCRIPT" mode route source "Karpathy LLM Wiki"
```

Do not migrate existing files automatically when changing modes. The mode only
controls future routing.
