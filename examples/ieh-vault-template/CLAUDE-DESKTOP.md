---
title: Claude Desktop Runtime Manual
type: maintenance
ai-first: true
sources: []
---

# Claude Desktop Runtime Manual

## For future Claude
Claude Desktop should use this vault through filesystem access, MCP, or project
instructions. Claude Desktop does not automatically inherit Claude Code slash
commands.

## Recommended setup

1. Point Claude Desktop project context or MCP filesystem access at this vault.
2. Add `_CLAUDE.md`, `SCHEMA.md`, and `DESKTOP-ADAPTERS.md` to project
   instructions.
3. If shell tools are available, use the compound vault script for ingest,
   retrieval, and health.

## Operating rules

- Read `CRITICAL_FACTS.md`, `SOUL.md`, `_CLAUDE.md`, and `SCHEMA.md`.
- Preserve raw sources before synthesis.
- Use manifest-aware ingest when shell access exists.
- Do not overwrite durable notes without explicit user approval.
- Treat `wiki/meta/` as generated review material, not durable knowledge.
