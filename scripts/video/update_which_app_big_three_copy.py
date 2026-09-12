#!/usr/bin/env python3
"""Update only the What It Is copy on the approved Big Three board."""

from pathlib import Path

from PIL import Image, ImageDraw

from editorial_typography import face


ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "illustrations/which-app-big-three-v2.jpg"
PREP = ROOT / "lessons/which-app-1-big-three.jpg"
BODY = "#3a3550"
WHITE = "#ffffff"


def wrap(draw, text, font, width):
    lines = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if not current or draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def main():
    image = Image.open(PAGE).convert("RGB")
    draw = ImageDraw.Draw(image)
    label_font = face("bold", 22)
    body_font = face("medium", 27)
    # The previous Claude copy extended below the What It Is panel. Clear that
    # obsolete overflow before restoring the divider above ANTHROPIC ASKS.
    draw.rectangle((559, 850, 1040, 878), fill=WHITE)
    draw.line((558, 851, 1041, 851), fill="#e4e0f3", width=1)
    columns = (
        (40, 526, "#0f9f86", "One general-purpose AI app for a wide range of tasks. You can ask questions, create things, and get help with your work."),
        (557, 1042, "#4f2fc4", "An AI assistant for thinking through ideas and working through difficult tasks. Anthropic puts a strong emphasis on safety and how its AI behaves."),
        (1074, 1560, "#3283f5", "Google’s AI assistant, especially useful when your work connects to the Google tools you already use."),
    )
    for left, right, accent, copy in columns:
        draw.rectangle((left + 2, 549, right - 2, 849), fill=WHITE)
        text_x = left + 34
        draw.text((text_x, 583), "WHAT IT IS", font=label_font, fill=accent, anchor="la")
        for index, line in enumerate(wrap(draw, copy, body_font, right - left - 68)):
            draw.text((text_x, 628 + index * 38), line, font=body_font, fill=BODY, anchor="la")
    image.save(PAGE, quality=95, subsampling=0, optimize=True)
    PREP.write_bytes(PAGE.read_bytes())
    print(f"updated {PAGE.relative_to(ROOT)}")
    print(f"copied byte-identically to {PREP.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
