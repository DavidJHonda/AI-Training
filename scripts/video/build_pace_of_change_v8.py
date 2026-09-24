#!/usr/bin/env python3
"""Pace of Change v8 review candidate (v7 plus David's two notes of 2026-09-24: Why So Fast? arrives on "This diagram outlines..."
instead of after roll 4's circuit sketch, which is dropped; the AI Helps Build AI ring stays on through "Slow down..." and the
repeated line; also the capability-cards hold frame moved before the morph). Originally: Pace of Change v7 review candidate from pace-of-change-4 (2026-09-24 roll). Review only.

David 2026-09-24 on roll 4: "I like what it did. There are graphical representations of our boards which look like they're
true to our boards ... it's more engaging. We could show our board for a couple of seconds at the beginning or end." The
review (video-audit/pace-of-change-rerolls-2026-09-24/REVIEW.md) agreed for Board 1 only: roll 4's animated 2023-vs-2026
build is true to the canonical board, but its Boards 2-4 carry invented statistics (98.4%, 100x) and draw the four future
ideas as a roadmap / timeline, which the lesson says they are not. David: "Build it."

Narration: roll 4 (6 of 6 required lines exact) with three sentence cuts and one phrase cut, all measured on the roll's own
audio (silencedetect -35 dB; the phrase cut at RMS troughs, joined audio re-transcribed "Current models can hold a million
tokens."):
  cut 1  "We are looking at a side-by-side view of what a model like ChatGPT could do in 2023 versus where the models of 2026
         are headed." (24.40-32.53; 2026 treated as a projection)
  cut 2  "aiming for 2026 capabilities" (78.60-80.77; same error, inside the Context Window row)
  cut 3  "Three years turned a text generator with poor memory into an autonomous agent." (103.30-108.60; overclaim)
  cut 4  "Because the tool builds a better version of itself, it creates a compounding feedback loop, driving an exponential
         rate of change." (199.50-208.20; states the undemonstrated loop as fact; banned "exponential")
  Kept, as with roll 1 (David 2026-09-23): the on-screen furniture sentences, "the ultimate question", "theoretical concepts".
Pictures:
  hook: roll 4's own brain / sound-wave drawing, roll 1's 2023-2026 collage over roll 4's ACCELERATION DRIVERS chart, roll 4's
    own four capability cards under "look at the baseline of what AI can actually do" (held before its EXPONENTIAL TRAJECTORY
    morph); canonical Board 1 at full view, no ring, for ~7 s under "Look at this comparison..." / "...in just three years.";
    then roll 4's own animated 2023-vs-2026 build, row by row, through "...fix code errors right in front of you."
  race: roll 4 robot arm and stopwatch (re-timed after cut 3), roll 3 MOMENTUM and roll 2 phone -> check/X over roll 4's
    ChatGPT/Claude/Gemini cards (invented token counts) and GEN N diagram, roll 4 circuit sketch under "This diagram outlines...".
  Boards 2-4 canonical (Board 2 broken by roll 2's data-center aisle and roll 4's hand at a keyboard); roll 4's own forked
    spectrum ("?" paths, "Not a guaranteed timeline") under "These are theoretical concepts ... not a guaranteed timeline of
    future events."; standard close.
Live assets, all rolls, lesson, boards, index.html unchanged.
"""
from pathlib import Path
import argparse, sys
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, readwav, writewav, FPS, SR, SPF, NEUTRAL, PURPLE, BLUE, TEAL, RED

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC = P / "pace-of-change-4.mp4"
R1, R2, R3 = P / "pace-of-change-1.mp4", P / "pace-of-change-2.mp4", P / "pace-of-change-3.mp4"
OUT = ROOT / "video-audit/pace-of-change-rerolls-2026-09-24/build-v8"
DEST = P / "pace-of-change-v8.mp4"
A = ROOT / "course-assets/pace-of-change"
B1, B2, B3, B4, CLOSE = (A / "pace-of-change-three-years.jpg", A / "pace-of-change-what-speeds-it-up.jpg",
                         A / "pace-of-change-could-ai-improve-itself.jpg", A / "pace-of-change-how-far-can-ai-go.jpg", A / "pace-of-change-close.jpg")
LESSON = ROOT / "lessons/pace-of-change.md"
R2B = OUT / "roll2-rewind.mp4"   # second sequential reader on roll 2: its data-center aisle (earlier frames) follows its phone

