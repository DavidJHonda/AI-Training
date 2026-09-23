#!/usr/bin/env python3
"""Where's the Line? v2 review candidate from wheres-the-line-9-21-1 (2026-09-21 roll). Review only.

Full production pass from the best-of plan in video-audit/wheres-the-line-comparison-2026-09-23/REVIEW.md (David: "Build it",
2026-09-23). Roll 9-21-1 is the narration (7 of 7 required lines exact, every beat present). Changes:
  cuts (sentence silences): a' "This graphic summarizes the New York Times reporting, showing that DraftKings developed AI for two
      distinct purposes. First, we look at the left side," (98.40-107.20); b' "Next, we look at the right side," (122.90-124.55);
      c "This board outlines four actionable moves designed to help creators and companies make responsible choices when deploying
      AI." (153.75-160.20); d "The spinal banner says it plainly." (202.45-204.75); the roll's own 3.0 s dead air before the ethical
      question trimmed to ~1.2 s (86.60-88.40).
  audio-only grafts (same Notebook voice family; level-matched to the roll's neighbouring sentences):
      ethics <- last-2 23.00-30.55 "There's a word for this, ethics. It means thinking through what you should do and how your
      decisions affect other people." over the roll's 13.60-19.90 (which dropped "what you should do");
      struggle <- last-2 54.20-57.35 "However, some people struggle to control their gambling." inserted at 39.47 (the roll skipped
      the page's step between the casinos and the addiction sentence);
      own <- 9-21-2 181.00-191.05 "Finally, own the outcome. Monitor what happens in the real world. If the consequences warrant it,
      you must be willing to change or completely stop the system." over the roll's garbled move 4 (188.60-198.95).
  pictures: canonical Board 1 from the roll's cut to its INVESTIGATING collage (94.00) to its cut to the crown (137.83), compact,
      still; canonical Board 2 from 153.00 to the close, dense, dive card to card, pull back for the takeaway. Donor drawings cover
      the roll's bad frames: full-1's We the People parchment under the opening line (0-7.73); 9-21-2's roulette table and last-2's
      BET NOW phone under the invented-statistics slides (58.30-70.50); the roll's own phone-and-chips drawing re-timed over the
      crown emblem (137.83-141.43); full-2's keyboard-and-graph drawing over the drawn woman (149.03-153.00). Standard close;
      close hold faded to silence (Transformer v10 pattern). v2 (David 2026-09-23, "At 2:26 we need a transition"): full-2's "Making responsible choices requires four specific moves."
      (125.60-129.50) grafted, audio only, at the cut-c join between "...harming people." and "The first move..."; picture Board 2 at full view.
      Live assets, all six raw rolls, lesson, boards, index.html unchanged.
"""
from pathlib import Path
import argparse, json, subprocess, sys
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, rms, readwav, writewav, FPS, W, H, SR, SPF, NEUTRAL, PURPLE, BLUE, TEAL, GREEN, AMBER

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC = P / "wheres-the-line-9-21-1.mp4"
R9212, LAST2, FULL1, FULL2 = P / "wheres-the-line-9-21-2.mp4", P / "wheres-the-line-last-2.mp4", P / "wheres-the-line-full-1.mp4", P / "wheres-the-line-full-2.mp4"
OUT = ROOT / "video-audit/wheres-the-line-comparison-2026-09-23/build-v2"
DEST = P / "wheres-the-line-v2.mp4"
A = ROOT / "course-assets/wheres-the-line"
B1, B2, CLOSE = A / "wheres-the-line-two-uses.jpg", A / "wheres-the-line-responsible-choice.jpg", A / "wheres-the-line-close.jpg"
LESSON = ROOT / "lessons/wheres-the-line.md"
REWIND = OUT / "base-rewind.mp4"   # symlink to the roll: a second sequential reader so an EARLIER drawing can be borrowed after later frames

