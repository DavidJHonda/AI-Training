#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
output_dir="$repo_root/board-review-first-four/alternatives/work-with-ai"
art_source="$output_dir/where-ai-works-best-four-shapes-alternative.jpg"
check_source="$repo_root/board-review-first-four/pre-standardization/start-smarter/does-ai-think-rulebook.jpg"
ffmpeg="$repo_root/scripts/video/ffmpeg.sh"
title_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Heavy.otf"
subtitle_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Medium.otf"
takeaway_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Demi.otf"

for required in "$art_source" "$check_source" "$title_font" "$subtitle_font" "$takeaway_font"; do
  if [[ ! -f "$required" ]]; then
    echo "Missing required file: $required" >&2
    exit 2
  fi
done

mkdir -p "$output_dir"

render_strength() {
  local filename="$1"
  local title="$2"
  local accent="$3"
  local art_x="$4"
  local mechanism_1="$5"
  local mechanism_2="$6"
  local mechanism_3="$7"
  local mechanism_4="$8"
  local example_1="$9"
  local example_2="${10}"
  local example_3="${11}"
  local example_4="${12}"
  local takeaway="${13}"
  local lockup_x="${14}"
  local strength_number="${15}"
  local output="$output_dir/$filename"
  local temp_png="${output%.jpg}.tmp.png"
  local text_x=$((lockup_x+68))
  local filter

  filter="color=c=white:s=1440x564,format=rgba[panelcolor]"
  filter+=";color=c=black:s=1440x564,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask]"
  filter+=";[panelcolor][panelmask]alphamerge[panel]"
  filter+=";[0:v]crop=300:270:${art_x}:424,setsar=1,scale=460:400:force_original_aspect_ratio=decrease,pad=500:420:(ow-iw)/2:(oh-ih)/2:color=white[art]"
  filter+=";color=c=0xffe9ab:s=1440x84,format=rgba[barcolor]"
  filter+=";color=c=black:s=1440x84,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[barmask]"
  filter+=";[barcolor][barmask]alphamerge[bar]"
  filter+=";[1:v]crop=86:86:340:731,format=rgba[iconcolor]"
  filter+=";color=c=black:s=86x86,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),42),255,0)'[iconmask]"
  filter+=";[iconcolor][iconmask]alphamerge,scale=52:52[check]"
  filter+=";[2:v][panel]overlay=80:172[s1]"
  filter+=";[s1][art]overlay=150:244[s2]"
  filter+=";[s2][bar]overlay=80:776[s3];[s3][check]overlay=${lockup_x}:792[s4]"
  filter+=";[s4]drawbox=x=720:y=212:w=2:h=484:color=0xe4e0f3:t=fill"
  filter+=",drawtext=fontfile='$title_font':text='STRENGTH ${strength_number} OF 4':fontsize=28:fontcolor=0x${accent}:x=(w-text_w)/2:y=34"
  filter+=",drawtext=fontfile='$title_font':text='$title':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=76"
  filter+=",drawtext=fontfile='$title_font':text='WHAT IT DOES':fontsize=24:fontcolor=0x${accent}:x=770:y=214"
  filter+=",drawtext=fontfile='$subtitle_font':text='$mechanism_1':fontsize=30:fontcolor=0x08072b:x=770:y=252"
  filter+=",drawtext=fontfile='$subtitle_font':text='$mechanism_2':fontsize=30:fontcolor=0x08072b:x=770:y=290"
  filter+=",drawtext=fontfile='$subtitle_font':text='$mechanism_3':fontsize=30:fontcolor=0x08072b:x=770:y=328"
  if [[ -n "$mechanism_4" ]]; then
    filter+=",drawtext=fontfile='$subtitle_font':text='$mechanism_4':fontsize=30:fontcolor=0x08072b:x=770:y=366"
  fi
  filter+=",drawbox=x=770:y=412:w=680:h=2:color=0xe4e0f3:t=fill"
  filter+=",drawtext=fontfile='$title_font':text='EXAMPLES':fontsize=24:fontcolor=0x${accent}:x=770:y=440"
  filter+=",drawtext=fontfile='$title_font':text='•':fontsize=26:fontcolor=0x${accent}:x=770:y=482"
  filter+=",drawtext=fontfile='$subtitle_font':text='$example_1':fontsize=28:fontcolor=0x08072b:x=804:y=480"
  filter+=",drawtext=fontfile='$title_font':text='•':fontsize=26:fontcolor=0x${accent}:x=770:y=527"
  filter+=",drawtext=fontfile='$subtitle_font':text='$example_2':fontsize=28:fontcolor=0x08072b:x=804:y=525"
  filter+=",drawtext=fontfile='$title_font':text='•':fontsize=26:fontcolor=0x${accent}:x=770:y=572"
  filter+=",drawtext=fontfile='$subtitle_font':text='$example_3':fontsize=28:fontcolor=0x08072b:x=804:y=570"
  filter+=",drawtext=fontfile='$title_font':text='•':fontsize=26:fontcolor=0x${accent}:x=770:y=617"
  filter+=",drawtext=fontfile='$subtitle_font':text='$example_4':fontsize=28:fontcolor=0x08072b:x=804:y=615"
  filter+=",drawtext=fontfile='$takeaway_font':text='$takeaway':fontsize=32:fontcolor=0x08072b:x=${text_x}:y=805"

  "$ffmpeg" -loglevel error -y \
    -i "$art_source" -i "$check_source" \
    -f lavfi -i "color=c=0xeeeaff:s=1600x900" \
    -filter_complex "$filter" \
    -frames:v 1 -update 1 "$temp_png"
  "$ffmpeg" -loglevel error -y -i "$temp_png" \
    -frames:v 1 -update 1 -q:v 2 "$output"
  rm -f "$temp_png"
  echo "Built $output"
}

