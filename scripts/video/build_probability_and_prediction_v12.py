#!/usr/bin/env python3
"""Insert the exact requested spoken transition from math-line-1. Review only."""
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

DEST = ROOT / 'Prompts/probability-and-prediction-v12.mp4'
DONOR = ROOT / 'Prompts/math-line-1.mp4'
DONOR_SHA = '70c52323512282929897a9b2d07f40eaa4e94754a77a80ba42c065719fe1dbe3'
# Full speech-RMS match would add 2.615 dB and clip 12 samples. A 1.7 dB
# adjustment leaves the donor within 0.915 dB of the adjacent speech and
# preserves peak headroom without limiting or changing the base narration.
GAIN_DB = 1.7
OUT = ROOT / 'video-audit/probability-and-prediction-spoken-bridge-v12-2026-11-07'
ROWS = [
    (0, 2150, 'source', 'Opening restored; through four equally likely results'),
    (2326, 2587, 'source', 'One matches our goal; 25% calculation'),
    (2827, 3286, 'source', 'Conditional probability; first coin is heads'),
    (3536, 4298, 'source', 'Elimination and 50%; knowledge-change insight'),
    (891, 1008, 'bridge', 'Exact spoken conditional-probability transition from math-line-1'),
    (4894, 5196, 'source', 'Dog question and response prefix'),
    (5393, 6184, 'source', 'All three names/probabilities restored; repeat loop and complete close'),
]
OVERRIDES = [
    (2827, 2847, 2586, 'Hold completed 25% board until next scene'),
    (3536, 3549, 3549, 'Bring clue board forward; remove old diagram remnant'),
    (4894, 4899, 4899, 'Bring dog board forward; remove old coin callback remnant'),
]


def bridge_image():
    # Use the canonical dog board as an unmarked introduction, not a text card.
    asset = ROOT / 'course-assets/probability-and-prediction/probability-and-prediction-what-comes-next.jpg'
    im = cv2.imread(str(asset)); h, w = im.shape[:2]
    scale = min(1220 / w, 680 / h)
    nw, nh = round(w * scale), round(h * scale)
    x, y = (1280 - nw) // 2, (720 - nh) // 2
    canvas = np.full((720, 1280, 3), (251, 245, 246), np.uint8)
    canvas[y:y + nh, x:x + nw] = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_AREA)
    return Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))


def main():
    assert not DEST.exists(), 'Never overwrite a review candidate'
    assert sha(SOURCE) == EXPECTED
    assert sha(DONOR) == DONOR_SHA
    OUT.mkdir(exist_ok=True)
    (OUT / 'qa').mkdir(exist_ok=True)
    bridge_path = OUT / 'dog-board-unmarked.png'
    bridge_image().save(bridge_path)
    bridge = cv2.imread(str(bridge_path))
    protected = {str(p): sha(p) for p in [SOURCE, DONOR, ROOT / 'Prompts/math-line-2.mp4', ROOT / 'Prompts/probability-and-prediction-v11.mp4',
        ROOT / 'course-assets/probability-and-prediction/probability-and-prediction.mp4',
        ROOT / 'lessons/probability-and-prediction.md',
        *sorted((ROOT / 'course-assets/probability-and-prediction').glob('*.jpg'))]}
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    pcm = np.frombuffer(subprocess.check_output([ff, '-v', 'error', '-i', str(SOURCE), '-vn', '-ac', '1',
        '-ar', str(RATE), '-f', 'f32le', 'pipe:1']), np.float32).copy()
    donor_pcm = np.frombuffer(subprocess.check_output([ff, '-v', 'error', '-i', str(DONOR), '-vn', '-ac', '1',
        '-ar', str(RATE), '-f', 'f32le', 'pipe:1']), np.float32).copy()
    parts, timeline, joins = [], [], []
    cursor = 0
    for i, (a, b, visual, label) in enumerate(ROWS):
        x = (donor_pcm if visual == 'bridge' else pcm)[a * SPF:b * SPF].copy()
        if visual == 'bridge':
            x *= 10 ** (GAIN_DB / 20)
        assert np.max(np.abs(x)) < 1, 'Audio clipping'
        if i:
            x[:240] *= np.linspace(0, 1, 240)
            joins.append(dict(frame=cursor, seconds=cursor / FPS, label=label))
        if i < len(ROWS) - 1:
            x[-240:] *= np.linspace(1, 0, 240)
        parts.append(x)
        timeline.append(dict(source=[a, b], output=[cursor, cursor + b - a], visual=visual, label=label, audio_source=str(DONOR if visual == 'bridge' else SOURCE), gain_db=GAIN_DB if visual == 'bridge' else 0))
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
                         screen_text='Canonical What Comes Next? board; unmarked full view',
                         narration='AI uses conditional probability to answer your questions.',
                         source_frames=[891, 1008], donor=str(DONOR), donor_sha256=DONOR_SHA, gain_db=GAIN_DB, output_frames=timeline[4]['output']),
             scope='Replace v11 text transition and relocated explanation with the exact spoken line from math-line-1, over the unmarked canonical dog board. Preserve restored opening, all three names/probabilities, and other approved cuts.',
             audio='One complete donor sentence, +1.7 dB gain (within 0.915 dB of adjacent speech RMS, with peak headroom). Five-ms quiet-edge ramps; no synthesized voice or extra silence. Remaining narration comes from v9 unchanged.',
             source_limitation='Built directly from finished v9 in one additional H.264 encode; not transcoded from v10 or v11.',
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
