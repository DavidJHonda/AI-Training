#!/usr/bin/env python3
"""Approved narrow repair: explain tokens and numerical representations in motion."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Prompts/understand-ai-opener-v12.mp4'
EXPECTED = '678834d55181084916a2db0e79bdf741c800b7b764299d933130ee8d4cc249ba'
DEST = ROOT / 'Prompts/understand-ai-opener-v13.mp4'
OUT = ROOT / 'video-audit/understand-ai-opener-build-2026-09-29-v13'
FPS, TOTAL = 30, 4441
START, END = 3235, 3561  # 107.833 through 118.700, before fourth-topic onset 119.60
TOKENS, NUMBERS = 3339, 3467  # 111.300 and 115.567, rounded to output frames
BG, INK, MUTED = '#f7faf8', '#172c36', '#52656a'
TEAL, PALE = '#0e8f86', '#e4f3ef'
SS = 2


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def font(size, bold=False):
    name = 'Arial Bold.ttf' if bold else 'Arial.ttf'
    return ImageFont.truetype('/System/Library/Fonts/Supplemental/' + name, size * SS)


def text(draw, xy, words, size=32, color=INK, bold=False):
    draw.text(tuple(round(v * SS) for v in xy), words, font=font(size, bold),
              fill=color, anchor='mm')


def box(draw, bounds, fill, outline=None, radius=16):
    draw.rounded_rectangle(tuple(round(v * SS) for v in bounds),
                           radius=radius * SS, fill=fill, outline=outline, width=2 * SS)


def arrow(draw, start, end, y, color=TEAL):
    draw.line((start * SS, y * SS, end * SS, y * SS), fill=color, width=3 * SS)
    draw.polygon([(end * SS, y * SS), ((end-10)*SS, (y-6)*SS),
                  ((end-10)*SS, (y+6)*SS)], fill=color)


def ease(value):
    x = min(1, max(0, value))
    return x*x*(3-2*x)


def render(frame):
    im = Image.new('RGB', (1280 * SS, 720 * SS), BG)
    d = ImageDraw.Draw(im)
    text(d, (640, 105), 'Words become numbers', 46, bold=True)
    movement = ease((frame - (TOKENS-12)) / 12)
    split = ease((frame - TOKENS) / 10)
    numeric = ease((frame - NUMBERS) / 10)
    cx = 640 - 395 * movement
    text(d, (cx, 228), 'TEXT', 22, MUTED, True)
    text(d, (cx, 360), 'The cat sat.', 40, bold=True)
    # Token strings are a simple illustrative segmentation, not tokenizer IDs.
    if split > 0:
        layer = Image.new('RGB', im.size, BG)
        p = ImageDraw.Draw(layer)
        text(p, (630, 228), 'TOKENS', 22, TEAL, True)
        arrow(p, 405, 486, 360)
        for j, token in enumerate(['The', 'cat', 'sat', '.']):
            y = 298 + j * 72
            box(p, (530, y-27, 730, y+27), PALE, TEAL)
            text(p, (630, y), token, 32, TEAL, True)
        # Composite only this column and the incoming arrow, keeping moving text intact.
        im.paste(Image.blend(im.crop((395*SS, 200*SS, 750*SS, 574*SS)),
                             layer.crop((395*SS, 200*SS, 750*SS, 574*SS)), split),
                 (395*SS, 200*SS))
    if numeric > 0:
        layer = im.copy()
        p = ImageDraw.Draw(layer)
        text(p, (1030, 228), 'NUMBERS', 22, TEAL, True)
        vectors = ['[ 0.2,  -0.7,  … ]', '[ 0.8,   0.1,  … ]',
                   '[ -0.4,  0.6,  … ]', '[ 0.1,  -0.2,  … ]']
        for j, value in enumerate(vectors):
            y = 298 + j * 72
            arrow(p, 753, 837, y)
            text(p, (1030, y), value, 32, bold=True)
        text(p, (1030, 588), 'Illustrative values', 22, MUTED)
        im = Image.blend(im, layer, numeric)
    return im.resize((1280, 720), Image.Resampling.LANCZOS)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    assert sha(SOURCE) == EXPECTED, 'Reviewed source changed.'
    assert not DEST.exists(), 'Never overwrite a review candidate.'
    OUT.mkdir(parents=True, exist_ok=True)
    for name, n in [('text', START), ('tokens', TOKENS+15), ('numbers', NUMBERS+15)]:
        render(n).save(OUT / f'graphic-{name}.png')
    manifest = dict(
        scope='Approved narrow visual-only replacement; review candidate, not shipped.',
        approval='David: agree. Build it please. Approved text/token/number graphic through ~118.7s.',
        source=str(SOURCE), source_sha256=EXPECTED, output=str(DEST),
        fps=FPS, frames=TOTAL, duration=TOTAL/FPS,
        graphic_span=[START, END], token_reveal=TOKENS, number_reveal=NUMBERS,
        graphic_brief='Readable minimal text -> token pieces -> numerical lists; no tokenizer IDs. '
                      'Show text first, token pieces with spoken token explanation, then numeric '
                      'representations at the numbers clause. Toy vector values labeled illustrative. '
                      'Code-native explanatory graphic; no course board recreation.',
        audio='Original AAC copied without edits, fades, or new pauses.',
        board_plan='Preserve all existing boards/rings/cameras; return at 118.700s, '
                   '0.900s before fourth-topic narration. Existing third-row ring resumes.',
        map_runs=[[2423/FPS, START/FPS], [END/FPS, 4174/FPS]],
        map_run_seconds=[(START-2423)/FPS, (4174-END)/FPS],
        longest_board_chain_seconds=(TOTAL-END)/FPS,
        boundaries=[{'frame': START, 'label': 'map-to-token-graphic'},
                    {'frame': END, 'label': 'token-graphic-to-map'}],
        limitations=['Source is the approved finished v12; retained visuals re-encoded once.',
                     'No real-time audio listening claimed.'])
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    if args.prepare_only:
        return
    command = [imageio_ffmpeg.get_ffmpeg_exe(), '-n', '-v', 'error', '-f', 'rawvideo',
               '-pix_fmt', 'bgr24', '-s', '1280x720', '-r', str(FPS), '-i', 'pipe:0',
               '-i', str(SOURCE), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264',
               '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
               '-movflags', '+faststart', str(DEST)]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(str(SOURCE))
    count = 0
    cache = {}
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if START <= count < END:
            key = count
            if count < TOKENS-12: key = START
            elif TOKENS+12 <= count < NUMBERS: key = TOKENS+12
            elif count >= NUMBERS+10: key = NUMBERS+10
            if key not in cache:
                cache[key] = cv2.cvtColor(np.asarray(render(key)), cv2.COLOR_RGB2BGR)
            frame = cache[key]
        proc.stdin.write(frame.tobytes())
        count += 1
        if count % 900 == 0: print(f'Encoded {count}/{TOTAL}', flush=True)
    cap.release()
    proc.stdin.close()
    assert proc.wait() == 0
    assert count == TOTAL
    assert sha(SOURCE) == EXPECTED
    manifest.update(render_sha256=sha(DEST), encode_command=command)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(DEST, flush=True)


if __name__ == '__main__':
    cv2.setNumThreads(1)
    main()
