#!/usr/bin/env python3
"""Build Flattery Trap v3 from flattery-trap-4 (2026-09-21 five-way review: rolls 1-4 and the live video).

Full production pass, review only. Roll 4 carries the whole narration with no cuts; one approved
audio-only graft from roll 2 supplies "But while the problem has improved, it has not disappeared.",
the clause every other roll drops. Roll 4 is the only roll that keeps the prompt's RLHF qualification
and speaks the standing instruction word for word. The post-only comparison board walks the Gatsby
scenario; canonical Boards 2, 3 and 4 replace Notebook's renders with rings; standard close.
Live video, raw rolls, lesson, and boards unchanged.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, PURPLE, BLUE, TEAL, AMBER, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/flattery-trap-4.mp4"
DONOR = ROOT / "Prompts/flattery-trap-2.mp4"
OUT = ROOT / "video-audit/flattery-trap-comparison-2026-09-21/build-v3"
DEST = ROOT / "Prompts/flattery-trap-v3.mp4"
A = ROOT / "course-assets/flattery-trap"
COMPARE, CYCLE, SYCO, MOVES, CLOSE = (A / f"flattery-trap-{n}.jpg" for n in
                                      ("comparison", "cycle-of-praise", "sycophancy", "five-moves", "close"))
LIVE, LESSON = A / "flattery-trap.mp4", ROOT / "lessons/flattery-trap.md"
OTHER_ROLLS = [ROOT / f"Prompts/flattery-trap-{i}.mp4" for i in (1, 2, 3)]

# Every row boundary below sits inside a measured silence (ffmpeg silencedetect, -40 dB / 0.18 s).
CMP_IN, CMP_OUT = 690, 2487        # 0:23.00 (quiet 22.79-23.24, before "Let's look at a concrete example")
CYCLE_IN, CYCLE_OUT = 2487, 3385   # 1:22.90 (quiet 82.48-83.19); out 1:52.83 (quiet 112.66-113.12)
SYCO_IN, SYCO_OUT = 4000, 4317     # 2:13.33 (quiet 133.16-133.51); out 2:23.90 (quiet 143.68-144.08)
SYCO_PICTURE_RESUME = 4333         # roll 4 holds Notebook's Sycophancy render to its own cut at 2:24.43
GRAFT_AT = 4717                    # 2:37.23, inside the quiet 157.12-157.51 after "…many different AI assistants"
G_IN, G_OUT = 4537, 4650           # roll 2, 2:31.23-2:35.00; v3 widened into its own pauses (151.045-151.535 and 154.755-155.271) so the 5 ms row crossfade never touches "But" or "disappeared."
G_PICTURE = 4733                   # the graft carries roll 4's own drawn devices scene forward, unbroken
MOVES_IN, MOVES_OUT = 4970, 8168   # 2:45.67 (quiet 165.42-165.82); out 4:32.27 (quiet 272.05-272.49)
MOVES2_IN, MOVES2_OUT = 8378, 8894 # 4:39.27 (quiet 278.98-279.47); out 4:56.47 (quiet 296.28-296.70)
MOVES3_IN = 9265                   # 5:08.83 (quiet 308.41-309.01)
CLOSE_IN = 9475                    # 5:15.83, inside the quiet 315.74-316.17 before "Useful feedback points…"
CLOSE_AUDIO_OUT = 9618             # 5:20.60, after "not approval." (320.24); engine outro cut at 5:20.97
DRAWN_END = 4975                   # the last roll-4 frame before its Five Ways render begins
# v2: three more of roll 4's own board renders run a few frames past the pause the audio cuts in, so each
# resumed picture starts at the roll's own cut and leads its audio by 4-5 frames (transition_guard caught v1).
CYCLE_PICTURE_RESUME, CYCLE_PICTURE_END = 3390, 4007
MOVES_PICTURE_RESUME, MOVES_PICTURE_END = 8172, 8383
MOVES2_PICTURE_RESUME, MOVES2_PICTURE_END = 8899, 9272

# Board geometry, measured from the assets.
CMP_SCENARIO = [40, 112, 1560, 351]
CMP_L, CMP_R = [40, 383, 790, 1427], [816, 383, 1564, 1427]
ROW = lambda card, y0, y1: [card[0] + 16, y0, card[2] - 16, y1]
PRAISED, MIDDLE, RESULT = (1057, 1148), (1176, 1267), (1295, 1385)
CMP_BANNER = [40, 1454, 1560, 1542]
CYCLE_COLS = ([67, 127, 393, 711], [605, 127, 992, 711], [1207, 127, 1533, 711])   # full white-box height
SYCO_PARA1 = [57, 232, 1543, 402]
MOVE_ROW = lambda y0, y1: [56, y0, 1544, y1]                                        # 16 px inside the white box
MOVES_BANNER = [40, 1190, 1560, 1278]

def target(label, at, rect, color, radius=14):
    return {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true"); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, COMPARE, CYCLE, SYCO, MOVES, CLOSE, LESSON, *OTHER_ROLLS])
    b.load_audio([(4.85, 5.40), (12.96, 13.32), (22.79, 23.24), (28.48, 28.90), (38.07, 38.74), (44.87, 45.51),
                  (53.21, 53.67), (62.39, 62.93), (70.19, 70.63), (76.35, 77.00), (82.48, 83.19), (92.06, 92.52),
                  (98.62, 99.03), (103.70, 104.11), (112.66, 113.12), (119.97, 120.41), (133.16, 133.51),
                  (137.94, 138.41), (143.68, 144.08), (149.79, 150.22), (157.12, 157.51), (165.42, 165.82),
                  (175.64, 176.10), (196.26, 197.03), (215.56, 216.47), (230.96, 231.55), (243.59, 244.43),
                  (258.90, 259.49), (272.05, 272.49), (278.98, 279.47), (288.44, 288.90), (296.28, 296.70),
                  (303.35, 303.90), (308.41, 309.01), (312.18, 312.49), (315.74, 316.17), (318.06, 318.50)])

    b.keep(0, CMP_IN, "Notebook drawings: the student at the laptop, the marked-up essay, the trap definition")
    b.keep(CMP_IN, CMP_OUT, "Flattery vs. Useful Feedback", "compare")
    b.keep(CYCLE_IN, CYCLE_OUT, "How the Praise Got Baked In", "cycle")
    b.keep(CYCLE_OUT, SYCO_IN, "Notebook drawings: the artificial-praise card, April 2025, the gag product",
           video_from=CYCLE_PICTURE_RESUME, video_end=CYCLE_PICTURE_END)
    b.keep(SYCO_IN, SYCO_OUT, "Sycophancy", "syco")
    b.keep(SYCO_OUT, GRAFT_AT, "Notebook drawings: update rolled back, the three devices",
           video_from=SYCO_PICTURE_RESUME, video_end=DRAWN_END)
    b.graft(DONOR, G_IN, G_OUT, "The problem has improved but has not disappeared (roll 2)", "improved",
            picture_from=G_PICTURE, video_end=DRAWN_END, gain_db=-0.9)
    b.keep(GRAFT_AT, MOVES_IN, "Notebook drawings: the training-model map, the speech bubble",
           video_from=G_PICTURE + (G_OUT - G_IN), video_end=DRAWN_END)
    b.keep(MOVES_IN, MOVES_OUT, "Five Ways to Fight the Flattery Trap", "moves")
    b.keep(MOVES_OUT, MOVES2_IN, "Notebook drawing: the crossed-out thumbs-up",
           video_from=MOVES_PICTURE_RESUME, video_end=MOVES_PICTURE_END)
    b.keep(MOVES2_IN, MOVES2_OUT, "Five Ways to Fight the Flattery Trap (the fifth move)", "moves2")
    b.keep(MOVES2_OUT, MOVES3_IN, "Notebook drawing: the standing-instruction diagram and its limit",
           video_from=MOVES2_PICTURE_RESUME, video_end=MOVES2_PICTURE_END)
    b.keep(MOVES3_IN, CLOSE_IN, "Five Ways to Fight the Flattery Trap (the takeaway)", "moves3")
    b.mark_close_start()
    b.close(CLOSE_IN, CLOSE_AUDIO_OUT, tail=150)
    b.finish_audio()

    # Board 1 (1600x1582, faces, post-only): compact - every line reads at full view, and each card is
    # taller than a 16:9 dive can hold, so the camera stays still and the rings follow the spoken sections.
    b.board("compare", COMPARE, CMP_IN, CMP_OUT, "compact", [
        target("The scenario: the Gatsby intro", 28.90, CMP_SCENARIO, NEUTRAL, radius=18),
        target("Flattery (whole card)", 38.74, CMP_L, AMBER, radius=20),
        target("Flattery / Praised: the work without pointing to evidence", 45.51, ROW(CMP_L, *PRAISED), AMBER),
        target("Flattery / Could fit: almost any Gatsby essay", 50.51, ROW(CMP_L, *MIDDLE), AMBER),
        target("Useful Feedback (whole card)", 53.67, CMP_R, BLUE, radius=20),
        target("Useful / Named: the missing thesis", 64.35, ROW(CMP_R, *MIDDLE), BLUE),
        target("Useful / Result: a specific next move", 67.78, ROW(CMP_R, *RESULT), BLUE),
    ], banner_at=70.63, banner=CMP_BANNER, push=False)

    # Board 2 (1600x751, three columns inside one shared white box): rings run the box's full height.
    b.board("cycle", CYCLE, CYCLE_IN, CYCLE_OUT, "compact", [
        target("People Rank", 92.52, list(CYCLE_COLS[0]), PURPLE, radius=18),
        target("Agreement Can Win", 99.03, list(CYCLE_COLS[1]), BLUE, radius=18),
        target("Numbers Move", 104.11, list(CYCLE_COLS[2]), TEAL, radius=18),
    ], push=False)

    # Board 3 (1600x667, one card holding the quotation): the narrator reads a short excerpt of the
    # first paragraph, so that paragraph is ringed and the second is left alone.
    b.board("syco", SYCO, SYCO_IN, SYCO_OUT, "compact", [
        target("ChatGPT's response, first paragraph", 138.41, SYCO_PARA1, PURPLE, radius=12),
    ], push=False)

    # Board 4 (1600x1318, five stacked rows inside one white box): compact; each row rings as its move is named.
    b.board("moves", MOVES, MOVES_IN, MOVES_OUT, "compact", [
        target("01 Ask, Don't Tell", 176.10, MOVE_ROW(143, 309), NEUTRAL),
        target("02 Ask for the Gaps", 197.03, MOVE_ROW(325, 528), NEUTRAL),
        target("03 Use a Rubric", 216.47, MOVE_ROW(544, 747), NEUTRAL),
        target("04 Argue the Other Side", 244.43, MOVE_ROW(763, 966), NEUTRAL),
    ], push=False)
    b.board("moves2", MOVES, MOVES2_IN, MOVES2_OUT, "compact", [
        target("05 Set a Standing Instruction", 279.47, MOVE_ROW(982, 1134), NEUTRAL),
    ], push=False, min_open=0)   # the board returns on the move-5 line itself: the ring pops in the full view (spec rule 3)
    b.board("moves3", MOVES, MOVES3_IN, CLOSE_IN, "compact", [], banner_at=312.49, banner=MOVES_BANNER, push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("flattery")
    b.manifest({
        "scope_detail": "Full production review candidate from the 2026-09-21 five-way review (roll 4 base, one approved roll-2 graft); live video, raw rolls, lesson, and boards unchanged.",
        "narration_changes": {
            "graft": "roll 2 2:31.53-2:34.77 ('But while the problem has improved, it has not disappeared.') inserted at 2:37.23; audio only, no roll-4 words removed",
            "graft_gain_db": -0.9,
            "engine_outro_removed_from_frame": CLOSE_AUDIO_OUT,
        },
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"frames": [CYCLE_IN, CYCLE_OUT], "replacement": "canonical How the Praise Got Baked In"},
            {"frames": [SYCO_IN, SYCO_PICTURE_RESUME], "replacement": "canonical Sycophancy"},
            {"frames": [MOVES_IN, MOVES_OUT], "replacement": "canonical Five Ways to Fight the Flattery Trap"},
            {"frames": [MOVES2_IN, MOVES2_OUT], "replacement": "canonical Five Ways (the fifth move)"},
            {"frames": [MOVES3_IN, CLOSE_IN], "replacement": "canonical Five Ways (the takeaway banner)"},
            {"frames": [CLOSE_IN, CLOSE_AUDIO_OUT], "replacement": "standard close"},
        ],
        "post_only_board_inserted": {
            "asset": "course-assets/flattery-trap/flattery-trap-comparison.jpg",
            "frames": [CMP_IN, CMP_OUT],
            "over": "Notebook's own typographic recreation of the Gatsby comparison",
        },
        "picture_advance": {
            "rows": "four rows: 1:52.83-2:13.33, 2:23.90-2:45.67, 4:32.27-4:39.27 and 4:56.47-5:08.83",
            "detail": ("roll 4 holds each of its own board renders a few frames past the pause the audio cuts in. "
                       "The Sycophancy case is the largest: the render runs to frame 4333 while the next "
                       "sentence starts at 144.08, so the audio boundary is placed in the pause at 4317 and the "
                       "drawn picture resumes at 4333. The audio-only graft then carries that drawn scene forward "
                       "unbroken (4733-4830), and the last 108 frames of the following row hold frame 4974, a "
                       "static speech-bubble card, to absorb the graft's 97 added frames."),
        },
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round((MOVES_OUT - MOVES_IN) / FPS, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
