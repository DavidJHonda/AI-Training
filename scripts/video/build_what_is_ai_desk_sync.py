#!/usr/bin/env python3
"""What Is AI?: swap the refreshed Ask the Desk illustration into the shipped video.

Illustration-only retrofit under RETROFIT-PLAYBOOK.md, the same pass run on Why Learn AI
on 2026-09-21 (scripts/video/build_why_learn_ai_press_sync.py). The lesson's illustration
(course-assets/what-is-ai/what-is-ai-ask-the-desk.jpg) was replaced in the 2026-09-21 cast
refresh: same board, same 1600x1150 dimensions, same title, photo rect, speech bubbles and
takeaway banner, new cast in the photograph. The shipped video shows it, still and whole,
from output frame 370 (0:12.33) through 573 (0:19.10).

Nothing else changes. The rest of the picture comes from the frozen baseline, the approved
audio is packet-copied, and the output keeps 5298 frames at 30 fps.

The pristine roll this video was assembled from no longer exists, so the baseline is the
shipped file itself, snapshotted in the audit directory. Geometry is reproduced by the same
code that built the leg in the shipped video (editspec_build.Build.compose with
tall_margin=False), which on a 1600x1150 board yields a 2044x1150 canvas at offset (222, 0)
and the full-view camera window [1022, 575, 2044] - identical to leg-desk.json in the 09-16
audit.

Usage:
  .video-venv/bin/python scripts/video/build_what_is_ai_desk_sync.py
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
TOTAL = 5298
SPAN = (370, 574)            # half-open output frames: the desk board leg, 204 frames, no pause hold after it
ASSET = ROOT / 'course-assets/what-is-ai/what-is-ai-ask-the-desk.jpg'
AUDIT = ROOT / 'video-audit/what-is-ai-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-16.mp4'
BASELINE_SHA = '640a8d915399e213073f6d191755b5fef1f0abf55e582c68db816c69dfe37e07'
DEST = ROOT / 'Prompts/what-is-ai-v2.mp4'


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/what-is-ai/what-is-ai.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (1150, 1600), board.shape

    # 1. Canvas and camera, reproduced by the shipped build's own code path.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT, tall_margin=False), ASSET, 'desk')
    assert (cw, ch, ox, oy) == (2044, 1150, 222, 0), (cw, ch, ox, oy)
    full = [cw / 2, ch / 2, float(cw)]
    assert full == [1022.0, 575.0, 2044.0], full

    # 2. One still leg over the board's span.
    frames = SPAN[1] - SPAN[0]
    spec = {'image': str(canvas_path), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
            'beats': [{'label': 'full-view', 'frames': frames, 'from': full, 'to': full}], 'rings': []}
    spec_path = AUDIT / 'leg-desk.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / 'leg-desk.mkv'
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
                'treatment': 'compact, still, full view, no rings (as shipped)',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            '--boundary', f'{SPAN[0]}:source-to-desk', '--boundary', f'{SPAN[1]}:desk-to-source',
                            '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
