# Ultimate Gap Audit

Generated: 2026-06-28

This document is the control plane for evolving this fork from a complete code
base into a live, multi-runtime, self-growing second-brain system.

## Current judgement

The repository is no longer an empty shell. The core code base, adapters,
Compound Vault runtime, Desktop install flow, IEH/SINGULARITY stage model,
PDF/OCR ingest, BM25 chunk retrieval, patch proposals, and fusion draft workflow
exist and have been tested.

The remaining gap is operational: making the IEH vault run as a daily system
across Codex Desktop, Claude Desktop, Hermes, Claude Code, and future ChatGPT
or MCP clients. That requires identity files, runtime manuals, scheduled
automation, and large-scale source ingestion.

## Evidence snapshot

- Repository remote: `https://github.com/hrrrb408/Intellect_Evolution_Hub.git`
- Current README rewrite commit: `2ce8e27 Rewrite IEH project README`
- Latest functional workflow commit before README: `c3835e9 Add reviewable fusion draft workflow`
- Command count: 58 command files under `commands/`
- Build outputs present:
  - `dist/claude-code/`
  - `dist/codex-cli/`
  - `dist/gemini-cli/`
  - `dist/opencode/`
  - `dist/hermes/`
- IEH vault path: `/Users/huangruibang/项目/Intellect_Evolution_Hub/IEH`
- IEH health at audit time:
  - dead links: 0
  - orphan pages: 0
  - missing frontmatter: 0
  - missing `ai-first`: 0
  - duplicate titles: 0
  - PDF extraction issues: 0
- Desktop install check: pass
- Current IEH content scale:
  - raw articles: 3
  - raw papers: 0
  - source summaries: 3
  - concepts: 3
  - entities: 1
  - queries: 1
  - MOCs: 1
  - manifest sources: 4
  - chunk directories: 18
  - BM25 index: present

## Layer 1 - Code base

### Complete

- Single command source under `commands/`.
- Multi-platform adapters for Claude Code, Codex CLI, Gemini CLI, OpenCode,
  and Hermes.
- Compound Vault engine in `scripts/compound_vault.py`.
- Desktop installer/check/rollback in `scripts/install_desktop.py`.
- Configurable SINGULARITY routes.
- PDF extraction plus OCR fallback diagnostics.
- Manifest/delta tracking for ingested sources.
- Chunked BM25 retrieval.
- Optional rerank path.
- Source claim extraction.
- Contradiction candidate generation.
- Timeline/history-oriented patch proposal generation.
- Safe `apply-proposals` workflow.
- Fusion proposal and reviewable draft workflow.
- Tests covering smoke, compound vault, and desktop installer.

### Still open

- True semantic vector retrieval is not implemented as a first-class index.
  Current retrieval is BM25/chunks plus lexical or optional local rerank.
- ZAI/API-backed embeddings are not wired into the retrieval protocol.
- Hermes lifecycle hook has a known runtime seam: the default headless command
  is `hermes run --quiet`, but it still needs live confirmation against the
  user's installed Hermes version.
- ChatGPT/MCP bridge is not formalized in this repository.
- Scheduled automation is documented and emitted for Hermes, but not verified
  as installed and running on the user's machine.

## Layer 2 - IEH vault protocol

### Complete

- IEH stage directories exist.
- `SCHEMA.md` describes the stage model and routing rules.
- `index.md` works as the human front door.
- Runtime files exist:
  - `wiki/hot.md`
  - `wiki/index.md`
  - `wiki/log.md`
  - `wiki/meta/`
  - `.vault-meta/compound-manifest.json`
  - `.vault-meta/chunks/`
  - `.vault-meta/bm25/index.json`
- Codex Desktop adapter files exist:
  - `AGENTS.md`
  - `.agents/skills/`
  - `.codex/scripts/compound_vault.py`
  - `.codex/references/`
  - `DESKTOP-ADAPTERS.md`

### Added in this phase

- `_CLAUDE.md`: shared vault operating manual for Claude-family runtimes.
- `SOUL.md`: durable identity and mission file.
- `CRITICAL_FACTS.md`: small high-priority context file for quick startup.
- `CODEX-DESKTOP.md`: Codex Desktop runtime manual.
- `CLAUDE-DESKTOP.md`: Claude Desktop runtime manual.
- `HERMES.md`: Hermes runtime manual.

### Still open

- Large-scale re-ingest from the old SINGULARITY vault has not been done.
- The advisor-paper seed set is small; it proves the workflow but is not yet a
  complete research map.
- Root index, MOCs, and queries must be updated continuously as real source
  ingestion grows.

## Layer 3 - External runtime integration

### Codex Desktop

Current status: usable.

Evidence:

- `scripts/install_desktop.py --check --json` passes against the IEH vault.
- `.agents/skills/` exists.
- `.codex/scripts/compound_vault.py` exists.
- `.codex/references/desktop-adapters.md` exists.

