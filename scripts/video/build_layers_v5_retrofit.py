#!/usr/bin/env python3
"""Layers v5: the current course boards and the canonical close, as a visual-only retrofit of the shipped v4 (2026-09-17). Review only.

The shipped file (course-assets/layers/layers.mp4, 4767 frames) is v4 (build_layers_v4.py, 2026-09-10). Its rolls (Prompts/layers-1.mp4,
-2.mp4) and its audit folder (with the generated tracing illustration and the composed close) no longer exist, so this build takes the
finished v4 as its picture source, re-renders the three course-board spans from the current course-assets JPGs (same dimensions as the
renders v4 used; the site credit line, and the 2026-09-15 title-banner standardization on How Layers Update the Numbers, are the
differences) with v4's exact schedule (the same edit timeline, donor visual holds and maps, events, static full views fit to 1230x670, and
rings at the same frames), replaces the close with the canonical closing JPG (make_close_board.py --lesson layers), and muxes v4's
original audio stream back in untouched. Every Notebook, donor-roll, and generated-illustration span is v4's picture. Spans on the
output timeline: horse [223, 766); stack [1043, 1830); it [2337, 3071); close [4511, 4767).
"""
from pathlib import Path
import argparse, subprocess, sys, hashlib, json
import numpy as np, cv2, imageio_ffmpeg
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Reader, CLOSE_PREHOLD, CLOSE_PUSH, W, H, FPS
from build_one_more_thing_review_repair import ring
from make_close_board import close_board_copy

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/layers/layers.mp4'   # the shipped v4
OUT = ROOT / 'video-audit/layers-repair-2026-09-17'
DEST = ROOT / 'Prompts/layers-v5.mp4'
D = ROOT / 'course-assets/layers'
ASSETS = {'horse': D / 'layers-horse-three-reads.jpg', 'stack': D / 'layers-inside-layer.jpg', 'it': D / 'layers-resolves-it.jpg'}
NEUTRAL, EP, BLUE, TEAL = '#6e51ff', '#4f2fc4', '#1652f0', '#0e8f86'
BG = (251, 245, 246)
def fr(t): return round(t * FPS)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# ---- v4's edit timeline (source seconds of roll 1, donor spans from roll 2) -> output frames
TIMELINE = []; cursor = 0
def keep(n, a, b, label, visual_hold=None, visual_map=None):
    global cursor; s, e = fr(a), fr(b); t = dict(kind='source', src=n, s=s, e=e, o0=cursor, o1=cursor + e - s, label=label)
    if visual_hold is not None: t['hold'] = fr(visual_hold)
    if visual_map is not None: t['map'] = visual_map
    TIMELINE.append(t); cursor += e - s
def pause(sec, label, hold):
    global cursor; n = fr(sec); TIMELINE.append(dict(kind='hold', hold=fr(hold), o0=cursor, o1=cursor + n, label=label)); cursor += n
keep(1, 0, 6.433333, 'Original Notebook rereading hook'); pause(1, 'Pause before horse example', 6.4)
keep(1, 16.7, 43.033333, 'Horse example and rereading; redundant AI preview removed'); pause(1, 'Pause before neural network', 43)
keep(1, 43.2, 85.333333, 'Layer mechanics and bridge to IT'); pause(1, 'Pause before IT sentence', 85.3)
keep(1, 86.733333, 91.266667, 'Read CAT and IT sentence directly; Test Sentence removed')
keep(2, 77.5, 83.4, 'Accurate START explanation from version 2', visual_hold=91.3)
keep(2, 83.4, 92.6, 'Layers 1 and 2 build the connection over successive layers', visual_map=[[fr(83.4), fr(96.133333)], [fr(85.26), fr(98.4)], [fr(90.7), fr(100.6)]])
keep(1, 100.833333, 112.8, 'Result and contextual connections'); pause(1, 'Pause before layer count', 112.766667)
keep(1, 115.666667, 154.533333, 'Layer-count question directly; depth and computing tradeoff without added pause'); pause(1, 'Pause before closing message', 154.5)
CLOSE = cursor; keep(1, 154.633333, 162.166667, 'Closing narration'); pause(1, 'Settled standard close', 162.133333); TOTAL = cursor
assert (CLOSE, TOTAL) == (4511, 4767), (CLOSE, TOTAL)

