#!/usr/bin/env python3
"""Build the approved Critical Thinking repair candidate.

Review output only. Reroll 4 supplies the narration and most Notebook scenes.
Reroll 3 supplies the complete Habits 4-5 narration, the hand-drawn chocolate
headline sequence, and the accurate AI decision diagram. Current course-board
JPGs replace every Notebook-rendered board. The live course video and lesson
materials are protected and remain unchanged.
"""

from pathlib import Path
import argparse
import json
import sys

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, GREEN, AMBER, NEUTRAL


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "Prompts/critical-thinking-reroll-4.mp4"
DONOR = ROOT / "Prompts/critical-thinking-reroll-3.mp4"
AUDIT = ROOT / "video-audit/critical-thinking-repair-2026-09-16"
DEST = ROOT / "Prompts/critical-thinking-v3.mp4"
HABITS_BOARD_IN_SECONDS = 125.88
DONOR_H45_OUT_SECONDS = 170.56
KEEP_LAPTOP_BRIDGE = True
BOARDS = {
    "equation": ROOT / "course-assets/critical-thinking/critical-thinking-equation.jpg",
    "reactions": ROOT / "course-assets/critical-thinking/critical-thinking-two-reactions.jpg",
    "habits": ROOT / "course-assets/critical-thinking/critical-thinking-five-habits.jpg",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--reuse-prepared", action="store_true")
    args = parser.parse_args()

    b = Build(
        ROOT,
        BASE,
        AUDIT,
        DEST,
        protected=[
            DONOR,
            ROOT / "index.html",
            ROOT / "lessons/critical-thinking.md",
            ROOT / "Prompts/critical-thinking-video-prompt.txt",
            ROOT / "Prompts/critical-thinking-upload-files.txt",
            ROOT / "course-assets/critical-thinking/critical-thinking.mp4",
            ROOT / "course-assets/critical-thinking/critical-thinking-close.jpg",
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
        (4.38, 5.22), (11.22, 12.16), (14.84, 15.64),
        (32.00, 32.84), (37.58, 38.34), (39.68, 40.34),
        (55.80, 56.52), (59.22, 60.16), (70.28, 71.12),
        (78.42, 79.12), (82.52, 83.32), (86.20, 86.86),
        (94.82, 95.42), (106.24, 107.14), (117.20, 118.04),
        (130.20, 130.98), (133.22, 133.98), (141.50, 142.30),
        (152.00, 152.84), (156.18, 157.20), (166.32, 166.94),
        (181.24, 182.00), (188.32, 189.10), (193.28, 196.70),
    ])

    # Exact base visual cuts and narration-safe edit boundaries.
    EQUATION_OUT = fr(46.72)      # after "for a claim to hold up"
    REACTIONS_IN = 1695           # 56.500, raw cut from chocolate photo
    REACTIONS_OUT = 2300          # 76.667, raw cut into the study example
    HABITS_IN = fr(HABITS_BOARD_IN_SECONDS)  # quiet boundary after "confirmation bias"
    BASE_H45_IN = fr(156.18)      # start of the clean gap before Habit 4
    BASE_H45_OUT = fr(174.02)     # "These five questions..." onset
    DONOR_H45 = (fr(153.48), fr(DONOR_H45_OUT_SECONDS))
    HABITS_SUMMARY_OUT = fr(181.24)  # through "with artificial intelligence"
    AI_DIAGRAM_IN = 5461          # 182.033, raw cut to the inaccurate paper
    CLOSE_IN = 5670               # 189.000, raw cut to the close
    CLOSE_OUT = fr(193.70)        # after the exact two-line close, before logo

    donor_h45_len = DONOR_H45[1] - DONOR_H45[0]
    habits_after_graft = BASE_H45_IN + donor_h45_len
    habits_virtual_out = habits_after_graft + (HABITS_SUMMARY_OUT - BASE_H45_OUT)

    # Board 1 stays intact through the definition and the tool-level takeaway.
    b.keep(0, EQUATION_OUT, "B1 What You Know. How You Think.", "equation")
    b.pause(15, "Half-second pause after 'for a claim to hold up'")

    # Reroll 3's drawn newspaper/headline sequence replaces the stock chocolate
    # photo while reroll 4's approved narration remains untouched.
    b.keep(
        EQUATION_OUT,
        REACTIONS_IN,
        "Reroll 3 picture: hand-drawn chocolate newspaper and headline",
        video_from=1368,
        video_src=DONOR,
        video_end=1689,
    )
    b.keep(REACTIONS_IN, REACTIONS_OUT, "B2 Same Claim. Different Thinking.", "reactions")
    b.keep(REACTIONS_OUT, HABITS_IN, "Notebook: study design, sample sizes, website, journalist, and confirmation-bias drawings")
    b.pause(15, "Half-second pause after 'confirmation bias'")

    b.keep(HABITS_IN, BASE_H45_IN, "B3 Five Habits through Habit 3", "habits")
    b.graft(
        DONOR,
        DONOR_H45[0],
        DONOR_H45[1],
        "Reroll 3 audio: complete and correctly worded Habits 4-5",
        "reroll3-habits-4-5",
        picture_from=BASE_H45_IN,
        gain_db=-0.4,
        visual="habits",
    )
    b.keep(
        BASE_H45_OUT,
        HABITS_SUMMARY_OUT,
        "B3 full-board summary through applying the questions to AI",
        "habits",
        video_from=habits_after_graft,
    )

    # Replace the inaccurate lorem-style page with reroll 3's accurate AI
    # decision diagram. V4 also removes the short old-laptop bridge that David
    # identified as a flash at 3:02.
    if KEEP_LAPTOP_BRIDGE:
        b.keep(HABITS_SUMMARY_OUT, AI_DIAGRAM_IN, "Notebook: AI laptop drawing")
        diagram_audio_in = AI_DIAGRAM_IN
    else:
        diagram_audio_in = HABITS_SUMMARY_OUT
    b.keep(
        diagram_audio_in,
        CLOSE_IN,
        "Reroll 3 picture: accurate AI decision diagram",
        video_from=5308,
        video_src=DONOR,
        video_end=5508,
    )

    b.mark_close_start()
    b.close(CLOSE_IN, CLOSE_OUT)
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

    # Board 1 is readable in the full frame; rings follow the spoken equation.
    b.board(
        "equation", BOARDS["equation"], 0, EQUATION_OUT, "compact",
        [
            target("Knowledge", 12.16, [90, 167, 751, 463], BLUE),
            target("Critical Thinking", 21.68, [850, 167, 1511, 463], TEAL),
            target("Better Questions + Better Decisions", 32.84, [90, 562, 1511, 675], PURPLE),
        ],
        banner_at=38.34,
        banner=[40, 756, 1560, 845],
    )

    # Board 2 is tall and dense: establish the claim, visit each complete
    # reaction card, and return to the full board for the conclusion.
    b.board(
        "reactions", BOARDS["reactions"], REACTIONS_IN, REACTIONS_OUT, "dense",
        [
            target("The Claim", 59.22, [40, 127, 1560, 252], PURPLE, cam=[40, 127, 1560, 252]),
            target("Face Value", 60.16, [40, 279, 784, 910], AMBER, cam=[40, 279, 784, 910]),
            target("Critical Thinking", 65.16, [816, 279, 1560, 910], GREEN, cam=[816, 279, 1560, 910]),
        ],
        banner_at=71.12,
        pullback_at=70.28,
        banner=[40, 949, 1560, 1039],
    )

    def donor_mapped(t):
        return (BASE_H45_IN + (fr(t) - DONOR_H45[0])) / 30

    # Board 3 visits each complete habit card. Habits 4 and 5 use virtual
    # source positions because their corrected donor narration is shorter.
    b.board(
        "habits", BOARDS["habits"], HABITS_IN, habits_virtual_out, "dense",
        [
            target("Habit 1", 133.98, [40, 141, 330, 623], PURPLE, cam=[40, 141, 330, 623]),
            target("Habit 2", 142.30, [347, 141, 638, 623], BLUE, cam=[347, 141, 638, 623]),
            target("Habit 3", 149.98, [655, 141, 946, 623], TEAL, cam=[655, 141, 946, 623]),
            target("Habit 4", donor_mapped(154.50), [963, 141, 1254, 623], GREEN, cam=[963, 141, 1254, 623]),
            target("Habit 5", donor_mapped(163.12), [1271, 141, 1560, 623], AMBER, cam=[1271, 141, 1560, 623]),
        ],
        banner_at=habits_after_graft / 30,
        pullback_at=donor_mapped(169.14),
        banner=[40, 660, 1560, 750],
    )

    b.render_legs()
    for key in b.boards:
        # Preserve already-generated review sheets when a storage-recovery
        # rerun only needs to recreate the lossless render legs.
        if not (AUDIT / f"states-{key}.jpg").exists():
            b.state_sheet(key)
    b.make_close("critical")
    b.manifest({
        "approved_repair_plan": {
            "base": str(BASE),
            "donor": str(DONOR),
            "replaced_base_habits_4_5_frames": [BASE_H45_IN, BASE_H45_OUT],
            "donor_habits_4_5_frames": list(DONOR_H45),
            "donor_gain_db": -0.4,
            "habits_board_in_seconds": HABITS_BOARD_IN_SECONDS,
            "donor_habits_4_5_out_seconds": DONOR_H45_OUT_SECONDS,
            "keep_laptop_bridge": KEEP_LAPTOP_BRIDGE,
        },
        "selective_pause_plan": [
            {
                "after": "for a claim to hold up",
                "duration_frames": 15,
                "duration_seconds": 0.5,
                "visual": "canonical equation board",
            },
            {
                "after": "confirmation bias",
                "duration_frames": 15,
                "duration_seconds": 0.5,
                "visual": "last Notebook study frame before canonical habits board",
            },
        ],
        "borrowed_visuals": [
            {
                "purpose": "replace stock chocolate photograph",
                "source": str(DONOR),
                "source_frames": [1368, 1661],
            },
            {
                "purpose": "replace inaccurate lorem-style AI paper",
                "source": str(DONOR),
                "source_frames": [5308, 5508],
                "held_final_frames": max(0, CLOSE_IN - diagram_audio_in - (5508 - 5308)),
            },
        ],
        "board_plan": {
            "equation": "compact full-board view; Knowledge, Critical Thinking, result, takeaway",
            "reactions": "full establish; claim and two complete-card dives; full-board takeaway",
            "habits": "full establish; five complete-card dives; full-board takeaway and AI summary",
        },
        "listening_required": [
            "the two half-second room-tone pause insertions",
            "both joins around the reroll-3 Habits 4-5 audio graft",
            "the transition from the habits summary back to reroll-4 narration",
            "the exact two-line close and its tail",
        ],
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
