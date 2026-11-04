#!/usr/bin/env python3
"""Render text-only upload layouts from the current Curiosity board definitions.

Creates new typography layouts, without altering or reading photographic artwork.
Canonical board dimensions, copy, colors, and card order are preserved.
"""
import hashlib
import json

from PIL import Image, ImageDraw

from editorial_typography import draw_board_title, draw_inner_title, face
from render_editorial_full_bleed_batch import (
    BOARDS, ROOT, FRAME, WHITE, BODY, CARDS_TOP, GUTTER, PADDING,
    EE4_CARD_WIDTH, TEXT_SIDE, TITLE_LINE, TITLE_BODY_GAP, BODY_LINE,
    mix_with_white, multiline, wrap,
)


def main():
    directory = ROOT / 'gemini-notebook/curiosity/assets'
    directory.mkdir(parents=True, exist_ok=True)
    outputs = {'curiosity-four-ways': 'curiosity-why-faceless.jpg',
               'curiosity-ai-habits': 'curiosity-ai-faceless.jpg'}
    records = []
    for board in BOARDS:
        if board.key not in outputs:
            continue
        canonical = ROOT / board.page_output
        with Image.open(canonical) as source:
            width, height = source.size
        canvas = Image.new('RGB', (width, height), WHITE)
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=22, fill=FRAME)
        draw_board_title(draw, board.title)
        card_height = (height - CARDS_TOP - PADDING - GUTTER) // 2
        font = face('medium', 29)
        for i, ((title, body), accent) in enumerate(zip(board.cards, board.accents)):
            x = 40 if i % 2 == 0 else 816
            y = CARDS_TOP + (i // 2) * (card_height + GUTTER)
            lines = wrap(draw, body, font, EE4_CARD_WIDTH - 2 * TEXT_SIDE)
            text_height = TITLE_LINE + TITLE_BODY_GAP + len(lines) * BODY_LINE
            assert text_height + 64 <= card_height
            draw.rounded_rectangle((x, y, x + EE4_CARD_WIDTH, y + card_height),
                                   radius=14, fill=WHITE,
                                   outline=mix_with_white(accent, .22), width=1)
            text_y = y + (card_height - text_height) // 2
            draw_inner_title(draw, (x + TEXT_SIDE, text_y), title, fill=accent)
            multiline(draw, (x + TEXT_SIDE, text_y + TITLE_LINE + TITLE_BODY_GAP),
                      lines, font, BODY, BODY_LINE)
        target = directory / outputs[board.key]
        canvas.save(target, quality=95, subsampling=0, optimize=True)
        records.append({
            'upload': str(target.relative_to(ROOT)),
            'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
            'canonical': board.page_output,
            'canonical_sha256': hashlib.sha256(canonical.read_bytes()).hexdigest(),
            'dimensions': [width, height],
            'title': board.title,
            'cards': [{'title': title, 'body': body} for title, body in board.cards],
        })
        print(f'{target.relative_to(ROOT)}: {width}x{height}')
    (directory / 'source-manifest.json').write_text(json.dumps(records, indent=2) + '\n')


if __name__ == '__main__':
    main()
