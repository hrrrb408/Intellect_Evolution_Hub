---
description: Run IEH/Compound Vault health checks: links, frontmatter, manifest, duplicate raw PDFs, stage-model layout, audit artifacts, template marker, and git baseline.
category: meta
triggers_en: ["compound health", "check compound vault", "compound vault health", "lint compound vault"]
argument-hint: "[--fix-index]"
allowed-tools: Bash, Read
---

# /obsidian-compound-health

Run the Compound Vault lint/health check and write:

- `wiki/meta/lint-report-YYYY-MM-DD.md`
- `wiki/meta/lint-report-latest.md`

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
python3 "$SCRIPT" health $ARGUMENTS
```

Then read `wiki/meta/lint-report-latest.md` and summarize the action items.

## Rules

- Default behavior is report-only.
- Only rebuild generated `hot.md`/`index.md` when the user asks for `--fix-index`.
- Never auto-delete notes.
- Current checks include dead links, orphan pages, missing frontmatter,
  missing `ai-first: true`, duplicate titles, manifest pointers, stale generated
  files, index gaps, duplicate raw PDFs by content hash, flat processed
  stage-model pages, missing manifest distributed links, missing latest audit
  artifacts, IEH template marker, and git baseline status.
