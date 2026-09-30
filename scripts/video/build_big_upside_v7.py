#!/usr/bin/env python3
"""Add the requested Hassabis quotation; reconstruct v6 from its original sources."""
import json
import sys
from pathlib import Path
import cv2
from PIL import Image, ImageDraw, ImageFont
import build_big_upside_v6 as b

ROOT = b.ROOT
OUT = ROOT / 'video-audit/big-upside-quote-2026-09-30-v7'
DEST = ROOT / 'Prompts/big-upside-v7.mp4'
ASSET = ROOT / 'scripts/video/assets/big-upside-quote-2026-09-30/hassabis-quote.png'
START, END = 2760, 3049
SOURCE_URL = 'https://deepmind.google/blog/demis-hassabis-john-jumper-awarded-nobel-prize-in-chemistry/'
QUOTE = 'I’ve dedicated my career to advancing AI because of its unparalleled potential to improve the lives of billions of people.'
FONT = ROOT / 'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
original_setup, original_replacement = b.setup, b.replacement


def graphic():
    ASSET.parent.mkdir(parents=True, exist_ok=True)
    scale = 3
    im = Image.new('RGB', (1280*scale, 720*scale), '#f8f8f3')
    d = ImageDraw.Draw(im)
    def face(size, weight=500):
        font = ImageFont.truetype(str(FONT), round(size*scale))
        font.set_variation_by_axes([weight])
        return font
    def text(x, y, words, size, weight=500, color='#20292c'):
        font = face(size, weight)
        assert x*scale + d.textlength(words, font=font) < 1195*scale
        d.text((x*scale, y*scale), words, font=font, fill=color, anchor='lt')
    text(98, 66, '“', 115, 800, '#6e51ff')
    lines = ['I’ve dedicated my career to advancing AI',
             'because of its unparalleled potential to',
             'improve the lives of',
             'billions of people.”']
    assert ' '.join(lines).rstrip('”') == QUOTE
    for i, line in enumerate(lines):
        text(104, 190+i*65, line, 47, 750 if i >= 2 else 500,
             '#4f2fc4' if i >= 2 else '#20292c')
    d.rounded_rectangle((104*scale, 520*scale, 164*scale, 525*scale), radius=2*scale, fill='#6e51ff')
    text(104, 551, 'Demis Hassabis', 28, 750)
    text(104, 594, 'On receiving the 2024 Nobel Prize in Chemistry', 21, 500, '#626772')
    text(104, 658, 'Source: Google DeepMind · October 9, 2024', 16, 500, '#626772')
    im.resize((1280,720), Image.Resampling.LANCZOS).save(ASSET)
    return cv2.imread(str(ASSET))


def configure():
    b.OUT, b.DEST = OUT, DEST
    quote = graphic()
    def setup():
        old, renderers, specs, images = original_setup()
        old['boundaries'].append(dict(frame=START, label='Hassabis quote: motivation'))
        images['hassabis-quote'] = quote
        for n in [START, START+60, END-1]:
            cv2.imwrite(str(OUT/'preview'/f'{n:05d}.png'), quote)
        return old, renderers, specs, images
    def replacement(n, renderers, specs, images):
        if START <= n < END:
            return images['hassabis-quote']
        return original_replacement(n, renderers, specs, images)
    b.setup, b.replacement = setup, replacement
    b.changed = lambda n: START <= n < 6349


def main():
    configure()
    b.main()
    p = OUT/'edit-manifest.json'
    manifest = json.loads(p.read_text())
    manifest.update(scope='User-requested quote graphic at 1:32, retaining all v6 repairs. Build only.',
                    changed_spans=[[START,6349]],
                    quote=dict(start=START, end=END, text=QUOTE, attribution='Demis Hassabis',
                               asset=str(ASSET), source=SOURCE_URL,
                               treatment='Full-frame, static readable typography; purple emphasis on final phrase.',
                               timing='Starts at 1:32 before the motivation introduction; rejoins existing health board at 1:41.633.'))
    manifest['protected'][str(ASSET)] = b.sha(ASSET)
    manifest['protected'][str(FONT)] = b.sha(FONT)
    p.write_text(json.dumps(manifest, indent=2)+'\n')


if __name__ == '__main__':
    main()