render_strength \
  "where-ai-works-best-1-transform-alternative.jpg" \
  "Patterned transformation" "1970cf" 110 \
  "AI learns patterns, so it can take your input" \
  "and recast it into something clearer, cleaner," \
  "or better structured. The meaning stays the same." \
  "Only the shape changes." \
  "Coding help" "Reformatting messy data" \
  "Translating between languages" "Turning an outline into prose" \
  "Use AI when the meaning stays and the shape changes." 353 1

render_strength \
  "where-ai-works-best-2-generate-alternative.jpg" \
  "Generative variation" "e68100" 470 \
  "AI builds each answer by predicting likely pieces." \
  "There are usually many likely options, so it can" \
  "give you several versions at once." "" \
  "Brainstorming angles" "Give me 10 variations" \
  "Rewriting in a different tone" "First drafts of common documents" \
  "Use AI when you want several possibilities quickly." 400 2

render_strength \
  "where-ai-works-best-3-compress-alternative.jpg" \
  "Semantic compression and retrieval" "7145d3" 830 \
  "AI can read long documents and see past the" \
  "words on the page to what they actually mean." \
  "It can shrink them to the core or surface the" \
  "one part you actually need." \
  "Summarizing a chapter" "Extracting key points" \
  "Finding the relevant section" "Answering questions from supplied material" \
  "Use AI when you need the signal from long material." 354 3

render_strength \
  "where-ai-works-best-4-reason-alternative.jpg" \
  "Structured reasoning and synthesis" "138c82" 1190 \
  "AI can hold a lot of information at once. Give it" \
  "the facts, the constraints, and the goal, and it" \
  "can work through them toward an answer." "" \
  "Planning a project" "Debugging code" \
  "Comparing options" "Critiquing a draft" \
  "Use AI to work through facts, constraints, and goals." 344 4

publish_board() {
  local source_name="$1"
  local canonical_name="$2"
  local source="$output_dir/$source_name"

  cp "$source" "$repo_root/illustrations/$canonical_name"
  cp "$source" "$repo_root/lessons/$canonical_name"
  cp "$source" "$repo_root/board-review-first-four/current-selected/work-with-ai/$canonical_name"
}

publish_board "where-ai-works-best-1-transform-alternative.jpg" \
  "where-ai-works-best-1-transform.jpg"
publish_board "where-ai-works-best-2-generate-alternative.jpg" \
  "where-ai-works-best-2-variation.jpg"
publish_board "where-ai-works-best-3-compress-alternative.jpg" \
  "where-ai-works-best-3-compression.jpg"
publish_board "where-ai-works-best-4-reason-alternative.jpg" \
  "where-ai-works-best-4-reasoning.jpg"

preview="$output_dir/where-ai-works-best-detailed-preview.jpg"
"$ffmpeg" -loglevel error -y \
  -i "$output_dir/where-ai-works-best-1-transform-alternative.jpg" \
  -i "$output_dir/where-ai-works-best-2-generate-alternative.jpg" \
  -i "$output_dir/where-ai-works-best-3-compress-alternative.jpg" \
  -i "$output_dir/where-ai-works-best-4-reason-alternative.jpg" \
  -filter_complex \
  "[0:v]scale=720:405[a];[1:v]scale=720:405[b];[2:v]scale=720:405[c];[3:v]scale=720:405[d];[a][b][c][d]xstack=inputs=4:layout=0_0|760_0|0_445|760_445:fill=white[grid];[grid]pad=1600:930:40:40:color=white[out]" \
  -map "[out]" -frames:v 1 -update 1 -q:v 2 "$preview"

echo "Built $preview"
