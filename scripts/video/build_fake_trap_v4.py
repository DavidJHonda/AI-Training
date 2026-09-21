#!/usr/bin/env python3
"""Build the Fake Trap v4 review candidate from the 2026-09-20 materials-test rolls.

Full production pass, review only.  fake-trap-new-2 is the spine (single voice,
complete coverage, verbatim close).  fake-trap-new-1 supplies the complete
four-motive beat under the canonical reasons board (approved best-of plan,
video-audit/fake-trap-materials-test-2026-09-20/REVIEW.md) and four drawings
that cover roll 2's photo-real paper-craft scenes (Edit Spec 8c).  The two
faceless upload boards and the close board Notebook showed mid-video are
replaced by the canonical page boards.  No narration pause is added: every
proposed pause point already carries a 0.6-0.8 s natural gap.  The live video,
both raw rolls, the lesson, and the boards remain unchanged.
"""

from pathlib import Path
import argparse
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, AMBER, RED, NEUTRAL


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/fake-trap-new-2.mp4"
DONOR = ROOT / "Prompts/fake-trap-new-1.mp4"
OUT = ROOT / "video-audit/fake-trap-materials-test-2026-09-20/build-v4"
DEST = ROOT / "Prompts/fake-trap-v4.mp4"
# Revision 5 (owner request 2026-09-20 after viewing v4): Board 1 rings its individual
# sections as they are spoken instead of whole cards.  Everything else is identical to v4.
OUT_V5 = ROOT / "video-audit/fake-trap-materials-test-2026-09-20/build-v5"
DEST_V5 = ROOT / "Prompts/fake-trap-v5.mp4"

COMPARISON = ROOT / "course-assets/fake-trap/fake-trap-comparison.jpg"
REASONS = ROOT / "course-assets/fake-trap/fake-trap-reasons.jpg"
SOURCE = ROOT / "course-assets/fake-trap/fake-trap-follow-the-source.jpg"
CHECKS = ROOT / "course-assets/fake-trap/fake-trap-checks.jpg"
CLOSE = ROOT / "course-assets/fake-trap/fake-trap-close.jpg"
LESSON = ROOT / "lessons/fake-trap.md"
LIVE = ROOT / "course-assets/fake-trap/fake-trap.mp4"

# Roll-2 visual cuts (scenes.txt, sequential decode) and audio boundaries
# (10 ms RMS scan; every audio cut sits inside a measured quiet window).
COMPARE_IN = 804            # 0:26.80 cut into the faceless comparison board; "This chart" 26.76
COMPARE_OUT = 2037          # 1:07.90 quiet after "checked." (67.42) before "The fake trap" (68.22)
BENCH_IN = 2316             # 1:17.20 cut from the board render to the bench drawing
CUP_PHOTO_IN, CUP_PHOTO_OUT = 2381, 2496        # 1:19.37-1:23.20 photo-real Stanley Cup on a notebook (bench drawing on either side)
REASONS_IN = 2830           # 1:34.33 cut into the reasons board; "This graphic" 94.42
REASONS_INTRO_OUT = 2931    # 1:37.70 quiet after "fakes." (97.42), before the breath for "First" (98.02)
THIN_LIST_OUT = 3390        # 1:53.00 cut to the detector drawing; "If you suspect" onset 113.12
SOURCE_IN, SOURCE_OUT = 4036, 4327              # 2:14.53-2:24.23 Notebook showed the close board here
CHECKS_IN, CHECKS_OUT = 4655, 5599              # 2:35.17-3:06.63 Notebook's checks-board render
FOLDER_PHOTO_IN, FOLDER_PHOTO_OUT = 6648, 6802  # 3:41.60-3:46.73 photo-real folder
CONTACTS_PHOTO_IN, CONTACTS_PHOTO_OUT = 7216, 7365  # 4:00.53-4:05.50 photo-real phone contacts
SHIELD_PHOTO_IN, SHIELD_PHOTO_OUT = 8558, 8817  # 4:45.27-4:53.90 photo-real shield / NCMEC
CLOSE_AUDIO_IN = 8879       # 4:55.97 quiet after "targeted." (295.74), before "Seeing" (296.32)
CLOSE_AUDIO_OUT = 9033      # 5:01.10 after "pixels." (301.00); the engine outro is digital silence from 301.14

# Roll-1 donor audio: quiet before "Money" (86.56) through quiet after "school." (103.98).
MOTIVES_DONOR = (2589, 3135)                    # 1:26.30-1:44.50
MOTIVES_GAIN_DB = 0.0                           # speech RMS roll 1 -16.18 dBFS, roll 2 -16.20 dBFS

