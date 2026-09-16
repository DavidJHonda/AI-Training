#!/usr/bin/env python3
"""What You Can Control from roll 1 under EDIT-SPEC.md (2026-09-13). Review only.

v3 (2026-09-16, board refresh): the v2 assembly with the current course-assets boards, which carry the site URL at the bottom (same
dimensions as the boards v2 used, so every row rect, card rect, and ring onset is unchanged), and the canonical close. No audio change.
Framing kept at v2 parity (tall_margin off).

Base: Prompts/what-you-can-control-1.mp4 (3:22, REPAIR under NARRATION-REVIEW). Output: Prompts/what-you-can-control-v2.mp4.
Audit: video-audit/what-you-can-control-repair-2026-09-13/.
Roll 1's garbled opening triple (0:13.1-0:31.6, "trust [unintelligible] online") is replaced, audio only, by roll 2's clean
line (0:08.4-0:20.9, +2 dB to match) under roll 1's own city and cooling-tower drawings. Two cuts of inflated asides
(1:11.3-1:22.4; 3:02.3-3:08.4). Two boards, compact and still: What's in Your Hands (ten row rings as spoken, banner) and
Three Moves Worth Your Energy (three card rings, banner). Four pauses at idea boundaries. The closing lines are the roll's
near-verbatim paraphrase, prefaced by "The cultural conversation around AI is deafening right now" (no gap to cut on).
Standard close; corner mark cleaned in render.
"""

try:
    from .course_asset_paths import asset_path, asset_dir
except ImportError:
    from course_asset_paths import asset_path, asset_dir

from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, BLUE, GREEN, PURPLE, TEAL
from build_honesty_privacy_review import cards

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/what-you-can-control-1.mp4'
SRC2 = ROOT / 'Prompts/what-you-can-control-2.mp4'
OUT = ROOT / 'video-audit/what-you-can-control-repair-2026-09-16'; DEST = ROOT / 'Prompts/what-you-can-control-v3.mp4'   # v2 shipped 2026-09-14; v3 = v2 with the URL-bearing boards
B = {k: asset_path('lessons', f'what-you-can-control-{k}.jpg') for k in ('1-hands', '2-three-moves')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'course-assets/what-you-can-control/what-you-can-control.mp4', SRC2, *B.values()])
    b.tall_margin = False   # board swap on the shipped v2: keep v2's edge-to-edge framing of the two tall boards
    b.load_audio([(12.75, 13.30), (31.31, 31.97), (41.03, 41.69), (48.89, 49.38), (70.96, 71.49), (81.94, 82.57), (86.31, 86.96), (120.27, 120.92), (131.43, 131.90),
                  (137.11, 137.62), (150.14, 150.68), (165.58, 166.11), (177.72, 178.08), (182.02, 182.41), (187.95, 188.52), (198.82, 202.20)])
    GARBLE = (fr(13.1), fr(31.6))          # roll 1: "AI is also actively shifting… trust [garble] online."
    GRAFT2 = (fr(8.4), fr(20.9))           # roll 2: "The impact extends far beyond the workplace. AI shifts who holds power, consumes vast planetary resources, and challenges the nature of what you can actually trust online."
    B1, B1_OUT = fr(41.3), 3957            # What's in Your Hands: from the silence before "So, looking at this board…" (Notebook cut 1248) to Notebook's cut to the moves board (2:11.90)
    CUT1 = (fr(71.3), fr(82.4))            # "Obsessing over these external shifts… preparing for it."
    B2, B2_OUT = 3957, fr(182.3)           # Three Moves: from "That right column is a strict to-do list…" through "…changes your outcome."
    CUT2 = (B2_OUT, fr(188.4))             # "To navigate this transition effectively… outcomes you can affect."
    CLOSE_END = fr(199.8)                  # "…decide what you do next." ends 199.06
    b.keep(0, GARBLE[0], 'Notebook: phone-scrolling crowd (hook)')
    b.graft(SRC2, GRAFT2[0], GRAFT2[1], 'Roll 2 audio: power, planet, trust online (replaces the garbled sentence) over roll 1 city drawings', 'roll2-triple', picture_from=GARBLE[0], gain_db=2.0)
    b.keep(GARBLE[1], B1, 'Notebook: nobody knows, none of it in your hands (phone in hand)')
    b.keep(B1, B1 + 1, 'B1 arrives', '1-hands'); b.pause(30, 'Pause: into the question'); b.keep(B1 + 1, CUT1[0], 'B1 the question, out of your hands', '1-hands')
    b.keep(CUT1[1], fr(131.6), 'B1 in your hands, banner, keep informed', '1-hands'); b.pause(30, 'Pause: into the to-do list'); b.keep(fr(131.6), B1_OUT, 'B1 tail', '1-hands')
    b.keep(B2, B2_OUT, 'B2 three moves, banner', '2-three-moves'); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CUT2[1], CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    ROWS = [(650, 715), (740, 805), (830, 895), (918, 1015), (1045, 1145)]; L = (60, 780); R = (820, 1540)
    out_t = [55.16, 58.44, 60.90, 64.68, 68.10]; in_t = [86.96, 91.18, 101.16, 108.00, 114.38]
    targets = [T(f'out {i+1}', out_t[i], [L[0], ROWS[i][0], L[1], ROWS[i][1]], BLUE) for i in range(5)] + [T(f'in {i+1}', in_t[i], [R[0], ROWS[i][0], R[1], ROWS[i][1]], GREEN) for i in range(5)]
    b.board('1-hands', B['1-hands'], B1, B1_OUT, 'compact', targets, banner_at=120.92, min_open=0, push=False)
    c3 = cards(B['2-three-moves'], 3)
    b.board('2-three-moves', B['2-three-moves'], B2, B2_OUT, 'compact', [T('Go deep', 137.62, c3[0], PURPLE), T('Think first', 150.68, c3[1], BLUE), T('Skip the hype', 166.11, c3[2], TEAL)], banner_at=178.08, min_open=0, push=False)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('control')
    b.manifest({'narration_cuts_source_frames': [list(CUT1), list(CUT2)], 'replaced_garble_source_frames': list(GARBLE), 'graft_roll2_frames': list(GRAFT2), 'cards_detected': {'2-three-moves': c3}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
