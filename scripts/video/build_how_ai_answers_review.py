#!/usr/bin/env python3
"""How AI Answers repair (2026-09-10): current inference board + four teaching pauses + standard close.

Base: Prompts/how-ai-answers.mp4 (untouched). Output: videos/how-ai-answers-v2.mp4 (review only).
Audit: video-audit/how-ai-answers-repair-2026-09-10/

Edits (source times):
  * 1.0s matched-room-tone pauses at 47.83, 81.90, 145.93, 170.87 (each inside a measured
    silence window; the current visual holds through the pause).
  * Source frames [4389, 5126) (the Notebook rendering of the face-free inference board)
    replaced by a ken_burns_path leg over the CURRENT illustrated board
    (illustrations/how-ai-answers.jpg): full board unmarked, dive to each step card at its
    spoken onset with its locked accent ring, pull back to the full board with the takeaway
    banner ringed. Rings are drawn post-crop at a constant 5px.
  * Standard close: app close board (make_close_board.py --lesson prediction), 48-frame
    prehold, 150-frame push to 1.2x, settled hold; engine outro dropped.
Audio outside the pauses is the source audio, sample-exact.
"""
from pathlib import Path
import json, hashlib, subprocess, wave, argparse
import cv2, numpy as np, imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/how-ai-answers.mp4'
OUT = ROOT / 'video-audit/how-ai-answers-repair-2026-09-10'
DEST = ROOT / 'videos/how-ai-answers-v2.mp4'
BOARD = ROOT / 'illustrations/how-ai-answers.jpg'
KB = ROOT / 'scripts/video/ken_burns_path.py'
PY = ROOT / '.video-venv/bin/python'
FPS = 30; SR = 48000; W = 1280; H = 720; SPF = SR // FPS  # 1600 samples per frame
TOKENS = {'rank': '#4f2fc4', 'pick': '#1652f0', 'add': '#0e8f86', 'repeat': '#0f7a4a', 'neutral': '#6e51ff'}

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

class Reader:
    def __init__(self, p): self.c = cv2.VideoCapture(str(p)); self.n = -1; self.im = None
    def at(self, n):
        assert n >= self.n, (n, self.n)
        while self.n < n:
            ok, self.im = self.c.read(); assert ok, n; self.n += 1
        return self.im.copy()

