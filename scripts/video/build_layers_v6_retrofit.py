#!/usr/bin/env python3
"""Layers v6: v5 (current boards + canonical close in the shipped v4) plus a one-second pause after "The horse raced past the barn fell."
(David, 2026-09-17: "Add a one second pause at :12 after the sentence").

Everything is v5 (build_layers_v5_retrofit.py) with 30 frames inserted at output frame 383 (12.77 s, inside the quiet floor between
"fell." ending at 12.22 s and "At first" starting at 12.96 s; natural gap 0.74 s, so the gap becomes 1.74 s). The picture holds frame
382 (The Horse Raced Past the Barn Fell with its title ring; the First Read ring still pops on "At first"). The audio is v4's stream
with 30 frames of matched room tone spliced in at the same point: the tone is seeded from this file's own floor at 12.70-12.80 s
(RMS about 20, the quietest 100 ms of that gap) and joined with the house 240-sample crossfades, then encoded AAC 192k like every
audio-changing build. Every frame after the insert is v5's frame 30 later; the close starts at 4541 and the file runs 4797 frames.
"""
from pathlib import Path
import argparse, subprocess, sys, hashlib, json
import numpy as np, cv2, imageio_ffmpeg
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_layers_v5_retrofit as v5
from build_layers_v5_retrofit import ROOT, LIVE, D, ASSETS, EVENTS, source_at, render, fr, sha
from editspec_build import Reader, CLOSE_PREHOLD, CLOSE_PUSH, W, H, FPS, SR, SPF, readwav, writewav
from make_close_board import close_board_copy