# Roll-1 drawings borrowed under roll-2 narration (increasing order in roll 1).
JAW_DRAWING = (1860, 2104)      # 1:02.00-1:10.13 "1st Jaw / 2nd Jaw" diagram (settled by 1:02; scene fades in from 1:00.47)
CUP_DRAWING = (2104, 2258)      # 1:10.13-1:15.27 three friends with the Stanley Cup, backs turned
UNVERIFIED_DRAWING = (5227, 5361)   # 2:54.23-2:58.70 question mark and magnifier
CONTACTS_DRAWING = (5760, 5875)     # 3:12.00-3:15.83 "urgent audio and calls" cards; the drawing fades to blank from 3:15.9, so the settled two-card frame holds for the last 34 frames
PROTOCOL_DRAWING = (6900, 7005)     # 3:50.00-3:53.50 trusted adult / platform report / Take It Down (settled by 3:50; fades in from 3:47)

MOTIVES_LEN = MOTIVES_DONOR[1] - MOTIVES_DONOR[0]
REASONS_VIRTUAL_END = REASONS_INTRO_OUT + MOTIVES_LEN


def donor_onset(seconds: float) -> float:
    """Map a roll-1 word onset onto the reasons-board leg's synthetic clock."""
    return (REASONS_INTRO_OUT + (fr(seconds) - MOTIVES_DONOR[0])) / 30.0


