---
description: Ingest a local file or URL into wiki/sources, then refresh hot/index/log.
category: research
triggers_en: ["compound ingest", "ingest to compound vault", "add source to wiki sources", "compound vault ingest"]
argument-hint: "<file path or URL>"
allowed-tools: Bash, Read, Grep, Glob
---

# /obsidian-compound-ingest

Ingest a source into the Compound Vault source layer, refresh generated context,
record manifest/delta state, and create low-confidence entity/concept stubs when
deterministic candidates are visible.

## Procedure

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
python3 "$SCRIPT" ingest "$ARGUMENTS"
```

Then read:

- the new source note
- `wiki/meta/rewrite-plan-latest.md`
- `wiki/meta/source-claims-latest.json`
- `wiki/meta/contradictions-latest.json`
- `wiki/meta/patch-proposals-latest.md`
- `wiki/hot.md`
- `wiki/index.md`

If the source is unchanged in `.vault-meta/compound-manifest.json`, the script
skips it unless `--force` is passed.

## AI follow-up

After ingestion, run the rewrite workflow. The script preserves the source,
creates low-confidence stubs, and writes a deterministic rewrite plan. You must
complete the synthesis step:

1. Read the source note completely.
2. Read `wiki/meta/rewrite-plan-latest.md`.
3. Read `wiki/meta/source-claims-latest.json` for extracted claims.
4. Read `wiki/meta/contradictions-latest.json` for possible conflicts.
5. Read `wiki/meta/patch-proposals-latest.md` for structured review items.
6. Read each existing durable note listed under "Existing Notes to Review".
7. For each verified entity/concept/project/decision:
   - update the existing note if one exists
   - otherwise promote the generated stub into a durable note
   - add source wikilinks and confidence labels
   - preserve changed old claims in a History or Timeline section
8. Do not treat deterministic stubs, claims, contradictions, or patch proposals
   as verified until the source and target notes support them.
9. Append any meaningful update to `wiki/log.md`.
10. Refresh generated context:

   ```bash
   python3 "$SCRIPT" index
   python3 "$SCRIPT" chunks
   python3 "$SCRIPT" hot
   ```

When editing existing files, use the locking protocol from `references/locking-protocol.md`.
