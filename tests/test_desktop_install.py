#!/usr/bin/env python3
import json
import subprocess
import sys


def test_desktop_install_check_and_rollback(tmp_path):
    repo = __import__("pathlib").Path(__file__).resolve().parents[1]
    vault = tmp_path / "vault"
    subprocess.run(["bash", "scripts/build.sh", "--platform", "codex-cli"], cwd=repo, check=True, capture_output=True, text=True)

    install = subprocess.run(
        [sys.executable, "scripts/install_desktop.py", str(vault), "--no-build", "--json"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(install.stdout)
    assert payload["ok"] is True
    assert (vault / "AGENTS.md").exists()
    assert (vault / ".codex/scripts/compound_vault.py").exists()
    assert (vault / ".vault-meta/desktop-install-manifest.json").exists()

    check = subprocess.run(
        [sys.executable, "scripts/install_desktop.py", str(vault), "--check", "--json"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(check.stdout)["ok"] is True

    rollback = subprocess.run(
        [sys.executable, "scripts/install_desktop.py", str(vault), "--rollback", "--json"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    removed = set(json.loads(rollback.stdout)["removed"])
    assert "AGENTS.md" in removed
    assert ".vault-meta/desktop-install-manifest.json" in removed
    assert not (vault / "AGENTS.md").exists()

    missing = subprocess.run(
        [sys.executable, "scripts/install_desktop.py", str(vault), "--check", "--json"],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    assert missing.returncode == 1
    assert json.loads(missing.stdout)["ok"] is False