def source_at(f):
    t = next(t for t in TIMELINE if t['o0'] <= f < t['o1'])
    if t['kind'] == 'hold': return t['hold']
    sf = t['s'] + f - t['o0']
    if 'map' in t: return next(v for a, v in reversed(t['map']) if sf >= a)
    return t.get('hold', sf)

# ---- v4's events (roll-1 seconds); 'native'/'human'/'book'/'tracing' spans take the shipped picture
def mark(rect, color): return dict(rect=rect, color=color, highlight_source='neutral_video_purple' if color == NEUTRAL else 'card_locked_accent')
EVENTS = []
def ev(t, key, label, rect=None, color=NEUTRAL): EVENTS.append(dict(sf=fr(t), board=key, label=label, marks=[] if rect is None else [mark(rect, color)]))
ev(0, 'native', 'notebook-opening')
ev(16.7, 'horse', 'horse-establish')
ev(19.6, 'horse', 'horse-spoken-title', [35, 28, 1190, 113], NEUTRAL)
ev(22.16, 'horse', 'horse-first-read', [80, 140, 538, 782], EP)
ev(24.58, 'horse', 'horse-more-reads', [571, 140, 1029, 782], BLUE)
ev(30.3, 'horse', 'horse-meaning-clicks', [1062, 140, 1520, 782], TEAL)
ev(34.8, 'native', 'notebook-rereading')
ev(38.566667, 'native', 'notebook-horse-sentence-animation')
ev(43.2, 'stack', 'stack-establish')
ev(52.76, 'stack', 'attention-and-transformation', [303, 155, 735, 738], NEUTRAL)
ev(58.46, 'stack', 'pass-updated-numbers-onward')
ev(61.24, 'stack', 'starting-number-row', [75, 861, 390, 991], EP)
ev(64.22, 'stack', 'after-one-layer', [454, 861, 769, 991], EP)
ev(65.8, 'stack', 'after-many-layers', [833, 861, 1148, 991], EP)
ev(67.1, 'stack', 'final-number-row', [1212, 861, 1527, 991], EP)
ev(69.433333, 'native', 'notebook-book-rereading')
ev(78.466667, 'native', 'tracing-one-word-illustration')
ev(85.5, 'it', 'it-establish')
ev(86.94, 'it', 'cat-it-sentence', [80, 157, 1520, 289], NEUTRAL)
ev(91.3, 'it', 'it-start-ambiguous', [80, 330, 352, 754], EP)
ev(96.133333, 'it', 'it-layer-one', [372, 330, 645, 754], EP)
ev(98.4, 'it', 'it-layer-two', [664, 330, 936, 754], EP)
ev(100.6, 'it', 'it-repeat', [956, 330, 1228, 754], EP)
ev(100.8, 'it', 'it-result', [1249, 330, 1521, 754], EP)
ev(105.666667, 'native', 'notebook-connections-and-scale')

