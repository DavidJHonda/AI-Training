#!/usr/bin/env python3
"""Verify actual encoded v12; audio packet identity, frame and ring evidence."""
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

import build_learn_with_ai_v10 as b

OUT = b.ROOT / 'video-audit/learn-with-ai-build-2026-09-29-v12'
VIDEO = b.ROOT / 'Prompts/learn-with-ai-v12.mp4'


def main():
    m = json.loads((OUT / 'edit-manifest.json').read_text())
    assert b.sha(VIDEO) == m['candidate_sha256']
    encoded = OUT / 'encoded'
    encoded.mkdir(exist_ok=True)
    wanted = set(m['preview_frames']) | set(range(560, 846, 10)) | {580, 600, 720, 825, 1487, 1560, 1659}
    renderers = {k: b.ShippedCameraRenderer(v) for k, v in m['boards'].items()}
    samples, rings, diffs = [], [], []
    mapping = m['board_frame_mapping']
    cap = cv2.VideoCapture(str(VIDEO))
    source = b.Reader(b.SOURCE)
    count = 0
    min_mean = 255
    while True:
        ok, im = cap.read()
        if not ok:
            break
        assert im.shape == (720, 1280, 3)
        min_mean = min(min_mean, float(im.mean()))
        if count in wanted:
            cv2.imwrite(str(encoded / f'{count:05d}.jpg'), im, [cv2.IMWRITE_JPEG_QUALITY, 95])
        if count % 120 == 0:
            samples.append((count, Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)).resize((480, 270))))
            row = next(r for r in m['visual_timeline'] if r['start'] <= count < r['end'])
            if row['label'] == 'retained':
                old = source.at(count)
                diffs.append(dict(frame=count, mean_abs_delta=float(np.abs(im.astype(float)-old).mean())))
        if count % 30 == 0 and str(count) in mapping and not any(r['start'] <= count < r['end'] for r in b.CUTAWAYS):
            key, local = mapping[str(count)]
            renderer = renderers[key]
            settled = local > 0 and local+1 < len(renderer.cameras) and renderer.cameras[local-1] == renderer.cameras[local] == renderer.cameras[local+1]
            if settled:
                expected, base, geo = renderer.at(local)
                for g in geo:
                    x0, y0, x1, y1 = g['box']
                    assert min(x0-2, y0-2) >= 0 and x1+2 < 1280 and y1+2 < 720, (count, g)
                    widths, errors = [], []
                    # Luma isolates stroke coverage from 4:2:0 chroma bleed.
                    # The canonical board without rings supplies the background.
                    luma = np.array([.114, .587, .299])
                    for fraction in [.4, .5, .6]:
                        xx = round(x0+(x1-x0)*fraction)
                        for yy in [round(y0-2), round(y1+2)-4]:
                            bg = base[yy-5:yy+9, xx].astype(float) @ luma
                            signal = im[yy-5:yy+9, xx].astype(float) @ luma
                            contrast = np.array(g['color_bgr']) @ luma - bg
                            if np.abs(contrast).min() > 20:
                                widths.append(int((((signal-bg)/contrast) > .5).sum()))
                            delta = im[yy:yy+4, xx].astype(float)-expected[yy:yy+4, xx].astype(float)
                            errors.append(float(np.abs(delta @ luma).mean()))
                    rings.append(dict(frame=count, board=key, widths=widths,
                        max_mean_luma_delta=max(errors), geometry=g))
        count += 1
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    source.c.release()
    assert count == 6583 and fps == 30
    for page in range(0, len(samples), 12):
        group = samples[page:page+12]
        sheet = Image.new('RGB', (1440, 295*((len(group)+2)//3)), 'white')
        for j, (f, im) in enumerate(group):
            x, y = j%3*480, j//3*295
            sheet.paste(im, (x,y+25))
            ImageDraw.Draw(sheet).text((x+6,y+5), f'{f/30:.2f}s / f{f}', fill='black')
        sheet.save(OUT / f'encoded-sheet-{page//12}.jpg')
    cmd = [str(b.ROOT/'.video-venv/bin/python'), str(b.ROOT/'scripts/video/transition_guard.py'), str(VIDEO), '--outdir', str(OUT/'guard')]
    for f in m['boundaries']:
        cmd.extend(['--boundary', f'{f}:changed-span'])
    guard = subprocess.run(cmd)
    audio_hash = b.payload_hash(VIDEO)
    source_hash = b.payload_hash(b.SOURCE)
    assert audio_hash == source_hash
    assert all(b.sha(Path(p)) == h for p,h in m['protected'].items())
    assert all(r['mean_abs_delta'] < 5 for r in diffs), diffs
    ring_values = [v for r in rings for v in r['widths']]
    assert ring_values and all(v == 4 for v in ring_values), sorted(set(ring_values))
    assert all(r['max_mean_luma_delta'] < 8 for r in rings)
    assert guard.returncode == 0
    result = dict(candidate_sha256=b.sha(VIDEO), decoded_frames=count, fps=fps, duration=count/fps,
        audio_packet_payload_identical=True, audio_payload_sha256=audio_hash,
        source_unchanged=b.sha(b.SOURCE)==b.EXPECTED, protected_files_unchanged=True,
        transition_guard_exit=guard.returncode, minimum_frame_mean=min_mean,
        retained_frame_comparisons=diffs, settled_ring_samples=rings,
        ring_luma_coverage_width_values=sorted(set(ring_values)),
        ring_measurement_count=len(ring_values),
        ring_max_mean_luma_delta=max(r['max_mean_luma_delta'] for r in rings),
        listening_performed=False, reason='No audio changes; packet identity establishes preservation, not an auditory quality review.')
    b.write_json(OUT / 'qa.json', result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['retained_frame_comparisons','settled_ring_samples']}, indent=2), flush=True)


if __name__ == '__main__':
    main()
