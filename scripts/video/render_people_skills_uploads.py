#!/usr/bin/env python3
"""Render text-only Notebook stand-ins; face-bearing page boards are post-only.

Build from text/layout primitives, never copy artwork into upload variants.
Keep canonical pixel dimensions and teaching text for replacement during editing.
"""
from PIL import Image, ImageDraw

from editorial_typography import draw_board_title, face
from render_editorial_full_bleed_batch import Board, render, wrap
from render_people_skills_cards import ROOT, SPECS


def save(image, name, canonical):
    with Image.open(ROOT / 'course-assets/people-skills' / canonical) as page:
        assert image.size == page.size, (name, image.size, page.size)
    output = ROOT / 'gemini-notebook/people-skills/assets' / name
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, quality=95, subsampling=0)
    print(f'{output.relative_to(ROOT)}: {image.width}x{image.height}')


def main():
    lesson = (ROOT / 'lessons/people-skills.md').read_text()
    dialogue = 'Maya, we didn’t hear the rest of your idea. Do you want to finish?'
    banner = 'Show her that what she has to say matters.'
    assert dialogue in lesson and banner in lesson
    scene = Image.new('RGB', (1600, 1200), 'white')
    draw = ImageDraw.Draw(scene)
    draw.rounded_rectangle((0, 0, 1599, 1199), radius=22, fill='#eae7fd')
    draw_board_title(draw, 'Your Next Move')
    draw.rounded_rectangle((34, 119, 1566, 1043), radius=18, fill='white')
    font = face('bold', 44)
    for i, line in enumerate(wrap(draw, dialogue, font, 500)):
        draw.text((630, 210 + i * 60), line, font=font, fill='#0e0a1f')
    draw.rounded_rectangle((34, 1074, 1566, 1165), radius=16, fill='#ffe4a2')
    font = face('bold', 36)
    width = draw.textlength(banner, font=font)
    draw.text(((1600 - width) / 2, 1097), banner, font=font, fill='#0e0a1f')
    save(scene, 'people-skills-next-move-faceless.jpg', 'people-skills-why-people-matter.jpg')

    spec = SPECS['four-ways']
    assert all(body in lesson for _, body in spec['cards'])
    board = Board(key='people-skills-upload', title=spec['title'], cards=spec['cards'],
                  art_sheet='', page_output='', prep_output='', accents=spec['accents'])
    image = render(board, art_panels=[Image.new('RGB', (744, 339), 'white') for _ in range(4)],
                   preserve_art_colors=True)
    save(image, 'people-skills-four-ways-faceless.jpg', 'people-skills-four-ways.jpg')


if __name__ == '__main__':
    main()
