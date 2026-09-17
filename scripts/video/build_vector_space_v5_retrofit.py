#!/usr/bin/env python3
"""Vector Space v5: the current course boards and the canonical close, as a visual-only retrofit of the shipped v3 (2026-09-17). Review only.

The shipped file (course-assets/vector-space/vector-space.mp4, 6987 frames) is the roll-4 candidate of 2026-09-10/11
(build_vector_space_v4_review.py: six boards as ken_burns_path legs with rings, seven pauses, standard close). Roll 4 no longer exists,
so this build takes the finished file as its picture source, re-renders the six board legs from the current course-assets JPGs with the
shipped script's exact board definitions (same source cuts, density, ring targets and onsets, banner rects re-measured on the current
files; `tall_margin = False` so the framing matches the pre-2026-09-14 stage), splices each leg over its span of the output timeline,
replaces the close with the canonical closing JPG (make_close_board.py --lesson vectorspace), and muxes the shipped audio stream back
in untouched. Every Notebook span is the shipped picture. The shipped timeline (roll-4 frames -> output frames) is replayed with the
same keep/pause calls so every leg lands where it did.
"""
from pathlib import Path
import argparse, subprocess, sys, hashlib, json
import numpy as np, cv2, imageio_ffmpeg
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, Reader, fr, banner_rect, sha, PURPLE, BLUE, TEAL, GREEN, NEUTRAL, CLOSE_PREHOLD, CLOSE_PUSH, W, H, FPS, SPF
from make_close_board import close_board_copy

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/vector-space/vector-space.mp4'
OUT = ROOT / 'video-audit/vector-space-repair-2026-09-17'
DEST = ROOT / 'Prompts/vector-space-v5.mp4'
D = ROOT / 'course-assets/vector-space'
A = dict(cities=D / 'vector-space-cities.jpg', closest=D / 'vector-space-cities-closest.jpg', taste=D / 'vector-space-taste.jpg',
         nbhd=D / 'vector-space-neighborhoods.jpg', drink=D / 'vector-space-closest-drink.jpg', ctx=D / 'vector-space-meaning-map.jpg')
