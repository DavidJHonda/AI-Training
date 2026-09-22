#!/usr/bin/env python3
"""Training v6 review candidate from training-1 (2026-09-22 roll). Review only.

Full production pass from the approved plan in video-audit/training-comparison-2026-09-22/REVIEW.md (roll 1 REPAIR
PLAN a-h and BEST-OF PLAN, David approved all of it including h: accept the four-kind data list, and f: take the live
donor pair). Roll 1 is the narration (8 of 8 verbatim lines). Six of its own sentences are cut at sentence silences (v6 adds the word-for-word banner read, David 2026-09-22)
(a "This diagram shows the core training framework.", b the garbled "Dualness once is not enough.", c the mislabelled
"This panel shows the specific process of teaching a model to follow instructions.", e the two-sentence summary after
the feedback line, g "This graphic summarizes the entire development journey..."), and two beats are audio-only grafts
from the live v4 (d "Use one hand to shoot, and the other to steady the ball." under Board 6; f "When those three
phases of training conclude, the heavy lifting is done. The model is packaged up and ready for public use." under a
held FROZEN WEIGHTS drawing). Canonical boards replace Notebook's six renders at the roll's own visual cuts; three
selective pauses; standard close. The paper-craft phone photograph (rule 8c) is covered by the held drawing; the
bridge's morphing "THREE CURRICULUM PHASES" diagram is covered by a hold of the last clean FOUNDATIONAL TRAINING LOOP
frame. Live video, raw roll, lesson, boards, index.html and the registry are untouched.
"""
from pathlib import Path
import argparse, json, subprocess, sys
import cv2, numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, rms, readwav, FPS, W, H, SR, NEUTRAL, PURPLE, BLUE, TEAL, GREEN

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/training-1.mp4"
LIVE = ROOT / "course-assets/training/training.mp4"          # live v4 (2026-09-16), the donor for grafts d and f; protected
OUT = ROOT / "video-audit/training-comparison-2026-09-22/build-v6"
DEST = ROOT / "Prompts/training-v6.mp4"
A = ROOT / "course-assets/training"
LOOP, BEFORE, PHASES = A / "training-guess-check-adjust.jpg", A / "training-before-starts.jpg", A / "training-three-phases.jpg"
PRE, INST, PREF, CLOSE = A / "training-pretraining.jpg", A / "training-instruction-tuning.jpg", A / "training-preference-tuning.jpg", A / "training-close.jpg"
LESSON = ROOT / "lessons/training.md"

# ---- Roll-1 source frames. Visual cuts from scenes.txt, confirmed by a sequential decode with a per-frame diff against
# clean reference frames (all board cuts are hard cuts; the phone photograph is [8468, 8684) with no dissolve). Audio
# edges from the small.en word stamps, silencedetect (-35 dB, 0.3 s) and a 20 ms RMS profile at every edge, each cut
# placed after the preceding word's tail and before the next sentence's inhale (breath-onset rule).
P1_AT = 263               # 8.77: inside the 8.44-9.10 gap after "skills?" (no breath blip); pause +18 f
A_OUT, A_IN = 855, 948    # cut a: 28.50 (after "output." 28.20, before the soft inhale at ~28.80) -> 31.60 (before "Let's" 31.94)
LOOP_RENDER_IN = 866      # 28.87 Notebook's hard cut into its Training Loop render (inside cut a; never ships)
B_OUT, B_IN = 1825, 1899  # cut b: 60.83 (after "situation." 60.42) -> 63.30 (after the "enough." tail decays; "The" at 63.48)
BEFORE_IN = 2083          # 69.43 hard cut, Loop render -> Before Training Starts render ("This illustration shows" 69.44)
H_OUT, H_IN = 1982, 2076  # cut h (v6, David 2026-09-22): the banner read word for word, "Repeat with more examples. The patterns build." 66.34-68.72; out 66.07 after "example." (tail 65.85), in 69.20 inside the 68.89-69.46 gap before "This illustration"
BRIDGE_IN = 2662          # 88.73 hard cut to the FOUNDATIONAL TRAINING LOOP drawing ("Building the system" 88.74)
BRIDGE_HOLD = 2795        # 93.17: first frame of the morph into THREE CURRICULUM PHASES (garbled boxes); frame 2794 holds from here
C_OUT, C_IN = 2958, 3089  # cut c: 98.60 (after "phases." 98.28 + exhale tail, before the inhale at ~98.62) -> 102.97 ("We" at 103.26)
PHASES_RENDER_IN = 2962   # 98.73 Notebook's cut into its Three Phases render (inside cut c)
P2_AT = 3210              # 107.00: after the "phases." tail decays, 0.22 s before "How" 107.22; pause +18 f
PRE_IN, INST_IN, PREF_IN = 3690, 5082, 6482   # 2:03.00 / 2:49.40 / 3:36.07 hard cuts between Notebook's phase renders
D_OUT, D_IN = 7355, 7446  # graft d: roll 1 out 245.17 (after "hoop." 244.78, before the inhale at ~245.18) / in 248.20 ("Bend" ~248.5)
D_LIVE = (6411, 6525)     # live 213.70-217.50: "Use one hand to shoot, and the other to steady the ball." 213.88-217.22 (small.en)
D_TONE = 6                # 0.2 s of roll-1 room tone so the gap before "Use" matches the roll's own (~0.6 s)
E_OUT = 8028              # cut e out 267.60 (after "right." 267.30); this is also the roll's own hard cut to the summary scene
F_LIVE = (7055, 7290)     # live 235.17-243.00: "When those three phases of training conclude, the heavy lifting is done.
                          #   The model is packaged up and ready for public use." 235.38-242.70 (small.en)
