#!/usr/bin/env bash
# Recapture the Welcome lesson's two content boards at 1600x900 (video-source shape),
# composed on the page background like lessons/welcome-3-close.jpg.
#
# Run this after ANY edit to the Welcome lesson's quote card or five-step path, so the
# boards the video engine gets still match what a reader sees on the page.
#
#   bash scripts/capture-welcome-boards.sh
#
# Uses its own --user-data-dir: the shared profile refuses to attach while David's
# Chrome is running (ECONNREFUSED).
set -euo pipefail
cd "$(dirname "$0")/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT="${PORT:-8774}"
DBG="${DBG:-9344}"
TMP="$(mktemp -d)"
PROFILE="$(mktemp -d)"
trap 'kill "${SERVER_PID:-}" "${CHROME_PID:-}" 2>/dev/null; sleep 1; rm -rf "$TMP" "$PROFILE" 2>/dev/null; true' EXIT

python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SERVER_PID=$!
"$CHROME" --headless=new --disable-gpu --remote-debugging-port="$DBG" \
  --user-data-dir="$PROFILE" about:blank >/dev/null 2>&1 &
CHROME_PID=$!
sleep 3

node scripts/capture-welcome-boards.js "$PORT" "$DBG" "$TMP"

for png in "$TMP"/*.png; do
  out="lessons/$(basename "${png%.png}").jpg"
  sips -s format jpeg -s formatOptions 88 "$png" --out "$out" >/dev/null
  echo "  wrote $out  ($(sips -g pixelWidth -g pixelHeight "$out" | awk '/pixel/{printf "%s ", $2}'))"
done
echo "Eyeball both before committing."
