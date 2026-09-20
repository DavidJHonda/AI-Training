#!/usr/bin/env python3
"""Build the approved Fake Trap best-of review candidate.

Full production pass, review only.  Fake-trap-2 supplies the spine.  The
complete four-motive explanation comes from Fake-trap-1 under the canonical
reasons board.  Candidate 2's unsupported detector sentence is removed at its
own scene boundaries, and its final lie-detector conclusion is moved before the
two required closing lines.  The live video and both raw rolls remain unchanged.
"""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, AMBER, RED, NEUTRAL


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/fake-trap-2.mp4"
DONOR = ROOT / "Prompts/fake-trap-1.mp4"
LIVE = ROOT / "course-assets/fake-trap/fake-trap.mp4"
OUT = ROOT / "video-audit/fake-trap-repair-2026-09-18"
DEST = ROOT / "Prompts/fake-trap-v1.mp4"
OUT_V2 = ROOT / "video-audit/fake-trap-repair-2026-09-20-v2"
DEST_V2 = ROOT / "Prompts/fake-trap-v2.mp4"

COMPARISON = ROOT / "course-assets/fake-trap/fake-trap-comparison.jpg"
REASONS = ROOT / "course-assets/fake-trap/fake-trap-reasons.jpg"
SOURCE = ROOT / "course-assets/fake-trap/fake-trap-follow-the-source.jpg"
CHECKS = ROOT / "course-assets/fake-trap/fake-trap-checks.jpg"
CLOSE = ROOT / "course-assets/fake-trap/fake-trap-close.jpg"
LESSON = ROOT / "lessons/fake-trap.md"
PAGE = ROOT / "index.html"

# Candidate-2 visual cuts, confirmed by sequential frame decode.
COMPARE_IN, COMPARE_OUT = 400, 1005             # 0:13.33-0:33.50
PHOTO_IN, PHOTO_OUT = 1409, 1697                # 0:46.97-0:56.57
REASONS_IN, THIN_REASONS_OUT = 1951, 2551       # 1:05.03-1:25.03
REASONS_INTRO_OUT = 2241                        # after "four things"
DETECTOR_IN, WRONG_SENTENCE_IN = 2551, 3314     # detector through "not definitive proof"
WRONG_SENTENCE_OUT = 3540                       # resumes on "Fakes travel quickly"
SOURCE_IN, SOURCE_OUT = 3803, 3939              # 2:06.77-2:11.30
CHECKS_IN, CHECKS_OUT = 3939, 5444              # 2:11.30-3:01.47
RESOURCE_IN, RESOURCE_OUT = 6491, 6731           # displayed web address
SAFETY_TO_MOVE = 6960                           # 3:52.00, quiet before "So always"
RAW_CLOSE_OUT = 7219                            # 4:00.63, source cut after hard close
EYES_IN, EYES_OUT = 7219, 7475                  # moved conclusion, through quiet

# Candidate-1 approved whole-beat donor.  Start is a -75 dB trough 120 ms
# before "First is money"; end is a -70 dB trough after the final sibilant in
# "school environments" and before the next sentence's onset.
MOTIVES_DONOR = (2604, 3544)                    # 1:26.80-1:58.13
MOTIVES_GAIN_DB = 0.8                           # donor mix measured 0.8 dB lower

# Candidate-1 drawing that replaces candidate 2's photo-real trophy span.
HOCKEY_DRAWING_IN = 1909                        # 1:03.63, harmless-joke drawing

# Live-video neutral report/NCMEC diagram, ending before the no-fault scene.
LIVE_RESOURCE_IN, LIVE_RESOURCE_OUT = 6087, 6306

# Revision 2 user corrections.  The live opening ends on its next scene cut,
# after the harmless-joke conclusion and before the live motive board.  The
# NCMEC replacement begins only once both resource labels are fully visible.
LIVE_OPENING_OUT = 2229                         # 1:14.30
LIVE_OPENING_GAIN_DB = 0.8
LIVE_RESOURCE_V2_IN, LIVE_RESOURCE_V2_OUT = 6180, 6300  # 3:26.00-3:30.00

