#!/usr/bin/env python3
"""Render review-only board alternatives for the remaining course lessons."""

from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
ALT = ROOT / "board-review-first-four/alternatives"
W, H = 1600, 900

LAVENDER = "#eeeaff"
PALE = "#f8f6ff"
WHITE = "#ffffff"
NAVY = "#08072b"
CARD_TITLE = "#152b7a"
BODY = "#24203a"
MUTED = "#655f7c"
PURPLE = "#6f52ff"
BLUE = "#3678f4"
TEAL = "#15998c"
GREEN = "#18885b"
RED = "#d45168"
GOLD = "#ffe9ab"
GOLD_DARK = "#886310"
RULE = "#ded9ed"
SOFT_BLUE = "#eaf2ff"
SOFT_GREEN = "#e8f6ef"
SOFT_RED = "#fff0f2"
SOFT_GOLD = "#fff8e6"

FONT_ROOT = Path("/Users/davidobrien/Library/Fonts")


def font(weight: str, size: int):
    filename = {
        "heavy": "AvenirNextforINTUIT-Heavy.otf",
        "bold": "AvenirNextforINTUIT-Bold.otf",
        "demi": "AvenirNextforINTUIT-Demi.otf",
        "medium": "AvenirNextforINTUIT-Medium.otf",
    }[weight]
    return ImageFont.truetype(str(FONT_ROOT / filename), size)


def rounded(draw, box, radius=16, fill=WHITE, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_width(draw, text, face):
    box = draw.textbbox((0, 0), text, font=face)
    return box[2] - box[0]


def fit_lines(draw, text, face, max_width, max_lines=3):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if not current or text_width(draw, trial, face) <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while text_width(draw, lines[-1] + "...", face) > max_width and " " in lines[-1]:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += "..."
    return lines


def multiline(draw, xy, text, face, fill, max_width, line_gap=6, anchor="la", max_lines=4):
    lines = fit_lines(draw, text, face, max_width, max_lines)
    x, y = xy
    line_h = face.size + line_gap
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=face, fill=fill, anchor=anchor)
    return len(lines) * line_h - line_gap


def centered_block(draw, cx, top, text, face, fill, max_width, line_gap=4, max_lines=3):
    lines = fit_lines(draw, text, face, max_width, max_lines)
    for i, line in enumerate(lines):
        draw.text((cx, top + i * (face.size + line_gap)), line, font=face, fill=fill, anchor="ma")
    return len(lines) * (face.size + line_gap) - line_gap


def board_frame(title, subtitle, takeaway):
    image = Image.new("RGB", (W, H), LAVENDER)
    draw = ImageDraw.Draw(image)
    title_face = font("heavy", 44)
    title_lines = fit_lines(draw, title, title_face, 1380, 2)
    title_top = 74 if len(title_lines) == 1 else 31
    for i, line in enumerate(title_lines):
        draw.text((800, title_top + i * 50), line, font=title_face, fill=NAVY, anchor="ma")
    rounded(draw, (80, 172, 1520, 736), 16, WHITE)
    rounded(draw, (80, 776, 1520, 860), 16, GOLD)
    tf = font("demi", 32)
    tw = text_width(draw, takeaway, tf)
    lockup_w = 52 + 16 + tw
    x = (W - lockup_w) / 2
    rounded(draw, (x, 792, x + 52, 844), 26, PURPLE)
    draw.line([(x + 14, 818), (x + 23, 827), (x + 39, 807)], fill=WHITE, width=5, joint="curve")
    draw.text((x + 68, 818), takeaway, font=tf, fill=NAVY, anchor="lm")
    return image, draw


def marker(draw, cx, cy, label, color=PURPLE, radius=28, face=None):
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=color)
    draw.text((cx, cy), label, font=face or font("heavy", 24), fill=WHITE, anchor="mm")


def arrow(draw, x1, y1, x2, y2, color=PURPLE, width=4):
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    if abs(x2 - x1) >= abs(y2 - y1):
        s = 1 if x2 > x1 else -1
        draw.polygon([(x2, y2), (x2 - s * 12, y2 - 8), (x2 - s * 12, y2 + 8)], fill=color)
    else:
        s = 1 if y2 > y1 else -1
        draw.polygon([(x2, y2), (x2 - 8, y2 - s * 12), (x2 + 8, y2 - s * 12)], fill=color)


