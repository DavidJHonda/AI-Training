#!/usr/bin/env python3
"""How AI Answers repair candidate under EDIT-SPEC.md (2026-09-11): every board, pauses, close.

Base: Prompts/how-ai-answers.mp4 (untouched). Output: videos/how-ai-answers-v3.mp4 (review only).
Audit: video-audit/how-ai-answers-repair-2026-09-11/

Boards (source cuts measured by sequential decode; each replaced from its own cut):
  B1 Before the Answer Begins   frames [400, 1442)   dense   4 cards + banner
  B2 Why the Final Token Matters frames [1442, 2467)  compact 2 cards + banner
  B3a The Answer, Token by Token frames [2467, 3804)  dense   Prediction 1 / three more / Prediction 5
      (Notebook's own loop diagram [3804, 4074) is kept: accurate, engaging)
  B3b The Answer, Token by Token frames [4074, 4389)  full view + banner ring
  B4 Inference: How AI Builds an Answer [4389, 5126) dense 4 steps + banner (current illustrated board)
Every board opens at full view unmarked; dense boards dive to complete cards at spoken onsets with one
uniform window per board; rings are drawn post-crop at 5px in each card's locked accent.
Pauses: 1.0s matched room tone at 47.83, 81.90, 145.93, 170.87 (visual held). Standard close.
Audio outside the pauses is the source audio.
"""
from pathlib import Path
import json, hashlib, subprocess, wave, argparse
import cv2, numpy as np, imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/how-ai-answers.mp4'
OUT = ROOT / 'video-audit/how-ai-answers-repair-2026-09-11'
DEST = ROOT / 'videos/how-ai-answers-v3.mp4'
KB = ROOT / 'scripts/video/ken_burns_path.py'
PY = ROOT / '.video-venv/bin/python'
ILL = ROOT / 'illustrations'
FPS = 30; SR = 48000; W = 1280; H = 720; SPF = SR // FPS
PURPLE, BLUE, TEAL, GREEN, NEUTRAL = '#4f2fc4', '#1652f0', '#0e8f86', '#0f7a4a', '#6e51ff'
RING_PX, MARGIN, TR, PULL = 5, 40, 24, 30  # margin: frame clearance around a dive's ring (spec minimum 24)

def fr(t): return round(t * FPS)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def readwav(p):
    with wave.open(str(p)) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
def writewav(p, a):
    with wave.open(str(p), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.clip(a, -32768, 32767).astype(np.int16).tobytes())
def rms(x): return float(np.sqrt(np.mean(x * x)))

class Reader:
    def __init__(self, p): self.c = cv2.VideoCapture(str(p)); self.n = -1; self.im = None
    def at(self, n):
        assert n >= self.n, (n, self.n)
        while self.n < n:
            ok, self.im = self.c.read(); assert ok, n; self.n += 1
        return self.im.copy()

# ---------------------------------------------------------------- geometry (image px)
def bbox(mask):
    ys, xs = np.where(mask); return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
def fill_bbox(im, pt, region, tol=8):
    c = im[pt[1], pt[0]].astype(int); m = np.abs(im.astype(int) - c).sum(axis=2) <= tol
    x0, y0, x1, y1 = region; mm = np.zeros_like(m); mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]; return bbox(mm)
def banner_rect(im):
    b, g, r = [im[:, :, i].astype(int) for i in range(3)]
    gold = (r > 225) & (g > 195) & (b < 200) & (r - b > 50)
    ys = np.where(gold.mean(axis=1) > 0.5)[0]; xs = np.where(gold[ys].mean(axis=0) > 0.5)[0]
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
def rect_wh(b): return [b[0], b[1], b[2] - b[0], b[3] - b[1]]

def geom_b1(im):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    arrows = []
    for x0, x1 in ((416, 447), (783, 815), (1151, 1183)):
        ys, xs = np.where(g[380:470, x0:x1] < 235); arrows.append([x0 + int(xs.min()), x0 + int(xs.max())])
    edges = [40] + [a[0] for a in arrows] + [1560]
    cards = []
    for i in range(4):
        lo = edges[i] + (6 if i else 0); hi = edges[i + 1] - 6
        ys, xs = np.where(g[300:560, lo:hi] < 238); ix0, ix1 = lo + int(xs.min()), lo + int(xs.max())
        ys2, _ = np.where(g[540:880, lo:hi] < 170); tb = 540 + int(ys2.max())
        cards.append([ix0, 300 + int(ys.min()), ix1, tb])
    top = min(c[1] for c in cards) - 8; bot = max(c[3] for c in cards) + 16
    return [[c[0], top, c[2], bot] for c in cards], banner_rect(im), arrows
