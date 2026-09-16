#!/usr/bin/env python3
"""Tokens v8: the current course boards and the canonical close, as a visual-only retrofit of the shipped v7 (2026-09-16). Review only.

The shipped file (course-assets/tokens/tokens.mp4, 6528 frames) is v7 (build_tokens_v7.py, 2026-09-10). Its roll no longer exists, so
this build takes the finished file as its picture source, re-renders the five course-board spans from the current course-assets JPGs
(same dimensions as the pre-attribution renders v7 used; the URL line is the difference) with v7's exact camera schedule (full views, the
Building Blocks and How AI Splits Text dives with 24-frame moves, the same rings at the same source frames), replaces the close with the
canonical closing JPG, and muxes v7's original audio stream back in untouched. v7's two video-only illustrations (words-to-math,
whole-and-part) and every Notebook span are v7's picture. Spans on the output timeline: chat [0, 363); blocks [1638, 2388);
send [3655, 4186); cat [4186, 4576); examples [5025, 5737); close [6304, 6528).
"""
from pathlib import Path
import argparse, subprocess, sys, hashlib, json
import numpy as np, cv2, imageio_ffmpeg
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, Reader, CLOSE_PREHOLD, CLOSE_PUSH, W, H
from build_one_more_thing_review_repair import ring

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/tokens/tokens.mp4'   # the shipped v7, sha256 f7db1df1b0cf2634…
OUT = ROOT / 'video-audit/tokens-repair-2026-09-16'
RENDER = OUT / 'v8-render.mp4'   # placeholder for Build (the final encode goes straight to DEST)
DEST = ROOT / 'Prompts/tokens-v8.mp4'
D = ROOT / 'course-assets/tokens'
ASSETS = {'chat': D / 'tokens-using-ai-feels-like.jpg', 'blocks': D / 'tokens-building-blocks.jpg', 'send': D / 'tokens-how-tokenization-works.jpg', 'cat': D / 'tokens-cat-token-id.jpg', 'examples': D / 'tokens-how-ai-splits-text.jpg'}
BG = (251, 245, 246); PURPLE = '#6e51ff'; EP = '#4f2fc4'; BLUE = '#1652f0'; TEAL = '#0e8f86'
TOTAL, CLOSE = 6528, 6304
def fr(t): return round(t * 30)
# v7's edit timeline (source seconds of the roll; pauses hold the frame before them) -> output frames
TIMELINE = []; cursor = 0
def keep(a, b):
    global cursor; s, e = fr(a), fr(b); TIMELINE.append(dict(kind='source', s=s, e=e, o0=cursor, o1=cursor + e - s)); cursor += e - s
def pause(n, hold):
    global cursor; TIMELINE.append(dict(kind='hold', hold=fr(hold), o0=cursor, o1=cursor + n)); cursor += n
keep(0, 11.1); pause(30, 11.066667); keep(15.233333, 42.8); pause(30, 42.766667); keep(43.066667, 86.433333); pause(30, 86.4); keep(99.3, 135.1); pause(30, 135.066667)
keep(135.333333, 180); pause(30, 179.966667); keep(189.9, 212.633333); pause(30, 212.6); keep(224, 241.9); pause(30, 241.866667)
assert cursor == CLOSE, cursor
def source_at(f):
    t = next(t for t in TIMELINE if t['o0'] <= f < t['o1']); return t['s'] + f - t['o0'] if t['kind'] == 'source' else t['hold']
