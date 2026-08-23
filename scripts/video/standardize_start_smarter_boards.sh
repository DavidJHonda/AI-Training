#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
source_root="$repo_root/board-review-first-four/pre-standardization/start-smarter"
output_root="$repo_root/board-review-first-four/standardized/start-smarter"
ffmpeg="$repo_root/scripts/video/ffmpeg.sh"
title_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Heavy.otf"
card_title_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Bold.otf"
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

  filter="color=c=white:s=1520x748,format=rgba[panelcolor]"
  filter+=";color=c=black:s=1520x748,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask]"
  filter+=";[panelcolor][panelmask]alphamerge[panel]"
  filter+=";color=c=0x6546d7:s=64x64,format=rgba[badgecolor]"
  filter+=";color=c=black:s=64x64,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),31),255,0)'[badgemask]"
  filter+=";[badgecolor][badgemask]alphamerge,split=3[badge1][badge2][badge3]"
  filter+=";[0:v]crop=420:280:88:225,scale=390:260:force_original_aspect_ratio=decrease,pad=390:270:(ow-iw)/2:(oh-ih)/2:color=white[art1]"
  filter+=";[0:v]crop=410:280:595:225,scale=390:260:force_original_aspect_ratio=decrease,pad=390:270:(ow-iw)/2:(oh-ih)/2:color=white[art2]"
  filter+=";[0:v]crop=410:270:1090:235,scale=390:260:force_original_aspect_ratio=decrease,pad=390:270:(ow-iw)/2:(oh-ih)/2:color=white[art3]"
  filter+=";[2:v][panel]overlay=80:172[s1]"
  filter+=";[s1][badge1]overlay=288:206[s2];[s2][badge2]overlay=768:206[s3];[s3][badge3]overlay=1248:206[s4]"
  filter+=";[s4][art1]overlay=125:550[s5];[s5][art2]overlay=605:550[s6];[s6][art3]overlay=1085:550[s7]"
  filter+=";[s7]drawbox=x=560:y=204:w=2:h=624:color=0xe4e0f3:t=fill,drawbox=x=1040:y=204:w=2:h=624:color=0xe4e0f3:t=fill"
  filter+=",drawbox=x=120:y=526:w=400:h=2:color=0xc9c3e8:t=fill,drawbox=x=600:y=526:w=400:h=2:color=0xc9c3e8:t=fill,drawbox=x=1080:y=526:w=400:h=2:color=0xc9c3e8:t=fill"
  filter+=",drawtext=fontfile='$title_font':text='Why you’ll thrive in the AI future':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40+(100-text_h)/2-2"
  filter+=",drawtext=fontfile='$title_font':text='1':fontsize=30:fontcolor=white:x=320-text_w/2:y=206+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='2':fontsize=30:fontcolor=white:x=800-text_w/2:y=206+(64-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='3':fontsize=30:fontcolor=white:x=1280-text_w/2:y=206+(64-text_h)/2"
  filter+=",drawtext=fontfile='$card_title_font':text='THIS IS YOUR TIME':fontsize=32:fontcolor=0x152b7a:x=80+(480-text_w)/2:y=286"
  filter+=",drawtext=fontfile='$card_title_font':text='YOU’LL MOVE FASTER':fontsize=32:fontcolor=0x152b7a:x=560+(480-text_w)/2:y=286"
  filter+=",drawtext=fontfile='$card_title_font':text='NOTHING TO UNLEARN':fontsize=32:fontcolor=0x152b7a:x=1040+(480-text_w)/2:y=286"
  filter+=",drawtext=fontfile='$subtitle_font':text='Nobody has a twenty-year':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=334"
  filter+=",drawtext=fontfile='$subtitle_font':text='head start. That almost':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=370"
  filter+=",drawtext=fontfile='$subtitle_font':text='never happens with':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=406"
  filter+=",drawtext=fontfile='$subtitle_font':text='something this big. You’re':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=442"
  filter+=",drawtext=fontfile='$subtitle_font':text='showing up right as it lands.':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=478"
  filter+=",drawtext=fontfile='$subtitle_font':text='AI collapses years of':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=334"
  filter+=",drawtext=fontfile='$subtitle_font':text='paying dues, learning the':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=370"
  filter+=",drawtext=fontfile='$subtitle_font':text='trade, and climbing the':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=406"
  filter+=",drawtext=fontfile='$subtitle_font':text='ladder. What took a decade':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=442"
  filter+=",drawtext=fontfile='$subtitle_font':text='is within reach now.':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=478"
  filter+=",drawtext=fontfile='$subtitle_font':text='Others must undo the':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=334"
  filter+=",drawtext=fontfile='$subtitle_font':text='workflow that made them':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=370"
  filter+=",drawtext=fontfile='$subtitle_font':text='fast. You skip all of that':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=406"
  filter+=",drawtext=fontfile='$subtitle_font':text='and learn the new way':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=442"
  filter+=",drawtext=fontfile='$subtitle_font':text='from the start.':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=478"

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
  filter+=",drawtext=fontfile='$title_font':text='What’s an LLM?':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40+(100-text_h)/2-2"
  filter+=",drawtext=fontfile='$card_title_font':text='Large':fontsize=32:fontcolor=0x152b7a:x=80+(480-text_w)/2:y=282"
  filter+=",drawtext=fontfile='$card_title_font':text='Language':fontsize=32:fontcolor=0x152b7a:x=560+(480-text_w)/2:y=282"
  filter+=",drawtext=fontfile='$card_title_font':text='Model':fontsize=32:fontcolor=0x152b7a:x=1040+(480-text_w)/2:y=282"
  filter+=",drawtext=fontfile='$subtitle_font':text='Trained on huge amounts':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=332"
  filter+=",drawtext=fontfile='$subtitle_font':text='of text and code.':fontsize=30:fontcolor=0x08072b:x=80+(480-text_w)/2:y=370"
  filter+=",drawtext=fontfile='$subtitle_font':text='Reads, writes, summarizes,':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=332"
  filter+=",drawtext=fontfile='$subtitle_font':text='translates, and explains.':fontsize=30:fontcolor=0x08072b:x=560+(480-text_w)/2:y=370"
  filter+=",drawtext=fontfile='$subtitle_font':text='Predicts likely output':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=332"
  filter+=",drawtext=fontfile='$subtitle_font':text='from learned patterns.':fontsize=30:fontcolor=0x08072b:x=1040+(480-text_w)/2:y=370"
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
  cp "$output" "$repo_root/board-review-first-four/alternatives/start-smarter/what-is-ai-3-llm-alternative.jpg"
  cp "$output" "$repo_root/board-review-first-four/alternatives/start-smarter/what-is-ai-llm.jpg"
  cp "$output" "$repo_root/illustrations/what-is-ai-llm.jpg"
  cp "$output" "$repo_root/lessons/what-is-ai-3-llm.jpg"
  echo "Built $output"
}

