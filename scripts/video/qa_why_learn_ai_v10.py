#!/usr/bin/env python3
"""Check narrow photographic revision, including all changed frame boundaries."""
import json
import subprocess
import sys
from pathlib import Path
import cv2
import numpy as np
from editspec_build import sha

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/why-learn-ai-rerolls-2026-09-29/build-v10'
VIDEO = ROOT / 'Prompts/why-learn-ai-v10.mp4'


def main():
    m = json.loads((OUT / 'edit-manifest.json').read_text())
    spans = m['revision']['changed_spans']
    boundaries = [(r[k], r['key'] + '-' + k) for r in spans for k in ['start', 'end']]
    cmd = [sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(VIDEO), '--outdir', str(OUT / 'guard')]
    for f, label in boundaries:
        cmd += ['--boundary', f'{f}:{label}']
    subprocess.run(cmd, check=True)
    cap = cv2.VideoCapture(str(VIDEO))
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = [int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))]
    assert count == 7075 and fps == 30 and size == [1280, 720]
    qa = OUT / 'qa'
    qa.mkdir(exist_ok=True)
    for row in spans:
        tiles = []
        for f in [row['start'], (row['start'] + row['end']) // 2, row['end'] - 1]:
            cap.set(cv2.CAP_PROP_POS_FRAMES, f)
            ok, im = cap.read()
            assert ok
            cv2.imwrite(str(qa / f"{row['key']}-{f}.png"), im)
            tile = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
            cv2.putText(tile, f'f{f}  {f/30:.2f}s', (12, 24), cv2.FONT_HERSHEY_SIMPLEX, .65, (255, 255, 255), 2, cv2.LINE_AA)
            tiles.append(tile)
        cv2.imwrite(str(qa / f"{row['key']}-strip.jpg"), cv2.vconcat(tiles))
    # Sample every untouched span against v9. Both are rendered from pristine
    # sources; lossy encoder differences are expected, wholesale changes aren't.
    old = cv2.VideoCapture(m['revision']['base_video'])
    differences = []
    for row in m['visual_timeline']:
        if row['kind'] == 'still':
            continue
        f = (row['start'] + row['end']) // 2
        cap.set(cv2.CAP_PROP_POS_FRAMES, f)
        old.set(cv2.CAP_PROP_POS_FRAMES, f)
        ok, im = cap.read()
        ok2, before = old.read()
        assert ok and ok2
        mad = float(np.abs(im.astype(np.float32) - before).mean())
        assert mad < 2.0, (f, mad)
        differences.append({'frame': f, 'label': row['label'], 'mean_absolute_pixel_difference': mad})
    cap.release()
    old.release()
    checks = dict(video=str(VIDEO), sha256=sha(VIDEO), frames=count, fps=fps, dimensions=size,
                  duration=count/fps, audio_packet_identical=m['revision']['audio_packet_md5']['identical'],
                  protected_files_unchanged=m['protected_files_unchanged'],
                  untouched_span_samples=differences, changed_boundaries=len(boundaries),
                  visual_inspection_complete=False, listening_performed=False)
    (OUT / 'checks.json').write_text(json.dumps(checks, indent=2))
    print(json.dumps({'frames': count, 'duration': count/fps, 'changed_boundaries': len(boundaries), 'max_untouched_sample_difference': max(r['mean_absolute_pixel_difference'] for r in differences)}, indent=2))


if __name__ == '__main__':
    main()
