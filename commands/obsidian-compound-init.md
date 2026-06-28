---
description: Initialize an IEH Compound Vault: stage-model folders, wiki/hot.md, wiki/index.md, wiki/log.md, routes, manifest metadata, and health-ready scaffold.
category: meta
triggers_en: ["initialize compound vault", "setup compound vault", "create hot index log", "obsidian compound init"]
argument-hint: "[vault path]"
allowed-tools: Bash, Read
---

# /obsidian-compound-init

Initialize the IEH Compound Vault layer on top of obsidian-second-brain.

This does not delete or rewrite existing notes. It creates missing IEH stage-model files and directories, marks the vault with `.vault-meta/ieh-template.json`, and defaults the vault to `singularity` mode when no mode has been configured.

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

Then read `wiki/index.md`, `wiki/hot.md`, and `.vault-meta/ieh-template.json` to confirm the IEH scaffold exists.

## Rules

- New IEH vaults MUST use the default `init` behavior, which is `--template ieh`.
- Use `--template generic` only for legacy obsidian-second-brain compatibility checks.
- Any runtime that initializes a user vault must create or preserve `.vault-meta/ieh-template.json`.
