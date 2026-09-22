#!/usr/bin/env python3
"""Training Bias: swap the refreshed Wrong Pattern. Wrong Answer. illustration into the shipped video.

Fourteenth of the 2026-09-21 illustration syncs. The cast refresh replaced the board in place: same
board, same 1600x1308 dimensions, same title, photograph and takeaway banner, new cast in the
photograph. The composition did not move - the brass machine and the beach card sit where they sat -
so the shipped camera walk is reused verbatim and only the artwork changes. No rings on this board.

The board runs from output frame 657 (0:21.90) to 1012 (0:33.73), 355 frames: 118-frame establish
with a small push, 30-frame dive to the machine, 85-frame hold, 30-frame move to the beach card,
92-frame hold. The walk ends on that dive, with no pull-back - as shipped.

Nothing else changes: the rest of the picture comes from the frozen baseline, the approved audio is
packet-copied, and the output keeps 7830 frames at 30 fps.

Usage:
  .video-venv/bin/python scripts/video/build_training_bias_wrong_pattern_sync.py
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
TOTAL = 7830
SPAN = (657, 1012)           # half-open output frames: the Wrong Pattern leg, 355 frames
ASSET = ROOT / 'course-assets/training-bias/training-bias-wrong-pattern.jpg'
SHIPPED = ROOT / 'video-audit/training-bias-comparison-2026-09-21/build-v6/edit-manifest.json'
AUDIT = ROOT / 'video-audit/training-bias-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-21-v6.mp4'
BASELINE_SHA = '705abdb1ad860ea9b39b8baa52699a34ae7a5003761c184c8dcf73abf1045d70'
DEST = ROOT / 'Prompts/training-bias-v7.mp4'


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/training-bias/training-bias.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (1308, 1600), board.shape
    shipped = json.loads(SHIPPED.read_text())
    assert shipped['render_sha256'] == BASELINE_SHA, 'build-v6 is not the live file'
    wrong = shipped['boards']['wrong']

    # 1. Canvas and camera, reproduced by the shipped build's own code path.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT), ASSET, 'wrong')
    assert (cw, ch, ox, oy) == (2512, 1414, 456, 53), (cw, ch, ox, oy)
    assert [ox, oy] == wrong['canvas_offset']

    # 2. The shipped camera walk, verbatim, on the new canvas.
    spec = {'image': str(canvas_path), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
            'beats': wrong['beats'], 'rings': wrong.get('rings', [])}
    frames = sum(int(b['frames']) for b in spec['beats'])
    assert frames == SPAN[1] - SPAN[0] == wrong['src_out'] - wrong['src_in'], (frames, SPAN)
    assert spec['beats'][0]['from'] == [cw / 2, ch / 2, float(cw)], spec['beats'][0]
    assert not spec['rings']
    spec_path = AUDIT / 'leg-wrong.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / 'leg-wrong.mkv'
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
                'asset': str(ASSET), 'asset_sha256': asset_sha, 'asset_size': [1600, 1308],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy}, 'shipped_manifest': str(SHIPPED),
                'beats': spec['beats'], 'rings': spec['rings'],
                'replaced_output_frames': list(SPAN), 'replaced_seconds': [SPAN[0] / FPS, SPAN[1] / FPS],
                'treatment': 'illustration camera walk: establish, dive to the machine, hold, move to the beach card, hold (as shipped); no rings, no pull-back',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    declared = {SPAN[0]: 'source-to-board', SPAN[1]: 'board-to-source'}
    at = SPAN[0]
    for b in spec['beats']:
        declared.setdefault(at, f"beat-{b['label'].replace(' ', '-')}")
        at += int(b['frames'])
    boundaries = [x for f in sorted(declared) for x in ('--boundary', f'{f}:{declared[f]}')]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            *boundaries, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
