---
description: Install built desktop-facing adapter files into a target Obsidian vault for Codex Desktop and Claude Desktop handoff.
category: meta
triggers_en: ["install desktop adapter", "install codex desktop", "prepare claude desktop", "desktop install"]
argument-hint: "<vault path> [--no-build]"
allowed-tools: Bash, Read
---

# /obsidian-desktop-install

Install the shared Desktop-facing vault files. This is more concrete than
`/obsidian-desktop-setup`: it runs the installer script against a target vault.

## Procedure

```bash
SCRIPT=""
for candidate in \
  scripts/install_desktop.py \
  .codex/scripts/install_desktop.py \
  .gemini/scripts/install_desktop.py \
  .opencode/scripts/install_desktop.py \
  "$HOME/.claude/skills/obsidian-second-brain/scripts/install_desktop.py"; do
  if [ -f "$candidate" ]; then
    SCRIPT="$candidate"
    break
  fi
done
if [ -z "$SCRIPT" ]; then
  echo "install_desktop.py not found. Run from the skill checkout or install a built platform dist into the vault." >&2
  exit 2
fi
python3 "$SCRIPT" $ARGUMENTS
```

Then verify the target vault contains:

- `AGENTS.md`
- `.agents/skills/`
- `.codex/scripts/compound_vault.py`
- `.codex/references/desktop-adapters.md`
- `DESKTOP-ADAPTERS.md`

Claude Desktop still needs MCP or project instructions pointing at the vault.
The installer does not mutate Claude Desktop app settings.