# ---- Roll 9-21-1 source frames. Hard cuts from scenes.txt confirmed by a per-frame diff (598, 864, 2659, 2820, 2959, 4135, 4243,
# 4471, 4620, 6080 are single-frame spikes); the first 90 s are slow same-background builds (diff < 3/frame), so covers there are
# placed by time from 1 s contact strips. Audio edges from small.en word stamps + silencedetect (-35 dB, 0.25 s).
PARCH_END = 232            # 7.73: the roll's own soft transition HUMAN AGENCY -> TASK SELECTION (215-230) completes; parchment covers 0-232
E_OUT, E_IN = 408, 597     # ethics graft: out 13.60 (after "choices." 13.24; silence 13.52-14.02) / in 19.90 (after "people." 19.34; "To" ~20.1)
PHONE_IN, REV_IN = 598, 864   # 19.93 cut to the roll's phone-and-chips drawing; 28.80 cut to its revenue-model slides
STRUG_AT = 1184            # 39.47: inside the 39.18-39.69 silence between "way." and "The challenge"
COVER_A = (1749, 1928)     # 58.30-64.27: "Metrics 2 & 3 ... +240% / -$3,450" slide -> roulette table (9-21-2)
COVER_B = (1928, 2115)     # 64.27-70.50: "AI Target Segment ... 92% Probability" slide -> BET NOW phone (last-2); the roll's email card fades in from ~71
GAP_OUT, GAP_IN = 2598, 2652   # 86.60-88.40: the roll's 3.0 s dead air (85.80-88.78) before "When should DraftKings" trimmed by 1.8 s (static Thought B slide)
POSTER_IN = 2659           # 88.63 cut to the WHERE IS THE LINE? poster (kept under the ethical question)
B1_IN = 2820               # 94.00 cut to the INVESTIGATING CORPORATE AI BOUNDARIES collage: Board 1 arrives here instead
A_OUT, A_IN = 2952, 3216   # cut a': 98.40 (after "choices." 97.98; silence 98.30-98.75) -> 107.20 (before "targeted" 107.46); the board render cut 2959 is inside
B_OUT, B_IN = 3687, 3736   # cut b': 122.90 (after "it." 122.66; silence 122.53-123.12) -> 124.55 (before "customer" 124.72)
B1_OUT = 4135              # 137.83 cut from the board render to the crown emblem
CROWN = (4135, 4243)       # crown + gibberish quote (covered by the roll's own phone-and-chips drawing, re-timed)
AUDIT = (4243, 4471)       # "Audit / Current Safety Protocols / New Algorithm Testing" poster (kept)
WOMAN_OUT = 4590           # 153.00: the drawn woman at a laptop runs 4471-4620; covered 4471-4590 by full-2's keyboard drawing, then Board 2 from 4590
B2_IN = 4590               # Board 2 opens under "...harming people." so its first ring has a 2 s+ open across cut c
C_OUT, C_IN = 4613, 4806   # cut c: 153.75 (after "people." 153.44; silence 153.59-154.07) -> 160.20 (before "The first move" 160.32); render cut 4620 inside
G_OUT, G_IN = 5658, 5969   # move-4 graft: out 188.60 (after "mistakes." 188.10; silence 188.37-189.02) / in 198.95 (after "it." 198.62; "A" 199.08)
D_OUT, D_IN = 6074, 6143   # cut d: 202.45 (after "it." 202.14; silence 202.15-202.83) -> 204.75 (before "We" 204.98); the close render cut 6080 is inside
CLOSE_END = 6284           # 209.45: after "responsibility." 209.00; the roll's silence runs 209.28-212.65
# donors (frames in their own files)
PARCH = (235, 406)         # full-1 7.83-13.53: the We the People parchment (its cuts either side)
ROULETTE = (1590, 1830)    # 9-21-2 53.00-61.00: roulette table with chips, static
BETNOW = (1183, 1370)      # last-2 39.43-45.67: BET NOW phone with chips, static
KEYBOARD = (3313, 3618)    # full-2 110.43-120.60: hand on keyboard with a rising graph, no text
PHONE = (598, 864)         # the roll's own phone-and-chips drawing (19.93-28.80), re-timed over the crown
ETHICS = (690, 917)        # last-2 23.00-30.55: 0.28 s lead, "There's a word for this, ethics. ... other people." 23.28-30.20, 0.35 s tail
STRUGGLE = (1626, 1720)    # last-2 54.20-57.35: 0.24 s lead, "However, some people struggle to control their gambling." 54.44-56.96, 0.39 s tail
TRANS = (3768, 3885)      # full-2 125.60-129.50: 0.34 s lead, "Making responsible choices requires four specific moves." 125.94-129.00, 0.50 s tail (silence 129.16-129.78)
OWN = (5430, 5731)         # 9-21-2 181.00-191.05: 0.26 s lead, "Finally, own the outcome. ... stop the system." 181.26-190.68, 0.37 s tail
LEAD = (OWN[1] - OWN[0]) - (G_IN - G_OUT)   # -10: the donor is 10 frames shorter than the roll-1 span it replaces