MOTIVES_LEN = MOTIVES_DONOR[1] - MOTIVES_DONOR[0]
MOTIVES_VIRTUAL_END = REASONS_INTRO_OUT + MOTIVES_LEN


def donor_onset(seconds: float) -> float:
    """Map a donor-roll word onset onto the synthetic reasons-board clock."""
    return (REASONS_INTRO_OUT + (fr(seconds) - MOTIVES_DONOR[0])) / 30.0


def target(label, at, rect, color, cam=None, *, full_view=False):
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
    return item


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument(
        "--render-existing",
        action="store_true",
        help="reuse board and moved-conclusion legs from a prepare-only pass",
    )
    parser.add_argument(
        "--revision-v2",
        action="store_true",
        help="use the live 0:00-1:14.30 opening and an immediately visible CyberTipline card",
    )
    args = parser.parse_args()

    out = OUT_V2 if args.revision_v2 else OUT
    dest = DEST_V2 if args.revision_v2 else DEST

    build = Build(
        ROOT,
        SRC,
        out,
        dest,
        protected=(
            [DONOR, LIVE, COMPARISON, REASONS, SOURCE, CHECKS, CLOSE, LESSON]
            + ([] if args.revision_v2 else [PAGE])
        ),
    )
    build.load_audio([
        (4.70, 5.06), (7.38, 8.04), (12.62, 13.38),
        (24.20, 24.88), (26.22, 27.10), (32.64, 33.52),
        (46.28, 46.94), (58.82, 59.48), (64.32, 65.04),
        (71.38, 72.20), (73.86, 74.70), (84.26, 85.14),
        (107.88, 108.56), (109.74, 110.48), (117.22, 118.08),
        (120.20, 121.16), (126.08, 126.76), (130.46, 131.06),
        (144.14, 145.02), (153.04, 153.82), (158.50, 159.34),
        (164.52, 165.32), (174.16, 175.24), (177.94, 178.66),
        (186.40, 187.08), (192.56, 193.58), (202.66, 203.40),
        (215.68, 216.34), (223.62, 224.36), (231.84, 232.06),
        (234.58, 235.24), (237.30, 238.00), (240.10, 240.62),
    ])

    if args.revision_v2:
        # The live opening teaches the school example, both jaws of the trap,
        # and the harmless-joke distinction more fully.  End on the live scene
        # cut after “no one is meant to believe it,” then resume candidate 2 in
        # its quiet scene change before “The danger doesn't come...”.
        build.graft(
            LIVE,
            0,
            LIVE_OPENING_OUT,
            "Live-video opening through complete harmless-joke conclusion",
            "live-opening",
            cover_intro=False,
            gain_db=LIVE_OPENING_GAIN_DB,
        )
        build.keep(
            PHOTO_OUT,
            REASONS_IN,
            "Candidate-2 deception boundary: danger begins when a lie is believed",
        )
    else:
        # Opening and school-closure comparison.
        build.keep(0, COMPARE_IN, "Notebook drawings: convincing clip and reaction window")
        build.keep(COMPARE_IN, COMPARE_OUT, "The Same Clip. Two Eras.", "comparison")
        build.keep(COMPARE_OUT, PHOTO_IN, "Notebook drawings: the two-jawed Fake Trap")

        # Candidate 2 uses a photo-real trophy here.  Candidate 1 drew the same
        # harmless-joke idea, so borrow that drawing while retaining candidate
        # 2's approved narration and timing.
        build.keep(
            PHOTO_IN,
            PHOTO_OUT,
            "Candidate-1 drawing: harmless hockey joke (covers photo-real trophy)",
            video_from=HOCKEY_DRAWING_IN,
            video_src=DONOR,
            video_end=2488,
        )
        build.keep(PHOTO_OUT, REASONS_IN, "Notebook drawing: friends share the joke; deception boundary")

    # Candidate 2 introduces the board and its takeaway.  Candidate 1 then
    # supplies the complete four-item teaching beat under the same course board.
    build.keep(REASONS_IN, REASONS_INTRO_OUT, "Why Some Fakes Aren't Friendly: introduction", "reasons")
    build.graft(
        DONOR,
        MOTIVES_DONOR[0],
        MOTIVES_DONOR[1],
        "Candidate-1 audio: complete money, power, fame, and cruelty explanations",
        "candidate1-motives",
        picture_from=REASONS_INTRO_OUT,
        gain_db=MOTIVES_GAIN_DB,
        visual="reasons",
    )

    # Retain the accurate detector passage, then delete the unsupported sentence
    # at the source's exact visual cuts.  The resumed audio starts 80 ms before
    # "Fakes travel quickly," preserving its natural onset.
    build.keep(DETECTOR_IN, WRONG_SENTENCE_IN, "Notebook drawings: detectors disagree; clue, not ruling")
    build.keep(WRONG_SENTENCE_OUT, SOURCE_IN, "Notebook drawing: emotion spike and stop cue")

    # Current page assets replace both face-bearing/post-production boards and
    # Notebook's rendering of the three checks.
    build.keep(SOURCE_IN, SOURCE_OUT, "Check the Source, Not the Pixels", "follow-source")
    build.keep(CHECKS_IN, CHECKS_OUT, "Move the Test Off the Image", "checks")

    build.keep(CHECKS_OUT, RESOURCE_IN, "Notebook drawings: voicemail, viral clip, and personal-safety guidance")

    # Candidate 2 displays a web address here despite the generation prompt.
    # Reuse the live video's concise, URL-free report/NCMEC diagram and hold its
    # final resource frame for the last 21 frames of the source span.
    resource_video_in = LIVE_RESOURCE_V2_IN if args.revision_v2 else LIVE_RESOURCE_IN
    resource_video_out = LIVE_RESOURCE_V2_OUT if args.revision_v2 else LIVE_RESOURCE_OUT
    build.keep(
        RESOURCE_IN,
        RESOURCE_OUT,
        "Live-video diagram: CyberTipline and NCMEC visible at narration onset (covers displayed URL)",
        video_from=resource_video_in,
        video_src=LIVE,
        video_end=resource_video_out,
    )
    build.keep(RESOURCE_OUT, SAFETY_TO_MOVE, "Notebook drawing: Take It Down and no-fault reassurance")

    # Move candidate 2's own two-sentence lie-detector conclusion before the
    # hard close.  This is a same-voice, whole-beat move beginning and ending on
    # source scene cuts; no narration follows the hard close afterward.
    build.graft(
        SRC,
        EYES_IN,
        EYES_OUT,
        "Moved same-file conclusion: eyes are not a lie detector",
        "moved-eyes-conclusion",
        cover_intro=False,
        gain_db=0.0,
    )

    build.mark_close_start()
    build.close(SAFETY_TO_MOVE, RAW_CLOSE_OUT, tail=120)
    build.finish_audio()

    # Board 1 (1600x1470): full view, then each complete comparison card, then
    # return to the full board for the source-trail takeaway.
    before_ai = [40, 271, 784, 1302]
    ai_era = [816, 271, 1560, 1302]
    comparison_banner = [40, 1342, 1560, 1430]
    if not args.revision_v2:
        build.board(
            "comparison",
            COMPARISON,
            COMPARE_IN,
            COMPARE_OUT,
            "dense",
            [
                target("Before AI: Does It Look Real?", 16.46, before_ai, AMBER, before_ai),
                target("The AI Era: Where Is It From?", 24.88, ai_era, BLUE, ai_era),
                target("Appearance can mislead; check the source trail", 27.10, comparison_banner, NEUTRAL, full_view=True),
            ],
            per_target_camera=True,
            lead_camera=True,
        )

    # Board 2 (1329x1183): the takeaway is spoken before the four-item donor
    # list, so its banner rings at that spoken onset while the board remains at
    # full view.  Each donor item then gets a complete-card zoom and ring.
    money = [35, 105, 652, 565]
    power = [678, 105, 1294, 565]
    fame = [35, 591, 652, 1051]
    cruelty = [678, 591, 1294, 1051]
    reasons_banner = [35, 1086, 1294, 1158]
    build.board(
        "reasons",
        REASONS,
        REASONS_IN,
        MOTIVES_VIRTUAL_END,
        "dense",
        [
            target("Harmful fakes are made to get something back", 68.42, reasons_banner, NEUTRAL, full_view=True),
            target("Money", donor_onset(86.92), money, PURPLE, money),
            target("Power", donor_onset(93.56), power, BLUE, power),
            target("Fame", donor_onset(101.54), fame, AMBER, fame),
            target("Cruelty", donor_onset(110.02), cruelty, RED, cruelty),
        ],
        per_target_camera=True,
        lead_camera=True,
    )

    # Board 3 is one whole-board idea; it remains complete and unmarked.
    build.board(
        "follow-source",
        SOURCE,
        SOURCE_IN,
        SOURCE_OUT,
        "compact",
        [],
        push=False,
    )

    # Board 4 is legible at full 720p view.  Ring the complete cards at their
    # spoken onsets and return to the takeaway banner for the one-rule line.
    source_card = [40, 127, 525, 651]
    context_card = [557, 127, 1043, 651]
    corroboration_card = [1075, 127, 1560, 651]
    checks_banner = [40, 691, 1560, 779]
    build.board(
        "checks",
        CHECKS,
        CHECKS_IN,
        CHECKS_OUT,
        "compact",
        [
            target("Source", 137.94, source_card, PURPLE),
            target("Context", 141.76, context_card, BLUE),
            target("Corroboration", 145.60, corroboration_card, TEAL),
        ],
        banner_at=178.66,
        banner=checks_banner,
        push=False,
    )

    if not args.render_existing:
        build.render_legs()
        for key in build.boards:
            build.state_sheet(key)

    build.make_close("faketrap")
    build.manifest({
        "scope_detail": (
            "Revision 2 uses the live video's complete opening through the harmless-joke conclusion and aligns the CyberTipline visual with its spoken mention. index.html is excluded from the render-integrity set because an unrelated Where's the Line lesson edit was active concurrently; all video inputs, board assets, and fake-trap.md remain protected."
            if args.revision_v2 else
            "Full production review candidate from the user-approved Fake-trap-2 best-of plan; live video and lesson unchanged."
        ),
        "narration_changes": {
            "candidate1_motives_donor_frames": list(MOTIVES_DONOR),
            "candidate2_thin_motives_removed_frames": [REASONS_INTRO_OUT, THIN_REASONS_OUT],
            "candidate2_unsupported_detector_sentence_removed_frames": [WRONG_SENTENCE_IN, WRONG_SENTENCE_OUT],
            "candidate2_conclusion_moved_frames": [EYES_IN, EYES_OUT],
            "candidate2_close_frames": [SAFETY_TO_MOVE, RAW_CLOSE_OUT],
            "donor_gain_db": MOTIVES_GAIN_DB,
            "live_opening_donor_frames": [0, LIVE_OPENING_OUT] if args.revision_v2 else None,
            "live_opening_gain_db": LIVE_OPENING_GAIN_DB if args.revision_v2 else None,
        },
        "added_teaching_pauses": [],
        "photographs_replaced": ([
            {
                "candidate2_frames": [0, PHOTO_OUT],
                "replacement": "Live-video opening through the complete harmless-joke conclusion",
                "replacement_frames": [0, LIVE_OPENING_OUT],
            },
        ] if args.revision_v2 else [
            {
                "candidate2_frames": [PHOTO_IN, PHOTO_OUT],
                "replacement": "Candidate-1 harmless-hockey-joke drawing",
                "replacement_start_frame": HOCKEY_DRAWING_IN,
            },
        ]),
        "displayed_urls_replaced": [
            {
                "candidate2_frames": [RESOURCE_IN, RESOURCE_OUT],
                "replacement": "Live-video URL-free report/NCMEC diagram with CyberTipline visible at narration onset",
                "replacement_frames": [resource_video_in, resource_video_out],
            },
        ],
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round((CHECKS_OUT - SOURCE_IN) / 30, 2),
    })

    print(
        "Prepared",
        build.total,
        f"frames ({build.total / 30:.2f}s)",
        "motives graft",
        MOTIVES_LEN,
        "frames",
        flush=True,
    )
    if args.prepare_only:
        return
    build.render()
    print(dest)


if __name__ == "__main__":
    main()
