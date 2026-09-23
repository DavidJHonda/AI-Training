#!/usr/bin/env python3
"""Layers v2 review candidate from layers-6 (2026-09-23). Review only.

Full production pass from the approved plan in video-audit/layers-comparison-2026-09-23/REVIEW.md (roll 6 REPAIR PLAN a-e,
EDITING NOTES, BEST-OF PLAN, edit-plan table; David approved all of it, repair a as the graft). Roll 6 is the base (6 of 8 required
lines exact, the middle number values unspoken); two audio-only grafts and two cuts change its narration:
  a. graft: roll 6's split sentence + production phrase ("The horse raced past the barn. Fell. This infographic breaks down exactly
     why that sentence trips us up.", 6.60-14.67) is replaced by roll 5's "The horse raced past the barn fell." (11.40-14.87: 0.46 s
     lead, the sentence 11.86-14.04, the 0.83 s beat after it), level-matched by speech RMS to roll 6's neighbours. Picture: Board 1.
  b. cut: "This diagram shows how those internal layers actually update the numbers." (68.70-73.37); Board 2 arrives at the resume.
  c. cut: "This chart maps out the five stages of how the AI resolves that pronoun." (117.37-122.53); Board 3 arrives at the resume.
  d. graft: roll 6's garbled, compressed "Untamelling sarcasm ... horse sentence." (172.57-181.03) is replaced by roll 2's three
     sentences "The horse sentence took a few reads to untangle. Sarcasm, story twists, and complicated reasoning can take even more
     work. AI's layers give it more steps to work through those relationships and build meaning." (192.67-206.20), level-matched
     (roll 2 is a different day). Picture: a held, settled frame of roll 6's own stacked-layers drawing (5150) from the graft start
     through "...worth the cost.", so the invented Simple Syntax / Complex Reasoning / Depth: 32 Layers / 128+ Layers / Optimal: ~48
     Layers cards (5187-5804) never show.
  e. close: roll 6's own 0.44 s gap between "layer," and "attention" is widened to ~1.0 s with matched room tone under the standard
     close board (17 frames inserted at 196.00); the close audio ends after the "times." sibilant; 120-frame tail with the tone fade
     from build_transformer_v10.py (the framework's 0.2 s tone loop pulses on a long hold).
Canonical boards replace Notebook's three renders. Board 1 arrives at the roll's own cut at 5.17 (its cut to the "Fell?" card, which
would otherwise flash for 1.4 s before the graft start), so it is on screen for "Try this sentence." and the grafted sentence. The
invented LAYER 1 attention/transformation diagram (1569-1957, with [0.42, -1.15] printed) is covered by the roll's own 3D
stacked-layers drawing held back from 2000. No other pauses. Live video, all raw rolls, lesson, index.html and boards unchanged.

All audio edges were placed on 20 ms RMS profiles + silencedetect; the small.en stamps ran early at the close ("Meaning" starts
193.39, not 192.74) and late at "Numbers" (73.45, not 73.80).

Usage: .video-venv/bin/python scripts/video/build_layers_v2.py [--prepare-only] [--render-existing]
"""
from pathlib import Path
import argparse, subprocess, sys
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, rms, readwav, writewav, FPS, SR, SPF, NEUTRAL, PURPLE, BLUE, TEAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/layers-6.mp4"
ROLL5 = ROOT / "Prompts/layers-5.mp4"       # donor: the horse sentence
ROLL2 = ROOT / "Prompts/layers-2.mp4"       # donor: untangle / sarcasm / more steps
LIVE = ROOT / "course-assets/layers/layers.mp4"   # protected, unused
OUT = ROOT / "video-audit/layers-comparison-2026-09-23/build-v2"
DEST = ROOT / "Prompts/layers-v2.mp4"
A = ROOT / "course-assets/layers"
B1, B2, B3, CLOSE = A / "layers-horse-three-reads.jpg", A / "layers-inside-layer.jpg", A / "layers-resolves-it.jpg", A / "layers-close.jpg"
LESSON = ROOT / "lessons/layers.md"

