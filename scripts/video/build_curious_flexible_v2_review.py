#!/usr/bin/env python3
"""Curious & Flexible from roll 2 under EDIT-SPEC.md (2026-09-12). Review only.

Base: Prompts/curious-and-flexible-2.mp4 (3:34, REPAIR under NARRATION-REVIEW; ampersand-free copy of
Prompts/curious-&-flexible-2.mp4). Output: videos/curious-and-flexible-v5.mp4 (v4's hand-off replaced by roll 1's ending, a graft with its own Adaptive System diagram, owner call 2026-09-12; v3 framed the first-row cards text-only, detector fix 2026-09-12; v2 cut the "passive filters" span and jumped board to board; owner call 2026-09-12: keep it, Notebook's sketch is the transition). Audit: video-audit/curious-and-flexible-repair-2026-09-12/.
One narration cut (3:15.9-3:25.9 "The technology we use will continue to shift… shown on screen"). Two tall 2x2 boards on the house side
bars, dense: Stay Curious arrives at its intro sentence ("This board outlines four simple habits…") and dives per habit;
Be Flexible arrives at its intro ("Finding a new tool is only the first step…") and dives per step, pulling back for
"Curiosity uncovers new possibilities…". Four pauses at idea boundaries only. Standard close; corner mark cleaned in render.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, AMBER
from build_people_skills_review import cards_grid

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/curious-and-flexible-2.mp4'
SRC1 = ROOT / 'Prompts/curious-and-flexible-1.mp4'   # roll 1: its ending (2:04.2-2:20.0) is grafted in for the hand-off
OUT = ROOT / 'video-audit/curious-and-flexible-repair-2026-09-12'; DEST = ROOT / 'videos/curious-and-flexible-v5.mp4'
B = {k: ROOT / f'lessons/curious-and-flexible-{k}.jpg' for k in ('1-stay-curious', '2-be-flexible')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/curious-and-flexible.mp4', ROOT / 'lessons/curious-and-flexible.md', *B.values()])
    b.load_audio([(28.91, 29.48), (54.49, 54.89), (112.01, 112.52), (123.17, 123.91), (195.62, 196.15), (205.56, 206.01), (211.26, 214.55)])
    B1, B1_OUT = fr(54.7), 3372            # Stay Curious: intro "This board outlines…" (Notebook cut 1644) to Notebook's own cut at 1:52.40
    B2, B2_OUT = 3718, fr(185.5)           # Be Flexible: intro "Finding a new tool is only the first step…" through "…keep your old method if it does not."
    GRAFT = (fr(124.2), fr(140.0))         # roll 1: "Look at how these elements combine… as you navigate shifting technologies." (silences 123.98-124.52, 139.74-140.14)
    CLOSE_AUDIO = fr(205.9)                # roll 2's closing lines; roll 2's 3:05.5-3:25.9 (its hand-off and the "shown on screen" beat) is dropped
    CLOSE_END = fr(212.0)                  # "…keeps changing." ends 211.2
    def open_board(key, s):
        b.keep(s, s + 1, f'{key} arrives', key); b.pause(30, f'Pause: into {key}'); return s + 1
    b.keep(0, fr(29.2), 'Notebook: basketball hook'); b.pause(30, 'Pause: into why it matters')
    b.keep(fr(29.2), B1, 'Notebook: why it matters')
    s = open_board('1-stay-curious', B1); b.keep(s, B1_OUT, 'B1 intro + four habits', '1-stay-curious')
    b.keep(B1_OUT, B2, 'Notebook: passive filters, Weekly AI Updates sketch')   # kept as the transition (owner call)
    s = open_board('2-be-flexible', B2); b.keep(s, B2_OUT, 'B2 intro + four steps', '2-be-flexible'); b.pause(30, 'Pause: into how they combine')
    b.graft(SRC1, GRAFT[0], GRAFT[1], 'Roll 1: how these elements combine (Adaptive System diagram)', 'roll1-ending'); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CLOSE_AUDIO, CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    c1 = cards_grid(B['1-stay-curious'], 4); c2 = cards_grid(B['2-be-flexible'], 4)
    b.board('1-stay-curious', B['1-stay-curious'], B1, B1_OUT, 'dense',
        [T('Use AI regularly', 65.07, c1[0], PURPLE), T('Check what changed', 77.00, c1[1], BLUE), T('Follow one reliable source', 88.19, c1[2], TEAL), T('Compare with others', 102.50, c1[3], AMBER)],
        pullback_at=111.0, min_open=0)   # whole board again for the last second before the cut into Be Flexible
    b.board('2-be-flexible', B['2-be-flexible'], B2, B2_OUT, 'dense',
        [T('Start with a real need', 136.60, c2[0], PURPLE), T('Test it on familiar work', 147.94, c2[1], BLUE), T('Compare the results', 161.15, c2[2], TEAL), T('Keep what works best', 173.60, c2[3], AMBER)],
        pullback_at=184.3, min_open=0)   # pull-back ends 185.3, board holds whole to 185.5
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('becurious')
    b.manifest({'dropped_source_frames_roll2': [B2_OUT, CLOSE_AUDIO], 'graft_roll1_frames': list(GRAFT), 'cards_detected': {'1-stay-curious': c1, '2-be-flexible': c2}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
