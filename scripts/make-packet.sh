#!/usr/bin/env bash
# Regenerate the downloadable course packet(s) from the live ?print= pages.
# A static snapshot — rerun this whenever the Start Smarter lessons change.
# Usage: bash scripts/make-packet.sh
set -euo pipefail
cd "$(dirname "$0")/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT="${PORT:-8765}"
mkdir -p packets
python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT
sleep 1
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=25000 \
  --print-to-pdf="packets/start-smarter.pdf" \
  "http://127.0.0.1:$PORT/index.html?print=start-smarter" 2>&1 | grep -vi "fontconfig\|GPU\|Fallback" || true
echo "Wrote packets/start-smarter.pdf"
