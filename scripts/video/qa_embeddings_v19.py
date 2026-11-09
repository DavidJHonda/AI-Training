#!/usr/bin/env python3
"""Verify the banner border repair and preserve v18's audio and timing."""
import json
import subprocess

import cv2
import numpy as np

import build_embeddings_v19 as v


def main():
    manifest = json.loads((v.OUT / 'edit-manifest.json').read_text())
    assert v.b.base.sha(v.DEST) == manifest['output_sha256']
    source = cv2.VideoCapture(str(v.AUDIO))
    candidate = cv2.VideoCapture(str(v.DEST))
    assert source.get(cv2.CAP_PROP_FRAME_COUNT) == candidate.get(cv2.CAP_PROP_FRAME_COUNT) == v.b.TOTAL
    assert candidate.get(cv2.CAP_PROP_FPS) == 30
    assert (candidate.get(3), candidate.get(4)) == (1280, 720)
    renderer = v.Render()
    expected, _ = renderer.frame(6300, None)
    max_retained = max_banner = 0
    changed = 0
    for frame in range(v.b.TOTAL):
        ok, before = source.read()
        ok2, after = candidate.read()
        assert ok and ok2, frame
        if v.START <= frame < v.END:
            error = float(cv2.absdiff(after, expected).mean())
            assert error < 5, (frame, error)
            max_banner = max(max_banner, error)
            # Outside the banner area, even the repaired frames remain the same.
            error_outside = float(cv2.absdiff(after[:610], before[:610]).mean())
            assert error_outside < .5, (frame, error_outside)
            changed += 1
            # Measure the straight sides in the actual encoded picture.
            blue, green, red = cv2.split(after)
            purple = (blue > 170) & (red > 65) & (red < 165) & (green < 135)
            for y, target in [(618, 'top'), (677, 'bottom')]:
                assert purple[y - 2:y + 3, 160:1120].mean() > .7, (frame, target)
            for x, target in [(132, 'left'), (1148, 'right')]:
                assert purple[635:660, x - 2:x + 3].mean() > .7, (frame, target)
        else:
            error = float(cv2.absdiff(after, before).mean())
            assert error < .5, (frame, error)
            max_retained = max(max_retained, error)
        if frame == 5010:
            cv2.imwrite(str(v.OUT / 'encoded-167s.png'), after)
    assert not candidate.read()[0]
    source.release()
    candidate.release()
    assert v.audio_hash(v.DEST) == v.audio_hash(v.AUDIO)
    guard_command = [str(v.ROOT / '.video-venv/bin/python'), str(v.ROOT / 'scripts/video/transition_guard.py'),
                     str(v.DEST), '--outdir', str(v.OUT / 'guard'),
                     '--boundary', f'{v.START}:banner-highlight', '--boundary', f'{v.END}:word-pieces']
    subprocess.run(guard_command, check=True)
    guard = json.loads((v.OUT / 'guard/transition-guard.json').read_text())
    assert guard['pass']
    report = dict(frames=v.b.TOTAL, fps=30, duration=v.b.TOTAL / 30, changed_frames=changed,
                  changed_seconds=[v.START / 30, v.END / 30],
                  max_retained_frame_mae=max_retained, max_repaired_frame_mae=max_banner,
                  encoded_border_coordinates_pass=True, copied_audio_identical=True,
                  transition_guard_pass=True, output_sha256=v.b.base.sha(v.DEST))
    (v.OUT / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