def label_pill(draw, cx, cy, text, fill=PURPLE, text_fill=WHITE, width=None):
    face = font("heavy", 24)
    pw = width or text_width(draw, text, face) + 34
    rounded(draw, (cx - pw / 2, cy - 20, cx + pw / 2, cy + 20), 20, fill)
    draw.text((cx, cy), text, font=face, fill=text_fill, anchor="mm")


def three_cards(draw, cards, *, top=202, bottom=706, numbered=True):
    gap = 22
    x0 = 108
    cw = (1384 - 2 * gap) / 3
    for i, card in enumerate(cards):
        x = x0 + i * (cw + gap)
        fill = card.get("fill", PALE)
        accent = card.get("accent", [PURPLE, BLUE, TEAL][i])
        rounded(draw, (x, top, x + cw, bottom), 16, fill, RULE, 1)
        if numbered:
            marker(draw, x + cw / 2, top + 62, str(i + 1), accent)
            title_y = top + 112
        else:
            label = card.get("eyebrow")
            if label:
                label_pill(draw, x + cw / 2, top + 48, label, accent)
                title_y = top + 91
            else:
                title_y = top + 47
        centered_block(draw, x + cw / 2, title_y, card["title"], font("bold", 32), CARD_TITLE, cw - 52, 4, 3)
        body_y = card.get("body_y", title_y + 78)
        centered_block(draw, x + cw / 2, body_y, card["body"], font("medium", 30), BODY, cw - 60, 7, 6)
        if card.get("footer"):
            rounded(draw, (x + 28, bottom - 76, x + cw - 28, bottom - 28), 12, WHITE)
            draw.text((x + cw / 2, bottom - 52), card["footer"], font=font("demi", 24), fill=accent, anchor="mm")


def two_cards(draw, left, right, *, top=202, bottom=706, gap=24):
    x0 = 108
    cw = (1384 - gap) / 2
    for i, card in enumerate((left, right)):
        x = x0 + i * (cw + gap)
        accent = card.get("accent", PURPLE if i == 0 else BLUE)
        rounded(draw, (x, top, x + cw, bottom), 16, card.get("fill", PALE), RULE, 1)
        if card.get("eyebrow"):
            label_pill(draw, x + cw / 2, top + 48, card["eyebrow"], accent)
        title_y = top + (92 if card.get("eyebrow") else 44)
        centered_block(draw, x + cw / 2, title_y, card["title"], font("bold", 32), CARD_TITLE, cw - 70, 4, 3)
        if card.get("quote"):
            rounded(draw, (x + 42, top + 151, x + cw - 42, top + 242), 14, WHITE, accent, 2)
            centered_block(draw, x + cw / 2, top + 177, card["quote"], font("demi", 28), BODY, cw - 120, 5, 2)
            body_y = top + 275
        else:
            body_y = top + 139
        centered_block(draw, x + cw / 2, body_y, card["body"], font("medium", 30), BODY, cw - 78, 8, 7)
        if card.get("footer"):
            rounded(draw, (x + 40, bottom - 83, x + cw - 40, bottom - 30), 13, WHITE)
            draw.text((x + cw / 2, bottom - 56), card["footer"], font=font("demi", 24), fill=accent, anchor="mm")


def save(image, section, filename):
    out = ALT / section
    out.mkdir(parents=True, exist_ok=True)
    path = out / filename
    image.save(path, quality=94, subsampling=0)
    print(path.relative_to(ROOT))


def render_tokens():
    image, draw = board_frame(
        "Before AI can read, text becomes tokens",
        "An ordinary program does the splitting.",
        "A token ID is an address, not a meaning.",
    )
    cards = [
        {"title": "Split the input", "body": "A tokenizer breaks text into reusable chunks. No AI is involved.", "footer": "TOKENIZER"},
        {"title": "Create tokens", "body": "A token can be a whole word, part of a word, punctuation, an emoji, or a space.", "footer": "REUSABLE CHUNKS"},
        {"title": "Assign an ID", "body": "Each token gets a number that points to its place in the vocabulary.", "footer": "VOCABULARY ADDRESS"},
    ]
    three_cards(draw, cards)
    save(image, "understand-ai", "tokens-tokenization-alternative.jpg")


