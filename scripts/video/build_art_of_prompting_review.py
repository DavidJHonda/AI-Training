#!/usr/bin/env python3
"""Build the Art of Prompting best-of review candidate (2026-09-16).

Full production pass from Prompts/art-of-prompting-1.mp4. The approved plan:
replace the thin four-quality list with three board-covered donor runs, mute the
literal placeholder words in move two, remove the overclaim after move four,
replace every Notebook course-board render with the current page JPGs, cover
photographs and the gibberish document, clean the engine corner mark, and end
on the canonical standard close. Review candidate only; the live lesson/video
is unchanged.
"""

from pathlib import Path
import argparse
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import (  # noqa: E402
    AMBER,
    BLUE,
    NEUTRAL,
    PURPLE,
    SPF,
    TEAL,
    Build,
    fr,
)


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/art-of-prompting-1.mp4"
SRC2 = ROOT / "Prompts/art-of-prompting-2.mp4"
Q_DONOR = ROOT / "Prompts/questions-matter-1.mp4"
OUT = ROOT / "video-audit/art-of-prompting-repair-2026-09-16"
DEST = ROOT / "Prompts/art-of-prompting-v3.mp4"

ASSET_DIR = ROOT / "course-assets/art-of-prompting"
GOOD = ASSET_DIR / "art-of-prompting-good-question.jpg"
MOVES12 = ASSET_DIR / "art-of-prompting-four-moves.jpg"
MOVES34 = ASSET_DIR / "art-of-prompting-four-moves-continued.jpg"
CLOSE = ASSET_DIR / "art-of-prompting-close.jpg"


def target(label, at_frame, rect, cam, color, radius=18):
    return {
        "label": label,
        "at": at_frame / 30,
        "rects": [rect],
        "cam": cam,
        "color": color,
        "radius": radius,
    }


def mute_keep(build, start, end, label):
    """Keep moving source video while replacing a spoken artifact with room tone."""
    build.keep(start, end, label)
    build.parts[-1] = build.tone((end - start) * SPF)
    build.rows[-1]["audio_replacement"] = "matched room tone"


