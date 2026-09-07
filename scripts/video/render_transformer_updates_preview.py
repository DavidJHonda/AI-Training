#!/usr/bin/env python3
"""Preview only: show the separate attention and feed-forward updates."""

from PIL import Image, ImageDraw

import render_understand_ai_retrofit_review as r


def render_preview():
    canvas = Image.new("RGB", (1600, 928), r.FRAME)
    draw = ImageDraw.Draw(canvas)
    r.draw_board_title(draw, "Attention, Then Transformation")

    for left, accent, heading, body in (
        (40, r.PURPLE, "Attention", "Weigh relevant words and blend their information into IT’s numbers."),
        (816, r.AMBER, "Transformation", "Use learned patterns to further update IT’s numbers."),
    ):
        draw.rounded_rectangle((left, 127, left + 744, 760), radius=14, fill=r.WHITE)
        draw.rounded_rectangle((left, 127, left + 744, 535), radius=14, fill=r.mix(accent, 0.08))
        draw.rounded_rectangle((left + 40, 167, left + 704, 505), radius=16, fill=r.WHITE)
        draw.rounded_rectangle((left, 127, left + 744, 760), radius=14, outline=r.mix(accent, 0.22), width=2)
        draw.line((left, 535, left + 744, 535), fill=r.mix(accent, 0.22), width=2)
        r.draw_inner_title(draw, (left + 34, 567), heading, fill=accent)
        r.draw_wrapped(draw, body, left + 34, 636, 676, r.face("medium", 29), r.BODY)

    def vector(left, values, color, caption):
        draw.rounded_rectangle((left, 329, left + 220, 453), radius=12,
                               fill=r.mix(color, 0.075), outline=r.mix(color, 0.30), width=2)
        draw.text((left + 110, 358), "IT", font=r.face("bold", 28), fill=color, anchor="mm")
        for offset, number in zip((35, 96, 156, 197), (*values, "…")):
            draw.text((left + offset, 413), number, font=r.face("bold", 24), fill=color, anchor="mm")
        draw.text((left + 110, 477), caption, font=r.face("medium", 24), fill=r.MUTED, anchor="mm")

    # The attention output and transformation input deliberately match.
    vector(100, ("0.2", "0.1", "0.4"), r.MUTED, "Starting numbers")
    vector(504, ("0.4", "−0.1", "0.7"), r.PURPLE, "Updated numbers")
    vector(876, ("0.4", "−0.1", "0.7"), r.PURPLE, "Updated numbers")
    vector(1280, ("0.3", "−0.2", "0.8"), r.TEAL, "Updated again")

    draw.rounded_rectangle((269, 187, 555, 260), radius=12,
                           fill=r.mix(r.PURPLE, 0.12), outline=r.mix(r.PURPLE, 0.30), width=2)
    draw.text((412, 211), "CAT", font=r.face("bold", 28), fill=r.PURPLE, anchor="mm")
    draw.text((412, 242), "+ other earlier words", font=r.face("medium", 22), fill=r.PURPLE, anchor="mm")
    draw.text((412, 295), "Weigh + blend", font=r.face("bold", 24), fill=r.PURPLE, anchor="mm")
    r.arrow(draw, (412, 318), (412, 387), r.PURPLE, 4)
    r.arrow(draw, (334, 399), (490, 399), r.PURPLE, 5)

    draw.text((1188, 295), "Process", font=r.face("bold", 24), fill=r.AMBER, anchor="mm")
    r.arrow(draw, (1110, 399), (1266, 399), r.AMBER, 5)
    r.arrow(draw, (790, 399), (810, 399), r.MUTED, 4)

    r.draw_takeaway_band(canvas, top=800, left=40, right=1560,
                        text="Both steps update the numbers. Attention brings in context.",
                        font=r.face("medium", r.TAKEAWAY_TEXT_SIZE))
    out = r.OUT / "previews/transformer-attention-transformation-v1.jpg"
    r.save(canvas, out)
    return out


if __name__ == "__main__":
    render_preview()