F_TONE_BEFORE, F_TONE_AFTER = 6, 4
F_IN = 8676               # 289.20: roll 1 resumes before "During" 289.44 (after the "everyday use." tail)
PHOTO = (8468, 8684)      # the paper-craft phone photograph (rule 8c); inside cut e/f and the hold below
FROZEN_IN, FROZEN_SETTLED = 8684, 8750   # FROZEN WEIGHTS drawing: hard cut in at 289.47, box fades in, settled by 291.67
G_OUT, G_IN = 9114, 9285  # cut g: 303.80 (after "time." 303.42 + exhale tail) -> 309.50 ("AI" 309.74); pause +18 f before the close
CLOSE_RENDER_IN = 9124    # 304.13 Notebook's close render (inside cut g); its spinner at 9469 is never rendered
CLOSE_END = 9459          # 315.30: after "repeat." incl. the final /t/ release at 315.16-315.20; the file's digital zeros begin 315.48

# ---- Board rects (image px, measured on the JPGs 2026-09-22; see the measurement notes in REVIEW.md)
# The Training Loop (1600x1095): one white box [40,127,1560,927] with a shared caption row and the REPEAT bracket; the
# three columns are ringed as component blocks (tile x-extent +16, tile top -16, shared text-bottom rail +16), clear of
# the caption above and the bracket below.
LOOP_COLS = [[65, 236, 552, 790], [556, 236, 1043, 790], [1047, 236, 1534, 790]]
LOOP_BANNER = [40, 967, 1560, 1055]
# Before Training Starts (1600x757): two separate rounded cards; tile x-extent and top, last near-white row above the shadow.
BEFORE_CARDS = [[41, 128, 782, 715], [817, 128, 1558, 715]]
# Three Phases of Training (1600x620): the question card and three separate cards.
PHASES_Q = [40, 112, 1560, 244]
PHASES_CARDS = [[40, 272, 530, 558], [555, 272, 1045, 558], [1070, 272, 1560, 558]]
# Phase boards: three stacked bordered sections inside one white box; each ring traces the section's own border
# (accent bar at x=74 to the border at x=1526), sharing the rails.
PRE_S = [[74, 165, 1526, 467], [74, 499, 1526, 664], [74, 696, 1526, 861]]
INST_S = [[74, 165, 1526, 412], [74, 444, 1526, 650], [74, 682, 1526, 847]]
PREF_S = [[74, 165, 1526, 412], [74, 444, 1526, 691], [74, 723, 1526, 888]]
ADJUST = TEAL   # the Adjust chip/title on the board is the teal token (#0e8f86)