def render_transformer():
    image, draw = board_frame(
        "The surrounding words decide the meaning",
        "Two language problems the Transformer has to solve.",
        "Attention uses context to resolve what each word means.",
    )
    two_cards(draw,
        {"eyebrow": "AMBIGUITY", "title": "The same word can change", "quote": "Turn on the LIGHT.  /  Pack LIGHT.", "body": "The nearby words tell the model whether LIGHT means a lamp or low weight.", "footer": "CONTEXT SETS THE SENSE"},
        {"eyebrow": "REFERENCE", "title": "A small word can point back", "quote": "The cat drank the milk because IT was thirsty.", "body": "Attention connects IT to the cat. Change thirsty to fresh, and IT points to the milk.", "footer": "CONTEXT SETS THE TARGET", "accent": TEAL},
    )
    save(image, "understand-ai", "transformer-context-problems-alternative.jpg")


def render_inference_path():
    image, draw = board_frame(
        "How a question becomes the next token",
        "The complete inference path.",
        "Every answer is built one token at a time.",
    )
    steps = [
        ("1", "TOKENS", "Split the input", PURPLE),
        ("2", "POSITIONS", "Stamp the order", BLUE),
        ("3", "MEANING", "Start with vectors", TEAL),
        ("4", "LAYERS", "Update with context", GREEN),
        ("5", "RANK", "Choose the next token", RED),
    ]
    x, y, cw, gap = 108, 241, 248, 30
    for i, (n, title, body, color) in enumerate(steps):
        bx = x + i * (cw + gap)
        rounded(draw, (bx, y, bx + cw, y + 386), 16, PALE, RULE, 1)
        marker(draw, bx + cw / 2, y + 60, n, color)
        draw.text((bx + cw / 2, y + 118), title, font=font("heavy", 24), fill=color, anchor="ma")
        centered_block(draw, bx + cw / 2, y + 166, body, font("bold", 30), CARD_TITLE, cw - 38, 4, 3)
        if i < len(steps) - 1:
            arrow(draw, bx + cw + 5, y + 193, bx + cw + gap - 5, y + 193, MUTED, 3)
        if i == 4:
            rounded(draw, (bx + 33, y + 272, bx + cw - 33, y + 331), 13, WHITE, color, 2)
            draw.text((bx + cw / 2, y + 301), "...then run again", font=font("demi", 24), fill=color, anchor="mm")
    save(image, "understand-ai", "how-ai-answers-inference-path-alternative.jpg")


def render_transcript_memory():
    image, draw = board_frame(
        "The transcript is the memory",
        "You remember the chat. The model rebuilds it.",
        "You carry the conversation. AI re-reads it every turn.",
    )
    two_cards(draw,
        {"eyebrow": "YOU", "title": "Carry the conversation", "body": "The earlier questions and answers stay in your memory. You bring that history to the next turn.", "footer": "MEMORY CONTINUES", "accent": TEAL, "fill": SOFT_GREEN},
        {"eyebrow": "AI", "title": "Re-read the transcript", "body": "Before every new word, the system sends the available chat back through the model. Nothing is remembered between runs.", "footer": "CONTEXT IS REBUILT", "accent": PURPLE},
    )
    save(image, "understand-ai", "one-more-thing-transcript-memory-alternative.jpg")


def render_mind_trap():
    image, draw = board_frame(
        "Human advice has something AI does not",
        "Knowledge of you and a stake in the outcome.",
        "Human-sounding is not a mind.",
    )
    two_cards(draw,
        {"eyebrow": "A PERSON WHO KNOWS YOU", "title": "Your mom", "body": "She knows your history, notices what you leave out, and has to live with what happens next.", "footer": "CONTEXT + STAKE", "accent": TEAL, "fill": SOFT_GREEN},
        {"eyebrow": "A SYSTEM THAT SOUNDS HUMAN", "title": "AI", "body": "It matches patterns from pages and the current chat. It has no life with you and no stake in the choice.", "footer": "PATTERNS + FLUENCY", "accent": PURPLE},
    )
    save(image, "avoid-traps", "mind-trap-human-stake-alternative.jpg")


