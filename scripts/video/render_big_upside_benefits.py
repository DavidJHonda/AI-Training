#!/usr/bin/env python3
"""Render Big Upside's four single-scene editorial boards.

Run: .video-venv/bin/python scripts/video/render_big_upside_benefits.py
Art and built-in imagegen prompts: output/imagegen/big-upside-four-benefits-2026-11-03/.
Uses the shared editorial shell and type, with one scene beside two teaching labels.
"""
from PIL import Image, ImageDraw, ImageOps
from editorial_typography import ROOT, face, draw_board_title, draw_inner_title
from course_credit import save_course_image
ART = ROOT / 'output/imagegen/big-upside-four-benefits-2026-11-03'
ART_FILES = {'protein': 'protein-v2.png', 'cancer': 'cancer-v3.png'}
BOARDS = [
    ('protein', 'A New Scale for Science', '#4f2fc4', [
        ('Experiments', 'About 200,000 protein structures determined through decades of experiments.'),
        ('AlphaFold AI', 'Over 200 million protein structures predicted and shared free.'),
    ]),
    ('cancer', 'Helping Doctors Find Cancer', '#a9760c', [
        ('AI Flags', 'AI highlights patterns in a scan that deserve a closer look.'),
        ('Doctors Review', 'Doctors examine the scan and decide what care is needed.'),
    ]),
    ('reading', 'Reading Everyday Information', '#0e8f86', [
        ('Point the Camera', 'A phone camera brings a menu or food label into view.'),
        ('Hear the Words', 'AI reads the text aloud, making the information easier to access.'),
    ]),
    ('flood', 'Earlier Flood Warnings', '#1652f0', [
        ('Earlier Warning', 'AI helps provide flood warnings days ahead.'),
        ('Time to Act', 'People can prepare and move to safety before the water arrives.'),
    ]),
]
def wrap(draw, text, width):
    lines, line = [], ''
    for word in text.split():
        candidate = f'{line} {word}'.strip()
        if draw.textlength(candidate, font=face('medium', 29)) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    return lines + [line]
def render(key, title, accent, blocks, *, art_path=None, output=None):
    image = Image.new('RGB', (1600, 662), '#eae7fd')
    d = ImageDraw.Draw(image)
    draw_board_title(d, title)
    d.rounded_rectangle((40, 127, 1560, 622), radius=14, fill='white')
    with Image.open(art_path or ART / ART_FILES.get(key, f'{key}.png')) as source:
        art = ImageOps.fit(source.convert('RGB'), (880, 495), Image.Resampling.LANCZOS)
    mask = Image.new('L', (880, 495), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, 879, 494), radius=14, fill=255)
    md.rectangle((14, 0, 879, 494), fill=255)
    image.paste(art, (40, 127), mask)
    y = 151
    for heading, body in blocks:
        draw_inner_title(d, (960, y), heading, fill=accent)
        y += 62
        for line in wrap(d, body, 558):
            d.text((960, y), line, font=face('medium', 29), fill='#3a3550', anchor='la')
            y += 41
        y += 36
    assert y - 36 <= 597, (key, y)
    d.text((1560, 652), 'besmarterthanthetool.com', font=face('medium', 20), fill='#625c7a', anchor='rd')
    output = output or ROOT / f'course-assets/big-upside/big-upside-{key}.jpg'
    save_course_image(image, output, quality=95, subsampling=0, optimize=True)
    print(f'{output}: {image.width}x{image.height}')
    return image
if __name__ == '__main__':
    for board in BOARDS:
        render(*board)
