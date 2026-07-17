#!/usr/bin/env bash
# Export each lesson as a PLAIN-TEXT markdown file (lessons/<id>.md) for feeding to
# NotebookLM as a source. Unlike the PDF export (a styled page render the video
# generator can screenshot), this is just the information: headings, paragraphs,
# lists. Content only — TRY IT / LAB / nav / video pill are dropped.
#
# Usage:
#   bash scripts/make-lesson-texts.sh            # all teaching lessons
#   bash scripts/make-lesson-texts.sh layers     # just one (or several) by id
set -euo pipefail
cd "$(dirname "$0")/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT="${PORT:-8766}"
DBG="${DBG:-9334}"
OUT="lessons"
mkdir -p "$OUT"

python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SERVER_PID=$!
"$CHROME" --headless=new --disable-gpu --remote-debugging-port="$DBG" about:blank >/dev/null 2>&1 &
CHROME_PID=$!
trap 'kill "$SERVER_PID" "$CHROME_PID" 2>/dev/null || true' EXIT
# Chrome's debug port can take several seconds to come up; poll instead of a fixed sleep.
for i in $(seq 1 30); do
  curl -s -o /dev/null "http://127.0.0.1:$DBG/json/version" && break
  sleep 0.5
done

node scripts/make-lesson-texts.js "$PORT" "$DBG" "$OUT" "$@"
echo "Done. Markdown lesson texts in $OUT/"
