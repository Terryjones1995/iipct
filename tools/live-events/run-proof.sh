#!/usr/bin/env bash
# Runs the live events proof: a throwaway certificate, the stand-in feed (standin.py), then proof.mjs. Never shipped.
# usage (from the repo root, through the box-wide lock):
#   HOF_HEAVY_WAIT=1800 timeout 1500 /home/terry/bin/hof-heavy bash tools/live-events/run-proof.sh <out-dir> <base-dir>
# <base-dir>: the site as it was before the reader (e.g. git archive 4fcfd8d | tar -x -C <base-dir>).
set -euo pipefail
ROOT="$(pwd)"
OUT="$(realpath -m "${1:?out dir}")"; BASE="$(realpath "${2:?base dir}")"
PORT="${PORT:-18943}"
PY=/home/terry/tasks/iipct/tools/venv/bin/python
TMP="$(mktemp -d)"
trap 'kill "${SPID:-}" 2>/dev/null || true; rm -rf "$TMP"' EXIT
mkdir -p "$OUT"
openssl req -x509 -newkey rsa:2048 -nodes -days 1 -subj "/CN=stand-in" -keyout "$TMP/key.pem" -out "$TMP/cert.pem" 2>/dev/null
echo equal > "$TMP/scenario"
"$PY" -I "$ROOT/tools/live-events/standin.py" "$ROOT" "$BASE" "$PORT" "$TMP/cert.pem" "$TMP/key.pem" "$TMP/scenario" > "$TMP/standin.log" 2>&1 &
SPID=$!
for _ in $(seq 1 50); do grep -q 'stand-in ready' "$TMP/standin.log" 2>/dev/null && break; sleep 0.2; done
grep -q 'stand-in ready' "$TMP/standin.log" || { echo "stand-in did not start:"; cat "$TMP/standin.log"; exit 1; }
node "$ROOT/tools/live-events/proof.mjs" "$OUT" "$PORT" "$TMP/scenario"
echo "stand-in log (errors only):"; grep -v 'stand-in ready' "$TMP/standin.log" | grep -iv 'BrokenPipe\|ConnectionReset' | tail -20 || true
