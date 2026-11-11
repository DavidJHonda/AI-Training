#!/usr/bin/env python3
"""Technical QA of the actual encoded candidate; does not certify listening."""
from pathlib import Path
import json
import subprocess
import sys

import av
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import readwav
from ring_stroke import side_runs, hex_bgr

OUT = Path(__file__).resolve().parent
manifest = json.loads((OUT / 'edit-manifest.json').read_text())
candidate = Path(manifest['output'])
assert 'render_sha256' in manifest, 'Wait for rendering to complete.'
qa_dir = OUT / 'qa'
qa_dir.mkdir(exist_ok=True)
boundaries = sorted(set(row['start_frame'] for row in manifest['timeline'][1:]))
cmd = [str(ROOT / '.video-venv/bin/python'), str(ROOT / 'scripts/video/transition_guard.py'),
       str(candidate), '--outdir', str(qa_dir / 'transitions')]
for f in boundaries:
    cmd.extend(['--boundary', f'{f}:edit'])
subprocess.run(cmd, check=True)

spec = json.loads((OUT / 'leg-map.json').read_text())
map_start = manifest['shared_intro_graft']['output_frames'][0]
samples = {0, manifest['total_frames'] - 1, map_start, manifest['close']['start_frame']}
samples.update(map_start + ring['start'] + 25 for ring in spec['rings'])
samples.update(range(0, manifest['total_frames'], 90))
sampled = {}
black_frames = []
capture = cv2.VideoCapture(str(candidate))
fps = capture.get(cv2.CAP_PROP_FPS)
width, height = int(capture.get(3)), int(capture.get(4))
count = 0
previous = None
maximum_step = 0
while True:
    ok, frame = capture.read()
    if not ok:
        break
    if float(frame.mean()) < 3:
        black_frames.append(count)
    if count in samples:
        sampled[count] = frame.copy()
    if previous is not None:
        maximum_step = max(maximum_step, float(np.abs(frame.astype(np.int16) - previous).mean()))
    previous = frame.astype(np.int16)
    count += 1
capture.release()
assert count == manifest['total_frames'], (count, manifest['total_frames'])
assert (width, height, fps) == (1280, 720, 30)
assert not black_frames
for f in sorted(samples):
    if f in sampled:
        cv2.imwrite(str(qa_dir / f'frame-{f:05d}.jpg'), sampled[f])

ring_checks = []
for ring in spec['rings']:
    f = map_start + ring['start'] + 25
    frame = sampled[f]
    mask = (np.sqrt(((frame.astype(np.int32) - hex_bgr(ring['color'])) ** 2).sum(axis=2)) < 45).astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    found = []
    for k in range(1, n):
        x, y, w, h, area = stats[k]
        if w > 900 and 80 < h < 200:
            stroke, sides = side_runs(labels, k, x, y, w, h)
            found.append(dict(frame=f, color=ring['color'], box=[int(x), int(y), int(w), int(h)],
                              median_stroke=stroke, sides=sides))
    assert len(found) == 1, (ring, found)
    assert 3.5 <= found[0]['median_stroke'] <= 4.5, found
    ring_checks.extend(found)

ff = __import__('imageio_ffmpeg').get_ffmpeg_exe()
wav = OUT / 'encoded-audio.wav'
subprocess.run([ff, '-y', '-v', 'error', '-i', str(candidate), '-vn', '-ac', '1',
                '-ar', '48000', '-c:a', 'pcm_s16le', str(wav)], check=True)
actual, expected = readwav(wav), readwav(OUT / 'edited.wav')
assert abs(len(actual) - len(expected)) < 2048
n = min(len(actual), len(expected))
signal = expected[:n]
error = actual[:n] - signal
snr = float(10 * np.log10(np.sum(signal ** 2) / np.sum(error ** 2)))
correlation = float(np.corrcoef(actual[:n:100], expected[:n:100])[0, 1])
assert snr > 20, snr
assert correlation > .995, correlation
peak = float(np.max(np.abs(actual)) / 32768)
assert peak < .9999

container = av.open(str(candidate))
streams = [dict(type=s.type, codec=s.codec_context.name,
                sample_rate=s.codec_context.sample_rate if s.type == 'audio' else None)
           for s in container.streams]
container.close()

# Verify the encoded settled last frame against the exact canonical close at 1.2x.
close_image = cv2.imread(str(OUT / 'close.png'))
h, w = close_image.shape[:2]
ww, hh = w / 1.2, w / 1.2 * 9 / 16
reference = cv2.warpAffine(close_image, np.float32([
    [ww / 1280, 0, (w - ww) / 2], [0, hh / 720, (h - hh) / 2],
]), (1280, 720), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
last = sampled[manifest['total_frames'] - 1]
close_difference = float(np.abs(last.astype(float) - reference.astype(float)).mean())
assert close_difference < 3, close_difference

result = dict(
    candidate=str(candidate), decoded_frames=count, expected_frames=manifest['total_frames'],
    duration=count / fps, width=width, height=height, fps=fps, black_frames=black_frames,
    ring_checks=ring_checks, encoded_audio_snr_db=snr, encoded_audio_correlation=correlation,
    encoded_audio_peak=peak, streams=streams, final_close_mean_absolute_error=close_difference,
    protected_files_unchanged=manifest['protected_files_unchanged'],
    direct_listening_performed=False, continuous_motion_review_performed=False,
    technical_checks_pass=True,
)
(OUT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