# ---- Roll 4 source frames (audio edges inside silencedetect -35 dB gaps unless noted)
COLLAGE_AT = 132            # 4.40 (silence 4.17-4.65): "The reason for this intensity is simple." -> roll 1 collage (covers the chart from 6.0)
CARDS_AT = 407              # 13.57 (13.46-13.71): "you have to look at the baseline of what AI can actually do"
CARDS_END = 510             # 17.00: last clean frame of the four capability cards (the EXPONENTIAL TRAJECTORY morph starts at 513;
                            # v7 held 525, which already showed an empty grey pill, lower right)
B1_IN = 631                 # 21.03 (20.73-21.36): "Look at this comparison mapping AI capabilities."
CUT1 = (732, 976)           # 24.40 -> 32.53 (24.12-24.46 / 32.36-32.78)
NATIVE_B1 = 1103            # 36.77 (36.47-37.03): "First, look at answering." -> roll 4's own animated board
CUT2 = (2358, 2423)         # 78.60 -> 80.77: "aiming for 2026 capabilities" (RMS troughs -47 / -50 dB; "can" onsets 81.10)
CUT3 = (3099, 3258)         # 103.30 -> 108.60 (102.90-103.41 / 108.48-108.76)
WATCH_AT = 3440             # 114.67 (114.39-114.98): "This rapid release cycle is driven by market forces."
MOM_AT = 3760               # 125.33 (125.07-125.58): "Each time a major player releases a new version..."
PHONE_AT = 4107             # 136.90 (136.57-137.23): "Because of this constant replacement ... today's no is not necessarily permanent."
B2_IN = 4447                # 148.23 (147.88-148.59): "This diagram outlines what exactly is driving this relentless acceleration."
                            # (v8, David: the board must be up when the narration says "This diagram"; v7 showed roll 4's circuit sketch here)
DC_BREAK = (5089, 5367)     # 169.63-178.90 "Running these models require massive amounts of chips ... computing power."
HAND_BREAK = (5462, 5742)   # 182.07-191.40 "On well-defined tasks, the strongest models can write code ... human programmers."
CUT4 = (5985, 6246)         # 199.50 -> 208.20 (199.15-199.85 / 207.75-208.63)
B3_IN, B3_OUT = 6246, 7932  # 208.20 "Look at this conceptual map of the future." -> 264.40 (264.03-264.55)
B4_IN, B4_OUT = 7932, 9012  # 264.40 "That brings us to the ultimate question..." -> 300.40 (300.18-300.63)
CLOSE_IN = 9210             # 307.00 (306.82-307.39): "AI keeps getting faster and more powerful."
CLOSE_END = 9366            # 312.20: "stops." ends 311.58; the roll's silence runs 311.84-315.28
# roll 4's own donor drawings (hard cuts both ends, verified frame by frame 2026-09-24)
R4_ROBOT = (3104, 3262)     # robot arm, "MANUAL ENTRY" -> "AI ASSEMBLY"
R4_WATCH = (3262, 3449)     # stopwatch
R4_HAND = (5869, 5999)      # hand at a keyboard, neural net on the monitor (no face)
# other rolls
R1_COLLAGE = (469, 625)     # roll 1 0:15.63-0:20.83 "2023-2026" torn-paper collage
R3_MOM = (990, 1213)        # roll 3 0:33.00-0:40.43 MOMENTUM
R2_PHONE_CHECK = (3375, 3670)  # roll 2 1:52.50-2:02.33 phone "System Error" -> check, then green check / grey X
R2_DC = (3019, 3151)        # roll 2 1:40.63-1:45.03 data-center aisle

B2_BT, B2_MC, B2_AB = [40, 128, 526, 732], [558, 128, 1042, 732], [1076, 128, 1560, 732]
B34_L, B34_R = [40, 127, 784, 759], [816, 127, 1560, 759]

