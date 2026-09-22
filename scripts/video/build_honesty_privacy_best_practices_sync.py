#!/usr/bin/env python3
"""Honesty & Privacy: swap the refreshed Best Practices illustration into the shipped video.

Eighteenth of the 2026-09-21 illustration syncs. The cast refresh replaced the board in place: same
board, same 1706x922 dimensions, same title, three numbered cards and takeaway banner, new cast in
the photographs. The cards did not move, so the shipped leg spec is reused verbatim - still full
view, no camera move, four rings in the shipped order - and only the artwork changes.

The board is on screen from output frame 1959 (1:05.30) to 2880 (1:36.00), 921 frames, in the three
pieces the 09-12 build created: a single arrival frame, a 30-frame pause that freezes it, then the
leg's remaining 890 frames. This build renders the 891-frame leg and re-times it the same way, so
the freeze lands on the frame it always did.

Stroke: no change here. The artwork-scaled rule (owner, 2026-09-21) gives 5 px at this camera -
1706 board px across a 1280 px frame is close to the rule's reference framing - which is exactly
what the shipped video carries.

Nothing else changes: the rest of the picture comes from the frozen baseline, the approved audio is
packet-copied, and the output keeps 7200 frames at 30 fps.

Usage:
  .video-venv/bin/python scripts/video/build_honesty_privacy_best_practices_sync.py
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
TOTAL = 7200
SPAN = (1959, 2880)          # half-open output frames the board occupies: arrival + freeze + leg tail
FREEZE = 31                  # frames showing leg frame 0 (its arrival frame plus the 30-frame pause)
ASSET = ROOT / 'course-assets/honesty-and-privacy/honesty-and-privacy-best-practices.jpg'
SHIPPED = ROOT / 'video-audit/honesty-and-privacy-repair-2026-09-12/edit-manifest.json'
AUDIT = ROOT / 'video-audit/honesty-and-privacy-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-12.mp4'
BASELINE_SHA = '99604cf032d32166fc07ba1ee0cf2ccdea27a9fbffb28723849a04c123954018'
DEST = ROOT / 'Prompts/honesty-and-privacy-v2.mp4'


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/honesty-and-privacy/honesty-and-privacy.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (922, 1706), board.shape
    shipped_all = json.loads(SHIPPED.read_text())
    assert shipped_all['render_sha256'] == BASELINE_SHA, 'the 09-12 repair is not the live file'
    shipped = shipped_all['boards']['2-best-practices']

    # 1. Canvas and camera, reproduced by the shipped build's own code path.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT), ASSET, '2-best-practices')
    assert (cw, ch, ox, oy) == (1706, 960, 0, 19), (cw, ch, ox, oy)
    assert [ox, oy] == shipped['canvas_offset']

    # 2. The shipped leg spec, verbatim, on the new canvas.
    spec = {'image': str(canvas_path), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
            'beats': shipped['beats'], 'rings': shipped['rings']}
    frames = sum(int(b['frames']) for b in spec['beats'])
    assert frames == shipped['src_out'] - shipped['src_in'] == 891, frames
    assert frames + FREEZE - 1 == SPAN[1] - SPAN[0], (frames, SPAN)
    assert spec['beats'][0]['from'] == spec['beats'][0]['to'] == [cw / 2, ch / 2, float(cw)], spec['beats'][0]
    assert len(spec['rings']) == 4
    spec_path = AUDIT / 'leg-2-best-practices.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / 'leg-2-best-practices.mkv'
    leg.unlink(missing_ok=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'), str(spec_path), str(leg)], check=True)
    assert decoded_frames(leg)[0] == frames

    # 3. Re-time the way the 09-12 build did: the arrival frame, its 30-frame pause freeze, then the rest.
    cap = cv2.VideoCapture(str(leg))
    rendered = []
    while True:
        ok, im = cap.read()
        if not ok:
            break
        rendered.append(im)
    cap.release()
    assert len(rendered) == frames
    sequence = [rendered[0]] * FREEZE + rendered[1:]
    assert len(sequence) == SPAN[1] - SPAN[0]
    retimed = AUDIT / 'leg-2-best-practices-retimed.mkv'
    retimed.unlink(missing_ok=True)
    proc = subprocess.Popen([FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1280x720', '-r', str(FPS),
                             '-i', 'pipe:0', '-c:v', 'ffv1', '-level', '3', str(retimed)], stdin=subprocess.PIPE)
    for im in sequence:
        proc.stdin.write(im.tobytes())
    proc.stdin.close()
    assert proc.wait() == 0
    assert decoded_frames(retimed)[0] == len(sequence)

    # 4. One assembly pass: baseline head, re-timed board, baseline tail; audio packet-copied.
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
                'asset': str(ASSET), 'asset_sha256': asset_sha, 'asset_size': [1706, 922],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy}, 'shipped_manifest': str(SHIPPED),
                'beats': spec['beats'], 'rings': spec['rings'],
                'ring_stroke_px': 'artwork-scaled rule (5 px at this camera, unchanged from the shipped video)',
                'replaced_output_frames': list(SPAN), 'replaced_seconds': [SPAN[0] / FPS, SPAN[1] / FPS],
                'freeze': {'leg_frame': 0, 'frames': FREEZE},
                'treatment': 'compact, still, full view, three card rings and the banner (as shipped)',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    declared = {SPAN[0]: 'source-to-board', SPAN[1]: 'board-to-source'}
    for r in spec['rings']:
        declared.setdefault(SPAN[0] + FREEZE - 1 + int(r['start']), f"ring-{int(r['rect'][0])}-{int(r['rect'][1])}")
    boundaries = [x for f in sorted(declared) for x in ('--boundary', f'{f}:{declared[f]}')]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            *boundaries, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