def geom_b2(im):
    q = fill_bbox(im, (120, 200), (40, 140, 800, 500)); f = fill_bbox(im, (860, 200), (800, 140, 1560, 500))
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); ys, _ = np.where(g[490:700, 60:1540] < 170); tb = 490 + int(ys.max())
    return [[q[0], q[1] - 8, q[2], tb + 12], [f[0], f[1] - 8, f[2], tb + 12]], banner_rect(im)
def geom_b3(im):
    p1 = fill_bbox(im, (100, 340), (40, 300, 620, 800)); p5 = fill_bbox(im, (1020, 340), (980, 300, 1560, 800))
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    mid = bbox(np.pad(g[440:700, 620:980] < 200, ((440, 0), (620, 0))))
    lab1 = bbox(np.pad(g[770:940, 60:620] < 200, ((770, 0), (60, 0)))); lab5 = bbox(np.pad(g[770:940, 980:1560] < 200, ((770, 0), (980, 0))))
    mid_ring = [mid[0] - 14, mid[1] - 14, mid[2] + 14, mid[3] + 14]
    # dive camera: the card box plus its title line below ("1 · Prediction 1"), not the token pill under it
    return dict(p1=p1, p5=p5, mid=mid_ring, cam1=[p1[0], p1[1], p1[2], lab1[1] + 58], cam5=[p5[0], p5[1], p5[2], lab5[1] + 58]), banner_rect(im)
def geom_b4(im):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    wr = (g > 246).mean(axis=1); rows = np.where(wr > 0.85)[0]; cy0, cy1 = int(rows.min()), int(rows.max())
    y0, y1 = cy0 + 18, cy1; ink = g[y0:y1] < 170; xs = np.where(ink.sum(axis=0) > 0)[0]
    groups = [gr for gr in np.split(xs, np.where(np.diff(xs) > 30)[0] + 1) if gr.max() - gr.min() > 100]; assert len(groups) == 4
    steps = []
    for gr in groups:
        a, b = int(gr.min()), int(gr.max()); yy = np.where(ink[:, a:b + 1].any(axis=1))[0]; steps.append([a, y0 + int(yy.min()), b, y0 + int(yy.max())])
    soft = g[y0:y1] < 235; arrows = []
    for (s, t) in zip(steps, steps[1:]):
        gap = np.where(soft[:, s[2] + 1:t[0]].any(axis=0))[0]; arrows.append([s[2] + 1 + int(gap.min()), s[2] + 1 + int(gap.max())])
    top = min(s[1] for s in steps) - 12; bot = max(s[3] for s in steps) + 12; rects = []
    for i, s in enumerate(steps):
        x0, x1 = s[0] - 14, s[2] + 14
        if i > 0: x0 = max(x0, arrows[i - 1][1] + 6)
        if i < 3: x1 = min(x1, arrows[i][0] - 6)
        rects.append([x0, top, x1, bot])
    return rects, banner_rect(im), arrows

