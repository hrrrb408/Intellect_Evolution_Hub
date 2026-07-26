---
description: Generate a compact IEH task review
category: vault
triggers_en: ["review tasks", "task summary", "today tasks", "todo review"]
---

Use the obsidian-second-brain skill. Execute `/obsidian-task-review $ARGUMENTS`:

1. Run:
   `python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" task review $ARGUMENTS`
2. Read `wiki/meta/task-review-latest.md`.
3. Summarize active, waiting, and done counts; then surface the highest-priority active tasks.
4. If the user asks to plan today, use `tasks/today.md`, `tasks/waiting.md`, and `tasks/upcoming.md` as the durable source of truth.

This command reviews the task layer only. Do not mutate tasks unless the user explicitly asks.
