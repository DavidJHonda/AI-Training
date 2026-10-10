#!/usr/bin/env python3
"""Canonical Transformer context-board renderer, revision 2026-10-10.

Owns the four context/example boards; reuses the editable Editorial board source.
The preserved artwork is unchanged from the approved board. Other lessons and
historical video builds are not regenerated. Run from the repository root:
.video-venv/bin/python scripts/video/render_transformer_context_revision.py
"""
from pathlib import Path
from PIL import Image, ImageDraw
import render_understand_ai_retrofit_review as r

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'scripts/video/assets/transformer-context-20261010'
OUT = ROOT / 'course-assets/transformer'


def render_before(out):
    """Retain the original sequential path, with the approved revised example."""
    canvas = Image.new('RGB', (1600, 734), r.FRAME)
    d = ImageDraw.Draw(canvas)
    r.draw_board_title(d, 'How Earlier AI Read Text')
    d.rounded_rectangle((40, 127, 1560, 518), radius=14, fill=r.WHITE,
                        outline=r.mix(r.PURPLE, .22), width=1)
    words = ['The', 'tired', 'cat', 'sat', 'on', 'the', 'mat', 'during',
             'the', 'May', 'rainstorm.', 'IT', 'soon', 'fell', 'asleep.']
    rows = (words[:8], words[8:])
    row_edges = []
    for row, y in zip(rows, (187, 407)):
        widths = [max(145, round(d.textlength(w, font=r.face('bold', 29))) + 28) for w in row]
        gap = 25
        x = (1600 - sum(widths) - gap * (len(row)-1)) / 2
        row_edges.append((x, 1600-x))
        for i, (word, width) in enumerate(zip(row, widths)):
            is_it = word == 'IT'
            d.rounded_rectangle((x, y, x+width, y+86), radius=14,
                                fill=r.mix(r.PURPLE, .14 if is_it else .04),
                                outline=r.BRAND if is_it else r.mix(r.PURPLE, .25),
                                width=4 if is_it else 2)
            d.text((x+width/2, y+43), word, font=r.face('bold', 29),
                   fill=r.BRAND if is_it else r.INK, anchor='mm')
            if i < len(row)-1:
                r.arrow(d, (x+width+5, y+43), (x+width+gap-4, y+43), r.mix(r.PURPLE,.35), 3)
            x += width+gap
    # Row-to-row path reads left to right, then resumes at the left.
    color = r.mix(r.PURPLE,.40)
    end = row_edges[0][1] + 5
    start = row_edges[1][0] - 22
    d.line([(end,230),(1520,230),(1520,352),(start,352),(start,450)], fill=color, width=4)
    r.arrow(d, (start,450), (row_edges[1][0]-5,450), color, 3)
    d.text((800,568), 'We know IT refers to CAT.', font=r.face('medium',29), fill=r.INK, anchor='mm')
    r.draw_takeaway_band(canvas, top=606, left=40, right=1560,
                        text='Earlier AI often struggled to keep that connection, especially in longer passages.',
                        font=r.face('medium',r.TAKEAWAY_TEXT_SIZE))
    r.save(canvas,out)


def main():
    r.render_context_problems(ASSETS/'light-pair.png', ASSETS/'pronoun-pair.png', OUT/'transformer-context-problems.jpg', art_is_washed=True)
    render_before(OUT/'transformer-before-transformers.jpg')
    r.render_transformer_reads_whole_message(OUT/'transformer-how-transformer-reads.jpg')
    r.render_context_resolutions(ASSETS/'light-pair.png', ASSETS/'pronoun-pair.png', OUT/'transformer-resolves-meaning.jpg', art_is_washed=True)

if __name__ == '__main__':
    main()
