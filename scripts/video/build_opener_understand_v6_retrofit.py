#!/usr/bin/env python3
"""Understand AI opener v6: v5 (the What Kind of Thing Is AI? card + canonical close) plus the current section-map render (2026-09-16).
Review only. Visual-only retrofit of the shipped v4; v4's audio stream is copied back in untouched.

David 2026-09-16: "We want the current board." The map span [2451, 4410) is re-rendered from the current
course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg with the shipped treatment reproduced (the board at full view
throughout, the same five row rings at the same output frames, the takeaway ring on the banner; the shipped v4 never used the
v4 script's topic pans, so none are used here; the takeaway ring follows the new banner, which now runs edge to edge). Old and new maps measured identical in every row panel and text row; only the title
alignment and the banner width differ. The two pauses inside the span hold the frame before them, as v4 did.
Spans: [0, 352) the kind card (leg from Build, as v5); [352, 2451) v4 picture; [2451, 4410) the map render; [4410, 4638) the canonical close.
"""
from pathlib import Path
import argparse, subprocess, sys, hashlib, json
import numpy as np, cv2, imageio_ffmpeg
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, Reader, CLOSE_PREHOLD, CLOSE_PUSH, W, H
from build_one_more_thing_review_repair import ring

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/understand-ai-opener/understand-ai-opener.mp4'   # the shipped v4, sha256 e657b34b984d7ceb…
OUT = ROOT / 'video-audit/understand-ai-opener-repair-2026-09-16'
RENDER = OUT / 'v6-render.mp4'
DEST = ROOT / 'Prompts/understand-ai-opener-v6.mp4'
KIND = ROOT / 'course-assets/understand-ai-opener/understand-ai-opener-kind.jpg'
MAP = ROOT / 'course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg'
GOLD = '#eccf6b'
LINES = [[110, 375, 1489, 423], [110, 424, 1489, 472], [110, 472, 1489, 514], [110, 522, 1489, 571]]
TOTAL, K_OUT, M_IN, CLOSE = 4638, 352, 2451, 4410
BG = (251, 245, 246)
# v4's map schedule on the output timeline (source 82.7667 s = output 2451; the pause at 4201-4231 holds; source 141.333 = output 4231)
def fr(t): return round(t * 30)
def o(t): return M_IN + fr(t) - fr(82.7667)     # source seconds before the pause -> output frame
EVENTS = [  # (output frame, label, ring rect or None, color, view None = the full board, as the shipped v4 shows it)
    (M_IN, 'map-establish', None, None, None),
    (o(94.82), 'topic-training', [80, 127, 1520, 278], '#4f2fc4', None),
    (o(102.36), 'topic-probability', [80, 278, 1520, 430], '#1652f0', None),
    (o(110.6), 'topic-words-numbers', [80, 430, 1520, 580], '#0e8f86', None),
    (o(121.98), 'topic-meaning', [80, 580, 1520, 773], '#0f7a4a', None),
    (o(131.28), 'topic-answer', [80, 773, 1520, 925], '#a9760c', None),
    (4231, 'map-takeaway', [40, 963, 1560, 1051], '#6e51ff', None),   # the new banner runs 40-1560 (v4: 80-1520)
]
PAUSES = [(4201, 4231), (4380, 4410)]   # hold the frame before each

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, LIVE, OUT, RENDER, protected=[KIND, MAP]); b.tall_margin = False
    b.load_audio([(29.7, 30.5), (35.6, 36.4), (65.3, 66.1), (80.8, 81.6), (140.1, 140.9), (146.1, 146.9), (151.2, 154.5)])
    b.keep(0, K_OUT, 'B0 What Kind of Thing Is AI? card, four line rings', 'kind'); b.keep(K_OUT, M_IN, 'v4 picture (unchanged)')
    b.keep(M_IN, CLOSE, 'Section map re-rendered from the current asset with the v4 camera schedule'); b.mark_close_start(); b.keep(CLOSE, TOTAL, 'Close (canonical closing JPG)'); b.finish_audio()
    T = lambda label, at, r: dict(label=label, at=at, rects=[r], color=GOLD, radius=18)
    b.board('kind', KIND, 0, K_OUT, 'compact', [T("It's not magic.", 0.30, LINES[0]), T('Not a person.', 1.82, LINES[1]), T('Not normal software.', 3.12, LINES[2]), T("It's its own kind of thing.", 5.96, LINES[3])], min_open=0, push=False)
    b.render_legs(); b.state_sheet('kind'); b.make_close('openerfoundations')
    im = cv2.imread(str(MAP)); h, w = im.shape[:2]
    s = min(1230 / w, 670 / h); ww, hh = W / s, H / s; full = [(w - ww) / 2, (h - hh) / 2, (w + ww) / 2, (h + hh) / 2]
    sched = []
    for i, (f0, label, rect, color, view) in enumerate(EVENTS):
        f1 = EVENTS[i + 1][0] if i + 1 < len(EVENTS) else CLOSE
        target = view or full; prev = sched[-1]['target'] if sched else target
        move = 0 if (label == 'map-takeaway' or prev == target) else 24
        sched.append(dict(start=f0, end=f1, label=label, rect=rect, color=color, target=target, frm=(target if label == 'map-takeaway' else prev), move=move))
    def map_frame(f):
        for p0, p1 in PAUSES:
            if p0 <= f < p1: f = p0 - 1
        e = next(e for e in sched if e['start'] <= f < e['end'])
        q = min(1, max(0, (f - e['start']) / max(1, e['move']))) if e['move'] else 1; q = q * q * (3 - 2 * q)
        view = np.array(e['frm']) * (1 - q) + np.array(e['target']) * q; a, bb, c, d = view; sc = W / (c - a)
        out = cv2.warpAffine(im, np.float32([[(c - a) / W, 0, a], [0, (d - bb) / H, bb]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_CONSTANT, borderValue=BG)
        if e['rect']:
            x0, y0, x1, y1 = e['rect']; r = [(x0 - a) * sc, (y0 - bb) * sc, (x1 - a) * sc, (y1 - bb) * sc]; assert min(r[0], r[1], W - r[2], H - r[3]) >= 24, (e['label'], r); ring(out, r, e['color'])
        return out
    b.manifest({'retrofit_of': str(LIVE), 'retrofit_of_sha256': hashlib.sha256(LIVE.read_bytes()).hexdigest(), 'audio_note': 'copied from the shipped v4 at mux', 'kind_lines': LINES,
                'map_schedule': [dict(start=e['start'], end=e['end'], label=e['label'], rect=e['rect'], color=e['color'], view=e['target'], move_frames=e['move']) for e in sched], 'map_pauses_hold': PAUSES})
    (OUT / 'states').mkdir(exist_ok=True)
    for e in sched: cv2.imwrite(str(OUT / 'states' / f"{e['label']}.jpg"), map_frame(min(e['end'] - 1, e['start'] + 35)))
    print('Prepared', TOTAL, 'map events', [(e['start'], e['label']) for e in sched], flush=True)
    if args.prepare_only: return
    assert not DEST.exists(), f'{DEST} exists; version-suffix instead of overwriting'
    ff = imageio_ffmpeg.get_ffmpeg_exe(); ci = cv2.imread(str(OUT / 'close.png'))
    p = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '30', '-i', 'pipe:0', '-i', str(LIVE), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    live = Reader(str(LIVE)); kind = Reader(str(OUT / 'leg-kind.mkv'))
    for f in range(TOTAL):
        if f < K_OUT: frame = kind.at(f)
        elif f < M_IN: frame = live.at(f)
        elif f < CLOSE: frame = map_frame(f)
        else:
            k = f - CLOSE; q = np.clip((k - CLOSE_PREHOLD) / (CLOSE_PUSH - 1), 0, 1); z = 1 + .2 * q * q * (3 - 2 * q)
            hh_, ww_ = ci.shape[:2]; cw = ww_ / z; chh = cw * 9 / 16
            frame = cv2.warpAffine(ci, np.float32([[cw / W, 0, (ww_ - cw) / 2], [0, chh / H, (hh_ - chh) / 2]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
        p.stdin.write(frame.tobytes())
    p.stdin.close(); assert p.wait() == 0
    m = json.load(open(OUT / 'edit-manifest.json')); m['render_sha256'] = hashlib.sha256(DEST.read_bytes()).hexdigest(); m['output'] = str(DEST)
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2)); print(DEST)

if __name__ == '__main__':
    main()
