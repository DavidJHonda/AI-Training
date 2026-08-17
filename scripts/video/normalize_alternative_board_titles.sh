#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
background="$repo_root/board-review-first-four/assets/board-background.png"
source_root="$repo_root/board-review-first-four/.pre-board-spec"
output_root="$repo_root/board-review-first-four/alternatives"
title_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Heavy.otf"
subtitle_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Medium.otf"
ffmpeg="$repo_root/scripts/video/ffmpeg.sh"

for required in "$background" "$title_font" "$subtitle_font"; do
  if [[ ! -f "$required" ]]; then
    echo "Missing required file: $required" >&2
    exit 2
  fi
done

if [[ ! -d "$source_root" ]]; then
  echo "Missing source snapshot: $source_root" >&2
  exit 2
fi

escape_drawtext() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//:/\\:}"
  value="${value//\'/\\\'}"
  value="${value//=/\\=}"
  printf '%s' "$value"
}

render_board() {
  local section="$1"
  local filename="$2"
  local old_body_top="$3"
  local band_height="$4"
  local title_line_1="$5"
  local title_line_2="${6:-}"
  local subtitle="${7:-}"
  local source="$source_root/$section/$filename"
  local output="$output_root/$section/$filename"
  local title_filter

  title_line_1="$(escape_drawtext "$title_line_1")"
  title_line_2="$(escape_drawtext "$title_line_2")"
  subtitle="$(escape_drawtext "$subtitle")"

  if [[ -n "$subtitle" ]]; then
    title_filter="drawtext=fontfile='$title_font':text='$title_line_1':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40"
    title_filter+=",drawtext=fontfile='$subtitle_font':text='$subtitle':fontsize=26:fontcolor=0x655f7c:x=(w-text_w)/2:y=93"
  elif [[ -n "$title_line_2" ]]; then
    title_filter="drawtext=fontfile='$title_font':text='$title_line_1':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=34"
    title_filter+=",drawtext=fontfile='$title_font':text='$title_line_2':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=84"
  else
    title_filter="drawtext=fontfile='$title_font':text='$title_line_1':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=(120-text_h)/2-2"
  fi

  mkdir -p "$(dirname "$output")"
  "$ffmpeg" -loglevel error -y \
    -i "$source" -i "$background" \
    -filter_complex "[1:v]scale=1600:900,crop=1600:900[canvas];[0:v]crop=1600:$((900-old_body_top)):0:$old_body_top[body];[canvas][body]overlay=0:$band_height[board];[board]$title_filter" \
    -frames:v 1 -update 1 -q:v 2 "$output"
}

apply_hierarchy() {
  local section="$1"
  local filename="$2"
  local filter="$3"
  local output="$output_root/$section/$filename"
  local temp_png="${output%.jpg}.hierarchy.tmp.png"

  "$ffmpeg" -loglevel error -y -i "$output" \
    -vf "format=rgb24,$filter" \
    -frames:v 1 -update 1 "$temp_png"
  "$ffmpeg" -loglevel error -y -i "$temp_png" \
    -frames:v 1 -update 1 -q:v 2 "$output"
  rm -f "$temp_png"
}

# One-line title: 120 px band. Title plus subline or a two-line title: 160 px.
# Titles remain 44 px; wrapping changes the band height, never the type size.
render_board start-smarter does-ai-think-1-rulebook-alternative.jpg 155 120 "Matching the pattern is not understanding it"
render_board start-smarter does-school-matter-1-two-skills-alternative.jpg 180 160 "Same AI. Different value." "" "Two skills grow with what you know."
render_board start-smarter learn-with-ai-1-study-tools-alternative.jpg 125 120 "Which study tool for the job?"
render_board start-smarter what-you-can-control-1-hands-alternative.jpg 125 120 "What’s actually in your hands?"
render_board start-smarter why-learn-ai-2-thrive-alternative.jpg 165 120 "Why you’ll thrive in the AI future"

render_board work-with-ai context-window-2-outside-alternative.jpg 125 120 "Outside the window = invisible to the model"
render_board work-with-ai questions-matter-1-answers-cheap-alternative.jpg 145 120 "How answers got cheap"
render_board work-with-ai where-ai-works-best-four-shapes-alternative.jpg 255 160 "AI is strongest when the job" "has one of four shapes."

