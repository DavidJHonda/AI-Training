#!/usr/bin/env python3
"""Render deterministic illustrated boards for the People Skills and Creative Thinking lessons."""

import math

from render_editorial_board_refresh import (
    BLUE,
    PURPLE,
    TEAL,
    WHITE,
    art_stage,
    draw_chat,
    draw_check,
    draw_chip,
    draw_document,
    draw_heart,
    draw_magnifier,
    draw_sound_wave,
    open_columns,
    open_two_by_two,
    rounded,
    save_all,
    tint,
)


def art_same_tools(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, width=320, height=210)
    for offset in (-106, 0, 106):
        draw_chip(draw, cx + offset, cy, accent, 0.48 * scale)


def art_trust(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, width=310, height=210)
    for offset in (-112, 112):
        draw.line((cx + offset, cy, cx + (-48 if offset < 0 else 48), cy), fill=accent, width=6)
        draw.ellipse(
            (cx + offset - 20, cy - 20, cx + offset + 20, cy + 20),
            fill=WHITE,
            outline=accent,
            width=5,
        )
    shield = [
        (cx, cy - 88),
        (cx + 68, cy - 58),
        (cx + 58, cy + 30),
        (cx, cy + 88),
        (cx - 58, cy + 30),
        (cx - 68, cy - 58),
    ]
    draw.polygon(shield, fill=tint(accent, 0.68), outline=accent)
    draw.line(shield + [shield[0]], fill=accent, width=5, joint="curve")
    draw_check(draw, cx, cy, accent, 1.35 * scale)


def art_connection(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, width=330, height=220)
    draw_chat(draw, cx - 56, cy + 18, PURPLE, 0.68 * scale)
    draw_chat(draw, cx + 60, cy - 26, accent, 0.68 * scale, heart=True)


def art_listen(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, width=235, height=135)
    draw_chat(draw, cx - 35, cy, accent, 0.55 * scale)
    draw_sound_wave(draw, cx + 72, cy, accent, 0.48 * scale)


def art_notice(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, width=235, height=135)
    draw_chat(draw, cx - 30, cy, accent, 0.52 * scale)
    draw_magnifier(draw, cx + 55, cy + 18, accent, 0.52 * scale)


def art_value(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, width=235, height=135)
    draw_document(draw, cx - 24, cy, accent, 0.50 * scale, highlighted=True)
    draw_heart(draw, cx + 62, cy - 6, accent, 0.52 * scale)


def art_disagree(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, width=255, height=140)
    draw_chat(draw, cx - 54, cy + 10, PURPLE, 0.46 * scale)
    draw_chat(draw, cx + 58, cy - 10, accent, 0.46 * scale)
    draw_check(draw, cx + 2, cy + 48, TEAL, 0.58 * scale)


def art_lawyer(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, width=235, height=135)
    draw_document(draw, cx - 62, cy + 4, accent, 0.48 * scale, highlighted=True)
    draw.line((cx + 42, cy - 48, cx + 42, cy + 49), fill=accent, width=7)
    draw.line((cx - 18, cy - 26, cx + 102, cy - 26), fill=accent, width=7)
    for x in (cx - 8, cx + 92):
        draw.line((x, cy - 25, x - 20, cy + 15), fill=accent, width=4)
        draw.line((x, cy - 25, x + 20, cy + 15), fill=accent, width=4)
        draw.arc((x - 25, cy - 2, x + 25, cy + 38), 0, 180, fill=accent, width=5)


def art_entrepreneur(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, width=235, height=135)
    draw_lightbulb(draw, cx, cy - 4, accent, scale)
    draw.line((cx + 72, cy + 44, cx + 116, cy), fill=accent, width=6)
    draw.line((cx + 116, cy, cx + 116, cy + 30), fill=accent, width=6)
    draw.line((cx + 116, cy, cx + 86, cy), fill=accent, width=6)


def draw_lightbulb(draw, cx, cy, accent, scale=1.0):
    draw.ellipse((cx - 42, cy - 64, cx + 42, cy + 20), fill=tint(accent, 0.72), outline=accent, width=5)
    draw.rounded_rectangle((cx - 24, cy + 12, cx + 24, cy + 54), radius=8, fill=WHITE, outline=accent, width=5)
    for angle in (-72, -40, 0, 40, 72):
        radians = math.radians(angle - 90)
        x1 = cx + math.cos(radians) * 62
        y1 = cy - 22 + math.sin(radians) * 62
        x2 = cx + math.cos(radians) * 82
        y2 = cy - 22 + math.sin(radians) * 82
        draw.line((x1, y1, x2, y2), fill=accent, width=5)