def render_flattery():
    image, draw = board_frame(
        "How the praise got baked in",
        "The model learned which answers people reward.",
        "The model learned what people give a thumbs-up.",
    )
    cards = [
        {"title": "People rank answers", "body": "Human reviewers compare model responses and choose the ones they prefer.", "footer": "FEEDBACK"},
        {"title": "Support often wins", "body": "Positive, confident, agreeable answers can feel better in the moment.", "footer": "REWARD", "accent": BLUE},
        {"title": "The numbers move", "body": "Training pushes the model toward answer patterns that earned approval.", "footer": "LEARNED PRAISE", "accent": TEAL},
    ]
    three_cards(draw, cards)
    save(image, "avoid-traps", "flattery-trap-praise-loop-alternative.jpg")


def render_engagement():
    image, draw = board_frame(
        "The answer ends. The chat keeps going.",
        "One decision point changes where your time goes.",
        "The chat is built to continue. You decide when it ends.",
    )
    rounded(draw, (112, 206, 1488, 702), 16, PALE, RULE, 1)
    marker(draw, 800, 276, "?", PURPLE, 34, font("heavy", 28))
    draw.text((800, 332), "Did the answer solve the question?", font=font("heavy", 29), fill=NAVY, anchor="ma")
    arrow(draw, 760, 372, 470, 449, TEAL, 5)
    arrow(draw, 840, 372, 1130, 449, RED, 5)
    rounded(draw, (188, 442, 695, 652), 16, SOFT_GREEN, TEAL, 2)
    label_pill(draw, 441, 478, "YES: STOP", TEAL)
    centered_block(draw, 441, 526, "Use the answer and leave the chat.", font("bold", 30), CARD_TITLE, 420, 4, 2)
    draw.text((441, 608), "About 1 minute", font=font("demi", 26), fill=TEAL, anchor="mm")
    rounded(draw, (905, 442, 1412, 652), 16, SOFT_RED, RED, 2)
    label_pill(draw, 1158, 478, "ACCEPT THE FOLLOW-UP", RED)
    centered_block(draw, 1158, 526, "New offers create new questions.", font("bold", 30), CARD_TITLE, 420, 4, 2)
    draw.text((1158, 608), "The loop can last for hours", font=font("demi", 26), fill=RED, anchor="mm")
    save(image, "avoid-traps", "engagement-trap-decision-point-alternative.jpg")


def render_support():
    image, draw = board_frame(
        "Supportive words are not support",
        "Some value is real. The relationship is not.",
        "Use AI to get ready for people, not instead of people.",
    )
    two_cards(draw,
        {"eyebrow": "WHAT CAN BE REAL", "title": "Relief and useful advice", "body": "A calm response can help you name a feeling, organize your thoughts, or prepare for a hard conversation.", "footer": "USEFUL WORDS", "accent": TEAL, "fill": SOFT_GREEN},
        {"eyebrow": "WHAT IS MISSING", "title": "A person who can act", "body": "AI cannot notice what changed, show up, take responsibility, or check on you tomorrow.", "footer": "NO RELATIONSHIP", "accent": RED, "fill": SOFT_RED},
    )
    save(image, "avoid-traps", "support-trap-real-vs-missing-alternative.jpg")


def render_fake():
    image, draw = board_frame(
        "Move the test off the image",
        "Strong feeling is the cue to run three checks.",
        "Check the source, not the pixels.",
    )
    cards = [
        {"title": "Source", "body": "Who posted it? Do they have a reason and a way to know?", "footer": "WHO KNOWS?"},
        {"title": "Context", "body": "What happened before and after? What details are missing?", "footer": "WHAT IS AROUND IT?", "accent": BLUE},
        {"title": "Corroboration", "body": "Can an independent source confirm the same event or claim?", "footer": "WHO ELSE CONFIRMS?", "accent": TEAL},
    ]
    three_cards(draw, cards)
    save(image, "avoid-traps", "fake-trap-three-checks-alternative.jpg")


