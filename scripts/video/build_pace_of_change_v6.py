#!/usr/bin/env python3
"""Pace of Change v6 review candidate: v5 with the race beat re-pictured from the 2026-09-24 rerolls. Review only.

David 2026-09-23 on v5: "From 1:23 to 2:12, the Gemini Notebook graphics are disappointing ... use this video as the base and
reroll to get more engaging graphics for that part." Rolls 3 and 4 (2026-09-24) were rolled as picture donors; review in
video-audit/pace-of-change-rerolls-2026-09-24/REVIEW.md. David approved the proposed v6 ("yes", 2026-09-24), MOMENTUM and the
hand-at-keyboard included. Audio is v5's exactly (roll 1, cut 1 and phrase cut 5'); only pictures change:
  race beat (roll 1 source 92.30-142.43): roll 4 robot arm, roll 4 stopwatch, roll 3 MOMENTUM, roll 2 error-to-check phone
  (kept from v5, moved under today's-"no"), roll 4 circuit sketch. Out: roll 1's two phones, roll 2's check/X, roll 1's
  checklist and red X.
  Board 2: roll 4's hand at a keyboard (neural net on screen) under "The strongest current models are actively helping humans
  write code for the next generation of models." (a second break after the data-center aisle).
Each donor span was checked frame by frame: hard cuts at both ends, no fade frames inside. Picture changes are cut at the
sentence silences (roll 1 base.en word stamps). Live assets, all rolls, lesson, boards, index.html unchanged.
"""
from pathlib import Path
import argparse, json, subprocess, sys
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, rms, readwav, writewav, FPS, W, H, SR, SPF, NEUTRAL, PURPLE, BLUE, TEAL, GREEN, AMBER, RED

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC = P / "pace-of-change-1.mp4"
R2 = P / "pace-of-change-2.mp4"
R3 = P / "pace-of-change-3.mp4"
R4 = P / "pace-of-change-4.mp4"
OUT = ROOT / "video-audit/pace-of-change-rerolls-2026-09-24/build-v6"
DEST = P / "pace-of-change-v6.mp4"
A = ROOT / "course-assets/pace-of-change"
B1, B2, B3, B4, CLOSE = (A / "pace-of-change-three-years.jpg", A / "pace-of-change-what-speeds-it-up.jpg",
                         A / "pace-of-change-could-ai-improve-itself.jpg", A / "pace-of-change-how-far-can-ai-go.jpg", A / "pace-of-change-close.jpg")
LESSON = ROOT / "lessons/pace-of-change.md"
R2B = OUT / "roll2-rewind.mp4"   # symlink to roll 2: a second sequential reader so an EARLIER roll-2 drawing (data center) can be borrowed after later ones

