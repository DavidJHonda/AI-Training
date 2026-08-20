#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
assets="$repo_root/board-review-first-four/assets/ai-is-different"
output_dir="$repo_root/board-review-first-four/alternatives/work-with-ai"
output="$output_dir/ai-is-different-3-kryptonite-alternative.jpg"
temp_png="${output%.jpg}.tmp.png"
check_source="$repo_root/board-review-first-four/pre-standardization/start-smarter/does-ai-think-rulebook.jpg"
ffmpeg="$repo_root/scripts/video/ffmpeg.sh"
title_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Heavy.otf"
card_title_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Bold.otf"
body_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Medium.otf"
takeaway_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Demi.otf"
node="/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node"
node_modules="/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules"

NODE_PATH="$node_modules" "$node" \
  "$repo_root/scripts/video/render_ai_is_different_schematic_assets.js"

for required in \
  "$assets/scams-that-scale.png" \
  "$assets/deepfake-real-person.png" \
  "$assets/confident-but-wrong.png" \
  "$check_source" "$title_font" "$body_font" "$takeaway_font"; do
  if [[ ! -f "$required" ]]; then
    echo "Missing required file: $required" >&2
    exit 2
  fi
done

mkdir -p "$output_dir" \
  "$repo_root/board-review-first-four/current-selected/work-with-ai"

filter="[0:v]scale=310:250:force_original_aspect_ratio=decrease[art1]"
filter+=";[1:v]scale=310:250:force_original_aspect_ratio=decrease[art2]"
filter+=";[2:v]scale=300:250:force_original_aspect_ratio=decrease[art3]"
filter+=";color=c=white:s=1440x564,format=rgba[panelcolor]"
filter+=";color=c=black:s=1440x564,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask]"
filter+=";[panelcolor][panelmask]alphamerge[panel]"
filter+=";color=c=0x1970cf:s=64x64,format=rgba[m1color]"
filter+=";color=c=0x7145d3:s=64x64,format=rgba[m2color]"
filter+=";color=c=0x138c82:s=64x64,format=rgba[m3color]"
filter+=";color=c=black:s=64x64,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),31),255,0)'[markmask]"
filter+=";[m1color][markmask]alphamerge[m1]"
filter+=";color=c=black:s=64x64,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),31),255,0)'[markmask2]"
filter+=";[m2color][markmask2]alphamerge[m2]"
filter+=";color=c=black:s=64x64,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),31),255,0)'[markmask3]"
filter+=";[m3color][markmask3]alphamerge[m3]"
filter+=";color=c=0xffe9ab:s=1440x84,format=rgba[barcolor]"
filter+=";color=c=black:s=1440x84,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[barmask]"
filter+=";[barcolor][barmask]alphamerge[bar]"
filter+=";[3:v]crop=86:86:340:731,format=rgba[iconcolor]"
filter+=";color=c=black:s=86x86,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),42),255,0)'[iconmask]"
filter+=";[iconcolor][iconmask]alphamerge,scale=52:52[check]"
filter+=";[4:v][panel]overlay=80:172[s1]"
filter+=";[s1][m1]overlay=288:208[s2];[s2][m2]overlay=768:208[s3];[s3][m3]overlay=1248:208[s4]"
filter+=";[s4][art1]overlay=320-overlay_w/2:486[s5]"
filter+=";[s5][art2]overlay=800-overlay_w/2:486[s6]"
filter+=";[s6][art3]overlay=1280-overlay_w/2:486[s7]"
filter+=";[s7][bar]overlay=80:776[s8];[s8][check]overlay=307:792[s9]"
filter+=";[s9]drawbox=x=560:y=204:w=2:h=500:color=0xe4e0f3:t=fill"
filter+=",drawbox=x=1040:y=204:w=2:h=500:color=0xe4e0f3:t=fill"
filter+=",drawbox=x=120:y=466:w=400:h=2:color=0xc9c3e8:t=fill"
filter+=",drawbox=x=600:y=466:w=400:h=2:color=0xc9c3e8:t=fill"
filter+=",drawbox=x=1080:y=466:w=400:h=2:color=0xc9c3e8:t=fill"
filter+=",drawtext=fontfile='$title_font':text='You’ll see stories like this':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40+(100-text_h)/2-2"
filter+=",drawtext=fontfile='$title_font':text='!':fontsize=31:fontcolor=white:x=320-text_w/2:y=208+(64-text_h)/2"
filter+=",drawtext=fontfile='$title_font':text='=':fontsize=31:fontcolor=white:x=800-text_w/2:y=208+(64-text_h)/2"
filter+=",drawtext=fontfile='$title_font':text='+':fontsize=34:fontcolor=white:x=1280-text_w/2:y=208+(64-text_h)/2"
filter+=",drawtext=fontfile='$card_title_font':text='Scams that scale':fontsize=32:fontcolor=0x152b7a:x=80+(480-text_w)/2:y=288"
filter+=",drawtext=fontfile='$card_title_font':text='Deepfakes of real people':fontsize=32:fontcolor=0x152b7a:x=560+(480-text_w)/2:y=288"
filter+=",drawtext=fontfile='$card_title_font':text='Confident but wrong':fontsize=32:fontcolor=0x152b7a:x=1040+(480-text_w)/2:y=288"
filter+=",drawtext=fontfile='$body_font':text='AI generates code, convincing':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=338"
filter+=",drawtext=fontfile='$body_font':text='messages, and fake identities':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=376"
filter+=",drawtext=fontfile='$body_font':text='in seconds.':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=414"
filter+=",drawtext=fontfile='$body_font':text='Convincing fakes can target and':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=338"
filter+=",drawtext=fontfile='$body_font':text='humiliate anyone, including':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=376"
filter+=",drawtext=fontfile='$body_font':text='students.':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=414"
filter+=",drawtext=fontfile='$body_font':text='Medical or safety answers can':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=338"
filter+=",drawtext=fontfile='$body_font':text='sound fluent and sure even when':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=376"
filter+=",drawtext=fontfile='$body_font':text='they are flat wrong.':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=414"
filter+=",drawtext=fontfile='$takeaway_font':text='Trained behavior is harder to predict, inspect, and lock down.':fontsize=32:fontcolor=0x08072b:x=375:y=805"

"$ffmpeg" -loglevel error -y \
  -i "$assets/scams-that-scale.png" \
  -i "$assets/deepfake-real-person.png" \
  -i "$assets/confident-but-wrong.png" \
  -i "$check_source" \
  -f lavfi -i "color=c=0xeeeaff:s=1600x900" \
  -filter_complex "$filter" \
  -frames:v 1 -update 1 "$temp_png"

"$ffmpeg" -loglevel error -y -i "$temp_png" \
  -frames:v 1 -update 1 -q:v 2 "$output"
rm -f "$temp_png"

cp "$output" "$repo_root/illustrations/ai-is-different-kryptonite.jpg"
cp "$output" "$repo_root/lessons/ai-is-different-3-kryptonite.jpg"
cp "$output" "$repo_root/board-review-first-four/current-selected/work-with-ai/ai-is-different-3-kryptonite.jpg"

echo "Built $output"
