#!/usr/bin/env python3
"""Verify the encoded roadmap repair and preserve inspectable QA evidence."""
import json
import subprocess
import cv2
import numpy as np
from build_navigate_opener_v10 import ROOT, OUT, SOURCE, DEST, FFMPEG, sha


def audio_hash(path):
    return subprocess.check_output([
        FFMPEG, '-v', 'error', '-i', str(path), '-map', '0:a:0',
        '-c:a', 'copy', '-f', 'hash', '-hash', 'sha256', '-'], text=True).strip()


def main():
    captures = [cv2.VideoCapture(str(p)) for p in (SOURCE, DEST)]
    assert all(c.isOpened() for c in captures)
    assert all(c.get(cv2.CAP_PROP_FPS) == 30 for c in captures)
    states = [3092, 3099, 3246, 3247, 3472, 3473, 3554, 3555,
              3695, 3696, 3724, 3725, 4038, 4039, 4116, 4117, 4369]
    tiles, diffs, count = [], [], 0
    while True:
        a_ok, a = captures[0].read()
        b_ok, b = captures[1].read()
        assert a_ok == b_ok, f'Decode length mismatch at {count}'
        if not a_ok:
            break
        assert a.shape == b.shape == (720, 1280, 3)
        if not (3092 <= count < 3555 or 3696 <= count < 4117):
            diffs.append(float(np.abs(a.astype(np.int16) - b.astype(np.int16)).mean()))
        if count in states:
            cv2.imwrite(str(OUT / f'after-{count}.jpg'), b, [cv2.IMWRITE_JPEG_QUALITY, 95])
            tile = cv2.resize(b, (640, 360))
            cv2.putText(tile, f'frame {count}', (8, 24), 0, .65, (0, 0, 200), 2)
            tiles.append(tile)
        count += 1
    for c in captures:
        c.release()
    assert count == 4370
    assert max(diffs) < 3, f'Unexpected change outside board spans: {max(diffs)}'
    hashes = [audio_hash(p) for p in (SOURCE, DEST)]
    assert hashes[0] == hashes[1], 'Audio stream changed'
    while len(tiles) % 3:
        tiles.append(np.full_like(tiles[0], 255))
    cv2.imwrite(str(OUT / 'after-contact.jpg'), cv2.vconcat([
        cv2.hconcat(tiles[i:i + 3]) for i in range(0, len(tiles), 3)]))
    result = dict(decoded_frames=count, fps=30, duration_seconds=count / 30,
                  identical_audio_stream=True, audio_sha256=hashes[0],
                  unchanged_span_frames=len(diffs),
                  unchanged_span_mean_pixel_error=float(np.mean(diffs)),
                  unchanged_span_max_frame_pixel_error=max(diffs),
                  candidate_sha256=sha(DEST))
    (OUT / 'qa.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    subprocess.run([
        str(ROOT / '.video-venv/bin/python'), str(ROOT / 'scripts/video/transition_guard.py'), str(DEST),
        '--boundary', '3092:roadmap-in', '--boundary', '3555:original-cutaway-in',
        '--boundary', '3696:roadmap-return', '--boundary', '4117:original-close-in',
        '--outdir', str(OUT / 'transitions')], check=True)


if __name__ == '__main__':
    main()
