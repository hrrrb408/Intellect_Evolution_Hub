---
description: Add a machine-readable IEH task into tasks/
category: vault
triggers_en: ["add task", "new todo", "track this", "remind me"]
---

Use the obsidian-second-brain skill. Execute `/obsidian-task $ARGUMENTS`:

1. Read `_CLAUDE.md` first if it exists in the vault root.
2. Treat `tasks/` as the only durable task layer. Do not use legacy `Tasks/`, `Boards/`, or ad-hoc Kanban files unless the user explicitly asks.
3. Add the task through the manifest-aware runtime:
   `python3 scripts/compound_vault.py --vault "$OBSIDIAN_VAULT_PATH" task add "$ARGUMENTS"`
4. If the user gives clear metadata, pass it explicitly:
   - `--file inbox|today|upcoming|waiting`
   - `--priority low|medium|high`
   - `--context computer|phone|errands|reading`
   - `--due YYYY-MM-DD`
   - `--project <name>`
   - `--source <wikilink-or-path>`
5. Default ambiguous tasks to `tasks/inbox.md`, `priority:medium`, and `context:computer`.
6. After writing, refresh index/hot through the runtime and report the generated `task-YYYYMMDD-xxxxxxxx` id to the user.

The canonical IEH task structure is:

```text
tasks/
  inbox.md
  today.md
  upcoming.md
  waiting.md
  done.md
  projects/
  contexts/
    computer.md
    phone.md
    errands.md
    reading.md
```

Every real task line must be a checkbox with stable machine metadata:

```md
- [ ] 中文任务标题 / English task title id:task-20260726-abc12345 created:2026-07-26 due:2026-07-30 priority:high status:active context:computer
```

**AI-first rule:** `tasks/` pages are user-facing IEH notes. Keep headings and explanatory text Chinese-first with English correspondence. Task checkbox lines may be compact machine-readable records, but do not create fake bilingual placeholders such as `中文对应`.

**Anti-fabrication:** Never invent due dates, people, project names, or source links. If metadata is unclear, omit it or keep the task in `tasks/inbox.md`.
