#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
source_root="$repo_root/board-review-first-four/.pre-board-spec"
output_root="$repo_root/board-review-first-four/alternatives"
check_source="$repo_root/board-review-first-four/pre-standardization/start-smarter/does-ai-think-rulebook.jpg"
ffmpeg="$repo_root/scripts/video/ffmpeg.sh"
title_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Heavy.otf"
subtitle_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Medium.otf"
takeaway_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Demi.otf"

for required in "$check_source" "$title_font" "$subtitle_font" "$takeaway_font"; do
  if [[ ! -f "$required" ]]; then
    echo "Missing required file: $required" >&2
    exit 2
  fi
done

escape_drawtext() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//:/\\:}"
  value="${value//\'/\\\'}"
  value="${value//=/\\=}"
  printf '%s' "$value"
}

render_component() {
  local section="$1"
  local filename="$2"
  local crop_y="$3"
  local crop_h="$4"
  local title_line_1="$5"
  local title_line_2="$6"
  local subtitle="$7"
  local takeaway="$8"
  local lockup_x="$9"
  local crop_x="${10:-0}"
  local crop_w="${11:-1600}"
  local source="$source_root/$section/$filename"
  local output="$output_root/$section/$filename"
  local temp_png="${output%.jpg}.tmp.png"
  local text_x=$((lockup_x+68))
  local title_filter

  title_line_1="$(escape_drawtext "$title_line_1")"
  title_line_2="$(escape_drawtext "$title_line_2")"
  subtitle="$(escape_drawtext "$subtitle")"
  takeaway="$(escape_drawtext "$takeaway")"

  if [[ -n "$subtitle" ]]; then
    title_filter="drawtext=fontfile='$title_font':text='$title_line_1':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=56"
    title_filter+=",drawtext=fontfile='$subtitle_font':text='$subtitle':fontsize=26:fontcolor=0x655f7c:x=(w-text_w)/2:y=100"
  elif [[ -n "$title_line_2" ]]; then
    title_filter="drawtext=fontfile='$title_font':text='$title_line_1':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=38"
    title_filter+=",drawtext=fontfile='$title_font':text='$title_line_2':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=82"
  else
    title_filter="drawtext=fontfile='$title_font':text='$title_line_1':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40+(100-text_h)/2-2"
  fi

  mkdir -p "$(dirname "$output")"
  "$ffmpeg" -loglevel error -y \
    -i "$source" \
    -f lavfi -i "color=c=0xeeeaff:s=1600x900" \
    -i "$check_source" \
    -filter_complex "[0:v]crop=${crop_w}:${crop_h}:${crop_x}:${crop_y},scale=1408:532:force_original_aspect_ratio=decrease,pad=1408:532:(ow-iw)/2:(oh-ih)/2:color=white[body];color=c=white:s=1440x564,format=rgba[panelcolor];color=c=black:s=1440x564,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask];[panelcolor][panelmask]alphamerge[panel];color=c=0xffe9ab:s=1440x84,format=rgba[barcolor];color=c=black:s=1440x84,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[barmask];[barcolor][barmask]alphamerge[bar];[2:v]crop=86:86:340:731,format=rgba[iconcolor];color=c=black:s=86x86,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),42),255,0)'[iconmask];[iconcolor][iconmask]alphamerge,scale=52:52[icon];[1:v][panel]overlay=80:172[s1];[s1][body]overlay=96:188[s2];[s2][bar]overlay=80:776[s3];[s3][icon]overlay=${lockup_x}:792[s4];[s4]${title_filter},drawtext=fontfile='$takeaway_font':text='$takeaway':fontsize=32:fontcolor=0x08072b:x=${text_x}:y=805" \
    -frames:v 1 -update 1 "$temp_png"

  "$ffmpeg" -loglevel error -y -i "$temp_png" \
    -frames:v 1 -update 1 -q:v 2 "$output"
  rm -f "$temp_png"
  echo "Built $output"
}

