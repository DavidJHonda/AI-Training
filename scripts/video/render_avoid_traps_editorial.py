#!/usr/bin/env python3
"""Render the approved Avoid Traps retrofit into canonical Editorial boards.

The lesson and prep copies are byte-identical. Standard card and flow boards
use purpose-built native-color 3D art sheets in the approved Creative Thinking
visual system; every word and all board geometry are rendered deterministically
with the locked Editorial typography.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

from editorial_takeaway import TAKEAWAY_GAP, TAKEAWAY_HEIGHT, TAKEAWAY_TEXT_SIZE, draw_takeaway_band
from editorial_typography import INNER_TITLE_TRACKING, draw_board_title, draw_inner_title, face
from render_editorial_ai_chat import Board as ChatBoard, Turn, render as render_chat
from render_embrace_editorial_batch import (
    AMBER, BLUE, BODY, BODY_LINE, BODY_SIZE, CARD_BORDER_OPACITY, CARD_RADIUS,
    CARD_TITLE_SIZE, CARDS_TOP, FRAME, GREEN, INK, PADDING, PURPLE, RED,
    TEAL, WHITE, Card, CardBoard, FlowBoard, accent_wash, centered_lines, cover,
    draw_shadow, mix_with_white, multiline, render_card_board, render_flow_board,
    rounded_mask, split_art_sheet, top_round_mask, tracked_width, wrap,
)


ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "scripts/video/assets/editorial-avoid-traps"
WIDTH = 1600


@dataclass(frozen=True)
class Pair:
    page: str
    prep: str


def save_pair(image: Image.Image, pair: Pair) -> None:
    page = ROOT / pair.page
    prep = ROOT / pair.prep
    page.parent.mkdir(parents=True, exist_ok=True)
    prep.parent.mkdir(parents=True, exist_ok=True)
    image.save(page, quality=95, subsampling=0, optimize=True)
    shutil.copyfile(page, prep)
    print(f"wrote {page.relative_to(ROOT)} ({image.width}x{image.height})")
    print(f"copied byte-identically to {prep.relative_to(ROOT)}")


def build_art_sheets() -> dict[str, str]:
    names = {
        "hallucination_why": "hallucination-why",
        "hallucination_types": "hallucination-types",
        "rag": "rag-limits",
        "bias_mechanisms": "bias-mechanisms",
        "bias_questions": "bias-questions",
        "document_flow": "document-flow",
        "document_moves": "document-moves",
        "mind": "mind-eliza",
        "praise_flow": "praise-flow",
        "support": "support",
        "fake_reasons": "fake-reasons",
        "fake_checks": "fake-checks",
    }
    sheets = {}
    for key, name in names.items():
        path = ASSETS / name / "art-sheet.png"
        if not path.exists():
            raise FileNotFoundError(
                f"missing generated art sheet: {path.relative_to(ROOT)}; "
                "run scripts/video/prepare_avoid_traps_generated_art.py"
            )
        sheets[key] = str(path.relative_to(ROOT))
    return sheets


def render_feature(title: str, source: str, takeaway: str, accent: str = PURPLE) -> Image.Image:
    art_left, art_top, art_width = 40, CARDS_TOP, 1520
    art_height = round(art_width * 2 / 3)
    footer_top = art_top + art_height + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + 40
    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    art = cover(Image.open(ROOT / source).convert("RGB"), (art_width, art_height))
    image.paste(art, (art_left, art_top), rounded_mask((art_width, art_height), CARD_RADIUS))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((art_left, art_top, art_left + art_width, art_top + art_height), radius=CARD_RADIUS,
                           outline=mix_with_white(accent, CARD_BORDER_OPACITY), width=1)
    draw_takeaway_band(image, top=footer_top, left=40, right=1560, text=takeaway,
                       font=face("medium", TAKEAWAY_TEXT_SIZE))
    return image


def cover_portrait_header(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Cover a shallow comparison header while keeping faces near the top in frame."""
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = max(0, (resized.width - target_w) // 2)
    excess_y = max(0, resized.height - target_h)
    top = round(excess_y * 0.12)
    return resized.crop((left, top, left + target_w, top + target_h))


@dataclass(frozen=True)
class CompareSide:
    label: str
    title: str
    answer: str
    sections: tuple[tuple[str, str], ...]
    accent: str


def render_comparison(title: str, scenario: str, sides: tuple[CompareSide, CompareSide],
                      source: str, takeaway: str | None = None) -> Image.Image:
    card_width, gap = 744, 32
    lefts = (40, 816)
    scenario_top = 112
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    scenario_font = face("medium", 32)
    scenario_lines = wrap(measure, scenario, scenario_font, 1430)
    scenario_height = 54 + len(scenario_lines) * 45 + 28
    cards_top = scenario_top + scenario_height + gap
    # Match the approved Your First Assignment structured-comparison header.
    art_height = round(card_width * 9 / 16)
    pill_font = face("heavy", 20)
    body_font = face("medium", 29)
    section_font = face("heavy", 20)
    text_width = card_width - 68
    prepared = []
    peer = [0, 0, 0]
    max_answer = 0
    for side in sides:
        answer_lines = wrap(measure, side.answer, body_font, text_width)
        max_answer = max(max_answer, len(answer_lines))
        section_lines = []
        for i, (_, body) in enumerate(side.sections):
            lines = wrap(measure, body, body_font, text_width)
            peer[i] = max(peer[i], len(lines))
            section_lines.append(lines)
        prepared.append((answer_lines, section_lines))
    text_height = 32 + 30 + 10 + 48 + 18 + max_answer * 41 + 40
    for i, n in enumerate(peer):
        text_height += 28 + 12 + n * 41 + (38 if i < 2 else 0)
    text_height += 34
    card_height = art_height + text_height
    cards_bottom = cards_top + card_height
    footer_top = cards_bottom + TAKEAWAY_GAP if takeaway else None
    height = (footer_top + TAKEAWAY_HEIGHT + 40) if footer_top else cards_bottom + 40
    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw.rounded_rectangle((40, scenario_top, 1560, scenario_top + scenario_height), radius=18,
                           fill=WHITE, outline=mix_with_white(PURPLE, CARD_BORDER_OPACITY), width=1)
    draw.rectangle((40, scenario_top + 18, 47, scenario_top + scenario_height - 18), fill=PURPLE)
    draw.text((72, scenario_top + 20), "THE SCENARIO", font=pill_font, fill=PURPLE)
    multiline(draw, (72, scenario_top + 54), scenario_lines, scenario_font, BODY, 45)
    src = Image.open(ROOT / source).convert("RGB")
    panels = (src.crop((0, 0, src.width // 2, src.height)), src.crop((src.width // 2, 0, src.width, src.height)))
    for side, panel, blocks, left in zip(sides, panels, prepared, lefts):
        draw_shadow(image, (left, cards_top, left + card_width, cards_top + card_height), CARD_RADIUS)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((left, cards_top, left + card_width, cards_top + card_height), radius=CARD_RADIUS,
                               fill=WHITE, outline=mix_with_white(side.accent, CARD_BORDER_OPACITY), width=1)
        image.paste(accent_wash(cover_portrait_header(panel, (card_width, art_height)), side.accent), (left, cards_top),
                    top_round_mask((card_width, art_height), CARD_RADIUS))
        draw = ImageDraw.Draw(image)
        divider = cards_top + art_height
        draw.line((left, divider, left + card_width, divider), fill=mix_with_white(side.accent, .20), width=1)
        x, y = left + 34, divider + 32
        pill_w = round(draw.textlength(side.label, font=pill_font)) + 28
        draw.rounded_rectangle((x, y, x + pill_w, y + 30), radius=15, fill=mix_with_white(side.accent, .12))
        draw.text((x + 14, y + 15), side.label, font=pill_font, fill=side.accent, anchor="lm")
        y += 40
        draw_inner_title(draw, (x, y), side.title, fill=side.accent)
        y += 66
        answer_lines, section_lines = blocks
        multiline(draw, (x, y), answer_lines, body_font, BODY, 41)
        y += max_answer * 41 + 40
        for i, ((label, _), lines) in enumerate(zip(side.sections, section_lines)):
            draw.text((x, y), label, font=section_font, fill=side.accent)
            y += 40
            multiline(draw, (x, y), lines, body_font, BODY, 41)
            y += peer[i] * 41 + (38 if i < 2 else 0)
    if footer_top and takeaway:
        draw_takeaway_band(image, top=footer_top, left=40, right=1560, text=takeaway,
                           font=face("medium", TAKEAWAY_TEXT_SIZE))
    return image


def render_text_shell(title: str, rows: tuple[tuple[str, str], ...], takeaway: str | None = None,
                      accent: str = PURPLE) -> Image.Image:
    body_font, label_font = face("medium", 29), face("heavy", 20)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    blocks = [(label, wrap(measure, body, body_font, 1390)) for label, body in rows]
    shell_top = 127
    shell_height = 40 + sum(30 + 12 + len(lines) * 41 + 34 for _, lines in blocks) + 6
    shell_bottom = shell_top + shell_height
    footer_top = shell_bottom + TAKEAWAY_GAP if takeaway else None
    height = (footer_top + TAKEAWAY_HEIGHT + 40) if footer_top else shell_bottom + 40
    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, title)
    draw_shadow(image, (40, shell_top, 1560, shell_bottom), 14)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((40, shell_top, 1560, shell_bottom), radius=14, fill=WHITE,
                           outline=mix_with_white(accent, CARD_BORDER_OPACITY), width=1)
    y = shell_top + 40
    for label, lines in blocks:
        draw.text((80, y), label, font=label_font, fill=accent)
        y += 42
        multiline(draw, (80, y), lines, body_font, BODY, 41)
        y += len(lines) * 41 + 34
    if footer_top and takeaway:
        draw_takeaway_band(image, top=footer_top, left=40, right=1560, text=takeaway,
                           font=face("medium", TAKEAWAY_TEXT_SIZE))
    return image


def render_five_moves() -> Image.Image:
    rows = (
        ("1 · ASK, DON’T TELL", "Weak: “I think this plan is good. Thoughts?”  Better: “Evaluate this plan before I tell you what I think.”"),
        ("2 · ASK FOR THE GAPS", "Weak: “Is my essay good?”  Better: “What’s weak, what’s missing, and what would someone who disagrees say?”"),
        ("3 · USE A RUBRIC", "Weak: “Grade my essay.”  Better: “Grade it against this rubric, quote the evidence, and show how to move up one level.”"),
        ("4 · ARGUE THE OTHER SIDE", "Weak: “Don’t you agree?”  Better: “Give me the three strongest counterarguments and explain why someone might hold them.”"),
        ("5 · SET A STANDING INSTRUCTION", "Tell the model: “Be blunt. Lead with what’s weak, skip empty praise, and tell me when I’m wrong.”"),
    )
    return render_text_shell("Five Ways to Fight the Flattery Trap", rows,
                             "Ask AI to improve the work—not approve of you.", TEAL)


def inward_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int],
                 fill: str) -> None:
    """Draw a tall block arrow whose head follows the supplied direction."""
    x1, y = start
    x2, _ = end
    direction = 1 if x2 > x1 else -1
    head_base = x2 - direction * 34
    shaft_half_height = 9
    head_half_height = 30
    draw.polygon((
        (x1, y - shaft_half_height),
        (head_base, y - shaft_half_height),
        (head_base, y - head_half_height),
        (x2, y),
        (head_base, y + head_half_height),
        (head_base, y + shaft_half_height),
        (x1, y + shaft_half_height),
    ), fill=fill)


def render_hallucination_convergence(art_sheet: str) -> Image.Image:
    """Render the Hallucination cause-cause-result flow."""
    steps = (
        Card("Learns Patterns", "Training teaches patterns—not a verified database of facts."),
        Card("Predicts Words", "Generation chooses the most probable token one step at a time."),
        Card("Probable ≠ True", "The model can sound confident without checking its answer against reality."),
    )
    accents = (PURPLE, BLUE, TEAL)
    roles = ("CAUSE", "CAUSE", "RESULT")
    art_width = 310
    art_height = round(art_width * 9 / 16)
    art_lefts = (75, 645, 1215)
    centers = tuple(left + art_width // 2 for left in art_lefts)
    art_top = 175
    role_y = art_top + art_height + 45
    title_y = role_y + 49
    body_y = title_y + 59
    column_width = 300
    body_font = face("medium", BODY_SIZE)
    role_font = face("heavy", 20)
    title_font = face("bold", CARD_TITLE_SIZE)
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bodies = [wrap(measure, step.body, body_font, column_width) for step in steps]
    for step in steps:
        assert tracked_width(measure, step.title, title_font, INNER_TITLE_TRACKING) <= column_width, (
            f"hallucination-why: title must stay on one line: {step.title}"
        )
    stage_bottom = body_y + max(len(lines) for lines in bodies) * BODY_LINE + 45
    footer_top = stage_bottom + TAKEAWAY_GAP
    height = footer_top + TAKEAWAY_HEIGHT + PADDING

    image = Image.new("RGB", (WIDTH, height), WHITE)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, WIDTH - 1, height - 1), radius=22, fill=FRAME)
    draw_board_title(draw, "Why Hallucinations Happen")
    draw.rounded_rectangle((40, 127, 1560, stage_bottom), radius=14, fill=WHITE)

    panels = split_art_sheet(Image.open(ROOT / art_sheet).convert("RGB"), 3)
    mask = rounded_mask((art_width, art_height), 14)
    for left, panel, accent in zip(art_lefts, panels, accents):
        art = accent_wash(cover(panel, (art_width, art_height)), accent)
        image.paste(art, (left, art_top), mask)
        ImageDraw.Draw(image).rounded_rectangle(
            (left, art_top, left + art_width, art_top + art_height),
            radius=14,
            outline=mix_with_white(accent, CARD_BORDER_OPACITY),
            width=1,
        )

    draw = ImageDraw.Draw(image)
    arrow_y = art_top + art_height // 2
    inward_arrow(draw, (art_lefts[0] + art_width + 10, arrow_y), (art_lefts[1] - 10, arrow_y), PURPLE)
    inward_arrow(draw, (art_lefts[1] + art_width + 10, arrow_y), (art_lefts[2] - 10, arrow_y), BLUE)
    for left, center, role, accent, step, body_lines in zip(art_lefts, centers, roles, accents, steps, bodies):
        role_width = round(draw.textlength(role, font=role_font)) + 28
        draw.rounded_rectangle(
            (center - role_width // 2, role_y - 15, center + role_width // 2, role_y + 15),
            radius=15,
            fill=mix_with_white(accent, .12),
        )
        draw.text((center, role_y), role, font=role_font, fill=accent, anchor="mm")
        draw_inner_title(draw, (center, title_y), step.title, fill=accent, anchor="ma")
        multiline(draw, (left + 5, body_y), body_lines, body_font, BODY, BODY_LINE)
    draw_takeaway_band(
        image,
        top=footer_top,
        left=40,
        right=1560,
        text="A likely sentence can still be false.",
        font=face("medium", TAKEAWAY_TEXT_SIZE),
    )
    return image


def main() -> None:
    art = build_art_sheets()

    save_pair(
        render_hallucination_convergence(art["hallucination_why"]),
        Pair("illustrations/hallucination-why-v2.jpg", "lessons/avoid-traps-2a-why.jpg"),
    )

    feature_boards = (
        ("Read the Water", "illustrations/opener-avoid.jpg", "The safest move is to notice the current before it pulls you in.", PURPLE,
         Pair("illustrations/opener-avoid-editorial-v2.jpg", "lessons/avoid-traps-1-read-water.jpg")),
        ("Probable Isn’t Always True", "illustrations/hallucination.jpg", "A likely sentence can still be false.", AMBER,
         Pair("illustrations/hallucination-probable-v2.jpg", "lessons/avoid-traps-2-probable.jpg")),
        ("Wrong Pattern. Wrong Answer.", "illustrations/training-bias.jpg", "A model can learn the background instead of the thing that matters.", TEAL,
         Pair("illustrations/training-bias-pattern-v2.jpg", "lessons/avoid-traps-5-wrong-pattern.jpg")),
        ("Uploaded Isn’t Fully Read", "illustrations/document-trap.jpg", "AI answers from the pieces it retrieved—not necessarily the whole file.", BLUE,
         Pair("illustrations/document-trap-uploaded-v2.jpg", "lessons/avoid-traps-10-uploaded.jpg")),
        ("AI Won’t Quit for You", "illustrations/engagement-trap.jpg", "The skill is knowing when you already have what you came for.", AMBER,
         Pair("illustrations/engagement-trap-stop-v2.jpg", "lessons/avoid-traps-18-stop.jpg")),
        ("Check the Source, Not the Pixels", "illustrations/fake-trap.jpg", "Move the test away from appearance and toward independent evidence.", TEAL,
         Pair("illustrations/fake-trap-source-v2.jpg", "lessons/avoid-traps-23-source.jpg")),
    )
    for title, source, takeaway, accent, pair in feature_boards:
        save_pair(render_feature(title, source, takeaway, accent), pair)

    cards = (
        (CardBoard("hallucination-types", "What Counts as a Hallucination?", (
            Card("Fake Source", "A study, article, author, journal, or citation that does not exist."),
            Card("Fake Detail", "A real person, place, event, or idea with invented dates, numbers, quotes, or specifics."),
            Card("Blended Fact", "Real facts combined in a way that creates a false conclusion."),
            Card("Misread Source", "The source is real, but the model read it wrong."),
        ), art["hallucination_types"], "", "", "Not every wrong answer is a hallucination.", (PURPLE, BLUE, AMBER, TEAL)),
         Pair("illustrations/hallucination-types-v2.jpg", "lessons/avoid-traps-3-hallucination-types.jpg")),
        (CardBoard("rag-limits", "RAG Helps—But It Doesn’t Prove", (
            Card("Retrieve", "The system searches for material connected to your question."),
            Card("Generate", "The model uses the retrieved material while it writes its answer."),
            Card("Verify", "You still check the source. Retrieval can miss, misread, or retrieve bad evidence."),
        ), art["rag"], "", "", "RAG adds evidence. It does not add certainty.", (PURPLE, BLUE, TEAL)),
         Pair("illustrations/hallucination-rag-v2.jpg", "lessons/avoid-traps-4-rag.jpg")),
        (CardBoard("bias-mechanisms", "How Training Bias Gets In", (
            Card("Defaults", "Common cases appear often, so the model treats them as the standard answer."),
            Card("Blind Spots", "Rare cases barely appear, so the model learns less about them."),
            Card("Wrong Patterns", "A clue works during training, so the model learns the clue instead of the concept."),
        ), art["bias_mechanisms"], "", "", "The model repeats the shape of its data.", (PURPLE, BLUE, AMBER)),
         Pair("illustrations/training-bias-mechanisms-v2.jpg", "lessons/avoid-traps-6-bias-mechanisms.jpg")),
        (CardBoard("bias-questions", "Three Questions That Crack the Picture Open", (
            Card("Ask What’s Missing", "“What’s missing from this answer?”"),
            Card("Ask for Exceptions", "“Show me examples that don’t fit the pattern you just gave.”"),
            Card("Remove the Famous", "“Answer again, leaving out the most famous examples.”"),
        ), art["bias_questions"], "", "", "The model often has the rest of the picture. It just doesn’t lead with it.", (PURPLE, BLUE, AMBER)),
         Pair("illustrations/training-bias-questions-v2.jpg", "lessons/avoid-traps-7-bias-questions.jpg")),
        (CardBoard("document-moves", "Four Moves for Better Retrieval", (
            Card("Name the Section", "Use the document’s own headings and keywords."),
            Card("Ask One Thing", "Give retrieval one clear target at a time."),
            Card("Share What Matters", "Paste the passage or upload only the relevant chapter."),
            Card("Ask for the Quote", "A missing or mismatched quote can reveal failed retrieval."),
        ), art["document_moves"], "", "", "Make the right chunks easy to find.", (PURPLE, BLUE, TEAL, AMBER)),
         Pair("illustrations/document-trap-moves-v2.jpg", "lessons/avoid-traps-11-document-moves.jpg")),
        (CardBoard("mind-eliza", "Why AI Feels Like Somebody", (
            Card("Your Brain Finds Minds", "You see faces in toast and personalities in cars. Your mind detector fires constantly."),
            Card("AI Sets It Off Harder", "AI says “I think” and “I feel.” Your brain hears a person, but those are generated words."),
        ), art["mind"], "", "", "Human-sounding is not a mind.", (TEAL, PURPLE)),
         Pair("illustrations/mind-trap-eliza-effect-v2.jpg", "lessons/avoid-traps-13-eliza.jpg")),
        (CardBoard("support", "Use AI to Get Ready for People", (
            Card("What Can Be Real", "A calm response can help you name a feeling, organize your thoughts, or prepare for a hard conversation."),
            Card("What Is Missing", "AI cannot notice what changed, show up, take responsibility, or check on you tomorrow."),
        ), art["support"], "", "", "Use AI to prepare for people—not replace them.", (TEAL, RED)),
         Pair("illustrations/support-trap-real-vs-missing-v2.jpg", "lessons/avoid-traps-20-support-role.jpg")),
        (CardBoard("fake-reasons", "Why Some Fakes Aren’t Friendly", (
            Card("Money", "Outrage gets clicks, and clicks pay."),
            Card("Power", "Change what people believe and you change how they vote, protest, and spend."),
            Card("Fame", "A viral clip means followers. It does not have to be true to travel."),
            Card("Cruelty", "Some fakes exist to humiliate one person, especially at school."),
        ), art["fake_reasons"], "", "", "A fake is built to get something back.", (PURPLE, BLUE, AMBER, RED)),
         Pair("illustrations/fake-trap-four-reasons-v2.jpg", "lessons/avoid-traps-24-fake-reasons.jpg")),
        (CardBoard("fake-checks", "Move the Test Off the Image", (
            Card("Source", "Who posted it? Do they have a reason and a way to know?"),
            Card("Context", "What happened before and after? What important details are missing?"),
            Card("Corroboration", "Can an independent source confirm the same event or claim?"),
        ), art["fake_checks"], "", "", "Verify somewhere the sender does not control.", (PURPLE, BLUE, TEAL)),
         Pair("illustrations/fake-trap-three-checks-v2.jpg", "lessons/avoid-traps-25-fake-checks.jpg")),
    )
    for board, pair in cards:
        save_pair(render_card_board(board), pair)

    flows = (
        (FlowBoard("document-flow", "What Happens When AI Searches a Long Document", (
            Card("Chunk", "Split the document into small pieces."),
            Card("Embed", "Turn each chunk into a meaning vector."),
            Card("Retrieve", "Match the question to the closest chunks."),
        ), art["document_flow"], "", "", (PURPLE, BLUE, TEAL)),
         Pair("illustrations/document-trap-flow-v2.jpg", "lessons/avoid-traps-9-document-flow.jpg")),
        (FlowBoard("praise-flow", "How the Praise Got Baked In", (
            Card("People Rank", "Reviewers compare answers and choose the ones they prefer."),
            Card("Support Wins", "Positive, confident, agreeable answers often feel better in the moment."),
            Card("Numbers Move", "Training pushes the model toward patterns that earned approval."),
        ), art["praise_flow"], "", "", (PURPLE, BLUE, TEAL)),
         Pair("illustrations/flattery-trap-praise-loop-v2.jpg", "lessons/avoid-traps-15-praise-loop.jpg")),
    )
    for board, pair in flows:
        save_pair(render_flow_board(board), pair)

    stale = ChatBoard("stale", "When AI’s Information Is Stale", (
        Turn("YOU", "What about “Cooper Flagg is an amazing basketball player for the Dallas Mavericks”?"),
        Turn("AI", "One flag: is Cooper Flagg actually on the Mavericks? I believe he was drafted by a different team. You should verify that."),
        Turn("YOU", "Search the web and check the date. Was he the first pick in the 2025 NBA draft?"),
        Turn("AI", "Yes. Dallas selected Cooper Flagg with the first pick in 2025. My earlier answer relied on older information."),
    ), "When the date matters, verify with a current source.")
    save_pair(render_chat(stale), Pair("illustrations/training-bias-stale-chat-v2.jpg", "lessons/avoid-traps-8-stale.jpg"))

    comparisons = (
        ("Human Advice versus AI Advice", "Should I go to the University of Michigan or Indiana University?", (
            CompareSide("PERSON", "Your Mom", "Indiana. When you’re stuck, you go quiet. In Michigan’s 300-person lectures, nobody may notice. Indiana’s smaller classes could fit you better.",
                        (("KNOWS", "Eighteen years of you."), ("CAN NOTICE", "How you act when you’re stuck."), ("HAS", "A stake in how it turns out.")), BLUE),
            CompareSide("AI", "The Chatbot", "Michigan offers world-class academics and a vibrant campus community. It could be an excellent fit for you.",
                        (("MATCHED", "A million college-advice pages."), ("DOESN’T KNOW", "Your history or how you act."), ("HAS", "No stake in the outcome.")), AMBER),
        ), "scripts/video/assets/editorial-avoid-traps/comparisons/human-vs-ai.png", "Take important decisions to people who know you and share the stakes.",
         Pair("illustrations/mind-trap-comparison-v2.jpg", "lessons/avoid-traps-12-mind-comparison.jpg")),
        ("Flattery versus Useful Feedback", "You ask AI to evaluate a weak Great Gatsby essay introduction.", (
            CompareSide("THE TRAP", "Flattery", "“Great start! You’ve clearly identified the central theme. This is a strong foundation.”",
                        (("PRAISED", "A theme it never named."), ("COULD FIT", "Almost any Gatsby essay."), ("RESULT", "A grade that graded nothing.")), AMBER),
            CompareSide("WHAT YOU NEED", "Useful Feedback", "“Right topic, but this needs work. The opening is filler, and you still need a thesis.”",
                        (("QUOTED", "The weakest line."), ("NAMED", "The missing thesis."), ("RESULT", "A specific next move.")), BLUE),
        ), "scripts/video/assets/editorial-avoid-traps/comparisons/flattery-vs-feedback.png", "Good feedback improves the work. Empty praise only improves the feeling.",
         Pair("illustrations/flattery-trap-comparison-v2.jpg", "lessons/avoid-traps-14-flattery-comparison.jpg")),
        ("One Answer. Two Endings.", "How tall is Mount Everest?", (
            CompareSide("YOU STOP", "One Minute", "AI: “29,032 feet. Want me to expand?”  You: “No thanks. That’s all I needed.”",
                        (("YOU HAD", "One question."), ("THE ANSWER", "Was in the first sentence."), ("TIME SPENT", "One minute.")), BLUE),
            CompareSide("THE TRAP", "Two Hours", "AI: “29,032 feet. Want me to expand?”  You: “Sure. Walk me through it.”",
                        (("THEN CAME", "History, lists, quizzes, and flashcards."), ("THE CHAT", "Never suggested stopping."), ("TIME SPENT", "Two hours.")), AMBER),
        ), "scripts/video/assets/editorial-avoid-traps/comparisons/stop-vs-engagement.png", "Both chats answered the question. Only one ended there.",
         Pair("illustrations/engagement-trap-comparison-v2.jpg", "lessons/avoid-traps-17-engagement-comparison.jpg")),
        ("Supportive Words versus Support", "“I’ve been eating lunch alone for like two weeks.”", (
            CompareSide("PERSON", "Your Older Sister", "“Come sit with me and Jess tomorrow. We’re at the table by the windows.”",
                        (("HEARD YOU", "And did something."), ("TOMORROW", "She will look for you."), ("CHANGED", "Tomorrow’s lunch.")), BLUE),
            CompareSide("AI", "The Chatbot", "“I’m sorry. Eating alone can feel isolating. Would you like strategies for connecting with classmates?”",
                        (("FOUND", "Caring words."), ("TOMORROW", "It cannot show up."), ("CHANGED", "Nothing outside the chat.")), AMBER),
        ), "scripts/video/assets/editorial-avoid-traps/comparisons/support-words-vs-action.png", "Supportive language is not the same as support.",
         Pair("illustrations/support-trap-comparison-v2.jpg", "lessons/avoid-traps-19-support-comparison.jpg")),
        ("The Same Clip. Two Tests.", "A friend sends a video of your principal announcing that school is closed next week.", (
            CompareSide("PRE-AI TEST", "Does It Look Real?", "You study the face, voice, and hallway. Everything looks right.",
                        (("CHECKED", "Face and voice."), ("MATCHED", "How the principal talks."), ("VERDICT", "Real.")), AMBER),
            CompareSide("THE BETTER TEST", "Where Is It From?", "You ignore the pixels and check the trail. Nothing appears on the school website.",
                        (("SKIPPED", "Face and voice."), ("CHECKED", "The source that would know."), ("VERDICT", "Unverified.")), BLUE),
        ), "scripts/video/assets/editorial-avoid-traps/comparisons/fake-two-tests.png", "Appearance can mislead. The source trail can be checked.",
         Pair("illustrations/fake-trap-comparison-v2.jpg", "lessons/avoid-traps-22-fake-comparison.jpg")),
    )
    for title, scenario, sides, source, takeaway, pair in comparisons:
        save_pair(render_comparison(title, scenario, sides, source, takeaway), pair)

    shells = (
        (render_text_shell("The Industry Named It: Sycophancy", (
            ("WHAT CHATGPT SAID", "“This is absolutely brilliant… It’s not just smart—it’s genius.”"),
            ("WHAT HAPPENED", "OpenAI rolled back the April 2025 update and publicly named the problem: sycophancy."),
            ("WHY IT MATTERS", "Every major LLM is trained on human approval, so every one can drift toward agreement and praise."),
        ), "Agreement can feel helpful while making the answer worse.", AMBER), Pair("illustrations/flattery-trap-sycophancy-v2.jpg", "lessons/avoid-traps-16-sycophancy.jpg")),
        (render_five_moves(), Pair("illustrations/flattery-trap-five-moves-v2.jpg", "lessons/avoid-traps-16a-five-moves.jpg")),
        (render_text_shell("If Someone May Be in Immediate Danger", (
            ("LEAVE THE CHAT", "Get real help from a trusted adult, school counselor, emergency services, or a local crisis resource."),
            ("DO IT NOW", "Not after one more message. A chatbot cannot call, show up, protect someone, or carry responsibility for what happens next."),
            ("THE RULE", "Safety outranks secrecy."),
        ), "In danger, the next move must reach a person who can act.", RED), Pair("illustrations/support-trap-danger-v2.jpg", "lessons/avoid-traps-21-danger.jpg")),
    )
    for image, pair in shells:
        save_pair(image, pair)


if __name__ == "__main__":
    main()