OUT = ROOT / 'video-audit/layers-repair-2026-09-17-v6'
DEST = ROOT / 'Prompts/layers-v6.mp4'
INSERT_AT, INSERT = 383, 30                     # output frame of the insert (12.77 s) and its length
TONE_SEED = (12.70, 12.80)                       # seconds in the live audio: the quietest 100 ms of the natural gap
CLOSE = v5.CLOSE + INSERT; TOTAL = v5.TOTAL + INSERT
assert (CLOSE, TOTAL) == (4541, 4797)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); (OUT / 'states').mkdir(exist_ok=True)
    protected = [LIVE, *ASSETS.values(), D / 'layers-close.jpg', ROOT / 'index.html', ROOT / 'lessons/layers.md']
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    assert close_board_copy('layers') == ('Meaning builds up, layer by layer.', 'Attention and transformation. Dozens of times.')
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    if not (OUT / 'close.png').exists():
        subprocess.run([str(ROOT / '.video-venv/bin/python'), str(ROOT / 'scripts/video/make_close_board.py'), '--lesson', 'layers', '--out', str(OUT / 'close.png')], check=True, stdout=subprocess.DEVNULL)
    # ---- audio: v4's stream + 30 frames of matched room tone at the insert
    wav = OUT / 'source.wav'
    if not wav.exists(): subprocess.run([ff, '-y', '-v', 'error', '-i', str(LIVE), '-vn', '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', str(wav)], check=True)
    a = readwav(wav); seed = a[round(TONE_SEED[0] * SR):round(TONE_SEED[1] * SR)].copy(); seed -= seed.mean(); loop = np.r_[seed, seed[::-1]]
    tone = np.resize(loop, INSERT * SPF).copy(); r = np.linspace(0, 1, 240); cut = INSERT_AT * SPF
    head = a[:cut].copy(); tail = a[cut:].copy()
    head[-240:] = head[-240:] * (1 - r) + tone[:240] * r; tail[:240] = tail[:240] * r + tone[-240:] * (1 - r)   # house 5 ms crossfades into and out of the bed
    edited = np.concatenate([head, tone, tail]); writewav(OUT / 'edited.wav', edited)
    rms = lambda x: float(np.sqrt(np.mean(x * x)))
    audio_meta = dict(insert_output_frame=INSERT_AT, insert_frames=INSERT, insert_seconds=[INSERT_AT / FPS, (INSERT_AT + INSERT) / FPS], room_tone_seed_seconds=list(TONE_SEED), room_tone_rms=rms(seed),
                      natural_gap_seconds=[12.22, 12.96], crossfade_samples=240, encode='aac 192k (audio-changing build)')
    # ---- picture: v5's schedule with the insert
    boards = {k: cv2.imread(str(p)) for k, p in ASSETS.items()}; assert all(v is not None for v in boards.values())
    def choice(sf): return next(e for e in reversed(EVENTS) if e['sf'] <= sf)
    schedule = []; last = None
    for f in range(v5.CLOSE):
        e = choice(source_at(f))
        if e['label'] != last:
            if schedule: schedule[-1]['end'] = f
            schedule.append(dict(e, start=f)); last = e['label']
    schedule[-1]['end'] = v5.CLOSE
    hold_state = next(e for e in schedule if e['start'] <= INSERT_AT - 1 < e['end']); assert hold_state['label'] == 'horse-spoken-title', hold_state['label']
    states = {}
    for e in schedule:
        if e['board'] == 'native': continue
        states[e['label']] = render(boards[e['board']], e['marks']); cv2.imwrite(str(OUT / 'states' / (e['label'] + '.jpg')), states[e['label']], [cv2.IMWRITE_JPEG_QUALITY, 92])
    def shifted(f): return f if f < INSERT_AT else f + INSERT   # v5 output frame -> v6 output frame
    out_states = []
    for e in schedule:
        s, t = shifted(e['start']), shifted(e['end'])
        if e['start'] < INSERT_AT < e['end']: t = e['end'] + INSERT   # the held state spans the insert
        out_states.append(dict(start=s, end=t, board=e['board'], label=e['label'], marks=e['marks']))
    boundaries = {}
    for i, e in enumerate(out_states):
        if i and e['board'] != out_states[i - 1]['board']: boundaries[e['start']] = e['label']
    boundaries[INSERT_AT] = 'pause-hold-start'; boundaries[INSERT_AT + INSERT] = 'pause-hold-end'; boundaries[CLOSE] = 'standard-close'
    m = dict(scope='Review only; v5 (visual-only retrofit of the shipped v4) plus a one-second pause after "The horse raced past the barn fell."; live unchanged',
             retrofit_of=str(LIVE.relative_to(ROOT)), retrofit_of_sha256=hashes[str(LIVE.relative_to(ROOT))], output=str(DEST), fps=FPS, total_frames=TOTAL, duration=TOTAL / FPS, close_start_frame=CLOSE,
             audio=audio_meta, timeline=v5.TIMELINE, states=out_states, held_state=hold_state['label'],
             camera='v4: static full view, board fit to 1230x670 on the house stage; no dives', board_dimensions={k: list(v.shape[1::-1]) for k, v in boards.items()},
             assets={k: dict(path=str(p.relative_to(ROOT)), sha256=sha(p)) for k, p in ASSETS.items()},
             close=dict(asset='course-assets/layers/layers-close.jpg', sha256=hashes['course-assets/layers/layers-close.jpg'], prehold_frames=CLOSE_PREHOLD, push_frames=CLOSE_PUSH, zoom_endpoint=1.2, settled_frames=TOTAL - CLOSE - CLOSE_PREHOLD - CLOSE_PUSH),
             boundaries=[dict(frame=f, label=l) for f, l in sorted(boundaries.items())], protected_hashes=hashes)
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2))
    print('Prepared', TOTAL, 'frames; insert at', INSERT_AT, 'holding', hold_state['label'], '; close', CLOSE, flush=True)
    if args.prepare_only: return
    assert not DEST.exists(), f'{DEST} exists; version-suffix instead of overwriting'
    ci = cv2.imread(str(OUT / 'close.png'))
    p = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0', '-i', str(OUT / 'edited.wav'), '-map', '0:v', '-map', '1:a',
                          '-c:v', 'libx264', '-crf', '17', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    live = Reader(str(LIVE)); idx = 0; held = None
    for f in range(TOTAL):
        if f < CLOSE:
            src_f = f if f < INSERT_AT else (INSERT_AT - 1 if f < INSERT_AT + INSERT else f - INSERT)   # v5 output frame for this v6 frame
            if INSERT_AT <= f < INSERT_AT + INSERT: im = held
            else:
                while src_f >= schedule[idx]['end']: idx += 1
                e = schedule[idx]; im = live.at(src_f) if e['board'] == 'native' else states[e['label']]
                if f == INSERT_AT - 1: held = im.copy()
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
