#!/usr/bin/env bash
# Runs the #anchor proof (anchor.mjs) against the stand-in feed. Never shipped.
# usage (from the repo root, through the box-wide lock):
#   HOF_HEAVY_WAIT=1800 timeout 900 /home/terry/bin/hof-heavy bash tools/live-events/run-anchor.sh <out.json> [<control-dir>]
# <control-dir>: optional, a copy of the site with an older reader, served as /base/ and measured too (the control).
set -euo pipefail
ROOT="$(pwd)"
OUT="$(realpath -m "${1:?out file}")"; CONTROL="${2:-}"
PORT="${PORT:-18947}"
PY=/home/terry/tasks/iipct/tools/venv/bin/python
TMP="$(mktemp -d)"
trap 'kill "${SPID:-}" 2>/dev/null || true; rm -rf "$TMP"' EXIT
mkdir -p "$(dirname "$OUT")"
openssl req -x509 -newkey rsa:2048 -nodes -days 1 -subj "/CN=stand-in" -keyout "$TMP/key.pem" -out "$TMP/cert.pem" 2>/dev/null
echo equal > "$TMP/scenario"
BASE="${CONTROL:-$ROOT}"
"$PY" -I "$ROOT/tools/live-events/standin.py" "$ROOT" "$(realpath "$BASE")" "$PORT" "$TMP/cert.pem" "$TMP/key.pem" "$TMP/scenario" > "$TMP/standin.log" 2>&1 &
SPID=$!
for _ in $(seq 1 50); do grep -q 'stand-in ready' "$TMP/standin.log" 2>/dev/null && break; sleep 0.2; done
grep -q 'stand-in ready' "$TMP/standin.log" || { echo "stand-in did not start:"; cat "$TMP/standin.log"; exit 1; }
if [ -n "$CONTROL" ]; then SITES="iipct base"; else SITES="iipct"; fi
# shellcheck disable=SC2086
node "$ROOT/tools/live-events/anchor.mjs" "$OUT" "$PORT" "$TMP/scenario" $SITES
