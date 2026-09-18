#!/usr/bin/env python3
"""How AI Answers v6: the current course boards and the canonical close, as a visual-only retrofit of the shipped v5 (2026-09-18). Review only.

The shipped file (course-assets/how-ai-answers/how-ai-answers.mp4, 5483 frames) is the v5 candidate of 2026-09-10/11
(build_how_ai_answers_review.py: four boards over five spans, four one-second pauses, standard close, Notebook corner mark cleaned).
The raw roll (Prompts/how-ai-answers.mp4) no longer exists, so this build takes the finished file as its picture source, re-renders the
five board legs from the current course-assets JPGs with the shipped script's exact board definitions (same source cuts, densities,
ring targets, onsets and accents; geometry re-measured on the current files), splices each leg over its span of the output timeline,
replaces the close with the canonical closing JPG (make_close_board.py --lesson prediction), and muxes the shipped audio stream back
in untouched. Every Notebook span is the shipped picture. The shipped timeline (source frames -> output frames) is replayed with the
same keep/pause calls so every leg lands where it did.

Boards 1-3 changed only by the website credit line (rects detect at the shipped coordinates). Board 4 is a new layout (four cards
under the question and the answer so far, 1600x1000) and keeps the shipped treatment: compact, ring 1 Rank / 2 Pick / 3 Add / 4 Repeat
on the whole cards at the spoken onsets, banner ring last.
"""
from pathlib import Path
import argparse, subprocess, sys, json
import numpy as np, cv2, imageio_ffmpeg
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, Reader, fr, banner_rect, sha, PURPLE, BLUE, TEAL, GREEN, NEUTRAL, CLOSE_PREHOLD, CLOSE_PUSH, W, H, FPS, SPF
from make_close_board import close_board_copy

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/how-ai-answers/how-ai-answers.mp4'
OUT = ROOT / 'video-audit/how-ai-answers-repair-2026-09-18'
DEST = ROOT / 'Prompts/how-ai-answers-v6.mp4'
D = ROOT / 'course-assets/how-ai-answers'
A = dict(b1=D / 'how-ai-answers-before-answer-begins.jpg', b2=D / 'how-ai-answers-where-answer-begins.jpg',
         b3=D / 'how-ai-answers-token-by-token.jpg', b4=D / 'how-ai-answers-building-an-answer.jpg')
# shipped source cuts (frames of the shipped picture before the pauses) and pauses
B1, B2, B3, DIAG, B3B, B4 = 400, 1442, 2467, 3804, 4074, 4389
P1, P2, P3, P4 = fr(47.83), fr(81.90), fr(145.93), fr(170.87)
CLOSE_AUDIO_END = fr(174.78)

# ---------------------------------------------------------------- geometry (image px, xyxy), the shipped script's detectors
def bbox(mask):
    ys, xs = np.where(mask); return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
def fill_bbox(im, pt, region, tol=8):
    c = im[pt[1], pt[0]].astype(int); m = np.abs(im.astype(int) - c).sum(axis=2) <= tol
    x0, y0, x1, y1 = region; mm = np.zeros_like(m); mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]; return bbox(mm)
def geom_b1(im):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); arrows = []
    for x0, x1 in ((416, 447), (783, 815), (1151, 1183)):
        ys, xs = np.where(g[380:470, x0:x1] < 235); arrows.append([x0 + int(xs.min()), x0 + int(xs.max())])
    edges = [40] + [a[0] for a in arrows] + [1560]; cards = []
    for i in range(4):
        lo = edges[i] + (6 if i else 0); hi = edges[i + 1] - 6
        ys, xs = np.where(g[300:560, lo:hi] < 238); ix0, ix1 = lo + int(xs.min()), lo + int(xs.max())
        ys2, _ = np.where(g[540:880, lo:hi] < 170); tb = 540 + int(ys2.max())
        cards.append([ix0, 300 + int(ys.min()), ix1, tb])
    top = min(c[1] for c in cards) - 8; bot = max(c[3] for c in cards) + 16
    return [[c[0], top, c[2], bot] for c in cards]
