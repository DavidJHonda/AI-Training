#!/usr/bin/env python3
"""Render the matched before-and-after reading boards for Transformer."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
FONT_ROOT = Path("/Users/davidobrien/Library/Fonts")
W, H = 1600, 900

LAVENDER = "#eeeaff"
WHITE = "#ffffff"
PALE = "#f8f6ff"
NAVY = "#08072b"
CARD_TITLE = "#152b7a"
BODY = "#0e0a1f"
PURPLE = "#6f52ff"
GOLD = "#ffe9ab"
RULE = "#d9d4e9"
MUTED = "#6f6a82"


def font(weight, size):
    names = {
        "heavy": "AvenirNextforINTUIT-Heavy.otf",
        "bold": "AvenirNextforINTUIT-Bold.otf",
        "demi": "AvenirNextforINTUIT-Demi.otf",
        "medium": "AvenirNextforINTUIT-Medium.otf",
    }
    return ImageFont.truetype(str(FONT_ROOT / names[weight]), size)


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered(draw, xy, text, face, fill=NAVY):
    draw.text(xy, text, font=face, fill=fill, anchor="mm")


def check(draw, cx, cy):
    draw.line(
        (cx - 12, cy, cx - 3, cy + 10, cx + 16, cy - 12),
        fill=WHITE,
        width=6,
        joint="curve",
    )


def takeaway(draw, text):
    rounded(draw, (80, 776, 1520, 860), 16, GOLD)
    face = font("demi", 32)
    text_width = draw.textlength(text, font=face)
    group_width = 52 + 16 + text_width
    x = 800 - group_width / 2
    draw.ellipse((x, 792, x + 52, 844), fill=PURPLE)
    check(draw, x + 26, 818)
    draw.text((x + 68, 818), text, font=face, fill=NAVY, anchor="lm")


def arrow(draw, x0, y, x1, color=PURPLE, width=4):
    draw.line((x0, y, x1 - 12, y), fill=color, width=width)
    draw.polygon([(x1, y), (x1 - 14, y - 9), (x1 - 14, y + 9)], fill=color)


def token_card(draw, box, word, strength, highlight=False):
    x0, y0, x1, y1 = box
    fills = ["#fbfafd", "#f7f4ff", "#f0eaff", "#e7ddff"]
    outlines = ["#e6e2ed", "#d6cdeb", "#bbaaf0", PURPLE]
    rounded(
        draw,
        box,
        14,
        "#e4dcff" if highlight else fills[strength],
        PURPLE if highlight else outlines[strength],
        4 if highlight else 2,
    )
    word_size = 28 if len(word) >= 8 else 32
    centered(
        draw,
        ((x0 + x1) / 2, (y0 + y1) / 2 + 3),
        word.upper() if highlight else word,
        font("demi" if not highlight else "bold", word_size),
        PURPLE if highlight else NAVY,
    )


def rounded_photo(canvas, source, box, radius=16):
    x0, y0, x1, y1 = box
    size = (x1 - x0, y1 - y0)
    fitted = ImageOps.fit(source, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    canvas.paste(fitted, (x0, y0), mask)


def save(image, filename):
    outputs = [
        ROOT / "lessons" / filename,
        ROOT / "illustrations" / filename,
        ROOT / "board-review-first-four" / "current-selected" / "understand-ai" / filename,
    ]
    for output in outputs:
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, quality=95, subsampling=0)
        print(f"Built {output}")


def build_before():
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    centered(draw, (800, 57), "Before Transformers:", font("heavy", 44))
    centered(draw, (800, 117), "Yesterday's AI read one word at a time", font("heavy", 44))
    rounded(draw, (80, 172, 1520, 736), 16, WHITE)

    centered(draw, (800, 220), "AI moves forward through the sentence", font("demi", 28), CARD_TITLE)
    arrow(draw, 1080, 221, 1308, "#9885e5", 4)

    words = [
        "The", "cat", "sat", "on", "the", "mat", "during",
        "the", "May", "rainstorm", "because", "it", "was", "tired",
    ]
    card_w, card_h = 174, 82
    x_positions = [112 + 202 * index for index in range(7)]
    y_positions = [286, 494]
    for index, word in enumerate(words):
        row, col = divmod(index, 7)
        x0, y0 = x_positions[col], y_positions[row]
        strength = min(3, index // 4)
        token_card(
            draw,
            (x0, y0, x0 + card_w, y0 + card_h),
            word,
            strength,
            highlight=(word == "it"),
        )
        if col < 6:
            arrow(draw, x0 + card_w + 6, y0 + card_h / 2, x0 + card_w + 22, outlines_for_arrow(strength), 3)

    # Keep reading order obvious when the sentence wraps to its second line.
    draw.line((1488, 327, 1502, 327, 1502, 462, 99, 462, 99, 535), fill="#c1b5eb", width=4, joint="curve")
    draw.polygon([(99, 548), (89, 532), (109, 532)], fill="#c1b5eb")
    centered(draw, (800, 662), "CAT is still readable here, but old AI struggled to carry it forward to IT.", font("medium", 29), MUTED)
    takeaway(draw, "By the time AI reaches IT, CAT has faded.")
    return image


def outlines_for_arrow(strength):
    return ["#ddd8e8", "#cec5e9", "#b5a6e9", "#9885e5"][strength]


def word_pill(draw, box, word, active=False):
    rounded(draw, box, 16, "#e6deff" if active else WHITE, PURPLE if active else RULE, 4 if active else 2)
    centered(draw, ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2 + 2), word, font("bold", 34), PURPLE if active else CARD_TITLE)


def build_now():
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    centered(draw, (800, 57), "With Transformers:", font("heavy", 44))
    centered(draw, (800, 117), "Today's AI reads every word at once", font("heavy", 44))
    rounded(draw, (80, 172, 1520, 736), 16, WHITE)

    source = Image.open(ROOT / "illustrations" / "transformer.jpg").convert("RGB")
    rounded_photo(image, source, (110, 202, 844, 706), 16)

    rounded(draw, (884, 202, 1490, 706), 16, PALE, RULE, 2)
    centered(draw, (1187, 246), "ATTENTION", font("heavy", 21), PURPLE)
    centered(draw, (1187, 300), "Which words matter?", font("bold", 34), CARD_TITLE)
    draw.line((930, 336, 1444, 336), fill=RULE, width=2)

    cat_box = (942, 380, 1122, 464)
    tired_box = (1252, 380, 1432, 464)
    it_box = (1097, 536, 1277, 620)
    draw.line((1187, 576, 1032, 422), fill=PURPLE, width=6)
    draw.line((1187, 576, 1342, 422), fill=PURPLE, width=6)
    word_pill(draw, cat_box, "CAT", True)
    word_pill(draw, tired_box, "TIRED", True)
    word_pill(draw, it_box, "IT", True)
    centered(draw, (1187, 666), "IT can look directly at both.", font("medium", 29), BODY)

    takeaway(draw, "Attention connects IT to CAT and TIRED, even ten words later.")
    return image


def main():
    save(build_before(), "transformer-1-before.jpg")
    save(build_now(), "transformer-2-now.jpg")


if __name__ == "__main__":
    main()