def render_loudest_voices():
    image, draw = board_frame(
        "Three experts. Three different bets.",
        "Each one admits the other side may be right.",
        "Where AI will be in ten years is a bet.",
    )
    cards = [
        {"eyebrow": "OPTIMIST", "title": "Dario Amodei", "body": "AI could compress decades of progress in biology and medicine. He also says the technology is not mature yet.", "footer": "BET: RAPID PROGRESS", "accent": TEAL, "fill": SOFT_GREEN},
        {"eyebrow": "WORRIER", "title": "Geoffrey Hinton", "body": "AI may develop goals we did not intend. He also points to benefits such as earlier cancer detection.", "footer": "BET: SERIOUS RISK", "accent": RED, "fill": SOFT_RED},
        {"eyebrow": "SKEPTIC", "title": "Yann LeCun", "body": "Current LLMs may be a dead end for human-level intelligence. He still takes AI risk and agency seriously.", "footer": "BET: DIFFERENT PATH", "accent": PURPLE},
    ]
    three_cards(draw, cards, numbered=False)
    save(image, "embrace-the-future", "loudest-voices-three-bets-alternative.jpg")


def render_pace():
    image, draw = board_frame(
        "Why AI is moving so fast",
        "Three accelerants are working at the same time.",
        "Training, compute, and AI building AI reinforce one another.",
    )
    cards = [
        {"title": "Training", "body": "More data, and often better data, gives models more examples and patterns to learn from.", "footer": "BETTER INPUTS"},
        {"title": "Compute", "body": "AI companies spend billions on more chips and data centers to run more math.", "footer": "MORE POWER", "accent": BLUE},
        {"title": "AI building AI", "body": "Strong models help write and optimize parts of the software for the next model.", "footer": "FASTER ITERATION", "accent": TEAL},
    ]
    three_cards(draw, cards)
    save(image, "embrace-the-future", "pace-of-change-accelerants-alternative.jpg")


def render_downside():
    image, draw = board_frame(
        "Safeguards are always chasing the frontier",
        "Capability changes faster than society can respond.",
        "The black box moves faster than safeguards and rules.",
    )
    events = [
        ("NEW CAPABILITY", "The frontier moves", PURPLE),
        ("NEW FAILURE", "Gaps get discovered", RED),
        ("NEW GUARDRAIL", "Builders respond", BLUE),
        ("NEW RULE", "Society catches up", TEAL),
    ]
    y = 342
    xs = [248, 615, 982, 1349]
    for i, ((eyebrow, body, color), x) in enumerate(zip(events, xs)):
        marker(draw, x, y, str(i + 1), color, 32)
        if i < 3:
            arrow(draw, x + 42, y, xs[i + 1] - 42, y, MUTED, 4)
        label_pill(draw, x, y + 78, eyebrow, color, width=260)
        centered_block(draw, x, y + 124, body, font("bold", 30), CARD_TITLE, 265, 4, 2)
    rounded(draw, (190, 567, 1410, 681), 14, PALE, RULE, 1)
    draw.text((800, 599), "The lag used to be measured in decades.", font=font("heavy", 30), fill=NAVY, anchor="ma")
    draw.text((800, 642), "AI models can change every few months.", font=font("demi", 28), fill=RED, anchor="ma")
    save(image, "embrace-the-future", "big-downside-safeguard-gap-alternative.jpg")


def render_upside():
    image, draw = board_frame(
        "One release changed fifty years of work",
        "DeepMind gave the protein-shape predictions away.",
        "AI can compress decades of discovery.",
    )
    two_cards(draw,
        {"eyebrow": "HUMANS", "title": "50 years of lab work", "body": "About 200,000 protein shapes solved.", "footer": "SLOW, EXPENSIVE EXPERIMENTS", "accent": MUTED},
        {"eyebrow": "DEEPMIND", "title": "One release in 2022", "body": "About 200 million protein shapes predicted and released free to everyone.", "footer": "1,000x MORE SHAPES", "accent": TEAL, "fill": SOFT_GREEN},
    )
    draw.ellipse((765, 462, 835, 532), fill=PURPLE)
    draw.line((783, 497, 817, 497), fill=WHITE, width=6)
    draw.polygon([(821, 497), (809, 487), (809, 507)], fill=WHITE)
    save(image, "embrace-the-future", "big-upside-protein-folding-alternative.jpg")