def target(label, at, rect, color, cam=None, radius=18):
    d = {"label": label, "at": at, "rects": [rect] if rect else [], "color": color, "radius": radius}
    if cam: d["cam"] = cam
    return d

def speech_rms(wav, spans):
    a = readwav(wav); return rms(np.concatenate([a[round(s * SR):round(e * SR)] for s, e in spans]))

def active_level_db(wav, spans, frame=0.05, floor_db=-35.0):
    """Speech level that ignores the gaps inside a span: RMS over the 50 ms frames above -35 dBFS (DC removed), in dBFS.
    Used for the graft level match because the replaced roll-1 sentences and the donors carry different pause patterns."""
    a = readwav(wav); n = round(frame * SR); fr_ = []
    for s, e in spans:
        x = a[round(s * SR):round(e * SR)]; x = x - x.mean()
        for k in range(len(x) // n):
            r = rms(x[k * n:(k + 1) * n])
            if 20 * np.log10(r / 32768 + 1e-12) > floor_db: fr_.append(r)
    return float(20 * np.log10(np.sqrt(np.mean(np.square(fr_))) / 32768))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, LOOP, BEFORE, PHASES, PRE, INST, PREF, CLOSE, LESSON]); b.tall_margin = True
    b.load_audio([(5.75, 6.30), (8.46, 9.05), (17.22, 17.88), (28.32, 28.90), (36.05, 36.70), (44.45, 45.05), (60.46, 61.02),
                  (68.90, 69.44), (148.94, 149.48), (158.83, 159.40), (203.44, 204.00), (257.76, 258.46), (267.42, 268.00),
                  (294.32, 294.76), (303.70, 304.00)])

    # Level match per graft: roll 1's own sentence against the live donor's (speech RMS; both rolls are the same Notebook voice).
    donor_wav = OUT / "graft-steady.wav"
    if not donor_wav.exists():
        subprocess.run([b.ff, "-y", "-v", "error", "-i", str(LIVE), "-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(donor_wav)], check=True)
    # Match each donor to roll 1's speech on both sides of its join (active-speech level, gaps excluded), so the grafted
    # sentence sits at the level of the sentences around it; the replaced sentences' own raw RMS is recorded alongside.
    r1_d = speech_rms(OUT / "source.wav", [(245.32, 247.84)]); rl_d = speech_rms(donor_wav, [(213.88, 217.22)])
    r1_f = speech_rms(OUT / "source.wav", [(282.28, 288.82)]); rl_f = speech_rms(donor_wav, [(235.38, 242.70)])
    lvl_d_roll = active_level_db(OUT / "source.wav", [(242.76, 244.82), (248.50, 257.70)]); lvl_d_live = active_level_db(donor_wav, [(213.88, 217.22)])
    lvl_f_roll = active_level_db(OUT / "source.wav", [(258.50, 267.30), (289.44, 303.40)]); lvl_f_live = active_level_db(donor_wav, [(235.38, 242.70)])
    gain_d = round(lvl_d_roll - lvl_d_live, 2); gain_f = round(lvl_f_roll - lvl_f_live, 2)

    # ---------------- timeline (source frames of roll 1)
    b.keep(0, P1_AT, "Notebook opening: molecule, code monitor, essay (paper-craft), chemistry question mark")
    b.pause(18, "breath before the basketball (8.44-9.10 natural 0.66 s -> ~1.26 s)")
    b.keep(P1_AT, A_OUT, "Notebook: question mark, basketball shots, Universal Training Loop and Internal Weights drawings")
    # cut a (855 -> 948): "This diagram shows the core training framework." removed; the Loop board arrives with "Let's look at one baseline training example"
    b.keep(A_IN, B_OUT, "The Training Loop: example, Guess, Check, Adjust", "loop")
    # cut b (1825 -> 1899): "Dualness once is not enough." removed (inside the board; camera still)
    b.keep(B_IN, H_OUT, "The Training Loop: the loop runs again on the next example", "loop")
    b.keep(H_IN, BEFORE_IN, "The Training Loop: last frames before the Before Training Starts cut", "loop")
    b.keep(BEFORE_IN, BRIDGE_IN, "Before Training Starts", "before")
    b.keep(BRIDGE_IN, BRIDGE_HOLD, "Notebook bridge drawing: FOUNDATIONAL TRAINING LOOP")
    b.keep(BRIDGE_HOLD, C_OUT, "hold of the FOUNDATIONAL TRAINING LOOP drawing (covers the morph into THREE CURRICULUM PHASES)", video_from=BRIDGE_HOLD - 1, video_end=BRIDGE_HOLD)
    # cut c (2958 -> 3089): "This panel shows the specific process of teaching a model to follow instructions." removed
    b.keep(C_IN, P2_AT, "Three Phases of Training: we will track a single question", "phases")
    b.pause(18, "breath before the question (106.78-107.22 natural ~0.44 s -> ~1.04 s)")
    b.keep(P2_AT, PRE_IN, "Three Phases of Training: the question and the three phases", "phases")
    b.keep(PRE_IN, INST_IN, "1 · Pretraining", "pre")
    b.keep(INST_IN, PREF_IN, "2 · Instruction Tuning", "inst")
    b.keep(PREF_IN, D_OUT, "3 · Preference Tuning: feedback, answer opens", "pref")
    b.pause(D_TONE, "splice gap before the grafted sentence (roll-1 room tone)")
    # graft d: the live v4's "Use one hand to shoot, and the other to steady the ball." over roll 1's "...study the ball."
    # The donor is 23 frames longer than the roll-1 span it replaces, so the leg picture for it starts at D_OUT and the rest of
    # the board leg runs 23 frames ahead of source time (the camera is holding the answer section throughout: invisible);
    # the leg is 23 frames longer than the source span and the third section's onset is entered in leg time (+23 f).
    b.graft(LIVE, D_LIVE[0], D_LIVE[1], "graft d (live v4): Use one hand to shoot, and the other to steady the ball.", "steady", picture_from=D_OUT, gain_db=gain_d, visual="pref")
    LEAD = (D_LIVE[1] - D_LIVE[0]) - (D_IN - D_OUT)
    b.keep(D_IN, E_OUT, "3 · Preference Tuning: rest of the answer, what still needs work, feedback line", "pref", video_from=D_IN + LEAD)
    # cut e (8028 -> 8676) removes the summary and roll 1's own "architecture is locked" sentence; graft f carries the live beat instead
    b.pause(F_TONE_BEFORE, "splice gap before graft f (roll-1 room tone)")
    b.graft(LIVE, F_LIVE[0], F_LIVE[1], "graft f (live v4): When those three phases of training conclude... ready for public use.", "ready", picture_from=FROZEN_SETTLED, gain_db=gain_f, video_end=FROZEN_SETTLED + 1)
    b.pause(F_TONE_AFTER, "splice gap after graft f (roll-1 room tone)")
    b.keep(F_IN, FROZEN_SETTLED, "During a normal chat (FROZEN WEIGHTS settled frame held; covers the photograph's last frames and the box fade-in)", video_from=FROZEN_SETTLED, video_end=FROZEN_SETTLED + 1)
    b.keep(FROZEN_SETTLED, G_OUT, "Notebook FROZEN WEIGHTS drawing: weights lines, real-time line")
    # cut g (9114 -> 9285): "This graphic summarizes the entire development journey..." removed
    b.pause(18, "breath before the close (natural ~0.62 s across the cut -> ~1.22 s)")
    b.mark_close_start()
    b.close(G_IN, CLOSE_END, tail=120)
    b.finish_audio()

    # ---------------- boards
    # The Training Loop: compact, still (cut b inside the span). Column rings at "Step one/two/three", banner at "Repeat with more examples."
    b.board("loop", LOOP, A_IN, BEFORE_IN, "compact", [
        target("Guess", 36.76, LOOP_COLS[0], PURPLE),
        target("Check", 45.22, LOOP_COLS[1], BLUE),
        target("Adjust", 52.54, LOOP_COLS[2], ADJUST),
        target("unmarked: the loop runs again (banner read cut in v6)", 63.50, None, NEUTRAL),
    ], push=False)
    # Before Training Starts: compact at full view; two card rings.
    b.board("before", BEFORE, BEFORE_IN, BRIDGE_IN, "compact", [
        target("Set Up the System", 74.30, BEFORE_CARDS[0], PURPLE),
        target("Gather the Data", 80.56, BEFORE_CARDS[1], BLUE),
    ])
    # Three Phases of Training: compact, still (pause inside). Question ring, then the three cards as each phase is named.
    b.board("phases", PHASES, C_IN, PRE_IN, "compact", [
        target("The Same Question: How do I shoot a basketball?", 107.18, PHASES_Q, NEUTRAL, radius=22),
        target("1 Pretraining", 110.16, PHASES_CARDS[0], PURPLE),
        target("2 Instruction Tuning", 113.48, PHASES_CARDS[1], BLUE),
        target("3 Preference Tuning", 118.16, PHASES_CARDS[2], GREEN),
    ], push=False)
    # Phase boards: dense; dive to each stacked section at its spoken onset (per-target camera, arriving on the onset). No pull-back.
    b.board("pre", PRE, PRE_IN, INST_IN, "dense", [
        target("Learn from Vast Amounts of Data", 126.86, PRE_S[0], PURPLE, PRE_S[0]),      # "learns from vast amounts of text and code"
        target("What an Answer Might Look Like", 149.50, PRE_S[1], PURPLE, PRE_S[1]),       # "After pre-training, an answer... might look like this"
        target("What Still Needs Work", 159.36, PRE_S[2], PURPLE, PRE_S[2]),                # "The model successfully produces fluent... but"
    ], per_target_camera=True, lead_camera=True)
    b.board("inst", INST, INST_IN, PREF_IN, "dense", [
        target("Learn to Follow Instructions", 172.68, INST_S[0], BLUE, INST_S[0]),          # "Here the objective shifts entirely to teaching the model"
        target("What an Answer Might Look Like", 193.58, INST_S[1], BLUE, INST_S[1]),       # "After instruction tuning, the model's answer evolves"
        target("What Still Needs Work", 204.00, INST_S[2], BLUE, INST_S[2]),                # "The AI now successfully follows the format"
    ], per_target_camera=True, lead_camera=True)
    b.board("pref", PREF, PREF_IN, E_OUT + LEAD, "dense", [
        target("Learn from Feedback", 218.92, PREF_S[0], GREEN, PREF_S[0]),                 # "In this final stage, the model learns to prioritize"
        target("What an Answer Might Look Like", 238.64, PREF_S[1], GREEN, PREF_S[1]),      # "After preference tuning, the output is polished"
        target("What Still Needs Work", 258.50 + LEAD / FPS, PREF_S[2], GREEN, PREF_S[2]),  # "Despite this rigorous polishing" 258.50 spoken; +LEAD f in leg time
    ], per_target_camera=True, lead_camera=True)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("training")
    rows = b.rows
    run_start = next(r for r in rows if r.get("visual") == "phases")["start_frame"]
    run_end = next(r for r in rows if "graft f" in r["label"])["start_frame"] - F_TONE_BEFORE
    b.manifest({
        "scope_detail": "Full production review candidate from the approved 2026-09-22 plan (roll 1 base; cuts a, b, c, e, g; audio-only grafts d and f from the live v4; six canonical boards; three selective pauses; standard close). Live video, raw roll, lesson, boards, index.html and the registry unchanged.",
        "narration_changes": {
            "cut_a_diagram_shows": [A_OUT, A_IN], "cut_b_dualness": [B_OUT, B_IN], "cut_h_banner_read_v6": [H_OUT, H_IN], "cut_c_this_panel_shows": [C_OUT, C_IN],
            "graft_d_replaces_roll1_frames": [D_OUT, D_IN], "graft_d_live_frames": list(D_LIVE), "graft_d_gain_db": gain_d,
            "speech_rms_roll1_steady_sentence": r1_d, "speech_rms_live_steady_sentence": rl_d,
            "active_level_dbfs_roll1_neighbours_d": round(lvl_d_roll, 2), "active_level_dbfs_live_d": round(lvl_d_live, 2),
            "active_level_dbfs_roll1_neighbours_f": round(lvl_f_roll, 2), "active_level_dbfs_live_f": round(lvl_f_live, 2),
            "cut_e_summary_and_architecture_locked": [E_OUT, F_IN], "graft_f_live_frames": list(F_LIVE), "graft_f_gain_db": gain_f,
            "speech_rms_roll1_ready_sentence": r1_f, "speech_rms_live_ready_pair": rl_f,
            "cut_g_this_graphic_summarizes": [G_OUT, G_IN], "close_audio_end": CLOSE_END,
            "splice_gaps_roll1_room_tone_frames": {"before_graft_d": D_TONE, "before_graft_f": F_TONE_BEFORE, "after_graft_f": F_TONE_AFTER}},
        "added_teaching_pauses": [
            {"at_source_frame": P1_AT, "frames": 18, "why": "before 'Think about learning to shoot a basketball'"},
            {"at_source_frame": P2_AT, "frames": 18, "why": "before 'How do I shoot a basketball?'"},
            {"after_source_frame": G_OUT, "frames": 18, "why": "before the close"}],
        "board_render_covered": [
            {"frames": [LOOP_RENDER_IN, BEFORE_IN], "replacement": "canonical The Training Loop (from the cut-a resume at 948)"},
            {"frames": [BEFORE_IN, BRIDGE_IN], "replacement": "canonical Before Training Starts"},
            {"frames": [PHASES_RENDER_IN, PRE_IN], "replacement": "canonical Three Phases of Training (from the cut-c resume at 3089)"},
            {"frames": [PRE_IN, INST_IN], "replacement": "canonical 1 · Pretraining"}, {"frames": [INST_IN, PREF_IN], "replacement": "canonical 2 · Instruction Tuning"},
            {"frames": [PREF_IN, E_OUT], "replacement": "canonical 3 · Preference Tuning"}, {"frames": [CLOSE_RENDER_IN, "end"], "replacement": "standard close"}],
        "photographs_and_covers": [
            {"frames": list(PHOTO), "what": "paper-craft phone photograph (rule 8c) under the old 'deployed for everyday use' / 'During a normal chat'",
             "handling": f"frames {E_OUT}-{F_IN} are inside cut e/f; {F_IN}-{FROZEN_SETTLED} (the photograph's last 8 frames and the box fade-in) are covered by the held FROZEN WEIGHTS frame {FROZEN_SETTLED}, which also sits under graft f"},
            {"frames": [BRIDGE_HOLD, C_OUT], "what": "morph into the invented THREE CURRICULUM PHASES diagram (garbled boxes from 2795)", "handling": f"hold of frame {BRIDGE_HOLD - 1} (FOUNDATIONAL TRAINING LOOP) through cut c"},
            {"frames": [E_OUT, PHOTO[0]], "what": "AI TRAINING CURRICULUM / TRANSFORMATION invented diagrams", "handling": "inside cut e"}],
        "notebook_spans_kept": [
            {"source_frames": [0, 268], "what": "paper-craft molecule (frame 0), code monitor, highlighted essay, chemistry question mark", "note": "the first three are the same photographed-paper-craft style as the covered phone; David may pull them"},
            {"source_frames": [268, A_OUT], "what": "basketball shots, then Notebook's invented 'Universal Training Loop' (~0:20) and 'Internal Weights' (~0:24-0:28.5) drawings, both dissolves", "note": "kept per plan; David may pull them"},
            {"source_frames": [BRIDGE_IN, C_OUT], "what": "FOUNDATIONAL TRAINING LOOP drawing (held from 2795)"},
            {"source_frames": [FROZEN_SETTLED, G_OUT], "what": "FROZEN WEIGHTS drawing, its build-up in sync with the weights lines (settled frame also held under graft f)"}],
        "notebook_interleaves": [],
        "pref_leg_lead_frames_after_graft_d": LEAD,
        "longest_unbroken_board_run": {"boards": "Three Phases -> Pretraining -> Instruction Tuning -> Preference Tuning", "output_frames": [run_start, run_end], "seconds": round((run_end - run_start) / FPS, 2),
                                       "note": "roll 1 drew nothing between these boards (its renders cut straight into one another), so there is no Notebook scene to interleave without inventing filler"},
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", "gains d/f", gain_d, gain_f, "dB", "LEAD", LEAD, flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:48]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()