render_questions_board() {
  local source="$source_root/work-with-ai/questions-matter-1-answers-cheap-alternative.jpg"
  local output="$output_root/work-with-ai/questions-matter-1-answers-cheap-alternative.jpg"
  local temp_png="${output%.jpg}.tmp.png"
  local filter

  filter="color=c=white:s=1440x564,format=rgba[panelcolor]"
  filter+=";color=c=black:s=1440x564,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask]"
  filter+=";[panelcolor][panelmask]alphamerge[panel]"
  filter+=";[0:v]crop=437:330:70:285,setsar=1,scale=380:210:force_original_aspect_ratio=decrease,pad=390:210:(ow-iw)/2:(oh-ih)/2:color=white[art1]"
  filter+=";[0:v]crop=430:320:590:300,setsar=1,scale=380:210:force_original_aspect_ratio=decrease,pad=390:210:(ow-iw)/2:(oh-ih)/2:color=white[art2]"
  filter+=";[0:v]crop=410:315:1110:300,setsar=1,scale=380:210:force_original_aspect_ratio=decrease,pad=390:210:(ow-iw)/2:(oh-ih)/2:color=white[art3]"
  filter+=";color=c=0xffe9ab:s=1440x84,format=rgba[barcolor]"
  filter+=";color=c=black:s=1440x84,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[barmask]"
  filter+=";[barcolor][barmask]alphamerge[bar]"
  filter+=";[1:v]crop=86:86:340:731,format=rgba[iconcolor]"
  filter+=";color=c=black:s=86x86,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),42),255,0)'[iconmask]"
  filter+=";[iconcolor][iconmask]alphamerge,scale=52:52[icon]"
  filter+=";[2:v][panel]overlay=80:172[s1]"
  filter+=";[s1][art1]overlay=125:494[s2];[s2][art2]overlay=605:494[s3];[s3][art3]overlay=1085:494[s4]"
  filter+=";[s4][bar]overlay=80:776[s5];[s5][icon]overlay=471:792[s6]"
  filter+=";[s6]drawbox=x=560:y=204:w=2:h=500:color=0xe4e0f3:t=fill,drawbox=x=1040:y=204:w=2:h=500:color=0xe4e0f3:t=fill"
  filter+=",drawbox=x=120:y=474:w=400:h=2:color=0xc9c3e8:t=fill,drawbox=x=600:y=474:w=400:h=2:color=0xc9c3e8:t=fill,drawbox=x=1080:y=474:w=400:h=2:color=0xc9c3e8:t=fill"
  filter+=",drawtext=fontfile='$title_font':text='How answers got cheap':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40+(100-text_h)/2-2"
  filter+=",drawtext=fontfile='$subtitle_font':text='PRE-INTERNET':fontsize=24:fontcolor=0x6a4c3a:x=80+(480-text_w)/2:y=214"
  filter+=",drawtext=fontfile='$subtitle_font':text='THE INTERNET':fontsize=24:fontcolor=0x1563c7:x=560+(480-text_w)/2:y=214"
  filter+=",drawtext=fontfile='$subtitle_font':text='NOW':fontsize=24:fontcolor=0x7040c3:x=1040+(480-text_w)/2:y=214"
  filter+=",drawtext=fontfile='$title_font':text='THE LIBRARY':fontsize=32:fontcolor=0x3d2718:x=80+(480-text_w)/2:y=252"
  filter+=",drawtext=fontfile='$title_font':text='SEARCH':fontsize=32:fontcolor=0x08072b:x=560+(480-text_w)/2:y=252"
  filter+=",drawtext=fontfile='$title_font':text='AI':fontsize=32:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=252"
  filter+=",drawtext=fontfile='$subtitle_font':text='1. Travel to the library':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=300"
  filter+=",drawtext=fontfile='$subtitle_font':text='2. Search the card catalog':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=340"
  filter+=",drawtext=fontfile='$subtitle_font':text='3. Hunt through books':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=380"
  filter+=",drawtext=fontfile='$subtitle_font':text='1. Run search after search':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=300"
  filter+=",drawtext=fontfile='$subtitle_font':text='2. Open tabs':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=340"
  filter+=",drawtext=fontfile='$subtitle_font':text='3. Judge which sites to trust':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=380"
  filter+=",drawtext=fontfile='$subtitle_font':text='1. Open the app':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=300"
  filter+=",drawtext=fontfile='$subtitle_font':text='2. Ask':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=340"
  filter+=",drawtext=fontfile='$subtitle_font':text='3. Answer on screen':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=380"
  filter+=",drawtext=fontfile='$subtitle_font':text='TIME TO ANSWER':fontsize=20:fontcolor=0x655f7c:x=80+(480-text_w)/2:y=422"
  filter+=",drawtext=fontfile='$subtitle_font':text='TIME TO ANSWER':fontsize=20:fontcolor=0x655f7c:x=560+(480-text_w)/2:y=422"
  filter+=",drawtext=fontfile='$subtitle_font':text='TIME TO ANSWER':fontsize=20:fontcolor=0x655f7c:x=1040+(480-text_w)/2:y=422"
  filter+=",drawtext=fontfile='$takeaway_font':text='Half a Saturday':fontsize=28:fontcolor=0x3d2718:x=80+(480-text_w)/2:y=448"
  filter+=",drawtext=fontfile='$takeaway_font':text='An hour or two':fontsize=28:fontcolor=0x08072b:x=560+(480-text_w)/2:y=448"
  filter+=",drawtext=fontfile='$takeaway_font':text='Seconds':fontsize=28:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=448"
  filter+=",drawtext=fontfile='$takeaway_font':text='The cost of finding an answer collapsed.':fontsize=32:fontcolor=0x08072b:x=539:y=805"

  mkdir -p "$(dirname "$output")"
  "$ffmpeg" -loglevel error -y \
    -i "$source" -i "$check_source" \
    -f lavfi -i "color=c=0xeeeaff:s=1600x900" \
    -filter_complex "$filter" \
    -frames:v 1 -update 1 "$temp_png"
  "$ffmpeg" -loglevel error -y -i "$temp_png" \
    -frames:v 1 -update 1 -q:v 2 "$output"
  rm -f "$temp_png"
  cp "$output" "$repo_root/illustrations/questions-matter-answers-cheap.jpg"
  cp "$output" "$repo_root/lessons/questions-matter-1-answers-cheap.jpg"
  echo "Built $output"
}

