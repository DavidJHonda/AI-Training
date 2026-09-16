#!/usr/bin/env python3
"""How an LLM Works from roll 2 under EDIT-SPEC.md (2026-09-13). Review only.

v5 (2026-09-16, board refresh): the v4 assembly with the current course-assets boards, which carry the site URL at the bottom (same
dimensions as the boards v4 used, so every card rect and ring onset is unchanged), and the canonical close. No audio change. Framing
kept at v4 parity (tall_margin off).
v6 (2026-09-16, David: "The Learn Once. Answer Every Word. box shows the sections… we don't refer back to it"): the Learn Once board
returns at each of the four section entries with that step ringed (01 Training purple, 02 Patterns purple, 03 Probability amber, 04
Prediction amber), riding the existing pause plus the first 1.5 s of the section's intro sentence, then the section's own board or
drawing follows; the Training and Patterns boards arrive 1.5 s later than in v5, the Probability and Prediction drawings start on their
own cuts and run 1.5 s behind the audio, clamped at their span's end. Also the 2:44 flash: the roll 1 graft's picture now holds the
pattern-architecture card (video_end=4852) instead of running 12 frames into the math-and-grammar drawing before the pause.

Base: Prompts/how-an-llm-works-2.mp4 (4:36, REPAIR under NARRATION-REVIEW). Output: Prompts/how-an-llm-works-v4.mp4 (v3 carried a garbled "architecture" at 2:33.5 source; roll 1's clean line is grafted under roll 2's own picture, owner report 2026-09-13; v2 cut to Notebook's pattern-engine drawing while it was still fading in from blank paper; owner report 2026-09-13).
Audit: video-audit/how-an-llm-works-repair-2026-09-13/.
Two narration cuts (2:41.5-2:50.93 "matching and retrieving… genuine comprehension", resuming on Notebook's chart cut;
4:16.5-4:26.4 "An LLM is not magic…", which was Notebook narrating a stale close-board copy). Four boards, all compact
with rings: What's an LLM (from frame 0, its intro is the lesson's first sentence), Learn Once (four items + banner), How
Training Works (four steps + banner), How AI Learns Patterns (two cards; leaves for Notebook's pattern-engine drawings at
its own cut). Notebook's animated odds chart and autoregressive drawings are kept. Six pauses at idea boundaries.
Standard close from the last cut; corner mark cleaned in render.
"""

try:
    from .course_asset_paths import asset_path, asset_dir
except ImportError:
    from course_asset_paths import asset_path, asset_dir