ORANGE = '#b96108'
# the shipped script's measured geometry (image px, xyxy); boards share the old dimensions
MV, NYC, DALLAS = [180, 330, 495, 425], [1025, 290, 1362, 385], [645, 500, 945, 595]
NP1, NP2 = [208, 695, 548, 790], [992, 695, 1332, 790]
ROW = [[80, 285, 1520, 459], [80, 475, 1520, 649], [80, 665, 1520, 839]]
SOFT, HOT = [165, 154, 719, 720], [940, 350, 1420, 700]
MYSTERY = [740, 205, 1270, 320]; PEPSI = [258, 255, 604, 371]; COKE = [241, 514, 604, 612]
CIT_M, CIT_P, CIT_C = [1117, 255, 1163, 305], [531, 308, 583, 364], [531, 566, 578, 616]
PLQ_START, PLQ_LAYERS, PLQ_UPD = [99, 780, 324, 858], [510, 791, 841, 839], [929, 670, 1117, 743]
B1, B2, B3, B4, B5, B6 = 765, 1351, 2491, 3520, 4389, 6002
B1_OUT, B2_OUT, B3_OUT, B4_OUT, B5_OUT = 1351, 1939, 3283, 4104, 5311
P1, P2, P3, P4, P5, P6, P7 = fr(25.2), fr(71.7), fr(116.9), fr(145.85), fr(181.9), fr(189.3), fr(216.7)
CLOSE_END = fr(221.9)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, LIVE, OUT, DEST, protected=[ROOT / 'lessons/vector-space.md', D / 'vector-space-close.jpg', ROOT / 'index.html', *A.values()])
    b.tall_margin = False   # framing parity with the 2026-09-10 ship (the 4% tall-board stage margin postdates it)
    assert close_board_copy('vectorspace')[0]
    # replay the shipped timeline for the output-frame mapping only (audio is copied from the shipped file at mux)
    b.audio = np.zeros(CLOSE_END * SPF + SPF); b.loop = np.zeros(2 * 4800)
    b.keep(0, P1, 'Notebook opening: word to numbers, layers, mapping meaning'); b.pause(30, 'Pause: into the map')
    b.keep(P1, B1, 'Notebook tail'); b.keep(B1, B1_OUT, 'B1 Three Cities', 'cities'); b.keep(B2, B2_OUT, 'B2 Closest City', 'closest')
    b.keep(B2_OUT, P2, 'Notebook: calculated gap'); b.pause(30, 'Pause: into the drinks'); b.keep(P2, B3, 'Notebook: 2D to 7D')
    b.keep(B3, B3_OUT, 'B3 Taste table', 'taste'); b.keep(B3_OUT, P3, 'Notebook: radar'); b.pause(30, 'Pause: into the similarity map')
    b.keep(P3, B4, 'Notebook tail'); b.keep(B4, B4_OUT, 'B4 Neighborhoods', 'nbhd'); b.keep(B4_OUT, P4, 'Notebook: scatter'); b.pause(30, 'Pause: into the mystery drink')
    b.keep(P4, B5, 'Notebook tail'); b.keep(B5, B5_OUT, 'B5 Closest drink', 'drink'); b.keep(B5_OUT, P5, 'Notebook: 10,000 dimensions'); b.pause(30, 'Pause: into AI scale')
    b.keep(P5, P6, 'Notebook: matrix continues'); b.pause(30, 'Pause: into the sentence'); b.keep(P6, B6, 'Notebook: sentence tokens')
    b.keep(B6, P7, 'B6 Context changes IT', 'ctx'); b.pause(30, 'Pause: before the closing message')
    b.close(P7, CLOSE_END); b.total = b.cursor; TOTAL, CLOSE = b.total, b.close_start
    assert TOTAL == 6987, TOTAL
    ban = {k: banner_rect(cv2.imread(str(p))) for k, p in A.items()}
    b.board('cities', A['cities'], B1, B1_OUT, 'compact', [dict(label='Mountain View coordinates', at=33.42, rects=[MV], color=TEAL)], banner_at=39.36, banner=ban['cities'])
    b.board('closest', A['closest'], B2, B2_OUT, 'compact',
        [dict(label='New position 1', at=47.56, rects=[NP1], color=ORANGE), dict(label='New position 2', at=50.70, rects=[NP2], color=ORANGE),
         dict(label='Position 1 is closest to Mountain View', at=60.34, rects=[NP1, MV], color=ORANGE, colors=[ORANGE, TEAL]),
         dict(label='Position 2 is closest to New York City', at=62.72, rects=[NP2, NYC], color=ORANGE, colors=[ORANGE, BLUE])])
    b.board('taste', A['taste'], B3, B3_OUT, 'compact',
        [dict(label='A row of seven numbers is a vector (Coke row)', at=91.60, rects=[ROW[0]], color=NEUTRAL),
         dict(label='Coke and Pepsi share a profile', at=97.36, rects=[ROW[0], ROW[1]], color=NEUTRAL), dict(label='Coffee differs', at=104.16, rects=[ROW[2]], color=NEUTRAL)])
    b.board('nbhd', A['nbhd'], B4, B4_OUT, 'compact',
        [dict(label='Soft drinks neighborhood', at=125.28, rects=[SOFT], color=BLUE, radius=280), dict(label='Hot drinks neighborhood', at=132.22, rects=[HOT], color=PURPLE, radius=175)])
    b.board('drink', A['drink'], B5, B5_OUT, 'compact',
        [dict(label='Mystery drink ratings', at=148.30, rects=[MYSTERY], color=ORANGE), dict(label='First six match Pepsi', at=158.00, rects=[MYSTERY, PEPSI], color=ORANGE, colors=[ORANGE, BLUE]),
         dict(label='Citrus: 9 vs Pepsi 10', at=162.16, rects=[CIT_M, CIT_P], color=GREEN, radius=8), dict(label='Citrus: gap of 8 from Coke', at=169.44, rects=[CIT_M, CIT_C], color=GREEN, radius=8)],
        banner_at=172.10, banner=ban['drink'])
    b.board('ctx', A['ctx'], B6, P7, 'compact',
        [dict(label='Starting position numbers', at=202.20, rects=[PLQ_START], color=NEUTRAL, pad=8, radius=8), dict(label='The layers update the numbers', at=205.88, rects=[PLQ_LAYERS], color=NEUTRAL, pad=8, radius=8),
         dict(label='Updated position near CAT', at=211.02, rects=[PLQ_UPD], color=NEUTRAL, pad=8, radius=8)], banner_at=214.04, banner=ban['ctx'])
    # framing parity: at the 2026-09-10 ship, editspec_build's compact push was cw * (1 - 0.04 * n / 900) with no 4% cap and no
    # ring-clearance widening (both added 2026-09-11). Re-apply that formula to every leg so the whole-board push matches the live picture.
    for k, B in b.boards.items():
        spec = json.load(open(OUT / f'leg-{k}.json')); beat = spec['beats'][0]; n = beat['frames']; cw = beat['from'][2]
        beat['to'][2] = cw * (1 - 0.04 * n / (30 * FPS)); B['beats'] = spec['beats']; B['push_rule'] = 'ship-time (2026-09-10): 0.04 * n / 900, uncapped'
        (OUT / f'leg-{k}.json').write_text(json.dumps(spec, indent=1))
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('vectorspace')
    spans = [dict(key=r['visual'], out_start=r['start_frame'], out_end=r['end_frame'], src_in=b.boards[r['visual']]['src_in']) for r in b.rows if r['kind'] == 'source' and r['visual'] in b.boards]
    m = b.manifest(dict(retrofit_scope='Review only; visual-only retrofit of the shipped 2026-09-10 file (current course boards + canonical close); live unchanged',
                        retrofit_of=str(LIVE.relative_to(ROOT)), retrofit_of_sha256=sha(LIVE), audio_note='copied from the shipped file at mux (-c:a copy)', board_spans_output=spans,
                        banners=ban, tall_margin=False))
    print('Prepared', TOTAL, 'frames; close', CLOSE, '; board spans', [(s['key'], s['out_start'], s['out_end']) for s in spans], flush=True)
    if args.prepare_only: return
    assert not DEST.exists(), f'{DEST} exists; version-suffix instead of overwriting'
    ff = imageio_ffmpeg.get_ffmpeg_exe(); ci = b.close_img
    p = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0', '-i', str(LIVE), '-map', '0:v:0', '-map', '1:a:0',
                          '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    live = Reader(str(LIVE)); legs = {k: Reader(OUT / f'leg-{k}.mkv') for k in b.boards}; last = None
    for f in range(TOTAL):
        row = next(r for r in b.rows if r['start_frame'] <= f < r['end_frame'])
        if f >= CLOSE:
            k = f - CLOSE; q = np.clip((k - CLOSE_PREHOLD) / (CLOSE_PUSH - 1), 0, 1); z = 1 + .2 * q * q * (3 - 2 * q)
            hh_, ww_ = ci.shape[:2]; cw = ww_ / z; chh = cw * 9 / 16
            im = cv2.warpAffine(ci, np.float32([[cw / W, 0, (ww_ - cw) / 2], [0, chh / H, (hh_ - chh) / 2]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
            if k in [0, CLOSE_PREHOLD, CLOSE_PREHOLD + CLOSE_PUSH - 1, TOTAL - CLOSE - 1]: cv2.imwrite(str(OUT / f'close-{k}.jpg'), im, [cv2.IMWRITE_JPEG_QUALITY, 92])
        elif row['kind'] == 'room_tone': im = last.copy()   # the shipped build held the last rendered frame; the live picture holds the same frame
        elif row['visual'] in b.boards: im = legs[row['visual']].at(row['source_start'] + f - row['start_frame'] - b.boards[row['visual']]['src_in'])
        else: im = live.at(f)
        p.stdin.write(im.tobytes()); last = im
        if f % 1800 == 0: print('Rendered', f, '/', TOTAL, flush=True)
    p.stdin.close(); assert p.wait() == 0
    m = json.load(open(OUT / 'edit-manifest.json')); m['render_sha256'] = sha(DEST); m['protected_files_unchanged'] = {k: sha(k) == v for k, v in b.hashes.items()}; assert all(m['protected_files_unchanged'].values())
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2)); print(DEST, flush=True)

if __name__ == '__main__':
    main()