# ---------------------------------------------------------------- leg planning
def compose(asset, key):
    board = cv2.imread(str(asset)); bh, bw = board.shape[:2]
    # smallest 16:9 canvas that contains the board: sized by height for tall boards, by width for wide ones
    cw = max(bw, int(bh * 16 / 9)); cw += cw % 2; ch = -(-cw * 9 // 16); ch += ch % 2
    ox, oy = (cw - bw) // 2, (ch - bh) // 2; bg = tuple(int(v) for v in board[4, 4])
    canvas = np.full((ch, cw, 3), bg, np.uint8); canvas[oy:oy + bh, ox:ox + bw] = board
    p = OUT / f'canvas-{key}.png'; cv2.imwrite(str(p), canvas); return board, p, cw, ch, (ox, oy)
def fit_w(rect_wh_):
    # window width whose scale (W / width) fits the rect inside the frame with ring + margin clearance on both axes
    x, y, w, h = rect_wh_
    return max(w * W / (W - 2 * (RING_PX + MARGIN)), h * W / (H - 2 * (RING_PX + MARGIN)))

def plan_leg(key, asset, src_in, src_out, density, items, banner_at=None, pullback_at=None, banner=None, first_full_hold=None):
    """items: list of (label, onset_seconds, ring_rect_xyxy, camera_rect_xyxy, color). Returns spec dict + meta."""
    board, canvas_path, cw, ch, (ox, oy) = compose(asset, key)
    n = src_out - src_in; on = lambda t: fr(t) - src_in
    full = [cw / 2, ch / 2, float(cw)]
    sh = lambda r: [r[0] + ox, r[1] + oy, r[2] - r[0], r[3] - r[1]]     # xyxy image -> xywh canvas
    rings, beats, states = [], [], []
    ends = [on(it[1]) for it in items[1:]] + [on(banner_at) if banner_at else n]
    for (label, t, ring_r, cam_r, color), e in zip(items, ends):
        rings.append(dict(start=on(t), end=e, rect=sh(ring_r), color=color, pad=0, radius=14))
        states.append(dict(spoken_onset_source_frame=fr(t), highlight_target=label, highlight_mode='ring', highlight_color=color,
                           highlight_source='card_locked_accent' if color != NEUTRAL else 'neutral_video_purple'))
    if banner_at:
        rings.append(dict(start=on(banner_at), end=n, rect=sh(banner), color=NEUTRAL, pad=0, radius=22))
        states.append(dict(spoken_onset_source_frame=fr(banner_at), highlight_target='takeaway banner', highlight_mode='ring', highlight_color=NEUTRAL, highlight_source='neutral_video_purple'))
    first = on(items[0][1]) if items else (on(banner_at) if banner_at else n)
    assert first >= 2 * FPS, (key, 'full-view open under 2s', first)
    if density == 'compact':
        beats = [dict(label='full-view', frames=n, **{'from': full}, to=[cw / 2, ch / 2, cw * (1 - 0.04 * n / (30 * FPS))])]
    else:
        dive_w = max(fit_w(sh(it[3])) for it in items) if items else None
        beats = [dict(label='establish', frames=first, **{'from': full}, to=[cw / 2, ch / 2, cw * 0.97])]
        cursor = first
        for i, (label, t, ring_r, cam_r, color) in enumerate(items):
            c = sh(cam_r); cam = [c[0] + c[2] / 2, c[1] + c[3] / 2, dive_w]
            nxt = on(items[i + 1][1]) if i + 1 < len(items) else (on(pullback_at) if pullback_at else n)
            hold = nxt - cursor - TR; assert hold > 0, (key, label, hold)
            beats += [dict(label=f'to-{label}', frames=TR, to=cam), dict(label=f'hold-{label}', frames=hold, to=cam)]; cursor = nxt
        if pullback_at:
            beats += [dict(label='pull-back', frames=PULL, to=full), dict(label='full-hold', frames=n - cursor - PULL, to=full)]
    assert sum(b['frames'] for b in beats) == n and all(b['frames'] > 0 for b in beats), key
    spec = dict(image=str(canvas_path), fps=FPS, out_w=W, out_h=H, upscale=3, beats=beats, rings=rings)
    (OUT / f'leg-{key}.json').write_text(json.dumps(spec, indent=1))
    return dict(key=key, asset=str(asset.relative_to(ROOT)), sha256=sha(asset), src_in=src_in, src_out=src_out, density=density,
                full_view_frames=first, canvas_offset=[ox, oy], states=states, beats=beats, rings=rings)

def render_leg(key, n):
    (OUT / 'preview' / key).mkdir(parents=True, exist_ok=True)
    subprocess.run([str(PY), str(KB), str(OUT / f'leg-{key}.json'), '--preview', str(OUT / 'preview' / key)], check=True, stdout=subprocess.DEVNULL)
    subprocess.run([str(PY), str(KB), str(OUT / f'leg-{key}.json'), str(OUT / f'leg-{key}.mkv')], check=True, stdout=subprocess.DEVNULL)
    c = cv2.VideoCapture(str(OUT / f'leg-{key}.mkv')); k = 0
    while c.read()[0]: k += 1
    assert k == n, (key, k, n)

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); (OUT / 'preview').mkdir(exist_ok=True)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    assets = {k: ILL / f for k, f in dict(b1='how-ai-answers-before-answer-begins-v2.jpg', b2='how-ai-answers-where-answer-begins-v2.jpg',
                                           b3='how-ai-answers-token-by-token.jpg', b4='how-ai-answers.jpg').items()}
    protected = [SRC, ROOT / 'videos/how-ai-answers.mp4', ROOT / 'lessons/how-ai-answers.md', *assets.values()]
    hashes = {str(p): sha(p) for p in protected}

    # ---- audio
    if not (OUT / 'source.wav').exists():
        subprocess.run([ff, '-y', '-v', 'error', '-i', str(SRC), '-vn', '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', str(OUT / 'source.wav')], check=True)
    audio = readwav(OUT / 'source.wav')
    windows = [(47.56, 48.13), (81.56, 82.27), (145.65, 146.24)]
    floor = float(np.median([rms(audio[round(t * SR):round((t + .1) * SR)]) for a_, b_ in windows for t in np.arange(a_, b_ - .1, .05)]))
    _, tone_t = min((abs(rms(audio[round(t * SR):round((t + .1) * SR)]) - floor), t) for a_, b_ in windows for t in np.arange(a_, b_ - .1, .01))
    seed = audio[round(tone_t * SR):round((tone_t + .1) * SR)].copy(); seed -= seed.mean(); loop = np.r_[seed, seed[::-1]]
    def tone(n): return np.resize(loop, n)
    rows, parts, cursor = [], [], 0
    def keep(s, e, label, visual):
        nonlocal cursor
        data = audio[s * SPF:e * SPF].copy(); r = np.linspace(0, 1, 240); bed = tone(len(data))
        data[:240] = data[:240] * r + bed[:240] * (1 - r); data[-240:] = data[-240:] * (1 - r) + bed[-240:] * r
        rows.append(dict(kind='source', source_start=s, source_end=e, start_frame=cursor, end_frame=cursor + e - s, label=label, visual=visual)); parts.append(data); cursor += e - s
    def pause(n, label):
        nonlocal cursor
        rows.append(dict(kind='room_tone', start_frame=cursor, end_frame=cursor + n, label=label)); parts.append(tone(n * SPF)); cursor += n
    P1, P2, P3, P4 = fr(47.83), fr(81.90), fr(145.93), fr(170.87)
    B1, B2, B3, DIAG, B3B, B4 = 400, 1442, 2467, 3804, 4074, 4389
    CLOSE_AUDIO_END = fr(174.78)
    keep(0, B1, 'Notebook opening', 'source')
    keep(B1, P1, 'B1 Before the Answer Begins', 'b1'); pause(30, 'Pause: Board 1 to Board 2')
    keep(P1, B2, 'B1 tail', 'b1')
    keep(B2, P2, 'B2 Why the Final Token Matters', 'b2'); pause(30, 'Pause: into the prediction loop')
    keep(P2, B3, 'B2 tail', 'b2')
    keep(B3, DIAG, 'B3a The Answer, Token by Token', 'b3a')
    keep(DIAG, B3B, 'Notebook loop diagram (kept)', 'source')
    keep(B3B, P3, 'B3b banner return', 'b3b'); pause(30, 'Pause: before the inference board')
    keep(P3, B4, 'B3b tail', 'b3b')
    keep(B4, P4, 'B4 Inference board', 'b4'); pause(30, 'Pause: before the closing message')
    close_start = cursor
    keep(P4, CLOSE_AUDIO_END, 'Closing message', 'close'); pause(120, 'Settled close hold')
    total = cursor; writewav(OUT / 'edited.wav', np.concatenate(parts))

    # ---- boards
    im1, im2, im3, im4 = (cv2.imread(str(assets[k])) for k in ('b1', 'b2', 'b3', 'b4'))
    c1, ban1, arr1 = geom_b1(im1); c2, ban2 = geom_b2(im2); g3, ban3 = geom_b3(im3); c4, ban4, arr4 = geom_b4(im4)
    legs = {}
    legs['b1'] = plan_leg('b1', assets['b1'], B1, B2, 'dense',
        [('Tokens', 16.04, c1[0], c1[0], PURPLE), ('Positions', 20.98, c1[1], c1[1], BLUE),
         ('Starting Vectors', 26.24, c1[2], c1[2], TEAL), ('Through Layers', 31.82, c1[3], c1[3], GREEN)],
        banner_at=42.90, pullback_at=39.48, banner=ban1)
    legs['b2'] = plan_leg('b2', assets['b2'], B2, B3, 'compact',
        [('The Question', 57.84, c2[0], c2[0], PURPLE), ('The Final Token', 65.50, c2[1], c2[1], BLUE)], banner_at=74.08, banner=ban2)
    legs['b3a'] = plan_leg('b3a', assets['b3'], B3, DIAG, 'dense',
        [('Prediction 1', 89.70, g3['p1'], g3['cam1'], PURPLE), ('Three more predictions', 100.84, g3['mid'], g3['mid'], BLUE),
         ('Prediction 5', 107.18, g3['p5'], g3['cam5'], TEAL)])
    legs['b3b'] = plan_leg('b3b', assets['b3'], B3B, B4, 'compact', [], banner_at=141.84, banner=ban3)
    legs['b4'] = plan_leg('b4', assets['b4'], B4, P4, 'dense',
        [('1 · Rank', 154.64, c4[0], c4[0], PURPLE), ('2 · Pick', 158.06, c4[1], c4[1], BLUE),
         ('3 · Add', 159.88, c4[2], c4[2], TEAL), ('4 · Repeat', 162.38, c4[3], c4[3], GREEN)],
        banner_at=165.70, pullback_at=165.70, banner=ban4)
    for k, L in legs.items(): render_leg(k, L['src_out'] - L['src_in'])

    if not (OUT / 'close.png').exists():
        subprocess.run([str(PY), str(ROOT / 'scripts/video/make_close_board.py'), '--lesson', 'prediction', '--out', str(OUT / 'close.png')], check=True, stdout=subprocess.DEVNULL)
    close_img = cv2.imread(str(OUT / 'close.png'))

    boundaries = [dict(frame=r['start_frame'], label=r['label']) for r in rows[1:]]
    manifest = dict(output=str(DEST), source=str(SRC), fps=FPS, total_frames=total, duration=total / FPS, timeline=rows, boards=legs,
                    close=dict(start_frame=close_start, prehold=48, push=150, endpoint=1.2, settle=total - close_start - 198),
                    audio=dict(sample_rate=SR, room_tone_source=[tone_t, tone_t + .1], room_tone_rms=rms(seed), source_pause_floor_rms=floor, crossfade_ms=5, pauses_frames=30),
                    boundaries=boundaries, protected_hashes=hashes, scope='Review only; live unchanged')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2))
    print('Prepared', total, f'{total / FPS:.2f}s', {k: (L['src_in'], L['src_out'], L['density'], L['full_view_frames']) for k, L in legs.items()}, flush=True)
    if args.prepare_only: return

    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    p = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0', '-i', str(OUT / 'edited.wav'),
                          '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                          '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    src = Reader(SRC); readers = {k: Reader(OUT / f'leg-{k}.mkv') for k in legs}; last = None
    for f in range(total):
        row = next(r for r in rows if r['start_frame'] <= f < r['end_frame'])
        if f >= close_start:
            k = f - close_start; q = np.clip((k - 48) / 149, 0, 1); z = 1 + .2 * q * q * (3 - 2 * q)
            h, w = close_img.shape[:2]; ww = w / z; hh = ww * 9 / 16
            im = cv2.warpAffine(close_img, np.float32([[ww / W, 0, (w - ww) / 2], [0, hh / H, (h - hh) / 2]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
        elif row['kind'] == 'room_tone': im = last.copy()
        else:
            sf = row['source_start'] + f - row['start_frame']
            im = src.at(sf) if row['visual'] == 'source' else readers[row['visual']].at(sf - legs[row['visual']]['src_in'])
        p.stdin.write(im.tobytes()); last = im
    p.stdin.close(); assert p.wait() == 0
    manifest['render_sha256'] = sha(DEST); manifest['protected_files_unchanged'] = {k: sha(Path(k)) == v for k, v in hashes.items()}
    assert all(manifest['protected_files_unchanged'].values()); (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2)); print(DEST, flush=True)

if __name__ == '__main__':
    main()