def board_geometry(im):
    """Step-card ink rects, arrow glyph extents, banner rect, white card bounds (image px)."""
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); Hh, Ww = g.shape
    wr = (g > 246).mean(axis=1); rows = np.where(wr > 0.85)[0]
    card = dict(y0=int(rows.min()), y1=int(rows.max()))
    wc = (g[card['y0']:card['y1']] > 246).mean(axis=0); cols = np.where(wc > 0.85)[0]
    card.update(x0=int(cols.min()), x1=int(cols.max()))
    y0, y1 = card['y0'] + 18, card['y1']
    ink = g[y0:y1] < 170
    xs = np.where(ink.sum(axis=0) > 0)[0]
    groups = [gr for gr in np.split(xs, np.where(np.diff(xs) > 30)[0] + 1) if gr.max() - gr.min() > 100]
    assert len(groups) == 4, [(int(x.min()), int(x.max())) for x in groups]
    steps = []
    for gr in groups:
        a, b = int(gr.min()), int(gr.max()); yy = np.where(ink[:, a:b + 1].any(axis=1))[0]
        steps.append([a, y0 + int(yy.min()), b, y0 + int(yy.max())])
    # arrows / any lighter glyph between columns (must stay outside the rings)
    soft = g[y0:y1] < 235
    arrows = []
    for (a, b), (c, d) in zip([(s[0], s[2]) for s in steps], [(s[0], s[2]) for s in steps[1:]]):
        gap = np.where(soft[:, b + 1:c].any(axis=0))[0]
        arrows.append([b + 1 + int(gap.min()), b + 1 + int(gap.max())] if len(gap) else None)
    bb, gg, rr = [im[:, :, i].astype(int) for i in range(3)]
    gold = (rr > 225) & (gg > 195) & (bb < 200) & (rr - bb > 50)
    ys = np.where(gold.mean(axis=1) > 0.5)[0]; xs2 = np.where(gold[ys].mean(axis=0) > 0.5)[0]
    banner = [int(xs2.min()), int(ys.min()), int(xs2.max()), int(ys.max())]
    return steps, arrows, banner, card

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); (OUT / 'preview').mkdir(exist_ok=True)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    protected = [SRC, ROOT / 'videos/how-ai-answers.mp4', ROOT / 'lessons/how-ai-answers.md', BOARD]
    hashes = {str(p): sha(p) for p in protected}

    # ---- audio: decode once, build the edited track
    if not (OUT / 'source.wav').exists():
        subprocess.run([ff, '-y', '-v', 'error', '-i', str(SRC), '-vn', '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', str(OUT / 'source.wav')], check=True)
    audio = readwav(OUT / 'source.wav')
    # room tone seed: the 0.1s slice whose level matches the MEDIAN floor of the source's own
    # narration pauses (not the quietest slice: this AAC source gates toward digital zero, and a
    # tone ~15 dB under the surrounding floor reads as a cliff). Mirror-tiled.
    def rms(x): return float(np.sqrt(np.mean(x * x)))
    windows = [(47.56, 48.13), (81.56, 82.27), (145.65, 146.24)]
    floor = float(np.median([rms(audio[round(t * SR):round((t + .1) * SR)]) for a_, b_ in windows for t in np.arange(a_, b_ - .1, .05)]))
    cands = [(abs(rms(audio[round(t * SR):round((t + .1) * SR)]) - floor), t) for a_, b_ in windows for t in np.arange(a_, b_ - .1, .01)]
    _, tone_t = min(cands); seed = audio[round(tone_t * SR):round((tone_t + .1) * SR)].copy(); seed -= seed.mean()
    tone_rms = rms(seed)
    loop = np.r_[seed, seed[::-1]]
    def tone(n): return np.resize(loop, n)
    rows = []; parts = []; cursor = 0
    def keep(s, e, label, visual='source'):
        nonlocal cursor
        data = audio[s * SPF:e * SPF].copy()
        r = np.linspace(0, 1, 240); bed = tone(len(data))  # 5ms crossfades into matched tone at both ends
        data[:240] = data[:240] * r + bed[:240] * (1 - r); data[-240:] = data[-240:] * (1 - r) + bed[-240:] * r
        rows.append(dict(kind='source', source_start=s, source_end=e, start_frame=cursor, end_frame=cursor + e - s, label=label, visual=visual))
        parts.append(data); cursor += e - s
    def pause(n, label, hold):
        nonlocal cursor
        rows.append(dict(kind='room_tone', start_frame=cursor, end_frame=cursor + n, label=label, source_hold_frame=hold))
        parts.append(tone(n * SPF)); cursor += n
    P1, P2, P3, P4 = fr(47.83), fr(81.90), fr(145.93), fr(170.87)
    BOARD_IN = 4389            # source hard cut into the Notebook inference board (measured)
    CLOSE_AUDIO_END = fr(174.78)  # start of the post-narration silence
    keep(0, P1, 'Opening through Board 1 (final token predicts next)')
    pause(30, 'Pause: Board 1 to Board 2', P1 - 1)
    keep(P1, P2, 'Board 2: why the final token matters')
    pause(30, 'Pause: into the prediction loop', P2 - 1)
    keep(P2, P3, 'Board 3: the answer token by token')
    pause(30, 'Pause: before the inference board', P3 - 1)
    keep(P3, BOARD_IN, 'Board 3 tail (source video up to its own cut)')
    leg_start = cursor
    keep(BOARD_IN, P4, 'Inference board: current illustrated board leg', visual='board')
    leg_end = cursor
    pause(30, 'Pause: before the closing message', None)  # holds the leg's final frame
    close_start = cursor
    keep(P4, CLOSE_AUDIO_END, 'Closing message', visual='close')
    pause(120, 'Settled close hold', None)
    total = cursor
    writewav(OUT / 'edited.wav', np.concatenate(parts))

    # ---- inference board leg (ken_burns_path with post-crop rings)
    board = cv2.imread(str(BOARD)); bh, bw = board.shape[:2]
    steps, arrows, banner, card = board_geometry(board)
    bg = tuple(int(v) for v in board[4, 4])
    cw = int(bh * 16 / 9) // 2 * 2; ox = (cw - bw) // 2  # widest even 16:9 window that fits the board's height
    canvas = np.full((bh, cw, 3), bg, np.uint8); canvas[:, ox:ox + bw] = board
    cv2.imwrite(str(OUT / 'board-canvas.png'), canvas)
    PADX, PADY = 14, 12
    ytop = min(s[1] for s in steps) - PADY; ybot = max(s[3] for s in steps) + PADY  # shared vertical extent, all four cards
    rects = []
    for i, s in enumerate(steps):
        x0, x1 = s[0] - PADX, s[2] + PADX
        # the light column arrows are non-target ink: keep the ring at least 6px clear of them
        if i > 0 and arrows[i - 1]: x0 = max(x0, arrows[i - 1][1] + 6)
        if i < 3 and arrows[i]: x1 = min(x1, arrows[i][0] - 6)
        assert x0 < s[0] and x1 > s[2], ('ring would cut into ink', i, x0, x1, s)
        assert x0 - card['x0'] >= 16 and card['x1'] - x1 >= 16 and ytop - card['y0'] >= 16 and card['y1'] - ybot >= 16
        rects.append([x0 + ox, ytop, x1 - x0, ybot - ytop])
    banner_rect = [banner[0] + ox, banner[1], banner[2] - banner[0], banner[3] - banner[1]]
    n_leg = leg_end - leg_start
    on = lambda t: fr(t) - BOARD_IN  # leg-relative frame of a spoken onset
    o_rank, o_pick, o_add, o_repeat, o_take = on(154.64), on(158.06), on(159.88), on(162.38), on(165.70)
    full = [cw / 2, bh / 2, float(cw)]
    # One uniform dive window for all four cards (README: uniform zoom reads as one camera):
    # the widest single-card fit, centred on each card.
    RING_PX, MARGIN = 5, 100
    inner_w = W - 2 * (RING_PX + MARGIN); inner_h = H - 2 * (RING_PX + MARGIN)
    dive_w = max(max(r[2] * W / inner_w, r[3] * H / inner_h) for r in rects)
    fit = lambda r: [r[0] + r[2] / 2, r[1] + r[3] / 2, dive_w]
    TR = 24
    beats = [
        dict(label='establish', frames=o_rank, **{'from': full}, to=[cw / 2, bh / 2, cw * 0.97]),
        dict(label='to-rank', frames=TR, to=fit(rects[0])),
        dict(label='rank-hold', frames=o_pick - o_rank - TR, to=fit(rects[0])),
        dict(label='to-pick', frames=TR, to=fit(rects[1])),
        dict(label='pick-hold', frames=o_add - o_pick - TR, to=fit(rects[1])),
        dict(label='to-add', frames=TR, to=fit(rects[2])),
        dict(label='add-hold', frames=o_repeat - o_add - TR, to=fit(rects[2])),
        dict(label='to-repeat', frames=TR, to=fit(rects[3])),
        dict(label='repeat-hold', frames=o_take - o_repeat - TR, to=fit(rects[3])),
        dict(label='pull-back', frames=30, to=full),
        dict(label='takeaway-hold', frames=n_leg - o_take - 30, to=full),
    ]
    assert sum(b['frames'] for b in beats) == n_leg and all(b['frames'] > 0 for b in beats)
    rings = [
        dict(start=o_rank, end=o_pick, rect=rects[0], color=TOKENS['rank'], pad=0, radius=14, target='1 · Rank', source='card_locked_accent'),
        dict(start=o_pick, end=o_add, rect=rects[1], color=TOKENS['pick'], pad=0, radius=14, target='2 · Pick', source='card_locked_accent'),
        dict(start=o_add, end=o_repeat, rect=rects[2], color=TOKENS['add'], pad=0, radius=14, target='3 · Add', source='card_locked_accent'),
        dict(start=o_repeat, end=o_take, rect=rects[3], color=TOKENS['repeat'], pad=0, radius=14, target='4 · Repeat', source='card_locked_accent'),
        dict(start=o_take, end=n_leg, rect=banner_rect, color=TOKENS['neutral'], pad=0, radius=22, target='takeaway banner', source='neutral_video_purple'),
    ]
    spec = dict(image=str(OUT / 'board-canvas.png'), fps=FPS, out_w=W, out_h=H, upscale=3, beats=beats,
                rings=[{k: v for k, v in r.items() if k in ('start', 'end', 'rect', 'color', 'pad', 'radius')} for r in rings])
    (OUT / 'leg-spec.json').write_text(json.dumps(spec, indent=1))
    subprocess.run([str(PY), str(KB), str(OUT / 'leg-spec.json'), '--preview', str(OUT / 'preview')], check=True)
    subprocess.run([str(PY), str(KB), str(OUT / 'leg-spec.json'), str(OUT / 'leg.mkv')], check=True)
    c = cv2.VideoCapture(str(OUT / 'leg.mkv')); n = 0
    while c.read()[0]: n += 1
    assert n == n_leg, (n, n_leg)

    # ---- close board
    if not (OUT / 'close.png').exists():
        subprocess.run([str(PY), str(ROOT / 'scripts/video/make_close_board.py'), '--lesson', 'prediction', '--out', str(OUT / 'close.png')], check=True)
    close_img = cv2.imread(str(OUT / 'close.png'))

    boundaries = [dict(frame=r['start_frame'], label=r['label']) for r in rows[1:]]
    manifest = dict(output=str(DEST), source=str(SRC), fps=FPS, total_frames=total, duration=total / FPS,
                    timeline=rows, leg=dict(start_frame=leg_start, end_frame=leg_end, source_start=BOARD_IN, board=str(BOARD),
                    canvas_offset_x=ox, step_ink_rects=steps, arrows=arrows, banner=banner, card=card, rings=rings, beats=beats),
                    board_sync=dict(lesson_id='prediction', video_file='videos/how-ai-answers.mp4', board_asset=str(BOARD.relative_to(ROOT)),
                    board_sha256=sha(BOARD), density='dense', camera_treatment='zoom_pan_complete_areas', audio_action='selective_edit',
                    qa_status='review_ready', states=[dict(spoken_onset=leg_start + r['start'], highlight_target=r['target'], highlight_mode='ring',
                    highlight_color=r['color'], highlight_source=r['source']) for r in rings]),
                    close=dict(start_frame=close_start, prehold=48, push=150, endpoint=1.2, settle=total - close_start - 198),
                    audio=dict(sample_rate=SR, room_tone_source=[tone_t, tone_t + .1], room_tone_rms=tone_rms, source_pause_floor_rms=floor, crossfade_ms=5, pauses_frames=30),
                    boundaries=boundaries, protected_hashes=hashes, scope='Review only; live unchanged')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2))
    print('Prepared', total, f'{total / FPS:.2f}s', 'leg', leg_start, leg_end, 'close', close_start, flush=True)
    if args.prepare_only: return

    # ---- render, one pass
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    p = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0',
                          '-i', str(OUT / 'edited.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium',
                          '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    src = Reader(SRC); leg = Reader(OUT / 'leg.mkv'); last = None
    for f in range(total):
        row = next(r for r in rows if r['start_frame'] <= f < r['end_frame'])
        if f >= close_start:
            k = f - close_start; q = np.clip((k - 48) / 149, 0, 1); z = 1 + .2 * q * q * (3 - 2 * q)
            h, w = close_img.shape[:2]; ww = w / z; hh = ww * 9 / 16
            im = cv2.warpAffine(close_img, np.float32([[ww / W, 0, (w - ww) / 2], [0, hh / H, (h - hh) / 2]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
        elif row['kind'] == 'room_tone':
            im = last.copy()
        elif row['visual'] == 'board':
            im = leg.at(f - leg_start)
        else:
            im = src.at(row['source_start'] + f - row['start_frame'])
        p.stdin.write(im.tobytes()); last = im
    p.stdin.close(); assert p.wait() == 0
    manifest['render_sha256'] = sha(DEST)
    manifest['protected_files_unchanged'] = {k: sha(Path(k)) == v for k, v in hashes.items()}
    assert all(manifest['protected_files_unchanged'].values())
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2))
    print(DEST, flush=True)

if __name__ == '__main__':
    main()
