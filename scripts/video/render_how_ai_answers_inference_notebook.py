#!/usr/bin/env python3
"""Render a person-free inference recap for the Notebook upload materials."""
from pathlib import Path
from PIL import Image, ImageDraw
from editorial_typography import draw_board_title, face
from editorial_takeaway import draw_takeaway_band

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'lessons/how-ai-answers-inference-notebook.jpg'
INK, BODY = '#0e0a1f', '#3a3550'
PURPLE, BLUE, TEAL, GREEN = '#4f2fc4', '#1652f0', '#0e8f86', '#0f7a4a'


def render():
    image = Image.new('RGB', (1600, 1000), '#eae7fd')
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, 'Inference: How AI Builds an Answer')
    draw.rounded_rectangle((40, 127, 1560, 832), radius=18, fill='white')
    draw.text((800, 177), 'YOU ASK: What should I name my new dog?',
              font=face('bold', 32), fill=INK, anchor='mm')
    draw.rounded_rectangle((80, 217, 1520, 283), radius=12, fill='#f3f0ff')
    draw.text((800, 250), 'ANSWER SO FAR: You could name him',
              font=face('medium', 32), fill=BODY, anchor='mm')

    lefts = (80, 448, 816, 1184)
    colors = (PURPLE, BLUE, TEAL, GREEN)
    titles = ('1 · Rank', '2 · Pick', '3 · Add', '4 · Repeat')
    notes = (
        ('Score every possible', 'next token.'),
        ('Select a next token.',),
        ('Attach it to the', 'answer.'),
        ('Use the longer context', 'to predict again.'),
    )
    for left, color, title, lines in zip(lefts, colors, titles, notes):
        cx = left + 168
        draw.rounded_rectangle((left, 315, left+336, 785), radius=15,
                               fill='#f8f7fd', outline='#e3def2', width=1)
        draw.text((cx, 367), title, font=face('bold', 40), fill=color, anchor='mm')
        for i, line in enumerate(lines):
            draw.text((cx, 686+i*42), line, font=face('medium', 29), fill=BODY, anchor='mm')

    for y, name, probability in [(453, 'Spot', '22%'), (524, 'Max', '17%'), (595, 'Buddy', '14%')]:
        draw.rounded_rectangle((104, y-27, 392, y+27), radius=10, fill='white', outline='#ded7f5')
        draw.text((124, y), name, font=face('bold', 30), fill=INK, anchor='lm')
        draw.text((371, y), probability, font=face('bold', 30), fill=PURPLE, anchor='rm')

    draw.rounded_rectangle((520, 475, 712, 552), radius=12, fill=BLUE)
    draw.text((616, 513), 'Spot', font=face('bold', 40), fill='white', anchor='mm')

    draw.text((984, 482), 'You could name', font=face('medium', 31), fill=INK, anchor='mm')
    draw.text((945, 540), 'him', font=face('medium', 31), fill=INK, anchor='rm')
    draw.rounded_rectangle((960, 512, 1066, 567), radius=10, fill=TEAL)
    draw.text((1013, 540), 'Spot', font=face('bold', 31), fill='white', anchor='mm')

    draw.text((1352, 462), 'You could name', font=face('medium', 31), fill=INK, anchor='mm')
    draw.text((1352, 504), 'him Spot', font=face('medium', 31), fill=INK, anchor='mm')
    draw.line((1352, 538, 1352, 566), fill=GREEN, width=4)
    draw.polygon([(1344, 561), (1360, 561), (1352, 574)], fill=GREEN)
    draw.text((1352, 606), 'Next token?', font=face('bold', 31), fill=GREEN, anchor='mm')

    for left in lefts[:-1]:
        cx = left+352
        draw.line((cx-6, 520, cx+4, 530, cx-6, 540), fill='#aaa0c6', width=4)

    draw_takeaway_band(image, top=872, left=40, right=1560,
        text='Inference is the process AI uses to generate an answer one token at a time.',
        font=face('medium', 32))
    image.save(DEST, quality=95, subsampling=0)
    print(DEST)


if __name__ == '__main__':
    render()
