#!/usr/bin/env python3
"""Render the canonical Training overview board."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

try:
    from .course_credit import save_course_image
    from .editorial_typography import ROOT, draw_board_title, draw_tracked, face
except ImportError:
    from course_credit import save_course_image
    from editorial_typography import ROOT, draw_board_title, draw_tracked, face


WIDTH, HEIGHT = 1600, 620
FRAME = "#eae7fd"
INK = "#0e0a1f"
BODY = "#3a3550"
WHITE = "#ffffff"
PURPLE = "#4f2fc4"
BLUE = "#1652f0"
GREEN = "#0f7a4a"
OUTPUT = ROOT / "course-assets/training/training-three-phases.jpg"


def _rounded_panel(image, box, *, fill=WHITE, radius=18, shadow=True):
    if shadow:
        layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).rounded_rectangle(
            (box[0], box[1] + 7, box[2], box[3] + 7),
            radius=radius,
            fill=(62, 48, 120, 24),
        )
        image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(image).rounded_rectangle(box, radius=radius, fill=fill)


def render(output: Path = OUTPUT) -> Path:
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGBA", (WIDTH, HEIGHT), FRAME)
    draw = ImageDraw.Draw(image)

    draw_board_title(draw, "Three Phases of Training")

    question_box = (40, 112, 1560, 244)
    _rounded_panel(image, question_box, radius=18)
    draw = ImageDraw.Draw(image)
    draw_tracked(
        draw,
        (76, 140),
        "THE SAME QUESTION",
        face("heavy", 17),
        PURPLE,
        2.2,
    )
    draw.text(
        (76, 179),
        "How do I shoot a basketball?",
        font=face("bold", 34),
        fill=INK,
        anchor="la",
    )

    cards = (
        ((40, 272, 530, 558), PURPLE, "1", "Pretraining", "Learn patterns from data."),
        ((555, 272, 1045, 558), BLUE, "2", "Instruction Tuning", "Learn to follow instructions."),
        ((1070, 272, 1560, 558), GREEN, "3", "Preference Tuning", "Improve responses through\nfeedback."),
    )
    for box, color, number, title, copy in cards:
        _rounded_panel(image, box, radius=18)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (box[0] + 22, box[1] + 24, box[0] + 78, box[1] + 80),
            radius=28,
            fill=color,
        )
        draw.text(
            (box[0] + 50, box[1] + 52),
            number,
            font=face("heavy", 25),
            fill=WHITE,
            anchor="mm",
        )
        draw.text(
            (box[0] + 28, box[1] + 105),
            title,
            font=face("bold", 40),
            fill=color,
            anchor="la",
        )
        draw.multiline_text(
            (box[0] + 28, box[1] + 164),
            copy,
            font=face("medium", 29),
            fill=BODY,
            spacing=12,
            anchor="la",
        )

    save_course_image(
        image.convert("RGB"),
        output,
        "JPEG",
        quality=95,
        subsampling=0,
        optimize=True,
        progressive=True,
    )
    return output


if __name__ == "__main__":
    print(render().relative_to(ROOT))
