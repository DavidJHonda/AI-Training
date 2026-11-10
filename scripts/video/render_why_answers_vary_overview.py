#!/usr/bin/env python3
"""Render Why Answers Vary in canonical EE-3FB, preserving its approved copy."""
from pathlib import Path

from PIL import Image, ImageDraw

from course_credit import save_course_image
from editorial_typography import face
from render_editorial_full_bleed_batch import Board, render as render_board

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = 'course-assets/why-answers-vary/why-answers-vary-overview.jpg'
ART = 'scripts/video/assets/editorial-full-bleed/why-answers-vary-overview/art-sheet.png'
BOARD = Board(
    key='why-answers-vary-overview',
    title='Why Answers Vary',
    cards=(
        ('Model & Thinking', 'The model you use and how much thinking it does can change the answer.'),
        ('What AI Receives', 'Your prompt and the other information available to AI can change its answer.'),
        ('AI’s Choices', 'Behind the scenes, AI uses techniques that give different tokens a chance to be selected.'),
    ),
    art_sheet=ART,
    page_output=OUTPUT,
    prep_output=OUTPUT,
    accents=('#1652f0', '#0e8f86', '#4f2fc4'),
)


def render():
    with Image.open(ROOT / ART) as source:
        sheet = source.convert('RGB')
    # The generated sheet stacks the three purpose-built landscape scenes.
    # Boundaries follow the native blue/teal/purple backgrounds, not equal thirds.
    edges = [0, round(sheet.height * 0.3635), round(sheet.height * 0.683), sheet.height]
    panels = [sheet.crop((0, edges[i], sheet.width, edges[i + 1])) for i in range(3)]
    image = render_board(BOARD, art_panels=panels)
    ImageDraw.Draw(image).text((1560, image.height - 10), 'besmarterthanthetool.com',
                              font=face('medium', 20), fill='#625c7a', anchor='rd')
    save_course_image(image, ROOT / OUTPUT, 'JPEG', quality=95, subsampling=0,
                      optimize=True, progressive=True)
    print(f'{OUTPUT}: {image.width}x{image.height}')


if __name__ == '__main__':
    render()
