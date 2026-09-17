#!/usr/bin/env python3
"""Embeddings v5: the current course boards and the canonical close, as a visual-only retrofit of the shipped v4 (2026-09-17). Review only.

The shipped file (course-assets/embeddings/embeddings.mp4, 7145 frames) is v4 (build_embeddings_v4.py, 2026-09-10). Its rolls
(Prompts/embeddings-1.mp4, embeddings-2.mp4) no longer exist, so this build takes the finished file as its picture source,
re-renders the five course-board spans from the current course-assets JPGs (the website-credit line is the difference from the
pre-attribution renders v4 carried; the student-ID illustration is unchanged) with v4's exact schedule (the same edit timeline
mapping output frames to the rolls' seconds, the same events, the same crops, rings, and student-ID camera move at the same source
frames), replaces the close with the canonical closing JPG through make_close_board.py, and muxes v4's original audio stream back
in untouched. Every Notebook span is v4's picture. Spans on the output timeline: student [561, 1171); ratings [1518, 2776);
citrus [2776, 3741); comparison [3881, 5187); table [5352, 6509); close [6891, 7145).
"""
from pathlib import Path
import argparse, subprocess, sys, hashlib, json
import numpy as np, cv2, imageio_ffmpeg
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Reader, CLOSE_PREHOLD, CLOSE_PUSH, W, H, FPS
from build_one_more_thing_review_repair import ring
from make_close_board import close_board_copy

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/embeddings/embeddings.mp4'   # the shipped v4, sha256 adb23d034b23…
OUT = ROOT / 'video-audit/embeddings-repair-2026-09-17'
DEST = ROOT / 'Prompts/embeddings-v5.mp4'
D = ROOT / 'course-assets/embeddings'
ASSETS = {'student': D / 'embeddings-student-id.jpg', 'ratings': D / 'embeddings-meaning-row.jpg', 'citrus': D / 'embeddings-new-dimension.jpg',
          'comparison': D / 'embeddings-taste-test-to-ai.jpg', 'table': D / 'embeddings-inside-real-model.jpg'}
PURPLE, EP, BLUE, TEAL, GREEN, RED, AMBER = '#6e51ff', '#4f2fc4', '#1652f0', '#0e8f86', '#0f7a4a', '#c41f28', '#a9760c'
BG = (251, 245, 246)
def fr(t): return round(t * FPS)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# v4's edit timeline (source seconds of roll 2, then roll 1 for the close line; pauses hold the frame before them) -> output frames
TIMELINE = []; cursor = 0
def keep(a, b, label):
    global cursor; s, e = fr(a), fr(b); TIMELINE.append(dict(kind='source', label=label, s=s, e=e, o0=cursor, o1=cursor + e - s)); cursor += e - s
def pause(sec, label, hold):
    global cursor; n = fr(sec); TIMELINE.append(dict(kind='hold', label=label, hold=fr(hold), o0=cursor, o1=cursor + n)); cursor += n
keep(0, 49.6, 'Original opening, student ID and descriptive numbers'); pause(1, 'Pause before taste test', 49.566667)
keep(50, 102.733333, 'Taste test, terms and matching profiles'); keep(104.866667, 125.233333, 'Why add Citrus'); pause(1, 'Pause before applying to AI', 125.2)
keep(134.566667, 139.233333, 'AI uses the numerical-profile idea'); keep(143.5, 191.533333, 'AI comparison and embedding definition'); pause(1, 'Pause before table walkthrough', 191.5)
keep(191.533333, 229.433333, 'Inside a Real Model'); pause(.4, 'Join after embedding definition', 229.4)
keep(234.766667, 246.766667, 'Word pieces receive embeddings'); pause(1, 'Pause before closing', 246.733333)
CLOSE = cursor
keep(189.633333, 195.566667, 'Exact closing narration from version 1 (donor)'); pause(2.533333, 'Closing settled hold', 246.733333)
TOTAL = cursor
assert (CLOSE, TOTAL) == (6891, 7145), (CLOSE, TOTAL)

def source_at(f):
    t = next(t for t in TIMELINE if t['o0'] <= f < t['o1']); return t['s'] + f - t['o0'] if t['kind'] == 'source' else t['hold']

