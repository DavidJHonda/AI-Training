#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
ffmpeg="$repo_root/scripts/video/ffmpeg.sh"
alternatives_root="$repo_root/board-review-first-four/alternatives"
check_source="$repo_root/board-review-first-four/pre-standardization/start-smarter/does-ai-think-rulebook.jpg"
title_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Bold.otf"
body_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Medium.otf"
takeaway_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Demi.otf"

render_three_row_map() {
  local output="$1"
  local title="$2"
  local takeaway="$3"
  local lockup_x="$4"
  local text_x=$((lockup_x+68))
  local heading1="$5"
  local line1a="$6"
  local line1b="$7"
  local heading2="$8"
  local line2a="$9"
  local line2b="${10}"
  local heading3="${11}"
  local line3a="${12}"
  local line3b="${13}"
  local output_dir="${output%/*}"
  local temp_png="${output%.jpg}.tmp.png"
  local filter

  mkdir -p "$output_dir"

  filter="[0:v]crop=86:86:340:731,format=rgba[iconcolor]"
  filter+=";color=c=black:s=86x86,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),42),255,0)'[iconmask]"
  filter+=";[iconcolor][iconmask]alphamerge,scale=52:52[icon]"
  filter+=";color=c=white:s=1440x564,format=rgba[panelcolor]"
  filter+=";color=c=black:s=1440x564,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask]"
  filter+=";[panelcolor][panelmask]alphamerge[panel]"
  filter+=";color=c=0xf8f7ff:s=1376x160,format=rgba[rowcolor]"
  filter+=";color=c=black:s=1376x160,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[rowmask]"
  filter+=";[rowcolor][rowmask]alphamerge,split=3[row1][row2][row3]"
  filter+=";color=c=0x6546d7:s=64x64,format=rgba[badgecolor]"
  filter+=";color=c=black:s=64x64,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),31),255,0)'[badgemask]"
  filter+=";[badgecolor][badgemask]alphamerge,split=3[badge1][badge2][badge3]"
  filter+=";color=c=0xffe9ab:s=1440x84,format=rgba[barcolor]"
  filter+=";color=c=black:s=1440x84,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[barmask]"
  filter+=";[barcolor][barmask]alphamerge[bar]"
  filter+=";[1:v][panel]overlay=80:172[s1]"
  filter+=";[s1][row1]overlay=112:192[s2];[s2][row2]overlay=112:374[s3];[s3][row3]overlay=112:556[s4]"
  filter+=";[s4]drawbox=x=158:y=240:w=4:h=396:color=0xd9d2f4:t=fill[s5]"
  filter+=";[s5][badge1]overlay=128:240[s6];[s6][badge2]overlay=128:422[s7];[s7][badge3]overlay=128:604[s8]"
  filter+=";[s8][bar]overlay=80:776[s9];[s9][icon]overlay=${lockup_x}:792[s10]"
  filter+=";[s10]drawtext=fontfile='$title_font':text='$title':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40"
  filter+=",drawtext=fontfile='$body_font':text='In this section':fontsize=26:fontcolor=0x655f7c:x=(w-text_w)/2:y=104"
  filter+=",drawtext=fontfile='$title_font':text='1':fontsize=28:fontcolor=white:x=160-text_w/2:y=240+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='2':fontsize=28:fontcolor=white:x=160-text_w/2:y=422+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='3':fontsize=28:fontcolor=white:x=160-text_w/2:y=604+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='$heading1':fontsize=28:fontcolor=0x152b7a:x=224:y=211"
  filter+=",drawtext=fontfile='$body_font':text='$line1a':fontsize=24:fontcolor=0x08072b:x=224:y=255"
  filter+=",drawtext=fontfile='$body_font':text='$line1b':fontsize=24:fontcolor=0x08072b:x=224:y=287"
  filter+=",drawtext=fontfile='$title_font':text='$heading2':fontsize=28:fontcolor=0x152b7a:x=224:y=393"
  filter+=",drawtext=fontfile='$body_font':text='$line2a':fontsize=24:fontcolor=0x08072b:x=224:y=437"
  filter+=",drawtext=fontfile='$body_font':text='$line2b':fontsize=24:fontcolor=0x08072b:x=224:y=469"
  filter+=",drawtext=fontfile='$title_font':text='$heading3':fontsize=28:fontcolor=0x152b7a:x=224:y=575"
  filter+=",drawtext=fontfile='$body_font':text='$line3a':fontsize=24:fontcolor=0x08072b:x=224:y=619"
  filter+=",drawtext=fontfile='$body_font':text='$line3b':fontsize=24:fontcolor=0x08072b:x=224:y=651"
  filter+=",drawtext=fontfile='$takeaway_font':text='$takeaway':fontsize=32:fontcolor=0x08072b:x=${text_x}:y=805"

  "$ffmpeg" -loglevel error -y \
    -i "$check_source" \
    -f lavfi -i "color=c=0xeeeaff:s=1600x900" \
    -filter_complex "$filter" \
    -frames:v 1 -update 1 "$temp_png"

  "$ffmpeg" -loglevel error -y -i "$temp_png" \
    -frames:v 1 -update 1 -q:v 2 "$output"
  rm -f "$temp_png"
  echo "Built $output"
}