def geom_b2(im):
    q = fill_bbox(im, (120, 200), (40, 140, 800, 500)); f = fill_bbox(im, (860, 200), (800, 140, 1560, 500))
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); ys, _ = np.where(g[490:700, 60:1540] < 170); tb = 490 + int(ys.max())
    return [[q[0], q[1] - 8, q[2], tb + 12], [f[0], f[1] - 8, f[2], tb + 12]]
def geom_b3(im):
    p1 = fill_bbox(im, (100, 340), (40, 300, 620, 800)); p5 = fill_bbox(im, (1020, 340), (980, 300, 1560, 800))
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    mid = bbox(np.pad(g[440:700, 620:980] < 200, ((440, 0), (620, 0))))
    lab1 = bbox(np.pad(g[770:940, 60:620] < 200, ((770, 0), (60, 0)))); lab5 = bbox(np.pad(g[770:940, 980:1560] < 200, ((770, 0), (980, 0))))
    mid_ring = [mid[0] - 14, mid[1] - 14, mid[2] + 14, mid[3] + 14]
    # dive camera: the card box plus its title line below ("1 · Prediction 1"), not the token pill under it
    return dict(p1=p1, p5=p5, mid=mid_ring, cam1=[p1[0], p1[1], p1[2], lab1[1] + 58], cam5=[p5[0], p5[1], p5[2], lab5[1] + 58])
