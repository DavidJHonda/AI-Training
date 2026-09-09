#!/usr/bin/env python3
"""Create a person-free student-ID teaching board for the Notebook upload kit."""
from pathlib import Path
from PIL import Image, ImageDraw
from editorial_typography import draw_board_title, draw_inner_title, face
from editorial_takeaway import draw_takeaway_band

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'lessons/embeddings-student-id-notebook.jpg'
INK, MUTED = '#0e0a1f', '#716b84'
PURPLE, TEAL = '#4f2fc4', '#0e8f86'


def render():
    image = Image.new('RGB', (1600, 900), '#eae7fd')
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, 'An ID Identifies You. It Doesn’t Describe You.')
    draw.rounded_rectangle((40, 127, 1560, 732), radius=18, fill='white')
    draw.line((800, 177, 800, 675), fill='#e5e0f4', width=2)
    draw_inner_title(draw, (420, 190), 'Four student IDs', fill=PURPLE, anchor='mm')
    draw_inner_title(draw, (1170, 190), 'What the IDs don’t tell you', fill=TEAL, anchor='mm')

    for value, x, y in [('1024',120,272),('2048',440,272),('3072',120,475),('4096',440,475)]:
        draw.rounded_rectangle((x,y,x+280,y+158), radius=18, fill='#f3f0ff', outline='#d9d0fb', width=2)
        draw.rounded_rectangle((x+104,y-10,x+176,y+7), radius=7, fill='#d9d0fb')
        draw.text((x+140,y+47), 'STUDENT ID', font=face('heavy',23), fill=MUTED, anchor='mm')
        draw.text((x+140,y+107), value, font=face('bold',54), fill=PURPLE, anchor='mm')

    for y, text in [(312,'Funny?'),(454,'Into hockey?'),(596,'Steals fries at lunch?')]:
        draw.ellipse((888,y-6,900,y+6), fill=TEAL)
        draw.text((930,y), text, font=face('bold',37), fill=INK, anchor='lm')
    draw_takeaway_band(image, top=772, left=40, right=1560,
                       text='His ID won’t tell you he steals fries.', font=face('medium',32))
    image.save(DEST, quality=95, subsampling=0)
    print(DEST)


if __name__ == '__main__':
    render()