def art_engineer(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, width=235, height=135)
    for x, y, r in ((cx - 45, cy + 4, 42), (cx + 48, cy - 22, 34), (cx + 66, cy + 51, 24)):
        draw.ellipse((x - r, y - r, x + r, y + r), fill=tint(accent, 0.72), outline=accent, width=5)
        draw.ellipse((x - r * 0.35, y - r * 0.35, x + r * 0.35, y + r * 0.35), fill=WHITE, outline=accent, width=4)
        for dx, dy in ((-r - 10, -8), (r - 2, -8), (-8, -r - 10), (-8, r - 2)):
            draw.rounded_rectangle((x + dx, y + dy, x + dx + 18, y + dy + 18), radius=4, fill=accent)


def art_doctor(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy, accent, width=235, height=135)
    draw.rounded_rectangle((cx - 94, cy - 48, cx + 12, cy + 58), radius=18, fill=WHITE, outline=accent, width=5)
    draw.rectangle((cx - 50, cy - 28, cx - 31, cy + 38), fill=accent)
    draw.rectangle((cx - 74, cy - 4, cx - 7, cy + 15), fill=accent)
    draw_magnifier(draw, cx + 67, cy + 12, accent, 0.54 * scale)


def art_generate(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy + 8, accent, width=210, height=108)
    cards = [(-78, 14), (-40, -2), (0, -12), (40, -2), (78, 14)]
    for i, (dx, dy) in enumerate(cards):
        x, y = cx + dx, cy + dy
        fill = tint(accent, 0.72 if i == 2 else 0.84)
        draw.rounded_rectangle((x - 23, y - 31, x + 23, y + 31), radius=7, fill=fill, outline=accent, width=4)
        draw.line((x - 12, y - 10, x + 12, y - 10), fill=accent, width=3)
        draw.line((x - 12, y, x + 8, y), fill=accent, width=3)
        draw.line((x - 12, y + 10, x + 12, y + 10), fill=accent, width=3)


def art_what_if(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy + 8, accent, width=210, height=108)
    draw.rounded_rectangle((cx - 30, cy - 28, cx + 30, cy + 32), radius=14, fill=tint(accent, 0.7), outline=accent, width=4)
    for end_x, end_y in ((cx - 82, cy - 32), (cx + 82, cy - 32), (cx, cy + 54)):
        draw.line((cx, cy, end_x, end_y), fill=accent, width=5)
        draw.ellipse((end_x - 12, end_y - 12, end_x + 12, end_y + 12), fill=WHITE, outline=accent, width=4)


def art_combine(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy + 8, accent, width=210, height=108)
    draw_chip(draw, cx - 70, cy + 4, PURPLE, 0.31 * scale)
    draw_document(draw, cx + 70, cy + 4, accent, 0.33 * scale, highlighted=True)
    draw.line((cx - 40, cy + 4, cx - 20, cy + 4), fill=accent, width=5)
    draw.line((cx + 20, cy + 4, cx + 40, cy + 4), fill=accent, width=5)
    draw.ellipse((cx - 25, cy - 14, cx + 6, cy + 17), outline=accent, width=5)
    draw.ellipse((cx - 6, cy - 14, cx + 25, cy + 17), outline=accent, width=5)


def art_step_away(draw, cx, cy, accent, scale):
    art_stage(draw, cx, cy + 8, accent, width=210, height=108)
    draw_document(draw, cx - 75, cy + 4, accent, 0.32 * scale)
    draw.ellipse((cx - 30, cy - 26, cx + 30, cy + 34), fill=WHITE, outline=accent, width=5)
    draw.line((cx, cy + 4, cx, cy - 12), fill=accent, width=5)
    draw.line((cx, cy + 4, cx + 13, cy + 13), fill=accent, width=5)
    draw_document(draw, cx + 75, cy + 4, accent, 0.32 * scale, highlighted=True)
    draw.line((cx - 45, cy + 4, cx - 34, cy + 4), fill=accent, width=4)
    draw.line((cx + 34, cy + 4, cx + 45, cy + 4), fill=accent, width=4)


