#!/usr/bin/env python3
"""Work With AI opener: swap the refreshed Same Tool. Different Results. illustration into the shipped video.

Sixth of the 2026-09-21 illustration syncs, and the first over a camera walk. The cast refresh
replaced the board in place: same board, same 1600x1150 dimensions, same title, photograph rect,
the two phone panels inside it and the takeaway banner, new cast in the photograph. The composition
did not move, so the shipped camera walk is reused verbatim - establish with a small push, zoom to
the two phone photos, hold, pull back to the full illustration, hold - and only the artwork changes.

The board is on screen from output frame 1410 (0:47.00) to 1779 (0:59.30), in three pieces the
shipped build created: the walk's first 332 frames (1410-1742), a 30-frame pause that freezes the
last walk frame (1742-1772), and the walk's last 7 frames under the tail (1772-1779). This build
reproduces all three from one 339-frame leg, so the freeze lands on the same frame it always did.

Nothing else changes. The rest of the picture comes from the frozen baseline, the approved audio is
packet-copied, and the output keeps 4737 frames at 30 fps.

The pristine roll this video was assembled from no longer exists, so the baseline is the shipped
file itself, snapshotted in the audit directory. Geometry is reproduced by the same code that built
the shipped leg - editspec_build.Build.compose with tall_margin=False - giving a 2044x1150 canvas at
offset (222, 0), the full view [1022, 575, 2044] and the photo window [1032, 505.4375, 1342],
identical to leg-same-tool.json in the 09-16 audit.

Usage:
  .video-venv/bin/python scripts/video/build_opener_work_same_tool_sync.py
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
TOTAL = 4737
SPAN = (1410, 1779)          # half-open output frames the board occupies, walk + pause freeze + tail
WALK_CUT = 332               # leg frames before the pause; the freeze holds leg frame 331
HOLD = 30                    # pause frames, holding that same frame
ASSET = ROOT / 'course-assets/work-with-ai-opener/work-with-ai-opener-same-tool.jpg'
SHIPPED_LEG = ROOT / 'video-audit/opener-work-repair-2026-09-16/leg-same-tool.json'
AUDIT = ROOT / 'video-audit/opener-work-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-16.mp4'
BASELINE_SHA = '34a4e9ef42337b1bb1ee46560a62daa13f275826392dda035bd72b260de35280'
DEST = ROOT / 'Prompts/work-with-ai-opener-v8.mp4'


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/work-with-ai-opener/work-with-ai-opener.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (1150, 1600), board.shape

    # 1. Canvas and camera, reproduced by the shipped build's own code path.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT, tall_margin=False), ASSET, 'same-tool')
    assert (cw, ch, ox, oy) == (2044, 1150, 222, 0), (cw, ch, ox, oy)

    # 2. The shipped camera walk, verbatim, on the new canvas.
    shipped = json.loads(SHIPPED_LEG.read_text())
    spec = {**shipped, 'image': str(canvas_path)}
    walk = sum(int(b['frames']) for b in spec['beats'])
    assert walk == 339 and walk + HOLD == SPAN[1] - SPAN[0], (walk, SPAN)
    assert spec['beats'][0]['from'] == [cw / 2, ch / 2, float(cw)], spec['beats'][0]
    assert not spec.get('rings')
    spec_path = AUDIT / 'leg-same-tool.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / 'leg-same-tool.mkv'
    leg.unlink(missing_ok=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'), str(spec_path), str(leg)], check=True)
    assert decoded_frames(leg)[0] == walk

    # 3. Re-time the walk the way the shipped build did: walk[:332], the pause freezing walk[331], walk[332:].
    cap = cv2.VideoCapture(str(leg))
    frames = []
    while True:
        ok, im = cap.read()
        if not ok:
            break
        frames.append(im)
    cap.release()
    assert len(frames) == walk
    sequence = frames[:WALK_CUT] + [frames[WALK_CUT - 1]] * HOLD + frames[WALK_CUT:]
    assert len(sequence) == SPAN[1] - SPAN[0]
    retimed = AUDIT / 'leg-same-tool-retimed.mkv'
    retimed.unlink(missing_ok=True)
    proc = subprocess.Popen([FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1280x720', '-r', str(FPS),
                             '-i', 'pipe:0', '-c:v', 'ffv1', '-level', '3', str(retimed)], stdin=subprocess.PIPE)
    for im in sequence:
        proc.stdin.write(im.tobytes())
    proc.stdin.close()
    assert proc.wait() == 0
    assert decoded_frames(retimed)[0] == len(sequence)

    # 4. One assembly pass: baseline head, retimed board, baseline tail; audio packet-copied.
    graph = [f'[0:v]trim=start_frame=0:end_frame={SPAN[0]},setpts=N/({FPS}*TB),setsar=1[a]',
             f'[1:v]setpts=N/({FPS}*TB),setsar=1,format=yuv420p[b]',
             f'[0:v]trim=start_frame={SPAN[1]}:end_frame={TOTAL},setpts=N/({FPS}*TB),setsar=1[c]',
             f'[a][b][c]concat=n=3:v=1:a=0,setpts=N/({FPS}*TB),format=yuv420p[v]']
    subprocess.run([FF, '-v', 'error', '-i', str(BASELINE), '-i', str(retimed),
                    '-filter_complex', ';'.join(graph), '-map', '[v]', '-map', '0:a',
                    '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '3.1', '-crf', '16', '-preset', 'fast',
                    '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], check=True)

    # 5. Verify the encoded candidate, not the plan.
    n, fps = decoded_frames(DEST)
    audio_identical = payload_hash(BASELINE) == payload_hash(DEST)
    assert (n, fps) == (TOTAL, float(FPS)), (n, fps)
    assert audio_identical
    assert sha(BASELINE) == BASELINE_SHA and sha(ASSET) == asset_sha

    manifest = {'candidate': str(DEST), 'candidate_sha256': sha(DEST), 'baseline': str(BASELINE), 'baseline_sha256': BASELINE_SHA,
                'asset': str(ASSET), 'asset_sha256': asset_sha, 'asset_size': [1600, 1150],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy}, 'shipped_leg_spec': str(SHIPPED_LEG),
                'beats': spec['beats'], 'walk_frames': walk, 'pause_hold': {'after_leg_frame': WALK_CUT - 1, 'frames': HOLD},
                'replaced_output_frames': list(SPAN), 'replaced_seconds': [SPAN[0] / FPS, SPAN[1] / FPS],
                'treatment': 'photo camera walk: establish, zoom to the two phone photos, hold, pull back, hold (as shipped); no rings',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    beat_boundaries, at = [], SPAN[0]
    for b in spec['beats']:
        beat_boundaries += ['--boundary', f"{at if at < SPAN[0] + WALK_CUT else at + HOLD}:beat-{b['label'].replace(' ', '-')}"]
        at += int(b['frames'])
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            '--boundary', f'{SPAN[0]}:source-to-board', '--boundary', f'{SPAN[1]}:board-to-source',
                            *beat_boundaries[2:], '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
