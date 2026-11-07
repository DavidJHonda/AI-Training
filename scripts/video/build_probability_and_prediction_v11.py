#!/usr/bin/env python3
"""Restore requested passages and add an explicit narrated AI bridge. Review only."""
import json
import subprocess
import wave
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from editspec_build import Reader, sha
from build_probability_and_prediction_v10 import ROOT, SOURCE, EXPECTED, FPS, RATE, SPF

DEST = ROOT / 'Prompts/probability-and-prediction-v11.mp4'
OUT = ROOT / 'video-audit/probability-and-prediction-flow-v11-2026-11-07'
ROWS = [
    (0, 2150, 'source', 'Opening restored; through four equally likely results'),
    (2326, 2587, 'source', 'One matches our goal; 25% calculation'),
    (2827, 3286, 'source', 'Conditional probability; first coin is heads'),
    (3536, 4298, 'source', 'Elimination and 50%; knowledge-change insight'),
    (5196, 5393, 'bridge', 'Move complete AI calculation sentence before dog example'),
    (4894, 5196, 'source', 'Dog question and response prefix'),
    (5393, 6184, 'source', 'All three names/probabilities restored; repeat loop and complete close'),
]
OVERRIDES = [
    (2827, 2847, 2586, 'Hold completed 25% board until next scene'),
    (3536, 3549, 3549, 'Bring clue board forward; remove old diagram remnant'),
    (4894, 4899, 4899, 'Bring dog board forward; remove old coin callback remnant'),
]


def bridge_image():
    im = Image.new('RGB', (1280, 720), '#f6f5fb')
    d = ImageDraw.Draw(im)
    font_path = str(ROOT / 'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf')
    for text, size, y, color, weight in [
        ('FROM COINS TO AI', 23, 184, '#667079', 600),
        ('AI uses', 53, 257, '#182c2a', 700),
        ('conditional probability', 57, 333, '#4f2fc4', 700),
        ('to answer your questions.', 49, 413, '#182c2a', 700),
    ]:
        font = ImageFont.truetype(font_path, size)
        font.set_variation_by_axes([weight])
        box = d.textbbox((0, 0), text, font=font)
        width = box[2] - box[0]
        assert width < 1080
        d.text(((1280 - width) / 2 - box[0], y - box[1]), text, font=font, fill=color)
    return im


def main():
    assert not DEST.exists(), 'Never overwrite a review candidate'
    assert sha(SOURCE) == EXPECTED
    OUT.mkdir(exist_ok=True)
    (OUT / 'qa').mkdir(exist_ok=True)
    bridge_path = OUT / 'ai-conditional-probability-bridge.png'
    bridge_image().save(bridge_path)
    bridge = cv2.imread(str(bridge_path))
    protected = {str(p): sha(p) for p in [SOURCE, ROOT / 'Prompts/probability-and-prediction-v10.mp4',
        ROOT / 'course-assets/probability-and-prediction/probability-and-prediction.mp4',
        ROOT / 'lessons/probability-and-prediction.md',
        *sorted((ROOT / 'course-assets/probability-and-prediction').glob('*.jpg'))]}
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    pcm = np.frombuffer(subprocess.check_output([ff, '-v', 'error', '-i', str(SOURCE), '-vn', '-ac', '1',
        '-ar', str(RATE), '-f', 'f32le', 'pipe:1']), np.float32).copy()
    parts, timeline, joins = [], [], []
    cursor = 0
    for i, (a, b, visual, label) in enumerate(ROWS):
        x = pcm[a * SPF:b * SPF].copy()
        if i:
            x[:240] *= np.linspace(0, 1, 240)
            joins.append(dict(frame=cursor, seconds=cursor / FPS, label=label))
        if i < len(ROWS) - 1:
            x[-240:] *= np.linspace(1, 0, 240)
        parts.append(x)
        timeline.append(dict(source=[a, b], output=[cursor, cursor + b - a], visual=visual, label=label))
        cursor += b - a
    audio = np.concatenate(parts)
    assert len(audio) == cursor * SPF
    with wave.open(str(OUT / 'edited.wav'), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(np.clip(audio * 32768, -32768, 32767).astype('<i2').tobytes())
    m = dict(source=str(SOURCE), source_sha256=EXPECTED, candidate=str(DEST), fps=FPS, frames=cursor,
             duration=cursor / FPS, timeline=timeline, joins=joins, protected=protected,
             picture_overrides=[dict(source_frames=[a, b], use_source_frame=n, reason=r) for a,b,n,r in OVERRIDES],
             bridge=dict(image=str(bridge_path), sha256=sha(bridge_path),
                         screen_text='AI uses conditional probability to answer your questions.',
                         narration='Based on the words already written, the AI calculates the likelihood for the next word in the sequence.',
                         source_frames=[5196, 5393], output_frames=timeline[4]['output']),
             scope='Restore original opening 0:07–0:15 and full Spot/Max/Buddy readout; add a transition from coins to AI before the dog example. Preserve other approved cuts.',
             audio='Same source narrator; one complete sentence moved, 5ms quiet-edge ramps; no generated voice, added silence, or gain changes.',
             source_limitation='Built directly from finished v9 in one additional H.264 encode; not transcoded from v10.',
             publication='Review candidate only; installed course unchanged.')
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2) + '\n')
    r = Reader(SOURCE)
    stills = {n:r.at(n) for n in sorted({r[2] for r in OVERRIDES})}
    r.c.release()
    enc = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1280x720',
        '-r', '30', '-i', 'pipe:0', '-i', str(OUT / 'edited.wav'), '-map', '0:v', '-map', '1:a',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
        '-b:a', '192k', '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    rd = Reader(SOURCE)
    count = 0
    for a, b, visual, label in ROWS:
        for n in range(a, b):
            if visual == 'bridge':
                frame = bridge
            else:
                frame = rd.at(n)
                override = next((r for r in OVERRIDES if r[0] <= n < r[1]), None)
                if override:
                    frame = stills[override[2]]
            enc.stdin.write(frame.tobytes())
            count += 1
        print(f'Rendered {count}/{cursor}: {label}', flush=True)
    enc.stdin.close()
    assert enc.wait() == 0
    rd.c.release()
    assert count == cursor
    assert all(sha(Path(p)) == h for p,h in protected.items())
    m.update(render_sha256=sha(DEST), bytes=DEST.stat().st_size)
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2) + '\n')
    print(json.dumps(dict(candidate=str(DEST), duration=cursor / FPS)), flush=True)


if __name__ == '__main__':
    main()
