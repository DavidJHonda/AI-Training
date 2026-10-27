#!/usr/bin/env python3
"""Render the simplified phase map for the local lesson preview only."""
from PIL import Image, ImageDraw
from render_training_three_phases import (
    ROOT, FRAME, WHITE, BODY, PURPLE, BLUE, GREEN, _rounded_panel,
    draw_board_title, face, save_course_image,
)


def render():
    output = ROOT / "previews/training-three-phases-simplified.jpg"
    image = Image.new("RGBA", (1600, 460), FRAME)
    draw_board_title(ImageDraw.Draw(image), "Three Phases of Training")
    cards = [
        (40, PURPLE, "1", "Pretraining", "Learn patterns from data."),
        (555, BLUE, "2", "Instruction Tuning", "Learn from examples of\nfollowing requests."),
        (1070, GREEN, "3", "Preference Tuning", "Learn from feedback about\nbetter answers."),
    ]
    for x, color, number, title, copy in cards:
        _rounded_panel(image, (x, 112, x + 490, 400))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((x + 22, 136, x + 78, 192), radius=28, fill=color)
        draw.text((x + 50, 164), number, font=face("heavy", 25), fill=WHITE, anchor="mm")
        draw.text((x + 28, 217), title, font=face("bold", 40), fill=color, anchor="la")
        draw.multiline_text((x + 28, 276), copy, font=face("medium", 29),
                            fill=BODY, spacing=12, anchor="la")
    save_course_image(image.convert("RGB"), output, "JPEG", quality=95,
                      subsampling=0, optimize=True, progressive=True)
    return output


if __name__ == "__main__":
    print(render().relative_to(ROOT))
