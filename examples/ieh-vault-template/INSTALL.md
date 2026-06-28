---
title: IEH Template Install
type: maintenance
ai-first: true
sources: []
---

# IEH Template Install

## For future Claude
Use this file as the local setup checklist for a new IEH template instance.

## Steps

From the repository root:

```bash
cp -R examples/ieh-vault-template /path/to/NewVault
python3 scripts/compound_vault.py --vault /path/to/NewVault init
python3 scripts/compound_vault.py --vault /path/to/NewVault mode set singularity
python3 scripts/install_desktop.py /path/to/NewVault --json
python3 scripts/compound_vault.py --vault /path/to/NewVault health --json
```

Open `/path/to/NewVault` in Obsidian.

## Optional git baseline

```bash
cd /path/to/NewVault
git init
git add .
git commit -m "Initialize IEH vault"
```
