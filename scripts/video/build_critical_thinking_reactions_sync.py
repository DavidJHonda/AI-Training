#!/usr/bin/env python3
"""Critical Thinking: swap the refreshed Same Claim. Different Thinking. illustration into the shipped video.

Eleventh of the 2026-09-21 illustration syncs. The refresh replaced the board in place: same board,
same 1600x1077 dimensions, same title, THE CLAIM strip, two comparison cards and takeaway banner,
new cast in the photographs - and the two pills now read FIRST REACTION and SECOND REACTION where
they read LUKE'S REACTION and NATE'S REACTION, matching the lesson copy change made the same day.
The narration never speaks either name over this board ("The face value reaction was immediate…",
"a critical thinking reaction takes a different path"), so the new wording does not contradict what
is heard. The cards did not move, so the shipped leg spec is reused verbatim - same dives, same four
rings - and only the artwork changes.

The board runs from output frame 1710 (0:57.00) to 2315 (1:17.17), 605 frames. Nothing else changes:
the rest of the picture comes from the frozen baseline, the approved audio is packet-copied, and the
output keeps 5935 frames at 30 fps.

The live audio matters here: the shipped v12 is v11's video with a deliberately re-encoded AAC track
(256 kbps, PNS and TNS disabled to kill a tonal artifact at 2:54). Packet-copying keeps that exact
track; it must never be re-encoded.

Stroke: the artwork-scaled rule (owner, 2026-09-21, and his instruction today that a synced video
takes the current highlighting) gives 5 px at the dives - the shipped weight, so the two card rings
are unchanged - and 4 px at full view, where THE CLAIM ring and the banner ring live. The shipped
weights were confirmed first: the OLD JPG rendered through the shipped spec with the stroke forced
to 5 reproduces the live leg at 3.06 mean per-pixel difference, which also fixes the span.

Usage:
  .video-venv/bin/python scripts/video/build_critical_thinking_reactions_sync.py
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
TOTAL = 5935
SPAN = (1710, 2315)          # half-open output frames: the Same Claim leg, 605 frames
ASSET = ROOT / 'course-assets/critical-thinking/critical-thinking-two-reactions.jpg'
ASSET_SHA = 'a85e157775995677'      # prefix guard: the refresh this build was reviewed against
SHIPPED = ROOT / 'video-audit/critical-thinking-repair-2026-09-17-v11/edit-manifest.json'
AUDIT = ROOT / 'video-audit/critical-thinking-illustration-sync-2026-09-21'
BASELINE = AUDIT / 'baseline-live-2026-09-17.mp4'
BASELINE_SHA = 'fe9fed9a912bfe6c60a63c39d2b457707308404873fc2640a9608c43918b426d'
DEST = ROOT / 'Prompts/critical-thinking-v13.mp4'


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
    assert BASELINE.exists(), f'{BASELINE} missing: cp course-assets/critical-thinking/critical-thinking.mp4 {BASELINE}'
    assert sha(BASELINE) == BASELINE_SHA, 'baseline snapshot changed'
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    asset_sha = sha(ASSET)
    assert asset_sha.startswith(ASSET_SHA), f'the illustration changed again ({asset_sha[:16]}); re-review before building'
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (1077, 1600), board.shape
    shipped = json.loads(SHIPPED.read_text())['boards']['reactions']

    # 1. Canvas and camera, reproduced by the shipped build's own code path.
    canvas_path, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT), ASSET, 'reactions')
    assert (cw, ch, ox, oy) == (2068, 1164, 234, 43), (cw, ch, ox, oy)
    assert [ox, oy] == shipped['canvas_offset']

    # 2. The shipped camera walk and rings, verbatim, on the new canvas.
    spec = {'image': str(canvas_path), 'fps': FPS, 'out_w': 1280, 'out_h': 720, 'upscale': 3,
            'beats': shipped['beats'], 'rings': shipped['rings']}
    frames = sum(int(b['frames']) for b in spec['beats'])
    assert frames == SPAN[1] - SPAN[0] == shipped['src_out'] - shipped['src_in'], (frames, SPAN)
    assert spec['beats'][0]['from'] == [cw / 2, ch / 2, float(cw)], spec['beats'][0]
    assert len(spec['rings']) == 4
    spec_path = AUDIT / 'leg-reactions.json'
    spec_path.write_text(json.dumps(spec, indent=1) + '\n')
    leg = AUDIT / 'leg-reactions.mkv'
    leg.unlink(missing_ok=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts/video/ken_burns_path.py'), str(spec_path), str(leg)], check=True)
    assert decoded_frames(leg)[0] == frames

    # 3. One assembly pass: baseline head, new leg, baseline tail; audio packet-copied (v12's AAC track).
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
                'asset': str(ASSET), 'asset_sha256': asset_sha, 'asset_size': [1600, 1077],
                'canvas': {'w': cw, 'h': ch, 'ox': ox, 'oy': oy}, 'shipped_manifest': str(SHIPPED),
                'beats': spec['beats'], 'rings': spec['rings'],
                'ring_stroke_px': 'artwork-scaled rule (5 px at the dives, as shipped; 4 px at full view)',
                'replaced_output_frames': list(SPAN), 'replaced_seconds': [SPAN[0] / FPS, SPAN[1] / FPS],
                'treatment': 'dense: establish, THE CLAIM ring, dive to Face Value, across to Critical Thinking, pull back, banner (as shipped)',
                'decoded_frames': n, 'fps': fps, 'audio_packets_identical': audio_identical,
                'audio_payload_sha256': payload_hash(DEST)}
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    declared = {SPAN[0]: 'source-to-board', SPAN[1]: 'board-to-source'}
    at = SPAN[0]
    for b in spec['beats']:
        declared.setdefault(at, f"beat-{b['label'].replace(' ', '-')}")
        at += int(b['frames'])
    for r in spec['rings']:
        declared.setdefault(SPAN[0] + int(r['start']), f"ring-{int(r['rect'][0])}-{int(r['rect'][1])}")
    boundaries = [x for f in sorted(declared) for x in ('--boundary', f'{f}:{declared[f]}')]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
                            *boundaries, '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', n, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)


if __name__ == '__main__':
    main()
