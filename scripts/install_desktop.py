#!/usr/bin/env python3
"""Install desktop-facing adapter files into an Obsidian vault.

This script keeps Desktop support file-based and explicit:
- Codex Desktop gets the Codex adapter output copied into the vault root.
- Claude Desktop gets a handoff document in the vault; app-level MCP/project
  configuration remains a user-controlled step.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def copy_tree_contents(src: Path, dst: Path) -> None:
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def main() -> int:
    parser = argparse.ArgumentParser(description="Install desktop adapter files into a vault")
    parser.add_argument("vault", help="Target Obsidian vault path")
    parser.add_argument("--no-build", action="store_true", help="Use existing dist/codex-cli output")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    vault.mkdir(parents=True, exist_ok=True)

    if not args.no_build:
        result = subprocess.run(
            ["bash", "scripts/build.sh", "--platform", "codex-cli"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            print(result.stdout, end="")
            print(result.stderr, end="", file=sys.stderr)
            return result.returncode

    codex_dist = REPO_ROOT / "dist" / "codex-cli"
    if not codex_dist.is_dir():
        print(f"Missing {codex_dist}. Run scripts/build.sh --platform codex-cli first.", file=sys.stderr)
        return 2

    copy_tree_contents(codex_dist, vault)

    desktop_ref = REPO_ROOT / "references" / "desktop-adapters.md"
    if desktop_ref.is_file():
        shutil.copy2(desktop_ref, vault / "DESKTOP-ADAPTERS.md")

    print(f"Installed Codex Desktop adapter files into {vault}")
    print(f"- {vault / 'AGENTS.md'}")
    print(f"- {vault / '.agents/skills'}")
    print(f"- {vault / '.codex/scripts/compound_vault.py'}")
    print(f"- {vault / 'DESKTOP-ADAPTERS.md'}")
    print("Claude Desktop: configure MCP or project instructions to read this vault; app settings are not changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
