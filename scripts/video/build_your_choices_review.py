#!/usr/bin/env python3
"""Your Choices from roll 1 under EDIT-SPEC.md (2026-09-11). Review only.

Base: Prompts/your-choices-1.mp4 (3:12, REPAIR under NARRATION-REVIEW). Output: videos/your-choices-v3.mp4.
Audit: video-audit/your-choices-repair-2026-09-11/.
Two narration cuts (0:55.85-1:04.23 "Understanding these initial parameters…"; 2:45.25-2:54.80 "Mastering these
engine settings…"). Two boards, both compact (two cards each, legible at 720p; board 1 held still, owner call 2026-09-12; board 2 push capped so its rings stay in frame): Choose the Tool from Notebook's
own board cut carried through choice 2 and the model addition; Choose How It Works from its cut carried through
research. Rings are the whole card (image + text panel) in each card's own heading accent. Standard close from the
engine close card's arrival cut; Notebook's drawn scenes elsewhere kept; corner mark cleaned in render.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, AMBER

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/your-choices-1.mp4'
OUT = ROOT / 'video-audit/your-choices-repair-2026-09-11'; DEST = ROOT / 'videos/your-choices-v3.mp4'
B = {k: ROOT / f'lessons/your-choices-{k}.jpg' for k in ('1-choose-tool', '2-choose-how')}
# whole-card boxes (image + text panel), measured from the page assets: x 41-783 / 817-1559
CARDS1 = [[41, 127, 783, 797], [817, 127, 1559, 797]]
CARDS2 = [[41, 127, 782, 841], [817, 127, 1558, 841]]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/your-choices.mp4', ROOT / 'lessons/your-choices.md', *B.values()])
    b.load_audio([(7.83, 8.39), (38.10, 38.73), (55.57, 56.12), (63.77, 64.25), (69.16, 69.56), (86.23, 86.73), (116.06, 116.58),
                  (122.71, 123.31), (144.79, 145.36), (165.02, 165.46), (174.43, 174.81), (180.52, 181.12)])
    CUT1 = (fr(55.85), 1927)          # "Understanding these initial parameters…" through "…first prompt."; 1927 = frame before Notebook's board-1 cut (1928)
    B1, B1_OUT = 1927, 3498           # Choose the Tool through "…too weak a model." (3498 = Notebook's board-2 cut at 1:56.60)
    B2, B2_OUT = 3498, fr(165.25)     # Choose How It Works through "…many different sources."
    CUT2 = (fr(165.25), 5244)         # "Mastering these engine settings…" through "…deep analytical tool."; 5244 = frame before Notebook's close card (5245)
    CLOSE_END = fr(189.3)             # after "…the work demands more." (silence from 189.01)
    P_AI, P_AGE, P_B1, P_MODEL, P_HOW, P_B2, P_RESEARCH = fr(8.1), fr(38.4), fr(69.4), fr(86.5), fr(116.3), fr(123.0), fr(145.1)
    b.keep(0, P_AI, 'Notebook: music app'); b.pause(30, 'Pause: into AI')
    b.keep(P_AI, P_AGE, 'Notebook: four choices, default'); b.pause(30, 'Pause: into age rules')
    b.keep(P_AGE, CUT1[0], 'Notebook: age rules'); b.pause(30, 'Pause: cut 1, into board 1')
    b.keep(B1, P_B1, 'B1 arrives, intro', '1-choose-tool'); b.pause(30, 'Pause: board 1 full view')
    b.keep(P_B1, P_MODEL, 'B1 which app', '1-choose-tool'); b.pause(30, 'Pause: into which model')
    b.keep(P_MODEL, P_HOW, 'B1 which model + addition', '1-choose-tool'); b.pause(30, 'Pause: into how it works')
    b.keep(P_HOW, B1_OUT, 'B1 tail', '1-choose-tool')
    b.keep(B2, P_B2, 'B2 arrives, intro', '2-choose-how'); b.pause(30, 'Pause: board 2 full view')
    b.keep(P_B2, P_RESEARCH, 'B2 reasoning', '2-choose-how'); b.pause(30, 'Pause: into research')
    b.keep(P_RESEARCH, B2_OUT, 'B2 research', '2-choose-how'); b.pause(30, 'Pause: cut 2, into recap')
    b.mark_close_start(); b.close(CUT2[1], CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    b.board('1-choose-tool', B['1-choose-tool'], B1, B1_OUT, 'compact',
        [T('Which app', 69.60, CARDS1[0], PURPLE), T('Which model', 86.72, CARDS1[1], BLUE)], min_open=0, push=False)   # owner call 2026-09-12: no push on board 1
    b.board('2-choose-how', B['2-choose-how'], B2, B2_OUT, 'compact',
        [T('Reasoning', 123.28, CARDS2[0], TEAL), T('Research', 145.40, CARDS2[1], AMBER)], min_open=0)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('choosemodel')
    b.manifest({'narration_cuts_source_frames': [list(CUT1), list(CUT2)]})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['density'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