def render_agents():
    image, draw = board_frame(
        "A chatbot answers. An agent acts.",
        "The same LLM, plus tools and a loop.",
        "The agent does the work. The result still carries your name.",
    )
    steps = [
        ("1", "GOAL", "What should happen?", PURPLE),
        ("2", "PLAN", "Choose the steps", BLUE),
        ("3", "ACT", "Use tools", TEAL),
        ("4", "CHECK", "Inspect the result", GREEN),
    ]
    xs = [250, 610, 970, 1330]
    y = 380
    for i, ((n, title, body, color), x) in enumerate(zip(steps, xs)):
        rounded(draw, (x - 135, y - 130, x + 135, y + 150), 16, PALE, RULE, 1)
        marker(draw, x, y - 72, n, color)
        draw.text((x, y - 13), title, font=font("heavy", 28), fill=color, anchor="ma")
        centered_block(draw, x, y + 34, body, font("bold", 30), CARD_TITLE, 220, 4, 2)
        if i < 3:
            arrow(draw, x + 150, y, xs[i + 1] - 150, y, MUTED, 4)
    draw.line((1330, 548, 1330, 650), fill=PURPLE, width=4)
    draw.line((1330, 650, 610, 650), fill=PURPLE, width=4)
    draw.line((610, 650, 610, 553), fill=PURPLE, width=4)
    draw.polygon([(610, 548), (601, 562), (619, 562)], fill=PURPLE)
    rounded(draw, (790, 623, 1150, 677), 27, WHITE)
    draw.text((970, 650), "Repeat until the goal is met", font=font("demi", 28), fill=PURPLE, anchor="mm")
    save(image, "embrace-the-future", "rise-of-agents-loop-alternative.jpg")


def render_work_changes():
    image, draw = board_frame(
        "Two ways AI changes the work",
        "Most jobs will contain both.",
        "Your job title may stay. The work underneath it changes.",
    )
    two_cards(draw,
        {"eyebrow": "AUTOMATE", "title": "AI takes over a step", "body": "Sorting, grouping, and the first summary can happen with little human attention.", "footer": "SOME STEPS DISAPPEAR", "accent": PURPLE},
        {"eyebrow": "AUGMENT", "title": "AI helps a person do more", "body": "A person can explore more explanations, compare more options, and improve the recommendation faster.", "footer": "THE JOB GETS WIDER", "accent": TEAL, "fill": SOFT_GREEN},
    )
    save(image, "embrace-the-future", "work-changes-automate-augment-alternative.jpg")


def render_hidden_cost():
    image, draw = board_frame(
        "What one short answer costs",
        "Every token re-runs the whole network.",
        "Cheap to type is not free to run.",
    )
    labels = [
        ("~50", "TOKENS", PURPLE),
        ("~400B", "PARAMETERS", BLUE),
        ("2", "OPS EACH", TEAL),
    ]
    xs = [330, 800, 1270]
    for i, ((value, label, color), x) in enumerate(zip(labels, xs)):
        rounded(draw, (x - 175, 248, x + 175, 516), 18, PALE, RULE, 1)
        draw.text((x, 330), value, font=font("heavy", 58), fill=color, anchor="mm")
        draw.text((x, 405), label, font=font("heavy", 28), fill=NAVY, anchor="mm")
        if i < 2:
            draw.text(((xs[i] + xs[i + 1]) / 2, 383), "×", font=font("demi", 44), fill=MUTED, anchor="mm")
    rounded(draw, (402, 561, 1198, 687), 18, NAVY)
    draw.text((800, 600), "≈ 40 TRILLION", font=font("heavy", 42), fill=WHITE, anchor="ma")
    draw.text((800, 650), "calculations for one short reply", font=font("medium", 28), fill="#d8d4ea", anchor="ma")
    save(image, "embrace-the-future", "hidden-cost-calculations-alternative.jpg")


