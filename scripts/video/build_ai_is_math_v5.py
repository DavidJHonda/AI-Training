#!/usr/bin/env python3
"""AI is Math v5 review candidate from ai-is-math-1 (2026-09-22). Review only.

Full production pass from the approved plan in video-audit/ai-is-math-comparison-2026-09-22/REVIEW.md:
roll 1 is the narration (eight of eight verbatim lines exact). Two of its own additions are cut at sentence silences
(a: the "exact same mechanics" overclaim under Notebook's invented 1654/TODAY stats card, b: "Let's look at this text
generation diagram."). Two audio-only grafts from roll 2 (same-day Notebook voice) sit under our board legs:
d: "This new context changed the odds from 25 to 50 percent." after the hinge on A Clue Changes the Odds;
c: "Once a word is chosen, it joins the text ... repeating the loop." after "far from certain." on What Comes Next.
Canonical boards replace Notebook's four renders at the source's own hard cuts; all four compact at full view, still.
Two selective pauses (before "Let's start with this formula", before the close). Standard close from "AI builds
answers with probabilities." Live video, both raw rolls, lesson, and boards unchanged.
"""
from pathlib import Path
import argparse, json, subprocess, sys
import cv2, numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, rms, readwav, banner_rect, FPS, W, H, SR, SPF, NEUTRAL, PURPLE, BLUE, GREEN, RED

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/ai-is-math-1.mp4"
ROLL2 = ROOT / "Prompts/ai-is-math2.mp4"
LIVE = ROOT / "course-assets/ai-is-math/ai-is-math.mp4"     # protected, unused
OUT = ROOT / "video-audit/ai-is-math-comparison-2026-09-22/build-v5"
DEST = ROOT / "Prompts/ai-is-math-v5.mp4"
A = ROOT / "course-assets/ai-is-math"
MATH, COINS, CLUE, NEXT, CLOSE = (A / "ai-is-math-the-math.jpg", A / "ai-is-math-two-coins.jpg",
                                  A / "ai-is-math-conditional-probability.jpg", A / "ai-is-math-what-comes-next.jpg", A / "ai-is-math-close.jpg")
LESSON = ROOT / "lessons/ai-is-math.md"

# Roll-1 source frames. Visual cuts from scenes.txt, confirmed hard (no dissolve) by a +/-16 frame scan against clean
# reference frames on both sides; audio boundaries from the small.en word stamps, silencedetect (-35 dB, d=0.3) and a
# 20 ms RMS profile of each gap (breath-onset rule: resume before the next word's inhale).
A_OUT = 568        # 18.93: the source's own cut from the letters/dice/cards drawing to the invented stats card; "odds." tail ends 18.56, floor from there
A_IN = 830         # 27.67: floor after "today." (tail ends 27.64); the narrator's inhale for "Let's" (27.70-27.82) is kept; "Let's" at 28.24
MATH_OUT = 1353    # 45.10: Notebook's cut from its Standard Probability render to its Counting render
COINS_OUT = 2373   # 79.10: cut to the coins-with-question-mark drawing (kept)
EYE_OUT = 2757     # 91.90: cut from the H-coin-and-eye drawing (kept) to Notebook's Clue render; "Look at our diagram now" 92.00
D_SPLIT = 3605     # 120.17: floor after "did." (tail ends 120.06); graft d goes here; roll 1 resumes here with its small breath (120.46) and "This" 120.56
CLUE_OUT = 3617    # 120.57: cut to the Heads->speech-bubble drawing (kept)
NEXT_IN = 4112     # 137.07: cut from the FOCUSED word cloud to the capital-of-France drawing; the board arrives here under "When AI builds an answer..."
B_OUT, B_IN = 4262, 4349   # cut b: 142.07 (after "next." tail 141.88) -> 144.97 (before "You" 145.40; no breath blip in 144.86-145.38)
C_SPLIT = 5133     # 171.10: floor after "certain." (tail ends 170.84); graft c goes here; roll 1 resumes before its breath (171.28) and "Thousands" 171.42
P_SPLIT = 5446     # 181.53: floor after "next." (tail ends 181.40), before the breath at 181.78; the close pause goes here
NEXT_OUT = 5459    # 181.97: Notebook's cut to its own close; "AI" at 181.96; the standard close starts here
CLOSE_END = 5632   # 187.73: after "time." (ends 187.44, floor to 187.76); the roll's audio goes to digital zero at 187.78, never rendered
DONOR_D = (5990, 6133)   # roll 2 199.67-204.43: 0.33 s lead, "This new context changed the odds from 25 to 50 percent." 200.00-204.12, 0.31 s tail (before the breath at 204.66)
DONOR_C = (7754, 8039)   # roll 2 258.47-267.97: 0.31 s lead, "Once a word is chosen ... repeating the loop." 258.78-267.62, 0.35 s tail ("As the rule states" is after 268.47, not taken)
LD, LC = DONOR_D[1] - DONOR_D[0], DONOR_C[1] - DONOR_C[0]

