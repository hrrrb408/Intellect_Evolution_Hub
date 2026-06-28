#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "obsidian-hermes-session-end.sh"


@pytest.mark.skipif(shutil.which("jq") is None, reason="Hermes hook source guard uses jq")
def test_hermes_session_end_skips_hook_originated_sessions():
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        vault = tmp / "vault"
        vault.mkdir()
        marker = tmp / "consolidate-called"
        consolidate = tmp / "fake-consolidate.sh"
        consolidate.write_text(
            "#!/usr/bin/env bash\n"
            "cat >/dev/null\n"
            f"printf called > {marker}\n",
            encoding="utf-8",
        )
        consolidate.chmod(0o755)

        env = os.environ.copy()
        env.update(
            {
                "OBSIDIAN_VAULT_PATH": str(vault),
                "OBSIDIAN_HERMES_HOOK_ENABLED": "1",
                "OBSIDIAN_HERMES_CONSOLIDATE_CMD": str(consolidate),
            }
        )
        payload = {
            "session_id": "child-session",
            "source": "obsidian-hook",
            "extra": {"interrupted": False},
        }
        result = subprocess.run(
            ["bash", str(HOOK)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=True,
            env=env,
        )

        time.sleep(0.2)
        assert result.stdout == "{}\n"
        assert not marker.exists()
