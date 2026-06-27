# Compound Vault Layer

This overlay adds claude-obsidian-style vault mechanics to obsidian-second-brain without replacing the upstream command system.

## Fixed files

- `wiki/hot.md` - small recent working set. Read this first.
- `wiki/index.md` - generated vault map. Read this second.
- `wiki/log.md` - append-only operation log.
- `wiki/meta/index.json` - machine index used by scripts.
- `wiki/meta/last-query.md` - latest retrieval result for `/obsidian-query`.
- `wiki/meta/rewrite-plan-latest.md` - latest ingest rewrite queue.
- `wiki/meta/source-claims-latest.json` - extracted source claims for review.
- `wiki/meta/contradictions-latest.json` - possible conflicts with existing notes.
- `wiki/meta/patch-proposals-latest.json` - machine-readable patch proposal queue.
- `wiki/meta/patch-proposals-latest.md` - human/agent-readable patch proposal queue.
- `wiki/meta/apply-proposals-latest.json` - machine-readable dry-run/apply report.
- `wiki/meta/apply-proposals-latest.md` - human/agent-readable dry-run/apply report.
- `wiki/meta/lint-report-latest.md` - latest health report.
- `.vault-meta/compound-manifest.json` - source hash and distribution manifest.
- `.vault-meta/chunks/` - chunk store for retrieval.
- `.vault-meta/bm25/index.json` - chunked BM25 index.
- `.vault-meta/embed-cache.json` - optional Ollama embedding cache.

## Fixed directories

- `wiki/sources/` - raw ingested source notes. Do not delete.
- `wiki/entities/` - durable people/org/tool/topic entities.
- `wiki/concepts/` - reusable concepts and patterns.
- `wiki/projects/` - project memory.
- `wiki/decisions/` - ADR-style decisions.
- `wiki/questions/` - known gaps and unresolved questions.
- `wiki/meta/` - generated indexes/reports.
- `wiki/inbox/` - temporary notes awaiting classification.

## Query protocol

1. Read `wiki/hot.md`.
2. If insufficient, read `wiki/index.md`.
3. Run `python3 scripts/compound_vault.py query "<question>" --refresh --top-k 8 --rerank auto`.
4. Read only the top relevant notes.
5. Answer with wikilinks.
6. If evidence is missing, write or suggest a question note.

## Ingest protocol

1. Preserve source material under the active methodology route.
2. Record original URL/path and hash in `.vault-meta/compound-manifest.json`.
3. Skip unchanged sources unless `--force` is passed.
4. Create low-confidence deterministic entity/concept stubs when visible.
5. Extract source claims into `wiki/meta/source-claims-latest.json`.
6. Detect contradiction candidates into `wiki/meta/contradictions-latest.json`.
7. Generate reviewable patch proposals in `wiki/meta/patch-proposals-latest.md`.
8. Write `wiki/meta/rewrite-plan-latest.md`.
9. Run `/obsidian-apply-proposals` as a dry-run; add `--apply` only after reviewing targets.
10. Read the source, claims, contradiction candidates, and skipped proposals; then manually resolve contradictions with minimal patches.
11. Refresh `wiki/index.md`, `wiki/hot.md`, `.vault-meta/chunks/`, and `.vault-meta/bm25/index.json`.

## Safety defaults

- Never delete notes automatically.
- Never rewrite the whole vault.
- Prefer minimal patches.
- Preserve raw sources.
- Never auto-apply `review_contradiction`; it requires manual confirmation.
- Use `scripts/wiki-lock.sh` before editing existing notes in concurrent sessions.
