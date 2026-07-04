#!/usr/bin/env bash
# Export each lesson as a SINGLE continuous-height PDF (no page breaks, so no box is
# ever split) for feeding to NotebookLM. Content only: TRY IT / LAB / nav are dropped.
# Text stays selectable. Output: lessons/<id>.pdf
#
# Usage:
#   bash scripts/make-lesson-pdfs.sh            # all teaching lessons
#   bash scripts/make-lesson-pdfs.sh aivscode   # just one (or several) by id
set -euo pipefail
cd "$(dirname "$0")/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT="${PORT:-8765}"
DBG="${DBG:-9333}"
OUT="lessons"
mkdir -p "$OUT"

python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SERVER_PID=$!
"$CHROME" --headless=new --disable-gpu --remote-debugging-port="$DBG" about:blank >/dev/null 2>&1 &
CHROME_PID=$!
trap 'kill "$SERVER_PID" "$CHROME_PID" 2>/dev/null || true' EXIT
sleep 2

node scripts/make-lesson-pdfs.js "$PORT" "$DBG" "$OUT" "$@"
echo "Done. PDFs in $OUT/"
