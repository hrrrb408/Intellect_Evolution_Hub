---
description: Dry-run or safely apply generated Compound Vault patch proposals.
category: meta
triggers_en: ["apply patch proposals", "apply obsidian proposals", "compound apply proposals", "apply rewrite proposals"]
argument-hint: "[--apply] [--proposal-file wiki/meta/patch-proposals-latest.json]"
allowed-tools: Bash, Read
---

# /obsidian-apply-proposals

Safely process `wiki/meta/patch-proposals-latest.json`.

Default mode is a dry-run. It reports what would be appended and writes
`wiki/meta/apply-proposals-latest.md/json`.

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
python3 "$SCRIPT" apply-proposals $ARGUMENTS
```

## Safety rules

- Without `--apply`, do not modify durable notes.
- With `--apply`, only `append_evidence` and `append_timeline` proposals are written.
- `review_contradiction` proposals are never auto-applied; read the source,
  target note, and contradiction report, then decide manually.
- Unsafe targets such as `wiki/sources/`, `wiki/meta/`, `.vault-meta/`, or paths
  outside the vault are skipped.
- After a real apply, the runtime refreshes `wiki/index.md`, `wiki/hot.md`, and
  `.vault-meta/bm25/index.json`.