# ---- roll 6 source frames (hard cuts confirmed by a sequential decode: single-frame spikes 30-51 MAD, zero either side)
B1_IN = 155          # 5.17: the roll's cut from the lamp/book drawing to its "Fell?" card; Board 1 arrives here ("Try this sentence." 5.32)
GRAFT_A_OUT = 198    # 6.60: floor (-70 dBFS) after "sentence." (tail ends 6.16); roll 6's "The" starts 6.64
GRAFT_A_IN = 440     # 14.667: floor (-68) before "On" (onset 14.72); "up." tail ended 14.16
DONOR_A = (342, 446) # roll 5 11.40-14.867: 0.46 s lead (floor -65 to -72), "The horse raced past the barn fell." 11.86-14.04, 0.83 s beat (floor -67 to -73)
B1_OUT = 1497        # 49.90: cut to the phone drawing; "AI doesn't read" 50.08
PHONE_OUT = 1569     # 52.30: cut to blank paper that draws into the invented LAYER 1 diagram (never shows)
L3D_IN = 1957        # 65.23: cut to the 3D stacked-layers drawing (static to 2063: max 0.65 MAD vs its first frame)
L3D_HOLD = 2000      # a settled frame of it, held back over 1569-1957
CUT_B_OUT = 2061     # 68.70: floor (-68) after "network." (tail ends 68.08); "This" starts 68.78; the roll cuts to its Board 2 render at 2063
CUT_B_IN = 2201      # 73.367: floor (-70) before "Numbers" (onset 73.45, a full sentence-length breath is not present); Board 2 arrives
B2_OUT = 3357        # 111.90: cut to the sentence drawing, 0.2 s into "Now let's follow"
CUT_C_OUT = 3521     # 117.367: floor (-65) after "sentence." (tail ends 117.10); the roll's audio dips to digital zero 117.38-117.46 (never rendered); "This" 117.72
CUT_C_IN = 3676      # 122.533: floor (-63 to -67) before "At" (onset 122.74); Board 3 arrives
B3_OUT = 4884        # 162.80: cut to the stacked-layers drawing (framing A, static); "While" 162.80
STACK_REFRAME = 5026 # 167.53: the roll's own cut to framing B of the same drawing (static to 5187); kept as Notebook's own cut
GRAFT_D_OUT = 5177   # 172.567: floor (-71) after "layers." (tail ends 172.32); digital-zero dip 172.60-172.66 never rendered; "Untamelling" 172.80
STACK_HOLD = 5150    # a settled frame of framing B, held from the graft start to the close
DONOR_D = (5780, 6186)  # roll 2 192.667-206.20: 0.29 s lead (floor -70), three sentences 192.96-205.78, 0.42 s tail (floor -70); "Why not" would start 206.34
GRAFT_D_IN = 5431    # 181.033: floor (-70) before "If" (onset 181.08); the roll's cut to its Neural Model Architecture cards is 5432 (under the hold)
CLOSE_IN = 5801      # 193.367: 0.02 s before "Meaning" (onset 193.39); "cost." ended 192.80; the roll's own close render arrives 5804
GAP_SPLIT = 5880     # 196.00: inside the "layer," / "attention" gap (195.66-196.10, floor -67 here); the tone insert sits here
GAP_FRAMES = 17      # 0.567 s + the roll's own 0.44 s = ~1.0 s
CLOSE_END = 5985     # 199.50: after the "times." sibilant (ends 199.34; floor -66 to -70 to 199.52; digital zero from 199.54, never rendered)
LD_A = DONOR_A[1] - DONOR_A[0]; LD_D = DONOR_D[1] - DONOR_D[0]