render_board understand-ai embeddings-taste-profile-alternative.jpg 125 120 "Meaning becomes a row of numbers"
render_board understand-ai layers-2-inside-alternative.jpg 145 120 "What happens inside every layer"
render_board understand-ai training-map-alternative.jpg 145 120 "How a language model gets trained"

render_board avoid-traps document-trap-1-chunks-alternative.jpg 125 120 "What happens when AI searches a long document"
render_board avoid-traps hallucination-1-why-alternative.jpg 125 120 "Why hallucinations happen"
render_board avoid-traps training-bias-1-mechanisms-alternative.jpg 145 120 "How training bias gets in"

# Reduce the few interior headings and callouts that still competed with the
# board title. Card headings top out at 28 px; supporting copy is 24–26 px.
apply_hierarchy start-smarter why-learn-ai-2-thrive-alternative.jpg \
  "drawbox=x=90:y=510:w=420:h=64:color=white:t=fill,drawbox=x=590:y=510:w=420:h=64:color=white:t=fill,drawbox=x=1090:y=510:w=420:h=64:color=white:t=fill,drawbox=x=120:y=590:w=360:h=100:color=white:t=fill,drawbox=x=620:y=590:w=360:h=100:color=white:t=fill,drawbox=x=1120:y=590:w=360:h=100:color=white:t=fill,drawtext=fontfile='$title_font':text='THIS IS YOUR TIME':fontsize=28:fontcolor=0x08072b:x=90+(420-text_w)/2:y=528,drawtext=fontfile='$title_font':text='YOU’LL MOVE FASTER':fontsize=28:fontcolor=0x08072b:x=590+(420-text_w)/2:y=528,drawtext=fontfile='$title_font':text='NOTHING TO UNLEARN':fontsize=28:fontcolor=0x08072b:x=1090+(420-text_w)/2:y=528,drawtext=fontfile='$subtitle_font':text='Nobody has a':fontsize=24:fontcolor=0x08072b:x=120+(360-text_w)/2:y=612,drawtext=fontfile='$subtitle_font':text='twenty-year head start.':fontsize=24:fontcolor=0x08072b:x=120+(360-text_w)/2:y=642,drawtext=fontfile='$subtitle_font':text='What took a decade':fontsize=24:fontcolor=0x08072b:x=620+(360-text_w)/2:y=612,drawtext=fontfile='$subtitle_font':text='is within reach now.':fontsize=24:fontcolor=0x08072b:x=620+(360-text_w)/2:y=642,drawtext=fontfile='$subtitle_font':text='You’re learning the':fontsize=24:fontcolor=0x08072b:x=1120+(360-text_w)/2:y=612,drawtext=fontfile='$subtitle_font':text='new workflow first.':fontsize=24:fontcolor=0x08072b:x=1120+(360-text_w)/2:y=642"

apply_hierarchy start-smarter does-school-matter-1-two-skills-alternative.jpg \
  "drawbox=x=110:y=270:w=370:h=95:color=white:t=fill,drawbox=x=640:y=310:w=320:h=52:color=white:t=fill,drawbox=x=1090:y=270:w=400:h=95:color=white:t=fill,drawbox=x=140:y=390:w=320:h=80:color=white:t=fill,drawbox=x=670:y=390:w=260:h=80:color=white:t=fill,drawbox=x=1100:y=390:w=380:h=70:color=white:t=fill,drawbox=x=350:y=762:w=900:h=70:color=0xeeebfc:t=fill,drawtext=fontfile='$title_font':text='ASK THE RIGHT':fontsize=28:fontcolor=0x08072b:x=110+(370-text_w)/2:y=286,drawtext=fontfile='$title_font':text='QUESTION':fontsize=28:fontcolor=0x08072b:x=110+(370-text_w)/2:y=322,drawtext=fontfile='$title_font':text='AI ANSWER':fontsize=28:fontcolor=0x08072b:x=640+(320-text_w)/2:y=322,drawtext=fontfile='$title_font':text='MAKE THE ANSWER':fontsize=28:fontcolor=0x08072b:x=1090+(400-text_w)/2:y=286,drawtext=fontfile='$title_font':text='BETTER':fontsize=28:fontcolor=0x08072b:x=1090+(400-text_w)/2:y=322,drawtext=fontfile='$subtitle_font':text='What you know shapes':fontsize=24:fontcolor=0x08072b:x=140+(320-text_w)/2:y=401,drawtext=fontfile='$subtitle_font':text='what you ask.':fontsize=24:fontcolor=0x08072b:x=140+(320-text_w)/2:y=431,drawtext=fontfile='$subtitle_font':text='A starting point,':fontsize=24:fontcolor=0x08072b:x=670+(260-text_w)/2:y=401,drawtext=fontfile='$subtitle_font':text='not the finish.':fontsize=24:fontcolor=0x08072b:x=670+(260-text_w)/2:y=431,drawtext=fontfile='$subtitle_font':text='Judge it. Push back. Improve it.':fontsize=24:fontcolor=0x08072b:x=1100+(380-text_w)/2:y=411,drawtext=fontfile='$title_font':text='The tool brings answers. You bring judgment.':fontsize=30:fontcolor=0x08072b:x=350+(900-text_w)/2:y=782"

