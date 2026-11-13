#!/usr/bin/env python3
"""Render the illustrated Support Trap comparison and the text-only Notebook boards."""
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw
from course_credit import save_course_image
from render_avoid_traps_editorial import AMBER, BLUE, CompareSide, render_comparison
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


def render_lunch_comparison(source, *, illustrated):
    return render_comparison(
        'Same Problem. Different Answers.',
        'You tell your older sister and a chatbot the same thing:\n“At school, I’ve been eating lunch alone for like two weeks. I don’t like it, and I’m not sure what to do.”',
        (
            CompareSide('', 'Your Older Sister', '“Come sit with me and Jess tomorrow. We’re at the table by the windows.”',
                        (('THE TRUTH', 'Your sister loves you, even if she never says it. She’s made room for you at her table. Tomorrow you won’t be eating lunch alone.'),), BLUE),
            CompareSide('', 'The Chatbot', '“I’m sorry. Eating alone can feel isolating. Would you like strategies for connecting with classmates?”',
                        (('THE TRUTH', 'The chatbot offers caring words and ideas. But it won’t be in the cafeteria with you tomorrow.'),), AMBER),
        ),
        str(source), 'Supportive language is not the same as support.', scenario_label='',
        reuse_board_photos=illustrated, source_photo_top=271,
    )


def save_lunch_boards():
    source = ROOT / 'previews/illustration-cast-refresh-batch-8/support-trap-comparison-preview.jpg'
    board = render_lunch_comparison(source, illustrated=True)
    save_course_image(board, ROOT / 'course-assets/support-trap/support-trap-comparison.jpg',
                      quality=95, subsampling=0, optimize=True)
    with TemporaryDirectory() as folder:
        blank = Path(folder) / 'blank.png'
        Image.new('RGB', (1488, 419), 'white').save(blank)
        save(render_lunch_comparison(blank, illustrated=False), 'support-trap-comparison-faceless.jpg')


def main():
    save_lunch_boards()
    image, draw = canvas('support-trap-danger.jpg', 'When Someone May Be in Danger')
    cards = [
        ('Leave the Chat', 'Tell a trusted adult or school counselor. In the U.S., call or text 988 for crisis support. Call 911 if someone is in immediate danger.'),
        ('Do It Now', 'Tell a trusted adult now. If you’re worried about a friend, you can start with “I’m worried about my friend. Can you help?”'),
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
