#!/usr/bin/env python3
"""Build Your Skills opener from reroll 1 under EDIT-SPEC.md (2026-09-11). Review only.

Base: Prompts/opener-build-reroll-1.mp4 (2:37). Output: videos/opener-build-v2.mp4.
Audit: video-audit/opener-build-repair-2026-09-11/.
Boards: creed (source 0-473) and section map (2151-3618), both compact, held still, rings post-crop.
Narration cuts (David-approved): 1:30.3-1:40.35 "AI cannot navigate... collaboration." replaced by a 1s pause;
everything after "The skills are yours to keep." (2:30.4) dropped. Pauses before the bike, the map, the question.
Close: standard close from the engine close's arrival cut (frame 4365).
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, banner_rect, PURPLE, BLUE, TEAL
import cv2

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/opener-build-reroll-1.mp4'
OUT = ROOT / 'video-audit/opener-build-repair-2026-09-11'; DEST = ROOT / 'videos/opener-build-v2.mp4'
CREED = ROOT / 'lessons/opener-build-1-creed.jpg'; MAP = ROOT / 'lessons/opener-build-2-map.jpg'
GOLD = '#eccf6b'   # the creed card's own accent (its label color)

# creed lines (image px, xyxy): ink bounds + 14px pad; card is x 72-1527, y 230-669
L_CHOICES, L_QUESTIONS, L_JUDGMENT, L_SKILLS, L_SMARTER = [110, 328, 386, 385], [110, 390, 423, 455], [110, 454, 420, 520], [110, 518, 329, 575], [110, 569, 809, 634]
# map rows: shared rails inset 17px from the card (x 85-1515), vertical bounds from ink + pad, clear of the dividers at y 319 / 470
ROW1, ROW2, ROW3 = [102, 139, 1498, 305], [102, 331, 1498, 455], [102, 482, 1498, 647]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/opener-build.mp4', ROOT / 'lessons/Opener-Build.md', CREED, MAP])
    b.load_audio([(25.81, 26.58), (71.11, 71.81), (90.00, 90.59), (100.03, 100.67), (126.60, 127.17), (147.19, 147.64)])
    CREED_IN, CREED_OUT = 0, 473
    P1 = fr(26.2); P2 = fr(71.4); MAP_IN = 2151; CUT_A, CUT_B = fr(90.3), fr(100.35); MAP_OUT = 3618; P3 = fr(126.9)
    CLOSE_IN = 4365; P4 = fr(147.4); CLOSE_END = fr(150.4)
    b.keep(CREED_IN, CREED_OUT, 'B1 creed', 'creed'); b.keep(CREED_OUT, P1, 'Notebook: this final section'); b.pause(30, 'Pause: into the bike')
    b.keep(P1, P2, 'Notebook: bike, balance, skating, shoes, human durability'); b.pause(30, 'Pause: into the map')
    b.keep(P2, MAP_IN, 'Notebook tail'); b.keep(MAP_IN, CUT_A, 'B2 map, parts one and two', 'map'); b.pause(30, 'Pause: into step three (replaces the cut "AI cannot" sentences)')
    b.keep(CUT_B, MAP_OUT, 'B2 map, step three and takeaway', 'map'); b.keep(MAP_OUT, P3, 'Notebook: temporary interface'); b.pause(30, 'Pause: into the question')
    b.keep(P3, CLOSE_IN, 'Notebook: the question'); b.mark_close_start()
    b.keep(CLOSE_IN, P4, 'Close: "as this graphic reminds us"', 'close'); b.pause(30, 'Pause: before the closing lines'); b.close(P4, CLOSE_END)
    b.finish_audio()
    b.board('creed', CREED, CREED_IN, CREED_OUT, 'compact', push=False, targets=[
        dict(label='Your choices', at=6.30, rects=[L_CHOICES], color=GOLD, radius=10),
        dict(label='Your questions', at=7.26, rects=[L_QUESTIONS], color=GOLD, radius=10),
        dict(label='Your judgment', at=8.96, rects=[L_JUDGMENT], color=GOLD, radius=10),
        dict(label='Your skills', at=9.92, rects=[L_SKILLS], color=GOLD, radius=10),
        dict(label='Smarter than the tool', at=12.02, rects=[L_SMARTER], color=GOLD, radius=10)])
    b.board('map', MAP, MAP_IN, MAP_OUT, 'compact', push=False, targets=[
        dict(label='1 Use AI With Skill and Care', at=75.66, rects=[ROW1], color=PURPLE),
        dict(label='2 Skills That Grow in Value', at=85.84, rects=[ROW2], color=BLUE),
        dict(label='3 Stay Flexible. Make Your Move.', at=100.80, rects=[ROW3], color=TEAL)], banner_at=114.98, banner=banner_rect(cv2.imread(str(MAP))))
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('openerskills')
    b.manifest(); print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
