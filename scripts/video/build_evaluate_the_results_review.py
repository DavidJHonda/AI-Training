#!/usr/bin/env python3
"""Build the approved Evaluate the Results best-of review candidate.

Full production pass from the two pristine Notebook rolls:
* roll 2 supplies the richer complete opening;
* roll 1 supplies the Quick Pass, Decide, Dig, Move spine, and exact close;
* roll 2 replaces the incomplete Fix It beat and the compressed scholarship example;
* every course board is the current page JPG with post-crop 5 px rings;
* no pauses are added; the standard canonical close is the literal final frame.

Review output only. The live course video and lesson materials are unchanged.
"""

from pathlib import Path
import argparse
import json
import sys

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, PURPLE, TEAL, GREEN, AMBER, RED, NEUTRAL


ROOT = Path(__file__).resolve().parents[2]
SRC1 = ROOT / "Prompts/evaluate-the-results-1.mp4"
SRC2 = ROOT / "Prompts/evaluate-the-results-2.mp4"
AUDIT = ROOT / "video-audit/evaluate-the-results-repair-2026-09-16"
DEST = ROOT / "Prompts/evaluate-the-results-v5.mp4"
BOARDS = {
    "quick": ROOT / "course-assets/evaluate-the-results/evaluate-the-results-quick-pass.jpg",
    "decide": ROOT / "course-assets/evaluate-the-results/evaluate-the-results-decide.jpg",
    "dig": ROOT / "course-assets/evaluate-the-results/evaluate-the-results-dig.jpg",
    "move": ROOT / "course-assets/evaluate-the-results/evaluate-the-results-move.jpg",
    "example": ROOT / "course-assets/evaluate-the-results/evaluate-the-results-check-before-use.jpg",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--reuse-prepared", action="store_true")
    parser.add_argument("--reuse-legs", action="store_true")
    args = parser.parse_args()

    b = Build(
        ROOT,
        SRC1,
        AUDIT,
        DEST,
        protected=[
            SRC2,
            ROOT / "index.html",
            ROOT / "lessons/evaluate-the-results.md",
            ROOT / "course-assets/evaluate-the-results/evaluate-the-results.mp4",
            ROOT / "course-assets/evaluate-the-results/evaluate-the-results-close.jpg",
            *BOARDS.values(),
        ],
    )
    if args.reuse_prepared:
        manifest = json.loads((AUDIT / "edit-manifest.json").read_text())
        b.rows = manifest["timeline"]
        b.boards = manifest["boards"]
        b.grafts = manifest["grafts"]
        b.total = manifest["total_frames"]
        b.close_start = manifest["close"]["start_frame"]
        b.close_img = cv2.imread(str(AUDIT / "close.png"))
        if b.close_img is None:
            raise SystemExit("prepared close.png is missing")
        b.render()
        print(DEST)
        return
    b.load_audio([
        (24.91, 25.58), (69.81, 70.05), (71.50, 71.97),
        (114.10, 114.55), (164.10, 164.53), (178.18, 178.75),
        (186.03, 186.54), (200.33, 200.79), (216.04, 216.54),
        (222.26, 225.48),
    ])

    # Roll 1's exact board cuts, found by sequential frame inspection.
    QUICK_IN = fr(25.56)       # one frame before the raw cut so "This" is intact
    DECIDE_IN = 2156           # 1:11.867
    DIG_IN = 3436              # 1:54.533
    MOVE_IN = 4934             # 2:44.467
    EXAMPLE_IN = 6024          # 3:20.800
    CLOSE_IN = 6492            # 3:36.400

    # Approved donor spans.
    # End in the natural silence after "grade its homework" and before the
    # next word ("Let's", which leaked into v1 at the old 42.76 s boundary).
    R2_OPEN = (0, fr(42.50))
    R1_FIX_CUT = (fr(178.76), fr(186.56))
    # End in the silence after "applying it" and before roll 2 begins "or".
    R2_FIX = (fr(129.12), fr(137.50))
    # Stop two frames before roll 2's next narration onset. That onset leaves a
    # short audible blip after "proof" when exposed by the closing pause.
    R2_EXAMPLE = (fr(155.08), fr(182.50))
    CLOSE_OUT = fr(222.52)

    # Virtual board coordinates allow a donor beat to lengthen Make Your Move
    # without making the later source frames seek backwards inside the board leg.
    MOVE_FIX = R1_FIX_CUT[0]
    MOVE_AFTER_FIX = MOVE_FIX + (R2_FIX[1] - R2_FIX[0])
    MOVE_OUT = MOVE_AFTER_FIX + (EXAMPLE_IN - R1_FIX_CUT[1])
    EXAMPLE_VIRTUAL_IN = MOVE_OUT
    EXAMPLE_VIRTUAL_OUT = EXAMPLE_VIRTUAL_IN + (R2_EXAMPLE[1] - R2_EXAMPLE[0])

    def mapped(virtual_start, donor_start, t):
        return (virtual_start + (fr(t) - donor_start)) / 30

    # Audio and picture assembly. No synthetic pauses are inserted.
    b.graft(
        SRC2,
        R2_OPEN[0],
        R2_OPEN[1],
        "Roll 2 A/V: complete opening through Be Smarter Than the Tool",
        "roll2-opening",
        cover_intro=False,
        gain_db=1.1,
        reuse_leg=args.reuse_legs,
    )
    b.keep(QUICK_IN, DECIDE_IN, "B1 The Quick Pass", "quick")
    b.keep(DECIDE_IN, DIG_IN, "B2 Do You Need to Dig Deeper?", "decide")
    b.keep(DIG_IN, MOVE_IN, "B3 Dig Deeper", "dig")
    b.keep(MOVE_IN, R1_FIX_CUT[0], "B4 Make Your Move through Use It", "move")
    b.graft(
        SRC2,
        R2_FIX[0],
        R2_FIX[1],
        "Roll 2 audio: complete Fix It beat including revision check",
        "roll2-fix",
        picture_from=MOVE_FIX,
        gain_db=3.0,
        visual="move",
    )
    b.keep(
        R1_FIX_CUT[1],
        EXAMPLE_IN,
        "B4 Make Your Move: Walk Away and takeaway",
        "move",
        video_from=MOVE_AFTER_FIX,
    )
    b.graft(
        SRC2,
        R2_EXAMPLE[0],
        R2_EXAMPLE[1],
        "Roll 2 audio: complete scholarship example and evidence conclusion",
        "roll2-example",
        picture_from=EXAMPLE_VIRTUAL_IN,
        gain_db=2.2,
        visual="example",
    )
    # Preserve the approved picture timing while replacing the removed donor
    # onset with matched room tone on the scholarship board.
    b.pause(2, "Clean room-tone tail after proof")
    # Let the scholarship conclusion land before the closing reminder. The
    # canonical close board begins on this beat and holds under room tone for
    # exactly one second before the closing narration starts.
    b.mark_close_start()
    b.pause(30, "One-second close-board beat after proof")
    b.keep(CLOSE_IN, CLOSE_OUT, "Roll 1 exact closing lines", "close")
    b.pause(120, "Settled canonical close hold")
    b.finish_audio()

    def target(label, at, rect, color, *, cam=None, radius=18):
        return {
            "label": label,
            "at": at,
            "rects": [rect],
            "color": color,
            "cam": cam,
            "radius": radius,
        }

    # Compact three-card boards.
    cards3 = [
        [40, 250, 529, 681],
        [555, 250, 1045, 681],
        [1070, 250, 1560, 681],
    ]
    banner3 = [40, 720, 1560, 810]

    b.board(
        "quick", BOARDS["quick"], QUICK_IN, DECIDE_IN, "compact",
        [
            target("Read", 32.48, cards3[0], BLUE),
            target("Understand", 39.00, cards3[1], TEAL),
            target("Validate", 49.28, cards3[2], AMBER),
        ],
        banner_at=63.92,
        banner=banner3,
    )
    b.board(
        "decide", BOARDS["decide"], DECIDE_IN, DIG_IN, "compact",
        [
            target("Can You Judge It?", 78.16, cards3[0], BLUE),
            target("What Kind of Task Is It?", 90.96, cards3[1], TEAL),
            target("How Much Is Riding on It?", 102.40, cards3[2], AMBER),
        ],
        banner_at=112.32,
        banner=banner3,
    )

    # Five-card board is dense at 1280x720: establish whole, dive to complete
    # cards, then pull back for the takeaway.
    dig_cards = [
        [40, 250, 330, 750],
        [347, 250, 638, 750],
        [655, 250, 946, 750],
        [964, 250, 1254, 750],
        [1272, 250, 1560, 750],
    ]
    b.board(
        "dig", BOARDS["dig"], DIG_IN, MOVE_IN, "dense",
        [
            target("Check the Sources", 122.04, dig_cards[0], PURPLE, cam=dig_cards[0]),
            target("Challenge the Answer", 127.68, dig_cards[1], BLUE, cam=dig_cards[1]),
            target("Ask What's Missing", 135.16, dig_cards[2], TEAL, cam=dig_cards[2]),
            target("Search the Live Web", 145.64, dig_cards[3], GREEN, cam=dig_cards[3]),
            target("Check It Yourself", 152.88, dig_cards[4], AMBER, cam=dig_cards[4]),
        ],
        banner_at=160.44,
        pullback_at=160.00,
        banner=[40, 790, 1560, 880],
    )

    use_at = 170.84
    fix_at = MOVE_FIX / 30
    walk_at = (MOVE_AFTER_FIX + (fr(188.92) - R1_FIX_CUT[1])) / 30
    move_banner_at = (MOVE_AFTER_FIX + (fr(194.36) - R1_FIX_CUT[1])) / 30
    b.board(
        "move", BOARDS["move"], MOVE_IN, MOVE_OUT, "compact",
        [
            target("Use It", use_at, cards3[0], GREEN),
            target("Fix It", fix_at, cards3[1], BLUE),
            target("Walk Away", walk_at, cards3[2], RED),
        ],
        banner_at=move_banner_at,
        banner=banner3,
        push=False,
    )

    # The lower process panel is the dense active card. Keep all three stages
    # visible while moving the ring, rather than cropping inside a stage.
    process_panel = [40, 1007, 1560, 1230]
    example_claim = [70, 1035, 500, 1200]
    example_sources = [585, 1035, 1015, 1200]
    example_decision = [1100, 1035, 1530, 1200]
    b.board(
        "example", BOARDS["example"], EXAMPLE_VIRTUAL_IN, EXAMPLE_VIRTUAL_OUT, "dense",
        [
            target("Claim", mapped(EXAMPLE_VIRTUAL_IN, R2_EXAMPLE[0], 157.92), example_claim, BLUE, cam=process_panel),
            target("Sources", mapped(EXAMPLE_VIRTUAL_IN, R2_EXAMPLE[0], 161.68), example_sources, TEAL, cam=process_panel),
            target("Decision", mapped(EXAMPLE_VIRTUAL_IN, R2_EXAMPLE[0], 168.60), example_decision, RED, cam=process_panel),
        ],
        banner_at=mapped(EXAMPLE_VIRTUAL_IN, R2_EXAMPLE[0], 175.96),
        pullback_at=mapped(EXAMPLE_VIRTUAL_IN, R2_EXAMPLE[0], 175.40),
        banner=[40, 1271, 1560, 1360],
    )

    if not args.reuse_prepared and not args.reuse_legs:
        b.render_legs()
        for key in b.boards:
            b.state_sheet(key)
    b.make_close("evaluating")
    b.manifest({
        "approved_best_of_plan": {
            "base": str(SRC1),
            "opening_donor_frames": list(R2_OPEN),
            "fix_removed_roll1_frames": list(R1_FIX_CUT),
            "fix_donor_roll2_frames": list(R2_FIX),
            "example_donor_roll2_frames": list(R2_EXAMPLE),
            "close_roll1_frames": [CLOSE_IN, CLOSE_OUT],
        },
        "audio_cleanup": {
            "issue": "stray donor narration onset after proof",
            "removed_roll2_frames": [5475, 5477],
            "replacement_output_frames": [7372, 7374],
            "replacement": "matched room tone",
        },
        "selective_pause_plan": [
            {
                "after": "It is merely a claim that requires proof.",
                "output_frames": [7374, 7404],
                "duration_frames": 30,
                "visual": "canonical close board",
            }
        ],
        "notebook_interleaves": [],
        "longest_unbroken_board_run": {
            "start_output_frame": R2_OPEN[1],
            "end_output_frame": EXAMPLE_VIRTUAL_OUT - QUICK_IN + R2_OPEN[1],
            "reason": "The raw rolls contain no narration-matched Notebook drawings inside the framework; the approved board-led treatment is preserved.",
        },
        "board_plan": {
            "quick": "compact/full view; Read, Understand, Validate, banner",
            "decide": "compact/full view; three decision cards, banner",
            "dig": "dense/full establish; five complete-card dives; full-view banner",
            "move": "compact/full view; Use, Fix, Walk Away, banner",
            "example": "dense/full establish; complete lower panel with Claim, Sources, Decision; full-view banner",
        },
    })
    print(
        "Prepared",
        b.total,
        f"{b.total / 30:.2f}s",
        {key: (value["src_in"], value["src_out"], value["density"]) for key, value in b.boards.items()},
        "close",
        b.close_start,
        flush=True,
    )
    if args.prepare_only:
        return
    b.render()
    print(DEST)


if __name__ == "__main__":
    main()
