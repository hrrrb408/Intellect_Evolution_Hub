---
description: Refresh the Compound Vault hot cache at wiki/hot.md.
category: vault
triggers_en: ["refresh hot cache", "update hot cache", "obsidian hot", "compound hot"]
argument-hint: "[limit]"
allowed-tools: Bash, Read
---

# /obsidian-hot

Refresh `wiki/hot.md`, the small recent working set that should be loaded before broad retrieval.

## Procedure

Use `$OBSIDIAN_VAULT_PATH` or the current working directory as the vault.

```bash
LIMIT="${ARGUMENTS:-20}"
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
python3 "$SCRIPT" hot --limit "$LIMIT"
```

After refreshing, read `wiki/hot.md` and summarize the current working set briefly.
