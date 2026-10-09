#!/usr/bin/env python3
"""Render the Big Downside guardrails board with the shared EE-3FB renderer."""
from pathlib import Path
import argparse
from PIL import ImageDraw
from editorial_typography import ROOT, face
from render_editorial_full_bleed_batch import Board, render as render_ee3fb
from course_credit import save_course_image

OUTPUT = ROOT / 'course-assets/big-downside/big-downside-safety-guardrails.jpg'
BOARD = Board(
    key='big-downside-guardrails', title='Layers of Protection',
    cards=(
        ('Safety Training', 'During training, teach the model to avoid harmful responses and refuse dangerous requests.'),
        ('Screen for Harm', 'Use guardrails to detect and block risky requests and harmful answers.'),
        ('Limit What AI Can Do', 'Restrict its tools and permissions. Require human approval for important tasks, such as sending money or deleting files.'),
    ),
    art_sheet='scripts/video/assets/editorial-full-bleed/big-downside-guardrails/art-sheet.png',
    page_output=str(OUTPUT.relative_to(ROOT)), prep_output=str(OUTPUT.relative_to(ROOT)),
    accents=('#4f2fc4', '#1652f0', '#0e8f86'),
    takeaway='Each layer helps. No layer catches everything.',
)


def render():
    image = render_ee3fb(BOARD, wrap_titles=True)
    ImageDraw.Draw(image).text((1560, image.height-10), 'besmarterthanthetool.com',
                              font=face('medium',20), fill='#625c7a', anchor='rd')
    return image


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    save_course_image(render(), args.output, 'JPEG', quality=95, subsampling=0, optimize=True, progressive=True)
    print(args.output)
