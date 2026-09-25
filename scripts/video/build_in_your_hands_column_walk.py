#!/usr/bin/env python3
"""In Your Hands: walk the camera column by column over the What's in Your Hands? board.

David, 2026-09-25: "The board that appears at :48. We say 'This entire column represents...' We should
zoom in to the left column and highlight the full column in the white section of the board. We can stay
in the zoomed in view as the points are highlighted. At 1:06, we talk about the right column. Pan to the
right column and highlight the column as spoken. Then, stay zoomed-in until it moves to banner. Then zoom
out to see the full board."

The live leg (What You Can Control v3, 2026-09-16) held this board at full view (compact) for all 81.5 s.
This build makes it dense (Edit Spec rule 4): full view through the intro, dive to the Out of Your Hands
column at "This entire column" (0:46.82) with a whole-column ring over the white section, the five
approved row rings at their approved onsets, pan to the In of Your Hands column at "Now look at the right
side" (1:06.46) with a whole-column ring, its five row rings, then pull back to the full view at the
banner (1:44.83) for the banner ring.

Framing: David asked for the white section, so the dive window fits the column's white section (heading
and rows, y 552-1172), not the illustration above it. One uniform dive window for both columns. Row
rects, colours, radii and onsets are v3's verbatim, remapped from the v3 source-leg timeline to this
file's output timeline. House dive constants from editspec_build (24-frame transit starting at the onset,
30-frame pull-back starting at the banner onset, 40 px margin).

Replaces output frames 1059-3504 of the live file (the whole board span); audio packet-copied; one
re-encode.

Usage:
  .video-venv/bin/python scripts/video/build_in_your_hands_column_walk.py
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import types
from pathlib import Path

import cv2
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Build, TRANSIT, PULLBACK  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
TOTAL = 5508
SPAN = (1059, 3504)          # half-open output frames: the What's in Your Hands? leg, 2445 frames
ASSET = ROOT / 'course-assets/in-your-hands/in-your-hands-in-or-out.jpg'
ASSET_SHA = 'd012614234b5d55d7e1ca54a92eeca8db3308f509b6290e06bd182e289688054'
LIVE = ROOT / 'course-assets/in-your-hands/in-your-hands.mp4'
LIVE_SHA = 'ab5342bda5f6b0a6a82b25c828b4b179f8b5b4323d6717a1bbfc8531f4dc5801'
SHIPPED_LEG = ROOT / 'video-audit/what-you-can-control-repair-2026-09-16/leg-1-hands.json'   # v3, live
AUDIT = ROOT / 'video-audit/in-your-hands-column-walk-2026-09-25'
BASELINE = AUDIT / 'baseline-live-20260918rename1.mp4'
DEST = ROOT / 'Prompts/in-your-hands-v4.mp4'

# Spoken onsets in output seconds (faster-whisper medium.en word timestamps on the live file).
COLUMN_LEFT_AT = 46.82       # "This entire column represents external events."
COLUMN_RIGHT_AT = 66.46      # "Now look at the right side."

# White section of the shared white box, board px (measured: white from y 552, box bottom 1172,
# box x 40-1560, columns split at 800).
WHITE_TOP, WHITE_BOTTOM, BOX_LEFT, BOX_RIGHT, SPLIT = 552, 1172, 40, 1560, 800


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


def v3_leg_to_output(f: int) -> int:
    """v3's leg frame (source frame 1239 + f) -> this file's output frame, through v3's cut list."""
    src = 1239 + f
    if src <= 2139:
        return src - 150          # 30-frame pause after source 1240
    assert src >= 2472, src       # source 2139-2472 was cut
    return src - 483


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    if not BASELINE.exists():
        assert sha(LIVE) == LIVE_SHA, 'live video changed since the 2026-09-25 review'
        shutil.copy2(LIVE, BASELINE)
    assert sha(BASELINE) == LIVE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    assert sha(ASSET) == ASSET_SHA, 'board asset changed; recheck rects'

    # 1. Canvas reproduced exactly as v3 (pre-2026-09-14 framing, board centred, no tall margin).
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT, tall_margin=False), ASSET, '1-hands')
    assert (cw, ch, ox, oy) == (2382, 1340, 391, 0), (cw, ch, ox, oy)

    # 2. Rings: v3's rows verbatim, remapped to the output timeline, plus the two whole-column rings.
    shipped = json.loads(SHIPPED_LEG.read_text())
    old = shipped['rings']
    assert len(old) == 11 and old[-1]['color'] == '#6e51ff'
    n = SPAN[1] - SPAN[0]
    leg = lambda out_frame: out_frame - SPAN[0]   # noqa: E731
    starts = [leg(v3_leg_to_output(r['start'])) for r in old]
    left_col_at = leg(round(COLUMN_LEFT_AT * FPS))
    right_col_at = leg(round(COLUMN_RIGHT_AT * FPS))
    assert left_col_at < starts[0] and starts[4] < right_col_at < starts[5], (left_col_at, right_col_at, starts)

    h = WHITE_BOTTOM - WHITE_TOP
    left_rect = [BOX_LEFT + ox, WHITE_TOP + oy, SPLIT - BOX_LEFT, h]
    right_rect = [SPLIT + ox, WHITE_TOP + oy, BOX_RIGHT - SPLIT, h]
    out_rows, in_rows, banner = old[:5], old[5:10], old[10]
    rings = [dict(start=left_col_at, end=starts[0], rect=left_rect, color='#1652f0', pad=0, radius=18)]
    for i, r in enumerate(out_rows):
        end = starts[i + 1] if i < 4 else right_col_at
        rings.append({**r, 'start': starts[i], 'end': end})
    rings.append(dict(start=right_col_at, end=starts[5], rect=right_rect, color='#0f7a4a', pad=0, radius=18))
    for i, r in enumerate(in_rows):
        rings.append({**r, 'start': starts[5 + i], 'end': starts[6 + i]})
    rings.append({**banner, 'start': starts[10], 'end': n})
    assert all(r['end'] > r['start'] for r in rings)
    assert all(a['end'] == b['start'] for a, b in zip(rings, rings[1:])), 'one ring at a time'

    # 3. Camera: full view, dive to the left column, pan to the right column, pull back at the banner.
    full = [cw / 2, ch / 2, float(cw)]
    dive_w = Build.fit_w(SPLIT - BOX_LEFT, h)          # both columns are the same size: one uniform window
    cy = WHITE_TOP + oy + h / 2
    left_cam = [left_rect[0] + left_rect[2] / 2, cy, dive_w]
    right_cam = [right_rect[0] + right_rect[2] / 2, cy, dive_w]
    banner_at = starts[10]
    beats = [dict(label='establish', frames=left_col_at, **{'from': full}, to=full),
             dict(label='to-left-column', frames=TRANSIT, to=left_cam),
             dict(label='hold-left-column', frames=right_col_at - left_col_at - TRANSIT, to=left_cam),
             dict(label='to-right-column', frames=TRANSIT, to=right_cam),
             dict(label='hold-right-column', frames=banner_at - right_col_at - TRANSIT, to=right_cam),
             dict(label='pull-back', frames=PULLBACK, to=full),
             dict(label='full-hold', frames=n - banner_at - PULLBACK, to=full)]
    assert all(b['frames'] > 0 for b in beats) and sum(b['frames'] for b in beats) == n
    spec = {**shipped, 'image': str(canvas_path), 'beats': beats, 'rings': rings}
    spec_path = AUDIT / 'leg-1-hands.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg_path = AUDIT / 'leg-1-hands.mkv'
    leg_path.unlink(missing_ok=True)
    (AUDIT / 'preview').mkdir(exist_ok=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'), str(spec_path), '--preview', str(AUDIT / 'preview')], check=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'), str(spec_path), str(leg_path)], check=True)
    assert decoded_frames(leg_path)[0] == n

    # 4. One assembly pass: baseline head, new leg, baseline tail; audio packet-copied.
    graph = [f'[0:v]trim=start_frame=0:end_frame={SPAN[0]},setpts=N/({FPS}*TB),setsar=1[a]',
             f'[1:v]setpts=N/({FPS}*TB),setsar=1,format=yuv420p[b]',
             f'[0:v]trim=start_frame={SPAN[1]}:end_frame={TOTAL},setpts=N/({FPS}*TB),setsar=1[c]',
             f'[a][b][c]concat=n=3:v=1:a=0,setpts=N/({FPS}*TB),format=yuv420p[v]']
    subprocess.run([FF, '-v', 'error', '-i', str(BASELINE), '-i', str(leg_path),
                    '-filter_complex', ';'.join(graph), '-map', '[v]', '-map', '0:a',
                    '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '3.1', '-crf', '16', '-preset', 'fast',
                    '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy', '-movflags', '+faststart', str(DEST)], check=True)

    # 5. Verify the encoded candidate, not the plan.
    frames, fps = decoded_frames(DEST)
    audio_identical = payload_hash(BASELINE) == payload_hash(DEST)
    assert (frames, fps) == (TOTAL, float(FPS)), (frames, fps)
    assert audio_identical
    assert sha(BASELINE) == LIVE_SHA and sha(ASSET) == ASSET_SHA

    manifest = {'candidate': str(DEST), 'candidate_sha256': sha(DEST), 'baseline': str(BASELINE), 'baseline_sha256': LIVE_SHA,
                'asset': str(ASSET), 'asset_sha256': ASSET_SHA, 'asset_size': [1600, 1340],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy, 'camera': full},
                'v3_leg_spec': str(SHIPPED_LEG), 'rings': rings, 'beats': beats, 'dive_w': dive_w,
                'column_onsets_s': {'left': COLUMN_LEFT_AT, 'right': COLUMN_RIGHT_AT, 'banner': (SPAN[0] + banner_at) / FPS},
                'replaced_output_frames': list(SPAN), 'replaced_seconds': [SPAN[0] / FPS, SPAN[1] / FPS],
                'density': 'dense',
                'treatment': 'full view intro; dive to the left column white section at "This entire column" with a whole-column ring, '
                             'v3 row rings; pan to the right column at "Now look at the right side" with a whole-column ring, '
                             'v3 row rings; pull back to full view at the banner onset with the banner ring',
                'decoded_frames': frames, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    ring_boundaries = []
    for r in rings:
        ring_boundaries += ['--boundary', f"{SPAN[0] + int(r['start'])}:ring-on-{int(r['rect'][0])}-{int(r['rect'][1])}"]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            '--boundary', f'{SPAN[0]}:source-to-board', '--boundary', f'{SPAN[1]}:board-to-board',
                            *ring_boundaries, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', frames, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
