#!/usr/bin/env python3
"""Two experts, approved original quotations and artwork, standard evidence typography."""
import json, hashlib
from pathlib import Path
from PIL import Image, ImageDraw
from render_embrace_editorial_review import (
    VOICES, face, tracked_width, INNER_TITLE_TRACKING, wrap, WHITE, FRAME,
    draw_board_title, CARDS_TOP, draw_shadow, CARD_RADIUS, mix_with_white,
    CARD_BORDER_OPACITY, accent_wash, cover, top_round_mask, draw_inner_title,
    multiline, BODY, save_course_image)
ROOT = Path(__file__).resolve().parents[2]
ART = ROOT/'scripts/video/assets/loudest-two-experts'
LAYOUT = ART/'layout.json'
def render_two_experts() -> Image.Image:
    """Render the text-complete, vertically extended two-expert board."""

    width = 1600
    card_widths = (744, 744)
    card_xs = (40, 816)
    # EE-2FB artwork geometry, with the evidence sections and type of EE-LONG.
    art_height = 339
    role_font = face("heavy", 20)
    name_font = face("bold", 40)
    background_font = face("medium", 29)
    section_font = face("heavy", 20)
    quote_font = face("medium", 29)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    wrapped: list[tuple[list[str], list[list[str]], list[str]]] = []
    max_background = 0
    max_says = 0
    max_admits = 0
    for voice, card_width in zip(VOICES[:2], card_widths):
        text_width = card_width - 68
        assert tracked_width(measure, voice.name, name_font, INNER_TITLE_TRACKING) <= text_width
        background_lines = wrap(measure, voice.background, background_font, text_width)
        says_blocks = [wrap(measure, quote, quote_font, text_width - 20) for quote in voice.says]
        admits_lines = wrap(measure, voice.admits, quote_font, text_width - 20)
        wrapped.append((background_lines, says_blocks, admits_lines))
        max_background = max(max_background, len(background_lines))
        max_says = max(max_says, sum(len(block) for block in says_blocks) + max(0, len(says_blocks) - 1))
        max_admits = max(max_admits, len(admits_lines))

    role_height = 30
    name_height = 48
    background_line = 41
    quote_line = 41
    section_height = 28
    text_height = (
        32
        + role_height
        + 10
        + name_height
        + 14
        + max_background * background_line
        + 48
        + section_height
        + 12
        + max_says * quote_line
        + 48
        + section_height
        + 12
        + max_admits * quote_line
        + 34
    )
    card_height = art_height + text_height
    cards_bottom = CARDS_TOP + card_height
    height = cards_bottom + 40

    image = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Even the Experts Don’t Know")

    panels = [Image.open(ART / f"{i}.png").convert("RGB") for i in range(2)]
    layout = {"width": width, "height": height, "cards": []}
    for index, (voice, panel, card_width, x, blocks) in enumerate(
        zip(VOICES[:2], panels, card_widths, card_xs, wrapped)
    ):
        accent = voice.accent
        y = CARDS_TOP
        draw_shadow(image, (x, y, x + card_width, y + card_height), CARD_RADIUS)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (x, y, x + card_width, y + card_height),
            radius=CARD_RADIUS,
            fill=WHITE,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )
        image.paste(
            cover(panel, (card_width, art_height)),
            (x, y),
            top_round_mask((card_width, art_height), CARD_RADIUS),
        )
        draw = ImageDraw.Draw(image)
        # Artwork is pasted after the initial card shell, so redraw the complete
        # outline here to keep the accent visible around the illustration edges.
        draw.rounded_rectangle(
            (x, y, x + card_width, y + card_height),
            radius=CARD_RADIUS,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )
        divider_y = y + art_height
        draw.line(
            (x, divider_y, x + card_width, divider_y),
            fill=mix_with_white(accent, 0.20),
            width=1,
        )

        record = {"bounds": [x, y, x+card_width, y+card_height], "sections": [], "accent": accent}
        layout["cards"].append(record)
        section_start = divider_y + 16
        background_lines, says_blocks, admits_lines = blocks
        text_x = x + 34
        text_y = divider_y + 32
        role_width = round(draw.textlength(voice.role, font=role_font)) + 28
        draw.rounded_rectangle(
            (text_x, text_y, text_x + role_width, text_y + 30),
            radius=15,
            fill=mix_with_white(accent, 0.12),
        )
        draw.text((text_x + 14, text_y + 15), voice.role, font=role_font, fill=accent, anchor="lm")
        text_y += role_height + 10
        draw_inner_title(draw, (text_x, text_y), voice.name, fill=accent)
        text_y += name_height + 14
        multiline(draw, (text_x, text_y), background_lines, background_font, BODY, background_line)
        text_y += max_background * background_line + 48

        record["sections"].append([x+16, section_start, x+card_width-16, text_y-24])
        section_start = text_y-8
        draw.text((text_x, text_y), "SAYS", font=section_font, fill=accent)
        text_y += section_height + 12
        says_lines_drawn = 0
        for block_index, quote_lines in enumerate(says_blocks):
            quote_top = text_y + says_lines_drawn * quote_line
            rule_bottom = quote_top + len(quote_lines) * quote_line - 7
            draw.rounded_rectangle(
                (text_x, quote_top + 2, text_x + 4, rule_bottom),
                radius=2,
                fill=mix_with_white(accent, 0.65),
            )
            multiline(draw, (text_x + 20, quote_top), quote_lines, quote_font, BODY, quote_line)
            says_lines_drawn += len(quote_lines)
            if block_index < len(says_blocks) - 1:
                says_lines_drawn += 1
        text_y += max_says * quote_line + 48

        record["sections"].append([x+16, section_start, x+card_width-16, text_y-24])
        section_start = text_y-8
        draw.text((text_x, text_y), "BUT ADMITS", font=section_font, fill=accent)
        text_y += section_height + 12
        rule_bottom = text_y + len(admits_lines) * quote_line - 7
        draw.rounded_rectangle(
            (text_x, text_y + 2, text_x + 4, rule_bottom),
            radius=2,
            fill=mix_with_white(accent, 0.65),
        )
        multiline(draw, (text_x + 20, text_y), admits_lines, quote_font, BODY, quote_line)

        record["sections"].append([x+16, section_start, x+card_width-16, text_y+len(admits_lines)*quote_line+10])

    LAYOUT.write_text(json.dumps(layout, indent=2)+"\n")
    return image


if __name__ == '__main__':
    image = render_two_experts()
    output = ROOT/'course-assets/loudest-voices/loudest-voices-experts.jpg'
    save_course_image(image, output, quality=95, subsampling=0, optimize=True)
    p=ROOT/'course-assets/manifest.json';m=json.loads(p.read_text())
    m['generated_assets']=[a for a in m.get('generated_assets',[]) if a['new']!=str(output.relative_to(ROOT))]
    m['generated_assets'].append({'new':str(output.relative_to(ROOT)), 'sha256':hashlib.sha256(output.read_bytes()).hexdigest(), 'bytes':output.stat().st_size,'width':image.width,'height':image.height,'generator':'scripts/video/render_loudest_two_experts.py','purpose':'Two-expert evidence board; original Amodei and Hinton quotations retained.'})
    p.write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
    print('Rendered', output, image.size)
