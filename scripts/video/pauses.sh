#!/usr/bin/env bash
# List narration pauses (= safe audio cut points) via silencedetect.
# Cut video at a scene cut (scenes.py) that falls inside one of these.
#
# Usage: bash scripts/video/pauses.sh in.mp4 [noise_dB=-30] [min_dur=0.25]
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
IN="${1:?usage: pauses.sh in.mp4 [noise_dB] [min_dur]}"
NOISE="${2:--30}"
DUR="${3:-0.25}"

bash "$DIR/ffmpeg.sh" -hide_banner -i "$IN" \
  -af "silencedetect=noise=${NOISE}dB:d=${DUR}" -f null - 2>&1 |
  awk '/silence_start/ { s=$NF }
       /silence_end/   { printf "%9.3f -> %9.3f  (%.3fs)\n", s, $5, $8 }'
