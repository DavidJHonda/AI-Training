#!/usr/bin/env python3
"""Transformer v8: the current course boards and the canonical close, as a visual-only retrofit of the shipped v7 (2026-09-17). Review only.

The shipped file (course-assets/transformer/transformer.mp4, 7749 frames) is v7 (build_transformer_v7.py, 2026-09-10): v5's approved
edit for its first 6339 frames (build_transformer_v5.py: six course boards at full view with rings, the owner-requested attention paths
drawn over How a Transformer Reads a Sentence), then positional-encoding material from the earlier live video, the word-order board with
two rings, and v5's close. Its rolls (Prompts/transformer-1.mp4, -2.mp4) and the v5/v6 candidates no longer exist, so this build takes
the finished v7 as its picture source, re-renders every course-board span from the current course-assets JPGs (same dimensions as the
pre-attribution renders v5/v7 used; the site credit line, and the 2026-09-15 title-banner standardization on How Earlier AI Read Text,
are the differences) with v5's/v7's exact camera (static full view, the board fit to 1210x660 on the house stage) and rings at the same
frames, including the attention-path overlay, replaces the close with the canonical closing JPG (make_close_board.py --lesson attention),
and muxes v7's original audio stream back in untouched. Every Notebook / earlier-live span is v7's picture. Spans on the output
timeline: problems [1128, 2105); before [2815, 3305); reads [3628, 4125); reads + attention paths [4125, 4413); operations [5115, 5805);
resolves [5805, 6369); order [7148, 7519); close [7519, 7749).
"""
from pathlib import Path
import argparse, subprocess, sys, hashlib, json
import numpy as np, cv2, imageio_ffmpeg
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Reader, CLOSE_PREHOLD, CLOSE_PUSH, W, H, FPS
from build_one_more_thing_review_repair import ring
from make_close_board import close_board_copy

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/transformer/transformer.mp4'   # the shipped v7
OUT = ROOT / 'video-audit/transformer-repair-2026-09-17'
DEST = ROOT / 'Prompts/transformer-v8.mp4'
D = ROOT / 'course-assets/transformer'
ASSETS = {'problems': D / 'transformer-context-problems.jpg', 'before': D / 'transformer-before-transformers.jpg', 'reads': D / 'transformer-how-transformer-reads.jpg',
          'operations': D / 'transformer-attention-transformation.jpg', 'resolve': D / 'transformer-resolves-meaning.jpg', 'order': D / 'transformer-word-order.jpg'}
BLUE, GREEN, PURPLE, TEAL, NEUTRAL = '#1652f0', '#0f7a4a', '#4f2fc4', '#0e8f86', '#6e51ff'
BG = (251, 245, 246)
def fr(t): return round(t * FPS)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# ---- v7's output timeline: v5's rows for [0, 6339), then v7's own rows. Frame numbers are output frames; source seconds are the rolls'.
ROWS = []; cursor = 0
def keep(src, a, b, label, visual='native'):
    global cursor; s, e = fr(a), fr(b); ROWS.append(dict(kind='source', src=src, s=s, e=e, o0=cursor, o1=cursor + e - s, label=label, visual=visual)); cursor += e - s
def pause(n, label):
    global cursor; ROWS.append(dict(kind='hold', o0=cursor, o1=cursor + n, label=label)); cursor += n