apply_hierarchy work-with-ai questions-matter-1-answers-cheap-alternative.jpg \
  "drawbox=x=80:y=150:w=410:h=44:color=white:t=fill,drawbox=x=625:y=150:w=390:h=44:color=white:t=fill,drawbox=x=1120:y=150:w=390:h=44:color=white:t=fill,drawbox=x=80:y=190:w=410:h=70:color=white:t=fill,drawbox=x=625:y=190:w=390:h=70:color=white:t=fill,drawbox=x=1120:y=190:w=390:h=70:color=white:t=fill,drawbox=x=175:y=625:w=320:h=72:color=white:t=fill,drawbox=x=695:y=625:w=300:h=72:color=white:t=fill,drawbox=x=1225:y=625:w=300:h=72:color=white:t=fill,drawbox=x=280:y=760:w=1200:h=72:color=white:t=fill,drawtext=fontfile='$subtitle_font':text='PRE-INTERNET':fontsize=24:fontcolor=0x6a4c3a:x=80+(410-text_w)/2:y=162,drawtext=fontfile='$subtitle_font':text='THE INTERNET':fontsize=24:fontcolor=0x1563c7:x=625+(390-text_w)/2:y=162,drawtext=fontfile='$subtitle_font':text='NOW':fontsize=24:fontcolor=0x7040c3:x=1120+(390-text_w)/2:y=162,drawtext=fontfile='$title_font':text='THE LIBRARY':fontsize=28:fontcolor=0x3d2718:x=80+(410-text_w)/2:y=210,drawtext=fontfile='$title_font':text='SEARCH':fontsize=28:fontcolor=0x08072b:x=625+(390-text_w)/2:y=210,drawtext=fontfile='$title_font':text='AI':fontsize=28:fontcolor=0x08072b:x=1120+(390-text_w)/2:y=210,drawtext=fontfile='$title_font':text='Half a Saturday':fontsize=26:fontcolor=0x3d2718:x=175+(320-text_w)/2:y=646,drawtext=fontfile='$title_font':text='An hour or two':fontsize=26:fontcolor=0x08072b:x=695+(300-text_w)/2:y=646,drawtext=fontfile='$title_font':text='Seconds':fontsize=26:fontcolor=0x08072b:x=1225+(300-text_w)/2:y=646,drawtext=fontfile='$title_font':text='The cost of finding an answer collapsed.':fontsize=28:fontcolor=0x08072b:x=280+(1200-text_w)/2:y=780"