def mark(rect, col=PURPLE): return dict(rect=rect, color=col)
EVENTS = []   # v7's events; boards not in ASSETS ('live') take the shipped picture
def ev(t, key, label, *marks, view=None): EVENTS.append(dict(sf=fr(t), board=key, label=label, marks=list(marks), view=view))
ev(0, 'chat', 'chat-establish'); ev(3.0, 'chat', 'question-bubble', mark([780, 208, 1490, 300], EP)); ev(7.5, 'chat', 'answer-bubble', mark([110, 388, 1320, 583]))
ev(15.233333, 'live', 'words-to-math-illustration'); ev(24.566667, 'live', 'notebook-dictionary-and-inputs'); ev(43.066667, 'live', 'notebook-tokens-introduction'); ev(49.8, 'live', 'whole-word-and-fragment-illustration')
ev(57, 'blocks', 'building-blocks-establish'); ev(60.1, 'blocks', 'word-into-pieces', mark([367, 590, 1139, 883]), view=[-100, 120, 1700, 1132.5]); ev(69.433333, 'blocks', 'reuse-strip', mark([80, 1175, 1520, 1337]), view=[-100, 680, 1700, 1692.5])
ev(78.0, 'blocks', 'reuse-unusual', mark([1195, 1242, 1385, 1314]), view=[-100, 680, 1700, 1692.5]); ev(79.3, 'blocks', 'reuse-unmatchable', mark([651, 1242, 949, 1314]), view=[-100, 680, 1700, 1692.5])
ev(82, 'live', 'notebook-vocabulary-hub'); ev(99.3, 'live', 'notebook-vocabulary-setup')
ev(135.333333, 'send', 'send-establish'); ev(135.5, 'send', 'start-with-text', mark([70, 163, 548, 705], EP)); ev(141.4, 'send', 'split-into-tokens', mark([558, 163, 1046, 705], BLUE)); ev(144.1, 'send', 'look-up-token-ids', mark([1050, 163, 1535, 705], TEAL)); ev(147.5, 'send', 'unbelievable-three-ids', mark([1063, 173, 1520, 435], TEAL))
ev(153.033333, 'cat', 'cat-establish'); ev(156.7, 'cat', 'cat-id-card', mark([816, 127, 1560, 716], EP)); ev(166.033333, 'live', 'notebook-cat-and-catalog-id')
ev(189.9, 'examples', 'examples-establish'); ev(193.3, 'examples', 'chatgpt-row', mark([60, 540, 1540, 720], EP), view=[-100, 125, 1700, 1137.5]); ev(199.4, 'examples', 'leading-spaces-row', mark([60, 730, 1540, 910], EP), view=[-100, 315, 1700, 1327.5]); ev(207.8, 'examples', 'url-row', mark([60, 920, 1540, 1167], EP), view=[-100, 530, 1700, 1542.5])
ev(224, 'live', 'notebook-output-decoding')
EVENTS.sort(key=lambda e: e['sf'])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); (OUT / 'states').mkdir(exist_ok=True)
    b = Build(ROOT, LIVE, OUT, RENDER, protected=list(ASSETS.values()))
    b.load_audio([(11.2, 12.0), (39.6, 40.4), (84.6, 85.4), (121.2, 122.0), (166.6, 167.4), (190.4, 191.2), (209.4, 210.2), (214.7, 217.5)])   # v7's pauses (room tone only; the audio is copied at mux)
    b.keep(0, TOTAL, 'v7 picture with the five board spans and the close re-rendered (see the script)'); b.mark_close_start(); b.finish_audio(); b.close_start = CLOSE; b.make_close('tokens')
    images = {k: cv2.imread(str(p)) for k, p in ASSETS.items()}
    def choice(sf): return next(e for e in reversed(EVENTS) if e['sf'] <= sf)
    schedule = []; last = None
    for f in range(CLOSE):
        e = choice(source_at(f))
        if e['label'] != last:
            if schedule: schedule[-1]['end'] = f
            schedule.append(dict(e, start=f)); last = e['label']
    schedule[-1]['end'] = CLOSE
    def full_view(im): h, w = im.shape[:2]; s = min(1220 / w, 670 / h); ww = W / s; hh = H / s; return [(w - ww) / 2, (h - hh) / 2, (w + ww) / 2, (h + hh) / 2]
    for i, e in enumerate(schedule):
        if e['board'] == 'live': continue
        e['target'] = list(e['view'] or full_view(images[e['board']])); prev = schedule[i - 1] if i else None
        e['frm'] = prev['target'] if prev and prev['board'] == e['board'] else e['target']; e['move'] = 24 if e['frm'] != e['target'] else 0
    def render_state(e, f):
        im = images[e['board']]; q = min(1, max(0, (f - e['start']) / max(1, e['move']))) if e['move'] else 1; q = q * q * (3 - 2 * q)
        view = np.array(e['frm']) * (1 - q) + np.array(e['target']) * q; a, bb, c, d = view; s = W / (c - a)
        out = cv2.warpAffine(im, np.float32([[(c - a) / W, 0, a], [0, (d - bb) / H, bb]]), (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_CONSTANT, borderValue=BG)
        for m in e['marks']:
            x0, y0, x1, y1 = m['rect']; r = [(x0 - a) * s, (y0 - bb) * s, (x1 - a) * s, (y1 - bb) * s]
            if min(r[0], r[1], W - r[2], H - r[3]) < 20:
                assert f - e['start'] < e['move'], (e['label'], r); continue
            ring(out, r, m['color'])
        return out
    for e in schedule:
        if e['board'] != 'live': cv2.imwrite(str(OUT / 'states' / f"{e['label']}.jpg"), render_state(e, min(e['end'] - 1, e['start'] + 30)))
    b.manifest({'retrofit_of': str(LIVE), 'retrofit_of_sha256': hashlib.sha256(LIVE.read_bytes()).hexdigest(), 'audio_note': 'copied from the shipped v7 at mux',
                'schedule': [dict(start=e['start'], end=e['end'], board=e['board'], label=e['label'], marks=e['marks'], view=e.get('target'), move_frames=e.get('move', 0)) for e in schedule]})
    print('Prepared', TOTAL, 'board spans', [(e['start'], e['end'], e['label']) for e in schedule if e['board'] != 'live'][:6], '…', flush=True)
    if args.prepare_only: return
    assert not DEST.exists(), f'{DEST} exists; version-suffix instead of overwriting'
    ff = imageio_ffmpeg.get_ffmpeg_exe(); ci = cv2.imread(str(OUT / 'close.png'))
    p = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '30', '-i', 'pipe:0', '-i', str(LIVE), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    live = Reader(str(LIVE)); idx = 0
    for f in range(TOTAL):
        if f < CLOSE:
            while f >= schedule[idx]['end']: idx += 1
            e = schedule[idx]; frame = live.at(f) if e['board'] == 'live' else render_state(e, f)
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
