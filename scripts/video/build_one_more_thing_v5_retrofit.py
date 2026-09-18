#!/usr/bin/env python3
"""One More Thing v5: the current course boards and the canonical close, as a visual-only retrofit of the shipped v4 (2026-09-18). Review only.

The shipped file (course-assets/one-more-thing/one-more-thing.mp4, 6502 frames) is the v4 "engaging visuals" candidate of 2026-09-09
(build_one_more_thing_review_repair.py --engaging-visuals: three static board canvases with outline rings that change at spoken
events, Notebook motion graphics kept in three spans, four pauses and one join, standard close). The raw roll (Prompts/one-more-thing-2.mp4)
no longer exists, so this build takes the finished file as its picture source, re-renders the three board canvases from the current
course-assets JPGs with the shipped script's exact event list (same source times, rects, accents; the boards kept their pixel
dimensions, and every rect was checked against the current files), replays the shipped timeline so every state lands on the same
output frames, keeps the three Notebook spans as the shipped picture, replaces the close with the canonical closing JPG
(make_close_board.py --lesson inference), and muxes the shipped audio stream back in untouched.
"""
from pathlib import Path
import argparse, subprocess, sys, json, hashlib
import numpy as np, cv2, imageio_ffmpeg
sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_close_board import close_board_copy

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/one-more-thing/one-more-thing.mp4'
OUT = ROOT / 'video-audit/one-more-thing-repair-2026-09-18'
DEST = ROOT / 'Prompts/one-more-thing-v5.mp4'
D = ROOT / 'course-assets/one-more-thing'
A = dict(probability=D / 'one-more-thing-draws.jpg', temperature=D / 'one-more-thing-temperature.jpg', math=D / 'one-more-thing-bill.jpg')
FPS, SR, W, H = 30, 48000, 1280, 720
PURPLE, EDITORIAL, BLUE, RED, TEAL = '#6e51ff', '#4f2fc4', '#1652f0', '#c41f28', '#0e8f86'
BG = (251, 245, 246)   # BGR #f6f5fb, the shipped stage color
PREHOLD, PUSH = 48, 150
SHIPPED_SHA = '8ab2b18178c231dcca34ef6b342b0c17c9548f895ecb1ed36c1ccd65999584a0'
# the shipped Notebook spans on the output timeline (v4 edit-manifest visual_clips; scene cuts re-detected on the live file)
CLIPS = [(0, 1034, 'Original opening and dog-prompt animation'), (2977, 3227, 'Notebook temperature dial'), (4502, 5110, 'Original weights and computation animation')]

def frame(t): return round(t * FPS)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def bgr(h): return tuple(int(h[i:i + 2], 16) for i in (5, 3, 1))

class Reader:
    def __init__(self, p): self.c = cv2.VideoCapture(str(p)); self.n = -1; self.im = None
    def at(self, n):
        assert n >= self.n, (n, self.n)
        while self.n < n:
            ok, self.im = self.c.read(); assert ok, n; self.n += 1
        return self.im.copy()

