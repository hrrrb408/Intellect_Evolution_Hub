#!/usr/bin/env python3
"""Install desktop-facing adapter files into an Obsidian vault.

This script keeps Desktop support file-based and explicit:
- Codex Desktop gets the Codex adapter output copied into the vault root.
- Claude Desktop gets a handoff document in the vault; app-level MCP/project
  configuration remains a user-controlled step.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_REL = ".vault-meta/desktop-install-manifest.json"
EXPECTED_PATHS = [
    "AGENTS.md",
    ".agents/skills",
    ".codex/scripts/compound_vault.py",
    ".codex/references/desktop-adapters.md",
    "DESKTOP-ADAPTERS.md",
]


def copy_tree_contents(src: Path, dst: Path) -> None:
    installed = []
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
            for copied in target.rglob("*"):
                if copied.is_file():
                    installed.append(copied.relative_to(dst).as_posix())
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            installed.append(target.relative_to(dst).as_posix())
    return installed


def manifest_path(vault: Path) -> Path:
    return vault / MANIFEST_REL


def write_manifest(vault: Path, installed_paths: list[str]) -> None:
    path = manifest_path(vault)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "installed_at": dt.datetime.now().astimezone().isoformat(),
        "repo_root": str(REPO_ROOT),
        "installed_paths": sorted(set(installed_paths + ["DESKTOP-ADAPTERS.md"])),
        "expected_paths": EXPECTED_PATHS,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_manifest(vault: Path) -> dict:
    path = manifest_path(vault)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def check_install(vault: Path) -> dict:
    manifest = load_manifest(vault)
    expected = manifest.get("expected_paths", EXPECTED_PATHS) if isinstance(manifest, dict) else EXPECTED_PATHS
    items = []
    for rel in expected:
        path = vault / rel
        items.append({
            "path": rel,
            "exists": path.exists(),
            "kind": "dir" if path.is_dir() else "file" if path.is_file() else "missing",
        })
    return {
        "vault": str(vault),
        "manifest": MANIFEST_REL if manifest else "",
        "ok": all(item["exists"] for item in items),
        "items": items,
    }


def rollback(vault: Path) -> dict:
    manifest = load_manifest(vault)
    installed = manifest.get("installed_paths", []) if isinstance(manifest, dict) else []
    removed = []
    skipped = []
    for rel in sorted(set(str(x) for x in installed), key=lambda x: len(x.split("/")), reverse=True):
        path = vault / rel
        try:
            path.resolve().relative_to(vault.resolve())
        except ValueError:
            skipped.append({"path": rel, "reason": "outside vault"})
            continue
        if not path.exists():
            skipped.append({"path": rel, "reason": "missing"})
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        removed.append(rel)
    mp = manifest_path(vault)
    if mp.exists():
        mp.unlink()
        removed.append(MANIFEST_REL)
    return {"vault": str(vault), "removed": removed, "skipped": skipped}


def main() -> int:
    parser = argparse.ArgumentParser(description="Install desktop adapter files into a vault")
    parser.add_argument("vault", help="Target Obsidian vault path")
    parser.add_argument("--no-build", action="store_true", help="Use existing dist/codex-cli output")
    parser.add_argument("--check", action="store_true", help="Only check whether desktop adapter files are installed")
    parser.add_argument("--rollback", action="store_true", help="Remove files listed in the previous desktop install manifest")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    vault.mkdir(parents=True, exist_ok=True)

    if args.check:
        report = check_install(vault)
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"Desktop install check for {vault}: {'ok' if report['ok'] else 'incomplete'}")
            for item in report["items"]:
                print(f"- {item['path']}: {item['kind']}")
        return 0 if report["ok"] else 1

    if args.rollback:
        report = rollback(vault)
        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"Rolled back desktop adapter files from {vault}")
            for rel in report["removed"]:
                print(f"- removed {rel}")
            for item in report["skipped"]:
                print(f"- skipped {item['path']}: {item['reason']}")
        return 0

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

    installed = copy_tree_contents(codex_dist, vault)

    desktop_ref = REPO_ROOT / "references" / "desktop-adapters.md"
    if desktop_ref.is_file():
        shutil.copy2(desktop_ref, vault / "DESKTOP-ADAPTERS.md")
        installed.append("DESKTOP-ADAPTERS.md")
    write_manifest(vault, installed)
    report = check_install(vault)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["ok"] else 1

    print(f"Installed Codex Desktop adapter files into {vault}")
    print(f"- {vault / 'AGENTS.md'}")
    print(f"- {vault / '.agents/skills'}")
    print(f"- {vault / '.codex/scripts/compound_vault.py'}")
    print(f"- {vault / 'DESKTOP-ADAPTERS.md'}")
    print(f"- {manifest_path(vault)}")
    print("Claude Desktop: configure MCP or project instructions to read this vault; app settings are not changed.")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