render_four_row_map() {
  local output="$1"
  local title="$2"
  local takeaway="$3"
  local lockup_x="$4"
  local text_x=$((lockup_x+68))
  local heading1="$5"
  local line1a="$6"
  local line1b="$7"
  local heading2="$8"
  local line2a="$9"
  local line2b="${10}"
  local heading3="${11}"
  local line3a="${12}"
  local line3b="${13}"
  local heading4="${14}"
  local line4a="${15}"
  local line4b="${16}"
  local output_dir="${output%/*}"
  local temp_png="${output%.jpg}.tmp.png"
  local filter

  mkdir -p "$output_dir"

  filter="[0:v]crop=86:86:340:731,format=rgba[iconcolor]"
  filter+=";color=c=black:s=86x86,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),42),255,0)'[iconmask]"
  filter+=";[iconcolor][iconmask]alphamerge,scale=52:52[icon]"
  filter+=";color=c=white:s=1440x564,format=rgba[panelcolor]"
  filter+=";color=c=black:s=1440x564,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask]"
  filter+=";[panelcolor][panelmask]alphamerge[panel]"
  filter+=";color=c=0xf8f7ff:s=1376x122,format=rgba[rowcolor]"
  filter+=";color=c=black:s=1376x122,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[rowmask]"
  filter+=";[rowcolor][rowmask]alphamerge,split=4[row1][row2][row3][row4]"
  filter+=";color=c=0x6546d7:s=64x64,format=rgba[badgecolor]"
  filter+=";color=c=black:s=64x64,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),31),255,0)'[badgemask]"
  filter+=";[badgecolor][badgemask]alphamerge,split=4[badge1][badge2][badge3][badge4]"
  filter+=";color=c=0xffe9ab:s=1440x84,format=rgba[barcolor]"
  filter+=";color=c=black:s=1440x84,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[barmask]"
  filter+=";[barcolor][barmask]alphamerge[bar]"
  filter+=";[1:v][panel]overlay=80:172[s1]"
  filter+=";[s1][row1]overlay=112:192[s2];[s2][row2]overlay=112:324[s3];[s3][row3]overlay=112:456[s4];[s4][row4]overlay=112:588[s5]"
  filter+=";[s5]drawbox=x=158:y=221:w=4:h=428:color=0xd9d2f4:t=fill[s6]"
  filter+=";[s6][badge1]overlay=128:221[s7];[s7][badge2]overlay=128:353[s8];[s8][badge3]overlay=128:485[s9];[s9][badge4]overlay=128:617[s10]"
  filter+=";[s10][bar]overlay=80:776[s11];[s11][icon]overlay=${lockup_x}:792[s12]"
  filter+=";[s12]drawtext=fontfile='$title_font':text='$title':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40"
  filter+=",drawtext=fontfile='$body_font':text='In this section':fontsize=26:fontcolor=0x655f7c:x=(w-text_w)/2:y=104"
  filter+=",drawtext=fontfile='$title_font':text='1':fontsize=28:fontcolor=white:x=160-text_w/2:y=221+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='2':fontsize=28:fontcolor=white:x=160-text_w/2:y=353+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='3':fontsize=28:fontcolor=white:x=160-text_w/2:y=485+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='4':fontsize=28:fontcolor=white:x=160-text_w/2:y=617+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='$heading1':fontsize=28:fontcolor=0x152b7a:x=224:y=206"
  filter+=",drawtext=fontfile='$body_font':text='$line1a':fontsize=24:fontcolor=0x08072b:x=224:y=246"
  filter+=",drawtext=fontfile='$body_font':text='$line1b':fontsize=24:fontcolor=0x08072b:x=224:y=276"
  filter+=",drawtext=fontfile='$title_font':text='$heading2':fontsize=28:fontcolor=0x152b7a:x=224:y=338"
  filter+=",drawtext=fontfile='$body_font':text='$line2a':fontsize=24:fontcolor=0x08072b:x=224:y=378"
  filter+=",drawtext=fontfile='$body_font':text='$line2b':fontsize=24:fontcolor=0x08072b:x=224:y=408"
  filter+=",drawtext=fontfile='$title_font':text='$heading3':fontsize=28:fontcolor=0x152b7a:x=224:y=470"
  filter+=",drawtext=fontfile='$body_font':text='$line3a':fontsize=24:fontcolor=0x08072b:x=224:y=510"
  filter+=",drawtext=fontfile='$body_font':text='$line3b':fontsize=24:fontcolor=0x08072b:x=224:y=540"
  filter+=",drawtext=fontfile='$title_font':text='$heading4':fontsize=28:fontcolor=0x152b7a:x=224:y=602"
  filter+=",drawtext=fontfile='$body_font':text='$line4a':fontsize=24:fontcolor=0x08072b:x=224:y=642"
  filter+=",drawtext=fontfile='$body_font':text='$line4b':fontsize=24:fontcolor=0x08072b:x=224:y=672"
  filter+=",drawtext=fontfile='$takeaway_font':text='$takeaway':fontsize=32:fontcolor=0x08072b:x=${text_x}:y=805"

  "$ffmpeg" -loglevel error -y \
    -i "$check_source" \
    -f lavfi -i "color=c=0xeeeaff:s=1600x900" \
    -filter_complex "$filter" \
    -frames:v 1 -update 1 "$temp_png"

  "$ffmpeg" -loglevel error -y -i "$temp_png" \
    -frames:v 1 -update 1 -q:v 2 "$output"
  rm -f "$temp_png"
  echo "Built $output"
}

