#!/bin/bash
# ai-is-different v5 — rebuilt from v3 (pre-cut) in ONE pass, two cuts:
#
#  CUT 1  "This shift allows software to process the messy reality of human thought."
#         video [3028,3170) = 142 frames = 4.73333s ; audio [100.790, 105.52333]
#         retained gap 607ms (270ms + 337ms)
#
#  CUT 2  the "AI can interpret unstructured intent..." beat AND the "translator"
#         sentence, which are adjacent scenes: video [3631,4166) = 535 frames.
#         8 frames of the (static) cards board are held back at the join so the
#         audio only has to lose 527/30 = 17.56667s -> audio [120.620, 138.18667],
#         retained gap 523ms (170ms + 353ms). Cutting the full 535 would have left
#         only 307ms; v4's version of this cut left 60ms, which is why it's rebuilt.
#
# 7680 -> 7011 frames = 233.700s = 3:53.7
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$REPO_ROOT"
IN="$1"; OUT="$2"

bash scripts/video/ffmpeg.sh -y -i "$IN" -filter_complex "
[0:v]trim=start_frame=0:end_frame=3028,setpts=PTS-STARTPTS[v1];
[0:v]trim=start_frame=3170:end_frame=3631,setpts=PTS-STARTPTS[v2];
[0:v]trim=start_frame=4166:end_frame=4167,setpts=PTS-STARTPTS,loop=loop=7:size=1:start=0,settb=1/30,setpts=N/(30*TB)[hold];
[0:v]trim=start_frame=4166,setpts=PTS-STARTPTS[v3];
[v1][v2][hold][v3]concat=n=4:v=1:a=0[v];
[0:a]atrim=0:100.790,asetpts=PTS-STARTPTS[a1];
[0:a]atrim=105.52333:120.620,asetpts=PTS-STARTPTS[a2];
[0:a]atrim=138.18667,asetpts=PTS-STARTPTS[a3];
[a1][a2][a3]concat=n=3:v=0:a=1[a]" \
  -map "[v]" -map "[a]" \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 128k \
  "$OUT"
