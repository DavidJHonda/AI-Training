#!/bin/bash
# Remove two redundant narration passages from Transformer v5:
#   1. "Notice how cat faded..." before "This sequential..."
#   2. The repeated attention/transformation summary before positional order.
# The first edit starts in silence and rejoins at the next word onset. The
# second begins and ends inside pauses surrounding complete sentences.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../../.." && pwd)"
cd "$repo_root"

input="${1:?input video required}"
output="${2:?output video required}"

# Cuts in the original v5 timeline:
#   [2379,2524) = 79.300s to 84.133s
#   [5970,6411) = 199.000s to 213.700s
bash scripts/video/ffmpeg.sh -hide_banner -loglevel error -y \
  -i "$input" \
  -filter_complex "
[0:v]trim=start_frame=0:end_frame=2379,settb=1/30,setpts=N/(30*TB),setsar=1[v1];
[0:v]trim=start_frame=2524:end_frame=5970,settb=1/30,setpts=N/(30*TB),setsar=1[v2];
[0:v]trim=start_frame=6411,settb=1/30,setpts=N/(30*TB),setsar=1[v3];
[v1][v2][v3]concat=n=3:v=1:a=0,format=yuv420p[v];
[0:a]atrim=start=0:end=79.3,asetpts=PTS-STARTPTS[a1];
[0:a]atrim=start=84.133333:end=199.0,asetpts=PTS-STARTPTS[a2];
[0:a]atrim=start=213.7,asetpts=PTS-STARTPTS[a3];
[a1][a2][a3]concat=n=3:v=0:a=1[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -crf 17 -preset medium -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart \
  "$output"

echo "Built $output; removed 19.533s (586 frames)."
