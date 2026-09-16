#!/usr/bin/env python3
"""AI Is Math v4: the current course boards and the canonical close, as a visual-only retrofit of the shipped v3 (2026-09-16). Review only.

The shipped file (course-assets/ai-is-math/ai-is-math.mp4, 6310 frames) is v3: the v2 board build (build_ai_is_math_review_repair.py,
2026-09-09) with two Notebook spans restored (restore_ai_is_math_notebook.py). Its rolls no longer exist, so this build takes the
finished file as its picture source, re-renders the four board spans from the current course-assets JPGs (same 1600-wide layouts as the
pre-attribution boards v3 used: white cards and the site URL line are the differences) with v2's exact layout (scale min(1220/w, 680/h),
centered on the house stage), v2's ring rects and colors, and v2's event timing, replaces the close with the canonical closing JPG, and
muxes v3's original audio stream back in untouched.
Board spans on the output timeline (v2 timeline, confirmed by the live file's scene cuts): Standard Probability [1336, 1834); Counting the
Possibilities [1834, 2597); A Clue Changes the Odds [3549, 4480); What Comes Next? [5025, 5760); close [6070, 6310). The one-second
pauses inside those spans hold the frame before them, as v3 did. Everything else is v3's picture.
"""
from pathlib import Path
import argparse, subprocess, sys, hashlib, json
import numpy as np, cv2, imageio_ffmpeg
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, Reader, CLOSE_PREHOLD, CLOSE_PUSH, W, H
from build_one_more_thing_review_repair import ring

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/ai-is-math/ai-is-math.mp4'   # the shipped v3, sha256 50092ad96ef22b7f…
OUT = ROOT / 'video-audit/ai-is-math-repair-2026-09-16'
RENDER = OUT / 'v4-render.mp4'   # placeholder for Build (the final encode goes straight to DEST)
DEST = ROOT / 'Prompts/ai-is-math-v4.mp4'
D = ROOT / 'course-assets/ai-is-math'
ASSETS = {'formula': D / 'ai-is-math-the-math.jpg', 'coins': D / 'ai-is-math-two-coins.jpg', 'clue': D / 'ai-is-math-conditional-probability.jpg', 'dog': D / 'ai-is-math-what-comes-next.jpg'}
PURPLE, EDITORIAL, BLUE, TEAL, GREEN, RED = '#6e51ff', '#4f2fc4', '#1652f0', '#0e8f86', '#0f7a4a', '#c41f28'
BG = (251, 245, 246)
TOTAL, CLOSE = 6310, 6070
def fr(t): return round(t * 30)
# (output start, output end, board, source-seconds origin at the span start, pauses inside the span [(start, end)] holding the frame before)
SPANS = [(1336, 1834, 'formula', 43.533333, [(1804, 1834)]), (1834, 2597, 'coins', 66.966667, []), (3549, 4480, 'clue', 99.4 + (3549 - 2837) / 30, [(4450, 4480)]), (5025, 5760, 'dog', 170.333333, [(5730, 5760)])]
EVENTS = {   # v2's schedule: (source seconds, label, [rect in image px, color] or None)
    'formula': [(43.533333, 'formula-establish', None), (53.34, 'ways-to-get-result', ([378, 207, 922, 270], EDITORIAL)), (56.28, 'total-outcomes', ([360, 307, 940, 367], EDITORIAL)), (58.8, 'formula-settle', None)],
    'coins': [(66.966667, 'coins-establish', None), (69.0, 'coin-scenario', ([40, 127, 1560, 255], PURPLE)), (74.8, 'four-equally-likely-outcomes', ([70, 325, 1530, 598], PURPLE)), (77.36, 'heads-heads', ([65, 332, 425, 594], GREEN)),
              (79.0, 'heads-tails', ([435, 332, 795, 594], BLUE)), (80.28, 'tails-heads', ([805, 332, 1165, 594], BLUE)), (81.68, 'tails-tails', ([1175, 332, 1535, 594], BLUE)), (83.9, 'one-matching-outcome', ([65, 332, 425, 594], GREEN)), (85.6, 'one-out-of-four', ([238, 692, 1308, 872], EDITORIAL))],
    'clue': [(123.133333, 'clue-board-establish', None), (125.02, 'rule-out-tails-first', ([805, 372, 1535, 634], RED)), (131.1, 'two-remaining-outcomes', ([65, 372, 795, 634], PURPLE)), (134.95, 'one-remaining-double-heads', ([65, 372, 425, 634], GREEN)),
             (139.55, 'one-out-of-two', ([238, 732, 1308, 912], GREEN)), (143.32, 'unchanged-coins-changed-knowledge', None), (148.2, 'fifty-percent-takeaway', ([40, 1027, 1560, 1115], PURPLE))],
    'dog': [(170.333333, 'dog-board-establish', None), (171.44, 'dog-question', ([40, 127, 1560, 255], PURPLE)), (175.7, 'reply-so-far', ([490, 305, 1110, 442], EDITORIAL)), (180.38, 'possible-next-words', ([295, 451, 1305, 665], PURPLE)),
            (187.1, 'spot-probability', ([320, 518, 600, 648], EDITORIAL)), (190.06, 'max-probability', ([660, 518, 940, 648], EDITORIAL)), (191.78, 'buddy-probability', ([1000, 518, 1280, 648], EDITORIAL))],
}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); (OUT / 'states').mkdir(exist_ok=True)
    b = Build(ROOT, LIVE, OUT, RENDER, protected=list(ASSETS.values()))
    b.load_audio([(43.6, 44.4), (60.2, 61.0), (93.6, 94.4), (148.4, 149.2), (166.6, 167.4), (191.1, 191.9), (201.1, 201.9), (206.8, 210.2)])   # v3's pauses (room tone only; the audio is copied at mux)
    b.keep(0, TOTAL, 'v3 picture with the four board spans and the close re-rendered (see the script)'); b.mark_close_start(); b.finish_audio()
    b.close_start = CLOSE; b.make_close('aiismath')
    bases, layouts = {}, {}
    for key, path in ASSETS.items():
        im = cv2.imread(str(path)); h, w = im.shape[:2]; s = min(1220 / w, 680 / h); nw, nh = round(w * s), round(h * s); x, y = (W - nw) // 2, (H - nh) // 2
        base = np.full((H, W, 3), BG, np.uint8); base[y:y + nh, x:x + nw] = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_AREA); bases[key] = base; layouts[key] = (s, x, y)
    cache = {}
    def state(key, label):
        if (key, label) in cache: return cache[(key, label)]
        im = bases[key].copy(); ev = next(e for e in EVENTS[key] if e[1] == label)
        if ev[2]:
            s, x, y = layouts[key]; rect, color = ev[2]; rr = [x + rect[0] * s, y + rect[1] * s, x + rect[2] * s, y + rect[3] * s]; ring(im, rr, color)
        cache[(key, label)] = im; cv2.imwrite(str(OUT / 'states' / f'{label}.jpg'), im); return im
    def board_frame(f):
        for o0, o1, key, t0, pauses in SPANS:
            if o0 <= f < o1:
                for p0, p1 in pauses:
                    if p0 <= f < p1: f = p0 - 1
                t = t0 + (f - o0) / 30; label = [e for e in EVENTS[key] if fr(e[0]) <= fr(t)][-1][1]; return state(key, label)
        return None
    b.manifest({'retrofit_of': str(LIVE), 'retrofit_of_sha256': hashlib.sha256(LIVE.read_bytes()).hexdigest(), 'audio_note': 'copied from the shipped v3 at mux', 'board_spans_output': [dict(start=o0, end=o1, board=k, pauses_hold=p) for o0, o1, k, _, p in SPANS], 'events': {k: [dict(source_seconds=t, label=l, rect=(m[0] if m else None), color=(m[1] if m else None)) for t, l, m in v] for k, v in EVENTS.items()}, 'layout': {k: dict(scale=v[0], x=v[1], y=v[2]) for k, v in layouts.items()}})
    print('Prepared', TOTAL, 'close', CLOSE, flush=True)
    if args.prepare_only: return
    assert not DEST.exists(), f'{DEST} exists; version-suffix instead of overwriting'
    ff = imageio_ffmpeg.get_ffmpeg_exe(); ci = cv2.imread(str(OUT / 'close.png'))
    p = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '30', '-i', 'pipe:0', '-i', str(LIVE), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    live = Reader(str(LIVE))
    for f in range(TOTAL):
        frame = board_frame(f)
        if frame is None:
            if f < CLOSE: frame = live.at(f)
            else:
                k = f - CLOSE; q = np.clip((k - CLOSE_PREHOLD) / (CLOSE_PUSH - 1), 0, 1); z = 1 + .2 * q * q * (3 - 2 * q)
                hh_, ww_ = ci.shape[:2]; cw = ww_ / z; chh = cw * 9 / 16
                frame = cv2.warpAffine(ci, np.float32([[cw / W, 0, (ww_ - cw) / 2], [0, chh / H, (hh_ - chh) / 2]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
        else: live.at(f) if False else None
        p.stdin.write(frame.tobytes())
    p.stdin.close(); assert p.wait() == 0
    m = json.load(open(OUT / 'edit-manifest.json')); m['render_sha256'] = hashlib.sha256(DEST.read_bytes()).hexdigest(); m['output'] = str(DEST)
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2)); print(DEST)

if __name__ == '__main__':
    main()
