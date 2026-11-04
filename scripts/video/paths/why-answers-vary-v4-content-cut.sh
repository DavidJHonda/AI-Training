#!/bin/bash
# Remove the repeated explanation between the two natural pauses around
# 3:28 and 3:42. The cut begins and ends inside silence, preserving complete
# sentences and bringing the "The Math" title beat directly to the transition.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../../.." && pwd)"
cd "$repo_root"

input="${1:?input video required}"
output="${2:?output video required}"

# [6251,6681) at 30 fps = 208.367s through 222.700s.
bash scripts/video/ffmpeg.sh -hide_banner -loglevel error -y \
  -i "$input" \
  -filter_complex "
[0:v]trim=start_frame=0:end_frame=6251,settb=1/30,setpts=N/(30*TB),setsar=1[v1];
[0:v]trim=start_frame=6681,settb=1/30,setpts=N/(30*TB),setsar=1[v2];
[v1][v2]concat=n=2:v=1:a=0,format=yuv420p[v];
[0:a]atrim=start=0:end=208.366667,asetpts=PTS-STARTPTS[a1];
[0:a]atrim=start=222.7,asetpts=PTS-STARTPTS[a2];
[a1][a2]concat=n=2:v=0:a=1[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart \
  "$output"

echo "Built $output; removed 14.333s (430 frames)."