Remaining work:

- Use IEH as the actual Codex Desktop workspace.
- Confirm that Codex Desktop sees the `.agents/skills/` list in practice.
- Run a real query and ingest from inside Codex Desktop, not only from the
  repository shell.

### Claude Desktop

Current status: protocol ready, app wiring not verified.

Remaining work:

- Point Claude Desktop at the IEH vault through filesystem access, Obsidian MCP,
  or a Claude Project.
- Include `_CLAUDE.md`, `DESKTOP-ADAPTERS.md`, and `CLAUDE-DESKTOP.md` as
  project instructions or readable root files.
- Confirm whether Claude Desktop has shell access. If not, commands are
  operating manuals rather than executable slash commands.

### Hermes

Current status: build artifacts exist; runtime activation not verified.

Evidence:

- `dist/hermes/HOOKS.md` exists.
- `dist/hermes/hooks/obsidian-hermes-session-end.sh` exists.
- `dist/hermes/optional-skills/obsidian-morning/` exists.
- `dist/hermes/optional-skills/obsidian-nightly/` exists.
- `dist/hermes/optional-skills/obsidian-weekly/` exists.
- `dist/hermes/optional-skills/obsidian-health-check/` exists.

Remaining work:

- Install optional Hermes skills intentionally.
- Register the session-end hook in Hermes `cli-config.yaml`.
- Set `OBSIDIAN_VAULT_PATH`.
- Set `OBSIDIAN_HERMES_HOOK_ENABLED=1` only after trust review.
- Confirm or override `OBSIDIAN_HERMES_CONSOLIDATE_CMD`.
- Run one live session-end test and inspect the vault log.

### Claude Code

Current status: command build exists; local user install not audited in this
phase.

Remaining work:

- Install or symlink the Claude Code build if Claude Code is a target runtime.
- Decide whether to enable PostCompact background propagation.
- Decide whether to enable PostToolUse AI-first validator.
- Decide whether to enable scheduled commands through Claude Code scheduling.

### ChatGPT / MCP

Current status: not integrated.

Remaining work:

- Decide whether ChatGPT should access the vault through filesystem MCP,
  Obsidian MCP, or a custom bridge.
- Provide a ChatGPT-facing operating manual that mirrors `_CLAUDE.md` without
  assuming shell tools.

## Layer 4 - Knowledge ingestion

### Complete

- The workflow has been tested with the advisor-paper seed set.
- Query retrieval can answer "导师的研究方向是什么" from concept/query/source
  summary/entity pages.

### Still open

- Re-ingest important SINGULARITY sources by priority. Do not bulk-copy old
  notes unless explicitly requested.
- Ingest the remaining advisor PDFs.
- Add source identity checks before polluting IEH with misnamed PDFs.
- Expand route rules as new domains appear.
- Maintain query pages as learning maps, not just indexes.

## Layer 5 - Automation

### Complete

- Hermes scheduled skill blueprints exist.
- Claude Code hook scripts exist.
- Desktop adapter install/check/rollback exists.

### Still open

- No proof yet that scheduled agents are actually active.
- No proof yet that Hermes session-end hook runs on the user's machine.
- No proof yet that Claude Code PostCompact or SessionStart hooks are installed.
- No launchd/cron state has been audited.

## Layer 6 - Retrieval upgrade

### Complete

- `wiki/hot.md`
- `wiki/index.md`
- `.vault-meta/chunks/`
- `.vault-meta/bm25/index.json`
- `query --refresh --rerank auto`

### Still open

- Embedding index.
- Claim-level retrieval.
- Evidence graph across claims, sources, concepts, and contradictions.
- API-backed semantic rerank.
- Regression tests for multilingual query quality.

## Immediate execution order

1. Treat IEH as the official working vault.
2. Keep `_CLAUDE.md`, `SOUL.md`, `CRITICAL_FACTS.md`, and runtime manuals in
   the vault root.
3. Run health after adding or changing root protocol files.
4. Verify Codex Desktop in-app skill discovery.
5. Verify Hermes optional skills and session-end hook on live runtime.
6. Choose the first large ingestion batch from SINGULARITY.
7. Ingest in batches, then run:
   - health
   - query coverage check
   - fusion draft review
   - MOC update
8. Only after content scale grows, prioritize semantic retrieval.

## Definition of ultimate state

IEH becomes "ultimate" when all of the following are true:

- Any supported AI runtime can enter the vault and know how to operate without
  re-explanation.
- All important source material is preserved and traceable.
- Every durable claim points back to raw source material.
- Query pages teach the user and guide future reading.
- MOCs expose the shape of each active field.
- Health stays clean after normal use.
- Scheduled agents or runtime hooks keep the vault current without daily manual
  reminders.
- Search works at both note level and claim/evidence level.
- The system grows by rewriting and connecting knowledge, not merely collecting
  files.