render_three_row_map \
  "$alternatives_root/work-with-ai/opener-work-2-section-map-alternative.jpg" \
  "Work With AI" "The result depends on how you use the tool." 433 \
  "KNOW WHAT IT’S FOR" \
  "First, why AI works differently from ordinary software, the work it" \
  "does best, and how to pick your app and learn it well." \
  "USE IT WELL" \
  "Then, the moves that get a better answer, and a look at what the" \
  "model actually reads when you ask." \
  "THINK BEFORE YOU TRUST" \
  "Finally, what to do with the answer that comes back. Question it," \
  "verify it, and decide whether it’s good enough to use."

mkdir -p "$repo_root/board-review-first-four/current-selected/work-with-ai"
cp "$alternatives_root/work-with-ai/opener-work-2-section-map-alternative.jpg" \
  "$repo_root/illustrations/opener-work-section-map.jpg"
cp "$alternatives_root/work-with-ai/opener-work-2-section-map-alternative.jpg" \
  "$repo_root/lessons/opener-work-2-section.jpg"
cp "$alternatives_root/work-with-ai/opener-work-2-section-map-alternative.jpg" \
  "$repo_root/board-review-first-four/current-selected/work-with-ai/opener-work-2-section.jpg"

render_four_row_map \
  "$alternatives_root/understand-ai/opener-understand-2-section-map-alternative.jpg" \
  "Understand AI" "Each piece builds on the one before it." 468 \
  "HOW IT LEARNED" \
  "Before you open the hood, watch the machine get built. One guess-and-correct" \
  "loop, run billions of times over mountains of text." \
  "IT ALL RUNS ON MATH" \
  "See the math idea underneath it, then watch your words get turned into" \
  "numbers the machine can work with." \
  "INSIDE THE BLACK BOX" \
  "AI gets called a “black box.” Open it and find real, understandable machinery" \
  "inside, even if parts stay genuinely hard to explain." \
  "WHERE IT ALL COMES TOGETHER" \
  "Every piece snaps into place here. Learn how AI builds answers from scratch," \
  "and you’ll never look at a reply the same way again."

render_three_row_map \
  "$alternatives_root/avoid-traps/opener-avoid-2-section-map-alternative.jpg" \
  "Avoid Traps" "Recognizing the pattern is the real skill." 456 \
  "TRAPS IN THE ANSWER" \
  "First, the ways an answer goes wrong on its own. Invented facts, bias," \
  "stale knowledge, and summaries of documents the model never read." \
  "TRAPS IN YOU" \
  "Then, the traps that work on you instead of the answer. Helpful, agreeable," \
  "and engaging can make AI easy to use and easy to fall for." \
  "TRAPS FROM THE WORLD" \
  "Finally, the trap that comes looking for you. Other people’s AI can put fakes" \
  "in front of you so convincing that seeing is no longer proof."

render_three_row_map \
  "$alternatives_root/embrace-the-future/opener-embrace-2-section-map-alternative.jpg" \
  "Embrace the Future" "Take both views of the map seriously." 486 \
  "THE ARGUMENT" \
  "First, the loudest voices and why they disagree, and the reason the" \
  "argument keeps getting louder. The speed." \
  "MONSTERS AND OPEN WATER" \
  "Then, both views of the unknown. The honest case for worry," \
  "and the upside that already happened." \
  "WHERE IT LANDS ON YOU" \
  "Then, where it all lands. AI that acts, your work, the bill for all that math," \
  "and the one thing history promises about every prediction."

render_three_row_map \
  "$alternatives_root/build-your-skills/opener-build-2-section-map-alternative.jpg" \
  "Build Your Skills" "Build the skills you keep when the tool changes." 428 \
  "THE LAST OF THE AI" \
  "First, the last of the tool itself. Which model to pick, how hard to make it" \
  "think, what to type, and two habits for the road." \
  "SKILLS AI WON’T REPLACE" \
  "Then, what stays valuable when everyone has the same tool. The person in the" \
  "room, the angle nobody else brought, and the judgment that decides what’s worth doing." \
  "STAY SHARP" \
  "Then, staying current as the tools keep changing, and picking the one thing" \
  "you get genuinely good at."
