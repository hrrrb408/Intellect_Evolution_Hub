---
description: Answer a question from the Obsidian vault using Compound Vault hot/index/BM25 retrieval.
category: vault
triggers_en: ["query the vault", "ask the compound vault", "search compound vault", "answer from hot index"]
argument-hint: "<question>"
allowed-tools: Bash, Read, Glob, Grep
---

# /obsidian-query

Answer the user's question from the vault. This command adds the claude-obsidian-style query path to obsidian-second-brain:

1. Refresh or read `wiki/hot.md`.
2. Use `wiki/index.md` and chunked BM25 retrieval to find candidate notes.
3. Read only the top relevant notes.
4. Answer with wikilinks and file-backed evidence.
5. If the vault does not know the answer, say so and create/suggest a `wiki/questions/<slug>.md` follow-up.

## Procedure

Use the vault path in `$OBSIDIAN_VAULT_PATH`; if it is not set, use the current working directory as the vault.

```bash
SCRIPT=""
for candidate in \
  scripts/compound_vault.py \
  .codex/scripts/compound_vault.py \
  .gemini/scripts/compound_vault.py \
  .opencode/scripts/compound_vault.py \
  "$HOME/.claude/skills/obsidian-second-brain/scripts/compound_vault.py"; do
  if [ -f "$candidate" ]; then
    SCRIPT="$candidate"
    break
  fi
done
if [ -z "$SCRIPT" ]; then
  echo "compound_vault.py not found. Run from the skill checkout or install a built platform dist into the vault." >&2
  exit 2
fi
python3 "$SCRIPT" query "$ARGUMENTS" --refresh --top-k 8 --rerank auto
```

Then read:

- `wiki/hot.md`
- `wiki/meta/last-query.md`
- the top 3-8 files listed in `last-query.md`

`--refresh` also rebuilds `.vault-meta/chunks/` and `.vault-meta/bm25/index.json`.
If the chunk index is unavailable, the script falls back to whole-file BM25.
`--rerank auto` tries local Ollama embeddings with `nomic-embed-text`, then
falls back to lexical rerank. Remote `OLLAMA_URL` endpoints are blocked unless
the user explicitly passes `--allow-remote-ollama`.

## Response rules

- Prefer vault evidence over model memory.
- Cite relevant notes with `[[wikilinks]]` and mention the path when ambiguity matters.
- Do not scan the whole vault unless retrieval clearly fails.
- Do not invent sources.
- If evidence conflicts, show the conflict and recommend `/obsidian-reconcile` or a manual decision note.
