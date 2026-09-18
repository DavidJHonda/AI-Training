#!/usr/bin/env python3
"""Build the corrected Loudest Voices best-of review candidate.

Full production pass, review only.  Roll 1 supplies the spine; roll 2's complete
Dario Amodei beat replaces roll 1's thinner beat under the canonical expert
board.  Both current course boards and the canonical close replace Notebook's
renders.  Notebook drawings, never photographs, break up the long first board.
No teaching pauses are added. Person introductions stay on the full expert
board; the SAYS and BUT ADMITS beats use section-level zooms and rings.
"""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, AMBER, NEUTRAL


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/loudest-voices-1.mp4"
DONOR = ROOT / "Prompts/loudest-voices-2.mp4"
OUT = ROOT / "video-audit/loudest-voices-highlight-repair-2026-09-18"
DEST = ROOT / "Prompts/loudest-voices-v5.mp4"

EXPERTS = ROOT / "course-assets/loudest-voices/loudest-voices-experts.jpg"
PREDICTIONS = ROOT / "course-assets/loudest-voices/loudest-voices-missed-predictions.jpg"
CLOSE = ROOT / "course-assets/loudest-voices/loudest-voices-close.jpg"
LESSON = ROOT / "lessons/loudest-voices.md"

# Visual cuts in roll 1, confirmed by sequential decode.
B1_IN = 789                 # 0:26.30, Notebook cuts to its expert-board render
B1_OUT = 3882               # 2:09.40, "This has happened before" handoff
B2_OUT = 6208               # 3:26.93, after "people ultimately determine the result"
CLOSE_IN = 6607             # 3:40.23, engine close arrives
CLOSE_AUDIO_END = 6866      # 3:48.87, after "...your call"

# Approved best-of graft.  Boundaries sit inside measured quiet on both rolls.
BASE_GRAFT_IN = 1061        # roll 1 0:35.37, before "Let's start with our optimist"
BASE_RESUME = 1827          # roll 1 1:00.90, "Next is the Worrier"
DONOR_GRAFT = (1375, 2202)  # roll 2 0:45.83-1:13.40, complete Dario beat + room tone
GAIN_DB = 1.1               # donor -19.7 dBFS; base -18.6 dBFS

GRAFT_LEN = DONOR_GRAFT[1] - DONOR_GRAFT[0]
DELTA = GRAFT_LEN - (BASE_RESUME - BASE_GRAFT_IN)


def virtual(frame: int) -> int:
    """Map post-graft roll-1 frame coordinates onto the output/board clock."""
    return frame if frame < BASE_RESUME else frame + DELTA


def vsec(frame: int) -> float:
    return virtual(frame) / 30.0


def donor_vsec(seconds: float) -> float:
    return (BASE_GRAFT_IN + (fr(seconds) - DONOR_GRAFT[0])) / 30.0


