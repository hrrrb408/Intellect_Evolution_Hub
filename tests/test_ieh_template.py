#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "compound_vault.py"
TEMPLATE = ROOT / "examples" / "ieh-vault-template"


def run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=True,
    )


def test_ieh_template_initializes_cleanly():
    with tempfile.TemporaryDirectory() as td:
        vault = Path(td) / "IEH"
        shutil.copytree(TEMPLATE, vault)

        run("--vault", str(vault), "init")
        run("--vault", str(vault), "mode", "set", "singularity")
        health = run("--vault", str(vault), "health", "--json")
        payload = json.loads(health.stdout)

        assert payload["dead_links"] == []
        assert payload["orphan_pages"] == []
        assert payload["missing_frontmatter"] == []
        assert payload["missing_ai_first"] == []
        assert payload["template"]["is_ieh_template"] is True
        assert payload["template"]["mode"] == "singularity"
        assert (vault / "raw/articles").is_dir()
        assert (vault / "source-summaries").is_dir()
        assert (vault / "concepts").is_dir()
        assert (vault / "queries").is_dir()
        assert (vault / ".vault-meta/singularity-routes.json").is_file()
        assert (vault / ".vault-meta/ieh-template.json").is_file()
        assert not (vault / "wiki/entities").exists()
        assert not (vault / "wiki/concepts").exists()
        assert not (vault / "wiki/resources/incoming").exists()
