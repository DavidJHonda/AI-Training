"""Verify the encoded review candidate, without installing or modifying it."""
from pathlib import Path
import hashlib
import json
import subprocess
import wave

import av
import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
m = json.loads((OUT / 'edit-manifest.json').read_text())
candidate = Path(m['output'])
with av.open(str(candidate)) as container:
    video = container.streams.video[0]
    audio = container.streams.audio[0]
    metadata = dict(video_codec=video.codec_context.name,
        audio_codec=audio.codec_context.name, width=video.width, height=video.height,
        fps=float(video.average_rate), sample_rate=audio.sample_rate)
    pts = [float(frame.pts * frame.time_base) for frame in container.decode(video)]
assert len(pts) == m['total_frames'], (len(pts), m['total_frames'])
assert metadata['width'] == 1280 and metadata['height'] == 720
assert metadata['fps'] == 30
assert max(abs(d - 1 / 30) for d in np.diff(pts)) < .00001

frames_dir = OUT / 'verified-frames'
frames_dir.mkdir(exist_ok=True)
wanted = {0, 566, 837, 1938, 2656, 2778, 2865, 2960, 3039, 3139, 3243, 3362}
capture = cv2.VideoCapture(str(candidate))
i = 0
picked = {}
while True:
    ok, frame = capture.read()
    if not ok:
        break
    if i in wanted:
        picked[i] = frame
        cv2.imwrite(str(frames_dir / f'frame-{i:05d}.jpg'), frame)
    i += 1
capture.release()
assert i == m['total_frames']
close = cv2.imread(str(OUT / 'close.png'))
h, w = close.shape[:2]
ww = w / 1.2
hh = ww * 9 / 16
expected = cv2.warpAffine(close,
    np.float32([[ww / 1280, 0, (w - ww) / 2],
                [0, hh / 720, (h - hh) / 2]]), (1280, 720),
    flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)
final_mae = float(abs(expected.astype(float) - picked[3362].astype(float)).mean())
assert final_mae < 3, final_mae

ff = imageio_ffmpeg.get_ffmpeg_exe()
decoded = subprocess.check_output([ff, '-v', 'error', '-i', str(candidate),
    '-vn', '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'])
actual = np.frombuffer(decoded, dtype=np.float32).astype(float)
with wave.open(str(OUT / 'edited.wav')) as stream:
    reference = np.frombuffer(stream.readframes(stream.getnframes()), np.int16).astype(float) / 32768
assert abs(len(actual) - len(reference)) <= 1024
common = min(len(reference), len(actual))
correlation = float(np.corrcoef(reference[:common], actual[:common])[0, 1])
assert correlation > .99, correlation

joins = []
for row in m['timeline'][1:]:
    frame = row['start_frame']
    at = frame * 1600
    handle = actual[max(0, at - 240):at + 240]
    joins.append(dict(output_frame=frame, output_seconds=frame / 30,
        peak_in_5ms_handles_dbfs=float(20 * np.log10(max(abs(handle).max(), 1e-9)))))

report = dict(candidate=str(candidate), sha256=hashlib.sha256(candidate.read_bytes()).hexdigest(),
    bytes=candidate.stat().st_size, metadata=metadata, decoded_frames=i,
    expected_frames=m['total_frames'], duration_seconds=i / 30,
    original_duration_seconds=4747 / 30, saved_seconds=(4747 - i) / 30,
    final_frame_canonical_close_mae=final_mae,
    encoded_audio_reference_correlation=correlation,
    encoded_audio_peak_dbfs=float(20 * np.log10(max(abs(actual).max(), 1e-9))),
    audio_joins=joins,
    protected_files_unchanged={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() == h
        for p, h in m['protected_hashes'].items()},
    direct_listening_performed=False, continuous_motion_review_performed=False,
    installed=False)
assert all(report['protected_files_unchanged'].values())
(OUT / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
boundaries = sorted({r['start_frame'] for r in m['timeline'][1:]})
command = [str(ROOT / '.video-venv/bin/python'), str(ROOT / 'scripts/video/transition_guard.py'),
    str(candidate), '--outdir', str(OUT / 'transitions')]
for frame in boundaries:
    command += ['--boundary', f'{frame}:edit-{frame}']
subprocess.run(command, check=True)
print(json.dumps(report, indent=2))
