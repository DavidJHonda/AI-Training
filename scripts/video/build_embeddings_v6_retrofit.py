#!/usr/bin/env python3
"""Embeddings v6: v5 (current boards + canonical close in the shipped v4, audio copied) with a camera walk over Inside a Real Model
(David, 2026-09-17: v4 cut between three framings of that illustration board; "when we show these, we typically zoom and pan").

Everything outside the Inside a Real Model span [5352, 6509) is v5 (build_embeddings_v5_retrofit.py: v4's picture, the five current
boards, the canonical close). Inside it, v4's three hard cuts (full -> crop A at the cat, crop A -> crop B at the dimension columns,
crop B -> full at Value) become camera moves, and v4's rings keep their frames: establish the full board with a slight push (to 97%),
a 24-frame glide into a window on the cat and its token ID at the "cat" onset, a glide to the lookup-row window at that onset, a glide
up to the dimensions window at that onset, and a 30-frame pull-back to the full board at the Value onset, so the span ends on the full
illustration with Value and Embedding ringed. Windows are 16:9 in image px, widened 10% around the components they hold, and clamped
to the illustration's own rectangle (x 40-1559, y 127-1174) so the board's margin never enters a dived frame. Rings are drawn after the
crop at the constant 5 px; a ring that would clip during a move waits until it is fully inside the frame.
"""
from pathlib import Path
import argparse, subprocess, sys, hashlib, json
import numpy as np, cv2, imageio_ffmpeg
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_embeddings_v5_retrofit as v5
from build_embeddings_v5_retrofit import (ROOT, LIVE, D, ASSETS, BG, TIMELINE, EVENTS, CLOSE, TOTAL, fr, sha, source_at, student_frame, render_state)
from editspec_build import Reader, CLOSE_PREHOLD, CLOSE_PUSH, W, H, FPS
from build_one_more_thing_review_repair import ring
from make_close_board import close_board_copy

OUT = ROOT / 'video-audit/embeddings-repair-2026-09-17-v6'
DEST = ROOT / 'Prompts/embeddings-v6.mp4'
TABLE = [5352, 6509]                      # output frames of the Inside a Real Model span (v4/v5)
PHOTO = [40, 127, 1559, 1174]             # the illustration's own rectangle on the 1600x1215 board (measured 2026-09-17)
TRANSIT, PULLBACK = 24, 30

def full_window(w, h):
    s = min(1220 / w, 680 / h); return [w / 2, h / 2, W / s]   # v4's full view: the board fit to 1220x680 on the house stage
def window(content, min_w=0):
    """A 16:9 window (cx, cy, width in image px) holding `content` [x0,y0,x1,y1] with a 10% margin, clamped inside the illustration."""
    x0, y0, x1, y1 = content; ww = max(x1 - x0, (y1 - y0) * W / H) * 1.10; ww = max(ww, min_w); hh = ww * H / W
    px0, py0, px1, py1 = PHOTO
    cx = min(max((x0 + x1) / 2, px0 + ww / 2), px1 - ww / 2); cy = min(max((y0 + y1) / 2, py0 + hh / 2), py1 - hh / 2)
    return [cx, cy, ww]

def build_camera(board):
    """Keyframes on the output timeline: (frame, window, transit frames to reach it). Between keyframes the camera holds."""
    h, w = board.shape[:2]; full = full_window(w, h); by = {e['label']: e for e in EVENTS}
    def at(label): return fr(by[label]['sf'] / FPS)   # source frame
    def out(sf):  # output frame for a source frame inside the table span's keep row
        t = next(t for t in TIMELINE if t['kind'] == 'source' and t['s'] <= sf < t['e']); return t['o0'] + sf - t['s']
    cat = window([124, 330, 375, 878])                 # cat card + token ID card (v4 rings cat-token, cat-token-id)
    row = window([487, 840, 1492, 945])                # the lookup row (v4 ring lookup-row)
    dims = window([440, 155, 1490, 421])                # EMBEDDING TABLE caption through DIMENSIONS caption + the d1..dn header (v4 ring dimension-columns); starts where v4's crop did so no caption is cut mid-word
    keys = [dict(f=TABLE[0], win=full, transit=0, label='establish'),
            dict(f=TABLE[0], win=[full[0], full[1], full[2] * 0.97], transit=out(at('cat-token')) - TABLE[0], label='establish-push'),
            dict(f=out(at('cat-token')), win=cat, transit=TRANSIT, label='to-cat'),
            dict(f=out(at('lookup-row')), win=row, transit=TRANSIT, label='to-row'),
            dict(f=out(at('dimension-columns')), win=dims, transit=TRANSIT, label='to-dims'),
            dict(f=out(at('learned-value')), win=full, transit=PULLBACK, label='pull-back')]
    return keys