def target(label, at, rect, color, cam=None, radius=18, **kw):
    d = {"label": label, "at": at, "rects": [rect] if rect else [], "color": color, "radius": radius}
    if cam: d["cam"] = cam
    d.update(kw); return d

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[R1, R2, R3, B1, B2, B3, B4, CLOSE, LESSON, ROOT / "index.html"])
    if not R2B.is_symlink(): R2B.symlink_to(R2)
    b.load_audio([(20.73, 21.36), (36.47, 37.03), (49.51, 50.21), (68.07, 68.66), (136.57, 137.23), (190.97, 191.89),
                  (207.75, 208.63), (222.72, 223.57), (311.84, 315.28)])

    # ---------------- timeline (source frames of roll 4)
    b.keep(0, COLLAGE_AT, "roll 4's own brain and sound waves: The arguments surrounding artificial intelligence are getting louder.")
    b.keep(COLLAGE_AT, CARDS_AT, "roll 1's 2023-2026 collage over roll 4's ACCELERATION DRIVERS chart: ...simple. The technology is advancing at blazing speeds. To understand any debate...", video_from=R1_COLLAGE[0], video_src=R1, video_end=R1_COLLAGE[1])
    b.keep(CARDS_AT, B1_IN, "roll 4's own four capability cards, held before the EXPONENTIAL TRAJECTORY morph: look at the baseline of what AI can actually do", video_from=CARDS_AT, video_end=CARDS_END)
    b.keep(B1_IN, CUT1[0], "ChatGPT: 2023 vs. 2026 (canonical, full view): Look at this comparison mapping AI capabilities.", "compare")
    # cut 1 (732 -> 976)
    b.keep(CUT1[1], NATIVE_B1, "ChatGPT: 2023 vs. 2026 (canonical, full view): This shows how drastically the technology evolves in just three years.", "compare")
    b.keep(NATIVE_B1, CUT2[0], "roll 4's own animated 2023 vs 2026 build: answering, images, context window ... Current models")
    # cut 2 (2358 -> 2423): "aiming for 2026 capabilities"
    b.keep(CUT2[1], CUT3[0], "roll 4's own animated build: ...can hold a million tokens ... taking action ... fix code errors right in front of you.")
    # cut 3 (3099 -> 3258): "Three years turned ... autonomous agent."
    b.keep(CUT3[1], WATCH_AT, "roll 4's robot arm: The definition of what an AI is capable of shifts completely in a very short window of time.", video_from=R4_ROBOT[0], video_end=R4_ROBOT[1])
    b.keep(WATCH_AT, MOM_AT, "roll 4's stopwatch: This rapid release cycle is driven by market forces ... every couple of months.", video_from=R4_WATCH[0], video_end=R4_WATCH[1])
    b.keep(MOM_AT, PHONE_AT, "roll 3's MOMENTUM over roll 4's ChatGPT/Claude/Gemini cards: Each time a major player releases a new version ... replaces the previous one.", video_from=R3_MOM[0], video_src=R3, video_end=R3_MOM[1])
    b.keep(PHONE_AT, B2_IN, "roll 2's phone -> check, then check/X over roll 4's GEN N diagram: Because of this constant replacement ... today's no is not necessarily permanent.", video_from=R2_PHONE_CHECK[0], video_src=R2, video_end=R2_PHONE_CHECK[1])
    b.keep(B2_IN, DC_BREAK[0], "Why So Fast? (canonical): This diagram outlines ... three mechanical concepts ... better training ... The second driver is more compute.", "fast")
    b.keep(*DC_BREAK, "roll 2's data-center aisle: Running these models require massive amounts of chips ... computing power.", video_from=R2_DC[0], video_src=R2B, video_end=R2_DC[1])
    b.keep(DC_BREAK[1], HAND_BREAK[0], "Why So Fast?: The third driver is that AI helps build AI.", "fast")
    b.keep(*HAND_BREAK, "roll 4's hand at a keyboard: On well-defined tasks, the strongest models can write code for the next generation of models much faster than human programmers.", video_from=R4_HAND[0], video_end=R4_HAND[1])
    b.keep(HAND_BREAK[1], CUT4[0], "Why So Fast? (AI Helps Build AI still ringed): Slow down and consider that third concept again. AI is already helping people build better AI.", "fast")
    # cut 4 (5985 -> 6246): "Because the tool builds a better version of itself ... exponential rate of change."
    b.keep(B3_IN, B3_OUT, "Could AI Improve Itself? (canonical): conceptual map ... four ideas ... automated AI research ... self-improving AI ... the distinction (banner) ... hypothetical", "improve")
    b.keep(B4_IN, B4_OUT, "How Far Can AI Go? (canonical): the ultimate question ... AGI ... ASI ... Nobody knows whether AI will reach either milestone.", "far")
    b.keep(B4_OUT, CLOSE_IN, "roll 4's own forked spectrum ('?' paths, Not a guaranteed timeline): These are theoretical concepts ... not a guaranteed timeline of future events.")
    b.mark_close_start()
    b.keep(CLOSE_IN, CLOSE_END, "Closing lines: AI keeps getting faster and more powerful. / Nobody is sure where it stops.")
    b.pause(120, "Settled close hold")
    b.finish_audio()
    ed = readwav(b.out / "edited.wav"); hold = next(r for r in b.rows if r["label"] == "Settled close hold")
    s0 = hold["start_frame"] * SPF + int(0.4 * SR); n = int(1.2 * SR)
    ed[s0:s0 + n] *= np.linspace(1.0, 0.0, n); ed[s0 + n:] = 0.0; writewav(b.out / "edited.wav", ed)

    # ---------------- boards
    # Board 1: David's "show our board for a couple of seconds": full view, still (cut 1 inside), no ring; roll 4's own build follows.
    b.board("compare", B1, B1_IN, NATIVE_B1, "compact", [], push=False)
    b.board("fast", B2, B2_IN, CUT4[0], "compact", [
        target("Better Training: The first driver is better training", 157.25, B2_BT, PURPLE),
        target("More Compute: The second driver is more compute", 167.60, B2_MC, BLUE),
        target("AI Helps Build AI: The third driver is that AI helps build AI", 179.21, B2_AB, TEAL),
    ])   # v8 (David): no pull-back; the AI Helps Build AI ring stays on through "Slow down and consider that third concept again." and "AI is already helping people build better AI." 
    b.board("improve", B3, B3_IN, B3_OUT, "dense", [
        target("Automated AI Research: The first is automated AI research", 223.57, B34_L, TEAL, B34_L),
        target("Self-Improving AI: The second idea is self-improving AI", 235.30, B34_R, PURPLE, B34_R),
    ], banner_at=249.41, pullback_at=248.00, lead_camera=True)
    b.board("far", B4, B4_IN, B4_OUT, "dense", [
        target("General Intelligence (AGI): The first is AGI", 272.98, B34_L, BLUE, B34_L),
        target("Superintelligence (ASI): Further out is ASI", 283.74, B34_R, RED, B34_R),
    ], banner_at=297.39, lead_camera=True)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("paceofchange")
    b.manifest({
        "scope_detail": "v8 = v7 with Board 2 arriving on This diagram outlines (circuit sketch dropped), the AI Helps Build AI ring held through Slow down and the repeated line, and the cards hold frame 510. v7: roll 4 as the base (David 2026-09-24, 'Build it'): four narration cuts, roll 4's own animated Board 1 after ~7 s of the canonical board, canonical Boards 2-4, race beat and Board 2 breaks from rolls 1-4, roll 4's forked spectrum under the not-a-timeline line, standard close.",
        "narration_changes": {"cut_1_side_by_side_2026_headed": list(CUT1), "cut_2_phrase_aiming_for_2026_capabilities": list(CUT2),
                              "cut_3_autonomous_agent": list(CUT3), "cut_4_compounding_exponential_loop": list(CUT4), "added_pauses": "none", "close_audio_end": CLOSE_END},
        "kept_notebook_spans": [[0, COLLAGE_AT], [CARDS_AT, CARDS_END], [NATIVE_B1, CUT3[0]], [B4_OUT, CLOSE_IN]],
        "covered_spans": [
            {"frames": [180, 407], "what": "ACCELERATION DRIVERS chart (BLAZING SPEED curve)", "cover": "roll 1 collage 469-625, held"},
            {"frames": [CARDS_END, B1_IN], "what": "EXPONENTIAL TRAJECTORY morph", "cover": "roll 4 cards frame held"},
            {"frames": [B1_IN, NATIVE_B1], "what": "roll 4's empty board frame", "cover": "canonical Board 1, full view"},
            {"frames": [MOM_AT, B2_IN], "what": "ENGINE OF ACCELERATION, release cadence, ChatGPT/Claude/Gemini cards with invented token counts, GEN N diagram", "cover": "roll 3 MOMENTUM, roll 2 phone and check/X"},
            {"frames": [B2_IN, CUT4[0]], "what": "DRIVERS OF AI ACCELERATION render with invented statistics (98.4%, 100x)", "cover": "canonical Why So Fast?"},
            {"frames": [B3_IN, B3_OUT], "what": "AI Progression Roadmap 01-04, Phase 1 / Phase 2 (a sequence), gears and human silhouette", "cover": "canonical Could AI Improve Itself?"},
            {"frames": [B4_IN, B4_OUT], "what": "AI Capability Spectrum as a line with milestones (a timeline)", "cover": "canonical How Far Can AI Go?"},
            {"frames": [CLOSE_IN, "end"], "what": "Notebook closing card", "cover": "standard close"}],
        "notebook_breaks_inside_boards": [{"board": "fast", "frames": list(DC_BREAK), "picture": "roll 2 data-center aisle"}, {"board": "fast", "frames": list(HAND_BREAK), "picture": "roll 4 hand at a keyboard"}],
        "rewind_symlink": str(R2B),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:48]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