def target(label, at, rect, color, cam=None, *, full_view=False):
    item = {"label": label, "at": at, "rects": [rect], "color": color, "radius": 18}
    if cam is not None:
        item["cam"] = cam
    if full_view:
        item["full_view"] = True
    return item


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--render-existing", action="store_true", help="reuse legs from a prepare-only pass")
    parser.add_argument("--revision-v5", action="store_true", help="Board 1 section-level rings (owner request 2026-09-20)")
    args = parser.parse_args()

    out = OUT_V5 if args.revision_v5 else OUT
    dest = DEST_V5 if args.revision_v5 else DEST
    build = Build(ROOT, SRC, out, dest, protected=[DONOR, LIVE, COMPARISON, REASONS, SOURCE, CHECKS, CLOSE, LESSON])
    build.load_audio([
        (3.02, 3.28), (7.90, 8.55), (12.90, 13.50), (17.89, 18.74), (26.04, 26.86), (40.10, 40.66),
        (45.06, 45.82), (50.67, 51.35), (63.81, 64.34), (67.50, 68.22), (76.47, 77.26), (89.48, 90.17),
        (97.43, 98.03), (112.49, 113.13), (119.66, 120.21), (134.22, 134.63), (143.98, 144.34),
        (154.79, 155.18), (177.30, 177.91), (186.08, 186.55), (208.13, 208.59), (233.01, 233.49),
        (253.77, 254.32), (262.79, 263.32), (288.68, 289.26), (295.83, 296.32),
    ])

    # Opening drawings, then the comparison board at its spoken introduction.
    build.keep(0, COMPARE_IN, "Notebook drawings: fakes are cheap; knowing is not a skill; the clip arrives")
    build.keep(COMPARE_IN, COMPARE_OUT, "The Same Clip. Two Eras.", "comparison")
    # Roll 2 held its board render under the definition and second jaw; roll 1 drew the two jaws for the same lines.
    build.keep(COMPARE_OUT, BENCH_IN, "Roll-1 drawing: the two jaws of the Fake Trap (covers roll 2's board render)",
               video_from=JAW_DRAWING[0], video_src=DONOR, video_end=JAW_DRAWING[1])
    build.keep(BENCH_IN, CUP_PHOTO_IN, "Notebook drawing: friends on a bench, a fake that is just a joke")
    build.keep(CUP_PHOTO_IN, CUP_PHOTO_OUT, "Roll-1 drawing: friends with the Stanley Cup (covers photo-real cup)",
               video_from=CUP_DRAWING[0], video_src=DONOR, video_end=CUP_DRAWING[1])
    build.keep(CUP_PHOTO_OUT, REASONS_IN, "Notebook drawings: everyone in on the joke; the trap begins with intent to deceive")

    # Roll 2 introduces the reasons board; roll 1 teaches all four motives under it.
    build.keep(REASONS_IN, REASONS_INTRO_OUT, "Why Some Fakes Aren't Friendly: introduction", "reasons")
    build.graft(DONOR, MOTIVES_DONOR[0], MOTIVES_DONOR[1],
                "Roll-1 audio: money, power, fame, and cruelty in the lesson's words",
                "roll1-motives", picture_from=REASONS_INTRO_OUT, gain_db=MOTIVES_GAIN_DB, visual="reasons")

    build.keep(THIN_LIST_OUT, SOURCE_IN, "Notebook drawings: detector dead end")
    build.keep(SOURCE_IN, SOURCE_OUT, "Check the Source, Not the Pixels", "follow-source")
    build.keep(SOURCE_OUT, CHECKS_IN, "Notebook drawing: emotions spike, stop")
    build.keep(CHECKS_IN, CHECKS_OUT, "Move the Test Off the Image", "checks")
    build.keep(CHECKS_OUT, FOLDER_PHOTO_IN, "Notebook drawings: the three checks applied to the school clip")
    build.keep(FOLDER_PHOTO_IN, FOLDER_PHOTO_OUT, "Roll-1 drawing: unverified question mark (covers photo-real folder)",
               video_from=UNVERIFIED_DRAWING[0], video_src=DONOR, video_end=UNVERIFIED_DRAWING[1])
    build.keep(FOLDER_PHOTO_OUT, CONTACTS_PHOTO_IN, "Notebook drawings: unverified protects you; the one rule")
    build.keep(CONTACTS_PHOTO_IN, CONTACTS_PHOTO_OUT, "Roll-1 drawing: urgent voicemail, call the saved number (covers photo-real contacts)",
               video_from=CONTACTS_DRAWING[0], video_src=DONOR, video_end=CONTACTS_DRAWING[1])
    build.keep(CONTACTS_PHOTO_OUT, SHIELD_PHOTO_IN, "Notebook drawings: viral clip, eyes, if the fake is about you, under-18 rule")
    build.keep(SHIELD_PHOTO_IN, SHIELD_PHOTO_OUT, "Roll-1 drawing: trusted adult, platform report, Take It Down (covers photo-real shield)",
               video_from=PROTOCOL_DRAWING[0], video_src=DONOR, video_end=PROTOCOL_DRAWING[1])
    build.keep(SHIELD_PHOTO_OUT, CLOSE_AUDIO_IN, "Notebook drawing: you did nothing wrong")

    build.mark_close_start()
    build.close(CLOSE_AUDIO_IN, CLOSE_AUDIO_OUT, tail=120)
    build.finish_audio()

    # Board 1 (1600x1470), dense: full view for the introduction, complete-card dive on each
    # era at its spoken onset, back to the full board for the banner line.
    before_ai = [40, 271, 784, 1302]
    ai_era = [816, 271, 1560, 1302]
    comparison_banner = [40, 1342, 1560, 1430]
    if args.revision_v5:
        # Section rings inside each card, sharing the card's rails 16 px inside its edge.  Text
        # bands measured on the JPG: label 729-743, title 773-802, body 836-904, first row
        # 955-1019, second row 1074-1144, verdict 1193-1257.  Camera holds the complete card.
        def sections(x0, x1):
            return {
                "title": [x0, 717, x1, 814],      # era label + question
                "body": [x0, 824, x1, 916],
                "row1": [x0, 943, x1, 1031],      # CHECKED / SKIPPED
                "row2": [x0, 1062, x1, 1156],     # MATCHED / CHECKED
                "verdict": [x0, 1181, x1, 1269],
            }
        b = sections(56, 768)
        a = sections(832, 1544)
        combined = {"label": "Face, voice, hallway (body + Checked)", "at": 35.60, "rects": [b["body"], b["row1"]],
                    "color": AMBER, "colors": [AMBER, AMBER], "radius": 18, "cam": before_ai}
        ai_title = target("Where Is It From?", 48.62, a["title"], BLUE, ai_era)
        ai_title["camera_at"] = 45.74            # camera arrives on "In the AI era"; the ring waits for the question
        build.board("comparison", COMPARISON, COMPARE_IN, COMPARE_OUT, "dense", [
            target("Does It Look Real?", 30.94, b["title"], AMBER, before_ai),
            combined,
            target("Matched: how the principal talks", 40.56, b["row2"], AMBER, before_ai),
            target("Verdict: Real", 42.58, b["verdict"], AMBER, before_ai),
            ai_title,
            target("Ignore the pixels, check the trail", 51.24, a["body"], BLUE, ai_era),
            target("Skipped: face and voice", 54.38, a["row1"], BLUE, ai_era),
            target("Checked: the source that would know", 56.76, a["row2"], BLUE, ai_era),
            target("Nothing appears on the school website", 59.38, a["body"], BLUE, ai_era),
            target("Verdict: Unverified", 62.22, a["verdict"], BLUE, ai_era),
            target("Appearance can mislead; the source trail can be checked", 64.78, comparison_banner, NEUTRAL, full_view=True),
        ], per_target_camera=True, lead_camera=True)
    else:
        build.board("comparison", COMPARISON, COMPARE_IN, COMPARE_OUT, "dense", [
            target("Before AI: Does It Look Real?", 30.94, before_ai, AMBER, before_ai),
            target("The AI Era: Where Is It From?", 45.74, ai_era, BLUE, ai_era),
            target("Appearance can mislead; the source trail can be checked", 64.78, comparison_banner, NEUTRAL, full_view=True),
        ], per_target_camera=True, lead_camera=True)

    # Board 2 (1329x1183), dense: roll 2's introduction at full view, then each motive card
    # dives and rings at roll 1's spoken onset.  The banner is not spoken verbatim by either
    # roll and stays unringed (owner decision 2026-09-20).
    money = [35, 105, 652, 565]
    power = [678, 105, 1294, 565]
    fame = [35, 591, 652, 1051]
    cruelty = [678, 591, 1294, 1051]
    build.board("reasons", REASONS, REASONS_IN, REASONS_VIRTUAL_END, "dense", [
        target("Money", donor_onset(86.56), money, PURPLE, money),
        target("Power", donor_onset(90.23), power, BLUE, power),
        target("Fame", donor_onset(94.55), fame, AMBER, fame),
        target("Cruelty", donor_onset(98.89), cruelty, RED, cruelty),
    ], per_target_camera=True, lead_camera=True)

    # Board 3 (1387x1134), compact: one idea; the banner rings when its line is spoken.
    source_banner = [36, 1023, 1351, 1098]
    build.board("follow-source", SOURCE, SOURCE_IN, SOURCE_OUT, "compact", [],
                banner_at=140.14, banner=source_banner, push=False)

    # Board 4 (1600x819), compact: the three cards ring at their names.
    source_card = [40, 127, 525, 651]
    context_card = [557, 127, 1043, 651]
    corroboration_card = [1075, 127, 1560, 651]
    build.board("checks", CHECKS, CHECKS_IN, CHECKS_OUT, "compact", [
        target("Source", 157.74, source_card, PURPLE),
        target("Context", 163.36, context_card, BLUE),
        target("Corroboration", 171.12, corroboration_card, TEAL),
    ], push=False)

    if not args.render_existing:
        build.render_legs()
        for key in build.boards:
            build.state_sheet(key)

    build.make_close("faketrap")
    build.manifest({
        "scope_detail": "Full production review candidate from the approved 2026-09-20 materials-test best-of plan (roll 2 base, roll 1 motives); live video, raw rolls, lesson, and boards unchanged.",
        "narration_changes": {
            "roll1_motives_donor_frames": list(MOTIVES_DONOR),
            "roll2_thin_motives_removed_frames": [REASONS_INTRO_OUT, THIN_LIST_OUT],
            "roll2_engine_outro_removed_from_frame": CLOSE_AUDIO_OUT,
            "donor_gain_db": MOTIVES_GAIN_DB,
        },
        "added_teaching_pauses": [],
        "natural_gaps_at_proposed_pause_points_seconds": {
            "1:08 banner to definition": 0.80, "1:53 graft seam": 0.62, "2:24 board 3 to emotions": 0.70, "4:23 eyes to safety": 0.62,
        },
        "photographs_replaced": [
            {"roll2_frames": [CUP_PHOTO_IN, CUP_PHOTO_OUT], "replacement": "roll 1 Stanley Cup drawing", "replacement_frames": list(CUP_DRAWING)},
            {"roll2_frames": [FOLDER_PHOTO_IN, FOLDER_PHOTO_OUT], "replacement": "roll 1 unverified question-mark drawing", "replacement_frames": list(UNVERIFIED_DRAWING)},
            {"roll2_frames": [CONTACTS_PHOTO_IN, CONTACTS_PHOTO_OUT], "replacement": "roll 1 urgent-call cards", "replacement_frames": list(CONTACTS_DRAWING)},
            {"roll2_frames": [SHIELD_PHOTO_IN, SHIELD_PHOTO_OUT], "replacement": "roll 1 support protocol drawing", "replacement_frames": list(PROTOCOL_DRAWING)},
        ],
        "board_render_covered": [
            {"roll2_frames": [COMPARE_OUT, CUP_PHOTO_IN], "replacement": "roll 1 two-jaws drawing", "replacement_frames": list(JAW_DRAWING)},
            {"roll2_frames": [SOURCE_IN, SOURCE_OUT], "replacement": "canonical Board 3 (Notebook showed the close board)"},
        ],
        "notebook_interleaves": ["two-jaws drawing between Board 1 and the Stanley Cup scene"],
        "longest_unbroken_board_run_seconds": round((COMPARE_OUT - COMPARE_IN) / 30, 2),
    })

    print("Prepared", build.total, f"frames ({build.total / 30:.2f}s)", "motives graft", MOTIVES_LEN, "frames", flush=True)
    if args.prepare_only:
        return
    build.render()
    print(dest)


if __name__ == "__main__":
    main()
