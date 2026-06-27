---
description: Prepare the shared Obsidian vault protocol for Codex Desktop and Claude Desktop.
category: meta
triggers_en: ["desktop setup", "codex desktop setup", "claude desktop setup", "desktop adapter"]
argument-hint: "[vault path]"
allowed-tools: Bash, Read
---

# /obsidian-desktop-setup

Use this when the user wants the same Obsidian second brain to work from Codex
Desktop, Claude Desktop, Claude Code, and other CLI agents.

## Procedure

1. Read `references/desktop-adapters.md`.
2. Confirm the target vault path. If the user passes an argument, use it. If not,
   use `$OBSIDIAN_VAULT_PATH` or ask for the vault path.
3. For Codex Desktop, ensure the Codex platform build has been copied into the
   vault root:

   ```bash
   bash scripts/build.sh --platform codex-cli
   cp -R dist/codex-cli/. "<vault-path>/"
   ```

4. For Claude Desktop, do not install Claude Code slash commands. Configure MCP
   or project instructions so Claude Desktop can read and write the vault files.
5. Run or ask the user to run `/obsidian-compound-init` once for the vault.
6. Verify the shared files exist:
   - `AGENTS.md`
   - `_CLAUDE.md` when the vault uses one
   - `.agents/skills/`
   - `.codex/scripts/compound_vault.py`
   - `wiki/hot.md`
   - `wiki/index.md`
   - `wiki/log.md`

## Desktop rules

- Desktop apps are clients of the vault protocol, not separate forks.
- Use `wiki/hot.md` before broad search.
- Use `wiki/index.md` before opening many notes.
- Use `compound_vault.py query` for candidate retrieval when shell access exists.
- Follow `references/ai-first-rules.md` for every durable note.
- Never assume Claude Desktop can run Claude Code slash commands or hooks.