# v4's events (source seconds of roll 2); 'native' spans take the shipped picture
def mark(r, c=PURPLE): return dict(rect=r, color=c, highlight_source='neutral_video_purple' if c == PURPLE else 'card_locked_accent')
EVENTS = []
def event(t, board, label, *marks, crop=None): EVENTS.append(dict(sf=fr(t), board=board, label=label, marks=list(marks), crop=crop))
event(0, 'native', 'native-opening')
event(18.7, 'student', 'student-id-camera')
event(39.033333, 'native', 'native-id-and-characteristics')
event(50, 'ratings', 'ratings-establish')
event(55.72, 'ratings', 'ratings-scale', mark([593, 137, 1010, 196]))
event(64.06, 'ratings', 'coke-sweet', mark([80, 284, 1520, 458]))
event(64.92, 'ratings', 'coke-sweet-value', mark([443, 322, 543, 421], RED))
event(66.64, 'ratings', 'coke-sweet-and-fizz', mark([443, 322, 543, 421], RED), mark([817, 322, 918, 421], BLUE))
event(69.68, 'ratings', 'coffee-bitter-value', mark([630, 513, 731, 612], TEAL))
event(71.26, 'ratings', 'coffee-bitter-and-caffeine', mark([630, 513, 731, 612], TEAL), mark([1190, 513, 1291, 612], EP))
event(73.12, 'ratings', 'ratings-profile')
event(78.36, 'ratings', 'vector-whole-row', mark([80, 284, 1520, 458]))
event(82.76, 'ratings', 'dimension-headings', mark([425, 215, 560, 276], RED), mark([610, 215, 752, 276], TEAL))
event(88.86, 'ratings', 'one-value', mark([443, 322, 543, 421], RED))
event(91.933333, 'citrus', 'citrus-establish')
event(94, 'citrus', 'pepsi-row', mark([80, 475, 1520, 648]))
event(100.02, 'citrus', 'matching-six', mark([420, 309, 1342, 433]), mark([420, 500, 1342, 624]))
event(111.22, 'citrus', 'new-citrus-column', mark([1360, 188, 1510, 272], GREEN))
event(115.02, 'citrus', 'pepsi-citrus', mark([1390, 512, 1490, 612], GREEN))
event(117.1, 'citrus', 'coke-citrus', mark([1390, 322, 1490, 422], GREEN))
event(118.96, 'citrus', 'citrus-takeaway', mark([40, 909, 1560, 997]))
event(134.566667, 'native', 'native-bridge-to-ai')
event(143.5, 'comparison', 'comparison-establish')
event(148.42, 'comparison', 'three-drinks', mark([438, 262, 943, 344], TEAL))
event(152.38, 'comparison', 'every-token', mark([998, 250, 1503, 348], EP))
event(159.86, 'comparison', 'thousands-dimensions', mark([998, 382, 1503, 441], EP))
event(165.76, 'comparison', 'human-ratings', mark([438, 511, 943, 570], TEAL))
event(168.24, 'comparison', 'learned-in-training', mark([998, 468, 1503, 610], EP))
event(173.72, 'comparison', 'dimension-labels', mark([998, 722, 1503, 820], EP))
event(179.48, 'comparison', 'patterns-of-use', mark([998, 639, 1503, 698], EP))
event(184.02, 'comparison', 'values-work-together', mark([998, 722, 1503, 820], EP))
event(187.033333, 'native', 'native-embedding-row')
event(191.533333, 'table', 'table-establish')
event(197, 'table', 'cat-token', mark([124, 330, 375, 580], EP), crop=[80, 300, 1540, 990])
event(200.86, 'table', 'cat-token-id', mark([140, 633, 353, 878], EP), crop=[80, 300, 1540, 990])
event(205.24, 'table', 'lookup-row', mark([487, 840, 1492, 945], EP), crop=[80, 300, 1540, 990])
event(213.64, 'table', 'dimension-columns', mark([765, 351, 1490, 421], EP), crop=[450, 155, 1550, 1000])
event(219.6, 'table', 'learned-value', mark([772, 851, 877, 940], AMBER), mark([90, 1020, 462, 1170], AMBER))
event(225.4, 'table', 'embedding-complete-row', mark([765, 850, 1491, 941], TEAL), mark([940, 1020, 1440, 1170], TEAL))
event(235.033333, 'native', 'original-word-piece-animation')
EVENTS.sort(key=lambda e: e['sf'])