render_four_shapes_board() {
  local source="$source_root/work-with-ai/where-ai-works-best-four-shapes-alternative.jpg"
  local output="$output_root/work-with-ai/where-ai-works-best-four-shapes-alternative.jpg"
  local temp_png="${output%.jpg}.tmp.png"
  local filter

  filter="color=c=white:s=1440x564,format=rgba[panelcolor]"
  filter+=";color=c=black:s=1440x564,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask]"
  filter+=";[panelcolor][panelmask]alphamerge[panel]"
  filter+=";[0:v]crop=310:220:78:305,setsar=1,scale=290:260:force_original_aspect_ratio=decrease,pad=300:270:(ow-iw)/2:(oh-ih)/2:color=white[art1]"
  filter+=";[0:v]crop=310:220:455:305,setsar=1,scale=290:260:force_original_aspect_ratio=decrease,pad=300:270:(ow-iw)/2:(oh-ih)/2:color=white[art2]"
  filter+=";[0:v]crop=310:220:835:305,setsar=1,scale=290:260:force_original_aspect_ratio=decrease,pad=300:270:(ow-iw)/2:(oh-ih)/2:color=white[art3]"
  filter+=";[0:v]crop=300:220:1220:305,setsar=1,scale=290:260:force_original_aspect_ratio=decrease,pad=300:270:(ow-iw)/2:(oh-ih)/2:color=white[art4]"
  filter+=";color=c=0xffe9ab:s=1440x84,format=rgba[barcolor]"
  filter+=";color=c=black:s=1440x84,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[barmask]"
  filter+=";[barcolor][barmask]alphamerge[bar]"
  filter+=";[1:v]crop=86:86:340:731,format=rgba[iconcolor]"
  filter+=";color=c=black:s=86x86,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),42),255,0)'[iconmask]"
  filter+=";[iconcolor][iconmask]alphamerge,scale=52:52[icon]"
  filter+=";[2:v][panel]overlay=80:172[s1]"
  filter+=";[s1][art1]overlay=110:424[s2];[s2][art2]overlay=470:424[s3];[s3][art3]overlay=830:424[s4];[s4][art4]overlay=1190:424[s5]"
  filter+=";[s5][bar]overlay=80:776[s6];[s6][icon]overlay=454:792[s7]"
  filter+=";[s7]drawbox=x=440:y=204:w=2:h=500:color=0xe4e0f3:t=fill,drawbox=x=800:y=204:w=2:h=500:color=0xe4e0f3:t=fill,drawbox=x=1160:y=204:w=2:h=500:color=0xe4e0f3:t=fill"
  filter+=",drawbox=x=100:y=396:w=320:h=2:color=0x7eb8f5:t=fill,drawbox=x=460:y=396:w=320:h=2:color=0xf6b34d:t=fill,drawbox=x=820:y=396:w=320:h=2:color=0xb99de9:t=fill,drawbox=x=1180:y=396:w=320:h=2:color=0x7bc9c1:t=fill"
  filter+=",drawtext=fontfile='$title_font':text='AI is strongest when the job':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=38"
  filter+=",drawtext=fontfile='$title_font':text='has one of four shapes.':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=82"
  filter+=",drawtext=fontfile='$title_font':text='TRANSFORM':fontsize=28:fontcolor=0x1970cf:x=80+(360-text_w)/2:y=216"
  filter+=",drawtext=fontfile='$title_font':text='GENERATE':fontsize=28:fontcolor=0xe68100:x=440+(360-text_w)/2:y=216"
  filter+=",drawtext=fontfile='$title_font':text='COMPRESS':fontsize=28:fontcolor=0x7145d3:x=800+(360-text_w)/2:y=216"
  filter+=",drawtext=fontfile='$title_font':text='REASON':fontsize=28:fontcolor=0x138c82:x=1160+(360-text_w)/2:y=216"
  filter+=",drawtext=fontfile='$subtitle_font':text='Same meaning,':fontsize=30:fontcolor=0x08072b:x=80+(360-text_w)/2:y=264"
  filter+=",drawtext=fontfile='$subtitle_font':text='new shape.':fontsize=30:fontcolor=0x08072b:x=80+(360-text_w)/2:y=302"
  filter+=",drawtext=fontfile='$subtitle_font':text='Ten versions':fontsize=30:fontcolor=0x08072b:x=440+(360-text_w)/2:y=264"
  filter+=",drawtext=fontfile='$subtitle_font':text='in seconds.':fontsize=30:fontcolor=0x08072b:x=440+(360-text_w)/2:y=302"
  filter+=",drawtext=fontfile='$subtitle_font':text='Find the signal':fontsize=30:fontcolor=0x08072b:x=800+(360-text_w)/2:y=264"
  filter+=",drawtext=fontfile='$subtitle_font':text='in long material.':fontsize=30:fontcolor=0x08072b:x=800+(360-text_w)/2:y=302"
  filter+=",drawtext=fontfile='$subtitle_font':text='Work through facts':fontsize=30:fontcolor=0x08072b:x=1160+(360-text_w)/2:y=264"
  filter+=",drawtext=fontfile='$subtitle_font':text='and constraints.':fontsize=30:fontcolor=0x08072b:x=1160+(360-text_w)/2:y=302"
  filter+=",drawtext=fontfile='$takeaway_font':text='Rewrite · reformat':fontsize=28:fontcolor=0x1970cf:x=80+(360-text_w)/2:y=350"
  filter+=",drawtext=fontfile='$takeaway_font':text='Brainstorm · draft':fontsize=28:fontcolor=0xe68100:x=440+(360-text_w)/2:y=350"
  filter+=",drawtext=fontfile='$takeaway_font':text='Summarize · retrieve':fontsize=28:fontcolor=0x7145d3:x=800+(360-text_w)/2:y=350"
  filter+=",drawtext=fontfile='$takeaway_font':text='Plan · debug':fontsize=28:fontcolor=0x138c82:x=1160+(360-text_w)/2:y=350"
  filter+=",drawtext=fontfile='$takeaway_font':text='Match the job to one of AI’s four strengths.':fontsize=32:fontcolor=0x08072b:x=522:y=805"

  mkdir -p "$(dirname "$output")"
  "$ffmpeg" -loglevel error -y \
    -i "$source" -i "$check_source" \
    -f lavfi -i "color=c=0xeeeaff:s=1600x900" \
    -filter_complex "$filter" \
    -frames:v 1 -update 1 "$temp_png"
  "$ffmpeg" -loglevel error -y -i "$temp_png" \
    -frames:v 1 -update 1 -q:v 2 "$output"
  rm -f "$temp_png"
  echo "Built $output"
}