def render(im, marks):
    h, w = im.shape[:2]; s = min(1230 / w, 670 / h); x, y = (W - w * s) / 2, (H - h * s) / 2
    out = cv2.warpAffine(im, np.float32([[s, 0, x], [0, s, y]]), (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_CONSTANT, borderValue=BG)
    for m in marks:
        a, b, c, d = m['rect']; r = [a * s + x, b * s + y, c * s + x, d * s + y]; assert min(r[0], r[1], W - r[2], H - r[3]) >= 24, (m, r)
        ring(out, r, m['color']); m['output_rect'] = r; m['ring_width'] = 5
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); (OUT / 'states').mkdir(exist_ok=True)
    protected = [LIVE, *ASSETS.values(), D / 'layers-close.jpg', ROOT / 'index.html', ROOT / 'lessons/layers.md']
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    assert close_board_copy('layers') == ('Meaning builds up, layer by layer.', 'Attention and transformation. Dozens of times.')
    if not (OUT / 'close.png').exists():
        subprocess.run([str(ROOT / '.video-venv/bin/python'), str(ROOT / 'scripts/video/make_close_board.py'), '--lesson', 'layers', '--out', str(OUT / 'close.png')], check=True, stdout=subprocess.DEVNULL)
    boards = {k: cv2.imread(str(p)) for k, p in ASSETS.items()}; assert all(v is not None for v in boards.values())
    def choice(sf): return next(e for e in reversed(EVENTS) if e['sf'] <= sf)
    schedule = []; last = None
    for f in range(CLOSE):
        e = choice(source_at(f))
        if e['label'] != last:
            if schedule: schedule[-1]['end'] = f
            schedule.append(dict(e, start=f)); last = e['label']
    schedule[-1]['end'] = CLOSE
    states = {}
    for e in schedule:
        if e['board'] == 'native': continue
        states[e['label']] = render(boards[e['board']], e['marks']); cv2.imwrite(str(OUT / 'states' / (e['label'] + '.jpg')), states[e['label']], [cv2.IMWRITE_JPEG_QUALITY, 92])
    boundaries = {}
    for i, e in enumerate(schedule):
        if i and e['board'] != schedule[i - 1]['board']: boundaries[e['start']] = e['label']
    boundaries[CLOSE] = 'standard-close'
    m = dict(scope='Review only; visual-only retrofit of the shipped v4 (current course boards + canonical close); live unchanged',
             retrofit_of=str(LIVE.relative_to(ROOT)), retrofit_of_sha256=hashes[str(LIVE.relative_to(ROOT))], audio_note='copied from the shipped v4 at mux (-c:a copy)',
             output=str(DEST), fps=FPS, total_frames=TOTAL, duration=TOTAL / FPS, close_start_frame=CLOSE, timeline=TIMELINE,
             states=[dict(start=e['start'], end=e['end'], board=e['board'], label=e['label'], marks=e['marks']) for e in schedule],
             camera='v4: static full view, board fit to 1230x670 on the house stage; no dives',
             board_dimensions={k: list(v.shape[1::-1]) for k, v in boards.items()}, assets={k: dict(path=str(p.relative_to(ROOT)), sha256=sha(p)) for k, p in ASSETS.items()},
             close=dict(asset='course-assets/layers/layers-close.jpg', sha256=hashes['course-assets/layers/layers-close.jpg'], prehold_frames=CLOSE_PREHOLD, push_frames=CLOSE_PUSH, zoom_endpoint=1.2, settled_frames=TOTAL - CLOSE - CLOSE_PREHOLD - CLOSE_PUSH),
             boundaries=[dict(frame=f, label=l) for f, l in sorted(boundaries.items())], protected_hashes=hashes)
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2))
    print('Prepared', TOTAL, 'frames; spans', [(e['start'], e['end'], e['label']) for e in schedule if e['board'] != 'native'], flush=True)
    if args.prepare_only: return
    assert not DEST.exists(), f'{DEST} exists; version-suffix instead of overwriting'
    ff = imageio_ffmpeg.get_ffmpeg_exe(); ci = cv2.imread(str(OUT / 'close.png'))
    p = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0', '-i', str(LIVE), '-map', '0:v:0', '-map', '1:a:0',
                          '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    live = Reader(str(LIVE)); idx = 0
    for f in range(TOTAL):
        if f < CLOSE:
            while f >= schedule[idx]['end']: idx += 1
            e = schedule[idx]; im = live.at(f) if e['board'] == 'native' else states[e['label']]
        else:
            k = f - CLOSE; q = min(1, max(0, (k - CLOSE_PREHOLD) / (CLOSE_PUSH - 1))); z = 1 + .2 * q * q * (3 - 2 * q)
            hh_, ww_ = ci.shape[:2]; cw = ww_ / z; chh = cw * 9 / 16
            im = cv2.warpAffine(ci, np.float32([[cw / W, 0, (ww_ - cw) / 2], [0, chh / H, (hh_ - chh) / 2]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
            if k in [0, CLOSE_PREHOLD, CLOSE_PREHOLD + CLOSE_PUSH - 1, TOTAL - CLOSE - 1]: cv2.imwrite(str(OUT / 'states' / f'close-{k}.jpg'), im, [cv2.IMWRITE_JPEG_QUALITY, 92])
        p.stdin.write(im.tobytes())
        if f % 1800 == 0: print('Rendered', f, '/', TOTAL, flush=True)
    p.stdin.close(); assert p.wait() == 0
    current = {k: sha(ROOT / k) for k in hashes}; m['protected_files_unchanged'] = {k: v == current[k] for k, v in hashes.items()}; assert all(m['protected_files_unchanged'].values())
    m['render_sha256'] = sha(DEST); (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2)); print(DEST, flush=True)

if __name__ == '__main__':
    main()
