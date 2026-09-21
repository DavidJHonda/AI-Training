#!/usr/bin/env python3
"""Why Learn AI?: swap the refreshed AI Is the Press illustration into the shipped video.

Illustration-only retrofit under RETROFIT-PLAYBOOK.md. The lesson's illustration
(course-assets/why-learn-ai/why-learn-ai-press.jpg) was replaced in the 2026-09-21
cast refresh: same board, same 1600x1150 dimensions, same title/banner/photo rect,
new cast in the photograph. The shipped video shows it, still and whole, from
output frame 417 (0:13.90) through 756 (0:25.23) - the 310-frame board leg plus
the 30-frame pause hold that follows it, every frame identical.

Nothing else changes. The rest of the picture comes from the frozen baseline, the
approved audio is packet-copied, and the output keeps 7117 frames at 30 fps.

The pristine rolls this video was assembled from (Prompts/why-learn-ai-1.mp4 and
-2.mp4) no longer exist, so the baseline is the shipped file itself, snapshotted in
the audit directory. Geometry is reproduced by the same code that built the leg in
the shipped v6 (editspec_build.Build.compose with tall_margin=False), which on a
1600x1150 board yields a 2044x1150 canvas at offset (222, 0) and the full-view
camera window [1022, 575, 2044] - identical to leg-1-press.json in the 09-16 audit.

Usage:
  .video-venv/bin/python scripts/video/build_why_learn_ai_press_sync.py
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import types
from pathlib import Path

import cv2
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Build  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
TOTAL = 7117
SPAN = (417, 757)            # half-open output frames: board leg 417-727 + pause hold 727-757
ASSET = ROOT / 'course-assets/why-learn-ai/why-learn-ai-press.jpg'
AUDIT = ROOT / 'video-audit/why-learn-ai-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-16.mp4'
BASELINE_SHA = 'd3759d7ff1dcf31592cf0e9a55e68d859d4ac99d3015b96bfab39e0274dd38b3'
DEST = ROOT / 'Prompts/why-learn-ai-v7.mp4'


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def payload_hash(path: Path, stream: str = 'a') -> str:
    data = subprocess.check_output([FF, '-v', 'error', '-i', str(path), '-map', f'0:{stream}', '-c', 'copy', '-f', 'data', '-'])
    return hashlib.sha256(data).hexdigest()


def decoded_frames(path: Path) -> tuple[int, float]:
    cap = cv2.VideoCapture(str(path))
    n = 0
    while cap.grab():
        n += 1
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return n, fps


def main() -> None:
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/why-learn-ai/why-learn-ai.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (1150, 1600), board.shape

    # 1. Canvas and camera, reproduced by the shipped build's own code path.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT, tall_margin=False), ASSET, '1-press')
    assert (cw, ch, ox, oy) == (2044, 1150, 222, 0), (cw, ch, ox, oy)
    full = [cw / 2, ch / 2, float(cw)]
    assert full == [1022.0, 575.0, 2044.0], full

    # 2. One still leg covering the board and the pause hold that follows it.
    frames = SPAN[1] - SPAN[0]
    spec = {'image': str(canvas_path), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
            'beats': [{'label': 'full-view', 'frames': frames, 'from': full, 'to': full}], 'rings': []}
    spec_path = AUDIT / 'leg-1-press.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / 'leg-1-press.mkv'
    leg.unlink(missing_ok=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'), str(spec_path), str(leg)], check=True)
    assert decoded_frames(leg)[0] == frames

    # 3. One assembly pass: baseline head, new leg, baseline tail; audio packet-copied.
    graph = [f'[0:v]trim=start_frame=0:end_frame={SPAN[0]},setpts=N/({FPS}*TB),setsar=1[a]',
             f'[1:v]setpts=N/({FPS}*TB),setsar=1,format=yuv420p[b]',
             f'[0:v]trim=start_frame={SPAN[1]}:end_frame={TOTAL},setpts=N/({FPS}*TB),setsar=1[c]',
             f'[a][b][c]concat=n=3:v=1:a=0,setpts=N/({FPS}*TB),format=yuv420p[v]']
    subprocess.run([FF, '-v', 'error', '-i', str(BASELINE), '-i', str(leg),
                    '-filter_complex', ';'.join(graph), '-map', '[v]', '-map', '0:a',
                    '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '3.1', '-crf', '16', '-preset', 'fast',
                    '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], check=True)

    # 4. Verify the encoded candidate, not the plan.
    n, fps = decoded_frames(DEST)
    audio_identical = payload_hash(BASELINE) == payload_hash(DEST)
    assert (n, fps) == (TOTAL, float(FPS)), (n, fps)
    assert audio_identical
    assert sha(BASELINE) == BASELINE_SHA and sha(ASSET) == asset_sha

    manifest = {'candidate': str(DEST), 'candidate_sha256': sha(DEST), 'baseline': str(BASELINE), 'baseline_sha256': BASELINE_SHA,
                'asset': str(ASSET), 'asset_sha256': asset_sha, 'asset_size': [1600, 1150],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy, 'camera': full},
                'replaced_output_frames': list(SPAN), 'replaced_seconds': [SPAN[0] / FPS, SPAN[1] / FPS],
                'treatment': 'compact, still, full view, no rings (as shipped v6)',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            '--boundary', f'{SPAN[0]}:source-to-press', '--boundary', f'{SPAN[1]}:press-to-source',
                            '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
