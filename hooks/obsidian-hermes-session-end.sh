#!/usr/bin/env bash
# obsidian-hermes-session-end.sh - Hermes on_session_end vault-maintenance hook
#
# The Hermes-runtime analog of the Claude PostCompact hook (obsidian-bg-agent.sh).
# Hermes fires `on_session_end` hooks declared in cli-config.yaml, piping a JSON
# payload to stdin and reading JSON back from stdout. This hook runs the vault
# consolidation pass (the obsidian-nightly procedure) at the end of a completed
# session, so the vault stays current without waiting for the nightly cron.
#
# TRUST CAVEAT: like the Claude bg-agent, this writes to the vault UNATTENDED, so
# it is OPT-IN and ships INERT. It does nothing unless BOTH are set:
#   - OBSIDIAN_VAULT_PATH                 (where to write), AND
#   - OBSIDIAN_HERMES_HOOK_ENABLED=1      (a second, deliberate enable flag)
# It also no-ops on interrupted sessions, and never deletes/archives - add/update
# /link only.
#
# Setup:
#   1. Register this script as an on_session_end hook in cli-config.yaml
#      (see hooks/hermes-hooks.cli-config.example.yaml).
#   2. Export OBSIDIAN_VAULT_PATH and OBSIDIAN_HERMES_HOOK_ENABLED=1.
#   3. chmod +x this script.
# To disable: clear OBSIDIAN_HERMES_HOOK_ENABLED (the gate below makes that enough).
#
# The one runtime-specific seam: how to invoke Hermes headlessly to run the
# consolidation. It is configurable via OBSIDIAN_HERMES_CONSOLIDATE_CMD; the
# default below is the documented best guess and may need adjusting to your
# Hermes version (Issue #79 tracks confirming it on a live runtime).
#
# Contract: always print `{}` to stdout (silent no-op for an observer hook).
# Logs: /tmp/obsidian-hermes-session-end.log

emit_noop() { printf '{}\n'; }

# Defense-in-depth recursion guard. Child sessions started by this hook inherit
# this environment variable and must never trigger another consolidation pass,
# even if Hermes does not include `--source` in the hook payload.
[[ "${OBSIDIAN_HERMES_SUPPRESS_SESSION_END_HOOK:-0}" == "1" ]] && { emit_noop; exit 0; }

VAULT="${OBSIDIAN_VAULT_PATH:-}"
[[ -z "$VAULT" ]] && { emit_noop; exit 0; }

# Opt-in gate: the second, deliberate flag. Without it the hook is inert even
# when registered.
[[ "${OBSIDIAN_HERMES_HOOK_ENABLED:-0}" != "1" ]] && { emit_noop; exit 0; }

INPUT=$(cat)

# Only consolidate sessions that finished cleanly. Interrupted sessions are
# skipped so a half-finished context is not propagated.
INTERRUPTED=$(printf '%s' "$INPUT" | jq -r '.extra.interrupted // false' 2>/dev/null || echo "false")
[[ "$INTERRUPTED" == "true" ]] && { emit_noop; exit 0; }

# Prevent recursive hook storms. The consolidation command is expected to start
# its own Hermes session with `--source obsidian-hook`; when that child session
# ends, Hermes fires on_session_end again. Do not consolidate hook-originated
# sessions.
SOURCE=$(printf '%s' "$INPUT" | jq -r '.source // .extra.source // ""' 2>/dev/null || echo "")
[[ "$SOURCE" == "obsidian-hook" ]] && { emit_noop; exit 0; }

VAULT_HASH=$(python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.argv[1].encode()).hexdigest())' "$VAULT")
SENTINEL="/tmp/obsidian-hermes-session-end.${VAULT_HASH}.active"
if [[ -e "$SENTINEL" ]]; then
  NOW_EPOCH=$(date +%s)
  SENTINEL_MTIME=$(python3 -c 'import os,sys; print(int(os.path.getmtime(sys.argv[1])))' "$SENTINEL" 2>/dev/null || echo "$NOW_EPOCH")
  if (( NOW_EPOCH - SENTINEL_MTIME < 1800 )); then
    emit_noop
    exit 0
  fi
  rm -f "$SENTINEL"
fi

SESSION_ID=$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
TODAY=$(date +%Y-%m-%d)

PROMPT="Read _CLAUDE.md at the vault root and follow its rules exactly. Run the \
obsidian-nightly consolidation pass for VAULT=$VAULT (TODAY=$TODAY): close the \
day, reconcile conflicting entity/concept claims, synthesize cross-source \
patterns, heal orphan links, rebuild index.md, and append a line to log.md. \
Add/update/link only - never delete, archive, or merge. Run silently, ask \
nothing. Triggered by Hermes on_session_end for session $SESSION_ID."

# Default headless invocation. Override OBSIDIAN_HERMES_CONSOLIDATE_CMD if your
# Hermes build uses a different non-interactive entrypoint. The prompt is passed
# on the command's stdin.
CONSOLIDATE_CMD="${OBSIDIAN_HERMES_CONSOLIDATE_CMD:-hermes run --quiet}"

touch "$SENTINEL" 2>/dev/null || { emit_noop; exit 0; }
(
  export OBSIDIAN_HERMES_SUPPRESS_SESSION_END_HOOK=1
  trap 'rm -f "$SENTINEL"' EXIT
  cd "$VAULT" 2>/dev/null && \
  printf '%s' "$PROMPT" | $CONSOLIDATE_CMD >> /tmp/obsidian-hermes-session-end.log 2>&1
) &

emit_noop
exit 0
