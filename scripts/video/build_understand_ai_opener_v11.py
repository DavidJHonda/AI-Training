#!/usr/bin/env python3
"""Approved visual-only Opener repair: 8s drawing break, fixed 4px rings.

Uses the shipped v10 because its original raw roll no longer exists. The
published source, canonical JPGs, narration and timeline remain unchanged.
Run --prepare-only to inspect states, then run without arguments to encode.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile

import cv2
import imageio_ffmpeg

from editspec_build import Build
from ken_burns_path import draw_ring, ring_px, rings_for, window

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'course-assets/understand-ai-opener/understand-ai-opener.mp4'
EXPECTED = '2fcdd916bd77a35be247f4fbc6b0f8aecb98b7b641528c390fd0c5746826d40b'
OLD = ROOT / 'video-audit/understand-ai-opener-comparison-2026-09-22/build-v10'
OUT = ROOT / 'video-audit/understand-ai-opener-repair-2026-09-27-v11'
DEST = ROOT / 'Prompts/understand-ai-opener-v11.mp4'
ASSETS = ROOT / 'course-assets/understand-ai-opener'
FPS, TOTAL = 30, 4441
BREAK_IN, BREAK_OUT, DONOR_FRAME = 3235, 3475, 2400
SPANS = {'kind': (0, 352), 'hood': (1733, 1958), 'map': (2423, 4174)}
NAMES = {'kind': 'kind', 'hood': 'under-hood', 'map': 'section-map'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def render_states(spec, key):
    """Cache static full-board states using the shared renderer's geometry."""
    image = cv2.imread(spec['image'])
    ih, iw = image.shape[:2]
    cx, cy, width = spec['beats'][0]['from']
    assert spec['beats'][0]['to'] == [cx, cy, width]
    x, y, ww, hh = window(cx, cy, width, 16 / 9, iw, ih)
    up = spec['upscale']
    big = cv2.resize(image, (iw * up, ih * up), interpolation=cv2.INTER_LANCZOS4)
    xx, yy, w, h = [int(round(v * up)) for v in (x, y, ww, hh)]
    base = cv2.resize(big[yy:yy+h, xx:xx+w], (1280, 720), interpolation=cv2.INTER_AREA)
    rings = rings_for(spec)
    ends = sorted({0, spec['beats'][0]['frames'], *[n for a, b, *_ in rings for n in (a, b)]})
    states = []
    for start, end in zip(ends, ends[1:]):
        frame = base.copy()
        for a, b, rect, color, pad, radius in rings:
            if not a <= start < b:
                continue
            rx, ry, rw, rh = rect
            scale, t = 1280 / ww, ring_px(720)
            half = t / 2
            draw_ring(frame, (rx-pad-x)*scale-half, (ry-pad-y)*scale-half,
                      (rx+rw+pad-x)*scale+half, (ry+rh+pad-y)*scale+half,
                      color, radius*scale+half, t)
        cv2.imwrite(str(OUT / 'preview' / f'{key}-{start:04d}.png'), frame)
        states.append((start, end, frame))
    return states


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    assert sha(SOURCE) == EXPECTED, 'Published source changed; review required.'
    assert not DEST.exists(), 'Never overwrite a review candidate.'
    OUT.mkdir(parents=True, exist_ok=True)
    snapshot_record = OUT / 'source-snapshot.json'
    if snapshot_record.exists():
        snapshot = Path(json.loads(snapshot_record.read_text())['path'])
    else:
        snapshot = Path(tempfile.mkdtemp(prefix='understand-opener-v11-')) / 'source-v10.mp4'
        shutil.copyfile(SOURCE, snapshot)
        snapshot_record.write_text(json.dumps({'path': str(snapshot), 'sha256': EXPECTED}, indent=2))
    assert sha(snapshot) == EXPECTED
    assets = {k: ASSETS / f'understand-ai-opener-{NAMES[k]}.jpg' for k in SPANS}
    protected = [SOURCE, *assets.values(), ASSETS / 'understand-ai-opener-close.jpg',
                 ROOT / 'lessons/Opener-Understand.md']
    hashes = {str(p): sha(p) for p in protected}
    build = Build(ROOT, snapshot, OUT, DEST, protected=protected)
    build.tall_margin = True
    old_manifest = json.loads((OLD / 'edit-manifest.json').read_text())
    assert old_manifest['render_sha256'] == EXPECTED
    states, specs = {}, {}
    for key, asset in assets.items():
        assert sha(asset) == old_manifest['protected_hashes'][str(asset)]
        canvas, cw, ch, ox, oy = build.compose(asset, key)
        spec = json.loads((OLD / f'leg-{key}.json').read_text())
        assert spec['beats'][0]['from'] == [cw / 2, ch / 2, float(cw)]
        spec['image'] = str(canvas)
        spec['provenance'] = {'canonical_asset': str(asset), 'sha256': sha(asset),
                              'offset': [ox, oy], 'density': 'compact', 'ring_px': ring_px(720)}
        (OUT / f'leg-{key}.json').write_text(json.dumps(spec, indent=2))
        specs[key] = spec
        states[key] = render_states(spec, key)
    cap = cv2.VideoCapture(str(snapshot))
    for n in range(DONOR_FRAME + 1):
        ok, donor = cap.read()
        assert ok, n
    cap.release()
    cv2.imwrite(str(OUT / 'donor-prompt-transformation-response.png'), donor)
    boundaries = old_manifest['boundaries'] + [
        {'frame': BREAK_IN, 'label': 'Map-to-settled-drawing'},
        {'frame': BREAK_OUT, 'label': 'Drawing-to-map-continuation'}]
    manifest = {
        'scope': 'Approved narrow visual-only repair; review candidate, not publication.',
        'approval': 'User yes to drawing break, 4px rings, unchanged narration/framing/close.',
        'source': str(SOURCE), 'source_snapshot': str(snapshot), 'source_sha256': EXPECTED,
        'output': str(DEST), 'fps': FPS, 'total_frames': TOTAL, 'duration': TOTAL / FPS,
        'audio': 'Original stream copied with -c:a copy; no cuts, pauses, grafts or fades.',
        'boards': specs, 'board_spans_before_break': SPANS,
        'notebook_interleaves': [{'source_frame': DONOR_FRAME, 'source_time': DONOR_FRAME/FPS,
            'snapshot': str(OUT / 'donor-prompt-transformation-response.png'),
            'output_frames': [BREAK_IN, BREAK_OUT], 'duration': 8,
            'treatment': 'Hold settled existing drawing, no motion or audio change.'}],
        'map_runs': [[2423, BREAK_IN], [BREAK_OUT, 4174]],
        'map_run_seconds': [(BREAK_IN-2423)/FPS, (4174-BREAK_OUT)/FPS],
        'longest_teaching_board_run_seconds': (BREAK_IN-2423)/FPS,
        'longest_board_chain_including_close_seconds': (TOTAL-BREAK_OUT)/FPS,
        'pacing_exception': 'Approved residual map runs ~27s and ~23s; no filler.',
        'close': {'frames': [4174, TOTAL], 'treatment': 'Existing source picture preserved.'},
        'boundaries': sorted(boundaries, key=lambda b: b['frame']),
        'protected_hashes': hashes,
        'limitations': ['Only published source survives; retained source footage re-encoded once.',
                       'No real-time listening or full playback certification.']}
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2))
    if args.prepare_only:
        print('Prepared board states and donor for inspection.', flush=True)
        return
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    command = [ff, '-n', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1280x720',
               '-r', str(FPS), '-i', 'pipe:0', '-i', str(snapshot), '-map', '0:v:0', '-map', '1:a:0',
               '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p',
               '-c:a', 'copy', '-movflags', '+faststart', str(DEST)]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(str(snapshot))
    count = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if BREAK_IN <= count < BREAK_OUT:
            frame = donor
        else:
            for key, (a, b) in SPANS.items():
                if a <= count < b:
                    frame = next(im for s, e, im in states[key] if s <= count-a < e)
                    break
        proc.stdin.write(frame.tobytes())
        count += 1
        if count % 900 == 0:
            print(f'Encoded {count}/{TOTAL} frames', flush=True)
    cap.release()
    proc.stdin.close()
    assert proc.wait() == 0
    assert count == TOTAL, count
    manifest['render_sha256'] = sha(DEST)
    manifest['encode_command'] = command
    manifest['protected_files_unchanged'] = {p: sha(p) == h for p, h in hashes.items()}
    assert all(manifest['protected_files_unchanged'].values())
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2))
    print(DEST, flush=True)


if __name__ == '__main__':
    cv2.setNumThreads(1)
    main()