# ---- rects in each JPG's own pixels (re-measured 2026-09-23 by row/column probes; v1's rects confirmed, cards tightened to their edges)
BOX1 = (127, 818)                       # Board 1's shared white box, top and bottom rows
READS = [[80, BOX1[0], 537, BOX1[1]], [571, BOX1[0], 1028, BOX1[1]], [1062, BOX1[0], 1519, BOX1[1]]]   # columns in one white box: full height; x = the tinted label boxes' extents
B1_BANNER = [40, 858, 1560, 946]
DIAGRAM = [60, 150, 1540, 760]          # the layers picture with its NUMBERS IN / FINAL NUMBERS labels (nonwhite rows 160-749); the caption below is not ringed
CARD_START, CARD_FINAL = [70, 856, 393, 996], [1207, 856, 1530, 996]   # cards measured 74-389 / 1211-1526 x 860-992, +4 px
B2_BANNER = [40, 1060, 1560, 1148]
SENTENCE = [79, 154, 1521, 291]         # strip border measured 82-1516 x 157-287, +3 px
STAGES = [[77, 327, 355, 755], [369, 327, 647, 755], [661, 327, 939, 755], [953, 327, 1231, 755], [1245, 327, 1523, 755]]   # cards 80-352 ... 1248-1520 x 330-752, +3 px

def target(label, at, rect, color, rects=None, radius=18):
    return {"label": label, "at": at, "rects": rects if rects is not None else ([rect] if rect else []), "color": color, "radius": radius}

def speech_rms(wav, spans):
    a = readwav(wav); return rms(np.concatenate([a[round(s * SR):round(e * SR)] for s, e in spans]))

