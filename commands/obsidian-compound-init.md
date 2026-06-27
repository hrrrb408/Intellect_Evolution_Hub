---
description: Initialize Compound Vault files: wiki/hot.md, wiki/index.md, wiki/log.md, sources, entities, concepts, projects, decisions, questions, and meta.
category: meta
triggers_en: ["initialize compound vault", "setup compound vault", "create hot index log", "obsidian compound init"]
argument-hint: "[vault path]"
allowed-tools: Bash, Read
---

# /obsidian-compound-init

Initialize the Compound Vault layer on top of obsidian-second-brain.

This does not delete or rewrite existing notes. It creates missing files and directories under `wiki/`.

## Procedure

If the user passes a path, use it as the vault path. Otherwise use `$OBSIDIAN_VAULT_PATH` or current working directory.

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

if [ -n "$ARGUMENTS" ]; then
  python3 "$SCRIPT" --vault "$ARGUMENTS" init
else
  python3 "$SCRIPT" init
fi
```

Then read `wiki/index.md` and `wiki/hot.md` to confirm the scaffold exists.
