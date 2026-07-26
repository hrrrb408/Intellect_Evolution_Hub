---
description: List active, waiting, done, or all IEH tasks
category: vault
triggers_en: ["list tasks", "show todos", "what are my tasks", "task review"]
---

Use the obsidian-second-brain skill. Execute `/obsidian-task-list $ARGUMENTS`:

1. Read `_CLAUDE.md` first if it exists.
2. List tasks only through the runtime:
   `python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" task list $ARGUMENTS`
3. Supported filters:
   - `--status active|waiting|done|cancelled|all`
   - `--context computer|phone|errands|reading`
   - `--json`
4. Open the referenced `tasks/*.md` files only when the user asks for detail or when a task needs surrounding context.

Report task ids exactly. They are required for `/obsidian-task-done`.
