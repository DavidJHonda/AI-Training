#!/usr/bin/env bash
# Capture a lesson element as a 1600x900 video-source board jpg (lessons/*.jpg style):
# the element composed on the page-background color inside the standard white card,
# rendered at 2x. Finds the target by text content — the innermost element containing
# ALL of the --find strings.
#
# NOT AUTOMATIC: run by hand when a board needs (re)capturing after a lesson change.
# It only covers the common case — a board that IS a lesson element. When the board
# is a composed variant that exists on no page (e.g. the embeddings two-drink taste
# table), or needs its own scale/layout, build a one-off page and screenshot that
# instead; forcing this tool will give a worse board.
#
# Usage:
#   bash scripts/capture-board.sh <lesson-id> --find "STR||STR||STR" --out lessons/<name>.jpg [--title "Board title"] [--card-width 690]
# Example (transformer problems board):
#   bash scripts/capture-board.sh attention \
#     --find "Different Meanings||Pronouns||See the problem?" \
#     --out lessons/transformer-problems.jpg \
#     --title "Two problems the words around a word have to solve"
set -euo pipefail
cd "$(dirname "$0")/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT="${PORT:-8768}"
DBG="${DBG:-9338}"

LESSON="${1:?lesson id required}"; shift
FIND="" ; OUT="" ; TITLE="" ; CARDW="690"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --find) FIND="$2"; shift 2 ;;
    --out) OUT="$2"; shift 2 ;;
    --title) TITLE="$2"; shift 2 ;;
    --card-width) CARDW="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done
[[ -n "$FIND" && -n "$OUT" ]] || { echo "--find and --out are required" >&2; exit 1; }

python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SERVER_PID=$!
"$CHROME" --headless=new --disable-gpu --remote-debugging-port="$DBG" about:blank >/dev/null 2>&1 &
CHROME_PID=$!
trap 'kill "$SERVER_PID" "$CHROME_PID" 2>/dev/null || true' EXIT
sleep 2

TMP_PNG="$(mktemp -t board).png"
node scripts/capture-board.js "$PORT" "$DBG" "$LESSON" "$FIND" "$TMP_PNG" "$TITLE" "$CARDW"
sips -s format jpeg -s formatOptions 88 "$TMP_PNG" --out "$OUT" >/dev/null
rm -f "$TMP_PNG"
echo "Board written to $OUT (1600x900). Eyeball it before committing."
