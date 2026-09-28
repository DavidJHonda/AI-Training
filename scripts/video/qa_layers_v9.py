#!/usr/bin/env python3
"""Check preserved audio, frame count, retained pictures, and new illustration cuts."""
import hashlib
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

from build_layers_v9 import BASE, DEST, OUT, SPANS
from editspec_build import Reader, sha


def audio_hash(path, decoded=False):
    args = ['-acodec', 'pcm_s16le', '-f', 's16le'] if decoded else ['-c:a', 'copy', '-f', 'adts']
    result = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', str(path),
        '-map', '0:a:0', *args, 'pipe:1'], capture_output=True, check=True)
    return hashlib.sha256(result.stdout).hexdigest()


def main():
    manifest = json.loads((OUT / 'edit-manifest.json').read_text())
    assert sha(DEST) == manifest['render_sha256']
    audio = dict(aac=audio_hash(BASE), decoded_pcm=audio_hash(BASE, True))
    assert audio['aac'] == audio_hash(DEST)
    assert audio['decoded_pcm'] == audio_hash(DEST, True)
    previews = {int(p.name.split('-')[0]): p for p in (OUT / 'preview').glob('*.png')}
    (OUT / 'encoded').mkdir(exist_ok=True)
    cap = cv2.VideoCapture(str(DEST))
    base = Reader(BASE)
    assert cap.get(cv2.CAP_PROP_FPS) == 30
    n, retained, states = 0, [], []
    while True:
        ok, im = cap.read()
        if not ok:
            break
        assert im.shape == (720, 1280, 3)
        changed = any(s['start'] <= n < s['end'] for s in SPANS)
        if not changed and (n % 15 == 0 or n in previews):
            ref = base.at(n)
            mad = float(np.abs(im.astype(float) - ref).mean())
            retained.append(dict(frame=n, mad=mad))
            assert mad < 5, (n, mad)
        if n in previews:
            ref = cv2.imread(str(previews[n]))
            mad = float(np.abs(im.astype(float) - ref).mean())
            states.append(dict(frame=n, mad=mad))
            assert mad < 5, (n, mad)
            cv2.imwrite(str(OUT / 'encoded' / previews[n].name), im)
        n += 1
    cap.release()
    base.c.release()
    assert n == manifest['frames'] == 6101
    assert all(sha(Path(p)) == h for p, h in manifest['protected'].items())
    report = dict(decoded_frames=n, fps=30, seconds=n / 30,
        audio_hashes=audio, aac_exact=True, decoded_audio_exact=True,
        retained_frame_comparisons=retained, rendered_state_comparisons=states,
        max_retained_mad=max(x['mad'] for x in retained),
        max_state_mad=max(x['mad'] for x in states), protected_sources_unchanged=True)
    (OUT / 'qa.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if not isinstance(v, list)}, indent=2))
    # Context contact sheet: every changed cut, first/middle/last illustration frame.
    thumbs = []
    for f in sorted(previews):
        if f in [0, 6100]:
            continue
        im = cv2.imread(str(OUT / 'encoded' / previews[f].name))
        thumb = cv2.resize(im, (640, 360))
        cv2.rectangle(thumb, (0, 0), (180, 26), (255, 255, 255), -1)
        cv2.putText(thumb, f'{f} / {f / 30:.3f}s', (8, 19), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 1)
        thumbs.append(thumb)
    for index in range(0, len(thumbs), 4):
        group = thumbs[index:index + 4]
        while len(group) < 4:
            group.append(np.full_like(group[0], 255))
        sheet = np.vstack([np.hstack(group[:2]), np.hstack(group[2:])])
        cv2.imwrite(str(OUT / f'contact-{index // 4}.jpg'), sheet)


if __name__ == '__main__':
    main()
