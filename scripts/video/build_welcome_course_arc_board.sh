#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
art="$repo_root/board-review-first-four/assets/welcome-course-arc-art.png"
check_source="$repo_root/board-review-first-four/pre-standardization/start-smarter/does-ai-think-rulebook.jpg"
output="$repo_root/board-review-first-four/alternatives/start-smarter/welcome-course-arc-alternative.jpg"
temp_png="${output%.jpg}.tmp.png"
ffmpeg="$repo_root/scripts/video/ffmpeg.sh"
title_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Heavy.otf"
body_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Medium.otf"
takeaway_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Demi.otf"

for required in "$art" "$check_source" "$title_font" "$body_font" "$takeaway_font"; do
  if [[ ! -f "$required" ]]; then
    echo "Missing required file: $required" >&2
    exit 2
  fi
done

mkdir -p "$(dirname "$output")"

filter="color=c=white:s=1440x564,format=rgba[panelcolor]"
filter+=";color=c=black:s=1440x564,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[panelmask]"
filter+=";[panelcolor][panelmask]alphamerge[panel]"
filter+=";[0:v]crop=334:520:0:210,setsar=1,scale=250:285:force_original_aspect_ratio=decrease,pad=260:295:(ow-iw)/2:(oh-ih)/2:color=white[art1]"
filter+=";[0:v]crop=300:520:380:210,setsar=1,scale=250:285:force_original_aspect_ratio=decrease,pad=260:295:(ow-iw)/2:(oh-ih)/2:color=white[art2]"
filter+=";[0:v]crop=334:520:668:210,setsar=1,scale=250:285:force_original_aspect_ratio=decrease,pad=260:295:(ow-iw)/2:(oh-ih)/2:color=white[art3]"
filter+=";[0:v]crop=334:520:1002:210,setsar=1,scale=250:285:force_original_aspect_ratio=decrease,pad=260:295:(ow-iw)/2:(oh-ih)/2:color=white[art4]"
filter+=";[0:v]crop=334:520:1336:210,setsar=1,scale=250:285:force_original_aspect_ratio=decrease,pad=260:295:(ow-iw)/2:(oh-ih)/2:color=white[art5]"
filter+=";color=c=0x6547e8:s=60x60,format=rgba[markercolor]"
filter+=";color=c=black:s=60x60,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),29),255,0)'[markermask]"
filter+=";[markercolor][markermask]alphamerge,split=5[m1][m2][m3][m4][m5]"
filter+=";color=c=0xffe9ab:s=1440x84,format=rgba[barcolor]"
filter+=";color=c=black:s=1440x84,format=gray,geq=lum='if(lte(hypot(max(abs(X-W/2)-(W/2-16),0),max(abs(Y-H/2)-(H/2-16),0)),16),255,0)'[barmask]"
filter+=";[barcolor][barmask]alphamerge[bar]"
filter+=";[1:v]crop=86:86:340:731,format=rgba[iconcolor]"
filter+=";color=c=black:s=86x86,format=gray,geq=lum='if(lte(hypot(X-W/2,Y-H/2),42),255,0)'[iconmask]"
filter+=";[iconcolor][iconmask]alphamerge,scale=52:52[icon]"
filter+=";[2:v][panel]overlay=80:172[s1]"
filter+=";[s1]drawbox=x=224:y=216:w=1152:h=8:color=0xd6cef9:t=fill[s2]"
filter+=";[s2][m1]overlay=194:190[s3];[s3][m2]overlay=482:190[s4];[s4][m3]overlay=770:190[s5];[s5][m4]overlay=1058:190[s6];[s6][m5]overlay=1346:190[s7]"
filter+=";[s7][art1]overlay=94:402[s8];[s8][art2]overlay=382:402[s9];[s9][art3]overlay=670:402[s10];[s10][art4]overlay=958:402[s11];[s11][art5]overlay=1246:402[s12]"
filter+=";[s12][bar]overlay=80:776[s13];[s13][icon]overlay=440:792[s14]"
filter+=";[s14]drawtext=fontfile='$title_font':text='Here’s your path.':fontsize=44:fontcolor=0x08072b:x=(w-text_w)/2:y=40+(100-text_h)/2-2"
filter+=",drawtext=fontfile='$title_font':text='1':fontsize=24:fontcolor=white:x=224-text_w/2:y=202"
filter+=",drawtext=fontfile='$title_font':text='2':fontsize=24:fontcolor=white:x=512-text_w/2:y=202"
filter+=",drawtext=fontfile='$title_font':text='3':fontsize=24:fontcolor=white:x=800-text_w/2:y=202"
filter+=",drawtext=fontfile='$title_font':text='4':fontsize=24:fontcolor=white:x=1088-text_w/2:y=202"
filter+=",drawtext=fontfile='$title_font':text='5':fontsize=24:fontcolor=white:x=1376-text_w/2:y=202"
filter+=",drawtext=fontfile='$title_font':text='Work':fontsize=28:fontcolor=0x08072b:x=80+(288-text_w)/2:y=266"
filter+=",drawtext=fontfile='$title_font':text='Understand':fontsize=28:fontcolor=0x08072b:x=368+(288-text_w)/2:y=266"
filter+=",drawtext=fontfile='$title_font':text='Avoid':fontsize=28:fontcolor=0x08072b:x=656+(288-text_w)/2:y=266"
filter+=",drawtext=fontfile='$title_font':text='Embrace':fontsize=28:fontcolor=0x08072b:x=944+(288-text_w)/2:y=266"
filter+=",drawtext=fontfile='$title_font':text='Build':fontsize=28:fontcolor=0x08072b:x=1232+(288-text_w)/2:y=266"
filter+=",drawtext=fontfile='$body_font':text='Use AI':fontsize=23:fontcolor=0x302c4b:x=80+(288-text_w)/2:y=316"
filter+=",drawtext=fontfile='$body_font':text='effectively.':fontsize=23:fontcolor=0x302c4b:x=80+(288-text_w)/2:y=346"
filter+=",drawtext=fontfile='$body_font':text='See how':fontsize=23:fontcolor=0x302c4b:x=368+(288-text_w)/2:y=316"
filter+=",drawtext=fontfile='$body_font':text='it works.':fontsize=23:fontcolor=0x302c4b:x=368+(288-text_w)/2:y=346"
filter+=",drawtext=fontfile='$body_font':text='Recognize':fontsize=23:fontcolor=0x302c4b:x=656+(288-text_w)/2:y=316"
filter+=",drawtext=fontfile='$body_font':text='the traps.':fontsize=23:fontcolor=0x302c4b:x=656+(288-text_w)/2:y=346"
filter+=",drawtext=fontfile='$body_font':text='Prepare for':fontsize=23:fontcolor=0x302c4b:x=944+(288-text_w)/2:y=316"
filter+=",drawtext=fontfile='$body_font':text='what changes.':fontsize=23:fontcolor=0x302c4b:x=944+(288-text_w)/2:y=346"
filter+=",drawtext=fontfile='$body_font':text='Turn AI into':fontsize=23:fontcolor=0x302c4b:x=1232+(288-text_w)/2:y=316"
filter+=",drawtext=fontfile='$body_font':text='an advantage.':fontsize=23:fontcolor=0x302c4b:x=1232+(288-text_w)/2:y=346"
filter+=",drawtext=fontfile='$takeaway_font':text='Start with the tool. Finish with what you can do.':fontsize=32:fontcolor=0x08072b:x=508:y=805"

"$ffmpeg" -loglevel error -y \
  -i "$art" -i "$check_source" \
  -f lavfi -i "color=c=0xeeeaff:s=1600x900" \
  -filter_complex "$filter" \
  -frames:v 1 -update 1 "$temp_png"

"$ffmpeg" -loglevel error -y -i "$temp_png" \
  -frames:v 1 -update 1 -q:v 2 "$output"
rm -f "$temp_png"

echo "Built $output"
