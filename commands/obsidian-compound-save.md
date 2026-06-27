---
description: Save a memory into the Compound Vault log and refresh hot cache.
category: vault
triggers_en: ["compound save", "save to compound vault", "log this memory", "save memory to hot cache"]
argument-hint: "<memory/update>"
allowed-tools: Bash, Read, Edit
---

# /obsidian-compound-save

Save a concise memory/update to the Compound Vault log, then refresh `wiki/hot.md`.

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
python3 "$SCRIPT" log "compound-save" "$ARGUMENTS" --refresh-hot
```

If the update belongs in a durable note, write the smallest patch to the relevant project/entity/concept/decision note. Use wikilinks and add source context when available.

When editing existing files, use `scripts/wiki-lock.sh run <target-file> -- <write-command>` or manually follow `references/locking-protocol.md`.