render_school_board() {
  local source="$source_root/does-school-matter-two-skills.jpg"
  local output="$output_root/does-school-matter-two-skills.jpg"
  local temp_png="${output%.jpg}.tmp.png"
  local filter

  # The white stage is centered inside the 1600 px canvas: 40 px on each side.
  filter="color=c=white:s=1520x688,format=rgba[panelcolor]"
  filter+=";color=c=black:s=1520x688,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask]"
  filter+=";[panelcolor][panelmask]alphamerge[panel]"
  filter+=";color=c=0x6546d7:s=48x48,format=rgba[badge1color]"
  filter+=";color=c=0xc6c3d7:s=48x48,format=rgba[badge2color]"
  filter+=";color=c=0x2f6df6:s=48x48,format=rgba[badge3color]"
  filter+=";color=c=black:s=48x48,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),23),255,0)',split=3[badge1mask][badge2mask][badge3mask]"
  filter+=";[badge1color][badge1mask]alphamerge[badge1]"
  filter+=";[badge2color][badge2mask]alphamerge[badge2]"
  filter+=";[badge3color][badge3mask]alphamerge[badge3]"
  filter+=";[0:v]crop=455:225:65:480,scale=400:210:force_original_aspect_ratio=decrease,pad=400:210:(ow-iw)/2:(oh-ih)/2:color=white[art1]"
  filter+=";[0:v]crop=350:190:620:490,scale=400:210:force_original_aspect_ratio=decrease,pad=400:210:(ow-iw)/2:(oh-ih)/2:color=white[art2]"
  filter+=";[0:v]crop=445:240:1070:465,scale=400:210:force_original_aspect_ratio=decrease,pad=400:210:(ow-iw)/2:(oh-ih)/2:color=white[art3]"
  filter+=";[2:v][panel]overlay=40:124[s1]"
  filter+=";[s1][badge1]overlay=276:154[s2];[s2][badge2]overlay=776:154[s3];[s3][badge3]overlay=1276:154[s4]"
  filter+=";[s4][art1]overlay=100:580[s5];[s5][art2]overlay=600:580[s6];[s6][art3]overlay=1100:580[s7]"
  filter+=";[s7]drawbox=x=550:y=148:w=2:h=642:color=0xe4e0f3:t=fill,drawbox=x=1050:y=148:w=2:h=642:color=0xe4e0f3:t=fill"
  filter+=",drawbox=x=70:y=548:w=460:h=2:color=0xc9c3e8:t=fill,drawbox=x=570:y=548:w=460:h=2:color=0xc9c3e8:t=fill,drawbox=x=1070:y=548:w=460:h=2:color=0xc9c3e8:t=fill"
  filter+=",drawtext=fontfile='$arrow_font':text='→':fontsize=40:fontcolor=0x6546d7:x=532:y=486,drawtext=fontfile='$arrow_font':text='→':fontsize=40:fontcolor=0x2f6df6:x=1032:y=486"
  filter+=",drawtext=fontfile='$title_font':text='1':fontsize=22:fontcolor=white:x=300-text_w/2:y=154+(48-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='AI':fontsize=18:fontcolor=0x4b4960:x=800-text_w/2:y=154+(48-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='2':fontsize=22:fontcolor=white:x=1300-text_w/2:y=154+(48-text_h)/2"
  filter+=",drawtext=fontfile='$title_font':text='Same AI. Different value.':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=14+(100-text_h)/2-2"
  filter+=",drawtext=fontfile='$card_title_font':text='Ask the Right Question':fontsize=30:fontcolor=0x152b7a:x=50+(500-text_w)/2:y=224"
  filter+=",drawtext=fontfile='$card_title_font':text='AI Answer':fontsize=30:fontcolor=0x152b7a:x=550+(500-text_w)/2:y=224"
  filter+=",drawtext=fontfile='$card_title_font':text='Make the Answer Better':fontsize=30:fontcolor=0x152b7a:x=1050+(510-text_w)/2:y=224"
  filter+=",drawtext=fontfile='$subtitle_font':text='What you know shapes what':fontsize=28:fontcolor=0x343149:x=50+(500-text_w)/2:y=292"
  filter+=",drawtext=fontfile='$subtitle_font':text='you ask.':fontsize=28:fontcolor=0x343149:x=50+(500-text_w)/2:y=328"
  filter+=",drawtext=fontfile='$subtitle_font':text='A sharper question gets a':fontsize=28:fontcolor=0x343149:x=50+(500-text_w)/2:y=380"
  filter+=",drawtext=fontfile='$subtitle_font':text='better answer before AI does':fontsize=28:fontcolor=0x343149:x=50+(500-text_w)/2:y=416"
  filter+=",drawtext=fontfile='$subtitle_font':text='anything special.':fontsize=28:fontcolor=0x343149:x=50+(500-text_w)/2:y=452"
  filter+=",drawtext=fontfile='$subtitle_font':text='Similar questions get':fontsize=28:fontcolor=0x343149:x=550+(500-text_w)/2:y=292"
  filter+=",drawtext=fontfile='$subtitle_font':text='similar answers.':fontsize=28:fontcolor=0x343149:x=550+(500-text_w)/2:y=328"
  filter+=",drawtext=fontfile='$subtitle_font':text='The answer is a starting point, not':fontsize=28:fontcolor=0x343149:x=550+(500-text_w)/2:y=380"
  filter+=",drawtext=fontfile='$subtitle_font':text='the finish.':fontsize=28:fontcolor=0x343149:x=550+(500-text_w)/2:y=416"
  filter+=",drawtext=fontfile='$subtitle_font':text='Read it. Judge whether it’s right.':fontsize=28:fontcolor=0x343149:x=1050+(510-text_w)/2:y=292"
  filter+=",drawtext=fontfile='$subtitle_font':text='Push back and improve it.':fontsize=28:fontcolor=0x343149:x=1050+(510-text_w)/2:y=344"
  filter+=",drawtext=fontfile='$subtitle_font':text='AI doesn’t have the knowledge':fontsize=28:fontcolor=0x343149:x=1050+(510-text_w)/2:y=396"
  filter+=",drawtext=fontfile='$subtitle_font':text='you have.':fontsize=28:fontcolor=0x343149:x=1050+(510-text_w)/2:y=432"

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
  # The old raster contained essential 18–22 px copy. Preserve the code-native
  # readability rebuild; regenerate it with render_readability_gap_boards.py.
  local output="$output_root/learn-with-ai-study-tools.jpg"
  cp "$repo_root/illustrations/learn-with-ai-study-tools.jpg" "$output"
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
