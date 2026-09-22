#!/usr/bin/env python3
"""Learn with AI: swap the refreshed How Gemini Notebook Works illustration into the shipped video.

Fifth of the 2026-09-21 illustration syncs. The cast refresh replaced the lesson's How Gemini
Notebook Works board in place: same board, same 1600x844 dimensions, same title, two cards and
takeaway banner, new cast in the two photographs. The cards did not move, so the shipped ring
rectangles land on exactly the same components - this build reuses the shipped leg spec verbatim
(same rects, same colors, same onsets, same 669-frame still full view) and only repoints it at the
current JPG.

The board runs from output frame 3812 (2:07.07) to 4481 (2:29.37). Nothing else changes: the rest
of the picture comes from the frozen baseline, the approved audio is packet-copied, and the output
keeps 6613 frames at 30 fps.

Stroke: this wide board fills the frame at full view, so the artwork-scaled rule (owner,
2026-09-21) draws 5 px here - the same weight the video already carries. Verified before building:
the OLD JPG rendered through the shipped spec under the current rule reproduces the live leg at
3.04 mean per-pixel difference, ring frames included.

Usage:
  .video-venv/bin/python scripts/video/build_learn_with_ai_how_it_works_sync.py
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
TOTAL = 6613
SPAN = (3812, 4481)          # half-open output frames: the How Gemini Notebook Works leg, 669 frames
ASSET = ROOT / 'course-assets/learn-with-ai/learn-with-ai-how-it-works.jpg'
SHIPPED_LEG = ROOT / 'video-audit/learn-with-ai-repair-2026-09-16/leg-2-how-it-works.json'
AUDIT = ROOT / 'video-audit/learn-with-ai-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-16.mp4'
BASELINE_SHA = 'e4d26573870672be262a919e3e54f1602c906703669900d3a37b156033d93d2b'
DEST = ROOT / 'Prompts/learn-with-ai-v8.mp4'


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/learn-with-ai/learn-with-ai.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (844, 1600), board.shape

    # 1. Canvas and camera, reproduced by the shipped build's own code path.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT), ASSET, '2-how-it-works')
    assert (cw, ch, ox, oy) == (1600, 900, 0, 28), (cw, ch, ox, oy)

    # 2. The shipped leg spec, verbatim, on the new canvas: same beats, same rings, standard stroke.
    shipped = json.loads(SHIPPED_LEG.read_text())
    spec = {**shipped, 'image': str(canvas_path)}
    frames = sum(int(b['frames']) for b in spec['beats'])
    assert frames == SPAN[1] - SPAN[0], (frames, SPAN)
    assert spec['beats'][0]['from'] == [cw / 2, ch / 2, float(cw)], spec['beats'][0]
    assert [r['rect'] for r in spec['rings']] == [r['rect'] for r in shipped['rings']]
    spec_path = AUDIT / 'leg-2-how-it-works.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / 'leg-2-how-it-works.mkv'
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
                'asset': str(ASSET), 'asset_sha256': asset_sha, 'asset_size': [1600, 844],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy, 'camera': spec['beats'][0]['from']},
                'shipped_leg_spec': str(SHIPPED_LEG), 'rings': spec['rings'],
                'ring_stroke_px': 'artwork-scaled rule (5 px at this camera, as shipped)',
                'replaced_output_frames': list(SPAN), 'replaced_seconds': [SPAN[0] / FPS, SPAN[1] / FPS],
                'treatment': 'compact, still, full view, two card rings and the banner (as shipped)',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    ring_boundaries = []
    for r in spec['rings']:
        ring_boundaries += ['--boundary', f"{SPAN[0] + int(r['start'])}:ring-on-{int(r['rect'][0])}-{int(r['rect'][1])}"]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            '--boundary', f'{SPAN[0]}:source-to-board', '--boundary', f'{SPAN[1]}:board-to-source',
                            *ring_boundaries, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