apply_hierarchy work-with-ai where-ai-works-best-four-shapes-alternative.jpg \
  "drawbox=x=70:y=435:w=330:h=78:color=white:t=fill,drawbox=x=455:y=435:w=320:h=78:color=white:t=fill,drawbox=x=840:y=435:w=320:h=78:color=white:t=fill,drawbox=x=1225:y=435:w=300:h=78:color=white:t=fill,drawbox=x=80:y=535:w=310:h=90:color=white:t=fill,drawbox=x=465:y=535:w=310:h=90:color=white:t=fill,drawbox=x=850:y=535:w=310:h=90:color=white:t=fill,drawbox=x=1215:y=535:w=320:h=90:color=white:t=fill,drawtext=fontfile='$title_font':text='TRANSFORM':fontsize=28:fontcolor=0x08072b:x=70+(330-text_w)/2:y=457,drawtext=fontfile='$title_font':text='GENERATE':fontsize=28:fontcolor=0x08072b:x=455+(320-text_w)/2:y=457,drawtext=fontfile='$title_font':text='COMPRESS':fontsize=28:fontcolor=0x08072b:x=840+(320-text_w)/2:y=457,drawtext=fontfile='$title_font':text='REASON':fontsize=28:fontcolor=0x08072b:x=1225+(300-text_w)/2:y=457,drawtext=fontfile='$subtitle_font':text='Same meaning,':fontsize=24:fontcolor=0x1970cf:x=80+(310-text_w)/2:y=553,drawtext=fontfile='$subtitle_font':text='new shape.':fontsize=24:fontcolor=0x1970cf:x=80+(310-text_w)/2:y=583,drawtext=fontfile='$subtitle_font':text='Ten versions':fontsize=24:fontcolor=0xe68100:x=465+(310-text_w)/2:y=553,drawtext=fontfile='$subtitle_font':text='in seconds.':fontsize=24:fontcolor=0xe68100:x=465+(310-text_w)/2:y=583,drawtext=fontfile='$subtitle_font':text='Find the signal':fontsize=24:fontcolor=0x7145d3:x=850+(310-text_w)/2:y=553,drawtext=fontfile='$subtitle_font':text='in long material.':fontsize=24:fontcolor=0x7145d3:x=850+(310-text_w)/2:y=583,drawtext=fontfile='$subtitle_font':text='Work through facts':fontsize=24:fontcolor=0x138c82:x=1215+(320-text_w)/2:y=553,drawtext=fontfile='$subtitle_font':text='and constraints.':fontsize=24:fontcolor=0x138c82:x=1215+(320-text_w)/2:y=583"

apply_hierarchy avoid-traps hallucination-1-why-alternative.jpg \
  "drawbox=x=380:y=200:w=320:h=58:color=white:t=fill,drawbox=x=1090:y=200:w=360:h=58:color=white:t=fill,drawbox=x=390:y=260:w=330:h=96:color=white:t=fill,drawbox=x=1110:y=260:w=350:h=96:color=white:t=fill,drawbox=x=420:y=580:w=760:h=108:color=white:t=fill,drawbox=x=540:y=798:w=650:h=55:color=white:t=fill,drawtext=fontfile='$title_font':text='TRAINING':fontsize=28:fontcolor=0x7542bd:x=390:y=216,drawtext=fontfile='$title_font':text='GENERATION':fontsize=28:fontcolor=0x245fce:x=1110:y=216,drawtext=fontfile='$subtitle_font':text='Learned patterns,':fontsize=24:fontcolor=0x08072b:x=390:y=276,drawtext=fontfile='$subtitle_font':text='not facts.':fontsize=24:fontcolor=0x08072b:x=390:y=306,drawtext=fontfile='$subtitle_font':text='Picks each next token':fontsize=24:fontcolor=0x08072b:x=1110:y=276,drawtext=fontfile='$subtitle_font':text='by probability.':fontsize=24:fontcolor=0x08072b:x=1110:y=306,drawtext=fontfile='$title_font':text='PROBABLE':fontsize=36:fontcolor=0x7542bd:x=560:y=611,drawtext=fontfile='$title_font':text='≠':fontsize=36:fontcolor=0x08072b:x=790:y=611,drawtext=fontfile='$title_font':text='TRUE':fontsize=36:fontcolor=0xf05a00:x=850:y=611,drawtext=fontfile='$title_font':text='A likely sentence can still be false.':fontsize=26:fontcolor=0x08072b:x=540+(650-text_w)/2:y=812"

# The first five Start Smarter alternatives above are preserved as historical
# source-normalization steps, then replaced by the approved full component system.
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

echo "Applied the shared title and hierarchy system to 14 boards in $output_root"
