#!/usr/bin/env python3
"""Render text-only Notebook sources from layout primitives, without artwork.

These upload stand-ins keep the canonical dimensions and printed teaching.
They never replace the illustrated lesson boards or become video visuals.
"""
from pathlib import Path

from PIL import Image, ImageDraw
from editorial_typography import draw_board_title, face

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'gemini-notebook/support-trap/assets'
INK = '#36324b'


def paragraph(draw, text, x, y, width, size=32, color=INK, weight='medium'):
    font = face(weight, size)
    lines, line = [], ''
    for word in text.split():
        candidate = f'{line} {word}'.strip()
        if draw.textlength(candidate, font=font) > width and line:
            lines.append(line)
            line = word
        else:
            line = candidate
    lines.append(line)
    for line in lines:
        draw.text((x, y), line, font=font, fill=color)
        y += size + 13
    return y


def canvas(canonical, title):
    with Image.open(ROOT / 'course-assets/support-trap' / canonical) as board:
        image = Image.new('RGB', board.size, '#eae7fd')
    draw = ImageDraw.Draw(image)
    draw_board_title(draw, title)
    return image, draw


def save(image, name):
    OUT.mkdir(parents=True, exist_ok=True)
    image.save(OUT / name, quality=95, subsampling=0)
    print(f'{name}: {image.width}x{image.height}')


def main():
    image, draw = canvas('support-trap-comparison.jpg', 'Supportive Words versus Support')
    draw.rounded_rectangle((40, 114, 1560, 241), 18, fill='white')
    paragraph(draw, 'THE SCENARIO', 72, 128, 1450, 24, '#4f2fc4', 'bold')
    paragraph(draw, '“I’ve been eating lunch alone for like two weeks.”', 72, 173, 1450)
    cards = [
        (40, '#1652f0', 'PERSON', 'Your Older Sister',
         '“Come sit with me and Jess tomorrow. We’re at the table by the windows.”',
         [('HEARD YOU', 'And did something.'), ('TOMORROW', 'She will look for you.'), ('CHANGED', 'Tomorrow’s lunch.')]),
        (816, '#a9760c', 'AI', 'The Chatbot',
         '“I’m sorry. Eating alone can feel isolating. Would you like strategies for connecting with classmates?”',
         [('FOUND', 'Caring words.'), ('TOMORROW', 'It cannot show up.'), ('CHANGED', 'Nothing outside the chat.')]),
    ]
    for x, accent, label, title, quote, rows in cards:
        draw.rounded_rectangle((x, 272, x + 744, 1340), 18, fill='white')
        paragraph(draw, label, x + 32, 308, 680, 24, accent, 'bold')
        paragraph(draw, title, x + 32, 362, 680, 40, accent, 'bold')
        paragraph(draw, quote, x + 32, 442, 676, 32)
        for y, (label, body) in zip((720, 920, 1120), rows):
            paragraph(draw, label, x + 32, y, 680, 24, accent, 'bold')
            paragraph(draw, body, x + 32, y + 54, 680, 32)
    draw.rounded_rectangle((40, 1380, 1560, 1470), 16, fill='#ffe4a2')
    paragraph(draw, 'Supportive language is not the same as support.', 250, 1400, 1250, 34)
    save(image, 'support-trap-comparison-faceless.jpg')

    image, draw = canvas('support-trap-danger.jpg', 'If Someone May Be in Immediate Danger')
    cards = [
        ('Leave the Chat', 'Tell a trusted adult or school counselor. In the U.S., call or text 988 for crisis support. Call 911 if someone is in immediate danger.'),
        ('Do It Now', 'Not after one more message. A chatbot cannot call, show up, protect someone, or carry responsibility.'),
        ('Tell Anyway', 'Tell a trusted adult even if someone told you not to or made you promise. Safety outranks secrecy.'),
    ]
    for x, (title, body) in zip((40, 558, 1076), cards):
        draw.rounded_rectangle((x, 128, x + 484, 734), 18, fill='white')
        paragraph(draw, title, x + 30, 162, 424, 36, '#c41f28', 'bold')
        bottom = paragraph(draw, body, x + 30, 246, 424, 32)
        assert bottom < 710, (title, bottom)
    draw.rounded_rectangle((40, 773, 1560, 864), 16, fill='#ffe4a2')
    paragraph(draw, 'In danger, the next move must reach a person who can act.', 185, 795, 1380, 34)
    save(image, 'support-trap-danger-faceless.jpg')


if __name__ == '__main__':
    main()
