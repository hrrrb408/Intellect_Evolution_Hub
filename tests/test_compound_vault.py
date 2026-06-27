#!/usr/bin/env python3
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "compound_vault.py"


def run(*args, cwd=None):
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd, text=True, capture_output=True, check=True)


def test_init_ingest_query_health():
    with tempfile.TemporaryDirectory() as td:
        vault = Path(td)
        source = vault / "sample.md"
        source.write_text("# Project Alpha\n\nProject Alpha uses Obsidian and Claude for project memory. [[Decision One]] matters. Project Alpha has 3 active workflows in 2026.\n", encoding="utf-8")
        run("--vault", str(vault), "init")
        assert (vault / "wiki/index.md").exists()
        assert (vault / "wiki/hot.md").exists()
        assert (vault / "wiki/log.md").exists()
        existing = vault / "wiki/concepts/Project Alpha.md"
        existing.parent.mkdir(parents=True, exist_ok=True)
        existing.write_text(
            "---\ntitle: Project Alpha\ntype: concept\nai-first: true\n---\n\n## For future Claude\nOld Alpha note.\n\n# Project Alpha\n\nProject Alpha does not use Claude for memory.\n",
            encoding="utf-8",
        )

        run("--vault", str(vault), "ingest", str(source))
        source_notes = list((vault / "wiki/sources").glob("*.md"))
        assert source_notes
        assert source_notes[0].read_text(encoding="utf-8").startswith("---\n")
        assert (vault / ".vault-meta/compound-manifest.json").exists()
        assert (vault / ".vault-meta/bm25/index.json").exists()
        assert list((vault / ".vault-meta/chunks").glob("*/chunk-*.json"))
        assert list((vault / "wiki/entities").glob("*.md"))
        assert (vault / "wiki/meta/rewrite-plan-latest.md").exists()
        assert "`wiki/meta/" not in (vault / "wiki/meta/rewrite-plan-latest.md").read_text(encoding="utf-8").split("## Generated Analysis Artifacts", 1)[0]
        assert (vault / "wiki/meta/source-claims-latest.json").exists()
        assert (vault / "wiki/meta/contradictions-latest.json").exists()
        assert (vault / "wiki/meta/patch-proposals-latest.json").exists()
        assert (vault / "wiki/meta/patch-proposals-latest.md").exists()
        claims = json.loads((vault / "wiki/meta/source-claims-latest.json").read_text(encoding="utf-8"))
        proposals = json.loads((vault / "wiki/meta/patch-proposals-latest.json").read_text(encoding="utf-8"))
        assert claims
        assert proposals
        for proposal in proposals:
            if proposal["action"] in {"append_evidence", "append_timeline"}:
                assert not proposal["target_path"].startswith("wiki/sources/")
                assert not proposal["target_path"].startswith("wiki/meta/")
        assert "Project Alpha" in (vault / "wiki/index.md").read_text(encoding="utf-8")

        proposal_fixture = vault / "wiki/meta/test-proposals.json"
        proposal_fixture.write_text(json.dumps([
            {
                "proposal_id": "proposal-test-evidence",
                "target_path": "wiki/concepts/Project Alpha.md",
                "action": "append_evidence",
                "claim_id": "claim-test",
                "rationale": "test evidence append",
                "proposed_text": "- Project Alpha supports safe proposal application.",
                "status": "review-required",
            },
            {
                "proposal_id": "proposal-test-contradiction",
                "target_path": "wiki/concepts/Project Alpha.md",
                "action": "review_contradiction",
                "claim_id": "claim-test-2",
                "rationale": "test contradiction skip",
                "proposed_text": "- Review manually.",
                "status": "review-required",
            },
        ], ensure_ascii=False), encoding="utf-8")
        dry_run = run("--vault", str(vault), "apply-proposals", "--proposal-file", "wiki/meta/test-proposals.json")
        dry_payload = json.loads(dry_run.stdout)
        assert dry_payload["dry_run"] is True
        assert dry_payload["applied"] == 0
        assert any(item["status"] == "would-apply" for item in dry_payload["items"])
        assert "Project Alpha supports safe proposal application" not in existing.read_text(encoding="utf-8")
        applied = run("--vault", str(vault), "apply-proposals", "--proposal-file", "wiki/meta/test-proposals.json", "--apply")
        apply_payload = json.loads(applied.stdout)
        assert apply_payload["dry_run"] is False
        assert apply_payload["applied"] == 1
        assert any(item["reason"] == "contradiction review requires manual confirmation" for item in apply_payload["items"])
        assert "## Evidence" in existing.read_text(encoding="utf-8")
        assert "Project Alpha supports safe proposal application" in existing.read_text(encoding="utf-8")
        assert (vault / "wiki/meta/apply-proposals-latest.md").exists()

        result = run("--vault", str(vault), "query", "Alpha Claude memory", "--refresh")
        hits = json.loads(result.stdout)
        assert hits
        assert "chunk_id" in hits[0]
        assert "rerank_source" in hits[0]
        assert (vault / "wiki/meta/last-query.md").exists()

        result = run("--vault", str(vault), "query", "Alpha Claude memory", "--refresh", "--rerank", "none")
        hits = json.loads(result.stdout)
        assert hits[0]["rerank_source"] == "bm25-chunk"

        health_result = run("--vault", str(vault), "health", "--json")
        health_payload = json.loads(health_result.stdout)
        assert source_notes[0].relative_to(vault).as_posix() not in health_payload["missing_frontmatter"]
        assert all("\n" not in item["link"] for item in health_payload["dead_links"])
        assert (vault / "wiki/meta/lint-report-latest.md").exists()

        before = sorted((vault / "wiki/sources").glob("*.md"))
        result = run("--vault", str(vault), "ingest", str(source))
        assert "Already ingested unchanged source" in result.stdout
        after = sorted((vault / "wiki/sources").glob("*.md"))
        assert before == after


