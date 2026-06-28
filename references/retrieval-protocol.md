# Retrieval Protocol

Use this when answering from the vault.

## Retrieval order

1. `wiki/hot.md` - recent, high-signal working set.
2. `wiki/index.md` - generated map of the vault.
3. Chunked BM25 retrieval via `.vault-meta/chunks/` and `.vault-meta/bm25/index.json`.
4. Rerank candidates:
   - `--rerank auto` tries local Ollama embeddings first.
   - If Ollama is unavailable, auto falls back to lexical rerank.
   - Remote `OLLAMA_URL` is blocked unless `--allow-remote-ollama` is passed.
5. Top notes only.

Notes with frontmatter `retrieval: false` are retained in the vault but excluded from `wiki/index.md`, `wiki/hot.md`, chunked BM25, and query results. Use this for quarantined deterministic stubs, generated extraction artifacts, and audit-only pages that should not answer user questions.

## Command

```bash
python3 scripts/compound_vault.py query "your question" --refresh --top-k 8 --rerank auto
```

The script writes `wiki/meta/last-query.md` and prints JSON hits.

## Rerank modes

- `auto` - local Ollama `nomic-embed-text` when available, otherwise lexical.
- `ollama` - require Ollama attempt; falls back to BM25 order if unavailable.
- `lexical` - deterministic overlap/title rerank only.
- `none` - raw chunk BM25 order.

## Answer discipline

- Use the vault when it has evidence.
- Cite notes with wikilinks.
- Distinguish direct evidence from inference.
- If sources conflict, identify the conflict instead of silently choosing.
- If retrieval fails, ask the vault to ingest sources or create `wiki/questions/<slug>.md`.
