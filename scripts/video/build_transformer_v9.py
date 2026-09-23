#!/usr/bin/env python3
"""Transformer v9 review candidate from transformer-2 (2026-09-22). Review only.

Full production pass from the approved plan in video-audit/transformer-comparison-2026-09-22/REVIEW.md ("Rolls 2 and 3"):
roll 2 is the narration (8 of 8 required lines verbatim) with two changes.
  a. graft (David approved): roll 2's 2017 beat with the wrong letter ("...called the Transformer. This is the D in ChatGPT.",
     85.16-92.84) is replaced, audio only, by roll 3's "In 2017, researchers at Google published Attention is All You Need. This
     introduced the transformer architecture, the T in ChatGPT." (67.32-76.82), level-matched by speech RMS to roll 2's neighbouring
     sentences. The picture under the whole graft is a held, settled frame of roll 2's own ChatGPT-T drawing (frame 2620), so the
     garbled-text CAT/IT card (2400-2558) never shows.
  b. cut (David leans to cutting; cut): "This diagram shows that step-by-step path." (61.78-64.34); Board 2 arrives at the resume.
Canonical boards replace Notebook's six renders at the roll's own hard cuts (all confirmed single-frame, no dissolves). Board 1 returns
after the roll's cat/IT/glass drawing (0:39-0:43), which is kept between its two spans. Four invented drawings are covered: the
RELEVANCE SCORING diagram (3118-3397, which starts as blank paper) by a re-timed hold of the roll's own cat/IT/glass drawing; MODEL
ARCHITECTURE (4045-4255) by the ACTIVE DATA drawing held back from 4255; FULL-SEQUENCE ATTENTION (5048-5238) by a hold of the
LIGHT->Brightness drawing; the CAT/IT garbled card by Board 2 (extended to the end of its verbatim line) and the graft hold. No new
pauses. Standard close from "Attention is all you need." Live video, both raw rolls, lesson, index.html, and boards unchanged.
"""
from pathlib import Path
import argparse, json, os, subprocess, sys
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, rms, readwav, banner_rect, FPS, W, H, SR, SPF, NEUTRAL, PURPLE, BLUE, TEAL, GREEN

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/transformer-2.mp4"
ROLL3 = ROOT / "Prompts/transformer-3.mp4"
LIVE = ROOT / "course-assets/transformer/transformer.mp4"     # protected, unused (v8)
OUT = ROOT / "video-audit/transformer-comparison-2026-09-22/build-v9"
DEST = ROOT / "Prompts/transformer-v9.mp4"
A = ROOT / "course-assets/transformer"
B1, B2, B3, B4, B5, B6, CLOSE = (A / "transformer-context-problems.jpg", A / "transformer-before-transformers.jpg",
                                 A / "transformer-how-transformer-reads.jpg", A / "transformer-attention-transformation.jpg",
                                 A / "transformer-resolves-meaning.jpg", A / "transformer-word-order.jpg", A / "transformer-close.jpg")
LESSON = ROOT / "lessons/transformer.md"
REWIND = OUT / "roll2-rewind.mp4"   # symlink to the roll: a second sequential reader, so a drawing from EARLIER in the roll can be
                                    # borrowed after a later hold (Build's borrowed spans from one file must be used in increasing order)

