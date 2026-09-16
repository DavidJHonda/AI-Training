#!/usr/bin/env python3
"""Build Context Window v2 with the owner-requested trims and visual holds."""

from pathlib import Path
import sys

import cv2


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/video"))

from editspec_build import (  # noqa: E402
    AMBER,
    BLUE,
    GREEN,
    NEUTRAL,
    PURPLE,
    TEAL,
    Build,
    fr,
)


SOURCE = ROOT / "Prompts/context-window-4.mp4"
VISUAL_DONOR = ROOT / "Prompts/context-window-3.mp4"
DEST = ROOT / "Prompts/context-window-v2.mp4"
AUDIT = ROOT / "video-audit/context-window-repair-2026-09-16-v2"
ASSETS = ROOT / "course-assets/context-window"

# Silence-to-silence removals from the roll-4 audio timeline. These remove only
# the three owner-identified repetitions.
CUT_FIVE_CARDS = (fr(99.40), fr(101.80))
CUT_PERSONALIZATION_HEADING = (fr(106.54), fr(108.46))
CUT_PROJECT_HEADING = (fr(110.87), fr(112.30))


def frame_count(path: Path) -> int:
    cap = cv2.VideoCapture(str(path))
    assert cap.isOpened(), path
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return count


def target(label, at, rect, color, cam=None):
    row = dict(label=label, at=at, rects=[rect], color=color)
    if cam is not None:
        row["cam"] = cam
    return row