def ring(img, rect, color, radius=10):
    x0, y0, x1, y1 = map(round, rect); c = bgr(color); r = min(radius, (x1 - x0) // 2, (y1 - y0) // 2)
    for a, b in [((x0 + r, y0), (x1 - r, y0)), ((x0 + r, y1), (x1 - r, y1)), ((x0, y0 + r), (x0, y1 - r)), ((x1, y0 + r), (x1, y1 - r))]:
        cv2.line(img, a, b, c, 5, cv2.LINE_AA)
    for center, start in [((x0 + r, y0 + r), 180), ((x1 - r, y0 + r), 270), ((x1 - r, y1 - r), 0), ((x0 + r, y1 - r), 90)]:
        cv2.ellipse(img, center, (r, r), 0, start, start + 90, c, 5, cv2.LINE_AA)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); (OUT / 'states').mkdir(exist_ok=True)
    assert sha(LIVE) == SHIPPED_SHA, 'live file is not the 2026-09-09 ship'
    protected = [LIVE, ROOT / 'lessons/one-more-thing.md', D / 'one-more-thing-close.jpg', *A.values()]; hashes = {str(p): sha(p) for p in protected}
    assert close_board_copy('inference') == ('Not a mind. Math, at a scale nobody can picture.', 'Every time you hit send.')

    # ---- the shipped timeline (audio is copied from the shipped file at mux; only the output-frame mapping is replayed)
    timeline = []; cursor = 0
    def keep(a, b, label):
        nonlocal cursor
        start, end = frame(a), frame(b); count = end - start
        timeline.append(dict(kind='source', label=label, source_start=start, source_end=end, start_frame=cursor, end_frame=cursor + count)); cursor += count
    def pause(seconds, label, source_hold):
        nonlocal cursor
        count = frame(seconds); timeline.append(dict(kind='room_tone', label=label, source_hold=source_hold, start_frame=cursor, end_frame=cursor + count)); cursor += count
    keep(0, 98.233333, 'Probability explanation'); pause(1, 'Pause before temperature', 98.2)
    keep(98.233333, 119, 'Temperature and low-temperature example'); pause(1, 'Pause before high temperature', 118.95)
    keep(133.966667, 161.933333, 'High temperature and fixed weights'); pause(1, 'Pause before computation', 161.9)
    keep(170.966667, 205.7, 'Computation example'); pause(.366667, 'Join after repeated one-word calculation cut', 205.65)
    keep(212.233333, 234.9, 'Scale to 100 and 1000 newly written tokens'); pause(1, 'Pause before closing message', 234.85)
    close_start = cursor
    keep(237.8, 243, 'Approved closing narration'); pause(2.8, 'Closing settled hold', 243)
    total = cursor; assert (total, close_start) == (6502, 6262), (total, close_start)

    # ---- the shipped event list (engaging-visuals variant), rects in board pixels; boards kept their 1600-wide dimensions
    def mark(rect, color=EDITORIAL): return dict(rect=rect, color=color, highlight_source='neutral_video_purple' if color == PURPLE else 'card_locked_accent')
    events = []
    def event(t, board, label, *marks): events.append(dict(source_time=t, board=board, label=label, marks=list(marks)))
    event(0, 'probability', 'probability-overview')
    event(23.3, 'probability', 'answer-so-far', mark([80, 150, 1520, 236], PURPLE))
    event(27.7, 'probability', 'probability-list', mark([76, 266, 676, 710], EDITORIAL))
    event(38.75, 'probability', 'spot-22', mark([96, 362, 650, 410], EDITORIAL))
    event(47.35, 'probability', 'not-guaranteed', mark([40, 782, 1560, 870], PURPLE))
    event(50.04, 'probability', 'expected-frequency', mark([96, 362, 650, 410], EDITORIAL))
    event(56.3, 'probability', 'five-separate-tries', mark([936, 266, 1540, 694], EDITORIAL))
    for t, n in [(66.65, 0), (67.2, 1), (67.78, 2), (68.33, 3), (68.95, 4)]:
        y = 362 + n * 64; event(t, 'probability', f'try-{n + 1}', mark([956, y, 1520, y + 52], EDITORIAL))
    event(70.34, 'probability', 'separate-outcomes', mark([936, 266, 1540, 694], EDITORIAL))
    event(78, 'probability', 'why-variety')
    event(80.36, 'probability', 'always-top-choice', mark([96, 362, 650, 410], EDITORIAL))
    event(85.3, 'probability', 'other-likely-choices', mark([80, 418, 670, 637], EDITORIAL))
    event(90.14, 'probability', 'choice-shapes-context', mark([80, 150, 1520, 236], PURPLE))
    event(97.9, 'probability', 'probability-settle')
    event(98.4, 'temperature', 'temperature-title', mark([29, 33, 999, 116], PURPLE))
    event(113.2, 'temperature', 'spot-temperature-comparison', mark([330, 383, 715, 456], EDITORIAL), mark([733, 383, 1118, 456], BLUE))
    event(134.1, 'temperature', 'high-temperature', mark([1135, 283, 1520, 826], RED))
    event(145.1, 'temperature', 'other-combined-comparison', mark([330, 748, 715, 826], EDITORIAL), mark([1135, 748, 1520, 826], RED))
    event(154.32, 'temperature', 'temperature-takeaway', mark([40, 905, 1560, 994], PURPLE))
    event(161.9, 'temperature', 'temperature-settle')
    event(171.1, 'math', 'math-title', mark([26, 16, 632, 98], PURPLE))
    event(178.4, 'math', 'weights-per-token', mark([40, 118, 525, 722], BLUE))
    event(194.24, 'math', 'one-token-cost', mark([40, 118, 525, 722], BLUE))
    event(212.3, 'math', 'scaling-overview')
    event(216.48, 'math', 'short-answer', mark([557, 118, 1043, 722], EDITORIAL))
    event(221.46, 'math', 'longer-conversation', mark([1075, 118, 1560, 722], TEAL))
    event(230.12, 'math', 'new-output-tokens')
    event(234.8, 'math', 'math-settle')
    event(34.466667, 'probability', 'probability-establish')
    event(35.1, 'probability', 'probability-list-on-return', mark([76, 266, 676, 710], EDITORIAL))
    event(106.566667, 'temperature', 'temperature-establish')
    event(106.95, 'temperature', 'starting-versus-low-on-return', mark([330, 283, 715, 826], EDITORIAL), mark([733, 283, 1118, 826], BLUE))
    event(191.333333, 'math', 'math-establish')
    events.sort(key=lambda e: e['source_time'])

    def source_at(f):
        for part in timeline:
            if part['start_frame'] <= f < part['end_frame']:
                return (part['source_start'] + f - part['start_frame']) / FPS if part['kind'] == 'source' else part['source_hold']
        raise ValueError(f)
    def choice(t): return next(e for e in reversed(events) if frame(e['source_time']) <= frame(t))
    schedule = []; last = None
    for f in range(close_start):
        e = choice(source_at(f)); key = e['label']
        if key != last:
            if schedule: schedule[-1]['end_frame'] = f
            schedule.append(dict(e, start_frame=f)); last = key
    schedule[-1]['end_frame'] = close_start
    shipped = json.load(open(OUT / 'shipped-v4-edit-manifest.json'))['states']   # recovered from git (28ddced^) for the parity check
    assert [(s['start_frame'], s['end_frame'], s['board'], s['label']) for s in schedule] == [(s['start_frame'], s['end_frame'], s['board'], s['label']) for s in shipped], 'schedule drifted from the shipped v4'

    # ---- board canvases: the shipped fit (1220x680 centered on the stage color), current JPG pixels
    boards = {k: cv2.imread(str(p)) for k, p in A.items()}; layouts = {}; bases = {}
    for k, im in boards.items():
        assert im is not None; h, w = im.shape[:2]; s = min(1220 / w, 680 / h); nw, nh = round(w * s), round(h * s); x, y = (W - nw) // 2, (H - nh) // 2
        canvas = np.full((H, W, 3), BG, np.uint8); canvas[y:y + nh, x:x + nw] = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_AREA); bases[k] = canvas; layouts[k] = (s, x, y)
    states = {}
    for row in schedule:
        k = row['board']; im = bases[k].copy(); s, x, y = layouts[k]
        for m in row['marks']:
            rr = [x + m['rect'][0] * s, y + m['rect'][1] * s, x + m['rect'][2] * s, y + m['rect'][3] * s]
            assert min(rr[:2]) >= 24 and rr[2] <= W - 24 and rr[3] <= H - 24, (row['label'], rr)
            ring(im, rr, m['color']); m['output_rect'] = [round(v, 2) for v in rr]; m['ring_width'] = 5
        states[row['label']] = im; cv2.imwrite(str(OUT / 'states' / f"{row['label']}.png"), im)
    labels = list(states)
    for page in range(0, len(labels), 9):
        cells = []
        for name in labels[page:page + 9]:
            tile = cv2.copyMakeBorder(cv2.resize(states[name], (426, 240)), 24, 0, 0, 0, cv2.BORDER_CONSTANT, value=(255, 255, 255))
            cv2.putText(tile, name, (7, 16), cv2.FONT_HERSHEY_SIMPLEX, .42, (50, 35, 25), 1, cv2.LINE_AA); cells.append(tile)
        while len(cells) % 3: cells.append(np.full_like(cells[0], 255))
        cv2.imwrite(str(OUT / f'states-sheet-{page // 9}.jpg'), cv2.vconcat([cv2.hconcat(cells[n:n + 3]) for n in range(0, len(cells), 3)]))

    # ---- canonical close
    if not (OUT / 'close.png').exists():
        subprocess.run([str(ROOT / '.video-venv/bin/python'), str(ROOT / 'scripts/video/make_close_board.py'), '--lesson', 'inference', '--out', str(OUT / 'close.png')], check=True, stdout=subprocess.DEVNULL)
    close = cv2.imread(str(OUT / 'close.png'))
    manifest = dict(output=str(DEST), source=str(LIVE), retrofit_of_sha256=SHIPPED_SHA, fps=FPS, total_frames=total, duration=total / FPS, timeline=timeline, states=schedule,
                    close_start_frame=close_start, visual_clips=[dict(start_frame=a, end_frame=b, label=l, picture='shipped file, same output frames') for a, b, l in CLIPS],
                    highlight_style='outline_only', close_camera=dict(prehold_frames=PREHOLD, push_frames=PUSH, settled_frames=total - close_start - PREHOLD - PUSH, zoom_endpoint=1.2),
                    assets={k: dict(path=str(p.relative_to(ROOT)), sha256=sha(p)) for k, p in A.items()}, close_asset=dict(path='course-assets/one-more-thing/one-more-thing-close.jpg', sha256=sha(D / 'one-more-thing-close.jpg')),
                    audio_note='copied from the shipped file at mux (-c:a copy)', protected_hashes=hashes,
                    scope='Review only; visual-only retrofit of the shipped 2026-09-09 file (current course boards + canonical close); live unchanged')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Prepared {len(schedule)} states; {total} frames; close {close_start}', flush=True)
    if args.prepare_only: return

    assert not DEST.exists(), f'{DEST} exists; version-suffix instead of overwriting'
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0', '-i', str(LIVE), '-map', '0:v:0', '-map', '1:a:0',
                             '-c:v', 'libx264', '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    live = Reader(LIVE); idx = 0
    for f in range(total):
        if f < close_start:
            while f >= schedule[idx]['end_frame']: idx += 1
            im = states[schedule[idx]['label']]
            if any(a <= f < b for a, b, _ in CLIPS): im = live.at(f)
        else:
            local = f - close_start; progress = min(1, max(0, (local - PREHOLD) / (PUSH - 1))); eased = progress * progress * (3 - 2 * progress); zoom = 1 + .2 * eased
            h, w = close.shape[:2]; ww = w / zoom; hh = ww * 9 / 16
            im = cv2.warpAffine(close, np.float32([[ww / W, 0, (w - ww) / 2], [0, hh / H, (h - hh) / 2]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
            if local in (0, PREHOLD, PREHOLD + PUSH - 1, total - close_start - 1): cv2.imwrite(str(OUT / 'states' / f'close-{local}.png'), im)
        proc.stdin.write(im.tobytes())
        if f % 1800 == 0: print('Rendered', f, '/', total, flush=True)
    proc.stdin.close(); assert proc.wait() == 0
    m = json.load(open(OUT / 'edit-manifest.json')); m['render_sha256'] = sha(DEST); m['protected_files_unchanged'] = {k: sha(k) == v for k, v in hashes.items()}; assert all(m['protected_files_unchanged'].values())
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2) + '\n'); print(DEST, flush=True)

if __name__ == '__main__':
    main()
