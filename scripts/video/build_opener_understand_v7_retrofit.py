#!/usr/bin/env python3
"""Understand AI opener v7 (2026-09-16). Review only. Retrofit of the shipped v4 (the raw rolls no longer exist).

v7 = v6 with David's two notes:
1. The What Kind of Thing Is AI? card is shown as the page shows it. The page crops the 1600x900 JPG to the navy card (OpenerNavyBoard:
   board 80,300-1520,600); v5/v6 put the whole canvas on screen, so the card read as a thin band. The video now uses a 16:9 crop of the
   same JPG, [40, 22, 1560, 877], which centers the card and lets it span 94% of the frame width; nothing is redrawn, the crop is a
   temporary canvas of the canonical asset. Line rects shift by (-40, -22).
2. "As you move through the course," (141.10-142.36) is cut: source [4231, 4281), from the end of the pause to the trough before "you'll"
   (142.48-142.78, -46..-61 dB); the sentence resumes "you'll see that each topic builds directly on the one before it." The takeaway
   ring lands on that resume. Audio is now edited (Build's room-tone crossfades), so the mux takes edited.wav, not v4's stream.
Spans (source frames): [0,352) the card; [352,2451) v4 picture; [2451,4410) the section map re-rendered from the current asset at full
view with v4's rings (as v6); [4410,4638) the canonical close. Output = source minus the 50-frame cut: 4588 frames.
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
RENDER = OUT / 'v7-render.mp4'   # unused placeholder for Build (the final encode is written directly to DEST)
DEST = ROOT / 'Prompts/understand-ai-opener-v7.mp4'
KIND = ROOT / 'course-assets/understand-ai-opener/understand-ai-opener-kind.jpg'
MAP = ROOT / 'course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg'
GOLD = '#eccf6b'
CROP = [40, 22, 1560, 877]   # 1520x855, 16:9; the navy card (84-1515 x 301-598) centered
LINES = [[110 - 40, 375 - 22, 1489 - 40, 423 - 22], [110 - 40, 424 - 22, 1489 - 40, 472 - 22], [110 - 40, 472 - 22, 1489 - 40, 514 - 22], [110 - 40, 522 - 22, 1489 - 40, 571 - 22]]
TOTAL_SRC, K_OUT, M_IN, CLOSE = 4638, 352, 2451, 4410
CUT = (4231, 4281)   # "As you move through the course," (pause end 141.03 -> trough 142.7)
BG = (251, 245, 246)
def fr(t): return round(t * 30)
def o(t): return M_IN + fr(t) - fr(82.7667)     # v4 source seconds -> live frame
EVENTS = [(M_IN, 'map-establish', None, None), (o(94.82), 'topic-training', [80, 127, 1520, 278], '#4f2fc4'), (o(102.36), 'topic-probability', [80, 278, 1520, 430], '#1652f0'),
          (o(110.6), 'topic-words-numbers', [80, 430, 1520, 580], '#0e8f86'), (o(121.98), 'topic-meaning', [80, 580, 1520, 773], '#0f7a4a'), (o(131.28), 'topic-answer', [80, 773, 1520, 925], '#a9760c'),
          (4231, 'map-takeaway', [40, 963, 1560, 1051], '#6e51ff')]
PAUSES = [(4201, 4231), (4380, 4410)]   # live frames; each holds the frame before it

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    kind_crop = OUT / 'canvas-kind-crop.png'; im_k = cv2.imread(str(KIND)); x0, y0, x1, y1 = CROP; cv2.imwrite(str(kind_crop), im_k[y0:y1, x0:x1])
    b = Build(ROOT, LIVE, OUT, RENDER, protected=[KIND, MAP]); b.tall_margin = False
    b.load_audio([(29.7, 30.5), (35.6, 36.4), (65.3, 66.1), (80.8, 81.6), (140.1, 140.9), (146.1, 146.9), (151.2, 154.5)])
    b.keep(0, K_OUT, 'B0 What Kind of Thing Is AI? card (page crop), four line rings', 'kind'); b.keep(K_OUT, M_IN, 'v4 picture (unchanged)')
    b.keep(M_IN, CUT[0], 'Section map re-rendered from the current asset, full view, v4 rings'); b.keep(CUT[1], CLOSE, 'Section map: "you\'ll see that each topic builds…" (the phrase before it cut), takeaway ring')
    b.mark_close_start(); b.keep(CLOSE, TOTAL_SRC, 'Close (canonical closing JPG)'); b.finish_audio()
    T = lambda label, at, r: dict(label=label, at=at, rects=[r], color=GOLD, radius=18)
    b.board('kind', kind_crop, 0, K_OUT, 'compact', [T("It's not magic.", 0.30, LINES[0]), T('Not a person.', 1.82, LINES[1]), T('Not normal software.', 3.12, LINES[2]), T("It's its own kind of thing.", 5.96, LINES[3])], min_open=0, push=False)
    b.render_legs(); b.state_sheet('kind'); b.make_close('openerfoundations')
    im = cv2.imread(str(MAP)); h, w = im.shape[:2]; s = min(1230 / w, 670 / h); ww, hh = W / s, H / s; full = [(w - ww) / 2, (h - hh) / 2, (w + ww) / 2, (h + hh) / 2]
    sched = [dict(start=f0, end=(EVENTS[i + 1][0] if i + 1 < len(EVENTS) else CLOSE), label=label, rect=rect, color=color) for i, (f0, label, rect, color) in enumerate(EVENTS)]
    a_, b_, c_, d_ = full; sc = W / (c_ - a_)
    base_map = cv2.warpAffine(im, np.float32([[(c_ - a_) / W, 0, a_], [0, (d_ - b_) / H, b_]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_CONSTANT, borderValue=BG)
    def map_frame(sf):
        for p0, p1 in PAUSES:
            if p0 <= sf < p1: sf = p0 - 1
        e = next(e for e in sched if e['start'] <= sf < e['end']); out = base_map.copy()
        if e['rect']:
            x0, y0, x1, y1 = e['rect']; r = [(x0 - a_) * sc, (y0 - b_) * sc, (x1 - a_) * sc, (y1 - b_) * sc]; assert min(r[0], r[1], W - r[2], H - r[3]) >= 24, (e['label'], r); ring(out, r, e['color'])
        return out
    total = b.total; close_out = b.close_start
    def src_of(f): return f if f < CUT[0] else f + (CUT[1] - CUT[0])
    b.manifest({'retrofit_of': str(LIVE), 'retrofit_of_sha256': hashlib.sha256(LIVE.read_bytes()).hexdigest(), 'kind_crop_of_canonical_jpg': CROP, 'kind_lines_in_crop': LINES, 'narration_cut_live_frames': list(CUT),
                'map_schedule_live_frames': [dict(start=e['start'], end=e['end'], label=e['label'], rect=e['rect'], color=e['color']) for e in sched], 'map_pauses_hold': PAUSES})
    (OUT / 'states').mkdir(exist_ok=True)
    for e in sched: cv2.imwrite(str(OUT / 'states' / f"{e['label']}.jpg"), map_frame(min(e['end'] - 1, e['start'] + 35)))
    print('Prepared', total, f'{total / 30:.2f}s', 'close', close_out, 'cut', CUT, flush=True)
    if args.prepare_only: return
    assert not DEST.exists(), f'{DEST} exists; version-suffix instead of overwriting'
    ff = imageio_ffmpeg.get_ffmpeg_exe(); ci = cv2.imread(str(OUT / 'close.png'))
    p = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '30', '-i', 'pipe:0', '-i', str(OUT / 'edited.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    live = Reader(str(LIVE)); kind = Reader(str(OUT / 'leg-kind.mkv'))
    for f in range(total):
        sf = src_of(f)
        if f < K_OUT: frame = kind.at(f)
        elif sf < M_IN: frame = live.at(sf)
        elif f < close_out: frame = map_frame(sf)
        else:
            k = f - close_out; q = np.clip((k - CLOSE_PREHOLD) / (CLOSE_PUSH - 1), 0, 1); z = 1 + .2 * q * q * (3 - 2 * q)
            hh_, ww_ = ci.shape[:2]; cw = ww_ / z; chh = cw * 9 / 16
            frame = cv2.warpAffine(ci, np.float32([[cw / W, 0, (ww_ - cw) / 2], [0, chh / H, (hh_ - chh) / 2]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
        p.stdin.write(frame.tobytes())
    p.stdin.close(); assert p.wait() == 0
    m = json.load(open(OUT / 'edit-manifest.json')); m['render_sha256'] = hashlib.sha256(DEST.read_bytes()).hexdigest(); m['output'] = str(DEST)
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2)); print(DEST)

if __name__ == '__main__':
    main()
