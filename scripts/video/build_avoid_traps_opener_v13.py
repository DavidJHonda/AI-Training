#!/usr/bin/env python3
"""Restore the live opener's visual sequence under the unchanged v12 audio."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

from editspec_build import Reader, sha

ROOT = Path(__file__).resolve().parents[2]
# The selected installed v11 footage also survives under this immutable candidate
# name. Shipping v14 replaces the canonical path; keep the selected pixels pinned.
LIVE = ROOT/'Prompts/avoid-traps-opener-v11.mp4'
BASE = ROOT/'Prompts/avoid-traps-opener-v12.mp4'
DEST = ROOT/'Prompts/avoid-traps-opener-v13.mp4'
OUT = ROOT/'video-audit/avoid-opener-v13-2026-11-11'
FPS = 30
TOTAL = 4153
FF = imageio_ffmpeg.get_ffmpeg_exe()
WATER = ROOT/'course-assets/avoid-traps-opener/avoid-traps-opener-read-the-water.jpg'
EXPECTED = {
    LIVE: '0b1467c509908468e6c3e0e951671bb6cc581bf60e9b45cb0ddc83d5146f819b',
    BASE: '342a17b5a583c3ca7297e5affd1c105f45ede0c4c5777c3f4fbdb0b61295ee7a',
    WATER: '0c19d08cbfa8d11a1d599904964d60d3fe3586947a96a7e018ece0d4eca98bcc',
}

# Source intervals exclude every retired roadmap frame. The original motion,
# reveals and full-view/illustration camera are sampled monotonically within
# each selected scene; there is no crossfade, reverse playback or loop.
ROWS = [
    dict(start=0, end=300, file=str(LIVE), source_start=0, source_end=258,
         label='Server corridor: the same machinery produces capability and failure'),
    dict(start=300, end=489, file=str(LIVE), source_start=4874, source_end=5052,
         label='Server detail: characteristic repeating failure patterns'),
    dict(start=489, end=957, file=str(LIVE), source_start=510, source_end=897,
         label='Clean sentence reveals fabricated content: form does not establish truth'),
    dict(start=957, end=1233, file=str(LIVE), source_start=897, source_end=1108,
         label='Relaxed user: agreeable output feels reassuring'),
    dict(start=1233, end=1467, file=str(LIVE), source_start=2388, source_end=2625,
         label='Looks helpful, hides the risk: deceptive appearance'),
    dict(start=1467, end=1665, file=str(LIVE), source_start=1108, source_end=1252,
         label='Watchful computer user: look for what appearances conceal'),
    dict(start=1665, end=2468, file=str(LIVE), source_start=1275, source_end=1823,
         label='Rip-current reveal: calm gap, apparent safe spot, swimmer and offshore flow'),
    dict(start=2468, end=2930, file=str(LIVE), source_start=1823, source_end=2388,
         label='Current canonical Read the Water illustration with its approved camera sequence'),
    dict(start=2930, end=3085, file=str(LIVE), source_start=1108, source_end=1252,
         label='Return to watchful AI user: apply the recognition analogy'),
    dict(start=3085, end=3376, file=str(LIVE), source_start=4558, source_end=4786,
         label='Binoculars reveal the channel: recognize the deceptive pattern'),
    dict(start=3376, end=4153, file=str(BASE), source_start=3376, source_end=4153,
         label='Preserved current questions, highlights, shared introduction and standard close'),
]


def source_frame(row, output_frame):
    i = output_frame-row['start']
    n = row['end']-row['start']
    return row['source_start']+round(i*(row['source_end']-row['source_start']-1)/max(1, n-1))


def check_plan():
    assert ROWS[0]['start'] == 0 and ROWS[-1]['end'] == TOTAL
    assert all(left['end'] == right['start'] for left, right in zip(ROWS, ROWS[1:]))
    for path, expected in EXPECTED.items():
        assert sha(path) == expected, path
    for row in ROWS:
        assert row['start'] < row['end'] and row['source_start'] < row['source_end']
        assert source_frame(row, row['end']-1) == row['source_end']-1
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = dict(
        authorization='User rejected the weak v12 graphics and identified the live video as much more engaging; restore and adapt its visual sequence.',
        scope='Visual correction only; v12 AAC audio stream copied without modification, same duration and questions/close',
        source_hashes={str(path): expected for path, expected in EXPECTED.items()},
        output=str(DEST), fps=FPS, frames=TOTAL, duration=TOTAL/FPS, visual_rows=ROWS,
        audio_source=str(BASE), audio_operation='AAC stream copy; no audio processing, cuts, grafts or pauses',
        source_limitation='The approved installed finished video supplies already-rendered drawings; selected pixels receive one additional video encode.',
        current_asset_verification='Read the Water JPG hash matches the September 29 v9 manifest in the installed video lineage; retain its existing approved full-view/illustration/return camera.',
        picture_retime='Monotonic frame resampling within each complete selected scene; no narration speed change, loops or decorative crossfades',
        board_plan=[
            dict(title='Read the Water', output_frames=[2468,2930], highlight='unmarked',
                 camera='Preserve the live full-board opening, illustration walk and return',
                 seconds=462/30, reason='Restore the stronger student/beach analogy illustration already approved in the live cut'),
            dict(title='Avoid Traps', output_frames=[3376,3835], highlight='Retain v12 current row outlines exactly',
                 camera='Retain full-view compact framing', seconds=459/30),
            dict(title='When AI fails, nothing looks broken. / This section teaches you to read the water.',
                 output_frames=[3835,4153], highlight='unmarked', camera='Retain v12 standard close exactly', seconds=318/30),
        ],
        installed=False, direct_listening_performed=False, continuous_audiovisual_review_performed=False,
    )
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest


def prepare_preview(encoded=False):
    # A concrete frame comparison at the same output moments; the right column
    # previews the declared donor mapping, rather than comparing unrelated times.
    rows = [(0, 'Opening machinery'), (27, 'Confident false content'),
            (35, 'Flattery feels good'), (89, 'Recognize before entering'),
            (108, 'Learn to read the water')]
    sheet = Image.new('RGB', (1280, 58+len(rows)*388), '#f3f3f3')
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 15), 'V12: rejected visual selection', fill='black')
    draw.text((652, 15), 'V13: selected live-video graphics', fill='black')
    for index, (seconds, label) in enumerate(rows):
        frame = seconds*FPS
        row = next(row for row in ROWS if row['start'] <= frame < row['end'])
        pair = []
        right = (DEST, frame) if encoded else (Path(row['file']), source_frame(row, frame))
        for path, sf in [(BASE, frame), right]:
            reader = Reader(path)
            pair.append(reader.at(sf))
            reader.c.release()
        y = 58+index*388
        draw.text((12, y), f'{seconds//60}:{seconds%60:02d}  {label}', fill='black')
        for side, im in enumerate(pair):
            image = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)).resize((640,360))
            sheet.paste(image, (side*640, y+24))
    sheet.save(OUT/'visual-comparison.jpg')


def render(manifest):
    assert not DEST.exists(), 'Never overwrite an existing review candidate.'
    p = subprocess.Popen([
        FF, '-n', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', '1280x720', '-r', '30', '-i', 'pipe:0', '-i', str(BASE),
        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-threads', '2',
        '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
        '-movflags', '+faststart', str(DEST),
    ], stdin=subprocess.PIPE)
    for row in ROWS:
        reader = Reader(row['file'])
        for f in range(row['start'], row['end']):
            im = reader.at(source_frame(row, f))
            p.stdin.write(im.tobytes())
        reader.c.release()
        print(f"Rendered through {row['end']/FPS:.3f}s: {row['label']}", flush=True)
    p.stdin.close()
    assert p.wait() == 0
    assert all(sha(path) == expected for path, expected in EXPECTED.items())
    manifest['sha256'] = sha(DEST)
    manifest['protected_inputs_unchanged'] = True
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    manifest = check_plan()
    prepare_preview()
    if not args.prepare_only:
        render(manifest)
        prepare_preview(encoded=True)
    print(f'Prepared {TOTAL/FPS:.3f}s visual correction: {DEST}', flush=True)


if __name__ == '__main__':
    main()