def camera_at(keys, f):
    """Window at output frame f: smoothstep from the previous keyframe's window over `transit` frames, then hold."""
    prev = keys[0]['win']; cur = keys[0]['win']
    for k in keys:
        if f < k['f']: break
        q = 1.0 if k['transit'] == 0 else min(1.0, (f - k['f']) / k['transit']); q = q * q * (3 - 2 * q)
        cur = [p * (1 - q) + c * q for p, c in zip(prev, k['win'])]
        if q >= 1.0: prev = k['win']
    return cur

def table_frame(board, marks, win, settled):
    cx, cy, ww = win; hh = ww * H / W; x, y = cx - ww / 2, cy - hh / 2
    out = cv2.warpAffine(board, np.float32([[ww / W, 0, x], [0, hh / H, y]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_CONSTANT, borderValue=BG)
    drawn = []
    for m in marks:
        a, b, c, d = m['rect']; rr = [(a - x) * W / ww, (b - y) * H / hh, (c - x) * W / ww, (d - y) * H / hh]
        if min(rr[0], rr[1], W - rr[2], H - rr[3]) < 20:
            assert not settled, ('ring clips at a settled camera', m, rr); continue
        ring(out, rr, m['color']); drawn.append(rr)
    return out, drawn

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); (OUT / 'states').mkdir(exist_ok=True)
    protected = [LIVE, *ASSETS.values(), D / 'embeddings-close.jpg', ROOT / 'index.html', ROOT / 'lessons/embeddings.md']
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    assert close_board_copy('embeddings') == ('AI uses numbers to work with meaning.', 'Those numbers help AI recognize similarities and differences.')
    if not (OUT / 'close.png').exists():
        subprocess.run([str(ROOT / '.video-venv/bin/python'), str(ROOT / 'scripts/video/make_close_board.py'), '--lesson', 'embeddings', '--out', str(OUT / 'close.png')], check=True, stdout=subprocess.DEVNULL)
    boards = {k: cv2.imread(str(p)) for k, p in ASSETS.items()}; assert all(v is not None for v in boards.values())
    def choice(sf): return next(e for e in reversed(EVENTS) if e['sf'] <= sf)
    schedule = []; last = None
    for f in range(CLOSE):
        e = choice(source_at(f))
        if e['label'] != last:
            if schedule: schedule[-1]['end'] = f
            schedule.append(dict(e, start=f)); last = e['label']
    schedule[-1]['end'] = CLOSE
    assert [ (s['start'], s['end']) for s in schedule if s['board'] == 'table'][0][0] == TABLE[0] and [s['end'] for s in schedule if s['board'] == 'table'][-1] == TABLE[1]
    keys = build_camera(boards['table'])
    states = {}
    for e in schedule:
        if e['board'] in ('native', 'student', 'table'): continue
        states[e['label']] = render_state(e, boards); cv2.imwrite(str(OUT / 'states' / (e['label'] + '.jpg')), states[e['label']], [cv2.IMWRITE_JPEG_QUALITY, 92])
    # preview keyframes for the walk: each settled window (30 frames after its move ends) and each move's midpoint
    previews = []
    for k in keys[1:]:
        previews += [(k['f'] + k['transit'] // 2, f"{k['label']}-mid"), (min(k['f'] + k['transit'] + 30, TABLE[1] - 1), f"{k['label']}-settled")]
    previews += [(s['start'] + 30, s['label']) for s in schedule if s['board'] == 'table']; previews.append((TABLE[1] - 1, 'table-last'))
    def table_at(f, settled_check=True):
        e = next(s for s in schedule if s['start'] <= f < s['end']); assert e['board'] == 'table', f
        win = camera_at(keys, f); moving = any(k['f'] <= f < k['f'] + k['transit'] for k in keys[1:] if k['transit'])
        return table_frame(boards['table'], e['marks'], win, settled=settled_check and not moving)
    sheet = []
    for f, label in sorted(set(previews)):
        im, _ = table_at(f); cv2.imwrite(str(OUT / 'states' / f'table-{f:04d}-{label}.jpg'), im, [cv2.IMWRITE_JPEG_QUALITY, 92])
        c = cv2.resize(im, (640, 360)); cv2.putText(c, f'f{f} {label}', (8, 24), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 255), 2); sheet.append(c)
    while len(sheet) % 2: sheet.append(np.zeros_like(sheet[0]))
    cv2.imwrite(str(OUT / 'walk-sheet.jpg'), cv2.vconcat([cv2.hconcat(sheet[i:i + 2]) for i in range(0, len(sheet), 2)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
    boundaries = {}
    for i, e in enumerate(schedule):
        if i and e['board'] != schedule[i - 1]['board']: boundaries[e['start']] = e['label']
    boundaries[CLOSE] = 'standard-close'
    m = dict(scope='Review only; v5 (visual-only retrofit of the shipped v4) plus a camera walk over Inside a Real Model; live unchanged',
             retrofit_of=str(LIVE.relative_to(ROOT)), retrofit_of_sha256=hashes[str(LIVE.relative_to(ROOT))], audio_note='copied from the shipped v4 at mux (-c:a copy)',
             output=str(DEST), fps=FPS, total_frames=TOTAL, duration=TOTAL / FPS, close_start_frame=CLOSE, timeline=TIMELINE,
             states=[dict(start=e['start'], end=e['end'], board=e['board'], label=e['label'], marks=e['marks'], crop=None if e['board'] == 'table' else e['crop']) for e in schedule],
             table_camera=dict(span=TABLE, photo_rect=PHOTO, keyframes=keys, density='illustration camera walk with v4 rings'),
             student_camera=dict(zoom_in=[22.733333, 24.133333], hold=[24.133333, 29.266667], zoom_out=[29.266667, 30.166667], target_source_rect=[60, 675, 860, 1125]),
             assets={k: dict(path=str(p.relative_to(ROOT)), sha256=sha(p)) for k, p in ASSETS.items()},
             close=dict(asset='course-assets/embeddings/embeddings-close.jpg', sha256=hashes['course-assets/embeddings/embeddings-close.jpg'], prehold_frames=CLOSE_PREHOLD, push_frames=CLOSE_PUSH, zoom_endpoint=1.2, settled_frames=TOTAL - CLOSE - CLOSE_PREHOLD - CLOSE_PUSH),
             boundaries=[dict(frame=f, label=l) for f, l in sorted(boundaries.items())], protected_hashes=hashes)
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2))
    print('Prepared', TOTAL, 'frames; walk keyframes', [(k['f'], k['label'], k['transit'], [round(v) for v in k['win']]) for k in keys], flush=True)
    if args.prepare_only: return
    assert not DEST.exists(), f'{DEST} exists; version-suffix instead of overwriting'
    ff = imageio_ffmpeg.get_ffmpeg_exe(); ci = cv2.imread(str(OUT / 'close.png'))
    p = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0', '-i', str(LIVE), '-map', '0:v:0', '-map', '1:a:0',
                          '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    live = Reader(str(LIVE)); idx = 0
    for f in range(TOTAL):
        if f < CLOSE:
            while f >= schedule[idx]['end']: idx += 1
            e = schedule[idx]
            if e['board'] == 'native': im = live.at(f)
            elif e['board'] == 'student': im = student_frame(boards['student'], source_at(f))
            elif e['board'] == 'table': im, _ = table_at(f)
            else: im = states[e['label']]
        else:
            k = f - CLOSE; q = min(1, max(0, (k - CLOSE_PREHOLD) / (CLOSE_PUSH - 1))); z = 1 + .2 * q * q * (3 - 2 * q)
            hh_, ww_ = ci.shape[:2]; cw = ww_ / z; chh = cw * 9 / 16
            im = cv2.warpAffine(ci, np.float32([[cw / W, 0, (ww_ - cw) / 2], [0, chh / H, (hh_ - chh) / 2]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
        p.stdin.write(im.tobytes())
        if f % 1800 == 0: print('Rendered', f, '/', TOTAL, flush=True)
    p.stdin.close(); assert p.wait() == 0
    current = {k: sha(ROOT / k) for k in hashes}; m['protected_files_unchanged'] = {k: v == current[k] for k, v in hashes.items()}; assert all(m['protected_files_unchanged'].values())
    m['render_sha256'] = sha(DEST); (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2)); print(DEST, flush=True)

if __name__ == '__main__':
    main()