def add_intro_banner_ring(build, key, start_frame, end_frame, rect):
    """Add the early foundation-banner ring without changing the dense camera path."""
    board = build.boards[key]
    ox, oy = board["canvas_offset"]
    x1, y1, x2, y2 = rect
    ring = {
        "start": start_frame - board["src_in"],
        "end": end_frame - board["src_in"],
        "rect": [x1 + ox, y1 + oy, x2 - x1, y2 - y1],
        "color": NEUTRAL,
        "pad": 0,
        "radius": 22,
    }
    board["rings"].insert(0, ring)
    board["states"].insert(
        0,
        {
            "spoken_onset_source_frame": start_frame,
            "highlight_target": "foundation banner",
            "highlight_mode": "ring",
            "highlight_color": NEUTRAL,
            "highlight_source": "neutral_video_purple",
        },
    )
    spec_path = build.out / f"leg-{key}.json"
    spec = json.loads(spec_path.read_text())
    spec["rings"].insert(0, ring)
    spec_path.write_text(json.dumps(spec, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare-only", action="store_true")
    args = ap.parse_args()

    b = Build(
        ROOT,
        SRC,
        OUT,
        DEST,
        protected=[SRC2, Q_DONOR, GOOD, MOVES12, MOVES34, CLOSE],
    )
    b.load_audio(
        [
            (5.50, 6.01),
            (17.64, 18.22),
            (26.06, 26.67),
            (30.76, 31.34),
            (39.21, 39.76),
            (54.79, 55.45),
            (82.14, 83.03),
            (99.54, 100.14),
            (110.17, 110.89),
            (119.68, 120.34),
            (138.80, 139.51),
            (158.91, 159.72),
            (169.42, 170.15),
            (190.33, 190.94),
            (199.52, 200.03),
            (222.90, 223.57),
            (234.89, 238.40),
        ]
    )

    # Stable visual substitutions for source material that cannot ship.
    # Roll 2 frames are used in increasing order, per the donor-library rule.
    b.keep(
        0,
        177,
        "Roll 2 drawing: two people talking (covers the Socrates photograph)",
        video_from=0,
        video_src=SRC2,
        video_end=177,
    )
    b.keep(177, 545, "Notebook: shared-context bridge and AI system")
    b.keep(
        545,
        797,
        "Roll 2 drawings: server room and structured briefing (covers gibberish document)",
        video_from=518,
        video_src=SRC2,
        video_end=770,
    )

    # Good-question board with the approved composite definition replacement.
    good_in, quality_cut, quality_resume, good_out = 797, fr(31.05), fr(39.50), 1361
    v2_open_specific = (fr(35.25), fr(44.30))
    q_on_target = (fr(151.70), fr(156.35))
    v2_open_ended = (fr(46.65), fr(51.00))
    leg_open_specific = quality_cut
    leg_on_target = leg_open_specific + (v2_open_specific[1] - v2_open_specific[0])
    leg_open_ended = leg_on_target + (q_on_target[1] - q_on_target[0])
    leg_resume = leg_open_ended + (v2_open_ended[1] - v2_open_ended[0])
    good_leg_out = leg_resume + (good_out - quality_resume)

    b.keep(good_in, quality_cut, "Good-question board: foundation", "good-question")
    b.graft(
        SRC2,
        *v2_open_specific,
        "Roll 2 audio: Open-Minded and Specific definitions",
        "roll2-open-specific",
        picture_from=leg_open_specific,
        gain_db=-0.8,
        visual="good-question",
    )
    b.graft(
        Q_DONOR,
        *q_on_target,
        "Questions Matter audio: On Target definition",
        "questions-on-target",
        picture_from=leg_on_target,
        gain_db=1.7,
        visual="good-question",
    )
    b.graft(
        SRC2,
        *v2_open_ended,
        "Roll 2 audio: Open-Ended definition",
        "roll2-open-ended",
        picture_from=leg_open_ended,
        gain_db=-1.5,
        visual="good-question",
    )
    b.keep(
        quality_resume,
        good_out,
        "Good-question board: transition into the four moves",
        "good-question",
        video_from=leg_resume,
    )

    b.keep(good_out, 1661, "Notebook: four-move briefing introduction")

    # Move 1 board, then Notebook's worked-example drawing.
    b.keep(1661, 2149, "Four Moves board: Move 1", "moves12-move1")
    b.keep(2149, fr(82.20), "Notebook: Move 1 better-prompt diagram")

    # Bring the board in during the existing silence so the title can ring in full view.
    move2_in = fr(82.20)
    b.keep(move2_in, 3003, "Four Moves board: Move 2", "moves12-move2")

    # Preserve the animated better-prompt diagram; mute only the two literal placeholders.
    paragraph_mute = (fr(104.55), fr(105.00))
    question_mute = (fr(107.65), fr(108.04))
    b.keep(3003, paragraph_mute[0], "Notebook: Move 2 better-prompt diagram")
    mute_keep(b, *paragraph_mute, 'Muted literal placeholder: "Paragraph"')
    b.keep(paragraph_mute[1], question_mute[0], "Notebook: Move 2 better-prompt diagram")
    mute_keep(b, *question_mute, 'Muted literal placeholder: "Question"')
    b.keep(question_mute[1], 3611, "Notebook: Move 2 material and guesswork diagrams")

    # The continued board is introduced whole; Notebook's drawings carry Move 3.
    b.keep(3611, 3832, "Four Moves Continued: full-board introduction", "moves34-intro")
    move4_in = fr(159.00)
    b.keep(3832, move4_in, "Notebook: Move 3 format, limits, and caption diagrams")
    b.keep(move4_in, 5105, "Four Moves Continued: Move 4", "moves34-move4")
    b.keep(5105, fr(190.34), "Notebook: Move 4 paper and one-job-at-a-time diagrams")

    # Approved cut: remove the overclaim, including its stock photograph.
    overclaim = (fr(190.34), fr(200.00))
    # The resume audio begins four frames before Notebook's next drawn scene; hold
    # that destination drawing so no photograph flashes at the join.
    b.pause(30, "Approved one-second pause after the thesis-first example")
    b.keep(
        overclaim[1],
        6004,
        'Resume: "You do not need to apply this entire framework every single time"',
        video_from=6004,
        video_end=6005,
    )
    b.keep(6004, 6713, "Notebook: packaging scaled to the task")

    b.mark_close_start()
    b.close(6713, 7062)
    b.finish_audio()

    # Board coordinates are in the exact current JPGs.
    good_cards = [
        [40, 127, 784, 633],
        [816, 127, 1560, 633],
        [40, 665, 784, 1175],
        [816, 665, 1560, 1175],
    ]
    open_at = leg_open_specific + (fr(35.54) - v2_open_specific[0])
    specific_at = leg_open_specific + (fr(40.02) - v2_open_specific[0])
    target_at = leg_on_target + (fr(152.02) - q_on_target[0])
    ended_at = leg_open_ended + (fr(46.86) - v2_open_ended[0])
    b.board(
        "good-question",
        GOOD,
        good_in,
        good_leg_out,
        "dense",
        [
            target("Open-Minded", open_at, good_cards[0], good_cards[0], PURPLE),
            target("Specific", specific_at, good_cards[1], good_cards[1], BLUE),
            target("On Target", target_at, good_cards[2], good_cards[2], TEAL),
            target("Open-Ended", ended_at, good_cards[3], good_cards[3], AMBER),
        ],
        pullback_at=leg_resume / 30,
    )
    # Follow the banner itself exactly; the previous box extended into the footer.
    add_intro_banner_ring(b, "good-question", fr(29.00), open_at, [40, 1213, 1560, 1302])

    move1_card = [40, 127, 784, 1433]
    move2_card = [816, 127, 1560, 1433]
    b.board(
        "moves12-move1",
        MOVES12,
        1661,
        2149,
        "dense",
        [
            target("Move 1 whole card", fr(58.30), move1_card, move1_card, PURPLE),
            # Keep the ring outside both the INCLUDE label and the bullet dots.
            target("Move 1 Include", fr(61.76), [52, 720, 772, 936], move1_card, PURPLE),
            target("Move 1 Weak", fr(67.92), [52, 945, 772, 1105], move1_card, PURPLE),
        ],
    )
    b.board(
        "moves12-move2",
        MOVES12,
        move2_in,
        3003,
        "dense",
        [
            target("Move 2 whole card", fr(82.90), move2_card, move2_card, BLUE),
            target("Move 2 Include", fr(85.46), [828, 720, 1548, 936], move2_card, BLUE),
            target("Move 2 Weak", fr(95.88), [828, 945, 1548, 1105], move2_card, BLUE),
        ],
        min_open=0,
    )

    b.board("moves34-intro", MOVES34, 3611, 3832, "compact", [], push=False)
    move4_card = [816, 127, 1560, 1551]
    b.board(
        "moves34-move4",
        MOVES34,
        move4_in,
        5105,
        "dense",
        [
            target("Move 4 whole card", fr(159.60), move4_card, move4_card, AMBER),
            target("Move 4 Include", fr(162.40), [828, 745, 1548, 955], move4_card, AMBER),
        ],
        min_open=0,
    )

    b.render_legs()
    for key in b.boards:
        b.state_sheet(key)
    b.make_close("prompting")
    b.manifest(
        {
            "build_scope": "full production pass; review only",
            "approved_narration_repairs": {
                "thin_quality_list_removed_frames": [quality_cut, quality_resume],
                "placeholder_room_tone_frames": [list(paragraph_mute), list(question_mute)],
                "overclaim_removed_frames": list(overclaim),
            },
            "photographs_replaced": [
                {"source_frames": [0, 177], "cover": "art-of-prompting-2 frames 0-177"},
                {"source_frames": [5733, 6004], "cover": "removed with overclaim; destination drawing held for frames 6000-6004"},
            ],
            "gibberish_replaced": {
                "source_frames": [545, 797],
                "cover": "art-of-prompting-2 frames 518-770",
            },
            "approved_added_pause_frames": {
                "after_thesis_first_example": 30,
            },
            "longest_unbroken_board_run_frames": good_leg_out - good_in,
            "notebook_interleaves": [
                [2149, move2_in],
                [3003, 3611],
                [3832, move4_in],
                [5105, fr(190.34)],
            ],
        }
    )
    print(
        "Prepared",
        b.total,
        f"{b.total / 30:.2f}s",
        {k: (v["src_in"], v["src_out"], v["full_view_frames"]) for k, v in b.boards.items()},
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