# Roll-2 source frames. Visual cuts from scenes.txt, confirmed hard by a sequential decode (single-frame spikes, zero diff either
# side); audio boundaries from the small.en word stamps corrected by a 20 ms RMS profile (sentence-start stamps ran 0.1-0.4 s off).
B1_IN = 707        # 23.57: the roll's cut from the bank/river embedding strip to its Board 1 render; "There are two problems" 23.64
CAT_IN = 1171      # 39.03: cut to the cat/IT/glass drawing (kept, 3.8 s) under "The second problem is pronouns"
B1_RET = 1286      # 42.87: cut back to the Board 1 render (zoomed), mid "the cat drank the milk because it was thirsty"
B1_OUT = 1610      # 53.67: cut to the brain + "knowledge is power" monitor drawing (kept)
CUT_OUT = 1848     # 61.60: after "time." (tail ends 61.58; the roll's own audio dips to digital zero 61.60-61.66, never rendered)
CUT_IN = 1941      # 64.70: floor before "The model moves" ("The" 64.86; the "path." tail has decayed by 64.70; no inhale blip)
B2_RENDER_IN = 1852   # 61.73: the roll's cut into its Board 2 render (inside the cut; the board arrives at CUT_IN instead)
GRAFT_OUT = 2552   # 85.07: floor after "passages." (tail ends 84.80; "In 2017" would start 85.38)
GRAFT_IN = 2803    # 93.43: the roll's cut from the ChatGPT-T drawing to its Board 3 render; floor before "The Transformer reads" (93.54)
T_HOLD = 2620      # a settled frame of the ChatGPT-T drawing (static from 2561 to 2803)
B3_OUT = 3118      # 103.93: cut from the Board 3 render to blank paper that draws into the invented RELEVANCE SCORING diagram
B4_IN = 3397       # 113.23: cut to the Board 4 render; "This process involves two steps" 113.06
IT_HOLD = 1200     # the cat/IT/glass drawing (static 1171-1286), re-timed under "Reading everything at once is only the start..."
B4_OUT = 4045      # 134.83: cut to the invented MODEL ARCHITECTURE / Weights Stay Constant drawing (never shows)
AD_HOLD = 4255     # 141.83: the roll's cut to the ACTIVE DATA drawing (static to 4404); held back over 4045-4255
B5_IN = 4404       # 146.80: cut to the Board 5 render; "In our examples" 146.90
B5_OUT = 5048      # 168.27: the roll's cut from LIGHT->Brightness to the invented FULL-SEQUENCE ATTENTION drawing; "By" 168.14
LB_HOLD = 4930     # a settled frame of the LIGHT->Brightness drawing (static 4916-5048; the live span is under Board 5)
LB_OUT = 5238      # 174.60: cut to the "Oh, fantastic" drawing (kept)
B6_IN = 5821       # 194.03: cut to the Board 6 render; "Consider dog bites man" 193.90
B6_RENDER_OUT = 6400  # 213.33: the roll's cut to its token/position drawing, as the verbatim line starts (213.22); Board 6 extends over it
CLOSE_IN = 6528    # 217.60: the standard close starts 0.02 s before "Attention is all you need." (217.62)
CLOSE_END = 6708   # 223.60: after "message." (tail ends 223.38); the roll's audio goes to digital zero at 223.66, never rendered
DONOR = (2013, 2317)   # roll 3 67.10-77.23: 0.22 s lead (a soft breath), "In 2017 ... the T in ChatGPT." 67.32-76.82, 0.41 s tail
LD = DONOR[1] - DONOR[0]

# Rects in each JPG's own pixels (measured 2026-09-22 by row/column probes: white card runs, tinted box runs, banner_rect).
# Separate cards: rings hug the card's own edges (photo tile x extent + top, last white row above the shadow for the bottom).
B1_DM, B1_PR = [40, 127, 783, 1171], [816, 127, 1560, 1171]
B1_DM_S1, B1_DM_S2 = [71, 783, 753, 902], [71, 910, 753, 1029]        # sentence boxes 74-750 x 786-899 / 913-1026, +3 px
B1_PR_S1, B1_PR_S2 = [847, 783, 1529, 902], [847, 910, 1529, 1029]    # 850-1526
B2_CHAIN = [40, 127, 1560, 517]          # the word-chain card (the white box IS the diagram; its connector runs 60-1544 wide)
B2_IT = [922, 408, 1109, 497]            # IT chip 926-1105 x 412-493, +4 px
B3_BLOCK = [383, 176, 1216, 550]         # "THE COMPLETE MESSAGE ARRIVES TOGETHER" label (546-1071 x 194-204) + chips 400-1199 x 250-532
B3_CAT, B3_IT = [534, 246, 666, 332], [696, 450, 804, 536]   # chips 538-662 x 250-328 and 700-800 x 454-532, +4 px
B4_ATT, B4_TRA = [40, 127, 783, 728], [816, 127, 1560, 728]
B5_DM, B5_PR = [40, 127, 783, 1233], [816, 127, 1560, 1233]
B5_DM_CLUE, B5_PR_CLUE = [70, 957, 754, 1216], [846, 957, 1530, 1216]   # "WHICH WORDS PROVIDE THE CLUES?" label (963-976) + box 994-1212; 16 px above the card bottom
B6_HEAD = [40, 127, 1560, 268]
B6_WITHOUT, B6_STAMPS = [40, 299, 783, 759], [816, 299, 1560, 759]

