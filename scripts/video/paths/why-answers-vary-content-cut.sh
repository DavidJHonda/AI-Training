#!/bin/bash
# Remove the two long closing sentences between the main conclusion and the
# final reset line. The joins sit inside the pauses after "visualize" and after
# "discarded", so both remaining sentences stay complete.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../../.." && pwd)"
cd "$repo_root"

input="${1:?input video required}"
output="${2:?output video required}"

bash scripts/video/ffmpeg.sh -hide_banner -loglevel error -y \
  -i "$input" \
  -filter_complex "
[0:v]trim=start_frame=0:end_frame=7824,settb=1/30,setpts=N/(30*TB),setsar=1[v1];
[0:v]trim=start_frame=8217,settb=1/30,setpts=N/(30*TB),setsar=1[v2];
[v1][v2]concat=n=2:v=1:a=0,format=yuv420p[v];
[0:a]atrim=start=0:end=260.8,asetpts=PTS-STARTPTS[a1];
[0:a]atrim=start=273.9,asetpts=PTS-STARTPTS[a2];
[a1][a2]concat=n=2:v=0:a=1[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart \
  "$output"

echo "Built $output; removed 13.10s (393 frames)."
