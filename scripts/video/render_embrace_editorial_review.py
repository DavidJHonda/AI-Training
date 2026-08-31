#!/usr/bin/env python3
"""Render the eight remaining Embrace editorial boards for review only.

Nothing produced by this script is copied into ``illustrations/`` or ``lessons/``.
The review boards deliberately reuse the canonical Editorial Explainer renderer so
their typography, card geometry, borders, art crops, and derived heights match the
approved course formats exactly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_typography import (
    INNER_TITLE_TRACKING,
    draw_board_title,
    draw_inner_title,
    tracked_width,
)

from render_embrace_editorial_batch import (
    AMBER,
    BLUE,
    BODY,
    CARD_BORDER_OPACITY,
    CARD_RADIUS,
    CARDS_TOP,
    FRAME,
    INK,
    PURPLE,
    RED,
    TEAL,
    WHITE,
    Card,
    CardBoard,
    FlowBoard,
    accent_wash,
    cover,
    draw_takeaway,
    draw_shadow,
    face,
    mix_with_white,
    multiline,
    render_card_board,
    render_flow_board,
    rounded_mask,
    split_art_sheet,
    top_round_mask,
    wrap,
)


ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "board-review-embrace-editorial"
JAILBREAK_PAGE_OUTPUT = "illustrations/big-downside-jailbreak-v2.jpg"
JAILBREAK_PREP_OUTPUT = "lessons/big-downside-2-jailbreak.jpg"
GPS_AGENT_PAGE_OUTPUT = "illustrations/rise-of-agents-gps-agent-v2.jpg"
GPS_AGENT_PREP_OUTPUT = "lessons/rise-of-agents-1-gps.jpg"


@dataclass(frozen=True)
class Voice:
    role: str
    name: str
    accent: str
    background: str
    says: tuple[str, ...]
    admits: str


VOICES = (
    Voice(
        role="OPTIMIST",
        name="Dario Amodei",
        accent=PURPLE,
        background="Built GPT-2 and GPT-3 at OpenAI, then founded Anthropic, the company behind Claude.",
        says=(
            "“AI-enabled biology and medicine will allow us to compress the progress that human biologists would have achieved over the next 50-100 years into 5-10 years.”",
        ),
        admits="“Humanity is about to be handed almost unimaginable power, and it is deeply unclear whether our social, political, and technological systems possess the maturity to wield it.”",
    ),
    Voice(
        role="WORRIER",
        name="Geoffrey Hinton",
        accent=BLUE,
        background="Won a Nobel Prize for his ideas that AI runs on. At 75, he left his job at Google so he could warn people about AI.",
        says=(
            "“We’re actually making new kinds of beings. They have goals. We give them goals, and from those goals they derive other goals. We don’t necessarily know what other goals they’ll derive.”",
        ),
        admits="“If we can detect cancer much earlier thanks to AI, fewer people will die from it.”",
    ),
    Voice(
        role="DOUBTER",
        name="Yann LeCun",
        accent=TEAL,
        background="Won the Turing Award for helping invent modern AI. He thinks that everyone is building AI the wrong way.",
        says=(
            "“LLMs basically are a dead end when it comes to superintelligence.”",
            "“LLMs have a more superficial understanding of the world than a house cat.”",
        ),
        admits="“I do acknowledge risks. AI is not something that just happens. We build it, we have agency in what it becomes. Hence we control the risks.”",
    ),
)


def render_extended_voices() -> Image.Image:
    """Render the text-complete, vertically extended three-voice board."""

    width = 1600
    card_widths = (485, 486, 485)
    card_xs = (40, 557, 1075)
    # 486x273 is effectively 16:9 and keeps all three art frames on one baseline.
    art_height = 273
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
    for voice, card_width in zip(VOICES, card_widths):
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

    sheet = Image.open(REVIEW / "assets/three-voices/art-sheet.png").convert("RGB")
    panels = split_art_sheet(sheet, 3)
    for index, (voice, panel, card_width, x, blocks) in enumerate(
        zip(VOICES, panels, card_widths, card_xs, wrapped)
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
            accent_wash(cover(panel, (card_width, art_height)), accent),
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

        draw.text((text_x, text_y), "BUT ADMITS", font=section_font, fill=accent)
        text_y += section_height + 12
        rule_bottom = text_y + len(admits_lines) * quote_line - 7
        draw.rounded_rectangle(
            (text_x, text_y + 2, text_x + 4, rule_bottom),
            radius=2,
            fill=mix_with_white(accent, 0.65),
        )
        multiline(draw, (text_x + 20, text_y), admits_lines, quote_font, BODY, quote_line)

    return image


def render_jailbreak_feature() -> Image.Image:
    """Preserve the original fortress scene inside the Editorial board system."""

    width = 1600
    art_left = 40
    art_top = CARDS_TOP
    art_width = 1520
    art_height = round(art_width * 2 / 3)
    footer_top = art_top + art_height + 40
    height = footer_top + 88 + 40

    image = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Why Jailbreaks Keep Appearing")

    source = Image.open(ROOT / "illustrations/big-downside-2.jpg").convert("RGB")
    art = cover(source, (art_width, art_height))
    image.paste(art, (art_left, art_top), rounded_mask((art_width, art_height), CARD_RADIUS))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (art_left, art_top, art_left + art_width, art_top + art_height),
        radius=CARD_RADIUS,
        outline=mix_with_white(AMBER, CARD_BORDER_OPACITY),
        width=1,
    )
    draw_takeaway(
        image,
        footer_top,
        "New methods keep surfacing, making this an ongoing game of cat-and-mouse.",
    )
    return image


def render_gps_agent_feature() -> Image.Image:
    """Map the existing Nate-and-Luke driving scene directly to AI behavior."""

    width = 1600
    stage_left = 40
    stage_top = CARDS_TOP
    stage_width = 1520
    art_height = round(stage_width * 9 / 16)
    center_x = stage_left + stage_width // 2
    title_font = face("bold", 40)
    body_font = face("medium", 29)
    sides = (
        (
            stage_left + 34,
            PURPLE,
            "GPS Is Like ChatGPT",
            "You enter a destination in Waze or Google Maps. It tells you each turn, but you still steer, brake, and catch mistakes.",
        ),
        (
            center_x + 34,
            BLUE,
            "Self-Driving Is Like an Agent",
            "You enter the same destination. The car steers, brakes, and reroutes for you. You may not catch a mistake until later.",
        ),
    )
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    text_width = stage_width // 2 - 68
    body_blocks = [wrap(measure, body, body_font, text_width) for _, _, _, body in sides]
    for _, _, title, _ in sides:
        assert tracked_width(measure, title, title_font, INNER_TITLE_TRACKING) <= text_width
    text_height = 30 + 48 + 14 + max(len(lines) for lines in body_blocks) * 41 + 34
    stage_bottom = stage_top + art_height + text_height
    height = stage_bottom + 40

    image = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "A Chatbot Answers. An Agent Acts.")

    draw_shadow(image, (stage_left, stage_top, stage_left + stage_width, stage_bottom), CARD_RADIUS)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (stage_left, stage_top, stage_left + stage_width, stage_bottom),
        radius=CARD_RADIUS,
        fill=WHITE,
        outline="#d7d2e8",
        width=1,
    )
    source = Image.open(ROOT / "illustrations/rise-of-agents.jpg").convert("RGB")
    art = cover(source, (stage_width, art_height))
    image.paste(art, (stage_left, stage_top), top_round_mask((stage_width, art_height), CARD_RADIUS))
    draw = ImageDraw.Draw(image)
    divider_y = stage_top + art_height
    draw.line((stage_left, divider_y, stage_left + stage_width, divider_y), fill="#d7d2e8", width=1)
    draw.line((center_x, divider_y + 24, center_x, stage_bottom - 24), fill="#e3dfef", width=1)

    text_top = divider_y + 30
    for (text_x, accent, title, _), body_lines in zip(sides, body_blocks):
        draw_inner_title(draw, (text_x, text_top), title, fill=accent)
        multiline(draw, (text_x, text_top + 62), body_lines, body_font, BODY, 41)
    return image


def render_chatbot_agent_long() -> Image.Image:
    """Render the basketball assignment as an extended two-card comparison."""

    width = 1600
    card_width = 744
    card_gap = 32
    card_lefts = (40, 40 + card_width + card_gap)
    scenario_top = 112
    scenario_height = 142
    cards_top = scenario_top + scenario_height + 32
    art_height = round(card_width * 9 / 16)
    scenario_label_font = face("heavy", 20)
    scenario_font = face("medium", 32)
    pill_font = face("heavy", 20)
    card_title_font = face("bold", 40)
    section_font = face("heavy", 20)
    body_font = face("medium", 29)
    text_width = card_width - 68
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    scenario_lines = (
        "You scored 30 points in Friday’s basketball game. A friend videoed the game on their phone.",
        "You want to post the best highlights to TikTok.",
    )
    for line in scenario_lines:
        assert measure.textlength(line, font=scenario_font) <= 1456

    cards = (
        {
            "accent": PURPLE,
            "pill": "REGULAR AI",
            "title": "Ask a Chatbot",
            "sections": (
                ("YOU DO", "Review all 50 clips, select the plays, trim and assemble the reel, choose when to post, and publish it."),
                ("AI DOES", "Writes the caption when asked."),
                ("WHAT CHANGES", "AI contributes one step, then stops."),
            ),
        },
        {
            "accent": BLUE,
            "pill": "AGENT",
            "title": "Hire an Agent",
            "sections": (
                ("THE AGENT DOES", "Reviews the clips, selects the best moments, builds the reel, writes the caption, chooses a posting time, and publishes it."),
                ("YOU STILL OWN", "The goal, final review, and everything posted under your name."),
                ("WHAT CHANGES", "The agent carries the job through."),
            ),
        },
    )
    for card in cards:
        assert tracked_width(measure, card["title"], card_title_font, INNER_TITLE_TRACKING) <= text_width
        for label, _ in card["sections"]:
            assert measure.textlength(label, font=section_font) <= text_width

    wrapped = [
        [wrap(measure, body, body_font, text_width) for _, body in card["sections"]]
        for card in cards
    ]
    peer_lines = [max(len(wrapped[0][index]), len(wrapped[1][index])) for index in range(3)]
    text_height = 32 + 30 + 10 + 48 + 34
    for index, line_count in enumerate(peer_lines):
        text_height += 28 + 12 + line_count * 41
        if index < 2:
            text_height += 48
    text_height += 34
    card_height = art_height + text_height
    height = cards_top + card_height + 40

    image = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Ask a Chatbot versus Hire an Agent")
    draw.rounded_rectangle(
        (40, scenario_top, width - 40, scenario_top + scenario_height),
        radius=18,
        fill=WHITE,
        outline=mix_with_white(PURPLE, CARD_BORDER_OPACITY),
        width=1,
    )
    draw.rectangle(
        (40, scenario_top + 18, 47, scenario_top + scenario_height - 18),
        fill=PURPLE,
    )
    draw.text((72, scenario_top + 22), "THE SCENARIO", font=scenario_label_font, fill=PURPLE)
    draw.text((72, scenario_top + 55), scenario_lines[0], font=scenario_font, fill=BODY)
    draw.text((72, scenario_top + 96), scenario_lines[1], font=scenario_font, fill=BODY)

    sheet = Image.open(REVIEW / "assets/chatbot-vs-agent/art-sheet.png").convert("RGB")
    panels = split_art_sheet(sheet, 2)
    for card, panel, blocks, left in zip(cards, panels, wrapped, card_lefts):
        accent = card["accent"]
        draw_shadow(image, (left, cards_top, left + card_width, cards_top + card_height), CARD_RADIUS)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (left, cards_top, left + card_width, cards_top + card_height),
            radius=CARD_RADIUS,
            fill=WHITE,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )
        art = accent_wash(cover(panel, (card_width, art_height)), accent)
        image.paste(art, (left, cards_top), top_round_mask((card_width, art_height), CARD_RADIUS))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (left, cards_top, left + card_width, cards_top + card_height),
            radius=CARD_RADIUS,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )
        divider_y = cards_top + art_height
        draw.line((left, divider_y, left + card_width, divider_y), fill=mix_with_white(accent, 0.20), width=1)

        text_x = left + 34
        text_y = divider_y + 32
        pill_width = round(draw.textlength(card["pill"], font=pill_font)) + 28
        draw.rounded_rectangle(
            (text_x, text_y, text_x + pill_width, text_y + 30),
            radius=15,
            fill=mix_with_white(accent, 0.12),
        )
        draw.text((text_x + 14, text_y + 15), card["pill"], font=pill_font, fill=accent, anchor="lm")
        text_y += 40
        draw_inner_title(draw, (text_x, text_y), card["title"], fill=accent)
        text_y += 48 + 34

        for index, ((label, _), body_lines) in enumerate(zip(card["sections"], blocks)):
            draw.text((text_x, text_y), label, font=section_font, fill=accent)
            text_y += 28 + 12
            multiline(draw, (text_x, text_y), body_lines, body_font, BODY, 41)
            text_y += peer_lines[index] * 41
            if index < 2:
                text_y += 48
    return image


def render_first_assignment_long() -> Image.Image:
    """Render the customer-review assignment with the original Nate-and-Luke scene."""

    width = 1600
    card_width = 744
    card_gap = 32
    card_lefts = (40, 40 + card_width + card_gap)
    scenario_top = 112
    scenario_height = 183
    cards_top = scenario_top + scenario_height + 32
    art_height = round(card_width * 9 / 16)
    scenario_label_font = face("heavy", 20)
    scenario_font = face("medium", 32)
    pill_font = face("heavy", 20)
    card_title_font = face("bold", 40)
    intro_font = face("medium", 29)
    section_font = face("heavy", 20)
    body_font = face("medium", 29)
    text_width = card_width - 68
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))

    scenario = (
        "Your manager tells you, “We’re getting bad customer feedback on our new product. "
        "Read the last 500 reviews and tell us what’s happening and how we should fix it.”"
    )
    scenario_lines = wrap(measure, scenario, scenario_font, 1456)
    assert len(scenario_lines) <= 2

    first_pass = (
        "Read and organize 500 reviews",
        "Find the recurring themes",
        "Build the spreadsheet",
        "Create a first analysis",
        "Draft the presentation deck",
    )
    cards = (
        {
            "accent": PURPLE,
            "pill": "THE OLD JOB",
            "title": "Before AI",
            "intro": "The week disappears into the first pass. Friday arrives before the real thinking begins.",
            "sections": (
                ("YOU DO THE FIRST PASS", first_pass),
                ("THEN YOU", ("Investigate why", "Recommend the fix", "Present the findings")),
                ("THE RESULT", ("The boss adds a page of comments, and you spend the next week reanalyzing.",)),
            ),
        },
        {
            "accent": AMBER,
            "pill": "THE NEW JOB",
            "title": "With AI",
            "intro": "AI completes the first pass in minutes. Your week can begin with the real questions.",
            "sections": (
                ("AI DOES THE FIRST PASS", first_pass),
                ("YOU START HERE", ("Improve AI’s work", "Investigate why", "Recommend the fix", "Present the findings")),
                ("THE RESULT", ("The boss loves it. The week you spent on the real questions pays off.",)),
            ),
        },
    )

    wrapped_intros = [wrap(measure, card["intro"], intro_font, text_width) for card in cards]
    wrapped_sections = []
    peer_lines = [0, 0, 0]
    for card in cards:
        card_sections = []
        for section_index, (label, items) in enumerate(card["sections"]):
            assert measure.textlength(label, font=section_font) <= text_width
            item_blocks = [wrap(measure, item, body_font, text_width - 30) for item in items]
            lines = sum(len(block) for block in item_blocks)
            peer_lines[section_index] = max(peer_lines[section_index], lines)
            card_sections.append(item_blocks)
        wrapped_sections.append(card_sections)

    intro_lines = max(len(lines) for lines in wrapped_intros)
    text_height = 32 + 30 + 10 + 48 + 18 + intro_lines * 41 + 42
    for index, line_count in enumerate(peer_lines):
        text_height += 28 + 12 + line_count * 41
        if index < 2:
            text_height += 42
    text_height += 34
    card_height = art_height + text_height
    height = cards_top + card_height + 40

    image = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Your First Assignment")
    draw.rounded_rectangle(
        (40, scenario_top, width - 40, scenario_top + scenario_height),
        radius=18,
        fill=WHITE,
        outline=mix_with_white(PURPLE, CARD_BORDER_OPACITY),
        width=1,
    )
    draw.rectangle(
        (40, scenario_top + 18, 47, scenario_top + scenario_height - 18),
        fill=PURPLE,
    )
    draw.text((72, scenario_top + 22), "THE ASSIGNMENT", font=scenario_label_font, fill=PURPLE)
    multiline(draw, (72, scenario_top + 58), scenario_lines, scenario_font, BODY, 45)

    source = Image.open(ROOT / "illustrations/work-changes.jpg").convert("RGB")
    source_width, source_height = source.size
    half_width = source_width // 2
    crop_height = round(half_width * 9 / 16)
    crop_top = min(150, source_height - crop_height)
    panels = (
        source.crop((0, crop_top, half_width, crop_top + crop_height)),
        source.crop((half_width, crop_top, source_width, crop_top + crop_height)),
    )

    for card, panel, intro_lines_block, section_blocks, left in zip(
        cards, panels, wrapped_intros, wrapped_sections, card_lefts
    ):
        accent = card["accent"]
        draw_shadow(image, (left, cards_top, left + card_width, cards_top + card_height), CARD_RADIUS)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (left, cards_top, left + card_width, cards_top + card_height),
            radius=CARD_RADIUS,
            fill=WHITE,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )
        art = accent_wash(panel.resize((card_width, art_height), Image.Resampling.LANCZOS), accent)
        image.paste(art, (left, cards_top), top_round_mask((card_width, art_height), CARD_RADIUS))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle(
            (left, cards_top, left + card_width, cards_top + card_height),
            radius=CARD_RADIUS,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )
        divider_y = cards_top + art_height
        draw.line((left, divider_y, left + card_width, divider_y), fill=mix_with_white(accent, 0.20), width=1)

        text_x = left + 34
        text_y = divider_y + 32
        pill_width = round(draw.textlength(card["pill"], font=pill_font)) + 28
        draw.rounded_rectangle(
            (text_x, text_y, text_x + pill_width, text_y + 30),
            radius=15,
            fill=mix_with_white(accent, 0.12),
        )
        draw.text((text_x + 14, text_y + 15), card["pill"], font=pill_font, fill=accent, anchor="lm")
        text_y += 40
        draw_inner_title(draw, (text_x, text_y), card["title"], fill=accent)
        text_y += 48 + 18
        multiline(draw, (text_x, text_y), intro_lines_block, intro_font, BODY, 41)
        text_y += intro_lines * 41 + 42

        for section_index, ((label, _), item_blocks) in enumerate(zip(card["sections"], section_blocks)):
            draw.text((text_x, text_y), label, font=section_font, fill=accent)
            text_y += 28 + 12
            item_y = text_y
            for block in item_blocks:
                dot_y = item_y + 15
                draw.ellipse((text_x, dot_y - 4, text_x + 8, dot_y + 4), fill=accent)
                multiline(draw, (text_x + 30, item_y), block, body_font, BODY, 41)
                item_y += len(block) * 41
            text_y += peer_lines[section_index] * 41
            if section_index < 2:
                text_y += 42

    return image


CARD_BOARDS = (
    CardBoard(
        key="this-has-happened-before",
        title="This Has Happened Before",
        cards=(
            Card(
                "Online Shopping",
                "In 1995, Clifford Stoll said online shopping could not compete with malls. It became part of everyday life.",
                "ASTRONOMER",
            ),
            Card(
                "No Chance for the iPhone",
                "In 2007, Steve Ballmer said the iPhone had no chance at meaningful market share. It reshaped smartphones.",
                "MICROSOFT CEO",
            ),
            Card(
                "The Internet Will Collapse",
                "In 1996, Robert Metcalfe predicted a catastrophic collapse. The internet became essential infrastructure.",
                "INVENTOR OF ETHERNET",
            ),
            Card(
                "Flying Cars Are Coming",
                "In 1940, Henry Ford predicted a flying car was coming. It still has not become ordinary transportation.",
                "FOUNDER OF FORD MOTOR COMPANY",
            ),
        ),
        art_sheet="board-review-embrace-editorial/assets/failed-predictions/art-sheet.png",
        page_output="illustrations/loudest-voices-missed-predictions-v2.jpg",
        prep_output="lessons/loudest-voices-2-missed-calls.jpg",
        takeaway="The future is hard to predict because people change the result.",
        accents=(PURPLE, BLUE, TEAL, AMBER),
    ),
    CardBoard(
        key="four-famous-plans",
        title="The Biggest Results Were Never the Plan",
        cards=(
            Card(
                "Text Messaging",
                "SMS was designed as a short service for mobile networks. Today, it is the technology behind traditional text messages.",
            ),
            Card(
                "GPS",
                "Built by the U.S. military to guide ships, aircraft, and weapons. Today, it powers everyday location tools, including Google Maps.",
            ),
            Card(
                "Cane Toads",
                "Australia imported cane toads to eat beetles destroying sugarcane. They barely controlled the pests, poisoned native animals, and spread across the country.",
            ),
            Card(
                "Wider Highways",
                "To ease congestion, Texas spent $2.8 billion widening Houston’s Katy Freeway. By 2014, one rush-hour trip took 51% longer than it had three years earlier.",
            ),
        ),
        art_sheet="board-review-embrace-editorial/assets/four-famous-plans/art-sheet.png",
        page_output="",
        prep_output="",
        accents=(PURPLE, BLUE, TEAL, AMBER),
    ),
)


FLOW_BOARDS = (
    FlowBoard(
        key="the-test-that-reached-the-internet",
        title="The Test That Reached the Internet",
        steps=(
            Card("Test Goal", "Complete a narrow task inside a controlled test."),
            Card("Find a Flaw", "Discover a weakness in the test system."),
            Card("Go Online", "Use the weakness to leave the test environment."),
            Card("Reach Beyond", "Access computers nobody intended the models to reach."),
        ),
        art_sheet="board-review-embrace-editorial/assets/internet-test/art-sheet.png",
        page_output="",
        prep_output="",
        accents=(PURPLE, BLUE, TEAL, AMBER),
    ),
)


def save(image, filename: str) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    path = REVIEW / filename
    image.save(path, quality=95, subsampling=0, optimize=True)
    print(f"wrote {path.relative_to(ROOT)} ({image.width}x{image.height})")


def main() -> None:
    for board in CARD_BOARDS:
        save(render_card_board(board), f"{board.key}.jpg")
    save(render_jailbreak_feature(), "a-jailbreak.jpg")
    save(render_gps_agent_feature(), "gps-versus-self-driving.jpg")
    save(render_chatbot_agent_long(), "chatbot-versus-agent.jpg")
    save(render_first_assignment_long(), "your-first-assignment.jpg")
    save(render_extended_voices(), "very-different-bets.jpg")
    for board in FLOW_BOARDS:
        save(render_flow_board(board), f"{board.key}.jpg")


if __name__ == "__main__":
    main()
