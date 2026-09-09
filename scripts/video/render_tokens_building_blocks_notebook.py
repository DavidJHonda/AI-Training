#!/usr/bin/env python3
"""Render a person-free Notebook source board; preserve the illustrated lesson asset."""
from pathlib import Path
from PIL import Image, ImageDraw
from editorial_typography import draw_board_title, draw_inner_title, face
from editorial_takeaway import draw_takeaway_band

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'lessons/tokens-building-blocks-notebook.jpg'
INK, MUTED = '#0e0a1f', '#716b84'
PURPLE, BLUE, TEAL = '#4f2fc4', '#1652f0', '#0e8f86'


def render():
    image = Image.new('RGB', (1600, 900), '#eae7fd')
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, 'Building Blocks for Language')
    draw.rounded_rectangle((40, 127, 1560, 732), radius=18, fill='white')

    draw.text((350, 200), 'WORD', font=face('heavy', 25), fill=MUTED, anchor='mm')
    draw.text((1130, 200), 'TOKENS', font=face('heavy', 25), fill=MUTED, anchor='mm')
    draw.rounded_rectangle((100, 250, 600, 364), radius=16, fill='#f3f0ff')
    draw.text((350, 304), 'unbelievable', font=face('bold', 46), fill=INK, anchor='mm')
    draw.line((640, 307, 755, 307), fill=MUTED, width=5)
    draw.polygon([(752, 294), (773, 307), (752, 320)], fill=MUTED)
    for text, x0, x1, color, pale in [
        ('un', 820, 1000, PURPLE, '#ede9fc'),
        ('belie', 1025, 1235, BLUE, '#e8efff'),
        ('vable', 1260, 1480, TEAL, '#e7f4f2'),
    ]:
        draw.rounded_rectangle((x0, 250, x1, 364), radius=16, fill=pale, outline=color, width=2)
        draw.text(((x0+x1)/2, 304), text, font=face('bold', 46), fill=color, anchor='mm')

    draw_inner_title(draw, (800, 465), 'The same piece in different words', fill=INK, anchor='mm')
    font = face('bold', 40)
    for center, suffix in zip((310, 800, 1290), ('believable', 'matchable', 'usual')):
        prefix_width = draw.textlength('un', font=font)
        total = prefix_width + draw.textlength(suffix, font=font)
        left = center-total/2
        # Only the shared token is boxed; suffixes may contain several tokens.
        draw.rounded_rectangle((left-9, 553, left+prefix_width+7, 619), radius=10,
                               fill='#ede9fc', outline=PURPLE, width=2)
        draw.text((left, 584), 'un', font=font, fill=PURPLE, anchor='lm')
        draw.text((left+prefix_width+11, 584), suffix, font=font, fill=INK, anchor='lm')
    draw.text((800, 676), 'The remaining letters may span multiple tokens.',
              font=face('medium', 27), fill=MUTED, anchor='mm')
    draw_takeaway_band(image, top=772, left=40, right=1560,
                       text='Reuse the pieces. Build more words.', font=face('medium', 32))
    image.save(DEST, quality=95, subsampling=0)
    print(DEST)


if __name__ == '__main__':
    render()
