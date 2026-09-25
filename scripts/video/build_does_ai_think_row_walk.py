#!/usr/bin/env python3
"""Does AI Think?: walk the camera row by row over the When You Think / What AI Does board.

David, 2026-09-25: "The board that appears at 2:02. We need to zoom and pan between the lines as
spoken." The v7 leg held the board still at full view (compact) for all 72.5 s; this build turns it
dense (Edit Spec rule 4): full view through the intro, dive to the Meaning row at its spoken onset,
pan row to row as each comparison is spoken, and pull back to the full view for the takeaway banner.

Rings, colors, radii and onsets are v7's verbatim; only the camera changes. House dive constants
from editspec_build (24-frame transit starting at the onset, 30-frame pull-back, 40 px margin, one
uniform dive window sized to the row). The row spans the whole white card, so the dive window is
the board's full width: a straight zoom plus a vertical pan, never cropping inside a row.

Same frozen baseline and span as v7 (output frames 3669-5847); audio packet-copied; one re-encode.

Usage:
  .video-venv/bin/python scripts/video/build_does_ai_think_row_walk.py
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
from editspec_build import Build, TRANSIT, PULLBACK  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
TOTAL = 6600
SPAN = (3669, 5847)          # half-open output frames: the comparison board leg, 2178 frames
ASSET = ROOT / 'course-assets/does-ai-think/does-ai-think-side-by-side.jpg'
SYNC = ROOT / 'video-audit/does-ai-think-illustration-sync-2026-09-21'
SHIPPED_LEG = SYNC / 'leg-2-side-by-side.json'   # v7, live
AUDIT = ROOT / 'video-audit/does-ai-think-row-walk-2026-09-25'
BASELINE = SYNC / 'baseline-live-2026-09-16.mp4'
BASELINE_SHA = '7982de8a668b240991de042dc3373e37c0f1ec4e5dc2b1e63cb6f16f8d7d63c9'
DEST = ROOT / 'Prompts/does-ai-think-v8.mp4'
LIVE_V7_SHA = 'c6321f91964d5e308b970e942a4085dfc3a45d0acf5f156c2f8bfc3f907fcfbc'


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/does-ai-think/does-ai-think.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    assert sha(ROOT / 'course-assets/does-ai-think/does-ai-think.mp4') == LIVE_V7_SHA, 'live video is no longer v7'
    AUDIT.mkdir(parents=True, exist_ok=True)
    asset_sha = sha(ASSET)
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (1556, 1600), board.shape

    # 1. Canvas and camera, reproduced by the shipped build's own code path.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT, tall_margin=False), ASSET, '2-side-by-side')
    assert (cw, ch, ox, oy) == (2766, 1556, 583, 0), (cw, ch, ox, oy)

    # 2. v7's rings verbatim; a dense camera walk replaces the still full view.
    shipped = json.loads(SHIPPED_LEG.read_text())
    rings = shipped['rings']
    n = SPAN[1] - SPAN[0]
    full = [cw / 2, ch / 2, float(cw)]
    rows, banner = rings[:5], rings[5]
    assert banner['color'] == '#6e51ff' and all(r['color'] == '#0f7a4a' for r in rows)
    dive_w = max(Build.fit_w(*r['rect'][2:]) for r in rows)   # one uniform dive window for every row
    beats = [dict(label='establish', frames=rows[0]['start'], **{'from': full}, to=full)]
    for i, r in enumerate(rows):
        x, y, w, h = r['rect']
        cam = [x + w / 2, y + h / 2, dive_w]
        nxt = rows[i + 1]['start'] if i + 1 < len(rows) else banner['start']
        beats += [dict(label=f'to-row{i + 1}', frames=TRANSIT, to=cam), dict(label=f'hold-row{i + 1}', frames=nxt - r['start'] - TRANSIT, to=cam)]
    beats += [dict(label='pull-back', frames=PULLBACK, to=full), dict(label='full-hold', frames=n - banner['start'] - PULLBACK, to=full)]
    assert all(b['frames'] > 0 for b in beats)
    spec = {**shipped, 'image': str(canvas_path), 'beats': beats}
    frames = sum(int(b['frames']) for b in spec['beats'])
    assert frames == n, (frames, SPAN)
    assert spec['rings'] == shipped['rings']
    spec_path = AUDIT / 'leg-2-side-by-side.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / 'leg-2-side-by-side.mkv'
    leg.unlink(missing_ok=True)
    (AUDIT / 'preview').mkdir(exist_ok=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'), str(spec_path), '--preview', str(AUDIT / 'preview')], check=True)
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
                'asset': str(ASSET), 'asset_sha256': asset_sha, 'asset_size': [1600, 1556],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy, 'camera': spec['beats'][0]['from']},
                'v7_leg_spec': str(SHIPPED_LEG), 'live_v7_sha256': LIVE_V7_SHA, 'rings': spec['rings'], 'beats': beats, 'dive_w': dive_w,
                'ring_stroke_px': 'artwork-scaled rule (3 px full view, 5 px at the row dive)',
                'replaced_output_frames': list(SPAN), 'replaced_seconds': [SPAN[0] / FPS, SPAN[1] / FPS],
                'density': 'dense', 'treatment': 'full view intro, dive to each row at its spoken onset, pan row to row, pull back to full view for the banner (v7 rings verbatim)',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    ring_boundaries = []
    for r in spec['rings']:
        ring_boundaries += ['--boundary', f"{SPAN[0] + int(r['start'])}:ring-on-{int(r['rect'][1])}"]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            '--boundary', f'{SPAN[0]}:source-to-board', '--boundary', f'{SPAN[1]}:board-to-source',
                            *ring_boundaries, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
