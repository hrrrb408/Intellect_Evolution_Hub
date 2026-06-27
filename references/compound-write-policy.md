# Compound Vault Write Policy

## Allowed by default

- Create new notes under `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/projects/`, `wiki/decisions/`, `wiki/questions/`.
- Refresh generated files: `wiki/hot.md`, `wiki/index.md`, `wiki/meta/index.json`, `wiki/meta/last-query.md`, health reports.
- Append to `wiki/log.md`.

## Requires care

- Editing existing durable notes.
- Reconciling contradictions.
- Moving notes between folders.
- Updating decision records.

## Not allowed without explicit user confirmation

- Delete notes.
- Rewrite an entire existing note when a small patch works.
- Remove source URLs or original file references.
- Hide contradictions.
- Modify `.obsidian/` configuration.

## Required note shape for durable notes

```md
---
title: Example
type: concept|entity|project|decision|source|question
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: low|medium|high
---

# Example

## For future AI

One-paragraph retrieval-oriented summary.

## Notes

- Claim with [[wikilinks]] and source context.

## Sources

- [[source-note]]
```
