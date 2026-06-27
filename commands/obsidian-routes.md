---
description: List, test, or add IEH/SINGULARITY domain routing rules.
category: meta
triggers_en: ["route rules", "singularity routes", "domain routing", "test vault route"]
argument-hint: "list | test <title> [--text ...] | add <domain> <subdomain> <keywords>"
allowed-tools: Bash, Read
---

# /obsidian-routes

Manage `.vault-meta/singularity-routes.json`, the configurable domain/subdomain
router used by `singularity` mode ingest.

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
python3 "$SCRIPT" routes $ARGUMENTS
```

## Examples

```bash
python3 "$SCRIPT" routes list
python3 "$SCRIPT" routes test "A paper about market volatility" --text "asset allocation portfolio risk"
python3 "$SCRIPT" routes add science neuroscience "neuroscience,brain,cortex,attention"
```
