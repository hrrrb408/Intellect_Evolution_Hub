#!/usr/bin/env bash
# Per-file advisory lock for obsidian-second-brain-plus.
# Works without flock by using atomic mkdir.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/wiki-lock.sh run <target-file> -- <command> [args...]
  scripts/wiki-lock.sh acquire <target-file>
  scripts/wiki-lock.sh release <target-file>

Recommended use:
  scripts/wiki-lock.sh run "$TARGET" -- python3 scripts/compound_vault.py index --vault "$VAULT"

Locks live under .compound-locks/ next to the target file's vault root guess.
Stale locks older than WIKI_LOCK_STALE_SECONDS are removed automatically.
EOF
}

cmd="${1:-}"
[[ -n "$cmd" ]] || { usage; exit 64; }
shift || true

stale_seconds="${WIKI_LOCK_STALE_SECONDS:-600}"
sleep_seconds="${WIKI_LOCK_SLEEP_SECONDS:-1}"
timeout_seconds="${WIKI_LOCK_TIMEOUT_SECONDS:-60}"

hash_path() {
  if command -v shasum >/dev/null 2>&1; then
    printf '%s' "$1" | shasum -a 256 | awk '{print $1}'
  elif command -v sha256sum >/dev/null 2>&1; then
    printf '%s' "$1" | sha256sum | awk '{print $1}'
  else
    printf '%s' "$1" | cksum | awk '{print $1}'
  fi
}

lock_dir_for() {
  local target="$1"
  local abs parent root h
  parent="$(cd "$(dirname "$target")" 2>/dev/null && pwd -P || pwd -P)"
  root="$parent"
  # Walk up until we find a likely vault/repo marker, otherwise use current parent.
  while [[ "$root" != "/" ]]; do
    if [[ -d "$root/wiki" || -d "$root/.obsidian" || -d "$root/.git" ]]; then
      break
    fi
    root="$(dirname "$root")"
  done
  [[ "$root" != "/" ]] || root="$parent"
  h="$(hash_path "$target")"
  printf '%s/.compound-locks/%s.lock' "$root" "$h"
}

is_stale() {
  local lock="$1" now_ts lock_ts age
  [[ -f "$lock/pid" ]] || return 0
  now_ts="$(date +%s)"
  if stat -f %m "$lock/pid" >/dev/null 2>&1; then
    lock_ts="$(stat -f %m "$lock/pid")"
  else
    lock_ts="$(stat -c %Y "$lock/pid")"
  fi
  age=$((now_ts - lock_ts))
  [[ "$age" -gt "$stale_seconds" ]]
}

acquire() {
  local target="$1" lock start now_ts
  lock="$(lock_dir_for "$target")"
  mkdir -p "$(dirname "$lock")"
  start="$(date +%s)"
  while true; do
    if mkdir "$lock" 2>/dev/null; then
      printf '%s\n' "$$" > "$lock/pid"
      printf '%s\n' "$target" > "$lock/target"
      printf '%s\n' "$lock"
      return 0
    fi
    if is_stale "$lock"; then
      rm -rf "$lock"
      continue
    fi
    now_ts="$(date +%s)"
    if [[ $((now_ts - start)) -ge "$timeout_seconds" ]]; then
      echo "Timed out waiting for lock: $target ($lock)" >&2
      return 75
    fi
    sleep "$sleep_seconds"
  done
}

release() {
  local target="$1" lock
  lock="$(lock_dir_for "$target")"
  rm -rf "$lock"
}

case "$cmd" in
  acquire)
    [[ $# -eq 1 ]] || { usage; exit 64; }
    acquire "$1"
    ;;
  release)
    [[ $# -eq 1 ]] || { usage; exit 64; }
    release "$1"
    ;;
  run)
    [[ $# -ge 3 ]] || { usage; exit 64; }
    target="$1"; shift
    [[ "${1:-}" == "--" ]] || { usage; exit 64; }
    shift
    lock="$(acquire "$target")"
    trap 'rm -rf "$lock"' EXIT INT TERM
    "$@"
    ;;
  *)
    usage
    exit 64
    ;;
esac
