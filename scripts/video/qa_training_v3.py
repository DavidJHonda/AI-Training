#!/usr/bin/env python3
"""QA for Prompts/training-v3.mp4: frame count, audio identity vs the live track, tail silence, contact sheets."""
from pathlib import Path
import subprocess, hashlib, json, sys
import cv2, numpy as np, imageio_ffmpeg
ROOT = Path(__file__).resolve().parents[2]; OUT = ROOT / 'video-audit/training-repair-2026-09-16'
CAND = ROOT / "Prompts/training-v4.mp4"; LIVE = ROOT / 'course-assets/training/training.mp4'
FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 48000; FPS = 30
def pcm(p):
    raw = subprocess.check_output([FF, '-v', 'error', '-i', str(p), '-vn', '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'])
    return np.frombuffer(raw, np.int16).astype(float)
n = 0; cap = cv2.VideoCapture(str(CAND)); last = None
while True:
    ok, im = cap.read()
    if not ok: break
    n += 1; last = im
m = json.load(open(OUT / 'edit-manifest.json'))
print('decoded frames', n, 'plan', m['total_frames'], 'OK' if n == m['total_frames'] else 'MISMATCH')
a, b = pcm(LIVE), pcm(CAND); L = 8249 * SR // FPS
print('live samples', len(a), 'candidate samples', len(b), 'expected', m['total_frames'] * SR // FPS)
seg_a, seg_b = a[:L], b[:L]
# AAC re-encode + 5 ms edge fades: compare by correlation and RMS of the difference, excluding the first/last 240 samples
d = seg_a[240:-240] - seg_b[240:-240]
print('audio first 8249 frames: corr %.5f, diff RMS %.1f (live RMS %.1f), peak |diff| %.0f' % (np.corrcoef(seg_a[240:-240], seg_b[240:-240])[0, 1], np.sqrt((d * d).mean()), np.sqrt((seg_a * seg_a).mean()), np.abs(d).max()))
tail = b[L:]
print('tail samples', len(tail), '= %.2f s, tail RMS %.1f, peak %.0f' % (len(tail) / SR, np.sqrt((tail * tail).mean()) if len(tail) else 0, np.abs(tail).max() if len(tail) else 0))
# closing frame is the close asset
print('last frame mean colour', last.mean(axis=(0, 1)).round(1), 'close start frame', m['close']['start_frame'], 'settle frames', m['close']['settle'])
print('corner mark:', {k: (len(v) if isinstance(v, list) else v) for k, v in m['corner_mark'].items()})
print('protected unchanged:', all(m['protected_files_unchanged'].values()))
print('sha256', hashlib.sha256(CAND.read_bytes()).hexdigest())