# Rects in each JPG's own pixels (measured 2026-09-22: white card edges by column probe, component extents by
# non-white pixels, banners by editspec_build.banner_rect). Component rings sit >= 16 px inside their card.
MATH_CARD, MATH_BANNER = [40, 127, 1560, 447], [40, 487, 1560, 575]
COINS_SCENARIO, COINS_BANNER = [40, 127, 1560, 254], [40, 987, 1560, 1075]
COINS_TILES = [118, 346, 1518, 582]        # the four outcome columns (extent 132-1504 x 360-568), inside the 40-1560 card, above the 634 divider
COINS_HH = [116, 346, 373, 582]            # HEADS + HEADS column (extent 132-357)
COINS_FORMULA = [252, 700, 1283, 852]      # formula row incl. 1/4 and 25% (extent 270-1265 x 717-835)
CLUE_BANNER = [40, 1027, 1560, 1115]
CLUE_RULED_OUT = [846, 386, 1495, 627]     # TAILS + HEADS and TAILS + TAILS with their red crosses (extent 862-1479 x 400-613); divider at 674
CLUE_REMAINING = [116, 386, 780, 627]      # HEADS + HEADS and HEADS + TAILS (extent 132-764)
CLUE_FORMULA = [252, 740, 1285, 892]       # formula row incl. 1/2 and 50% (extent 270-1267 x 757-875)
NEXT_YOU, NEXT_BANNER = [40, 127, 1560, 254], [40, 788, 1560, 876]
NEXT_REPLY = [505, 318, 1090, 440]         # AI'S REPLY SO FAR + "You could name him ____" (extent 523-1072 x 332-426); card top 287
NEXT_CHIPS = [312, 510, 1288, 656]         # Spot / Max / Buddy chips as one point (extent 320-1280 x 518-648) plus 8 px; label bottom 495, footnote top 694
NEXT_SPOT = [314, 512, 606, 654]           # the Spot chip's own border (320-600 x 518-648) plus 6 px
NEXT_FOOTNOTE = [244, 684, 1354, 732]      # "Illustrative probabilities. Other possible next words make up the remaining 47%." (extent 258-1340 x 694-722); card bottom 748

def target(label, at, rect, color, radius=18):
    return {"label": label, "at": at, "rects": [rect] if rect else [], "color": color, "radius": radius}

def speech_rms(wav, spans):
    a = readwav(wav); return rms(np.concatenate([a[round(s * SR):round(e * SR)] for s, e in spans]))

