#!/bin/bash
# Which App review repair: remove the expendable choice-paralysis beat and
# stop before the closing message repeats.
#
# Visual cut: remove the complete retired scene [1171,1327), bounded by scene
# changes at 39.033s and 44.233s. This prevents a sub-second flash of the
# deleted choice-paralysis graphic.
#
# Audio cut: remove [38.55,43.75), the same 5.2s duration. Both boundaries sit
# in room-tone shoulders, retaining a natural 0.56s pause between sentences.
#
# Endpoint: frame 7592 / 253.0667s in the source, during the pause after
# "any other tool" and before the repeated closing-board narration begins.
#
# Source 7814 frames -> 7436 frames = 247.8667s (4:07.87).
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../../.." && pwd)"
cd "$repo_root"

input="${1:?input video required}"
output="${2:?output video required}"

bash scripts/video/ffmpeg.sh -hide_banner -loglevel error -y \
  -i "$input" \
  -filter_complex "
[0:v]trim=start_frame=0:end_frame=1171,setpts=PTS-STARTPTS[v1];
[0:v]trim=start_frame=1327:end_frame=7592,setpts=PTS-STARTPTS[v2];
[v1][v2]concat=n=2:v=1:a=0[v];
[0:a]atrim=start=0:end=38.55,asetpts=PTS-STARTPTS[a1];
[0:a]atrim=start=43.75:end=253.0666667,asetpts=PTS-STARTPTS[a2];
[a1][a2]concat=n=2:v=0:a=1[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "$output"

echo "Built $output"