def main() -> None:
    assert frame_count(SOURCE) == 8249, "roll 4 is not the reviewed source"
    assert frame_count(VISUAL_DONOR) == 7582, "roll 3 is not the reviewed visual donor"

    same = ASSETS / "context-window-same-question.jpg"
    five = ASSETS / "context-window-five-sources.jpg"
    head = ASSETS / "context-window-head-start.jpg"
    outside = ASSETS / "context-window-outside-the-window.jpg"

    b = Build(
        ROOT,
        SOURCE,
        AUDIT,
        DEST,
        protected=(VISUAL_DONOR, same, five, head, outside),
    )
    b.load_audio(
        [
            (0.0, 0.18),
            (4.56, 5.02),
            (8.57, 9.15),
            (32.49, 33.11),
            (64.20, 64.87),
            (99.14, 99.65),
            (101.72, 102.29),
            (106.35, 106.74),
            (108.28, 108.64),
            (110.60, 111.14),
            (112.07, 112.50),
            (113.09, 113.73),
            (130.35, 130.70),
            (138.88, 139.46),
            (150.67, 151.28),
            (167.45, 168.08),
            (227.81, 228.35),
            (271.67, 275.00),
        ]
    )

    # Keep the fully drawn deterministic-logic graphic from 0:09.50 until the
    # comparison board arrives at 0:12.47.
    b.keep(0, fr(9.50), "Notebook calculator opening")
    b.keep(
        fr(9.50),
        fr(12.48),
        "Deterministic-logic graphic hold",
        video_from=fr(9.50),
        video_end=fr(9.50) + 1,
    )
    b.keep(fr(12.48), 1613, "Same Question. Different Answers.", visual="same-question")
    b.keep(1613, 2893, "Notebook context-window explanation")

    # The exact five-sources board starts under its spoken introduction. Its
    # compact leg advances continuously while the three duplicate audio phrases
    # are omitted at silence boundaries.
    logical = 2893
    b.keep(2893, CUT_FIVE_CARDS[0], "The Context Window — introduction", visual="five-sources", video_from=logical)
    logical += CUT_FIVE_CARDS[0] - 2893
    b.keep(CUT_FIVE_CARDS[1], CUT_PERSONALIZATION_HEADING[0], "The Context Window — From This Chat", visual="five-sources", video_from=logical)
    logical += CUT_PERSONALIZATION_HEADING[0] - CUT_FIVE_CARDS[1]
    b.keep(CUT_PERSONALIZATION_HEADING[1], CUT_PROJECT_HEADING[0], "The Context Window — Personalization and Saved Memory", visual="five-sources", video_from=logical)
    logical += CUT_PROJECT_HEADING[0] - CUT_PERSONALIZATION_HEADING[1]
    b.keep(CUT_PROJECT_HEADING[1], 3918, "The Context Window — Projects and tray", visual="five-sources", video_from=logical)
    logical += 3918 - CUT_PROJECT_HEADING[1]
    assert logical == 3745

    b.keep(3918, 4088, "Notebook typing bridge", video_from=2579, video_end=2749)
    b.keep(4088, 5471, "Give AI a Head Start", visual="head-start")
    b.keep(5471, 5632, "Notebook hand-off")
    b.keep(5632, 6852, "Outside the Window", visual="outside-window")
    b.keep(6852, fr(251.12), "Notebook forgetting explanation")
    b.keep(
        fr(251.12),
        7973,
        "Fresh-chat clean-context visual",
        video_from=fr(229.60),
        video_src=VISUAL_DONOR,
        video_end=7324,
    )
    b.mark_close_start()
    b.close(7973, 8159)
    b.finish_audio()

    b.board(
        "same-question",
        same,
        fr(12.48),
        1613,
        "dense",
        [
            target("the question", 15.92, [40, 127, 1561, 253], NEUTRAL, [40, 127, 1561, 253]),
            target("Luke's AI", 18.88, [40, 279, 784, 1100], BLUE, [40, 279, 784, 1100]),
            target("Nate's AI", 33.04, [816, 279, 1561, 1100], PURPLE, [816, 279, 1561, 1100]),
        ],
        pullback_at=44.20,
        banner_at=45.20,
        banner=[40, 1140, 1561, 1230],
    )

    # Logical leg times reflect the three removed phrases. The board stays full
    # frame, with each surviving source label ringed at its spoken onset.
    b.board(
        "five-sources",
        five,
        2893,
        3745,
        "compact",
        [
            target("from this chat", 99.80, [162, 51, 506, 354], NEUTRAL),
            target("personalization and saved memory", 104.33, [512, 51, 889, 354], PURPLE),
            target("projects", 106.77, [897, 51, 1183, 354], GREEN),
            target("loaded context window", 107.70, [207, 389, 1010, 735], NEUTRAL),
        ],
        push=False,
    )

    # Each card stays completely framed. Within it, the ring moves from the
    # explanation section to the example section as the narration moves.
    b.board(
        "head-start",
        head,
        4088,
        5471,
        "dense",
        [
            target("Personalization explanation", 139.44, [64, 424, 504, 712], PURPLE, [40, 128, 526, 1053]),
            target("Personalization example", 144.64, [64, 775, 504, 1029], PURPLE, [40, 128, 526, 1053]),
            target("Saved Memory explanation", 151.20, [582, 424, 1021, 715], BLUE, [558, 128, 1043, 1053]),
            target("Saved Memory example", 160.44, [582, 775, 1021, 1029], BLUE, [558, 128, 1043, 1053]),
            target("Projects explanation", 167.82, [1099, 424, 1538, 748], TEAL, [1075, 128, 1561, 1053]),
            target("Projects example", 174.02, [1099, 775, 1538, 1029], TEAL, [1075, 128, 1561, 1053]),
        ],
    )

    b.board(
        "outside-window",
        outside,
        5632,
        6852,
        "dense",
        [
            target("Older Chats", 194.89, [40, 127, 784, 774], PURPLE, [40, 127, 784, 774]),
            target("Web Pages", 202.17, [816, 127, 1561, 774], BLUE, [816, 127, 1561, 774]),
            target("Files on Your Computer", 209.20, [40, 806, 784, 1399], TEAL, [40, 806, 784, 1399]),
            target("Other Apps and Tabs", 216.79, [816, 806, 1561, 1399], AMBER, [816, 806, 1561, 1399]),
        ],
        pullback_at=223.69,
        banner_at=225.12,
        banner=[40, 1422, 1561, 1512],
    )

    b.render_legs()
    for key in b.boards:
        b.state_sheet(key)
    b.make_close("prompt")
    b.manifest(
        extra={
            "scope_detail": "Owner-requested v2: opening visual hold, three duplicate narration trims, and section-level Head Start rings.",
            "audio_master": str(SOURCE.relative_to(ROOT)),
            "audio_cuts": [
                {"source_frames": list(CUT_FIVE_CARDS), "words": "Five cards feed the context window."},
                {"source_frames": list(CUT_PERSONALIZATION_HEADING), "words": "Personalization and memory."},
                {"source_frames": list(CUT_PROJECT_HEADING), "words": "Project context."},
            ],
            "added_pauses": [],
            "visual_donor": {
                "source": str(VISUAL_DONOR.relative_to(ROOT)),
                "source_frames": [fr(229.60), 7324],
                "purpose": "Fresh-chat clean-context drawing; picture only.",
            },
            "shipping_authorized": False,
        }
    )
    manifest = b.render(clean_corner=True)
    assert frame_count(DEST) == manifest["total_frames"] == 8106
    print(f"Built {DEST.relative_to(ROOT)}: {manifest['total_frames']} frames")


if __name__ == "__main__":
    main()
