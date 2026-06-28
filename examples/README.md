# Sample vault

This folder shows what an obsidian-second-brain vault looks like in practice. Every note inside `sample-vault/` follows the AI-first rule defined in [`references/ai-first-rules.md`](../references/ai-first-rules.md).

If you are evaluating the skill, browse the files here before installing. If you are contributing a new command, match the structure shown in the note type closest to your output.

## What's in here

```
ieh-vault-template/                                      # Clean distributable IEH compound/stage-model vault template
sample-vault/
├── _CLAUDE.md                                       # Vault operating manual (the file /obsidian-init writes)
├── Daily/2026-04-27.md                              # type: daily
├── people/Alex Rivera.md                            # type: person (vault owner)
├── people/Sam Patel.md                              # type: person (collaborator)
├── Projects/Tide.md                                 # type: project
├── Ideas/2026-04-27 — Streak insurance feature.md   # type: idea
└── wiki/logs/2026-04-27 — Tide retention rebuild.md # type: devlog
```

A real vault would also have `Companies/`, `Decisions/`, `Knowledge/`, `Research/`, `Boards/`, and `social-media/` folders. Those are referenced in wikilinks here but not included as files — a 7-file sample is enough to show the AI-first pattern without bloating the repo.

## What to look for

Each file demonstrates the 7 rules from the AI-first spec:

1. **Self-contained context** — every note explains itself without relying on backlinks alone
2. **`## For future Claude` preamble** — the 2-3 sentence summary right after the frontmatter
3. **Rich frontmatter** — `type`, `date`, `tags`, `ai-first: true`, plus type-specific fields
4. **Recency markers per claim** — external facts carry `(as of YYYY-MM, source.com)`
5. **Sources verbatim** — URLs preserved inline, not paraphrased
6. **Mandatory `[[wikilinks]]`** — every person, project, idea linked
7. **Confidence levels** — `stated | high | medium | speculation` where applicable

## Important note about the content

Everything here is fictional. **Alex Rivera**, **Sam Patel**, **Tide**, **Currentscale Labs**, and the cited URLs are made up. Do not treat any claim in this folder as a real fact about a real person or product. The point is to show structure and tone, not to provide research.

## How to use this for your own vault

Use `ieh-vault-template/` if you want the full IEH compound/stage-model structure immediately:

```
cp -R examples/ieh-vault-template /path/to/NewVault
python3 scripts/compound_vault.py --vault /path/to/NewVault init
python3 scripts/compound_vault.py --vault /path/to/NewVault mode set singularity
python3 scripts/install_desktop.py /path/to/NewVault --json
python3 scripts/compound_vault.py --vault /path/to/NewVault health --json
```

Do not copy `sample-vault/` into your vault. It exists only to show small AI-first note examples before you install.

If you want a clean starting point, run:

```
/obsidian-init
```

That writes a real `_CLAUDE.md` tailored to your name, your projects, and your folder preferences.