# v5 (build_transformer_v5.py)
keep(1, 0, 26.6, 'Full original opening, tokens, and starting embeddings'); keep(2, 26.6, 36.6, 'Context shapes meaning'); pause(30, 'Pause before the two context problems')
keep(2, 21.3, 52.85, 'Fuller LIGHT sentences and pronoun examples', 'problems'); pause(30, 'Pause before human understanding and AI math')
keep(1, 58.75, 82.4, 'Human understanding, mathematical work, and earlier AI'); keep(1, 82.4, 97.75, 'Full earlier-AI explanation', 'before'); pause(30, 'Pause before the Transformer breakthrough')
keep(1, 98, 108.78, 'Original 2017 research and Transformer graphic'); keep(1, 108.78, 120.5333333333, 'Whole message and direct CAT-to-IT connection', 'reads')
keep(1, 121.2, 124.7666666667, 'Draws information from CAT; instantly removed', 'reads'); keep(1, 125.1666666667, 126.4, 'Distance between them; physical removed', 'reads')
keep(1, 131.0, 140.6, 'Full explanation of calculating relevance', 'relevance'); keep(1, 140.6, 163.0, 'Recall exercise and why the numbers must change'); pause(30, 'Pause before attention and transformation')
keep(1, 163.0, 186.0, 'Full attention and transformation plus number-change reminder', 'operations'); keep(1, 186.0, 189.15, 'Original introduction to the returning examples', 'resolve')
keep(2, 177.55, 185.85, 'Full LIGHT context explanation', 'resolve_left'); pause(30, 'Pause between LIGHT and CAT examples'); keep(2, 42.0, 47.35, 'Cat and milk interpretations', 'resolve_right')
assert cursor == 6339, cursor
# v7 (build_transformer_v7.py): the earlier live video's positional-encoding material, then the word-order board
pause(30, 'Pause from CAT and milk to word order'); keep('live', 208.4, 224.8, 'Full DOG and MAN comparison'); keep('live', 224.8, 228.0, 'To solve this the architecture includes an extra step')
pause(12, 'Natural sentence gap after extra step'); keep('live', 235.8333333333, 241.8, 'Numbered-token position-stamp demonstration')
keep('live', 241.8, 246.1666666667, 'Name positional encoding on the current lesson board', 'order'); keep('live', 253.0333333333, 260.0333333333, 'Explain simultaneous processing with order preserved', 'order')
pause(30, 'Pause before closing message'); CLOSE = cursor; keep('v5', 243.4666666667, 251.1333333333, 'Preserved v5 closing narration and camera', 'close'); TOTAL = cursor
assert (CLOSE, TOTAL) == (7519, 7749), (CLOSE, TOTAL)
ORDER_START = next(r for r in ROWS if r.get('visual') == 'order')['o0']; ORDER_POSITIONS = ORDER_START + fr(2.6); ORDER_TAKEAWAY = ROWS[-3]['o0'] + fr(3.8)   # v7: highlight_frame, takeaway_frame
assert (ORDER_START, ORDER_POSITIONS, ORDER_TAKEAWAY) == (7148, 7226, 7393)

def mark(rect, color): return dict(rect=rect, color=color, highlight_source='neutral_video_purple' if color == NEUTRAL else 'card_locked_accent')
def board_state(row, f):
    """v5's board_state, verbatim, on the roll's seconds; v7's order-board states on output frames."""
    key = row['visual']; label = key + '-establish'; m = None
    if key == 'order':
        key = 'order'
        if f >= ORDER_TAKEAWAY: m = mark([40, 800, 1560, 889], NEUTRAL); label = 'order-takeaway'
        elif f >= ORDER_POSITIONS: m = mark([816, 299, 1560, 760], PURPLE); label = 'order-position-stamps'
        return dict(board=key, label=label, marks=[m] if m else [])
    sec = (row['s'] + f - row['o0']) / FPS
    if key == 'problems':
        if sec >= 47.65: m = mark([40, 1212, 1560, 1302], NEUTRAL); label = 'problems-context-takeaway'
        elif sec >= 44.55: m = mark([849, 912, 1527, 1028], GREEN); label = 'problems-milk-sentence'
        elif sec >= 41.95: m = mark([849, 786, 1527, 901], GREEN); label = 'problems-cat-sentence'
        elif sec >= 33.65: m = mark([816, 128, 1560, 1173], GREEN); label = 'problems-pronouns'
        elif sec >= 30.25: m = mark([74, 912, 751, 1028], BLUE); label = 'problems-suitcase-sentence'
        elif sec >= 26.3: m = mark([74, 786, 751, 901], BLUE); label = 'problems-lamp-sentence'
        elif sec >= 21.3: m = mark([40, 128, 784, 1173], BLUE); label = 'problems-different-meanings'
    elif key == 'before':
        if sec >= 93.17: m = mark([40, 605, 1560, 695], NEUTRAL); label = 'before-takeaway'   # the banner moved on 2026-09-15 (title-banner standardization put "We know IT refers to CAT." above it); v5's [40, 558, 1560, 695] would cut that line. Measured banner_rect: [40, 606, 1560, 694]
        elif sec >= 90.4: m = mark([927, 406, 1110, 494], NEUTRAL); label = 'before-it'
        elif sec >= 87.6: m = mark([287, 187, 471, 274], NEUTRAL); label = 'before-cat'
    elif key == 'relevance':
        key = 'reads'; m = mark([696, 450, 805, 538], NEUTRAL); label = 'reads-calculate-relevance'
    elif key == 'reads':
        if sec >= 119.6: m = mark([80, 150, 1515, 580], NEUTRAL); label = 'reads-cat-it-connection'
        elif sec >= 112.3: m = mark([40, 628, 1560, 716], NEUTRAL); label = 'reads-all-present'
    elif key == 'operations':
        if sec >= 181.5: m = mark([816, 128, 1560, 730], TEAL); label = 'operations-numbers-change'
        elif sec >= 176.78: m = mark([816, 128, 1560, 730], TEAL); label = 'operations-transformation'
        elif sec >= 165.45: m = mark([40, 128, 784, 730], BLUE); label = 'operations-attention'
    elif key.startswith('resolve'):
        if key == 'resolve_left': m = mark([40, 128, 784, 1234], BLUE); label = 'resolve-light-clues'
        elif key == 'resolve_right': m = mark([816, 128, 1560, 1234], GREEN); label = 'resolve-pronoun-clues'
        key = 'resolve'
    return dict(board=key, label=label, marks=[m] if m else [])

