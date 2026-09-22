#!/usr/bin/env python3
"""Questions Matter: swap the refreshed How Answers Got Easier and Faster illustration into the shipped video.

Ninth of the 2026-09-21 illustration syncs. The cast refresh replaced the board in place: same
board, same 1600x958 dimensions, same title, three columns with their photographs, TIME TO ANSWER
rows and takeaway banner, new cast in the photographs. The columns did not move, so the shipped leg
spec is reused verbatim - still full view, no camera move, seven rings in the shipped order - and
only the artwork changes.

The board runs from output frame 235 (0:07.83) to 1906 (1:03.53), 1671 frames. Nothing else
changes: the rest of the picture comes from the frozen baseline, the approved audio is
packet-copied, and the output keeps 6688 frames at 30 fps.

Stroke: the rings follow the artwork-scaled rule (owner, 2026-09-21, and his 09-21 instruction that
a synced video takes the current highlighting), which gives 4 px at this camera where the shipped
video carried 5 px. Rectangles, colors and onsets are untouched. The shipped weight was confirmed
first: the OLD JPG rendered through the shipped spec with the stroke forced to 5 reproduces the live
leg at 3.01 mean per-pixel difference, ring frames included, which also fixes the span.

Usage:
  .video-venv/bin/python scripts/video/build_questions_matter_answers_sync.py
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
TOTAL = 6688
SPAN = (235, 1906)           # half-open output frames: the How Answers Got Easier leg, 1671 frames
ASSET = ROOT / 'course-assets/questions-matter/questions-matter-answers-faster.jpg'
SHIPPED = ROOT / 'video-audit/questions-matter-repair-2026-09-16-v5/edit-manifest.json'
AUDIT = ROOT / 'video-audit/questions-matter-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-16.mp4'
BASELINE_SHA = '7ec1f3a73430bebb5deb9a39b1881cced3b611361a85ceda9f8d0e880b1bf643'
DEST = ROOT / 'Prompts/questions-matter-v6.mp4'


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/questions-matter/questions-matter.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (958, 1600), board.shape
    shipped = json.loads(SHIPPED.read_text())['boards']['answers']

    # 1. Canvas and camera, reproduced by the shipped build's own code path.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT), ASSET, 'answers')
    assert (cw, ch, ox, oy) == (1840, 1036, 120, 39), (cw, ch, ox, oy)
    assert [ox, oy] == shipped['canvas_offset']

    # 2. The shipped leg spec, verbatim, on the new canvas: still full view, same rings, same onsets.
    spec = {'image': str(canvas_path), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
            'beats': shipped['beats'], 'rings': shipped['rings']}
    frames = sum(int(b['frames']) for b in spec['beats'])
    assert frames == SPAN[1] - SPAN[0] == shipped['src_out'] - shipped['src_in'], (frames, SPAN)
    assert spec['beats'][0]['from'] == spec['beats'][0]['to'] == [cw / 2, ch / 2, float(cw)], spec['beats'][0]
    assert len(spec['rings']) == 7
    spec_path = AUDIT / 'leg-answers.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / 'leg-answers.mkv'
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
                'asset': str(ASSET), 'asset_sha256': asset_sha, 'asset_size': [1600, 958],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy}, 'shipped_manifest': str(SHIPPED),
                'beats': spec['beats'], 'rings': spec['rings'],
                'ring_stroke_px': 'artwork-scaled rule (4 px at this camera; the shipped video carried 5)',
                'replaced_output_frames': list(SPAN), 'replaced_seconds': [SPAN[0] / FPS, SPAN[1] / FPS],
                'treatment': 'compact, still, full view, three column rings, three TIME TO ANSWER rings, banner (as shipped)',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    declared = {SPAN[0]: 'source-to-board', SPAN[1]: 'board-to-source'}
    for r in spec['rings']:
        declared.setdefault(SPAN[0] + int(r['start']), f"ring-{int(r['rect'][0])}-{int(r['rect'][1])}")
    boundaries = [x for f in sorted(declared) for x in ('--boundary', f'{f}:{declared[f]}')]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            *boundaries, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