def target(label, at, rect, color, cam=None, *, full_view=False, camera_at=None):
    item = {
        "label": label,
        "at": at,
        "rects": [rect],
        "color": color,
        "radius": 18,
    }
    if cam is not None:
        item["cam"] = cam
    if full_view:
        item["full_view"] = True
    if camera_at is not None:
        item["camera_at"] = camera_at
    return item


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument(
        "--render-existing",
        action="store_true",
        help="reuse already-verified board legs from a prepare-only pass",
    )
    args = parser.parse_args()

    build = Build(
        ROOT,
        SRC,
        OUT,
        DEST,
        protected=[DONOR, EXPERTS, PREDICTIONS, CLOSE, LESSON],
    )
    build.load_audio([
        (5.97, 6.45), (14.94, 15.41), (16.94, 17.50),
        (25.85, 26.38), (35.37, 35.99), (38.53, 39.04),
        (42.28, 42.77), (49.20, 49.62), (62.58, 63.00),
        (67.54, 67.73), (73.20, 73.62), (81.40, 81.83),
        (88.81, 89.62), (98.86, 99.43), (107.18, 107.63),
        (116.49, 117.07), (128.93, 129.45), (138.25, 138.66),
        (151.79, 152.38), (168.02, 168.66), (181.94, 182.42),
        (197.47, 198.02), (206.25, 206.91), (219.39, 220.11),
        (223.48, 224.18), (226.48, 226.98), (228.87, 232.20),
    ])

    # The timeline preserves roll 1 outside the approved Dario replacement.
    build.keep(0, B1_IN, "Notebook drawings: public opinions and AI builders")
    build.keep(B1_IN, BASE_GRAFT_IN, "Even the Experts Don't Know: full-board introduction", "experts")
    build.graft(
        DONOR,
        DONOR_GRAFT[0],
        DONOR_GRAFT[1],
        "Roll 2 audio: complete Dario Amodei view and counterpoint under the expert board",
        "roll2-dario",
        picture_from=BASE_GRAFT_IN,
        gain_db=GAIN_DB,
        visual="experts",
    )

    # Hinton: cover the source photograph with the course board, then retain the
    # safe Notebook city/system drawing between measured pauses.
    hinton_drawing_in = fr(67.60)
    hinton_drawing_out = fr(73.53)
    build.keep(
        BASE_RESUME,
        hinton_drawing_in,
        "Expert board: Hinton background (covers source photograph)",
        "experts",
        video_from=virtual(BASE_RESUME),
    )
    build.keep(hinton_drawing_in, hinton_drawing_out, "Notebook drawing: AI system and human silhouette")
    build.keep(
        hinton_drawing_out,
        B1_OUT,
        "Expert board: Hinton and LeCun claims, admissions, and three-view synthesis",
        "experts",
        video_from=virtual(hinton_drawing_out),
    )

    # The raw roll uses only photographs during the four history examples, so
    # the canonical board stays continuous through its spoken takeaway.
    build.keep(
        B1_OUT,
        B2_OUT,
        "This Has Happened Before: four predictions and takeaway (covers all source photographs)",
        "predictions",
        video_from=virtual(B1_OUT),
    )
    build.keep(B2_OUT, CLOSE_IN, "Notebook drawings: machine speed, human habits, and the missing variable")

    build.mark_close_start()
    build.close(CLOSE_IN, CLOSE_AUDIO_END, tail=120)
    build.finish_audio()

    # Board 1: introductions stay on the complete board.  Each SAYS and BUT
    # ADMITS beat then gets its own section-level camera and correctly padded
    # ring, including the section label instead of striking through it.
    dario = [40, 127, 526, 1511]
    hinton = [557, 127, 1043, 1511]
    lecun = [1075, 127, 1560, 1511]
    dario_says = [60, 734, 506, 1084]
    dario_admits = [60, 1107, 506, 1502]
    hinton_says = [578, 734, 1024, 1084]
    hinton_admits = [578, 1107, 1024, 1340]
    lecun_says = [1096, 734, 1542, 1084]
    lecun_admits = [1096, 1107, 1542, 1422]
    build.board(
        "experts",
        EXPERTS,
        B1_IN,
        virtual(B1_OUT),
        "dense",
        [
            target("Dario Amodei: Optimist", donor_vsec(46.18), dario, PURPLE, full_view=True),
            target("Dario says", donor_vsec(53.92), dario_says, PURPLE, dario_says),
            target("Dario admits", donor_vsec(61.92), dario_admits, PURPLE, dario_admits),
            target("Geoffrey Hinton: Worrier", vsec(fr(60.90)), hinton, BLUE, full_view=True),
            target("Hinton says", vsec(fr(73.62)), hinton_says, BLUE, hinton_says,
                   camera_at=vsec(hinton_drawing_out)),
            target("Hinton admits", vsec(fr(81.72)), hinton_admits, BLUE, hinton_admits),
            target("Yann LeCun: Doubter", vsec(fr(89.70)), lecun, TEAL, full_view=True),
            target("LeCun says", vsec(fr(99.50)), lecun_says, TEAL, lecun_says),
            target("LeCun admits", vsec(fr(107.40)), lecun_admits, TEAL, lecun_admits),
        ],
        pullback_at=vsec(fr(116.49)),
        per_target_camera=True,
        lead_camera=True,
    )

    # Board 2: each example gets one complete-card ring; the full board returns
    # for the lesson's people-change-the-result takeaway.
    stoll = [40, 127, 785, 759]
    ballmer = [815, 127, 1560, 759]
    metcalfe = [40, 791, 785, 1424]
    ford = [815, 791, 1560, 1424]
    build.board(
        "predictions",
        PREDICTIONS,
        virtual(B1_OUT),
        virtual(B2_OUT),
        "dense",
        [
            target("Clifford Stoll: online shopping", vsec(fr(138.72)), stoll, PURPLE, stoll),
            target("Steve Ballmer: iPhone", vsec(fr(152.40)), ballmer, BLUE, ballmer),
            target("Robert Metcalfe: internet collapse", vsec(fr(168.66)), metcalfe, TEAL, metcalfe),
            target("Henry Ford: flying cars", vsec(fr(182.44)), ford, AMBER, ford),
        ],
        banner_at=vsec(fr(198.00)),
        pullback_at=vsec(fr(197.00)),
        per_target_camera=True,
        lead_camera=True,
    )

    if not args.render_existing:
        build.render_legs()
        build.state_sheet("experts")
        build.state_sheet("predictions")
    build.make_close("whatpeoplesay")
    build.manifest({
        "scope_detail": "Full production review candidate from approved best-of plan; live video and lesson unchanged.",
        "narration_graft": {
            "base_replaced_frames": [BASE_GRAFT_IN, BASE_RESUME],
            "donor_frames": list(DONOR_GRAFT),
            "gain_db": GAIN_DB,
        },
        "added_teaching_pauses": [],
        "photographs_replaced": [
            "Geoffrey Hinton portrait",
            "Yann LeCun portrait",
            "shopping mall",
            "Steve Ballmer",
            "iPhone launch/product photograph",
            "old desktop computer",
            "Henry Ford portrait",
        ],
        "notebook_interleaves": [
            {"source_frames": [hinton_drawing_in, hinton_drawing_out], "description": "AI system and human silhouette"},
        ],
        "longest_unbroken_board_run_seconds": round((B1_OUT - hinton_drawing_out) / 30, 2),
    })

    print(
        "Prepared",
        build.total,
        f"frames ({build.total / 30:.2f}s)",
        "graft delta",
        DELTA,
        "frames",
        flush=True,
    )
    if args.prepare_only:
        return
    build.render()
    print(DEST)


if __name__ == "__main__":
    main()