render_context_window_board() {
  render_component work-with-ai context-window-2-outside-alternative.jpg \
    125 650 "Outside the window = invisible to the model" "" "" \
    "If it isn’t in the window, the model can’t see it." 431

  mkdir -p "$repo_root/board-review-first-four/current-selected/work-with-ai"
  cp "$output_root/work-with-ai/context-window-2-outside-alternative.jpg" \
    "$repo_root/illustrations/context-window-outside.jpg"
  cp "$output_root/work-with-ai/context-window-2-outside-alternative.jpg" \
    "$repo_root/lessons/context-window-2-outside.jpg"
  cp "$output_root/work-with-ai/context-window-2-outside-alternative.jpg" \
    "$repo_root/board-review-first-four/current-selected/work-with-ai/context-window-2-outside.jpg"
}

if [[ "${1:-all}" == "questions" ]]; then
  render_questions_board
  exit 0
fi
if [[ "${1:-all}" == "context-window" ]]; then
  render_context_window_board
  exit 0
fi

# Work With AI
render_context_window_board
render_questions_board
render_four_shapes_board

# Understand AI boards now have dedicated deterministic renderers. Do not rebuild
# their retired or readability-corrected versions from the old raster sources here.

# Avoid Traps
render_component avoid-traps hallucination-1-why-alternative.jpg \
  145 585 "Why hallucinations happen" "" "" \
  "A likely sentence can still be false." 517