from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, GREEN, AMBER
from build_honesty_privacy_review import cards

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/how-an-llm-works-2.mp4'
SRC1 = ROOT / 'Prompts/how-an-llm-works-1.mp4'   # roll 1: its "Over billions of examples… commonly misspell words" line (1:44.2-1:54.95) replaces roll 2's garbled sentence, audio only
OUT = ROOT / 'video-audit/how-an-llm-works-repair-2026-09-16'; DEST = ROOT / 'Prompts/how-an-llm-works-v6.mp4'   # v4 shipped 2026-09-13; v5 = v4 with the URL-bearing boards; v6 = v5 + Learn Once callbacks at each section and the 2:44 flash fixed
B = {k: asset_path('lessons', f'how-an-llm-works-{k}.jpg') for k in ('1-llm', '2-learn-once', '3-training', '4-patterns')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'course-assets/how-an-llm-works/how-an-llm-works.mp4', SRC1, *B.values()])
    b.tall_margin = False   # board swap on the shipped v4: keep v4's edge-to-edge framing of the two tall boards
    b.load_audio([(6.32, 6.87), (13.26, 13.69), (17.82, 18.22), (27.65, 28.09), (36.07, 36.65), (52.66, 53.02), (61.19, 61.50), (65.39, 65.67), (76.36, 76.73), (84.33, 84.93),
                  (90.68, 91.03), (97.14, 97.66), (105.52, 105.91), (110.81, 111.17), (118.98, 119.28), (128.84, 129.41), (140.86, 141.55), (149.65, 150.27), (161.19, 161.78),
                  (170.38, 170.95), (218.58, 219.04), (256.32, 256.70), (266.20, 266.56), (272.19, 275.69)])
    B1, B1_OUT = 0, 1096                   # What's an LLM: the lesson opens on it; out at Notebook's cut to its engine drawing (0:36.53)
    B2, B2_OUT = 1408, fr(84.6)            # Learn Once: from Notebook's board cut (0:46.93) through "…every single answer it generates."
    B3, B3_OUT = fr(84.6), fr(129.1)       # How Training Works: from "We can see how the AI teaches itself…" through "…patterns it needs to function."
    B4, B4_OUT = fr(129.1), fr(150.2)      # Patterns: from "If I say peanut butter and blank…" to the silence before the garbled sentence (149.65-150.27)
    DRAWING_SOLID = fr(151.4)              # Notebook's pattern-engine drawing fades in from blank paper from 2:30.27; the graft's picture starts once it is solid
    GARBLE = (fr(150.27), fr(161.5))       # roll 2: "These learned patterns encompass the vast architecture…" ("architecture" is unintelligible); its picture stays, its sound is replaced
    GRAFT1 = (fr(104.2), fr(114.95))       # roll 1: "Over billions of examples… commonly misspell words." (silences 104.00-104.53, 114.78-115.10)
    CUTA = (fr(161.5), 5128)               # "matching and retrieving… genuine comprehension."; resumes on Notebook's chart cut (2:50.93)
    CUTB = (fr(256.5), fr(266.4))          # "An LLM is not magic… working out probabilities." (the stale close-board copy, narrated)
    CLOSE_END = fr(272.6)                  # "One word at a time." ends 272.19
    b.keep(B1, fr(36.3), 'B1 what is an LLM', '1-llm'); b.pause(30, 'Pause: into how it turns words into an answer'); b.keep(fr(36.3), B1_OUT, 'B1 tail', '1-llm')
    b.keep(B1_OUT, B2, 'Notebook: core processing engine drawing')
    CB = 45   # each callback holds 1.5 s into the section's intro sentence (plus the pause before it)
    M1 = (fr(84.4), fr(84.6), fr(86.1))     # 01 Training: ring from 0.2 s before the pause, through it, 1.5 s into "We can see how the AI teaches itself…"
    M2 = (fr(128.9), fr(129.1), fr(130.6))  # 02 Patterns: same shape into "If I say peanut butter and blank…"
    M3 = (CUTA[1] - 6, CUTA[1], CUTA[1] + CB) # 03 Probability: 6 silent roll 2 frames (170.38-170.95 is silence) before the pause, like the others, then 1.5 s into "This chart illustrates…"
    M4 = (fr(218.6), fr(218.8), fr(218.8) + CB)   # 04 Prediction: into "Probability handles one word at a time."
    b.keep(B2, M1[0], 'B2 two phases, learn once', '2-learn-once'); b.keep(M1[0], M1[1], 'Callback 01 Training (ring up before the pause)', 'map-1'); b.pause(30, 'Pause: into training (callback held)')
    b.keep(M1[1], M1[2], 'Callback 01 Training under "We can see how the AI teaches itself"', 'map-1')
    b.keep(M1[2], M2[0], 'B3 four training steps', '3-training'); b.keep(M2[0], M2[1], 'Callback 02 Patterns (ring up before the pause)', 'map-2'); b.pause(30, 'Pause: into patterns (callback held)')
    b.keep(M2[1], M2[2], 'Callback 02 Patterns under "If I say peanut butter and blank"', 'map-2')
    b.keep(M2[2], B4_OUT, 'B4 familiar pattern, patterns everywhere', '4-patterns')
    b.graft(SRC1, GRAFT1[0], GRAFT1[1], 'Roll 1 audio over roll 2 pattern-engine drawing and pattern-architecture card (replaces the garbled sentence); the card holds from 4852', 'roll1-patterns-line', picture_from=DRAWING_SOLID, video_end=4852)
    b.keep(M3[0], M3[1], 'Callback 03 Probability (ring up on 6 silent frames before the pause)', 'map-3'); b.pause(30, 'Pause: into probability (callback held)')
    b.keep(M3[1], M3[2], 'Callback 03 Probability under "This chart illustrates"', 'map-3')
    b.keep(M3[2], M4[0], 'Notebook: animated odds chart, network drawing (picture from its cut 5128, 1.5 s behind the audio, clamped)', video_from=CUTA[1], video_end=M4[0])
    b.keep(M4[0], M4[1], 'Callback 04 Prediction (ring up before the pause)', 'map-4'); b.pause(30, 'Pause: into prediction (callback held)')
    b.keep(M4[1], M4[2], 'Callback 04 Prediction under "Probability handles one word at a time"', 'map-4')
    b.keep(M4[2], CUTB[0], 'Notebook: autoregressive drawings, phone loop (picture from 218.8, 1.5 s behind the audio, clamped)', video_from=M4[1], video_end=CUTB[0]); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CUTB[1], CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    c1 = cards(B['1-llm'], 3); c4 = cards(B['4-patterns'], 2)
    LEARN = {'training': [58, 222, 652, 445], 'patterns': [58, 478, 652, 660], 'probability': [953, 222, 1547, 405], 'prediction': [953, 478, 1547, 660]}
    STEPS = [[60, 168, 400, 665], [440, 168, 780, 665], [820, 168, 1160, 665], [1200, 168, 1540, 665]]
    b.board('1-llm', B['1-llm'], B1, B1_OUT, 'compact',
        [T('Large', 6.87, c1[0], BLUE), T('Language', 13.69, c1[1], TEAL), T('Model', 18.22, c1[2], PURPLE)], banner_at=28.09, min_open=0, push=False)
    b.board('2-learn-once', B['2-learn-once'], B2, M1[0], 'compact',
        [T('01 Training', 53.02, LEARN['training'], PURPLE), T('02 Patterns', 61.50, LEARN['patterns'], PURPLE), T('03 Probability', 65.67, LEARN['probability'], AMBER), T('04 Prediction', 73.0, LEARN['prediction'], AMBER)],
        banner_at=76.73, min_open=0, push=False)
    for key, span, label, rect, col in (('map-1', M1, '01 Training', LEARN['training'], PURPLE), ('map-2', M2, '02 Patterns', LEARN['patterns'], PURPLE), ('map-3', M3, '03 Probability', LEARN['probability'], AMBER), ('map-4', M4, '04 Prediction', LEARN['prediction'], AMBER)):
        b.board(key, B['2-learn-once'], span[0], span[2], 'compact', [T(label, span[0] / 30, rect, col)], min_open=0, push=False)   # the callback: Learn Once with one step ringed from the leg's first frame
    b.board('3-training', B['3-training'], M1[2], M2[0], 'compact',
        [T('Read', 91.03, STEPS[0], PURPLE), T('Guess', 97.66, STEPS[1], BLUE), T('Check', 105.91, STEPS[2], TEAL), T('Adjust', 111.17, STEPS[3], GREEN)],
        banner_at=119.28, min_open=0, push=False)
    b.board('4-patterns', B['4-patterns'], M2[2], B4_OUT, 'compact',
        [T('One familiar pattern', M2[2] / 30, c4[0], PURPLE), T('Patterns are everywhere', 141.55, c4[1], TEAL)], min_open=0, push=False)   # the first ring pops as the board arrives (1.2 s after its onset, behind the 02 callback)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('aihistory')
    b.manifest({'narration_cuts_source_frames': [list(CUTA), list(CUTB)], 'replaced_garble_source_frames': list(GARBLE), 'graft_roll1_frames': list(GRAFT1), 'cards_detected': {'1-llm': c1, '4-patterns': c4}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
