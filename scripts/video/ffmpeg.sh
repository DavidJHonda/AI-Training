#!/usr/bin/env bash
# Run the venv's bundled ffmpeg binary (imageio-ffmpeg wheel; there is no system
# ffmpeg). Use for hand-written filter graphs from README.md.
#
# Usage: bash scripts/video/ffmpeg.sh -i in.mp4 ... out.mp4
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PY="$ROOT/.video-venv/bin/python"
[[ -x "$PY" ]] || { echo "no .video-venv — run scripts/video/env.sh first" >&2; exit 1; }
exec "$("$PY" -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')" "$@"
