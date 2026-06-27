---
description: Rebuild the Compound Vault chunk store and BM25 index under .vault-meta for chunk-level retrieval.
category: meta
triggers_en: ["rebuild chunk index", "build bm25 index", "compound chunks", "refresh retrieval index"]
argument-hint: "[--json]"
allowed-tools: Bash, Read
---

# /obsidian-compound-chunks

Rebuild the deterministic retrieval substrate used by `/obsidian-query`.

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
python3 "$SCRIPT" chunks $ARGUMENTS
```

Then read `.vault-meta/bm25/index.json` stats if needed and report the chunk
count. This command is deterministic and does not edit durable notes.