# ---- Roll 1 source frames (scenes.txt hard cuts; audio edges from base.en word stamps + silencedetect -30 dB)
COLLAGE = (469, 625)        # 15.63-20.83 the roll's own "2023-2026" torn-paper collage (its cuts either side)
B1_IN = 291                 # 9.70: Notebook's cut chart -> calendar; Board 1 arrives here under "To truly grasp ... three-year window"
CUT1 = (618, 915)           # 20.60 -> 30.50: "This table gives us ... capabilities." removed (silences 20.29-20.91 / 30.18-30.88)
B1_OUT = 2769               # 92.30: leave the Doing row for the phones under "AI agents can book flights..." ("thing." ends 92.06, "AI" 92.60)
# v6 race beat (David 2026-09-24): picture changes at sentence silences
ROBOT_AT = B1_OUT           # 92.30 "AI agents can book flights ..." / "These direct comparisons prove ..."
WATCH_AT = 3045             # 101.50 ("technology." ends 101.10, "What" 101.88): "... shattered in a matter of months." / fierce race / every couple of months
MOM_AT = 3435               # 114.50 ("months." ends 114.10, "Each" 114.88): "Each new release ... replacing the one before it."
PHONE_AT = 3648             # 121.60 ("it." ends 121.38, "Because" 121.80): "... rethink your assumptions ... today's no is not necessarily permanent."
CIRCUIT_AT = 4011           # 133.70 ("permanent." ends 133.34, "This" 134.06): "This commercially driven release cycle ... underlying mechanics."
B2_IN, B2_OUT = 4273, 6157  # 142.43 "We need to see exactly what is powering this speed under the hood" -> 205.23 "So what does the future..."
DC_BREAK = (5042, 5319)     # 168.07-177.30 "AI requires massive amounts of chips ... physical infrastructure." -> roll 2's data-center aisle
HAND_BREAK = (5433, 5615)   # 181.10-187.17 ("AI." ends 180.74 / "The" 181.42; "models." ends 186.78 / "On" 187.56): "The strongest current models are actively helping humans write code for the next generation of models." -> roll 4's hand at a keyboard
B3_IN, B3_OUT = 6157, 7626  # 205.23 -> 254.20 (Notebook's cut to its Board 4 render; "This brings us to the ultimate question" is Board 4's intro)
CUT5 = (6396, 6498)         # 213.20 -> 216.60: ", mapping the boundary between reality and hypothesis" removed (silences 213.03-213.49 / 216.43-217.14)
B4_IN, B4_OUT = 7626, 8959  # 254.20 -> 298.63 (Notebook's cut to its closing card)
CLOSE_END = 9110            # 303.67: "stops." ends 302.92; the roll's silence runs 303.25-306.50
# roll 2 donors (frames in roll 2)
R2_PHONE = (3375, 3531)     # 1:52.50-1:57.70 phone "System Error" turning to a check
R2_DC = (3019, 3151)        # 1:40.63-1:45.03 data-center aisle (no people)
# roll 3 / roll 4 donors (2026-09-24 rerolls; hard cuts at both ends, verified frame by frame)
R4_ROBOT = (3104, 3262)     # 1:43.47-1:48.73 robot arm assembling a city, "MANUAL ENTRY" -> "AI ASSEMBLY"
R4_WATCH = (3262, 3449)     # 1:48.73-1:54.97 stopwatch, hands blurred with speed
R3_MOM = (990, 1213)        # 0:33.00-0:40.43 MOMENTUM word art with a speed arrow
R4_CIRCUIT = (4287, 4457)   # 2:22.90-2:28.57 circuit sketch, torn-paper reveal
R4_HAND = (5869, 5999)      # 3:15.63-3:19.97 hand at a keyboard, neural net on the monitor (no face)

# ---- Board rects (image px). Board 1 rows from the 2026-09-18 ship (canvas offset 140,39 removed; asset unchanged since, sha checked
# in the manifest). Boards 2-4 cards re-probed 2026-09-23 (near-white runs: x 41-524/558-1042/1076-1559, y 128-732; x 41-783/817-1559,
# y 127-758); banners by banner_rect.
# v5 (David 2026-09-23, "highlights on this board extend too far right"): the 2026 boxes end at x=1520 (white card margin 1521-1559,
# stage from 1560); the row rings now end at 1532, 12 px past the box, instead of 1600.
B1_ROWS = {"Answering": [65, 218, 1532, 382], "Images": [65, 392, 1532, 565], "Context Window": [65, 566, 1532, 795], "Doing": [65, 796, 1532, 944]}
B2_BT, B2_MC, B2_AB = [40, 128, 526, 732], [558, 128, 1042, 732], [1076, 128, 1560, 732]
B34_L, B34_R = [40, 127, 784, 759], [816, 127, 1560, 759]