def ramp_graft_edges(b, lead_s, tail_s):
    """Blend the just-added audio-only graft's own lead-in and tail silence from/into roll 1's matched room tone over
    their whole length instead of graft()'s 5 ms butt, so the donor's higher noise floor (roll 2 sits ~6-9 dB above
    roll 1 in its gaps) fades in under the beat and out after it with no floor cliff. Speech samples are untouched."""
    data = b.parts[-1]; bed = b.tone(len(data))
    n0 = round(lead_s * SR); r0 = np.linspace(0, 1, n0); data[:n0] = bed[:n0] * (1 - r0) + data[:n0] * r0
    n1 = round(tail_s * SR); r1 = np.linspace(1, 0, n1); data[-n1:] = bed[-n1:] * (1 - r1) + data[-n1:] * r1

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, ROLL2, MATH, COINS, CLUE, NEXT, CLOSE, LESSON]); b.tall_margin = True
    b.load_audio([(18.60, 19.00), (27.86, 28.20), (44.80, 45.10), (74.80, 75.20), (86.90, 87.40), (112.30, 112.80), (120.10, 120.45),
                  (136.60, 137.10), (142.00, 142.40), (144.90, 145.35), (171.00, 171.25), (176.40, 177.00), (181.40, 181.75)])

    # Level match: each donor beat against the roll-1 sentence it follows (speech RMS over the whole beat).
    donor_wav = OUT / "graft-d.wav"
    if not donor_wav.exists():
        subprocess.run([b.ff, "-y", "-v", "error", "-i", str(ROLL2), "-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(donor_wav)], check=True)
    r1_hinge = speech_rms(OUT / "source.wav", [(115.74, 119.92)]); r1_certain = speech_rms(OUT / "source.wav", [(166.92, 170.74)])
    d_d = speech_rms(donor_wav, [(200.00, 204.12)]); d_c = speech_rms(donor_wav, [(258.78, 267.62)])
    gain_d = round(20 * np.log10(r1_hinge / d_d), 2); gain_c = round(20 * np.log10(r1_certain / d_c), 2)

    b.keep(0, A_OUT, "Notebook drawings: math-symbols collage, letters/dice/cards (1654, Pascal and Fermat)")
    b.pause(18, "breath before the formula board (cut a join: natural 0.37 + 0.57 = 0.94 s -> ~1.54 s)")
    b.keep(A_IN, MATH_OUT, "Standard Probability (canonical): formula card ring at On top, banner at the verbatim line", "math")
    b.keep(MATH_OUT, COINS_OUT, "Counting the Possibilities (canonical): scenario, four tiles, both heads, formula, banner", "coins")
    b.keep(COINS_OUT, EYE_OUT, "Notebook drawings: coins with question mark, H coin with the peeking eye")
    b.keep(EYE_OUT, D_SPLIT, "A Clue Changes the Odds (canonical): ruled-out pair, remaining pair, formula, banner, unmarked hinge", "clue")
    b.graft(ROLL2, *DONOR_D, "graft d (roll 2, audio only, under the Clue board): This new context changed the odds from 25 to 50 percent.", "d",
            picture_from=D_SPLIT, gain_db=gain_d, visual="clue")
    ramp_graft_edges(b, 0.30, 0.28)
    b.keep(D_SPLIT, CLUE_OUT, "Clue board: floor and breath before This exact process", "clue", video_from=D_SPLIT + LD)
    b.keep(CLUE_OUT, NEXT_IN, "Notebook drawings: Heads -> speech bubble, FOCUSED word cloud")
    b.keep(NEXT_IN, B_OUT, "What Comes Next (canonical) arrives under When AI builds an answer... (covers the capital-of-France drawing)", "next")
    b.keep(B_IN, C_SPLIT, "What Comes Next: question, reply, chips, Spot, far from certain", "next")
    b.graft(ROLL2, *DONOR_C, "graft c (roll 2, audio only, under the What Comes Next board): Once a word is chosen ... repeating the loop.", "c",
            picture_from=C_SPLIT, gain_db=gain_c, visual="next")
    ramp_graft_edges(b, 0.28, 0.30)
    b.keep(C_SPLIT, P_SPLIT, "What Comes Next: remaining 47% (footnote ring), banner line", "next", video_from=C_SPLIT + LC)
    b.pause(18, "breath before the close (natural 0.56 s -> ~1.16 s)")
    b.keep(P_SPLIT, NEXT_OUT, "What Comes Next: breath before AI builds", "next", video_from=P_SPLIT + LC)
    b.mark_close_start()
    b.keep(NEXT_OUT, CLOSE_END, "Closing lines: AI builds answers with probabilities. / One prediction at a time.")
    b.pause(120, "Settled close hold")
    b.finish_audio()

    # Standard Probability (1600x615), compact and still: whole formula card at "On top", banner at the verbatim line.
    b.board("math", MATH, A_IN, MATH_OUT, "compact", [
        target("formula card: On top / On the bottom", 34.02, MATH_CARD, PURPLE),
        target("banner: Ways to get the result / total possible outcomes = probability.", 40.24, MATH_BANNER, NEUTRAL, radius=22),
    ], push=False)

    # Counting the Possibilities (1600x1115, tall), compact and still.
    b.board("coins", COINS, MATH_OUT, COINS_OUT, "compact", [
        target("scenario card: The scenario is simple", 47.84, COINS_SCENARIO, PURPLE),
        target("four outcome tiles: four equally likely ways", 55.94, COINS_TILES, NEUTRAL),
        target("HEADS + HEADS tile: only one gives us the result", 66.80, COINS_HH, GREEN),
        target("formula: Plug that into our formula", 69.58, COINS_FORMULA, PURPLE),
        target("banner: Before new evidence, one out of four is 25%.", 75.24, COINS_BANNER, NEUTRAL, radius=22),
    ], push=False)

    # A Clue Changes the Odds (1600x1155, tall), compact and still. The scenario is spoken over Notebook's own peek
    # drawing (kept), so the board arrives on the source's cut at "Look at our diagram now" and opens whole for 3.3 s;
    # unmarked from the hinge through the grafted 25-to-50 line. The leg carries the graft's frames (LD) after D_SPLIT.
    b.board("clue", CLUE, EYE_OUT, CLUE_OUT + LD, "compact", [
        target("ruled-out pair: rules out two of our previous options", 95.24, CLUE_RULED_OUT, RED),
        target("remaining pair: left with just two possible outcomes", 103.52, CLUE_REMAINING, NEUTRAL),
        target("formula: Our formula now shows one divided by two", 108.50, CLUE_FORMULA, GREEN),
        target("banner: After the clue, one out of two is 50%.", 112.40, CLUE_BANNER, NEUTRAL, radius=22),
        target("unmarked: the hinge and the grafted 25-to-50 line", 115.74, None, NEUTRAL),
    ], push=False)

    # What Comes Next? (1600x916), compact and still. Onsets after the graft are in the leg's own (virtual) timeline.
    v = lambda t: (fr(t) + LC) / FPS
    b.board("next", NEXT, NEXT_IN, NEXT_OUT + LC, "compact", [
        target("question bubble: You ask the AI", 145.38, NEXT_YOU, PURPLE),
        target("reply: The AI starts its reply with", 149.02, NEXT_REPLY, PURPLE),
        target("three chips: calculates a probability for every possible word", 154.90, NEXT_CHIPS, PURPLE),
        target("Spot chip: spot sits at 22%", 160.96, NEXT_SPOT, PURPLE),
        target("unmarked: grafted repeat beat", C_SPLIT / FPS, None, NEUTRAL),
        target("footnote: Thousands of other possible words ... remaining 47%", v(171.46), NEXT_FOOTNOTE, PURPLE),
        target("banner: The question and the words already written shape what is likely to come next.", v(177.00), NEXT_BANNER, NEUTRAL, radius=22),
    ], push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("aiismath")
    b.manifest({
        "scope_detail": "Full production review candidate from the approved 2026-09-22 plan (roll 1 base, cuts a and b, grafts c and d from roll 2 under our boards); live video, both raw rolls, lesson, and boards unchanged.",
        "narration_changes": {
            "cut_a_exact_same_mechanics": [A_OUT, A_IN], "cut_b_text_generation_diagram": [B_OUT, B_IN],
            "graft_d_after_source_frame": D_SPLIT, "graft_d_roll2_frames": list(DONOR_D), "graft_d_gain_db": gain_d,
            "graft_c_after_source_frame": C_SPLIT, "graft_c_roll2_frames": list(DONOR_C), "graft_c_gain_db": gain_c,
            "speech_rms": {"roll1_hinge_115.74-119.92": r1_hinge, "roll2_donor_d_200.00-204.12": d_d, "roll1_far_from_certain_166.92-170.74": r1_certain, "roll2_donor_c_258.78-267.62": d_c},
            "graft_edge_ramps": "each donor's ~0.3 s lead-in and tail silence is blended from/into roll 1's matched room tone over its full length (ramp_graft_edges); speech untouched"},
        "added_teaching_pauses": [
            {"after_source_frame": A_OUT, "frames": 18, "why": "before Let's start with this formula (cut a join)"},
            {"after_source_frame": P_SPLIT, "frames": 18, "why": "before AI builds answers with probabilities"}],
        "board_render_covered": [
            {"frames": [A_IN, MATH_OUT], "replacement": "canonical Standard Probability (Notebook's render ran 844-1353; 830-844 is inside cut a)"},
            {"frames": [MATH_OUT, COINS_OUT], "replacement": "canonical Counting the Possibilities"},
            {"frames": [EYE_OUT, CLUE_OUT], "replacement": "canonical A Clue Changes the Odds (+ graft d)"},
            {"frames": [NEXT_IN, NEXT_OUT], "replacement": "canonical What Comes Next (arrives 4112 under the verbatim line, covering the capital-of-France drawing 4112-4273; Notebook's render ran 4273-5459)"},
            {"frames": [NEXT_OUT, "end"], "replacement": "standard close (Notebook's close and spinner never rendered)"}],
        "photographs_and_invented_diagrams": [
            {"frames": [568, 844], "what": "invented 1654 GAMBLING MATH / TODAY AI PREDICTION stats card", "handling": "inside cut a (568-830) and under the board (830-844)"},
            {"note": "no stock photographs seen: frame 0 is the drawn collage; kept spans sampled in kept-notebook-spans.jpg"}],
        "notebook_interleaves": [],
        "kept_notebook_spans_source_frames": [[0, A_OUT], [COINS_OUT, EYE_OUT], [CLUE_OUT, NEXT_IN]],
        "longest_unbroken_board_run_seconds": round((B_OUT - NEXT_IN + C_SPLIT - B_IN + LC + P_SPLIT - C_SPLIT + 18 + NEXT_OUT - P_SPLIT) / FPS, 2),
        "plan_deviations": [
            "Clue board: no scenario ring; the scenario sentence (87.48-91.30) plays over Notebook's kept H-coin-and-eye drawing and the board arrives on the source's cut at 91.90.",
            "What Comes Next arrives at 137.07 (under the verbatim 'When AI builds an answer...' line) instead of 142.43, covering the capital-of-France drawing: with cut b the 142.43 arrival would have given 0.37 s of full view before the first ring.",
        ],
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", "gain d", gain_d, "gain c", gain_c, flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:40]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
