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
```

The session-end hook is disabled by default. Do not set
`OBSIDIAN_HERMES_HOOK_ENABLED` or register `on_session_end` unless the user
explicitly chooses to re-enable per-session consolidation. The scheduled
morning, nightly, weekly, and health-check jobs are the default maintenance
mechanism.

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

## Browser-only URL ingest

WeChat Official Account pages commonly return a verification page to direct
HTTP clients. When the browser can read the article, save the complete visible
body to a temporary UTF-8 Markdown file and run:

```bash
python3 "$HOME/.hermes/skills/obsidian-second-brain/scripts/compound_vault.py" \
  --vault "$OBSIDIAN_VAULT_PATH" ingest "$URL" \
  --body-file "/tmp/wechat-article.md" --force
```

Never manually overwrite an existing raw note after ingest. The `--body-file`
entrypoint keeps the body hash, route, source-summary, claims, rewrite plan, and
manifest synchronized. If the raw note contains a verification page, stop and
leave it as `fetch_status: blocked` until real article text is available.