def render_why_people_skills_matter():
    image = open_columns(
        "Why people skills matter more in the AI future",
        [
            (
                "THE TOOL ISN’T THE DIFFERENCE",
                "When everyone has AI, polished work becomes common. How you work with people stands out.",
            ),
            (
                "TRUST STILL MATTERS",
                "People choose teammates and leaders who listen, keep promises, and treat others well.",
            ),
            (
                "HUMAN CONNECTION GAINS VALUE",
                "The more work AI handles, the more listening, empathy, and real interaction stand out.",
            ),
        ],
        [art_same_tools, art_trust, art_connection],
        accents=[PURPLE, BLUE, TEAL],
        heading_size=30,
        body_size=29,
        heading_top_override=226,
        body_top_overrides=[314, 298, 314],
        art_y=666,
        art_scale=1.0,
        show_rule=False,
    )
    save_all(
        image,
        [
            "board-review-first-four/alternatives/build-your-skills/people-skills-why-matter-alternative.jpg",
            "illustrations/people-skills-why-matter.jpg",
        ],
    )


def render_four_ways_to_practice():
    image = open_two_by_two(
        "Four ways to practice",
        [
            (
                "Listen to understand",
                "Do not plan your reply while the other person is talking. Ask one genuine follow-up question before offering your opinion.",
            ),
            (
                "Notice what isn’t being said",
                "Pay attention to tone, hesitation, enthusiasm, and changes in behavior. Before assuming what is wrong, ask.",
            ),
            (
                "Show people they matter",
                "Remember what they tell you, give specific appreciation, and give people credit when an idea is theirs.",
            ),
            (
                "Disagree without making it personal",
                "Address difficult things directly and calmly. Challenge the idea or behavior without attacking the person.",
            ),
        ],
        [art_listen, art_notice, art_value, art_disagree],
        accents=[PURPLE, BLUE, TEAL, "#ed8708"],
        heading_size=29,
        body_size=27,
        body_width=610,
        center_groups=False,
    )
    save_all(
        image,
        [
            "board-review-first-four/alternatives/build-your-skills/people-skills-four-ways-alternative.jpg",
            "illustrations/people-skills-four-ways.jpg",
        ],
    )


def render_creative_professions():
    image = open_two_by_two(
        "Who thinks creatively?",
        [
            (
                "A lawyer",
                "Finds a strategy nobody else saw in the same case file. Same laws and facts, different approach.",
            ),
            (
                "An entrepreneur",
                "Spots a need everyone else overlooked and builds a new way to meet it.",
            ),
            (
                "An engineer",
                "Finds a solution when the standard approach cannot solve the problem.",
            ),
            (
                "A doctor",
                "Looks at the same symptoms and considers a diagnosis others missed.",
            ),
        ],
        [art_lawyer, art_entrepreneur, art_engineer, art_doctor],
        accents=[PURPLE, BLUE, TEAL, "#ed8708"],
        heading_size=31,
        body_size=28,
        body_width=610,
        center_groups=False,
    )
    save_all(
        image,
        [
            "board-review-first-four/alternatives/build-your-skills/creative-thinking-professions-alternative.jpg",
            "illustrations/creative-thinking-professions.jpg",
        ],
    )


def render_creative_practice():
    image = open_two_by_two(
        "Four ways to think creatively",
        [
            (
                "Generate before you judge",
                "List several ideas, including bad ones, before deciding what works. The obvious ideas usually arrive first.",
            ),
            (
                "Ask “What if?”",
                "Change one rule or assumption. Ask what would happen if the opposite were true.",
            ),
            (
                "Connect unrelated things",
                "Borrow a pattern, feature, or approach from somewhere completely different and apply it to the problem.",
            ),
            (
                "Step away, then return",
                "Work on the problem, then take a walk or switch activities. New connections often appear after your attention moves elsewhere.",
            ),
        ],
        [art_generate, art_what_if, art_combine, art_step_away],
        accents=[PURPLE, BLUE, TEAL, "#ed8708"],
        heading_size=29,
        body_size=27,
        body_width=610,
        center_groups=False,
    )
    save_all(
        image,
        [
            "board-review-first-four/alternatives/build-your-skills/creative-thinking-practice-alternative.jpg",
            "illustrations/creative-thinking-practice.jpg",
        ],
    )


def main():
    render_why_people_skills_matter()
    render_four_ways_to_practice()
    render_creative_professions()
    render_creative_practice()


if __name__ == "__main__":
    main()
