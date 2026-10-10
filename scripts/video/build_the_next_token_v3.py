#!/usr/bin/env python3
"""Narrow repair: outline the opening labels at their spoken onsets."""
import json
import shutil
import cv2
from PIL import Image, ImageDraw
import build_the_next_token_v2 as previous

base = previous.base
OLD = base.OUT
base.OUT = base.ROOT / 'video-audit/the-next-token-build-2026-10-09-v3'
base.DEST = base.ROOT / 'Prompts/the-next-token-v3.mp4'
original_diagram = base.diagram

# Existing word timestamps: sampling 14.40, temperature 15.28 seconds.
# Use the nearest delivery frame; the latter is 15.30 seconds at 30 fps.
SAMPLING = 432
TEMPERATURE = 459
END = 486

def diagram(kind, k, n):
    frame = original_diagram(kind, k, n)
    if kind == 'opening' and SAMPLING <= k < END:
        im = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        x = 100 if k < TEMPERATURE else 965
        ImageDraw.Draw(im).rounded_rectangle(
            (x, 640, x + 220, 691), radius=15,
            outline=base.PURPLE, width=4)
        return base.arr(im)
    return frame

base.diagram = diagram
original_prepare = base.prepare

def prepare():
    film, manifest = original_prepare()
    manifest['narrow_repair'] = {
        'request': 'At :15, highlight sampling and temperature as spoken',
        'prior_candidate': str(previous.base.ROOT / 'Prompts/the-next-token-v2.mp4'),
        'changed_frames': [SAMPLING, END],
        'highlights': [
            {'label': 'Sampling', 'start_frame': SAMPLING, 'end_frame': TEMPERATURE,
             'rect': [100, 640, 220, 51]},
            {'label': 'Temperature', 'start_frame': TEMPERATURE, 'end_frame': END,
             'rect': [965, 640, 220, 51]}],
        'stroke_px': 4, 'color': base.PURPLE,
        'camera': 'Unchanged full view', 'audio': 'Unchanged',
        'timing_basis': 'Retained roll-3 word timestamps; nearest 30 fps frame'
    }
    for f in [431, 432, 444, 458, 459, 474, 485, 486]:
        cv2.imwrite(str(base.OUT / 'preview' / f'{f:06d}.jpg'), film.frame(f))
    film.release()
    return film, manifest

base.prepare = prepare

if __name__ == '__main__':
    base.OUT.mkdir(exist_ok=True)
    for name in ['roll-1.wav', 'roll-3.wav', *[f'temperature-{i}.png' for i in range(4)]]:
        if not (base.OUT / name).exists():
            shutil.copy2(OLD / name, base.OUT / name)
    base.main()
