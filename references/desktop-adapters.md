# Desktop adapters

This project treats Desktop apps as clients of the same vault protocol, not as
separate forks of the command set.

## Shared vault contract

All Desktop clients should operate on the same Obsidian vault:

- `_CLAUDE.md` defines the vault-specific operating rules.
- `AGENTS.md` or the platform equivalent defines tool-level routing.
- `wiki/hot.md` is the first retrieval stop.
- `wiki/index.md` is the generated map.
- `wiki/log.md` records Compound Vault operations.
- `wiki/meta/index.json` is the machine index for retrieval scripts.
- Durable notes follow `references/ai-first-rules.md`.

## Codex Desktop

Use the Codex build output as the Desktop install shape:

```bash
bash scripts/build.sh --platform codex-cli
cp -R dist/codex-cli/. /path/to/your/vault/
```

Open Codex Desktop with the vault as the workspace. Codex should see:

- `AGENTS.md` as the always-on operating manual.
- `.agents/skills/<command>/SKILL.md` as native skills.
- `.codex/references/` for shared rules.
- `.codex/scripts/compound_vault.py` for Compound Vault hot/index/query/health.

When a skill asks for `compound_vault.py`, use the command file's resolver. It
checks `scripts/`, `.codex/scripts/`, `.gemini/scripts/`, `.opencode/scripts/`,
and the Claude Code skill install path.

## Claude Desktop

Claude Desktop does not run Claude Code slash commands or hooks directly. Use
one of these access paths:

1. MCP filesystem or Obsidian MCP server pointed at the vault.
2. A Claude Project whose instructions include `_CLAUDE.md` plus this file.
3. Manual prompt commands that reference the same protocol:
   - "Read `wiki/hot.md`, then `wiki/index.md`, then answer from relevant notes."
   - "Run `python3 .codex/scripts/compound_vault.py query ...` if local tools are available."

Do not install Claude Code slash commands into Claude Desktop. Treat command
files as operating manuals unless the Desktop session exposes a shell tool.

## Claude Code

Use the Claude build output:

```bash
bash scripts/build.sh --platform claude-code
ln -sf "$(pwd)/dist/claude-code" ~/.claude/skills/obsidian-second-brain
ln -sf "$(pwd)/dist/claude-code/commands/"*.md ~/.claude/commands/
```

Claude Code can run slash commands, shell scripts, and hooks. It is the richest
runtime for command automation, but it must still follow the same vault contract
as Desktop clients.

## Rule

Adapters may differ in command invocation. They must not differ in vault shape,
write policy, retrieval order, or AI-first note rules.