def student_frame(src, source_frame):
    """v4's smooth camera move toward the two spoken IDs, then back to the whole scene."""
    t = source_frame / FPS
    if t < 22.733333: q = 0
    elif t < 24.133333: q = (t - 22.733333) / 1.4
    elif t < 29.266667: q = 1
    elif t < 30.166667: q = 1 - (t - 29.266667) / .9
    else: q = 0
    q = min(1, max(0, q)); q = q * q * (3 - 2 * q)
    h, w = src.shape[:2]; scale = min(1220 / w, 680 / h)
    full = np.array([(w - W / scale) / 2, (h - H / scale) / 2, W / scale, H / scale])
    target = np.array([60., 675., 800., 450.]); x, y, ww, hh = full * (1 - q) + target * q
    mat = np.float32([[ww / W, 0, x], [0, hh / H, y]])
    return cv2.warpAffine(src, mat, (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_CONSTANT, borderValue=BG)

def render_state(e, boards):
    """v4's static state: the board (or its crop) fit to 1220x680 inside the house background, rings drawn after the crop."""
    src = boards[e['board']]; h, w = src.shape[:2]; x0, y0, x1, y1 = e['crop'] or [0, 0, w, h]; part = src[y0:y1, x0:x1]
    hh, ww = part.shape[:2]; s = min(1220 / ww, 680 / hh); nw, nh = round(ww * s), round(hh * s); x, y = (W - nw) // 2, (H - nh) // 2
    base = np.full((H, W, 3), BG, np.uint8); base[y:y + nh, x:x + nw] = cv2.resize(part, (nw, nh), interpolation=cv2.INTER_AREA); im = base.copy()
    for m in e['marks']:
        a, b, c, d = m['rect']; rr = [x + (a - x0) * s, y + (b - y0) * s, x + (c - x0) * s, y + (d - y0) * s]; ring(im, rr, m['color']); m['output_rect'] = rr; m['ring_width'] = 5
        a, b, c, d = map(round, rr); assert min(a, b, W - c, H - d) >= 20, (e['label'], rr)
    return im

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); (OUT / 'states').mkdir(exist_ok=True)
    protected = [LIVE, *ASSETS.values(), D / 'embeddings-close.jpg', ROOT / 'index.html', ROOT / 'lessons/embeddings.md']
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    assert close_board_copy('embeddings') == ('AI uses numbers to work with meaning.', 'Those numbers help AI recognize similarities and differences.')
    if not (OUT / 'close.png').exists():
        subprocess.run([str(ROOT / '.video-venv/bin/python'), str(ROOT / 'scripts/video/make_close_board.py'), '--lesson', 'embeddings', '--out', str(OUT / 'close.png')], check=True, stdout=subprocess.DEVNULL)
    boards = {k: cv2.imread(str(p)) for k, p in ASSETS.items()}; assert all(v is not None for v in boards.values())
    dims = {k: list(v.shape[1::-1]) for k, v in boards.items()}
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
        if e['board'] in ('native', 'student'): continue
        states[e['label']] = render_state(e, boards); cv2.imwrite(str(OUT / 'states' / (e['label'] + '.jpg')), states[e['label']])
    for t in [18.7, 22.733333, 23.4, 24.133333, 26.3, 29.266667, 29.7, 30.166667, 38]:
        cv2.imwrite(str(OUT / 'states' / f'student-camera-{fr(t)}.jpg'), student_frame(boards['student'], fr(t)))
    boundaries = {}
    for i, e in enumerate(schedule):
        if i and (e['board'] != schedule[i - 1]['board'] or e['crop'] != schedule[i - 1]['crop']): boundaries[e['start']] = e['label']
    boundaries[CLOSE] = 'standard-close'
    m = dict(scope='Review only; visual-only retrofit of the shipped v4 (current course boards + canonical close); live unchanged',
             retrofit_of=str(LIVE.relative_to(ROOT)), retrofit_of_sha256=hashes[str(LIVE.relative_to(ROOT))], audio_note='copied from the shipped v4 at mux (-c:a copy)',
             output=str(DEST), fps=FPS, total_frames=TOTAL, duration=TOTAL / FPS, close_start_frame=CLOSE, timeline=TIMELINE,
             states=[dict(start=e['start'], end=e['end'], board=e['board'], label=e['label'], marks=e['marks'], crop=e['crop']) for e in schedule],
             student_camera=dict(zoom_in=[22.733333, 24.133333], hold=[24.133333, 29.266667], zoom_out=[29.266667, 30.166667], target_source_rect=[60, 675, 860, 1125]),
             board_dimensions=dims, assets={k: dict(path=str(p.relative_to(ROOT)), sha256=sha(p)) for k, p in ASSETS.items()},
             close=dict(asset='course-assets/embeddings/embeddings-close.jpg', sha256=hashes['course-assets/embeddings/embeddings-close.jpg'], prehold_frames=CLOSE_PREHOLD, push_frames=CLOSE_PUSH, zoom_endpoint=1.2, settled_frames=TOTAL - CLOSE - CLOSE_PREHOLD - CLOSE_PUSH),
             boundaries=[dict(frame=f, label=l) for f, l in sorted(boundaries.items())], protected_hashes=hashes)
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2))
    print('Prepared', TOTAL, 'frames; board spans', [(e['start'], e['end'], e['label']) for e in schedule if e['board'] != 'native'][:8], '…', flush=True)
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
            else: im = states[e['label']]
        else:
            k = f - CLOSE; q = min(1, max(0, (k - CLOSE_PREHOLD) / (CLOSE_PUSH - 1))); z = 1 + .2 * q * q * (3 - 2 * q)
            hh_, ww_ = ci.shape[:2]; cw = ww_ / z; chh = cw * 9 / 16
            im = cv2.warpAffine(ci, np.float32([[cw / W, 0, (ww_ - cw) / 2], [0, chh / H, (hh_ - chh) / 2]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
            if k in [0, CLOSE_PREHOLD, CLOSE_PREHOLD + CLOSE_PUSH - 1, TOTAL - CLOSE - 1]: cv2.imwrite(str(OUT / 'states' / f'close-{k}.jpg'), im)
        p.stdin.write(im.tobytes())
        if f % 1800 == 0: print('Rendered', f, '/', TOTAL, flush=True)
    p.stdin.close(); assert p.wait() == 0
    current = {k: sha(ROOT / k) for k in hashes}; m['protected_files_unchanged'] = {k: v == current[k] for k, v in hashes.items()}; assert all(m['protected_files_unchanged'].values())
    m['render_sha256'] = sha(DEST); (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2)); print(DEST, flush=True)

if __name__ == '__main__':
    main()
