#!/usr/bin/env python3
"""Build the Context Window roll-4 review candidate from pristine sources."""

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
DEST = ROOT / "Prompts/context-window-v1.mp4"
AUDIT = ROOT / "video-audit/context-window-repair-2026-09-16"
ASSETS = ROOT / "course-assets/context-window"


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
    assert frame_count(SOURCE) == 8249, "roll 4 is not the reviewed 8,249-frame source"
    assert frame_count(VISUAL_DONOR) == 7582, "roll 3 is not the reviewed 7,582-frame visual donor"

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
            (113.09, 113.73),
            (130.35, 130.70),
            (138.88, 139.46),
            (150.67, 151.28),
            (167.45, 168.08),
            (227.81, 228.35),
            (271.67, 275.00),
        ]
    )

    # Audio is roll 4 throughout. Rows select only the picture carried under it.
    b.keep(0, fr(12.48), "Notebook opening")
    b.keep(fr(12.48), 1613, "Same Question. Different Answers.", visual="same-question")
    b.keep(1613, 2992, "Notebook context-window explanation")
    b.keep(2992, 3918, "The Context Window", visual="five-sources")

    # A clean typing drawing breaks an otherwise 82-second board run. It covers
    # the Head Start introduction and returns to the board three seconds before
    # the first named card.
    b.keep(3918, 4088, "Notebook typing bridge", video_from=2579, video_end=2749)
    b.keep(4088, 5471, "Give AI a Head Start", visual="head-start")
    b.keep(5471, 5632, "Notebook hand-off")
    b.keep(5632, 6852, "Outside the Window", visual="outside-window")
    b.keep(6852, fr(251.12), "Notebook forgetting explanation")

    # Roll 3's clean-context drawing says what the narration teaches. It replaces
    # roll 4's misleading "Working Memory Reset" wording; roll 4 audio is unchanged.
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

    b.board(
        "five-sources",
        five,
        2992,
        3918,
        "compact",
        [
            target("from this chat", 102.29, [162, 51, 506, 354], NEUTRAL),
            target("personalization and memory", 106.74, [512, 51, 889, 354], PURPLE),
            target("project context", 111.14, [897, 51, 1183, 354], GREEN),
            target("loaded context window", 113.73, [207, 389, 1010, 735], NEUTRAL),
        ],
        push=False,
    )

    b.board(
        "head-start",
        head,
        4088,
        5471,
        "dense",
        [
            target("Personalization", 139.46, [40, 128, 526, 1053], PURPLE, [40, 128, 526, 1053]),
            target("Saved Memory", 151.28, [558, 128, 1043, 1053], BLUE, [558, 128, 1043, 1053]),
            target("Projects", 168.08, [1075, 128, 1561, 1053], TEAL, [1075, 128, 1561, 1053]),
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
            "scope_detail": "Full production review candidate from narration-KEEP roll 4; no narration grafts and no added pauses.",
            "audio_master": str(SOURCE.relative_to(ROOT)),
            "visual_donor": {
                "source": str(VISUAL_DONOR.relative_to(ROOT)),
                "source_frames": [fr(229.60), 7324],
                "output_audio_source_frames": [fr(251.12), 7973],
                "purpose": "Replace misleading Working Memory Reset graphic with a clean-context fresh-chat drawing.",
            },
            "notebook_bridge": {
                "source_frames": [2579, 2749],
                "output_audio_source_frames": [3918, 4088],
                "purpose": "Break the long board run under the Head Start introduction.",
            },
            "added_pauses": [],
            "longest_unbroken_board_run_frames": 1383,
            "longest_unbroken_board_run_seconds": 46.1,
            "shipping_authorized": False,
        }
    )
    manifest = b.render(clean_corner=True)
    assert frame_count(DEST) == manifest["total_frames"]
    print(f"Built {DEST.relative_to(ROOT)}: {manifest['total_frames']} frames")


if __name__ == "__main__":
    main()
