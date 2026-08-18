#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
source_image="$repo_root/board-review-first-four/alternatives/understand-ai/embeddings-meaning-as-numbers-photo-base.png"
review_output="$repo_root/board-review-first-four/alternatives/understand-ai/embeddings-meaning-as-numbers-photo-alternative.jpg"
lesson_output="$repo_root/illustrations/embeddings-1.jpg"
ffmpeg="$repo_root/scripts/video/ffmpeg.sh"
heavy_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Heavy.otf"
demi_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Demi.otf"
medium_font="/Users/davidobrien/Library/Fonts/AvenirNextforINTUIT-Medium.otf"

for required in "$source_image" "$heavy_font" "$demi_font" "$medium_font"; do
  if [[ ! -f "$required" ]]; then
    echo "Missing required file: $required" >&2
    exit 2
  fi
done

filter="drawbox=x=400:y=570:w=2:h=380:color=0xb98a45:t=fill"
filter+=",drawtext=fontfile='$heavy_font':text='MEANING AS NUMBERS':fontsize=44:fontcolor=0xf5ead4:x=(w-text_w)/2:y=34"
filter+=",drawtext=fontfile='$heavy_font':text='DIMENSION':fontsize=20:fontcolor=0xd9c29d:x=100+(300-text_w)/2:y=535"
filter+=",drawtext=fontfile='$heavy_font':text='COKE':fontsize=21:fontcolor=0xf07982:x=400+(438-text_w)/2:y=526"
filter+=",drawtext=fontfile='$medium_font':text='TOKEN ID 24317':fontsize=16:fontcolor=0xe7d9c2:x=400+(438-text_w)/2:y=550"
filter+=",drawtext=fontfile='$heavy_font':text='COFFEE':fontsize=21:fontcolor=0xd5aa7c:x=838+(600-text_w)/2:y=526"
filter+=",drawtext=fontfile='$medium_font':text='TOKEN ID 51820':fontsize=16:fontcolor=0xe7d9c2:x=838+(600-text_w)/2:y=550"

labels=(SWEET BITTER FIZZ HEAT CAFFEINE DARK)
coke_values=(9 1 10 2 3 8)
coffee_values=(1 9 0 9 8 10)
row_y=(588 650 711 771 832 895)

for index in "${!labels[@]}"; do
  filter+=",drawtext=fontfile='$demi_font':text='${labels[$index]}':fontsize=21:fontcolor=0xe4d2b5:x=138:y=${row_y[$index]}"
  filter+=",drawtext=fontfile='$heavy_font':text='${coke_values[$index]}':fontsize=27:fontcolor=0xf07982:x=400+(438-text_w)/2:y=$((row_y[$index]-3))"
  filter+=",drawtext=fontfile='$heavy_font':text='${coffee_values[$index]}':fontsize=27:fontcolor=0xd5aa7c:x=838+(600-text_w)/2:y=$((row_y[$index]-3))"
done

mkdir -p "$(dirname "$review_output")"
"$ffmpeg" -loglevel error -y -i "$source_image" \
  -vf "$filter" -frames:v 1 -update 1 -q:v 2 "$review_output"
cp "$review_output" "$lesson_output"

echo "Built $review_output"
echo "Updated $lesson_output"
