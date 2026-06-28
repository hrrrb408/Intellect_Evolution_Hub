---
description: Bootstrap an IEH vault with the project template, runtime manuals, index, hot cache, and operation log
category: meta
triggers_en: ["init vault", "bootstrap vault", "setup vault", "scan vault", "initialize IEH"]
argument-hint: "[vault path]"
allowed-tools: Bash, Read
---

# /obsidian-init

Initialize a vault as an IEH knowledge base. This command must not fall back to
the upstream obsidian-second-brain default PARA/template layout unless the user
explicitly asks for legacy compatibility.

## Procedure

1. Resolve the vault path from `$ARGUMENTS`, `$OBSIDIAN_VAULT_PATH`, or the current working directory.
2. Run the IEH Compound Vault initializer:

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
  python3 "$SCRIPT" --vault "$ARGUMENTS" init --template ieh
else
  python3 "$SCRIPT" init --template ieh
fi
```

3. Confirm these files/directories exist:
   - `.vault-meta/ieh-template.json`
   - `.vault-meta/mode.json` with `mode: singularity`
   - `raw/articles/engineering/ai-engineering/`
   - `raw/papers/engineering/ai-engineering/`
   - `source-summaries/engineering/ai-engineering/`
   - `concepts/engineering/ai-engineering/`
   - `entities/engineering/ai-engineering/`
   - `queries/engineering/ai-engineering/`
   - `mocs/engineering/ai-engineering/`
   - `wiki/hot.md`, `wiki/index.md`, `wiki/log.md`
4. If runtime manuals are missing, create IEH-style `_CLAUDE.md`, `CODEX-DESKTOP.md`, `CLAUDE-DESKTOP.md`, `HERMES.md`, and `AGENTS.md` from the repo template or the installed desktop adapter.
5. Run `python3 "$SCRIPT" health --json` and read `wiki/meta/lint-report-latest.md`.
6. If this is a new vault and no `.git/` directory exists, tell the user to create a baseline commit before ingesting large batches.

## Rules

- IEH is the product template; obsidian-second-brain is the engine/runtime.
- Do not initialize new IEH vaults with the legacy upstream template.
- Do not overwrite existing personal manuals without showing the diff or asking the user.
- Every PDF or attachment ingest after initialization must go through `/obsidian-compound-ingest`.
- A healthy new IEH vault should have no flat processed pages under `concepts/*.md`, `entities/*.md`, `queries/*.md`, `mocs/*.md`, or `comparisons/*.md`; processed pages belong under `{domain}/{subdomain}/`.
