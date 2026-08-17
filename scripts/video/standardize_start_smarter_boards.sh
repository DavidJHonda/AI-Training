#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
source_root="$repo_root/board-review-first-four/pre-standardization/start-smarter"
output_root="$repo_root/board-review-first-four/standardized/start-smarter"
ffmpeg="$repo_root/scripts/video/ffmpeg.sh"
title_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Heavy.otf"
subtitle_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Medium.otf"
takeaway_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Demi.otf"
arrow_font="/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

mkdir -p "$output_root"

escape_drawtext() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//:/\\:}"
  value="${value//\'/\\\'}"
  value="${value//=/\\=}"
  printf '%s' "$value"
}

render_board() {
  local input_name="$1"
  local output_name="$2"
  local crop_y="$3"
  local crop_h="$4"
  local title_band_h="$5"
  local title="$6"
  local subtitle="$7"
  local takeaway="$8"
  local lockup_x="$9"
  local crop_x="${10:-0}"
  local crop_w="${11:-1600}"
  local text_x=$((lockup_x+68))
  local body_h=564
  local input
  local output="$output_root/$output_name"
  local temp_png="${output%.jpg}.tmp.png"
  local title_filter

  if [[ "$input_name" = /* ]]; then
    input="$input_name"
  else
    input="$source_root/$input_name"
  fi

  title="$(escape_drawtext "$title")"
  subtitle="$(escape_drawtext "$subtitle")"
  takeaway="$(escape_drawtext "$takeaway")"

  if [[ -n "$subtitle" ]]; then
    title_filter="drawtext=fontfile='$title_font':text='$title':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40"
    title_filter+=",drawtext=fontfile='$subtitle_font':text='$subtitle':fontsize=26:fontcolor=0x655f7c:x=(w-text_w)/2:y=104"
  else
    title_filter="drawtext=fontfile='$title_font':text='$title':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40+(100-text_h)/2-2"
  fi

  "$ffmpeg" -loglevel error -y \
    -i "$input" \
    -f lavfi -i "color=c=0xeeeaff:s=1600x900" \
    -i "$source_root/does-ai-think-rulebook.jpg" \
    -filter_complex "[0:v]crop=${crop_w}:${crop_h}:${crop_x}:${crop_y},scale=1408:532:force_original_aspect_ratio=decrease,pad=1408:532:(ow-iw)/2:(oh-ih)/2:color=white[body];color=c=white:s=1440x564,format=rgba[panelcolor];color=c=black:s=1440x564,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask];[panelcolor][panelmask]alphamerge[panel];color=c=0xffe9ab:s=1440x84,format=rgba[barcolor];color=c=black:s=1440x84,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[barmask];[barcolor][barmask]alphamerge[bar];[2:v]crop=86:86:340:731,format=rgba[iconcolor];color=c=black:s=86x86,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),42),255,0)'[iconmask];[iconcolor][iconmask]alphamerge,scale=52:52[icon];[1:v][panel]overlay=80:172[stage];[stage][body]overlay=96:188[withbody];[withbody][bar]overlay=80:776[withbar];[withbar][icon]overlay=${lockup_x}:792[withicon];[withicon]$title_filter,drawtext=fontfile='$takeaway_font':text='$takeaway':fontsize=32:fontcolor=0x08072b:x=${text_x}:y=805" \
    -frames:v 1 -update 1 "$temp_png"

  "$ffmpeg" -loglevel error -y -i "$temp_png" \
    -frames:v 1 -update 1 -q:v 2 "$output"
  rm -f "$temp_png"
  echo "Built $output"
}

render_why_board() {
  local source="$source_root/why-learn-ai-thrive.jpg"
  local output="$output_root/why-learn-ai-thrive.jpg"
  local temp_png="${output%.jpg}.tmp.png"
  local filter

  filter="color=c=white:s=1440x564,format=rgba[panelcolor]"
  filter+=";color=c=black:s=1440x564,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask]"
  filter+=";[panelcolor][panelmask]alphamerge[panel]"
  filter+=";color=c=0x6546d7:s=64x64,format=rgba[badgecolor]"
  filter+=";color=c=black:s=64x64,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),31),255,0)'[badgemask]"
  filter+=";[badgecolor][badgemask]alphamerge,split=3[badge1][badge2][badge3]"
  filter+=";[0:v]crop=420:280:88:225,scale=390:210:force_original_aspect_ratio=decrease,pad=390:210:(ow-iw)/2:(oh-ih)/2:color=white[art1]"
  filter+=";[0:v]crop=410:280:595:225,scale=390:210:force_original_aspect_ratio=decrease,pad=390:210:(ow-iw)/2:(oh-ih)/2:color=white[art2]"
  filter+=";[0:v]crop=410:270:1090:235,scale=390:210:force_original_aspect_ratio=decrease,pad=390:210:(ow-iw)/2:(oh-ih)/2:color=white[art3]"
  filter+=";color=c=0xffe9ab:s=1440x84,format=rgba[barcolor]"
  filter+=";color=c=black:s=1440x84,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[barmask]"
  filter+=";[barcolor][barmask]alphamerge[bar]"
  filter+=";[1:v]crop=86:86:340:731,format=rgba[iconcolor]"
  filter+=";color=c=black:s=86x86,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),42),255,0)'[iconmask]"
  filter+=";[iconcolor][iconmask]alphamerge,scale=52:52[icon]"
  filter+=";[2:v][panel]overlay=80:172[s1]"
  filter+=";[s1][badge1]overlay=288:206[s2];[s2][badge2]overlay=768:206[s3];[s3][badge3]overlay=1248:206[s4]"
  filter+=";[s4][art1]overlay=125:502[s5];[s5][art2]overlay=605:502[s6];[s6][art3]overlay=1085:502[s7]"
  filter+=";[s7][bar]overlay=80:776[s8];[s8][icon]overlay=447:792[s9]"
  filter+=";[s9]drawbox=x=560:y=204:w=2:h=500:color=0xe4e0f3:t=fill,drawbox=x=1040:y=204:w=2:h=500:color=0xe4e0f3:t=fill"
  filter+=",drawbox=x=120:y=474:w=400:h=2:color=0xc9c3e8:t=fill,drawbox=x=600:y=474:w=400:h=2:color=0xc9c3e8:t=fill,drawbox=x=1080:y=474:w=400:h=2:color=0xc9c3e8:t=fill"
  filter+=",drawtext=fontfile='$title_font':text='Why you’ll thrive in the AI future':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40"
  filter+=",drawtext=fontfile='$subtitle_font':text='AI is new for everyone. This is your big advantage.':fontsize=26:fontcolor=0x655f7c:x=(w-text_w)/2:y=104"
  filter+=",drawtext=fontfile='$title_font':text='1':fontsize=28:fontcolor=white:x=320-text_w/2:y=206+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='2':fontsize=28:fontcolor=white:x=800-text_w/2:y=206+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='3':fontsize=28:fontcolor=white:x=1280-text_w/2:y=206+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='THIS IS YOUR TIME':fontsize=28:fontcolor=0x08072b:x=80+(480-text_w)/2:y=286"
  filter+=",drawtext=fontfile='$title_font':text='YOU’LL MOVE FASTER':fontsize=28:fontcolor=0x08072b:x=560+(480-text_w)/2:y=286"
  filter+=",drawtext=fontfile='$title_font':text='NOTHING TO UNLEARN':fontsize=28:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=286"
  filter+=",drawtext=fontfile='$subtitle_font':text='Nobody has a twenty-year head start.':fontsize=22:fontcolor=0x08072b:x=80+(480-text_w)/2:y=334"
  filter+=",drawtext=fontfile='$subtitle_font':text='That almost never happens with':fontsize=22:fontcolor=0x08072b:x=80+(480-text_w)/2:y=364"
  filter+=",drawtext=fontfile='$subtitle_font':text='something this big. You’re showing':fontsize=22:fontcolor=0x08072b:x=80+(480-text_w)/2:y=394"
  filter+=",drawtext=fontfile='$subtitle_font':text='up right as it lands.':fontsize=22:fontcolor=0x08072b:x=80+(480-text_w)/2:y=424"
  filter+=",drawtext=fontfile='$subtitle_font':text='AI collapses years of paying dues,':fontsize=22:fontcolor=0x08072b:x=560+(480-text_w)/2:y=334"
  filter+=",drawtext=fontfile='$subtitle_font':text='learning the trade, and climbing':fontsize=22:fontcolor=0x08072b:x=560+(480-text_w)/2:y=364"
  filter+=",drawtext=fontfile='$subtitle_font':text='the ladder. What took a decade':fontsize=22:fontcolor=0x08072b:x=560+(480-text_w)/2:y=394"
  filter+=",drawtext=fontfile='$subtitle_font':text='is within reach now.':fontsize=22:fontcolor=0x08072b:x=560+(480-text_w)/2:y=424"
  filter+=",drawtext=fontfile='$subtitle_font':text='Others must undo the workflow':fontsize=22:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=334"
  filter+=",drawtext=fontfile='$subtitle_font':text='that made them fast. You skip':fontsize=22:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=364"
  filter+=",drawtext=fontfile='$subtitle_font':text='all of that and learn the new way':fontsize=22:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=394"
  filter+=",drawtext=fontfile='$subtitle_font':text='from the start.':fontsize=22:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=424"
  filter+=",drawtext=fontfile='$takeaway_font':text='This is your time to learn the new workflow.':fontsize=32:fontcolor=0x08072b:x=515:y=805"

  "$ffmpeg" -loglevel error -y \
    -i "$source" \
    -i "$source_root/does-ai-think-rulebook.jpg" \
    -f lavfi -i "color=c=0xeeeaff:s=1600x900" \
    -filter_complex "$filter" \
    -frames:v 1 -update 1 "$temp_png"

  "$ffmpeg" -loglevel error -y -i "$temp_png" \
    -frames:v 1 -update 1 -q:v 2 "$output"
  rm -f "$temp_png"
  cp "$output" "$repo_root/board-review-first-four/alternatives/start-smarter/why-learn-ai-2-thrive-alternative.jpg"
  cp "$output" "$repo_root/board-review-first-four/alternatives/start-smarter/why-learn-ai-thrive.jpg"
  cp "$output" "$repo_root/illustrations/why-learn-ai-thrive.jpg"
  cp "$output" "$repo_root/lessons/why-learn-ai-2-thrive.jpg"
  echo "Built $output"
}

render_llm_board() {
  local source="$source_root/what-is-ai-llm.jpg"
  local base="$repo_root/board-review-first-four/assets/what-is-ai-llm-visual-base.png"
  local output="$output_root/what-is-ai-llm.jpg"
  local temp_png="${output%.jpg}.tmp.png"
  local filter

  filter="color=c=white:s=1440x564,format=rgba[panelcolor]"
  filter+=";color=c=black:s=1440x564,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask]"
  filter+=";[panelcolor][panelmask]alphamerge[panel]"
  filter+=";[1:v]crop=470:410:75:310,scale=390:270:force_original_aspect_ratio=decrease,pad=390:270:(ow-iw)/2:(oh-ih)/2:color=white[art1]"
  filter+=";[1:v]crop=460:410:610:310,scale=390:270:force_original_aspect_ratio=decrease,pad=390:270:(ow-iw)/2:(oh-ih)/2:color=white[art2]"
  filter+=";[1:v]crop=480:410:1120:310,scale=390:270:force_original_aspect_ratio=decrease,pad=390:270:(ow-iw)/2:(oh-ih)/2:color=white[art3]"
  filter+=";[0:v]crop=82:64:82:225,scale=64:50[badge1]"
  filter+=";[0:v]crop=72:64:590:225,scale=64:50[badge2]"
  filter+=";[0:v]crop=76:64:1086:225,scale=64:50[badge3]"
  filter+=";color=c=0xffe9ab:s=1440x84,format=rgba[barcolor]"
  filter+=";color=c=black:s=1440x84,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[barmask]"
  filter+=";[barcolor][barmask]alphamerge[bar]"
  filter+=";[2:v]crop=86:86:340:731,format=rgba[iconcolor]"
  filter+=";color=c=black:s=86x86,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),42),255,0)'[iconmask]"
  filter+=";[iconcolor][iconmask]alphamerge,scale=52:52[icon]"
  filter+=";[3:v][panel]overlay=80:172[s3]"
  filter+=";[s3][art1]overlay=125:430[s4];[s4][art2]overlay=605:430[s5];[s5][art3]overlay=1085:430[s6]"
  filter+=";[s6][badge1]overlay=288:206[s7];[s7][badge2]overlay=768:206[s8];[s8][badge3]overlay=1248:206[s9]"
  filter+=";[s9][bar]overlay=80:776[s10];[s10][icon]overlay=453:792[s11]"
  filter+=";[s11]drawbox=x=560:y=204:w=2:h=500:color=0xe4e0f3:t=fill,drawbox=x=1040:y=204:w=2:h=500:color=0xe4e0f3:t=fill,drawbox=x=120:y=408:w=400:h=2:color=0xc9c3e8:t=fill,drawbox=x=600:y=408:w=400:h=2:color=0xc9c3e8:t=fill,drawbox=x=1080:y=408:w=400:h=2:color=0xc9c3e8:t=fill"
  filter+=",drawtext=fontfile='$title_font':text='What’s an LLM?':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=56"
  filter+=",drawtext=fontfile='$subtitle_font':text='The engine under the app.':fontsize=26:fontcolor=0x655f7c:x=(w-text_w)/2:y=100"
  filter+=",drawtext=fontfile='$title_font':text='Large':fontsize=28:fontcolor=0x3b82f6:x=80+(480-text_w)/2:y=286"
  filter+=",drawtext=fontfile='$title_font':text='Language':fontsize=28:fontcolor=0x10b981:x=560+(480-text_w)/2:y=286"
  filter+=",drawtext=fontfile='$title_font':text='Model':fontsize=28:fontcolor=0xf59e0b:x=1040+(480-text_w)/2:y=286"
  filter+=",drawtext=fontfile='$subtitle_font':text='Trained on huge amounts':fontsize=24:fontcolor=0x08072b:x=80+(480-text_w)/2:y=338"
  filter+=",drawtext=fontfile='$subtitle_font':text='of text and code.':fontsize=24:fontcolor=0x08072b:x=80+(480-text_w)/2:y=368"
  filter+=",drawtext=fontfile='$subtitle_font':text='Reads, writes, summarizes,':fontsize=24:fontcolor=0x08072b:x=560+(480-text_w)/2:y=338"
  filter+=",drawtext=fontfile='$subtitle_font':text='translates, and explains.':fontsize=24:fontcolor=0x08072b:x=560+(480-text_w)/2:y=368"
  filter+=",drawtext=fontfile='$subtitle_font':text='Predicts likely output':fontsize=24:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=338"
  filter+=",drawtext=fontfile='$subtitle_font':text='from learned patterns.':fontsize=24:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=368"
  filter+=",drawtext=fontfile='$takeaway_font':text='ChatGPT is the app. The LLM is the engine.':fontsize=32:fontcolor=0x08072b:x=521:y=805"

  "$ffmpeg" -loglevel error -y \
    -i "$source" \
    -i "$base" \
    -i "$source_root/does-ai-think-rulebook.jpg" \
    -f lavfi -i "color=c=0xeeeaff:s=1600x900" \
    -filter_complex "$filter" \
    -frames:v 1 -update 1 "$temp_png"

  "$ffmpeg" -loglevel error -y -i "$temp_png" \
    -frames:v 1 -update 1 -q:v 2 "$output"
  rm -f "$temp_png"
  echo "Built $output"
}

render_school_board() {
  local source="$source_root/does-school-matter-two-skills.jpg"
  local output="$output_root/does-school-matter-two-skills.jpg"
  local temp_png="${output%.jpg}.tmp.png"
  local filter

  filter="color=c=white:s=1440x564,format=rgba[panelcolor]"
  filter+=";color=c=black:s=1440x564,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask]"
  filter+=";[panelcolor][panelmask]alphamerge[panel]"
  filter+=";color=c=0x6546d7:s=64x64,format=rgba[badge1color]"
  filter+=";color=c=0xc6c3d7:s=64x64,format=rgba[badge2color]"
  filter+=";color=c=0x0b66dc:s=64x64,format=rgba[badge3color]"
  filter+=";color=c=black:s=64x64,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),31),255,0)',split=3[badge1mask][badge2mask][badge3mask]"
  filter+=";[badge1color][badge1mask]alphamerge[badge1]"
  filter+=";[badge2color][badge2mask]alphamerge[badge2]"
  filter+=";[badge3color][badge3mask]alphamerge[badge3]"
  filter+=";[0:v]crop=455:225:65:480,scale=390:210:force_original_aspect_ratio=decrease,pad=390:210:(ow-iw)/2:(oh-ih)/2:color=white[art1]"
  filter+=";[0:v]crop=350:190:620:490,scale=390:210:force_original_aspect_ratio=decrease,pad=390:210:(ow-iw)/2:(oh-ih)/2:color=white[art2]"
  filter+=";[0:v]crop=445:240:1070:465,scale=390:210:force_original_aspect_ratio=decrease,pad=390:210:(ow-iw)/2:(oh-ih)/2:color=white[art3]"
  filter+=";color=c=0xffe9ab:s=1440x84,format=rgba[barcolor]"
  filter+=";color=c=black:s=1440x84,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[barmask]"
  filter+=";[barcolor][barmask]alphamerge[bar]"
  filter+=";[1:v]crop=86:86:340:731,format=rgba[iconcolor]"
  filter+=";color=c=black:s=86x86,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),42),255,0)'[iconmask]"
  filter+=";[iconcolor][iconmask]alphamerge,scale=52:52[icon]"
  filter+=";[2:v][panel]overlay=80:172[s1]"
  filter+=";[s1][badge1]overlay=288:206[s2];[s2][badge2]overlay=768:206[s3];[s3][badge3]overlay=1248:206[s4]"
  filter+=";[s4][art1]overlay=125:494[s5];[s5][art2]overlay=605:494[s6];[s6][art3]overlay=1085:494[s7]"
  filter+=";[s7][bar]overlay=80:776[s10];[s10][icon]overlay=433:792[s11]"
  filter+=";[s11]drawbox=x=560:y=204:w=2:h=500:color=0xe4e0f3:t=fill,drawbox=x=1040:y=204:w=2:h=500:color=0xe4e0f3:t=fill"
  filter+=",drawbox=x=120:y=484:w=400:h=2:color=0xc9c3e8:t=fill,drawbox=x=600:y=484:w=400:h=2:color=0xc9c3e8:t=fill,drawbox=x=1080:y=484:w=400:h=2:color=0xc9c3e8:t=fill"
  filter+=",drawtext=fontfile='$arrow_font':text='→':fontsize=64:fontcolor=0x6546d7:x=526:y=528,drawtext=fontfile='$arrow_font':text='→':fontsize=64:fontcolor=0x0b66dc:x=1006:y=528"
  filter+=",drawtext=fontfile='$title_font':text='1':fontsize=28:fontcolor=white:x=320-text_w/2:y=206+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='AI':fontsize=24:fontcolor=0x08072b:x=800-text_w/2:y=206+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='2':fontsize=28:fontcolor=white:x=1280-text_w/2:y=206+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='Same AI. Different value.':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40"
  filter+=",drawtext=fontfile='$subtitle_font':text='Two skills grow with what you know.':fontsize=26:fontcolor=0x655f7c:x=(w-text_w)/2:y=104"
  filter+=",drawtext=fontfile='$title_font':text='ASK THE RIGHT':fontsize=28:fontcolor=0x08072b:x=80+(480-text_w)/2:y=284"
  filter+=",drawtext=fontfile='$title_font':text='QUESTION':fontsize=28:fontcolor=0x08072b:x=80+(480-text_w)/2:y=318"
  filter+=",drawtext=fontfile='$title_font':text='AI ANSWER':fontsize=28:fontcolor=0x08072b:x=560+(480-text_w)/2:y=301"
  filter+=",drawtext=fontfile='$title_font':text='MAKE THE ANSWER':fontsize=28:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=284"
  filter+=",drawtext=fontfile='$title_font':text='BETTER':fontsize=28:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=318"
  filter+=",drawtext=fontfile='$subtitle_font':text='What you know shapes what you ask.':fontsize=22:fontcolor=0x08072b:x=80+(480-text_w)/2:y=354"
  filter+=",drawtext=fontfile='$subtitle_font':text='A sharper question gets a better':fontsize=22:fontcolor=0x08072b:x=80+(480-text_w)/2:y=384"
  filter+=",drawtext=fontfile='$subtitle_font':text='answer before AI does anything special.':fontsize=22:fontcolor=0x08072b:x=80+(480-text_w)/2:y=414"
  filter+=",drawtext=fontfile='$subtitle_font':text='Similar questions get similar answers.':fontsize=22:fontcolor=0x08072b:x=560+(480-text_w)/2:y=354"
  filter+=",drawtext=fontfile='$subtitle_font':text='The answer is a starting point,':fontsize=22:fontcolor=0x08072b:x=560+(480-text_w)/2:y=384"
  filter+=",drawtext=fontfile='$subtitle_font':text='not the finish.':fontsize=22:fontcolor=0x08072b:x=560+(480-text_w)/2:y=414"
  filter+=",drawtext=fontfile='$subtitle_font':text='Read it. Judge whether it’s right.':fontsize=22:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=354"
  filter+=",drawtext=fontfile='$subtitle_font':text='Push back and improve it.':fontsize=22:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=384"
  filter+=",drawtext=fontfile='$subtitle_font':text='AI cannot do that for you.':fontsize=22:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=414"
  filter+=",drawtext=fontfile='$subtitle_font':text='It does not know what you know.':fontsize=22:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=444"
  filter+=",drawtext=fontfile='$takeaway_font':text='The tool brings answers. You bring judgment.':fontsize=32:fontcolor=0x08072b:x=501:y=805"

  "$ffmpeg" -loglevel error -y \
    -i "$source" \
    -i "$source_root/does-ai-think-rulebook.jpg" \
    -f lavfi -i "color=c=0xeeeaff:s=1600x900" \
    -filter_complex "$filter" \
    -frames:v 1 -update 1 "$temp_png"

  "$ffmpeg" -loglevel error -y -i "$temp_png" \
    -frames:v 1 -update 1 -q:v 2 "$output"
  rm -f "$temp_png"
  cp "$output" "$repo_root/board-review-first-four/alternatives/start-smarter/does-school-matter-1-two-skills-alternative.jpg"
  cp "$output" "$repo_root/board-review-first-four/alternatives/start-smarter/does-school-matter-two-skills.jpg"
  cp "$output" "$repo_root/illustrations/does-school-matter-two-skills.jpg"
  cp "$output" "$repo_root/lessons/does-school-matter-1-two-skills.jpg"
  echo "Built $output"
}

render_study_board() {
  render_board \
    "learn-with-ai-study-tools.jpg" "learn-with-ai-study-tools.jpg" \
    284 573 160 \
    "Which study tool for the job?" "Do you want to learn from your materials or learn something new?" \
    "Match the tutor to its knowledge source." 470 58 1484

  local output="$output_root/learn-with-ai-study-tools.jpg"
  cp "$output" "$repo_root/board-review-first-four/alternatives/start-smarter/learn-with-ai-1-study-tools-alternative.jpg"
  cp "$output" "$repo_root/board-review-first-four/alternatives/start-smarter/learn-with-ai-study-tools.jpg"
  cp "$output" "$repo_root/illustrations/learn-with-ai-study-tools.jpg"
  cp "$output" "$repo_root/lessons/learn-with-ai-1-study-tools.jpg"
}

# Crop only the existing content stage. Titles and legacy footer treatments are
# intentionally excluded, then rebuilt with the shared component specification.
if [[ "${1:-all}" == "why" ]]; then
  render_why_board
  exit 0
fi

if [[ "${1:-all}" == "school" ]]; then
  render_school_board
  exit 0
fi

if [[ "${1:-all}" == "study" ]]; then
  render_study_board
  exit 0
fi

render_why_board

render_llm_board

render_board \
  "does-ai-think-rulebook.jpg" "does-ai-think-rulebook.jpg" \
  150 561 120 \
  "Matching the pattern is not understanding it" "" \
  "Fluent answer. No understanding required." 451 52 1498

hands_adjusted="$output_root/.what-you-can-control-adjusted.png"
"$ffmpeg" -loglevel error -y \
  -i "$source_root/what-you-can-control-hands.jpg" \
  -filter_complex "color=c=0x08072b:s=569x96,format=rgba[hcolor];color=c=black:s=569x96,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-24),0),max(abs(Y-H/2)-(H/2-24),0)),24),255,0)'[hmask];[hcolor][hmask]alphamerge[header];[0:v][header]overlay=63:138[base];[base]drawbox=x=63:y=200:w=569:h=35:color=0x08072b:t=fill,drawtext=fontfile='$title_font':text='OUT OF YOUR HANDS':fontsize=40:fontcolor=white:x=63+(569-text_w)/2:y=164" \
  -frames:v 1 -update 1 "$hands_adjusted"

render_board \
  "$hands_adjusted" "what-you-can-control-hands.jpg" \
  138 620 120 \
  "What’s actually in your hands?" "" \
  "The left side is loud. The right side is leverage." 428 63 1474
rm -f "$hands_adjusted"

render_school_board

render_study_board

echo "Standardized six Start Smarter boards in $output_root"
