#!/usr/bin/env python3
"""People Skills: swap the refreshed Four Ways to Practice illustration into the shipped video.

Nineteenth of the 2026-09-21 illustration syncs. The cast refresh replaced the board in place: same
board, same 1351x1164 dimensions, same title and four cards, new cast in the photographs. The cards
did not move, so the shipped leg spec is reused verbatim - establish, dive to each card in turn,
pull back, hold, with the same four rings - and only the artwork changes.

The board runs from output frame 3033 (1:41.10) to 4536 (2:31.20), 1503 frames.

Two details this build has to get right:

* The canvas predates the 4% tall-board stage margin (added 2026-09-14), so `tall_margin=False`
  reproduces the 09-12 framing: a 2070x1166 canvas at offset (359, 1), matching that manifest.
* Stroke. The artwork-scaled rule (owner, 2026-09-21, and his instruction that a synced video takes
  the current highlighting) gives 4 px at this board's full view and 8 px at its dives, where the
  09-12 build used a constant 5 px. The dives here are tight - about 1014 board px across the 1280
  frame - so the rule deliberately thickens the ring to keep its weight constant against the card's
  own text. This is the largest stroke change of the day's syncs.

Nothing else changes: the rest of the picture comes from the frozen baseline, the approved audio is
packet-copied, and the output keeps 5199 frames at 30 fps.

Usage:
  .video-venv/bin/python scripts/video/build_people_skills_four_ways_sync.py
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
TOTAL = 5199
SPAN = (3033, 4536)          # half-open output frames: the Four Ways leg, 1503 frames
ASSET = ROOT / 'course-assets/people-skills/people-skills-four-ways.jpg'
SHIPPED = ROOT / 'video-audit/people-skills-repair-2026-09-12/edit-manifest.json'
AUDIT = ROOT / 'video-audit/people-skills-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-12.mp4'
BASELINE_SHA = '138d2453553a3014d7698ce1d212dd120fef66ff4716262bd8f4912ff73bde16'
DEST = ROOT / 'Prompts/people-skills-v2.mp4'


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/people-skills/people-skills.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (1164, 1351), board.shape
    shipped_all = json.loads(SHIPPED.read_text())
    assert shipped_all['render_sha256'] == BASELINE_SHA, 'the 09-12 repair is not the live file'
    shipped = shipped_all['boards']['2-four-ways']

    # 1. Canvas and camera, reproduced by the shipped build's own code path (pre-09-14 framing).
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT, tall_margin=False), ASSET, '2-four-ways')
    assert (cw, ch, ox, oy) == (2070, 1166, 359, 1), (cw, ch, ox, oy)
    assert [ox, oy] == shipped['canvas_offset']

    # 2. The shipped camera walk and rings, verbatim, on the new canvas.
    spec = {'image': str(canvas_path), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
            'beats': shipped['beats'], 'rings': shipped['rings']}
    frames = sum(int(b['frames']) for b in spec['beats'])
    assert frames == SPAN[1] - SPAN[0] == shipped['src_out'] - shipped['src_in'], (frames, SPAN)
    assert spec['beats'][0]['from'] == [cw / 2, ch / 2, float(cw)], spec['beats'][0]
    assert len(spec['rings']) == 4
    spec_path = AUDIT / 'leg-2-four-ways.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / 'leg-2-four-ways.mkv'
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
                'asset': str(ASSET), 'asset_sha256': asset_sha, 'asset_size': [1351, 1164],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy, 'tall_margin': False},
                'shipped_manifest': str(SHIPPED), 'beats': spec['beats'], 'rings': spec['rings'],
                'ring_stroke_px': 'artwork-scaled rule (4 px at full view, 8 px at the dives; the 09-12 build used 5 px throughout)',
                'replaced_output_frames': list(SPAN), 'replaced_seconds': [SPAN[0] / FPS, SPAN[1] / FPS],
                'treatment': 'dense: establish, dive to each of the four cards in turn, pull back, hold (as shipped)',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    declared = {SPAN[0]: 'source-to-board', SPAN[1]: 'board-to-source'}
    at = SPAN[0]
    for b in spec['beats']:
        declared.setdefault(at, f"beat-{b['label'].replace(' ', '-').replace(chr(39), '')}")
        at += int(b['frames'])
    for r in spec['rings']:
        declared.setdefault(SPAN[0] + int(r['start']), f"ring-{int(r['rect'][0])}-{int(r['rect'][1])}")
    boundaries = [x for f in sorted(declared) for x in ('--boundary', f'{f}:{declared[f]}')]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            *boundaries, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
