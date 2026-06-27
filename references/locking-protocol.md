# Locking Protocol

Use this whenever a command or agent writes an existing note.

## Why

Multiple AI sessions can write the same markdown file at the same time. A per-file advisory lock reduces clobbering and corrupted notes.

## Shell usage

```bash
scripts/wiki-lock.sh run "wiki/projects/my-project.md" -- python3 your_writer.py
```

Manual mode:

```bash
LOCK=$(scripts/wiki-lock.sh acquire "wiki/projects/my-project.md")
# read latest file
# apply minimal patch
scripts/wiki-lock.sh release "wiki/projects/my-project.md"
```

## Rules

- Always read the latest file after acquiring the lock.
- Patch the smallest necessary region.
- Keep raw sources immutable.
- Append an operation to `wiki/log.md` after meaningful writes.
- Stale locks are removed automatically after `WIKI_LOCK_STALE_SECONDS` seconds; default is 600.
