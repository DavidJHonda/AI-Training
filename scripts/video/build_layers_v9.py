#!/usr/bin/env python3
"""Two approved illustration replacements; retain the approved v8 AAC stream."""
from pathlib import Path
import json
import subprocess

import cv2
import imageio_ffmpeg

import build_layers_v8 as b8
from editspec_build import Reader, sha
from gemini_mark import glyph_mask

ROOT = b8.ROOT
BASE = ROOT / 'Prompts/layers-v8.mp4'
DEST = ROOT / 'Prompts/layers-v9.mp4'
OUT = ROOT / 'video-audit/layers-build-2026-09-28-v9'
ASSETS = ROOT / 'scripts/video/assets/layers-visual-variety'
SPANS = [
    dict(start=2396, end=2546, asset='many-numbers-two-shown.png'),
    dict(start=4193, end=4416, asset='it-successive-updates.png'),
]


def illustration(im, fraction):
    # Restrained continuous push, retaining all lettering inside the frame.
    scale = 1 + .01 * fraction
    h, w = im.shape[:2]
    cw, ch = w / scale, h / scale
    x, y = (w - cw) / 2, (h - ch) / 2
    import numpy as np
    matrix = np.float32([[1280 / cw, 0, -x * 1280 / cw],
                         [0, 720 / ch, -y * 720 / ch]])
    return cv2.warpAffine(im, matrix, (1280, 720), flags=cv2.INTER_LANCZOS4)


def main():
    assert not DEST.exists(), 'Never overwrite a review candidate'
    prior = json.loads((b8.OUT / 'edit-manifest.json').read_text())
    assert sha(BASE) == prior['render_sha256']
    b8.OUT = OUT
    old, snapshot, specs, renderers, mapped, stack = b8.setup()
    # Site files can change between candidates. Protect their current state;
    # setup() separately validates the retained media and canonical board hashes.
    protected = {p: sha(Path(p)) for p in prior['protected']}
    protected[str(BASE)] = sha(BASE)
    images = {s['asset']: cv2.imread(str(ASSETS / s['asset'])) for s in SPANS}
    assert all(im is not None for im in images.values())
    assets = {str(ASSETS / k): sha(ASSETS / k) for k in images}
    readers = {'base': Reader(snapshot)}
    for row in b8.OVERRIDES:
        if row['kind'] != 'stack':
            readers[row['start']] = Reader(b8.ROLL1 if row['kind'] == 'horse' else b8.TRANSFORMER)
    mask, cleaning = glyph_mask(), dict(clone=0, inpaint=0, declined=0)
    wanted = {0, b8.TOTAL - 1}
    for s in SPANS:
        wanted.update([s['start'] - 1, s['start'], s['start'] + 1,
                       (s['start'] + s['end']) // 2, s['end'] - 1, s['end'], s['end'] + 1])
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.Popen([ff, '-v', 'error', '-n', '-f', 'rawvideo',
        '-pix_fmt', 'bgr24', '-s', '1280x720', '-r', '30', '-i', 'pipe:0',
        '-i', str(BASE), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264',
        '-preset', 'fast', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
        '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    timeline = []
    for f in range(b8.TOTAL):
        span = next((s for s in SPANS if s['start'] <= f < s['end']), None)
        if span:
            im = illustration(images[span['asset']], (f - span['start']) / (span['end'] - span['start'] - 1))
            label = Path(span['asset']).stem
        else:
            im, label = b8.frame_at(f, renderers, mapped, stack, readers, mask, cleaning)
        proc.stdin.write(im.tobytes())
        if not timeline or timeline[-1]['label'] != label:
            timeline.append(dict(label=label, start_frame=f, end_frame=f + 1))
        else:
            timeline[-1]['end_frame'] = f + 1
        if f in wanted:
            cv2.imwrite(str(OUT / 'preview' / f'{f:05d}-{label}.png'), im)
        if f % 1000 == 999:
            print('Rendered', f + 1, flush=True)
    proc.stdin.close()
    assert proc.wait() == 0
    for r in readers.values():
        r.c.release()
    assert all(sha(Path(p)) == h for p, h in protected.items())
    manifest = dict(candidate=str(DEST), render_sha256=sha(DEST), base=str(BASE),
        base_sha256=sha(BASE), fps=30, frames=b8.TOTAL, duration=b8.TOTAL / 30,
        audio='Approved v8 AAC stream copied without re-encoding or timing changes',
        reconstruction='Same original source and canonical board renders as v8; two new raster illustrations',
        visual_replacements=SPANS, assets=assets, visual_timeline=timeline,
        protected=protected, boundaries=prior['boundaries'], camera_push_percent=1,
        approval='User approved narration and lesson progression, then agreed to the two-illustration visual-only revision.',
        published=False)
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(DEST, flush=True)


if __name__ == '__main__':
    main()
