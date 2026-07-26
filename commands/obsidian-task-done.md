---
description: Mark an IEH task complete and archive it in tasks/done.md
category: vault
triggers_en: ["complete task", "mark done", "finish todo", "task done"]
---

Use the obsidian-second-brain skill. Execute `/obsidian-task-done <task-id>`:

1. Require a concrete task id such as `task-20260726-abc12345`.
2. Run:
   `python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" task done <task-id>`
3. The runtime moves the task into `tasks/done.md`, preserves the original id, and appends `completed:YYYY-MM-DD`.
4. If the id is missing, first run `/obsidian-task-list --status active` or ask the user which task they mean.

Do not manually delete completed tasks from the active files.