def test_mode_routing_and_chunks():
    with tempfile.TemporaryDirectory() as td:
        vault = Path(td)
        run("--vault", str(vault), "init")
        run("--vault", str(vault), "mode", "set", "para")
        routed = run("--vault", str(vault), "mode", "route", "source", "Test Source")
        assert "wiki/resources/incoming/test-source.md" in routed.stdout
        (vault / "Projects").mkdir()
        (vault / "Projects/Alpha.md").write_text(
            "---\ntype: project\nai-first: true\n---\n\n## For future Claude\nAlpha context.\n\n# Alpha\n\nClaude memory and Obsidian retrieval.\n",
            encoding="utf-8",
        )
        result = run("--vault", str(vault), "chunks", "--json")
        payload = json.loads(result.stdout)
        assert payload["chunk_count"] >= 1


def test_nested_git_repositories_are_not_vault_notes():
    with tempfile.TemporaryDirectory() as td:
        vault = Path(td)
        run("--vault", str(vault), "init")
        nested = vault / "nested-project"
        (nested / ".git").mkdir(parents=True)
        (nested / "README.md").write_text(
            "# Nested Project\n\nThis markdown belongs to a nested repository, not the vault.\n",
            encoding="utf-8",
        )
        note = vault / "wiki/concepts/Vault Note.md"
        note.parent.mkdir(parents=True, exist_ok=True)
        note.write_text(
            "---\ntitle: Vault Note\ntype: concept\nai-first: true\n---\n\n## For future Claude\nReal vault note.\n\n# Vault Note\n\nNested repository content should not be indexed.\n",
            encoding="utf-8",
        )
        run("--vault", str(vault), "index")
        index_text = (vault / "wiki/index.md").read_text(encoding="utf-8")
        assert "nested-project/README.md" not in index_text
        health = json.loads(run("--vault", str(vault), "health", "--json").stdout)
        assert "nested-project/README.md" not in health["missing_frontmatter"]
        query = json.loads(run("--vault", str(vault), "query", "Nested Project", "--refresh", "--rerank", "none").stdout)
        assert all(hit["path"] != "nested-project/README.md" for hit in query)


if __name__ == "__main__":
    test_init_ingest_query_health()
    test_mode_routing_and_chunks()
    test_nested_git_repositories_are_not_vault_notes()
    print("ok")