# ---- Board rects (image px, measured 2026-09-23 by stage-colour probes: card x-runs, last near-white row above the shadow)
# How DraftKings Uses AI (1600x967): two separate rounded cards; WHAT THEY DID sections below the divider at y=746, ringed 16 px inside.
B1_TP, B1_CP = [40, 127, 783, 917], [816, 127, 1559, 917]
B1_TP_S, B1_CP_S = [56, 762, 767, 901], [832, 762, 1543, 901]
# Making the Responsible Choice (1600x1381): four separate cards.
B2_TL, B2_TR, B2_BL, B2_BR = [40, 127, 783, 716], [815, 127, 1559, 716], [40, 750, 783, 1339], [815, 750, 1559, 1339]

def target(label, at, rect, color, cam=None, radius=18):
    d = {"label": label, "at": at, "rects": [rect] if rect else [], "color": color, "radius": radius}
    if cam: d["cam"] = cam
    return d

def active_level_db(wav, spans, frame=0.05, floor_db=-35.0):
    a = readwav(wav); n = round(frame * SR); fr_ = []
    for s, e in spans:
        x = a[round(s * SR):round(e * SR)]; x = x - x.mean()
        for k in range(len(x) // n):
            r = rms(x[k * n:(k + 1) * n])
            if 20 * np.log10(r / 32768 + 1e-12) > floor_db: fr_.append(r)
    return float(20 * np.log10(np.sqrt(np.mean(np.square(fr_))) / 32768))

def ramp_graft_edges(b, lead_s, tail_s):
    data = b.parts[-1]; bed = b.tone(len(data))
    n0 = round(lead_s * SR); r0 = np.linspace(0, 1, n0); data[:n0] = bed[:n0] * (1 - r0) + data[:n0] * r0
    n1 = round(tail_s * SR); r1 = np.linspace(1, 0, n1); data[-n1:] = bed[-n1:] * (1 - r1) + data[-n1:] * r1

def donor_wav(b, src, key):
    w = OUT / f"graft-{key}.wav"
    if not w.exists():
        subprocess.run([b.ff, "-y", "-v", "error", "-i", str(src), "-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(w)], check=True)
    return w

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[R9212, LAST2, FULL1, FULL2, B1, B2, CLOSE, LESSON, ROOT / "index.html"]); b.tall_margin = True
    if not REWIND.is_symlink(): REWIND.symlink_to(SRC)
    b.load_audio([(2.51, 2.76), (6.69, 7.25), (13.52, 14.02), (19.42, 20.11), (28.37, 28.94), (39.18, 39.69), (47.49, 48.06), (60.50, 60.87),
                  (75.35, 75.93), (86.00, 88.50), (93.62, 94.10), (98.30, 98.75), (108.41, 109.17), (122.53, 123.12), (137.30, 137.92),
                  (148.56, 149.12), (153.59, 154.07), (160.10, 160.41), (178.80, 179.32), (188.37, 189.02), (198.55, 199.23), (202.15, 202.83),
                  (204.40, 204.98), (209.30, 212.60)])
    src_wav = OUT / "source.wav"
    w_last2 = donor_wav(b, LAST2, "ethics"); w_9212 = donor_wav(b, R9212, "own"); w_full2 = donor_wav(b, FULL2, "trans")
    # Level match: each donor sentence against the roll's speech either side of its join (active 50 ms frames above -35 dBFS).
    g_ethics = round(active_level_db(src_wav, [(7.22, 13.24), (20.04, 28.04)]) - active_level_db(w_last2, [(23.28, 30.20)]), 2)
    g_strug = round(active_level_db(src_wav, [(34.20, 39.06), (39.66, 47.18)]) - active_level_db(w_last2, [(54.44, 56.96)]), 2)
    g_trans = round(active_level_db(src_wav, [(149.14, 153.44), (160.32, 170.92)]) - active_level_db(w_full2, [(125.94, 129.00)]), 2)
    g_own = round(active_level_db(src_wav, [(179.36, 188.10), (199.08, 202.14)]) - active_level_db(w_9212, [(181.26, 190.68)]), 2)

    # ---------------- timeline (source frames of roll 9-21-1)
    b.keep(0, PARCH_END, "full-1's We the People parchment under the opening line (covers the roll's blank paper and HUMAN AGENCY diagram)", video_from=PARCH[0], video_src=FULL1, video_end=PARCH[1])
    b.keep(PARCH_END, E_OUT, "Notebook drawings: TASK SELECTION & IMPACT PROPAGATION")
    b.graft(LAST2, *ETHICS, "graft ethics (last-2, audio only): There's a word for this, ethics. It means thinking through what you should do and how your decisions affect other people. Picture: the roll's ETHICS diagram, last frame held", "ethics",
            picture_from=E_OUT, gain_db=g_ethics, visual="source", video_end=PHONE_IN)
    ramp_graft_edges(b, 0.28, 0.35)
    b.keep(E_IN, STRUG_AT, "Notebook drawings: phone-and-chips (19.93), Platform Revenue Model slides")
    b.graft(LAST2, *STRUGGLE, "graft struggle (last-2, audio only): However, some people struggle to control their gambling. Picture: the roll's revenue slide held", "struggle",
            picture_from=STRUG_AT, gain_db=g_strug, visual="source", video_end=STRUG_AT + 1)
    ramp_graft_edges(b, 0.24, 0.39)
    b.keep(STRUG_AT, COVER_A[0], "Notebook drawings: Gambling Addiction impact, Digital Record & AI Behavioral Extraction (event stream, Metric 1 bars)")
    b.keep(*COVER_A, "9-21-2's roulette table over the roll's invented Metrics 2 & 3 (+240%, -$3,450) slide: the size of their bets ... a thought experiment", video_from=ROULETTE[0], video_src=R9212, video_end=ROULETTE[1])
    b.keep(*COVER_B, "last-2's BET NOW phone over the roll's invented 92% Probability slide: What if AI could predict ... trigger an email", video_from=BETNOW[0], video_src=LAST2, video_end=BETNOW[1])
    b.keep(COVER_B[1], GAP_OUT, "Notebook drawings: Place a Bet Today & Get Bonus Bets card, A Different Path banner, Thought Experiment B")
    # the roll's 3.0 s dead air before the ethical question trimmed to ~1.2 s (static slide; cut invisible)
    b.keep(GAP_IN, B1_IN, "Notebook: Thought Experiment B (last frames), WHERE IS THE LINE? poster under the ethical question")
    b.keep(B1_IN, A_OUT, "How DraftKings Uses AI (canonical) arrives under The New York Times investigated...", "uses")
    # cut a' (2952 -> 3216): "This graphic summarizes ... two distinct purposes. First, we look at the left side," removed
    b.pause(6, "splice gap after cut a' (0.2 s roll room tone; natural ~0.56 s -> ~0.76 s)")
    b.keep(A_IN, B_OUT, "How DraftKings Uses AI: Targeted Promotions card, its What They Did", "uses")
    # cut b' (3687 -> 3736): "Next, we look at the right side," removed
    b.pause(9, "splice gap after cut b' (0.3 s; natural ~0.41 s -> ~0.71 s)")
    b.keep(B_IN, B1_OUT, "How DraftKings Uses AI: Customer Protection card, its What They Did", "uses")
    b.keep(*CROWN, "the roll's own phone-and-chips drawing re-timed over the crown emblem: DraftKings disputes the claim...", video_from=PHONE[0], video_src=REWIND, video_end=PHONE[1])
    b.keep(*AUDIT, "Notebook: Audit poster (Current Safety Protocols / New Algorithm Testing) under the company's response")
    b.keep(AUDIT[1], WOMAN_OUT, "full-2's keyboard-and-graph drawing over the drawn woman: AI will do exactly what it is asked to do", video_from=KEYBOARD[0], video_src=FULL2, video_end=KEYBOARD[1])
    b.keep(B2_IN, C_OUT, "Making the Responsible Choice (canonical) opens under ...harming people.", "moves")
    # cut c (4613 -> 4806): "This board outlines four actionable moves ... when deploying AI." removed; v2: full-2's transition sentence in its place
    b.pause(6, "splice gap before the transition (0.2 s; with the roll's tail ~0.5 s)")
    b.graft(FULL2, *TRANS, "graft trans (full-2, audio only): Making responsible choices requires four specific moves. Picture: Board 2 full view", "trans",
            picture_from=C_OUT, gain_db=g_trans, visual="moves")
    ramp_graft_edges(b, 0.34, 0.50)
    b.pause(9, "breath before the first move (0.3 s; with the donor tail ~0.9 s)")
    b.keep(C_IN, G_OUT, "Making the Responsible Choice: moves 1-3", "moves")
    b.graft(R9212, *OWN, "graft own (9-21-2, audio only): Finally, own the outcome. Monitor what happens in the real world. If the consequences warrant it, you must be willing to change or completely stop the system.", "own",
            picture_from=G_OUT, gain_db=g_own, visual="moves")
    ramp_graft_edges(b, 0.26, 0.37)
    b.keep(G_IN, D_OUT, "Making the Responsible Choice: pull back for A responsible decision considers the people who live with it.", "moves", video_from=G_IN + LEAD)
    # cut d (6074 -> 6143): "The spinal banner says it plainly." removed
    b.pause(15, "breath before the close (natural ~0.54 s across the cut -> ~1.04 s)")
    b.mark_close_start()
    b.keep(D_IN, CLOSE_END, "Closing lines: We the people make the call. / What should AI do? That's our responsibility.")
    b.pause(120, "Settled close hold")
    b.finish_audio()
    # close hold: 0.4 s of tone after the last word's tail, then a 1.2 s fade to silence (removes the seed-loop pulse; Transformer v10)
    ed = readwav(b.out / "edited.wav"); hold = next(r for r in b.rows if r["label"] == "Settled close hold")
    s0 = hold["start_frame"] * SPF + int(0.4 * SR); n = int(1.2 * SR)
    ed[s0:s0 + n] *= np.linspace(1.0, 0.0, n); ed[s0 + n:] = 0.0; writewav(b.out / "edited.wav", ed)

    # ---------------- boards
    # Board 1 (1600x967): COMPACT, still (two cuts inside the span). Card text reads at full view (0.745 scale).
    b.board("uses", B1, B1_IN, B1_OUT, "compact", [
        target("Targeted Promotions card: targeted promotions", 107.46, B1_TP, PURPLE),
        target("Targeted Promotions / What They Did: As for what they did with this system", 116.55, B1_TP_S, PURPLE, radius=14),
        target("Customer Protection card: customer protection", 124.72, B1_CP, GREEN),
        target("Customer Protection / What They Did: In this case, DraftKings chose not to", 133.54, B1_CP_S, GREEN, radius=14),
    ], push=False)
    # Board 2 (1600x1381, tall): DENSE. Full view, dive to each complete card at its spoken onset (one shared dive width), pan card to
    # card, pull back for the takeaway. Move-4 onset and the pull-back are in leg time (the graft runs LEAD = -10 f against source time).
    own_at = G_OUT / FPS + (182.04 - OWN[0] / FPS)          # donor "own" 182.04 -> 1.04 s into the graft
    b.board("moves", B2, B2_IN, D_OUT + LEAD, "dense", [
        target("Consider Everyone Affected: consider everyone affected", 161.66, B2_TL, PURPLE, B2_TL),
        target("Be Clear With People: be clear with people", 172.92, B2_TR, BLUE, B2_TR),
        target("Build In Protection: build in protection", 180.42, B2_BL, TEAL, B2_BL),
        target("Own The Outcome: own the outcome (graft)", own_at, B2_BR, AMBER, B2_BR),
    ], pullback_at=199.08 + LEAD / FPS, lead_camera=True)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("wherestheline")
    b.manifest({
        "scope_detail": "Full production review candidate from the 2026-09-23 best-of plan (roll 9-21-1 base; cuts a', b', c, d + dead-air trim; audio-only grafts ethics/struggle from last-2 and own from 9-21-2; two canonical boards; four donor picture covers; four short splice gaps; standard close). Live assets, six raw rolls, lesson, boards, index.html unchanged.",
        "narration_changes": {
            "cut_a_graphic_summarizes_first_left_side": [A_OUT, A_IN], "cut_b_next_right_side": [B_OUT, B_IN], "cut_c_this_board_outlines": [C_OUT, C_IN],
            "cut_d_spinal_banner": [D_OUT, D_IN], "dead_air_trim_before_question": [GAP_OUT, GAP_IN],
            "graft_ethics": {"replaces": [E_OUT, E_IN], "last2_frames": list(ETHICS), "gain_db": g_ethics},
            "graft_struggle": {"inserted_at": STRUG_AT, "last2_frames": list(STRUGGLE), "gain_db": g_strug},
            "graft_own": {"replaces": [G_OUT, G_IN], "r9212_frames": list(OWN), "gain_db": g_own, "lead_frames": LEAD},
            "graft_trans": {"at_cut_c": [C_OUT, C_IN], "full2_frames": list(TRANS), "gain_db": g_trans},
            "splice_gaps_frames": {"after_cut_a": 6, "after_cut_b": 9, "before_trans": 6, "before_moves": 9, "before_close": 15}, "close_audio_end": CLOSE_END},
        "board_render_covered": [
            {"frames": [2959, B1_OUT], "replacement": "canonical How DraftKings Uses AI (from 2820, over the collage)"},
            {"frames": [4620, 6080], "replacement": "canonical Making the Responsible Choice (from 4590)"},
            {"frames": [6080, "end"], "replacement": "standard close"}],
        "covered_spans": [
            {"frames": [0, PARCH_END], "what": "blank paper + HUMAN AGENCY diagram", "cover": "full-1 parchment 235-406 (last frame held 61 f)"},
            {"frames": list(COVER_A), "what": "Metrics 2 & 3 slide with +240% / -$3,450", "cover": "9-21-2 roulette 1590-1769"},
            {"frames": list(COVER_B), "what": "AI Target Segment slide with 92% Probability", "cover": "last-2 BET NOW phone 1183-1370"},
            {"frames": [B1_IN, 2959], "what": "INVESTIGATING CORPORATE AI BOUNDARIES collage (invented headline)", "cover": "Board 1 arrives early"},
            {"frames": list(CROWN), "what": "crown emblem with gibberish quote (brand-adjacent)", "cover": "the roll's own phone-and-chips 598-706 via the rewind symlink"},
            {"frames": [AUDIT[1], 4620], "what": "drawn woman at a laptop (person)", "cover": "full-2 keyboard 3313-3432, then Board 2 from 4590"}],
        "kept_notebook_spans": [[PARCH_END, E_OUT], [E_IN, COVER_A[0]], [COVER_B[1], GAP_OUT], [GAP_IN, B1_IN], list(AUDIT)],
        "kept_notebook_flags": [
            "0:52-0:58 User Event Stream panel lists tiny wager amounts ($20, $100) - illegible at 1280 wide, kept",
            "1:12-1:20 the roll's own 'Place a Bet Today & Get Bonus Bets' card carries small editorial text (Outcome: Vulnerability Exploited) - kept, David may pull it",
            "1:28-1:34 WHERE IS THE LINE? poster (a chapter-card by the prompt's rule, but it is the lesson title under the ethical question) - kept",
            "2:21-2:29 Audit poster - Notebook's own reading of the company's response; labels are its own words - kept",
            "the parchment donor comes from a roll whose narration said 'to borrow a line from a famous document'; 9-21-1 says 'as creators' - the image still lands on 'we the people'"],
        "longest_board_runs_seconds": {"uses": round((B1_OUT - B1_IN - (A_IN - A_OUT) - (B_IN - B_OUT) + 15) / FPS, 1), "moves": round((D_OUT + LEAD - B2_IN - (C_IN - C_OUT) + 15 + (TRANS[1] - TRANS[0])) / FPS, 1)},
        "rewind_symlink": str(REWIND),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", "gains ethics/struggle/trans/own", g_ethics, g_strug, g_trans, g_own, "dB", "LEAD", LEAD, flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:40]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