def target(label, at, rect, color, cam=None, radius=18, camera_at=None, rects=None):
    d = {"label": label, "at": at, "rects": rects if rects is not None else ([rect] if rect else []), "color": color, "radius": radius}
    if cam: d["cam"] = cam
    if camera_at: d["camera_at"] = camera_at
    return d

def speech_rms(wav, spans):
    a = readwav(wav); return rms(np.concatenate([a[round(s * SR):round(e * SR)] for s, e in spans]))

def ramp_graft_edges(b, lead_s, tail_s):
    """Blend the just-added audio-only graft's own lead-in and tail silence from/into roll 2's matched room tone over their whole
    length instead of graft()'s 5 ms butt (as build_ai_is_math_v6). Speech samples are untouched."""
    data = b.parts[-1]; bed = b.tone(len(data))
    n0 = round(lead_s * SR); r0 = np.linspace(0, 1, n0); data[:n0] = bed[:n0] * (1 - r0) + data[:n0] * r0
    n1 = round(tail_s * SR); r1 = np.linspace(1, 0, n1); data[-n1:] = bed[-n1:] * (1 - r1) + data[-n1:] * r1

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, ROLL3, B1, B2, B3, B4, B5, B6, CLOSE, LESSON, ROOT / "index.html"]); b.tall_margin = True
    if not REWIND.is_symlink(): REWIND.symlink_to(SRC)
    b.load_audio([(5.05, 5.55), (9.90, 10.40), (15.30, 15.80), (23.00, 23.50), (26.30, 26.65), (38.50, 39.00), (40.70, 41.20), (50.75, 51.15),
                  (53.20, 53.70), (61.30, 61.56), (64.62, 64.82), (79.65, 80.00), (84.85, 85.30), (93.05, 93.50), (96.15, 96.50), (103.50, 103.90),
                  (115.15, 115.50), (134.20, 134.80), (146.20, 146.75), (167.70, 168.05), (185.00, 185.50), (193.40, 193.80), (200.10, 200.50),
                  (216.90, 217.50), (223.42, 223.62)])

    # Level match: the donor beat against roll 2's sentences either side of it (speech RMS over the spoken words).
    donor_wav = OUT / "graft-t.wav"
    if not donor_wav.exists():
        subprocess.run([b.ff, "-y", "-v", "error", "-i", str(ROLL3), "-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(donor_wav)], check=True)
    r2_neighbours = speech_rms(OUT / "source.wav", [(80.10, 84.80), (93.54, 96.02)]); d_t = speech_rms(donor_wav, [(67.32, 76.82)])
    gain_t = round(20 * np.log10(r2_neighbours / d_t), 2)
    floor_r2 = speech_rms(OUT / "source.wav", [(84.85, 85.30), (93.05, 93.50)]); floor_r3 = speech_rms(donor_wav, [(66.90, 67.28), (77.00, 77.42)])

    b.keep(0, B1_IN, "Notebook drawings: laptop, The cat sat on the mat, bank/river embedding strip")
    b.keep(B1_IN, CAT_IN, "Two Problems Context Must Solve (canonical, leg 1): Different Meanings card, its two sentences", "context1")
    b.keep(CAT_IN, B1_RET, "Notebook drawing: cat / IT / glass (The second problem is pronouns)")
    b.keep(B1_RET, B1_OUT, "Two Problems Context Must Solve (canonical, leg 2): Pronouns card, its two sentences, pull back, banner", "context2")
    b.keep(B1_OUT, CUT_OUT, "Notebook drawing: brain + knowledge is power monitor (earlier AI read in a strict sequence)")
    # cut b: "This diagram shows that step-by-step path." (CUT_OUT..CUT_IN) removed; the roll's Board 2 render (from 1852) is inside it
    b.keep(CUT_IN, GRAFT_OUT, "How Earlier AI Read Text (canonical): word chain, IT chip, banner; extended over the garbled CAT/IT card to the end of the verbatim line", "earlier")
    b.graft(ROLL3, *DONOR, "graft a (roll 3, audio only): In 2017, researchers at Google published Attention is All You Need. This introduced the transformer architecture, the T in ChatGPT. Picture: roll 2's ChatGPT-T drawing held", "t",
            picture_from=T_HOLD, gain_db=gain_t, visual="source", video_end=T_HOLD + 1)
    ramp_graft_edges(b, 0.22, 0.41)
    b.keep(GRAFT_IN, B3_OUT, "How a Transformer Reads a Sentence (canonical): arrives on the roll's cut under The Transformer reads your whole message at once; sentence block, CAT + IT", "reads")
    b.keep(B3_OUT, B4_IN, "cat / IT / glass drawing re-timed (covers the invented RELEVANCE SCORING diagram) under Reading everything at once is only the start...", video_from=IT_HOLD, video_src=REWIND, video_end=IT_HOLD + 1)
    b.keep(B4_IN, B4_OUT, "How Context Changes the Numbers (canonical): Attention card, Transformation card, banner", "numbers")
    b.keep(B4_OUT, AD_HOLD, "ACTIVE DATA drawing held back (covers the invented MODEL ARCHITECTURE / Weights Stay Constant drawing) under the weights-fixed lines", video_from=AD_HOLD, video_end=AD_HOLD + 1)
    b.keep(AD_HOLD, B5_IN, "Notebook drawing: ACTIVE DATA bars (Only the row of numbers ... are being updated)")
    b.keep(B5_IN, B5_OUT, "How the Transformer Resolves Meaning (canonical): Problem 1 clue block, Problem 2 clue block, pull back, banner; extended over LIGHT->Brightness to the end of the banner line", "resolves")
    b.keep(B5_OUT, LB_OUT, "LIGHT->Brightness drawing held (covers the invented FULL-SEQUENCE ATTENTION diagram) under By identifying these connections...", video_from=LB_HOLD, video_end=LB_HOLD + 1)
    b.keep(LB_OUT, B6_IN, "Notebook drawings: Oh, fantastic / Negative Sentiment; It was a cold day; blue squares; scattered squares")
    b.keep(B6_IN, CLOSE_IN, "How a Transformer Keeps Words in Order (canonical): header, Without Position card, Position Stamps card, banner; extended over the token/position drawing", "order")
    b.mark_close_start()
    b.keep(CLOSE_IN, CLOSE_END, "Closing lines: Attention is all you need. / AI uses relationships between words to help interpret your message.")
    b.pause(120, "Settled close hold")
    b.finish_audio()

    # Board 1 (1600x1341, tall): COMPACT, still. Judged on the full-view frame (~795x667 of the 1280x720 frame): every sentence and
    # clue line reads; only the small SENTENCE 1 / LIGHT = BRIGHTNESS labels are tiny, and the narration reads the sentences aloud.
    # A complete-card dive was previewed and rejected: it reaches only 1.21x, clips the board title at the top of the frame and
    # leaves a sliver of the banner at the bottom (the tall-card caution in EDIT-SPEC 1b). Leg 1: whole Different Meanings card,
    # then its two sentences. Leg 2 returns mid-sentence with the Pronouns card's whole ring, then its sentences, then the banner.
    b.board("context1", B1, B1_IN, CAT_IN, "compact", [
        target("Different Meanings card: The first is words with multiple meanings", 26.86, B1_DM, BLUE),
        target("sentence 1: In the sentence, please turn on the light", 29.44, B1_DM_S1, BLUE),
        target("sentence 2: But in, the suitcase is light enough to carry", 33.88, B1_DM_S2, BLUE),
    ], push=False)
    b.board("context2", B1, B1_RET, B1_OUT, "compact", [
        target("Pronouns card (return, mid-sentence): the cat drank the milk because it was thirsty", B1_RET / FPS, B1_PR, GREEN),
        target("sentence 1: it refers to the cat", 44.34, B1_PR_S1, GREEN),
        target("sentence 2: If we change the sentence to, because it was fresh", 46.18, B1_PR_S2, GREEN),
    ], banner_at=51.20, min_open=0, push=False)

    # Board 2 (1600x734): compact, still.
    b.board("earlier", B2, CUT_IN, GRAFT_OUT, "compact", [
        target("word-chain card: following a single line through the entire sentence", 68.88, B2_CHAIN, PURPLE),
        target("IT chip: By the time the AI reaches the word it", 73.92, B2_IT, PURPLE),
    ], banner_at=80.10, push=False)

    # Board 3 (1600x755): compact, still; the banner (All words are present from the start) is not spoken: unmarked.
    b.board("reads", B3, GRAFT_IN, B3_OUT, "compact", [
        target("sentence block: Since every word is present from the start", 96.54, B3_BLOCK, BLUE),
        target("CAT + IT chips (combined): it can immediately pull information from cat", 99.62, None, BLUE, rects=[B3_CAT, B3_IT]),
    ], push=False)

    # Board 4 (1600x897): compact, still.
    b.board("numbers", B4, B4_IN, B4_OUT, "compact", [
        target("Attention card: First, through attention", 115.58, B4_ATT, BLUE),
        target("Transformation card: Then, through transformation", 121.92, B4_TRA, TEAL),
    ], banner_at=130.14, push=False)

    # Board 5 (1600x1403, tall): COMPACT, still (same text sizes and the same dive verdict as Board 1). The board arrives on the
    # roll's cut 1.1 s before "turn on", so the first ring pops in the full view (min_open=0); second clue block at "Thirsty".
    b.board("resolves", B5, B5_IN, B5_OUT, "compact", [
        target("Problem 1 clue block: turn on tells the AI light means brightness", 147.94, B5_DM_CLUE, BLUE),
        target("Problem 2 clue block: Thirsty describes the cat", 156.76, B5_PR_CLUE, GREEN),
    ], banner_at=163.96, min_open=0, push=False)

    # Board 6 (1600x927): compact, still. The roll's cut lands 0.13 s into "Consider", so the header rings at its own sentence,
    # "They use the exact same tokens" (4.2 s open), rather than at once.
    b.board("order", B6, B6_IN, CLOSE_IN, "compact", [
        target("header: They use the exact same tokens", 198.18, B6_HEAD, NEUTRAL),
        target("Without Position Information card: Without position information", 200.58, B6_WITHOUT, TEAL),
        target("Position Stamps Preserve Order card: To fix this, the system uses position stamps", 207.70, B6_STAMPS, PURPLE),
    ], banner_at=213.22, push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("attention")
    b.manifest({
        "scope_detail": "Full production review candidate from the approved 2026-09-22 plan (roll 2 base, graft a from roll 3, cut b); live video, both raw rolls, lesson, index.html, and boards unchanged.",
        "narration_changes": {
            "cut_b_this_diagram_shows": [CUT_OUT, CUT_IN],
            "graft_a_replaces_source_frames": [GRAFT_OUT, GRAFT_IN], "graft_a_roll3_frames": list(DONOR), "graft_a_gain_db": gain_t,
            "speech_rms": {"roll2_neighbours_80.10-84.80_93.54-96.02": r2_neighbours, "roll3_donor_67.32-76.82": d_t},
            "pause_floor_rms": {"roll2_gaps_either_side": floor_r2, "roll3_gaps_either_side": floor_r3, "difference_db": round(20 * float(np.log10(floor_r3 / floor_r2)), 2)},
            "graft_edge_ramps": "the donor's 0.22 s lead (a soft breath) and 0.41 s tail are blended from/into roll 2's matched room tone over their full length (ramp_graft_edges); speech untouched"},
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"frames": [B1_IN, CAT_IN], "replacement": "canonical Two Problems Context Must Solve (leg 1)"},
            {"frames": [B1_RET, B1_OUT], "replacement": "canonical Two Problems Context Must Solve (leg 2)"},
            {"frames": [B2_RENDER_IN, 2400], "replacement": "canonical How Earlier AI Read Text (1852-1941 is inside cut b; the board runs 1941-2552, over the garbled CAT/IT card 2400-2552)"},
            {"frames": [GRAFT_IN, B3_OUT], "replacement": "canonical How a Transformer Reads a Sentence"},
            {"frames": [B4_IN, B4_OUT], "replacement": "canonical How Context Changes the Numbers"},
            {"frames": [B5_IN, 4916], "replacement": "canonical How the Transformer Resolves Meaning (extended to 5048 over LIGHT->Brightness)"},
            {"frames": [B6_IN, B6_RENDER_OUT], "replacement": "canonical How a Transformer Keeps Words in Order (extended to 6528 over the token/position drawing)"},
            {"frames": [6533, "end"], "replacement": "standard close (Notebook's close render and end card never rendered)"}],
        "covered_spans": [
            {"frames": [2400, 2558], "what": "garbled-text CAT/IT card", "cover": "Board 2 to 2552, then the ChatGPT-T hold (graft)"},
            {"frames": [2558, GRAFT_IN], "what": "roll 2's own ChatGPT-T span under its wrong-letter beat (audio replaced)", "cover": "hold of frame 2620 of the same drawing for the graft's 304 frames"},
            {"frames": [B3_OUT, B4_IN], "what": "blank paper drawing into the invented ATTENTION: RELEVANCE SCORING diagram (weights)", "cover": "hold of the roll's cat/IT/glass drawing (frame 1200) via the rewind symlink"},
            {"frames": [B4_OUT, AD_HOLD], "what": "invented MODEL ARCHITECTURE / Weights Stay Constant drawing", "cover": "hold of the ACTIVE DATA drawing (frame 4255), which then continues live 4255-4404"},
            {"frames": [4916, B5_OUT], "what": "LIGHT->Brightness live span", "cover": "Board 5 extended through the banner line"},
            {"frames": [B5_OUT, LB_OUT], "what": "invented FULL-SEQUENCE ATTENTION diagram (weights)", "cover": "hold of the LIGHT->Brightness drawing (frame 4930)"},
            {"frames": [B6_RENDER_OUT, 6533], "what": "token/position-index drawing under the verbatim positional-encoding line", "cover": "Board 6 extended to the close"}],
        "photographs": "none seen (frame 0 is the drawn laptop; kept spans sampled in kept-notebook-spans.jpg)",
        "notebook_interleaves": [
            {"frames": [CAT_IN, B1_RET], "what": "the roll's own cat/IT/glass drawing between Board 1's two legs"},
            {"frames": [B3_OUT, B4_IN], "what": "cat/IT/glass drawing re-timed between Boards 3 and 4"}],
        "kept_notebook_spans_source_frames": [[0, B1_IN], [CAT_IN, B1_RET], [B1_OUT, CUT_OUT], [AD_HOLD, B5_IN], [LB_OUT, B6_IN]],
        "held_notebook_frames": {"chatgpt_t": T_HOLD, "cat_it_glass": IT_HOLD, "active_data": AD_HOLD, "light_brightness": LB_HOLD},
        "longest_unbroken_board_run_seconds": round((CLOSE_IN - B6_IN) / FPS, 2),
        "plan_deviations": [
            "Boards 1 and 5 are compact (still, full view) rather than dense: the complete-card dive previewed at 1.21x clipped the board title and left a banner sliver, and the full-view frame reads.",
            "Board 1: no Pronouns-card ring at 39.12; the roll's cat/IT/glass drawing (kept, 39.03-42.87) is up for 'The second problem is pronouns'. The return at 42.87 lands framed on the Pronouns card with its whole-card ring, then sentence 1 rings at 'it refers to the cat' (44.34).",
            "Board 2: the word-chain ring is at 'following a single line through the entire sentence' (68.88), not at 64.80 (the board opens at 64.70; a ring at 64.80 would open it ringed). The IT chip rings at the word 'it' (73.92).",
            "Board 3 arrives on the roll's own cut at 93.43 (under 'The Transformer reads your whole message at once'), not ~1:36: the roll cuts from the ChatGPT-T drawing to its Board 3 render at 93.43, so there is no roll-2 ChatGPT-T span left under that line; the graft hold ends there.",
            "Board 4 cover: the roll shows blank paper at 1:44 that draws into the invented diagram, so the 'It' question-mark scene the plan named (the cat/IT/glass drawing from 0:39) is re-timed under 103.93-113.23.",
            "Board 5: first ring at 'turn on' (147.94), not 146.88 ('In our examples'); the board is on screen 1.1 s before it (min_open=0), and the dive waits for the 2 s open.",
            "Board 6: header ring at 'They use the exact same tokens' (198.18), not 193.88; the roll's cut lands 0.13 s into 'Consider'.",
            "Board 5 ends at the roll's own cut at 168.27 (0.13 s into 'By'), covering LIGHT->Brightness's live span; Board 6 ends at the close start (217.60).",
            "Cut b join: the remaining gap between 'time.' and 'The model moves' is ~0.2 s (the roll's own tightest sentence gap); no room tone was added (no new pauses).",
        ],
        "rewind_symlink": str(REWIND),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", "gain_t", gain_t, "speech r2/r3", round(r2_neighbours, 1), round(d_t, 1), "floors r2/r3", round(floor_r2, 1), round(floor_r3, 1), flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:38]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
