---
title: Hermes Runtime Manual
type: maintenance
ai-first: true
sources: []
---

# Hermes Runtime Manual

## For future Claude
Hermes should operate this vault through the same vault protocol as Codex and
Claude. Runtime activation must be verified before trusting unattended
automation.

## Build artifacts

From the repository root:

```bash
bash scripts/build.sh --platform hermes
```

The build emits:

```text
dist/hermes/skills/
dist/hermes/optional-skills/
dist/hermes/hooks/
dist/hermes/HOOKS.md
dist/hermes/INSTALL.md
```

## Required environment

```bash
export OBSIDIAN_VAULT_PATH="/path/to/vault"
export OBSIDIAN_HERMES_HOOK_ENABLED=1
```

Only set hook variables after reviewing and installing the hook.

## Scheduled skills

Optional Hermes skills are opt-in:

- `obsidian-morning`
- `obsidian-nightly`
- `obsidian-weekly`
- `obsidian-health-check`

Do not install unattended writers without user approval.

## Safety rules

- Add, update, and link only.
- Never delete or archive automatically.
- Never silently resolve contradictions.
- Keep generated maintenance reports separate from durable knowledge.
