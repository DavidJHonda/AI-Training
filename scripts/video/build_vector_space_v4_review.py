#!/usr/bin/env python3
"""Vector Space candidate from roll 4 under EDIT-SPEC.md (2026-09-11). Review only.

Base: Prompts/vector-space-4.mp4 (or Prompts/vector-space-4-clean.mp4 if a watermark pass produced it).
Output: videos/vector-space-v3.mp4. Audit: video-audit/vector-space-repair-2026-09-11/.
Six boards from their own source cuts; Notebook scenes between them kept; seven pauses; standard close.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, banner_rect, PURPLE, BLUE, TEAL, GREEN, RED, NEUTRAL
import cv2

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/vector-space-4-clean.mp4'
if not SRC.exists(): SRC = ROOT / 'Prompts/vector-space-4.mp4'
OUT = ROOT / 'video-audit/vector-space-repair-2026-09-11'; DEST = ROOT / 'videos/vector-space-v3.mp4'
ILL = ROOT / 'illustrations'
ORANGE = '#b96108'  # the boards' own NEW POSITION / MYSTERY DRINK callout accent (sampled from the asset border)
A = dict(cities=ILL / 'vector-space-cities.jpg', closest=ILL / 'vector-space-cities-closest.jpg', taste=ILL / 'vector-space-taste-profile.jpg',
         nbhd=ILL / 'vector-space-neighborhoods.jpg', drink=ILL / 'vector-space-closest-drink.jpg', ctx=ILL / 'vector-space.jpg')

# measured geometry (image px, xyxy)
MV, NYC, DALLAS = [180, 330, 495, 425], [1025, 290, 1362, 385], [645, 500, 945, 595]
NP1, NP2 = [208, 695, 548, 790], [992, 695, 1332, 790]
ROW = [[80, 285, 1520, 459], [80, 475, 1520, 649], [80, 665, 1520, 839]]   # Coke, Pepsi, Coffee row boxes
SOFT, HOT = [165, 154, 719, 720], [940, 350, 1420, 700]
MYSTERY = [740, 205, 1270, 320]; PEPSI = [258, 255, 604, 371]; COKE = [241, 514, 604, 612]
CIT_M, CIT_P, CIT_C = [1117, 255, 1163, 305], [531, 308, 583, 364], [531, 566, 578, 616]
PLQ_START, PLQ_LAYERS, PLQ_UPD = [99, 780, 324, 858], [510, 791, 841, 839], [929, 670, 1117, 743]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/vector-space.mp4', ROOT / 'lessons/vector-space.md', *A.values()])
    b.load_audio([(24.93, 25.56), (71.42, 72.01), (116.54, 117.35), (145.54, 146.17), (181.66, 182.11), (188.98, 189.56), (216.44, 217.00)])
    # source cuts (sequential decode) and pause points (inside measured silences)
    B1, B2, B3, B4, B5, B6 = 765, 1351, 2491, 3520, 4389, 6002
    B1_OUT, B2_OUT, B3_OUT, B4_OUT, B5_OUT = 1351, 1939, 3283, 4104, 5311
    P1, P2, P3, P4, P5, P6, P7 = fr(25.2), fr(71.7), fr(116.9), fr(145.85), fr(181.9), fr(189.3), fr(216.7)
    CLOSE_END = fr(221.9)
    b.keep(0, P1, 'Notebook opening: word to numbers, layers, mapping meaning'); b.pause(30, 'Pause: into the map')
    b.keep(P1, B1, 'Notebook tail'); b.keep(B1, B1_OUT, 'B1 Three Cities', 'cities'); b.keep(B2, B2_OUT, 'B2 Closest City', 'closest')
    b.keep(B2_OUT, P2, 'Notebook: calculated gap'); b.pause(30, 'Pause: into the drinks'); b.keep(P2, B3, 'Notebook: 2D to 7D')
    b.keep(B3, B3_OUT, 'B3 Taste table', 'taste'); b.keep(B3_OUT, P3, 'Notebook: radar'); b.pause(30, 'Pause: into the similarity map')
    b.keep(P3, B4, 'Notebook tail'); b.keep(B4, B4_OUT, 'B4 Neighborhoods', 'nbhd'); b.keep(B4_OUT, P4, 'Notebook: scatter'); b.pause(30, 'Pause: into the mystery drink')
    b.keep(P4, B5, 'Notebook tail'); b.keep(B5, B5_OUT, 'B5 Closest drink', 'drink'); b.keep(B5_OUT, P5, 'Notebook: 10,000 dimensions'); b.pause(30, 'Pause: into AI scale')
    b.keep(P5, P6, 'Notebook: matrix continues'); b.pause(30, 'Pause: into the sentence'); b.keep(P6, B6, 'Notebook: sentence tokens')
    b.keep(B6, P7, 'B6 Context changes IT', 'ctx'); b.pause(30, 'Pause: before the closing message')
    b.close(P7, CLOSE_END); b.finish_audio()

    ban = {k: banner_rect(cv2.imread(str(p))) for k, p in A.items()}
    b.board('cities', A['cities'], B1, B1_OUT, 'compact',
        [dict(label='Mountain View coordinates', at=33.42, rects=[MV], color=TEAL)], banner_at=39.36, banner=ban['cities'])
    b.board('closest', A['closest'], B2, B2_OUT, 'compact',
        [dict(label='New position 1', at=47.56, rects=[NP1], color=ORANGE), dict(label='New position 2', at=50.70, rects=[NP2], color=ORANGE),
         dict(label='Position 1 is closest to Mountain View', at=60.34, rects=[NP1, MV], color=ORANGE, colors=[ORANGE, TEAL]),
         dict(label='Position 2 is closest to New York City', at=62.72, rects=[NP2, NYC], color=ORANGE, colors=[ORANGE, BLUE])])
    # (53.98–60.34 "Which of our established cities is closest? Neither matches exactly" keeps the position-2 ring: the question is about the new positions)
    b.board('taste', A['taste'], B3, B3_OUT, 'compact',
        [dict(label='A row of seven numbers is a vector (Coke row)', at=91.60, rects=[ROW[0]], color=NEUTRAL),
         dict(label='Coke and Pepsi share a profile', at=97.36, rects=[ROW[0], ROW[1]], color=NEUTRAL),
         dict(label='Coffee differs', at=104.16, rects=[ROW[2]], color=NEUTRAL)])
    b.board('nbhd', A['nbhd'], B4, B4_OUT, 'compact',
        [dict(label='Soft drinks neighborhood', at=125.28, rects=[SOFT], color=BLUE, radius=280), dict(label='Hot drinks neighborhood', at=132.22, rects=[HOT], color=PURPLE, radius=175)])
    b.board('drink', A['drink'], B5, B5_OUT, 'compact',
        [dict(label='Mystery drink ratings', at=148.30, rects=[MYSTERY], color=ORANGE),
         dict(label='First six match Pepsi', at=158.00, rects=[MYSTERY, PEPSI], color=ORANGE, colors=[ORANGE, BLUE]),
         dict(label='Citrus: 9 vs Pepsi 10', at=162.16, rects=[CIT_M, CIT_P], color=GREEN, radius=8),
         dict(label='Citrus: gap of 8 from Coke', at=169.44, rects=[CIT_M, CIT_C], color=GREEN, radius=8)], banner_at=172.10, banner=ban['drink'])
    b.board('ctx', A['ctx'], B6, P7, 'compact',
        [dict(label='Starting position numbers', at=202.20, rects=[PLQ_START], color=NEUTRAL, pad=8, radius=8),
         dict(label='The layers update the numbers', at=205.88, rects=[PLQ_LAYERS], color=NEUTRAL, pad=8, radius=8),
         dict(label='Updated position near CAT', at=211.02, rects=[PLQ_UPD], color=NEUTRAL, pad=8, radius=8)], banner_at=214.04, banner=ban['ctx'])
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('vectorspace')
    m = b.manifest(); print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['density'], v['full_view_frames']) for k, v in b.boards.items()}, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()
