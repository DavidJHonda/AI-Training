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

from render_embrace_editorial_batch import (
    BLUE,
    BODY,
    CARD_BORDER_OPACITY,
    CARD_RADIUS,
    CARDS_TOP,
    FRAME,
    INK,
    PURPLE,
    TEAL,
    WHITE,
    Card,
    CardBoard,
    FlowBoard,
    accent_wash,
    cover,
    draw_shadow,
    face,
    mix_with_white,
    multiline,
    render_card_board,
    render_flow_board,
    split_art_sheet,
    top_round_mask,
    wrap,
)


ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "board-review-embrace-editorial"


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
    title_font = face("heavy", 56)
    role_font = face("heavy", 20)
    name_font = face("heavy", 40)
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
        assert measure.textlength(voice.name, font=name_font) <= text_width
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
    draw.text((40, 36), "Even the Experts Don’t Know", font=title_font, fill=INK)

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
        draw.text((text_x, text_y), voice.name, font=name_font, fill=accent)
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


CARD_BOARDS = (
    CardBoard(
        key="this-has-happened-before",
        title="This Has Happened Before",
        cards=(
            Card(
                "Online Shopping",
                "In 1995, Clifford Stoll said online shopping could not compete with malls. It became part of everyday life.",
            ),
            Card(
                "No Chance for the iPhone",
                "In 2007, Steve Ballmer said the iPhone had no chance at meaningful market share. It reshaped smartphones.",
            ),
            Card(
                "The Internet Will Collapse",
                "In 1996, Robert Metcalfe predicted a catastrophic collapse. The internet became essential infrastructure.",
            ),
            Card(
                "Flying Cars Are Coming",
                "In 1940, Henry Ford predicted a flying car was coming. It still has not become ordinary transportation.",
            ),
        ),
        art_sheet="board-review-embrace-editorial/assets/failed-predictions/art-sheet.png",
        page_output="",
        prep_output="",
        takeaway="The future is hard to predict because people change the result.",
    ),
    CardBoard(
        key="a-jailbreak",
        title="A Jailbreak",
        cards=(
            Card(
                "Defenders",
                "Must protect many possible paths into the model.",
            ),
            Card(
                "An Attacker",
                "Needs to find only one opening.",
            ),
        ),
        art_sheet="board-review-embrace-editorial/assets/jailbreak/art-sheet.png",
        page_output="",
        prep_output="",
        takeaway="New methods keep surfacing, making this an ongoing game of cat-and-mouse.",
    ),
    CardBoard(
        key="gps-versus-self-driving",
        title="GPS versus Self-Driving Car",
        cards=(
            Card(
                "Drive with GPS",
                "It knows the route and calls out every turn. You do the driving and catch mistakes as they happen.",
            ),
            Card(
                "Self-Driving Car",
                "It follows the route and reroutes on its own. You may not catch a mistake until the trip is over.",
            ),
        ),
        art_sheet="board-review-embrace-editorial/assets/gps-vs-self-driving/art-sheet.png",
        page_output="",
        prep_output="",
        takeaway="Regular AI gives advice. An agent takes action.",
    ),
    CardBoard(
        key="chatbot-versus-agent",
        title="Ask a Chatbot versus Hire an Agent",
        cards=(
            Card(
                "Ask a Chatbot",
                "It writes a caption when asked. You find the clips, build the post, and decide when to share it.",
            ),
            Card(
                "Hire an Agent",
                "It selects the clips, makes the reel, writes the caption, and posts while you are somewhere else.",
            ),
        ),
        art_sheet="board-review-embrace-editorial/assets/chatbot-vs-agent/art-sheet.png",
        page_output="",
        prep_output="",
        takeaway="You ask, and an agent does the work for you.",
    ),
    CardBoard(
        key="your-first-assignment",
        title="Your First Assignment",
        cards=(
            Card(
                "Before AI",
                "You spend the week reading 500 reviews, organizing the data, and building the deck. Analysis finally begins on Friday.",
            ),
            Card(
                "With AI",
                "AI handles the first pass in minutes. You spend the week investigating why and recommending the fix.",
            ),
        ),
        art_sheet="board-review-embrace-editorial/assets/first-assignment/art-sheet.png",
        page_output="",
        prep_output="",
        takeaway="AI handles the busy work. You focus on what matters.",
    ),
    CardBoard(
        key="four-famous-plans",
        title="Four Famous Plans",
        cards=(
            Card(
                "Text Messaging",
                "Built as a 160-character testing utility. It became a generation’s main way to communicate.",
                "BETTER THAN PREDICTED",
            ),
            Card(
                "GPS",
                "Built to guide military ships, planes, and missiles. It put maps, ride-hailing, and location tools in every pocket.",
                "BETTER THAN PREDICTED",
            ),
            Card(
                "Cane Toads",
                "Imported to eat crop-destroying beetles. They ignored the beetles and spread by the millions.",
                "WORSE THAN PREDICTED",
            ),
            Card(
                "Wider Highways",
                "Built to end congestion. More lanes drew more drivers, and commutes became slower.",
                "WORSE THAN PREDICTED",
            ),
        ),
        art_sheet="board-review-embrace-editorial/assets/four-famous-plans/art-sheet.png",
        page_output="",
        prep_output="",
        takeaway="The biggest results are often the ones nobody predicted.",
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
            Card("Reach Systems", "Access computers nobody intended the models to reach."),
        ),
        art_sheet="board-review-embrace-editorial/assets/internet-test/art-sheet.png",
        page_output="",
        prep_output="",
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
    save(render_extended_voices(), "very-different-bets.jpg")
    for board in FLOW_BOARDS:
        save(render_flow_board(board), f"{board.key}.jpg")


if __name__ == "__main__":
    main()
