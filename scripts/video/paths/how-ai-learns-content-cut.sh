#!/bin/bash
# Training review repair: remove the redundant explanation after the basketball
# test question and before "Learning cannot start cold."
#
# The 7.2-second cut keeps roughly 0.4 seconds of room tone on both sides. The
# source frames immediately after the cut have already been bridged to the next
# illustration, so no flash of the deleted data graphic survives the edit.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../../.." && pwd)"
cd "$repo_root"

input="${1:?input video required}"
output="${2:?output video required}"

bash scripts/video/ffmpeg.sh -hide_banner -loglevel error -y \
  -i "$input" \
  -filter_complex "
[0:v]trim=start_frame=0:end_frame=1245,setpts=PTS-STARTPTS[v1];
[0:v]trim=start_frame=1461:end_frame=8877,setpts=PTS-STARTPTS[v2];
[v1][v2]concat=n=2:v=1:a=0[v];
[0:a]atrim=start=0:end=41.50,asetpts=PTS-STARTPTS[a1];
[0:a]atrim=start=48.70,asetpts=PTS-STARTPTS[a2];
[a1][a2]concat=n=2:v=0:a=1[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "$output"

echo "Built $output"
