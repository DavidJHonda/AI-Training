#!/usr/bin/env python3
"""Does AI Think? from roll 2 under EDIT-SPEC.md (2026-09-13). Review only.

Base: Prompts/does-ai-think-2.mp4 (3:58, REPAIR under NARRATION-REVIEW). Output: videos/does-ai-think-v3.mp4 (v2 let nine frames of Notebook's data-center drawing flash between the comparison board and the gears; owner report 2026-09-13).
Audit: video-audit/does-ai-think-repair-2026-09-13/.
Three narration cuts: 0:44.3-0:54.0 ("The goal here is to uncouple two ideas…"), 3:29.2-3:33.5 ("resist our natural instinct
to anthropomorphize it"), and everything from 3:38.4 (roll 2's paraphrased close plus Notebook narrating the stale close-board
copy). The closing lines are roll 1's verbatim "Sounds human. Works differently. A convincing answer doesn't prove
understanding." grafted audio-only under our close board (same voice, 0.6 dB apart). Two boards, compact with rings: The
Chinese Room (uploaded; replaces Notebook's callout render; four rings, one per step callout) and When You Think / What AI Does
(faces; not uploaded; inserted over Notebook's own comparison matrix; five row rings and the banner). Six pauses at idea
boundaries. Notebook's drawings elsewhere are kept; no photographs; corner mark cleaned in render.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, GREEN, AMBER, NEUTRAL, CLOSE_TAIL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/does-ai-think-2.mp4'
SRC1 = ROOT / 'Prompts/does-ai-think-1.mp4'   # roll 1: its verbatim closing lines (2:35.9-2:41.5) become the close audio
OUT = ROOT / 'video-audit/does-ai-think-repair-2026-09-13'; DEST = ROOT / 'videos/does-ai-think-v3.mp4'
B = {k: ROOT / f'lessons/does-ai-think-{k}.jpg' for k in ('1-chinese-room', '2-side-by-side')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/does-ai-think.mp4', ROOT / 'lessons/does-ai-think.md', *B.values()])
    b.load_audio([(25.46, 25.92), (36.34, 36.70), (44.12, 44.47), (53.84, 54.12), (64.82, 65.19), (71.38, 71.75), (80.36, 80.70), (88.35, 88.96), (102.06, 102.52),
                  (127.84, 128.26), (135.20, 135.64), (145.30, 145.70), (155.52, 156.01), (164.75, 165.18), (176.31, 176.92), (189.87, 190.31), (198.82, 199.53),
                  (208.95, 209.39), (213.34, 213.69), (218.22, 218.54), (235.15, 238.47)])
    CUTA = (fr(44.3), fr(54.0))            # "The goal here is to uncouple two ideas… knows what that answer means."
    B1, B1_OUT = CUTA[1], 3077             # The Chinese Room: from "Let's picture someone locked inside a room…" (Notebook's board cut 1627) to its cut to the symbols drawing (1:42.57)
    B2, B2_OUT = fr(128.0), 5988           # When You Think / What AI Does: from "This matrix compares…" (Notebook cut 3847) to Notebook's own cut to the gears (3:19.60), so none of its data-center drawing leaks after the pause
    CUTB = (fr(209.2), fr(213.5))          # "But we have to resist our natural instinct to anthropomorphize it."
    CUTC = fr(218.4)                       # roll 2's paraphrased close and the stale close-board narration are dropped from here
    GRAFT1 = (fr(155.9), fr(161.5))        # roll 1: "Sounds human. Works differently. A convincing answer doesn't prove understanding." (silences 155.74-156.11, 161.35-164.72)
    b.keep(0, fr(25.7), 'Notebook: typing hands, cards, silhouette head'); b.pause(30, 'Pause: into sounding human')
    b.keep(fr(25.7), fr(36.5), 'Notebook: eye, poem cards, server and phone'); b.pause(30, 'Pause: into the Chinese Room')
    b.keep(fr(36.5), CUTA[0], 'Notebook: prediction engine, empty room')
    b.keep(B1, fr(102.3), 'B1 the Chinese Room, three steps, to anyone outside', '1-chinese-room'); b.pause(30, 'Pause: into what an LLM does'); b.keep(fr(102.3), B1_OUT, 'B1 tail', '1-chinese-room')
    b.keep(B1_OUT, B2, 'Notebook: symbols and prediction, OUTPUT / COMPREHENSION'); b.pause(30, 'Pause: into the comparison')
    b.keep(B2, fr(199.3), 'B2 five comparisons, banner', '2-side-by-side'); b.pause(30, 'Pause: into none of this means'); b.keep(fr(199.3), B2_OUT, 'B2 tail', '2-side-by-side')
    b.keep(B2_OUT, CUTB[0], 'Notebook: gears'); b.keep(CUTB[1], CUTC, 'Notebook: bubble, x, bulb'); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.graft(SRC1, GRAFT1[0], GRAFT1[1], 'Roll 1 audio: the closing lines, verbatim (under our close board)', 'roll1-close', picture_from=CUTC); b.pause(CLOSE_TAIL, 'Settled close hold'); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    STEPS = [[20, 30, 430, 285], [20, 290, 430, 505], [20, 515, 430, 730], [20, 740, 430, 1000]]
    ROWS = [[60, 672, 1540, 800], [60, 815, 1540, 942], [60, 958, 1540, 1085], [60, 1102, 1540, 1228], [60, 1245, 1540, 1372]]
    b.board('1-chinese-room', B['1-chinese-room'], B1, B1_OUT, 'compact',
        [T('Step 1', 65.19, STEPS[0], PURPLE), T('Step 2', 71.75, STEPS[1], PURPLE), T('Step 3', 80.70, STEPS[2], PURPLE), T('To anyone outside', 88.96, STEPS[3], NEUTRAL)], min_open=0, push=False)
    b.board('2-side-by-side', B['2-side-by-side'], B2, B2_OUT, 'compact',
        [T('Meaning', 135.64, ROWS[0], GREEN), T('Experience', 145.70, ROWS[1], GREEN), T('Word choice', 156.01, ROWS[2], GREEN), T('Beauty', 165.18, ROWS[3], GREEN), T('Uncertainty', 176.92, ROWS[4], GREEN)],
        banner_at=190.31, min_open=0, push=False)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('doesaithink')
    b.manifest({'narration_cuts_source_frames': [list(CUTA), list(CUTB), [CUTC, 7152]], 'graft_roll1_frames': list(GRAFT1)})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
