#!/usr/bin/env python3
"""Render the approved school/product-launch EE-COMPARE board."""
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from editorial_typography import face, draw_board_title, draw_inner_title
from editorial_takeaway import draw_takeaway_band

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'course-assets/does-school-matter/does-school-matter-product-launch.jpg'
ART = ROOT / 'scripts/video/assets/does-school-matter-product-launch'
ART_HEIGHT = 416
SCENARIO = ('Your boss asks you and a coworker to plan a new product launch. '
            'You ask AI similar questions and get similar plans.')
ROWS = [
    ('SALES PROJECTIONS', 'Accepts the sales projections.',
     'Using the math skills you learned in school, you work through the costs and find a more profitable pricing option.'),
    ('CUSTOMER EMAIL', 'Uses the customer email as written.',
     'Using the writing skills you developed in English class, you make the message clearer and more persuasive.'),
    ('MARKET RESEARCH', 'Accepts AI’s research without checking the sources.',
     'Using the research skills you developed in school, you compare sources and identify a more promising group of customers.'),
]
TAKEAWAY = 'The tool may be the same. What you bring to it is yours.'
BODY, LABEL = face('medium', 29), face('heavy', 20)


def wrap(draw, text, font, width):
    lines, line = [], ''
    for word in text.split():
        trial = (line + ' ' + word).strip()
        if line and draw.textlength(trial, font=font) > width:
            lines.append(line)
            line = word
        else:
            line = trial
    return lines + [line]


def paragraph(draw, text, x, y, width, color='#3a3550'):
    for line in wrap(draw, text, BODY, width):
        draw.text((x, y), line, font=BODY, fill=color)
        y += 41
    return y


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upload-variant', action='store_true',
                        help='Omit artwork and save a faceless Notebook upload board.')
    args = parser.parse_args()
    output = (ROOT / 'gemini-notebook/does-school-matter/assets/does-school-matter-product-launch-faceless.jpg'
              if args.upload_variant else OUT)
    measure = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    scenario_bottom = 128 + 26 + 28 + 12 + 41 * len(wrap(measure, SCENARIO, BODY, 1452)) + 26
    card_top = scenario_bottom + 32
    text_top = card_top + ART_HEIGHT
    row_top = text_top + 32 + 54 + 32
    heights = [28 + 12 + 41 * max(len(wrap(measure, left, BODY, 676)),
                                 len(wrap(measure, right, BODY, 676)))
               for _, left, right in ROWS]
    card_bottom = row_top + sum(heights) + 40 * (len(ROWS) - 1) + 34
    banner_top = card_bottom + 40
    height = banner_top + 88 + 40
    image = Image.new('RGB', (1600, height), '#eae7fd')
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, 'Same Tool. Different Advantage.')
    draw.rounded_rectangle((40, 128, 1560, scenario_bottom), 14, fill='white')
    draw.rectangle((40, 146, 47, scenario_bottom - 18), fill='#4f2fc4')
    draw.text((74, 154), 'THE ASSIGNMENT', font=LABEL, fill='#4f2fc4')
    paragraph(draw, SCENARIO, 74, 194, 1452)
    shadow = Image.new('RGBA', image.size)
    sd = ImageDraw.Draw(shadow)
    for x in (40, 816):
        sd.rounded_rectangle((x, card_top + 8, x + 744, card_bottom + 8), 14,
                             fill=(14, 10, 31, 18))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    image.paste(shadow, (0, 0), shadow)
    draw = ImageDraw.Draw(image)
    for x, title, accent, outline, side in [
        (40, 'Your Coworker', '#a36a17', '#ebdecf', 1),
        (816, 'You', '#4f2fc4', '#d8d1f2', 2),
    ]:
        draw.rounded_rectangle((x, card_top, x + 744, card_bottom), 14,
                               fill='white', outline=outline, width=1)
        if not args.upload_variant:
            art_path = ART / ('coworker.png' if side == 1 else 'you.png')
            with Image.open(art_path) as source:
                panel = ImageOps.fit(source.convert('RGB'), (744, ART_HEIGHT),
                                    method=Image.Resampling.LANCZOS)
            mask = Image.new('L', panel.size)
            ImageDraw.Draw(mask).rounded_rectangle((0, 0, 743, ART_HEIGHT + 14), 14, fill=255)
            image.paste(panel, (x, card_top), mask)
        draw.rounded_rectangle((x, card_top, x + 744, card_bottom), 14,
                               outline=outline, width=1)
        draw.line((x, text_top, x + 744, text_top), fill=outline, width=1)
        draw_inner_title(draw, (x + 34, text_top + 32), title, fill=accent)
        y = row_top
        for row, row_height in zip(ROWS, heights):
            draw.text((x + 34, y), row[0], font=LABEL, fill=accent)
            paragraph(draw, row[side], x + 34, y + 40, 676)
            y += row_height + 40
    draw_takeaway_band(image, top=banner_top, left=40, right=1560,
                       text=TAKEAWAY, font=face('medium', 32))
    draw.text((1560, height - 10), 'besmarterthanthetool.com',
              font=face('medium', 20), fill='#625c7a', anchor='rd')
    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, quality=95, subsampling=0, optimize=True)
    print(f'{output.relative_to(ROOT)}: 1600 × {height}')


if __name__ == '__main__':
    main()
