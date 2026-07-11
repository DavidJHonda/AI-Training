#!/usr/bin/env bash
# Build (or refresh) the video-editing environment: a repo-local venv at .video-venv/
# with opencv + the imageio-ffmpeg wheel. The wheel ships a full ffmpeg binary — no
# system ffmpeg exists on this machine or is needed. Run once per machine; the venv
# persists (gitignored).
#
# Also self-tests the wheel's tpad filter: some builds silently produce ZERO padding
# (output just comes out short, no error). All scripts here use the loop-filter
# substitute regardless, but the test tells you whether hand-written tpad commands
# from the README can be trusted on this build.
#
# Usage: bash scripts/video/env.sh
set -euo pipefail
cd "$(dirname "$0")/../.."
VENV=".video-venv"

[[ -d "$VENV" ]] || python3 -m venv "$VENV"
"$VENV/bin/pip" install --quiet --upgrade pip
"$VENV/bin/pip" install --quiet --upgrade opencv-python-headless imageio-ffmpeg
FFMPEG="$("$VENV/bin/python" -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')"
echo "venv:   $VENV"
echo "ffmpeg: $FFMPEG"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
"$FFMPEG" -hide_banner -loglevel error -y \
  -f lavfi -i color=c=red:s=160x90:r=30:d=2 -pix_fmt yuv420p "$TMP/clip.mp4"
"$FFMPEG" -hide_banner -loglevel error -y \
  -i "$TMP/clip.mp4" -vf "tpad=stop_mode=clone:stop_duration=2" -pix_fmt yuv420p "$TMP/padded.mp4"
FRAMES="$("$VENV/bin/python" - "$TMP/padded.mp4" <<'PY'
import sys, cv2
print(int(cv2.VideoCapture(sys.argv[1]).get(cv2.CAP_PROP_FRAME_COUNT)))
PY
)"
if [[ "$FRAMES" -ge 110 ]]; then
  echo "tpad:   OK ($FRAMES frames from a 60-frame clip + 2s pad)"
else
  echo "tpad:   BROKEN in this wheel build ($FRAMES frames; expected ~120)."
  echo "        Hand-written tpad commands will silently under-pad — use the loop"
  echo "        substitute from README.md. The scripts here already do."
fi
