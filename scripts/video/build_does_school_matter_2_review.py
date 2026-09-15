#!/usr/bin/env python3
"""Does School Matter? from roll 2 under EDIT-SPEC.md (2026-09-14). Review only.

Base: Prompts/does-school-matter-2.mp4 (3:09, REPAIR under NARRATION-REVIEW). Output: videos/does-school-matter-v2.mp4.
Audit: video-audit/does-school-matter-repair-2026-09-14/.
Two cuts ("But here is the friction… over the other." 0:35.2-0:45.37, resuming on Notebook's New Baseline cut; "Four key pillars
of future-proof skills." 2:20.6-2:23.7). Two boards: Same Tool. Different Advantage. (faces; not uploaded; compact, still; banner
ringed at "The tool may be identical…") over Notebook's own Luke-and-Nate diagram and Human Edge card; What to Start Building
Today (2x2, dense, dive per card, pull-back, banner). Six pauses at idea boundaries. Notebook's drawings kept elsewhere; no
photographs; standard close from the pause before the closing lines; corner mark cleaned in render.
"""

try:
    from .course_asset_paths import asset_path, asset_dir
except ImportError:
    from course_asset_paths import asset_path, asset_dir

from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, AMBER
from build_people_skills_review import cards_grid

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/does-school-matter-2.mp4'
OUT = ROOT / 'video-audit/does-school-matter-repair-2026-09-14'; DEST = ROOT / 'videos/does-school-matter-v2.mp4'
B = {k: asset_path('lessons', f'does-school-matter-{k}.jpg') for k in ('1-same-tool', '2-future')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/does-school-matter.mp4', ROOT / 'lessons/does-school-matter.md', *B.values()])
    b.load_audio([(13.10, 13.63), (34.84, 35.48), (44.78, 45.42), (53.71, 54.18), (78.34, 78.80), (91.33, 91.79), (98.37, 98.82), (135.90, 136.33), (140.51, 140.78),
                  (143.48, 143.90), (151.12, 151.69), (158.81, 159.23), (166.46, 166.86), (174.40, 174.79), (178.04, 178.37), (185.37, 188.57)])
    CUTA = (fr(35.2), 1361)                # "But here is the friction… neither of you has an advantage over the other."; resumes on Notebook's New Baseline cut (0:45.37)
    B1, B1_OUT = fr(53.9), 2962            # Same Tool: from the silence before "Let's look at two hypothetical workers…" (Notebook's diagram cut 1625) to its Individual Value cut (1:38.73)
    B2, B2_OUT = fr(136.1), fr(178.2)      # What to Start Building Today: from "This chart outlines…" (Notebook cut 4088) through "…beyond the new average."
    CUTB = (fr(140.6), fr(143.7))          # "Four key pillars of future-proof skills."
    CLOSE_END = fr(186.0)                  # "…beyond the new average." (closing) ends 185.37; Notebook's close card 5348 is replaced
    def open_board(key, s):
        b.keep(s, s + 1, f'{key} arrives', key); b.pause(30, f'Pause: into {key}'); return s + 1
    b.keep(0, fr(13.3), 'Notebook: woman at laptop, AI Core (the question)'); b.pause(30, 'Pause: into the dream job')
    b.keep(fr(13.3), CUTA[0], 'Notebook: parallel workplace diagram')
    b.keep(CUTA[1], B1, 'Notebook: New Baseline card, no unique advantage')
    s = open_board('1-same-tool', B1); b.keep(s, fr(78.5), 'B1 Luke and Nate', '1-same-tool'); b.pause(30, 'Pause: into the catch')
    b.keep(fr(78.5), fr(98.6), 'B1 the catch, the new average, the tool may be identical', '1-same-tool'); b.pause(30, 'Pause: into what sets you apart'); b.keep(fr(98.6), B1_OUT, 'B1 tail', '1-same-tool')
    b.keep(B1_OUT, B2, 'Notebook: Individual Value, Strong Skills cards, Collaboration, Dive Deep, crystals figure')
    s = open_board('2-future', B2); b.keep(s, CUTB[0], 'B2 intro', '2-future'); b.keep(CUTB[1], B2_OUT, 'B2 four things, banner', '2-future'); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(B2_OUT, CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    c4 = cards_grid(B['2-future'], 4)
    b.board('1-same-tool', B['1-same-tool'], B1, B1_OUT, 'compact', [], banner_at=91.79, min_open=0, push=False)
    b.board('2-future', B['2-future'], B2, B2_OUT, 'dense',
        [T('Deep subject knowledge', 143.90, c4[0], PURPLE), T('Strong skills', 151.69, c4[1], BLUE), T('AI fluency', 159.23, c4[2], TEAL), T('People skills', 166.86, c4[3], AMBER)],
        banner_at=174.79, pullback_at=173.5, min_open=0)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('whybother')
    b.manifest({'narration_cuts_source_frames': [list(CUTA), list(CUTB)], 'cards_detected': {'2-future': c4}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