def camera(im): h, w = im.shape[:2]; s = min((W - 70) / w, (H - 60) / h); return s, (W - w * s) / 2, (H - h * s) / 2
def render(im, marks):
    s, x, y = camera(im); out = cv2.warpAffine(im, np.float32([[s, 0, x], [0, s, y]]), (W, H), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_CONSTANT, borderValue=BG)
    for m in marks:
        a, b, c, d = m['rect']; r = [a * s + x, b * s + y, c * s + x, d * s + y]; assert min(r[0], r[1], W - r[2], H - r[3]) >= 24, (m, r)
        ring(out, r, m['color']); m['output_rect'] = r; m['ring_width'] = 5
    return out
def attention_paths(im, board, elapsed):
    """v5's owner-requested attention paths over How a Transformer Reads a Sentence, verbatim: three backward-looking paths from IT
    (mat, rainstorm faint; cat emphasized), then a ring on CAT from 4 s."""
    out = im.copy(); s, x, y = camera(board)
    def bezier(pts):
        q = np.linspace(0, 1, 100)[:, None]; a, b, c, d = np.array(pts, float); return (1 - q) ** 3 * a + 3 * (1 - q) ** 2 * q * b + 3 * (1 - q) * q * q * c + q ** 3 * d
    paths = [dict(name='mat', delay=.7, duration=1.3, color=(205, 190, 176), width=2, segments=[[(784, 446), (875, 436), (1190, 449), (1216, 429)], [(1216, 429), (1260, 403), (1238, 286), (1208, 287)]]),
             dict(name='rainstorm', delay=2.0, duration=1.3, color=(205, 190, 176), width=2, segments=[[(783, 447), (861, 439), (1148, 451), (1170, 433)], [(1170, 433), (1195, 415), (1173, 392), (1154, 392)]]),
             dict(name='cat', delay=4.0, duration=2.1, color=(255, 81, 110), width=4, segments=[[(750, 541), (742, 565), (412, 578), (384, 540)], [(384, 540), (355, 493), (354, 379), (387, 349)], [(387, 349), (415, 330), (565, 347), (600, 334)]])]
    for path in paths:
        q = min(1, max(0, (elapsed - path['delay']) / path['duration']))
        if q <= 0: continue
        pts = np.vstack([bezier(seg) for seg in path['segments']]); pts = pts[:max(2, round(len(pts) * q))]; pts = pts * s + [x, y]
        cv2.polylines(out, [np.round(pts).astype(np.int32)], False, path['color'], path['width'], cv2.LINE_AA)
        if q == 1:
            v = pts[-1] - pts[-7]; v /= np.linalg.norm(v); n = np.array([-v[1], v[0]]); end = pts[-1]; a = end - 9 * v + 4 * n; b = end - 9 * v - 4 * n
            cv2.polylines(out, [np.round([a, end, b]).astype(np.int32)], False, path['color'], path['width'], cv2.LINE_AA)
    if elapsed >= 4:
        a, b, c, d = [534, 245, 667, 334]; ring(out, [a * s + x, b * s + y, c * s + x, d * s + y], NEUTRAL)
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); (OUT / 'states').mkdir(exist_ok=True)
    protected = [LIVE, *ASSETS.values(), D / 'transformer-close.jpg', ROOT / 'index.html', ROOT / 'lessons/transformer.md']
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    assert close_board_copy('attention') == ('Attention is all you need.', 'AI uses relationships between words to help interpret your message.')
    if not (OUT / 'close.png').exists():
        subprocess.run([str(ROOT / '.video-venv/bin/python'), str(ROOT / 'scripts/video/make_close_board.py'), '--lesson', 'attention', '--out', str(OUT / 'close.png')], check=True, stdout=subprocess.DEVNULL)
    boards = {k: cv2.imread(str(p)) for k, p in ASSETS.items()}; assert all(v is not None for v in boards.values())
    # schedule: one span per visual state on the output timeline; pauses hold the state before them (v5/v7: the last rendered frame)
    schedule = []; last = None; prev_state = dict(board='native', label='native', marks=[])
    for f in range(CLOSE):
        row = next(r for r in ROWS if r['o0'] <= f < r['o1'])
        if row['kind'] == 'hold': state = dict(prev_state, label=prev_state['label'] + ('' if prev_state['label'].endswith('-hold') else '-hold') if prev_state['board'] != 'native' else 'native')
        elif row['visual'] == 'native': state = dict(board='native', label='native', marks=[])
        else: state = board_state(row, f); state['row'] = row['o0']; state['relevance'] = row['visual'] == 'relevance'
        prev_state = state
        if state['label'] != last:
            if schedule: schedule[-1]['end'] = f
            schedule.append(dict(state, start=f)); last = state['label']
    schedule[-1]['end'] = CLOSE
    states = {}
    for e in schedule:
        if e['board'] == 'native': continue
        key = e['label'].replace('-hold', '')
        if key not in states: states[key] = render(boards[e['board']], e['marks']); cv2.imwrite(str(OUT / 'states' / (key + '.jpg')), states[key], [cv2.IMWRITE_JPEG_QUALITY, 92])
    rel = next(e for e in schedule if e.get('relevance'))
    for elapsed in [0, 2, 4, 7, 9]: cv2.imwrite(str(OUT / 'states' / f'relevance-{elapsed}.jpg'), attention_paths(states['reads-calculate-relevance'], boards['reads'], elapsed), [cv2.IMWRITE_JPEG_QUALITY, 92])
    boundaries = {}
    for i, e in enumerate(schedule):
        if i and e['board'] != schedule[i - 1]['board']: boundaries[e['start']] = e['label']
    boundaries[CLOSE] = 'standard-close'
    m = dict(scope='Review only; visual-only retrofit of the shipped v7 (current course boards + canonical close); live unchanged',
             retrofit_of=str(LIVE.relative_to(ROOT)), retrofit_of_sha256=hashes[str(LIVE.relative_to(ROOT))], audio_note='copied from the shipped v7 at mux (-c:a copy)',
             output=str(DEST), fps=FPS, total_frames=TOTAL, duration=TOTAL / FPS, close_start_frame=CLOSE, timeline=ROWS,
             states=[dict(start=e['start'], end=e['end'], board=e['board'], label=e['label'], marks=e['marks']) for e in schedule],
             camera='v5/v7: static full view, board fit to 1210x660 on the house stage; no dives', attention_paths=dict(span=[rel['start'], rel['end']], note="v5's owner-requested overlay, reproduced verbatim"),
             board_dimensions={k: list(v.shape[1::-1]) for k, v in boards.items()}, assets={k: dict(path=str(p.relative_to(ROOT)), sha256=sha(p)) for k, p in ASSETS.items()},
             close=dict(asset='course-assets/transformer/transformer-close.jpg', sha256=hashes['course-assets/transformer/transformer-close.jpg'], prehold_frames=CLOSE_PREHOLD, push_frames=CLOSE_PUSH, zoom_endpoint=1.2, settled_frames=TOTAL - CLOSE - CLOSE_PREHOLD - CLOSE_PUSH),
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
            e = schedule[idx]
            if e['board'] == 'native': im = live.at(f)
            else:
                im = states[e['label'].replace('-hold', '')]
                if e.get('relevance'): im = attention_paths(im, boards['reads'], (f - e['row']) / FPS)
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