def geom_b4(im):
    """Current board (2026-09-15 layout): four bordered cards in a row under the question / answer-so-far lines.
    Card borders are the only sub-246 pixels on a row through the cards' empty middle; the top/bottom edges are the
    outermost border rows in a column through each card."""
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); ban = banner_rect(im); y0, y1 = 200, ban[1] - 20
    ink = g[y0:y1, 60:1540] < 246; counts = ink.sum(axis=1)
    rows8 = np.where(counts == 8)[0]   # rows crossing only the eight card borders (between the titles and the body text)
    assert len(rows8) > 20, len(rows8)
    xs = [sorted(int(x) + 60 for x in np.where(ink[y])[0]) for y in rows8]
    left = [min(r[2 * i] for r in xs) for i in range(4)]; right = [max(r[2 * i + 1] for r in xs) for i in range(4)]   # widest extent (rounded corners narrow the top rows)
    gap = (right[0] + left[1]) // 2   # between cards: the full-width answer strip above has ink here, the card borders do not
    cards = []
    for i in range(4):
        col = lambda x: g[y0:y1, x] < 246
        ys = [int(y) for y in np.where(col(left[i] + 40) & col(right[i] - 40) & ~col(gap))[0]]   # rows inking both card edges but not the gap: the top and bottom borders (text rows lie between)
        cards.append([int(left[i]), y0 + min(ys), int(right[i]), y0 + max(ys)])
    return cards

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, LIVE, OUT, DEST, protected=[ROOT / 'lessons/how-ai-answers.md', D / 'how-ai-answers-close.jpg', ROOT / 'index.html', *A.values()])
    b.tall_margin = False   # framing parity with the 2026-09-10 ship (the 4% tall-board stage margin postdates it)
    assert close_board_copy('prediction')[0]
    # replay the shipped timeline for the output-frame mapping only (audio is copied from the shipped file at mux)
    b.audio = np.zeros(CLOSE_AUDIO_END * SPF + SPF); b.loop = np.zeros(2 * 4800)
    b.keep(0, B1, 'Notebook opening')
    b.keep(B1, P1, 'B1 Before the Answer Begins', 'b1'); b.pause(30, 'Pause: Board 1 to Board 2'); b.keep(P1, B2, 'B1 tail', 'b1')
    b.keep(B2, P2, 'B2 Why the Final Token Matters', 'b2'); b.pause(30, 'Pause: into the prediction loop'); b.keep(P2, B3, 'B2 tail', 'b2')
    b.keep(B3, DIAG, 'B3a The Answer, Token by Token', 'b3a')
    b.keep(DIAG, B3B, 'Notebook loop diagram (kept)')
    b.keep(B3B, P3, 'B3b banner return', 'b3b'); b.pause(30, 'Pause: before the inference board'); b.keep(P3, B4, 'B3b tail', 'b3b')
    b.keep(B4, P4, 'B4 Inference board', 'b4'); b.pause(30, 'Pause: before the closing message')
    b.close(P4, CLOSE_AUDIO_END); b.total = b.cursor; TOTAL, CLOSE = b.total, b.close_start
    assert TOTAL == 5483 and CLOSE == 5246, (TOTAL, CLOSE)
    ims = {k: cv2.imread(str(p)) for k, p in A.items()}; ban = {k: banner_rect(im) for k, im in ims.items()}
    c1 = geom_b1(ims['b1']); c2 = geom_b2(ims['b2']); g3 = geom_b3(ims['b3']); c4 = geom_b4(ims['b4'])
    T = lambda label, at, rect, color, cam=None: dict(label=label, at=at, rects=[rect], color=color, cam=cam or rect)
    b.board('b1', A['b1'], B1, B2, 'dense',
        [T('Tokens', 16.04, c1[0], PURPLE), T('Positions', 20.98, c1[1], BLUE), T('Starting Vectors', 26.24, c1[2], TEAL), T('Through Layers', 31.82, c1[3], GREEN)],
        banner_at=42.90, pullback_at=39.48, banner=ban['b1'])
    b.board('b2', A['b2'], B2, B3, 'compact', [T('The Question', 57.84, c2[0], PURPLE), T('The Final Token', 65.50, c2[1], BLUE)], banner_at=74.08, banner=ban['b2'])
    b.board('b3a', A['b3'], B3, DIAG, 'dense',
        [T('Prediction 1', 89.70, g3['p1'], PURPLE, g3['cam1']), T('Three more predictions', 100.84, g3['mid'], BLUE), T('Prediction 5', 107.18, g3['p5'], TEAL, g3['cam5'])])
    b.board('b3b', A['b3'], B3B, B4, 'compact', [], banner_at=141.84, banner=ban['b3'])
    # Owner call 2026-09-11: the four-step strip reads at full view, so this board is compact (no dives); the current four-card board keeps that.
    b.board('b4', A['b4'], B4, P4, 'compact',
        [T('1 · Rank', 154.64, c4[0], PURPLE), T('2 · Pick', 158.06, c4[1], BLUE), T('3 · Add', 159.88, c4[2], TEAL), T('4 · Repeat', 162.38, c4[3], GREEN)],
        banner_at=165.70, banner=ban['b4'])
    # framing parity for the compact legs: at the 2026-09-10 ship, editspec_build's compact push was cw * (1 - 0.04 * n / 900) with no 4% cap
    # and no ring-clearance widening (both added 2026-09-11). Re-apply that formula so the compact boards push exactly as the live picture does.
    # Dense legs follow the current module (static establish per the owner rule of 2026-09-14: no zoom while the full board is shown).
    for k, B in b.boards.items():
        if B['density'] != 'compact': continue
        spec = json.load(open(OUT / f'leg-{k}.json')); beat = spec['beats'][0]; n = beat['frames']; cw = beat['from'][2]
        beat['to'][2] = cw * (1 - 0.04 * n / (30 * FPS)); B['beats'] = spec['beats']; B['push_rule'] = 'ship-time (2026-09-10): 0.04 * n / 900, uncapped'
        (OUT / f'leg-{k}.json').write_text(json.dumps(spec, indent=1))
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('prediction')
    spans = [dict(key=r['visual'], out_start=r['start_frame'], out_end=r['end_frame'], src_in=b.boards[r['visual']]['src_in']) for r in b.rows if r['kind'] == 'source' and r['visual'] in b.boards]
    b.manifest(dict(retrofit_scope='Review only; visual-only retrofit of the shipped 2026-09-10/11 file (current course boards + canonical close); live unchanged',
                    retrofit_of=str(LIVE.relative_to(ROOT)), retrofit_of_sha256=sha(LIVE), audio_note='copied from the shipped file at mux (-c:a copy)', board_spans_output=spans,
                    banners=ban, geometry=dict(b1=c1, b2=c2, b3=g3, b4=c4), tall_margin=False))
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
