---
title: Desktop Adapters
type: maintenance
ai-first: true
sources: []
---

# Desktop Adapters

## For future Claude
This template can be used by multiple desktop and CLI agents. The vault protocol
is the stable layer. Adapter files are generated from the repository.

## Codex Desktop

Install:

```bash
python3 scripts/install_desktop.py /path/to/vault --json
```

Check:

```bash
python3 scripts/install_desktop.py /path/to/vault --check --json
```

Rollback:

```bash
python3 scripts/install_desktop.py /path/to/vault --rollback --json
```

## Claude Desktop

Claude Desktop should use MCP, filesystem access, or project instructions to
read this vault. It does not automatically load Claude Code slash commands.

## Claude Code

Build and install:

```bash
bash scripts/build.sh --platform claude-code
mkdir -p ~/.claude/skills ~/.claude/commands
ln -sfn "$(pwd)/dist/claude-code" ~/.claude/skills/obsidian-second-brain
ln -sfn "$(pwd)/dist/claude-code/commands/"*.md ~/.claude/commands/
```

## Hermes

Build:

```bash
bash scripts/build.sh --platform hermes
```

Install skills and hooks according to `dist/hermes/INSTALL.md` and
`dist/hermes/HOOKS.md`.