def target(label, at, rect, color, cam=None, radius=18, **kw):
    d = {"label": label, "at": at, "rects": [rect] if rect else [], "color": color, "radius": radius}
    if cam: d["cam"] = cam
    d.update(kw); return d

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[R2, R3, R4, B1, B2, B3, B4, CLOSE, LESSON, ROOT / "index.html"])
    if not R2B.is_symlink(): R2B.symlink_to(R2)
    b.load_audio([(20.29, 20.90), (30.18, 30.87), (62.54, 63.17), (97.39, 97.98), (133.69, 134.39), (191.16, 191.79), (210.76, 211.42),
                  (216.43, 217.13), (253.59, 254.26), (303.30, 306.40)])

    # ---------------- timeline (source frames of roll 1)
    b.keep(0, B1_IN, "the roll's own 2023-2026 collage re-timed under the hook (covers the AI GROWTH HITS ESCAPE VELOCITY chart)", video_from=COLLAGE[0], video_end=COLLAGE[1])
    b.keep(B1_IN, CUT1[0], "ChatGPT: 2023 vs. 2026 (canonical) arrives under To truly grasp ... three-year window (covers the calendar silhouette)", "compare")
    # cut 1 (618 -> 915): "This table gives us ... visualizing the leap in capabilities." removed; natural gap 0.62 + 0.24 s
    b.keep(CUT1[1], B1_OUT, "ChatGPT: 2023 vs. 2026: Look at the top row, answering ... it actually does the thing.", "compare")
    b.keep(ROBOT_AT, WATCH_AT, "roll 4's robot arm (MANUAL ENTRY -> AI ASSEMBLY): AI agents can book flights ... These direct comparisons prove a crucial point", video_from=R4_ROBOT[0], video_src=R4, video_end=R4_ROBOT[1])
    b.keep(WATCH_AT, MOM_AT, "roll 4's stopwatch: ... shattered in a matter of months. The AI companies are locked in a fierce race ... every couple of months.", video_from=R4_WATCH[0], video_src=R4, video_end=R4_WATCH[1])
    b.keep(MOM_AT, PHONE_AT, "roll 3's MOMENTUM: Each new release of ChatGPT, Claude or Gemini is a stronger LLM, directly replacing the one before it.", video_from=R3_MOM[0], video_src=R3, video_end=R3_MOM[1])
    b.keep(PHONE_AT, CIRCUIT_AT, "roll 2's error-to-check phone: rethink your assumptions ... A limitation can disappear quickly, so today's no is not necessarily permanent.", video_from=R2_PHONE[0], video_src=R2, video_end=R2_PHONE[1])
    b.keep(CIRCUIT_AT, B2_IN, "roll 4's circuit sketch (torn-paper reveal): This commercially driven release cycle ... look at the underlying mechanics.", video_from=R4_CIRCUIT[0], video_src=R4, video_end=R4_CIRCUIT[1])
    b.keep(B2_IN, DC_BREAK[0], "Why So Fast? (canonical) arrives under We need to see exactly what is powering this speed under the hood", "fast")
    b.keep(*DC_BREAK, "roll 2's data-center aisle under More Compute: AI requires massive amounts of chips ... physical infrastructure (breaks the board hold)", video_from=R2_DC[0], video_src=R2B, video_end=R2_DC[1])
    b.keep(DC_BREAK[1], HAND_BREAK[0], "Why So Fast?: The third driver is that AI helps build AI.", "fast")
    b.keep(*HAND_BREAK, "roll 4's hand at a keyboard: The strongest current models are actively helping humans write code for the next generation of models. (breaks the board hold)", video_from=R4_HAND[0], video_src=R4, video_end=R4_HAND[1])
    b.keep(HAND_BREAK[1], B2_OUT, "Why So Fast?: On well-defined tasks ... slow down ... AI is already helping people build better AI ... self-accelerating loop", "fast")
    b.keep(B3_IN, CUT5[0], "Could AI Improve Itself? (canonical) arrives under So what does the future of AI look like? ... This graphic shows the first two,", "improve")
    # cut 5' (6396 -> 6498): ", mapping the boundary between reality and hypothesis" removed; natural gap 0.30 + 0.38 s
    b.keep(CUT5[1], B3_OUT, "Could AI Improve Itself?: automated AI research, self-improving AI, the distinction (banner), This brings us to the ultimate question", "improve")
    b.keep(B4_IN, B4_OUT, "How Far Can AI Go? (canonical): How far can AI go? ... AGI ... ASI ... just ideas ... Nobody knows whether AI will reach either milestone.", "far")
    b.mark_close_start()
    b.keep(B4_OUT, CLOSE_END, "Closing lines: AI keeps getting faster and more powerful. / Nobody is sure where it stops.")
    b.pause(120, "Settled close hold")
    b.finish_audio()
    # close hold: 0.4 s of tone after the last word's tail, then a 1.2 s fade to silence (Transformer v10 pattern)
    ed = readwav(b.out / "edited.wav"); hold = next(r for r in b.rows if r["label"] == "Settled close hold")
    s0 = hold["start_frame"] * SPF + int(0.4 * SR); n = int(1.2 * SR)
    ed[s0:s0 + n] *= np.linspace(1.0, 0.0, n); ed[s0 + n:] = 0.0; writewav(b.out / "edited.wav", ed)

    # ---------------- boards
    # Board 1 (1600x979, tall -> 1880x1058 canvas): DENSE. Full view under the intro (cut 1 sits inside the establish, which is static),
    # then dive to each complete row at its spoken onset, pan row to row. Rows ring in the 2026 column's purple (2026-09-18 call).
    b.board("compare", B1, B1_IN, B1_OUT, "dense", [
        target("Answering row: answering", 31.96, B1_ROWS["Answering"], PURPLE, B1_ROWS["Answering"]),
        target("Images row: Next is images", 46.34, B1_ROWS["Images"], PURPLE, B1_ROWS["Images"]),
        target("Context Window row: Then there is the context window", 63.12, B1_ROWS["Context Window"], PURPLE, B1_ROWS["Context Window"]),
        target("Doing row: Finally, the doing phase", 82.90, B1_ROWS["Doing"], PURPLE, B1_ROWS["Doing"]),
    ], lead_camera=True)
    # Board 2 (1600x773): COMPACT, full view; three whole-card rings; the third ring ends at "Let's slow down" so the board is whole
    # for the repeated line. The data-center break sits inside the More Compute ring.
    b.board("fast", B2, B2_IN, B2_OUT, "compact", [
        target("Better Training: The first is better training", 154.08, B2_BT, PURPLE),
        target("More Compute: The second is more compute", 166.08, B2_MC, BLUE),
        target("AI Helps Build AI: The third driver is that AI helps build AI", 178.18, B2_AB, TEAL),
    ], pullback_at=191.52)
    # Board 3 (1600x927): DENSE. Full view under the four-ideas intro (cut 5' inside the establish), dive to each card at its onset
    # (the first ring and camera move both land at 217.45, after the cut, so no transit frame is skipped and the ring does not pop
    # mid-move: v3 failed the transition guard at that boundary for exactly that), pull back for the banner.
    b.board("improve", B3, B3_IN, B3_OUT, "dense", [
        target("Automated AI Research: First is automated AI research (ring and camera arrive together, 0.47 s after First, before automated)", 217.45, B34_L, TEAL, B34_L),
        target("Self-Improving AI: Next is self-improving AI", 232.08, B34_R, PURPLE, B34_R),
    ], banner_at=248.66, pullback_at=248.66, lead_camera=True)
    # Board 4 (1600x927): DENSE. Dive to AGI and ASI; back to full view for "It is tempting to put these milestones on a guaranteed
    # timeline, but they are just ideas." (both cards, no ring); banner ringed at "Nobody knows whether AI will reach either milestone."
    b.board("far", B4, B4_IN, B4_OUT, "dense", [
        target("General Intelligence (AGI): The first is general intelligence", 263.64, B34_L, BLUE, B34_L),
        target("Superintelligence (ASI): The second is superintelligence", 276.54, B34_R, RED, B34_R),
        target("full view, no ring: It is tempting to put these milestones on a guaranteed timeline", 290.28, None, NEUTRAL, full_view=True),
    ], banner_at=295.58, lead_camera=True)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("paceofchange")
    b.manifest({
        "scope_detail": "v6 = v5 with the race beat re-pictured from the 2026-09-24 rerolls (roll 4 robot arm, stopwatch, circuit sketch; roll 3 MOMENTUM; roll 2 phone kept and moved) and a second Board 2 break (roll 4 hand at a keyboard). Audio identical to v5. Review: video-audit/pace-of-change-rerolls-2026-09-24/REVIEW.md.",
        "narration_changes": {"cut_1_this_table_projected_state": list(CUT1), "cut_5_mapping_the_boundary": list(CUT5), "added_pauses": "none", "close_audio_end": CLOSE_END},
        "board_render_covered": [
            {"frames": [625, B1_OUT], "replacement": "canonical ChatGPT: 2023 vs. 2026 (from 291, over the calendar silhouette)"},
            {"frames": [4391, 5752], "replacement": "canonical Why So Fast? (from 4273, over the PARALLEL TENSOR ACCELERATOR fade)"},
            {"frames": [6160, 7372], "replacement": "canonical Could AI Improve Itself? (from 6157)"},
            {"frames": [7626, 8709], "replacement": "canonical How Far Can AI Go?"},
            {"frames": [8959, "end"], "replacement": "standard close"}],
        "covered_spans": [
            {"frames": [0, B1_IN], "what": "AI GROWTH HITS ESCAPE VELOCITY chart (invented capability index)", "cover": "roll 1 collage 469-625, last frame held"},
            {"frames": [B1_IN, 469], "what": "calendar with a drawn silhouette person", "cover": "Board 1 arrives early"},
            {"frames": [ROBOT_AT, WATCH_AT], "what": "the Doing row's second half, the roll's two phones, the 2023 CONSTRAINTS diagram", "cover": "roll 4 robot arm 3104-3262, last frame held"},
            {"frames": [WATCH_AT, MOM_AT], "what": "AI CAPABILITY RACE chart naming GPT-4/Claude/Gemini", "cover": "roll 4 stopwatch 3262-3449, last frame held"},
            {"frames": [MOM_AT, PHONE_AT], "what": "capability-race chart, start of the checklist", "cover": "roll 3 MOMENTUM 990-1213"},
            {"frames": [PHONE_AT, CIRCUIT_AT], "what": "the roll's checklist and red X", "cover": "roll 2 phone 3375-3531, last frame held"},
            {"frames": [CIRCUIT_AT, B2_IN], "what": "red X, FRONTIER MODEL RELEASE CYCLE, DISTRIBUTED COMPUTE, PARALLEL TENSOR ACCELERATOR", "cover": "roll 4 circuit sketch 4287-4457, last frame held"},
            {"frames": [5752, 6157], "what": "RECURSIVE AI diagram (drawn researcher, 10x Exponential Loop)", "cover": "Board 2 stays on screen, unmarked"},
            {"frames": [7372, 7626], "what": "HUMAN-DIRECTED / SELF-REINFORCING LOOP diagrams (banner restatement)", "cover": "Board 3 stays on screen, banner ringed"},
            {"frames": [8709, 8959], "what": "Theoretical & Unproven Trajectories sketch", "cover": "Board 4 stays on screen, banner ringed"}],
        "kept_notebook_spans": [],
        "notebook_breaks_inside_boards": [{"board": "fast", "frames": list(DC_BREAK), "picture": "roll 2 data-center aisle 3019-3151"}, {"board": "fast", "frames": list(HAND_BREAK), "picture": "roll 4 hand at a keyboard 5869-5999"}],
        "no_drawing_available": "Boards 3 and 4 (6157-8959): neither roll drew a shippable scene for the future-ideas beats; dive-and-pan carries them (about 90 s back to back, minus the 3.4 s cut).",
        "longest_board_runs_seconds": {"compare": round((B1_OUT - B1_IN - (CUT1[1] - CUT1[0])) / FPS, 1), "fast_before_break": round((DC_BREAK[0] - B2_IN) / FPS, 1), "fast_between_breaks": round((HAND_BREAK[0] - DC_BREAK[1]) / FPS, 1), "fast_after_hand": round((B2_OUT - HAND_BREAK[1]) / FPS, 1), "improve_plus_far": round((B4_OUT - B3_IN - (CUT5[1] - CUT5[0])) / FPS, 1)},
        "rewind_symlink": str(R2B),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:48]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