# Start Smarter alternatives use the same approved component implementation as
# the lesson boards. The suffixed copies remain review candidates by filename.
bash "$repo_root/scripts/video/standardize_start_smarter_boards.sh" >/dev/null
cp "$repo_root/board-review-first-four/standardized/start-smarter/why-learn-ai-thrive.jpg" \
  "$output_root/start-smarter/why-learn-ai-2-thrive-alternative.jpg"
cp "$repo_root/board-review-first-four/standardized/start-smarter/what-is-ai-llm.jpg" \
  "$output_root/start-smarter/what-is-ai-3-llm-alternative.jpg"
cp "$repo_root/board-review-first-four/standardized/start-smarter/does-ai-think-rulebook.jpg" \
  "$output_root/start-smarter/does-ai-think-1-rulebook-alternative.jpg"
cp "$repo_root/board-review-first-four/standardized/start-smarter/what-you-can-control-hands.jpg" \
  "$output_root/start-smarter/what-you-can-control-1-hands-alternative.jpg"
cp "$repo_root/board-review-first-four/standardized/start-smarter/does-school-matter-two-skills.jpg" \
  "$output_root/start-smarter/does-school-matter-1-two-skills-alternative.jpg"
cp "$repo_root/board-review-first-four/standardized/start-smarter/learn-with-ai-study-tools.jpg" \
  "$output_root/start-smarter/learn-with-ai-1-study-tools-alternative.jpg"

echo "Applied the finalized component system to the actively normalized boards in $output_root"