def ramp_graft_edges(b, lead_s, tail_s):
    """Blend the just-added audio-only graft's own lead-in and tail silence from/into roll 6's matched room tone over their whole
    length instead of graft()'s 5 ms butt (build_transformer_v10). Speech samples are untouched."""
    data = b.parts[-1]; bed = b.tone(len(data))
    n0 = round(lead_s * SR); r0 = np.linspace(0, 1, n0); data[:n0] = bed[:n0] * (1 - r0) + data[:n0] * r0
    n1 = round(tail_s * SR); r1 = np.linspace(1, 0, n1); data[-n1:] = bed[-n1:] * (1 - r1) + data[-n1:] * r1

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, ROLL5, ROLL2, B1, B2, B3, CLOSE, LESSON, ROOT / "index.html"]); b.tall_margin = True
    b.load_audio([(6.20, 6.60), (14.40, 14.66), (68.40, 68.68), (73.16, 73.40), (117.16, 117.36), (122.54, 122.72), (172.36, 172.56),
                  (180.86, 181.04), (195.92, 196.08), (199.36, 199.52), (22.28, 22.50), (34.00, 34.10), (91.18, 91.36), (131.50, 131.64)])

    # Level match: each donor beat against roll 6's sentences either side of it (speech RMS over the spoken words).
    for key, roll in (("horse", ROLL5), ("untangle", ROLL2)):
        w = OUT / f"graft-{key}.wav"
        if not w.exists(): subprocess.run([b.ff, "-y", "-v", "error", "-i", str(roll), "-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(w)], check=True)
    src_wav = OUT / "source.wav"
    r6_a = speech_rms(src_wav, [(5.32, 6.16), (14.72, 18.50)]); d_a = speech_rms(OUT / "graft-horse.wav", [(11.86, 14.04)])
    gain_a = round(20 * float(np.log10(r6_a / d_a)), 2)
    r6_d = speech_rms(src_wav, [(169.70, 172.32), (181.08, 185.50)]); d_d = speech_rms(OUT / "graft-untangle.wav", [(192.96, 205.78)])
    gain_d = round(20 * float(np.log10(r6_d / d_d)), 2)
    floor6_a = speech_rms(src_wav, [(6.20, 6.60), (14.40, 14.66)]); floor5 = speech_rms(OUT / "graft-horse.wav", [(11.40, 11.84), (14.16, 14.86)])
    floor6_d = speech_rms(src_wav, [(172.36, 172.56), (180.86, 181.04)]); floor2 = speech_rms(OUT / "graft-untangle.wav", [(192.60, 192.94), (206.00, 206.20)])
    db = lambda x, y: round(20 * float(np.log10(x / y)), 2)

    b.keep(0, B1_IN, "Notebook drawing: desk lamp and book (Have you ever read a passage...)")
    b.keep(B1_IN, GRAFT_A_OUT, "The Horse Raced Past the Barn Fell (canonical) arrives on the roll's cut under Try this sentence.", "1-horse")
    b.graft(ROLL5, *DONOR_A, "graft a (roll 5, audio only): The horse raced past the barn fell. + its beat; picture: Board 1", "horse",
            picture_from=GRAFT_A_IN - LD_A, gain_db=gain_a, visual="1-horse")   # leg indices stay continuous into the resume
    ramp_graft_edges(b, 0.46, 0.76)
    b.keep(GRAFT_A_IN, B1_OUT, "The Horse Raced Past the Barn Fell (canonical): First Read, More Reads, Meaning Clicks, banner", "1-horse")
    b.keep(B1_OUT, PHONE_OUT, "Notebook drawing: phone / text messaging (AI doesn't read your message the way you do)")
    b.keep(PHONE_OUT, L3D_IN, "3D stacked-layers drawing held back (covers the invented LAYER 1 diagram) under It processes your text through a series of layers...", video_from=L3D_HOLD, video_end=L3D_HOLD + 1)
    b.keep(L3D_IN, CUT_B_OUT, "Notebook drawing: 3D stacked layers (The whole stack of layers is called a neural network.)")
    # cut b: "This diagram shows how those internal layers actually update the numbers." (CUT_B_OUT..CUT_B_IN) removed
    b.keep(CUT_B_IN, B2_OUT, "How Layers Update the Numbers (canonical): whole diagram, Starting Numbers, Final Numbers, banner", "2-numbers")
    b.keep(B2_OUT, CUT_C_OUT, "Notebook drawing: The cat sat on the mat sentence (Now let's follow a single word, it...)")
    # cut c: "This chart maps out the five stages of how the AI resolves that pronoun." (CUT_C_OUT..CUT_C_IN) removed
    b.keep(CUT_C_IN, B3_OUT, "How AI Connects IT to CAT (canonical): sentence + Start, Layer 1, Layer 2, Repeat, Result", "3-it-cat")
    b.keep(B3_OUT, GRAFT_D_OUT, "Notebook drawing: stacked layers, two framings at the roll's own cut 5026 (dozens and sometimes more than 100 layers)")
    b.graft(ROLL2, *DONOR_D, "graft d (roll 2, audio only): The horse sentence took a few reads to untangle. Sarcasm... AI's layers give it more steps...; picture: stacked layers held", "untangle",
            picture_from=STACK_HOLD, gain_db=gain_d, visual="source", video_end=STACK_HOLD + 1)
    ramp_graft_edges(b, 0.29, 0.40)
    b.keep(GRAFT_D_IN, CLOSE_IN, "stacked layers held (covers the invented Depth / Optimal layer-count cards) under If more layers... worth the cost.", video_from=STACK_HOLD, video_end=STACK_HOLD + 1)
    b.mark_close_start()
    b.keep(CLOSE_IN, GAP_SPLIT, "Closing line 1: Meaning builds up, layer by layer,")
    b.pause(GAP_FRAMES, "Close gap widened (layer, / attention)")
    b.keep(GAP_SPLIT, CLOSE_END, "Closing line 2: attention and transformation, dozens of times.")
    b.pause(120, "Settled close hold")
    b.finish_audio()
    # The framework's room tone is a 0.1 s seed mirrored into a 0.2 s loop, which pulses on a long hold (transformer v10, David:
    # "strange sounds after the closing message"). Keep 0.4 s of tone after the last word's tail, then fade it to silence over 1.2 s.
    ed = readwav(b.out / "edited.wav"); hold = next(r for r in b.rows if r["label"] == "Settled close hold")
    s0 = hold["start_frame"] * SPF + int(0.4 * SR); n = int(1.2 * SR)
    ed[s0:s0 + n] *= np.linspace(1.0, 0.0, n); ed[s0 + n:] = 0.0; writewav(b.out / "edited.wav", ed)

    # Board 1 (1600x986, tall canvas): compact, still. Three reads are columns in one shared white box: full-height rings.
    b.board("1-horse", B1, B1_IN, B1_OUT, "compact", [
        target("First Read column: On the first read", 14.72, READS[0], PURPLE),
        target("More Reads column: So you read it again", 22.54, READS[1], BLUE),
        target("Meaning Clicks column: Finally, the meaning clicks", 34.22, READS[2], TEAL),
    ], banner=B1_BANNER, banner_at=47.16, push=False)
    # Board 2 (1600x1188, tall canvas): compact, still. Arrives at the resume; the whole-diagram ring pops in the full view 0.08 s later.
    # The After One Layer / After Many Layers cards are never ringed (the narration skips their values).
    b.board("2-numbers", B2, CUT_B_IN, B2_OUT, "compact", [
        target("whole diagram: Numbers go in on one side", 73.45, DIAGRAM, NEUTRAL),
        target("Starting Numbers card: We start with a pair", 91.42, CARD_START, PURPLE),
        target("Final Numbers card: finishing at .19 and negative 1.12", 100.70, CARD_FINAL, PURPLE),
    ], banner=B2_BANNER, banner_at=107.86, min_open=0, push=False)
    # Board 3 (1600x835): compact, still. No takeaway banner on this board: the verbatim "AI works out that it refers to cat" is
    # the Result card's own text, so the Result ring holds through it. One combined point at the open: the sentence strip + Start.
    b.board("3-it-cat", B3, CUT_C_IN, B3_OUT, "compact", [
        target("sentence strip + Start card (combined): At the start, the word it could refer to different things", 122.74, None, PURPLE, rects=[SENTENCE, STAGES[0]]),
        target("Layer 1 card: By layer one", 131.72, STAGES[1], PURPLE),
        target("Layer 2 card: Moving into layer two", 137.56, STAGES[2], PURPLE),
        target("Repeat card: This process repeats", 144.92, STAGES[3], PURPLE),
        target("Result card: By the result stage ... AI works out that it refers to cat", 154.66, STAGES[4], PURPLE),
    ], min_open=0, push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("layers")
    b.manifest({
        "scope_detail": "Full production review candidate from the approved 2026-09-23 plan (roll 6 base; graft a from roll 5; cuts b and c; graft d from roll 2; close gap widened); live video, rolls 2/5/6, lesson, index.html and boards unchanged.",
        "narration_changes": {
            "graft_a_replaces_source_frames": [GRAFT_A_OUT, GRAFT_A_IN], "graft_a_roll5_frames": list(DONOR_A), "graft_a_gain_db": gain_a,
            "cut_b_this_diagram_shows": [CUT_B_OUT, CUT_B_IN],
            "cut_c_this_chart_maps_out": [CUT_C_OUT, CUT_C_IN],
            "graft_d_replaces_source_frames": [GRAFT_D_OUT, GRAFT_D_IN], "graft_d_roll2_frames": list(DONOR_D), "graft_d_gain_db": gain_d,
            "speech_rms": {"roll6_neighbours_a": r6_a, "roll5_donor": d_a, "roll6_neighbours_d": r6_d, "roll2_donor": d_d},
            "pause_floor_rms": {"roll6_gaps_a": floor6_a, "roll5_gaps": floor5, "diff_a_db": db(floor5, floor6_a),
                                 "roll6_gaps_d": floor6_d, "roll2_gaps": floor2, "diff_d_db": db(floor2, floor6_d)},
            "graft_edge_ramps": "graft a: 0.46 s lead / 0.76 s tail; graft d: 0.29 s lead / 0.40 s tail blended from/into roll 6's matched room tone (ramp_graft_edges); speech untouched",
            "close_gap": {"insert_source_frame": GAP_SPLIT, "inserted_frames": GAP_FRAMES, "natural_gap_s": 0.44, "planned_total_s": 1.0},
            "close_tail": "0.4 s of tone after the times. sibilant, then a 1.2 s fade to digital silence"},
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"frames": [313, B1_OUT], "replacement": "canonical The Horse Raced Past the Barn Fell (arrives at 155, the cut to the Fell? card)"},
            {"frames": [2063, B2_OUT], "replacement": "canonical How Layers Update the Numbers (2063-2201 is inside cut b; the board runs from the resume)"},
            {"frames": [3532, B3_OUT], "replacement": "canonical How AI Connects IT to CAT (3532-3676 is inside cut c; the board runs from the resume)"},
            {"frames": [5804, "end"], "replacement": "standard close (Notebook's close render and end card never rendered)"}],
        "covered_spans": [
            {"frames": [B1_IN, 313], "what": "Fell? card (1.4 s before the graft start would have flashed)", "cover": "Board 1 arrives at the roll's cut"},
            {"frames": [PHONE_OUT, L3D_IN], "what": "blank paper drawing into the invented LAYER 1 attention/transformation diagram with [0.42, -1.15] printed", "cover": "hold of the roll's own 3D stacked-layers drawing (frame 2000), which then continues live 1957-2061"},
            {"frames": [5187, 5804], "what": "invented Simple Syntax / Complex Reasoning / 96+ Deep Layers / Depth 32 / 128+ / Optimal ~48 Layers cards", "cover": "hold of frame 5150 of the stacked-layers drawing (graft d + the why-not/cost lines) to the close"}],
        "photographs": "none (all kept spans are line drawings; sampled in kept-notebook-spans.jpg)",
        "kept_notebook_spans_source_frames": [[0, B1_IN], [B1_OUT, PHONE_OUT], [L3D_IN, CUT_B_OUT], [B2_OUT, CUT_C_OUT], [B3_OUT, GRAFT_D_OUT]],
        "held_notebook_frames": {"layers_3d": L3D_HOLD, "stacked_layers": STACK_HOLD},
        "longest_unbroken_board_run_seconds": round((B1_OUT - B1_IN - (GRAFT_A_IN - GRAFT_A_OUT) + LD_A) / FPS, 2),
        "plan_deviations": [
            "Board 1 arrives at 5.17 (the roll's cut to the Fell? card) rather than at the graft start 6.60: the Fell? card would otherwise show for 1.4 s and never return (orphan-beat rule); the board is on screen for Try this sentence. and the grafted sentence, first ring 9.6 s later.",
            "Ring onsets re-measured on the RMS profile: More Reads 22.54, Meaning Clicks 34.22, banner 47.16, whole diagram 73.45, Starting Numbers 91.42, Final Numbers 100.70, banner 107.86, Start 122.74, Layer 1 131.72, Layer 2 137.56, Repeat 144.92, Result 154.66.",
            "Board 3 has no takeaway banner; the verbatim line at 159.80 is the Result card's own text, so the Result ring holds through it.",
            "Board 3 opens with one combined ring (sentence strip + Start) at At the start; the strip and the Start card are one point there.",
            "Close board from 193.37 (the measured Meaning onset), not 192.74 (the small.en stamp ran 0.65 s early); the close gap insert is 17 frames (the natural gap measures 0.44 s, not 0.38).",
            "Whole-diagram ring on Board 2 is the neutral video purple (a whole-picture point); Board 2/3 card rings are the cards' purple accent.",
        ],
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", "gain_a", gain_a, "gain_d", gain_d, "speech r6a/r5", round(r6_a, 1), round(d_a, 1),
          "r6d/r2", round(r6_d, 1), round(d_d, 1), "floors r6a/r5", round(floor6_a, 1), round(floor5, 1), "r6d/r2", round(floor6_d, 1), round(floor2, 1), flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:40]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
