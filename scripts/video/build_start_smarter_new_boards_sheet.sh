#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
output="$repo_root/board-review-first-four/start-smarter-new-lesson-boards.jpg"
temp_png="${output%.jpg}.tmp.png"
title_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Heavy.otf"
label_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Demi.otf"
ffmpeg="$repo_root/scripts/video/ffmpeg.sh"

"$ffmpeg" -loglevel error -y \
  -i "$repo_root/illustrations/why-learn-ai-thrive.jpg" \
  -i "$repo_root/illustrations/what-is-ai-llm.jpg" \
  -i "$repo_root/illustrations/does-ai-think-rulebook.jpg" \
  -i "$repo_root/illustrations/what-you-can-control-hands.jpg" \
  -i "$repo_root/illustrations/does-school-matter-two-skills.jpg" \
  -i "$repo_root/illustrations/learn-with-ai-study-tools.jpg" \
  -filter_complex "color=c=white:s=2400x1350,format=rgb24[bg];[0:v]scale=736:414[b1];[1:v]scale=736:414[b2];[2:v]scale=736:414[b3];[3:v]scale=736:414[b4];[4:v]scale=736:414[b5];[5:v]scale=736:414[b6];[bg][b1]overlay=60:170[s1];[s1][b2]overlay=832:170[s2];[s2][b3]overlay=1604:170[s3];[s3][b4]overlay=60:698[s4];[s4][b5]overlay=832:698[s5];[s5][b6]overlay=1604:698[s6];[s6]drawtext=fontfile='$title_font':text='Start Smarter — New lesson boards':fontsize=60:fontcolor=0x08072b:x=(w-text_w)/2:y=34,drawtext=fontfile='$label_font':text='WHY LEARN AI?':fontsize=26:fontcolor=0x655f7c:x=60+(736-text_w)/2:y=125,drawtext=fontfile='$label_font':text='WHAT IS AI?':fontsize=26:fontcolor=0x655f7c:x=832+(736-text_w)/2:y=125,drawtext=fontfile='$label_font':text='DOES AI THINK?':fontsize=26:fontcolor=0x655f7c:x=1604+(736-text_w)/2:y=125,drawtext=fontfile='$label_font':text='WHAT YOU CAN CONTROL':fontsize=26:fontcolor=0x655f7c:x=60+(736-text_w)/2:y=653,drawtext=fontfile='$label_font':text='DOES SCHOOL MATTER?':fontsize=26:fontcolor=0x655f7c:x=832+(736-text_w)/2:y=653,drawtext=fontfile='$label_font':text='LEARN WITH AI':fontsize=26:fontcolor=0x655f7c:x=1604+(736-text_w)/2:y=653,drawtext=fontfile='$label_font':text='Exact illustrations currently used on the lesson pages':fontsize=26:fontcolor=0x655f7c:x=(w-text_w)/2:y=1215" \
  -frames:v 1 -update 1 "$temp_png"

"$ffmpeg" -loglevel error -y -i "$temp_png" \
  -frames:v 1 -update 1 -q:v 2 "$output"
rm -f "$temp_png"

echo "Built $output"
