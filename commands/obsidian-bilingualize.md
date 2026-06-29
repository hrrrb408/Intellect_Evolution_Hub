---
description: Audit or normalize IEH user-facing notes into Chinese-first bilingual style.
category: maintenance
triggers_en: ["bilingualize IEH", "normalize bilingual vault", "check bilingual style"]
argument-hint: "[--apply]"
allowed-tools: Bash, Read
---

# /obsidian-bilingualize

Audit or normalize IEH user-facing durable notes.

User-facing paths:

- `index.md`
- `log.md`
- `source-summaries/`
- `concepts/`
- `entities/`
- `comparisons/`
- `queries/`
- `mocs/`

Required style:

- Headings use `中文 / English`.
- Technical terms use `中文（English）`.
- Full English sentences need a nearby Chinese explanation.
- Never use placeholder text such as `中文对应`, `待补译`, or `以下英文保留为原始表述` as a substitute for a real Chinese translation.
- Runtime files under `wiki/`, `.vault-meta/`, `.codex/`, and `.agents/` are not the user's main reading surface and may remain machine-friendly.

Default mode is dry-run. Use `--apply` only after reviewing the reported files.

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
python3 "$SCRIPT" bilingualize $ARGUMENTS
```
