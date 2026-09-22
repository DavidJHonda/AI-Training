#!/usr/bin/env python3
"""Flattery Trap: swap the refreshed Flattery vs. Useful Feedback illustration into the shipped video.

Sixteenth of the 2026-09-21 illustration syncs. The cast refresh replaced the board in place: same
board, same 1600x1582 dimensions, same title, THE SCENARIO strip, the Flattery and Useful Feedback
columns with their response quotes and PRAISED / COULD FIT / NAMED / RESULT rows, and the takeaway
banner, new cast in the two photographs. The columns did not move, so the shipped leg spec is
reused verbatim - still full view, no camera move, eight rings in the shipped order - and only the
artwork changes.

The board runs from output frame 690 (0:23.00) to 2487 (1:22.90), 1797 frames. It is the only board
in this video built from this asset; the other seven legs use the cycle, sycophancy and five-moves
boards. Nothing else changes: the rest of the picture comes from the frozen baseline, the approved
audio is packet-copied, and the output keeps 9881 frames at 30 fps.

Stroke: nothing to decide here. v6 was the first build under the artwork-scaled ring rule, so the
shipped rings are already at that weight (3 px at this camera), and re-rendering under the same
default reproduces them. Confirmed before building: the OLD JPG through the shipped spec, with no
stroke override, reproduces the live leg at 2.78 mean per-pixel difference across every sample and
all eight ring onsets.

Usage:
  .video-venv/bin/python scripts/video/build_flattery_trap_comparison_sync.py
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
TOTAL = 9881
SPAN = (690, 2487)           # half-open output frames: the Flattery vs. Useful Feedback leg, 1797 frames
ASSET = ROOT / 'course-assets/flattery-trap/flattery-trap-comparison.jpg'
SHIPPED = ROOT / 'video-audit/flattery-trap-comparison-2026-09-21/build-v6/edit-manifest.json'
AUDIT = ROOT / 'video-audit/flattery-trap-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-21-v6.mp4'
BASELINE_SHA = '2449fbb325ec90a9c3440e0a546ad45634f475e77860fffbe04ba6c54e04b936'
DEST = ROOT / 'Prompts/flattery-trap-v7.mp4'


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/flattery-trap/flattery-trap.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (1582, 1600), board.shape
    shipped_all = json.loads(SHIPPED.read_text())
    assert shipped_all['render_sha256'] == BASELINE_SHA, 'build-v6 is not the live file'
    shipped = shipped_all['boards']['compare']

    # 1. Canvas and camera, reproduced by the shipped build's own code path.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT), ASSET, 'compare')
    assert (cw, ch, ox, oy) == (3040, 1710, 720, 64), (cw, ch, ox, oy)
    assert [ox, oy] == shipped['canvas_offset']

    # 2. The shipped leg spec, verbatim, on the new canvas: still full view, same rings, same onsets.
    spec = {'image': str(canvas_path), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
            'beats': shipped['beats'], 'rings': shipped['rings']}
    frames = sum(int(b['frames']) for b in spec['beats'])
    assert frames == SPAN[1] - SPAN[0] == shipped['src_out'] - shipped['src_in'], (frames, SPAN)
    assert spec['beats'][0]['from'] == spec['beats'][0]['to'] == [cw / 2, ch / 2, float(cw)], spec['beats'][0]
    assert len(spec['rings']) == 8
    spec_path = AUDIT / 'leg-compare.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / 'leg-compare.mkv'
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
                'asset': str(ASSET), 'asset_sha256': asset_sha, 'asset_size': [1600, 1582],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy}, 'shipped_manifest': str(SHIPPED),
                'beats': spec['beats'], 'rings': spec['rings'],
                'ring_stroke_px': 'artwork-scaled rule (3 px at this camera, unchanged: v6 already used this rule)',
                'replaced_output_frames': list(SPAN), 'replaced_seconds': [SPAN[0] / FPS, SPAN[1] / FPS],
                'treatment': 'compact, still, full view, scenario ring, three Flattery rows, three Useful Feedback rows, banner (as shipped)',
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