def render_unexpected():
    image, draw = board_frame(
        "The plan and the outcome can split",
        "Two results better than predicted. Two results worse.",
        "The biggest results are the ones nobody predicted.",
    )
    cards = [
        ("TEXT MESSAGING", "Small network feature", "A central way to communicate", TEAL, SOFT_GREEN, "+"),
        ("GPS", "Military navigation", "Directions and location tools", TEAL, SOFT_GREEN, "+"),
        ("CANE TOADS", "Control crop beetles", "Spread and harmed wildlife", RED, SOFT_RED, "−"),
        ("WIDER HIGHWAYS", "Reduce congestion", "Traffic can return", RED, SOFT_RED, "−"),
    ]
    positions = [(110, 205), (810, 205), (110, 463), (810, 463)]
    for (title, plan, outcome, color, fill, sign), (x, y) in zip(cards, positions):
        rounded(draw, (x, y, x + 680, y + 224), 16, fill, RULE, 1)
        marker(draw, x + 48, y + 48, sign, color, 25, font("heavy", 25))
        draw.text((x + 88, y + 39), title, font=font("heavy", 28), fill=color, anchor="la")
        draw.text((x + 42, y + 103), "PLAN", font=font("heavy", 24), fill=MUTED)
        draw.text((x + 160, y + 98), plan, font=font("demi", 28), fill=BODY)
        draw.text((x + 42, y + 161), "RESULT", font=font("heavy", 24), fill=MUTED)
        draw.text((x + 160, y + 156), outcome, font=font("demi", 28), fill=BODY)
    save(image, "embrace-the-future", "unexpected-results-plan-outcome-alternative.jpg")


def make_contact_sheet(section, filenames, output_name):
    thumbs = []
    for name in filenames:
        path = ALT / section / name
        img = Image.open(path).convert("RGB")
        img.thumbnail((720, 405), Image.Resampling.LANCZOS)
        thumbs.append((name, img.copy()))
    cols = 2
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (1540, 80 + rows * 470), "#ffffff")
    draw = ImageDraw.Draw(sheet)
    draw.text((770, 36), section.replace("-", " ").title() + " remaining alternatives", font=font("heavy", 34), fill=NAVY, anchor="mm")
    for i, (name, img) in enumerate(thumbs):
        col, row = i % cols, i // cols
        x, y = 40 + col * 760, 75 + row * 470
        draw.rounded_rectangle((x - 4, y - 4, x + 724, y + 409), 8, fill="#e8e5ef")
        sheet.paste(img, (x, y))
        draw.text((x + 360, y + 430), name.replace("-alternative.jpg", "").replace("-", " "), font=font("demi", 18), fill=BODY, anchor="mm")
    path = ALT / section / output_name
    sheet.save(path, quality=92, subsampling=0)
    print(path.relative_to(ROOT))


def main():
    render_tokens()
    render_transformer()
    render_inference_path()
    render_transcript_memory()
    render_mind_trap()
    render_flattery()
    render_engagement()
    render_support()
    render_fake()
    render_loudest_voices()
    render_pace()
    render_downside()
    render_upside()
    render_agents()
    render_work_changes()
    render_hidden_cost()
    render_unexpected()

    make_contact_sheet("understand-ai", [
        "tokens-tokenization-alternative.jpg",
        "transformer-context-problems-alternative.jpg",
        "how-ai-answers-inference-path-alternative.jpg",
        "one-more-thing-transcript-memory-alternative.jpg",
    ], "remaining-alternatives-contact-sheet.jpg")
    make_contact_sheet("avoid-traps", [
        "mind-trap-human-stake-alternative.jpg",
        "flattery-trap-praise-loop-alternative.jpg",
        "engagement-trap-decision-point-alternative.jpg",
        "support-trap-real-vs-missing-alternative.jpg",
        "fake-trap-three-checks-alternative.jpg",
    ], "remaining-alternatives-contact-sheet.jpg")
    make_contact_sheet("embrace-the-future", [
        "loudest-voices-three-bets-alternative.jpg",
        "pace-of-change-accelerants-alternative.jpg",
        "big-downside-safeguard-gap-alternative.jpg",
        "big-upside-protein-folding-alternative.jpg",
        "rise-of-agents-loop-alternative.jpg",
        "work-changes-automate-augment-alternative.jpg",
        "hidden-cost-calculations-alternative.jpg",
        "unexpected-results-plan-outcome-alternative.jpg",
    ], "remaining-alternatives-contact-sheet.jpg")


if __name__ == "__main__":
    main()
