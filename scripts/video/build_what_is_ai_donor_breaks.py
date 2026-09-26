#!/usr/bin/env python3
"""What Is AI?: break the live video's back-to-back board run with four Notebook drawings.

Picture-only retrofit on the shipped file (2026-09-21 illustration sync, sha 954c22da…). David 2026-09-26:
"build it with A, B, C and Maya" (video-audit/what-is-ai-donor-graphics-2026-09-26/REVIEW.md). The live
narration, rings and close stay; audio is packet-copied and the output keeps the baseline's 5298 frames.

Cutaways (half-open output frames at 30 fps), each a hard cut out of and back into the board:
  A  2280-2386 (1:16.00-1:19.53)  roll 1 two-card diagram, push from full view onto the Recommendation card
                                   under "ranking ... most likely best match"; HOW IT WORKS ring shown ~1.5 s first
  B  2925-3201 (1:37.50-1:46.70)  same diagram, slow push onto the Generative card (Prompt: "Draft an essay...")
                                   under the prompt definition; HOW IT WORKS ring shown ~3.4 s first
  C  3906-3978 (2:10.20-2:12.60)  the live video's own film-strip grid (live 0:57.5-) under "find a movie ...
                                   from an existing catalog"; THE JOB ring shown ~1.7 s first
  M  4431-4638 (2:27.70-2:34.60)  roll 1 Maya/Leo card (roll 2:26.4-) under the Maya/Leo reading; back to the
                                   board before "It generated a scene"

Roll-1 frames pass through gemini_mark.clean_frame (corner mark). The live grid frames are already clean.

Usage:
  .video-venv/bin/python scripts/video/build_what_is_ai_donor_breaks.py
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from gemini_mark import clean_frame, glyph_mask  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, W, H, TOTAL = 30, 1280, 720, 5298
AUDIT = ROOT / 'video-audit/what-is-ai-donor-graphics-2026-09-26'
LIVE = ROOT / 'course-assets/what-is-ai/what-is-ai.mp4'
BASELINE = AUDIT / 'baseline-live-2026-09-21.mp4'
BASELINE_SHA = '954c22da0e596bf5a5b957b86f33f6174e8a0cd5a862595d145d4c147edaba18'
ROLL1 = ROOT / 'Prompts/what-is-ai-1.mp4'
DEST = ROOT / 'Prompts/what-is-ai-v6.mp4'

DIAGRAM_FRAME = 1800          # roll 1 1:00.00, the two-card diagram settled and clean (overlay gone by 0:57)
FULL = (640.0, 360.0, 1280.0)  # camera: centre x, centre y, window width
LEFT_CARD = (450.0, 360.0, 900.0)   # card x 172-586, y 162-558 sits whole inside
RIGHT_CARD = (830.0, 360.0, 900.0)  # card x 694-1108

SPANS = [
    dict(key='A', out=(2280, 2386), kind='push', src=DIAGRAM_FRAME, frm=FULL, to=LEFT_CARD),
    dict(key='B', out=(2925, 3201), kind='push', src=DIAGRAM_FRAME, frm=FULL, to=RIGHT_CARD),
    dict(key='C', out=(3906, 3978), kind='clip', video='live', src=1725),
    dict(key='M', out=(4431, 4638), kind='clip', video='roll1', src=4392),
]


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def payload_hash(path: Path) -> str:
    data = subprocess.check_output([FF, '-v', 'error', '-i', str(path), '-map', '0:a', '-c', 'copy', '-f', 'data', '-'])
    return hashlib.sha256(data).hexdigest()


def read_frames(path: Path, start: int, count: int) -> list[np.ndarray]:
    cap = cv2.VideoCapture(str(path))
    out, i = [], -1
    while len(out) < count:
        ok, im = cap.read()
        assert ok, (path, start, count, i)
        i += 1
        if i >= start:
            out.append(im)
    cap.release()
    return out


def view(img: np.ndarray, cam) -> np.ndarray:
    cx, cy, w = cam
    h = w * H / W
    m = np.float32([[w / W, 0, cx - w / 2], [0, h / H, cy - h / 2]])
    return cv2.warpAffine(img, m, (W, H), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REPLICATE)


def ease(q: float) -> float:
    return q * q * (3 - 2 * q)


def prepare_donors() -> tuple[dict[int, np.ndarray], dict]:
    """Donor picture for every cutaway, keyed by output frame, plus the corner-mark tally."""
    mask = glyph_mask()
    corner = {'clone': 0, 'inpaint': 0, 'declined': []}

    def clean(im, tag):
        out, how = clean_frame(im, mask)
        if how:
            corner[how] += 1
        else:
            corner['declined'].append(tag)
        return out

    replace: dict[int, np.ndarray] = {}
    diagram = clean(read_frames(ROLL1, DIAGRAM_FRAME, 1)[0], 'diagram')
    cv2.imwrite(str(AUDIT / 'donor-diagram-clean.jpg'), diagram)
    for s in SPANS:
        a, b = s['out']
        n = b - a
        if s['kind'] == 'push':
            for k in range(n):
                q = ease(k / (n - 1))
                cam = tuple(f + (t - f) * q for f, t in zip(s['frm'], s['to']))
                replace[a + k] = view(diagram, cam)
        else:
            src = BASELINE if s['video'] == 'live' else ROLL1
            frames = read_frames(src, s['src'], n)
            if s['video'] == 'roll1':
                frames = [clean(im, f"M+{k}") for k, im in enumerate(frames)]
            for k, im in enumerate(frames):
                replace[a + k] = im
    return replace, corner


def main() -> None:
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    if not BASELINE.exists():
        shutil.copy2(LIVE, BASELINE)
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot is not the 2026-09-21 live file'
    roll1_sha = sha(ROLL1)
    replace, corner = prepare_donors()

    # One pass: baseline frames, donors swapped in; audio packet-copied from the baseline.
    p = subprocess.Popen([FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0',
                          '-i', str(BASELINE), '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '3.1',
                          '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)],
                         stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(str(BASELINE))
    f = 0
    while True:
        ok, im = cap.read()
        if not ok:
            break
        p.stdin.write(replace.get(f, im).tobytes())
        f += 1
    cap.release()
    p.stdin.close()
    assert p.wait() == 0
    assert f == TOTAL, f

    # Verify the encoded candidate.
    cap = cv2.VideoCapture(str(DEST))
    n = 0
    while cap.grab():
        n += 1
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    audio_identical = payload_hash(BASELINE) == payload_hash(DEST)
    assert (n, fps) == (TOTAL, float(FPS)), (n, fps)
    assert audio_identical
    assert sha(BASELINE) == BASELINE_SHA and sha(ROLL1) == roll1_sha

    manifest = {'candidate': str(DEST.relative_to(ROOT)), 'candidate_sha256': sha(DEST),
                'baseline': str(BASELINE.relative_to(ROOT)), 'baseline_sha256': BASELINE_SHA,
                'donor_roll1': str(ROLL1.relative_to(ROOT)), 'donor_roll1_sha256': roll1_sha,
                'cutaways': [{**s, 'out_seconds': [s['out'][0] / FPS, s['out'][1] / FPS]} for s in SPANS],
                'corner_mark': corner, 'decoded_frames': n, 'fps': fps,
                'audio_packets_identical': audio_identical, 'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    bounds = []
    for s in SPANS:
        bounds += ['--boundary', f"{s['out'][0]}:board-to-{s['key']}", '--boundary', f"{s['out'][1]}:{s['key']}-to-board"]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST), *bounds,
                            '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'corner', {k: (v if k != 'declined' else len(v)) for k, v in corner.items()},
          'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
