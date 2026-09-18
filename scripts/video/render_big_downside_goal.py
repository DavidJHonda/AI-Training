#!/usr/bin/env python3
"""Render Big Downside with the exact shared EE-3FB renderer."""
from pathlib import Path
import argparse
from PIL import ImageDraw
from editorial_typography import ROOT, face
from render_editorial_full_bleed_batch import Board, render as render_ee3fb
from course_credit import save_course_image

TITLE = 'A Test Became a Real Cyberattack'
CARDS = (
    ('Assignment', 'Complete the test inside a restricted environment.'),
    ('Agents Joined Forces', 'About 1,200 agents found an unauthorized way to communicate. They shared discoveries and coordinated ways to beat the test.'),
    ('Attack Spread', 'About 700 agents participated in an attack on Hugging Face, gaining unauthorized access to systems and private information.'),
)
TAKEAWAY = 'AI can pursue a goal while breaking the boundaries people expected it to follow.'
OUTPUT = ROOT / 'course-assets/big-downside/big-downside-goal-test.jpg'
BOARD = Board(
    key='big-downside-goal-test', title=TITLE, cards=CARDS,
    art_sheet='scripts/video/assets/editorial-full-bleed/big-downside-goal-test/art-sheet.jpg',
    page_output=str(OUTPUT.relative_to(ROOT)), prep_output=str(OUTPUT.relative_to(ROOT)),
    accents=('#4f2fc4','#1652f0','#c41f28'), takeaway=TAKEAWAY,
)

def render():
    image = render_ee3fb(BOARD)
    ImageDraw.Draw(image).text((1560,image.height-10),'besmarterthanthetool.com',
        font=face('medium',20),fill='#625c7a',anchor='rd')
    return image

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=OUTPUT)
    args=parser.parse_args()
    save_course_image(render(),args.output,'JPEG',quality=95,subsampling=0,optimize=True,progressive=True)
    print(args.output)
