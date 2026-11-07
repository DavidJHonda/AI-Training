#!/usr/bin/env python3
"""Approved redundancy cuts, using finished v9. Review candidate only."""
from pathlib import Path
import json
import subprocess
import wave

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Reader, sha

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Prompts/probability-and-prediction-v9.mp4'
DEST = ROOT / 'Prompts/probability-and-prediction-v10.mp4'
OUT = ROOT / 'video-audit/probability-and-prediction-shortening-v10-2026-11-07'
EXPECTED = 'ece825d7d83cd6249a6ce240fb2c2a1cc41a21283e9cfd407f14f20055eec1b3'
FPS, RATE, SPF = 30, 48000, 1600
# Half-open source frame ranges. Boundary placement uses measured audio gaps,
# not the earlier approximate transcript times.
CUTS = [
    (208, 457, 'Repeated-Claude-opening', 'Tools like Claude ... behind the interface.'),
    (2150, 2326, 'Coin-list', 'You could get two heads ... or two tails.'),
    (2587, 2827, 'Repeated-quarter-result', 'At this stage ... exactly one out of four.'),
    (3286, 3536, 'Clue-pre-explanation', 'Knowing the first coin ... no longer possible.'),
    (4298, 4894, 'Repeated-odds-and-AI-overview', 'That new information ... just like knowing the result of the first coin toss.'),
    (5196, 5393, 'Repeated-next-word-explanation', 'Based on the words already written ... next word in the sequence.'),
    (5486, 5619, 'Max-and-Buddy-list', '17 percent for Max, and 14 percent for Buddy.'),
]
# Repair tiny picture remnants at the audio joins without moving speech.
# Use approved adjacent picture states, then resume original moving footage.
OVERRIDES = [
    (457, 463, 207, 'Hold ChatGPT opening until probability scene; omit Claude remnant'),
    (2827, 2847, 2586, 'Hold completed 25% board until conditional-probability scene; omit recap remnant'),
    (3536, 3549, 3549, 'Bring unmarked clue board forward; omit eliminated diagram remnant'),
    (4894, 4899, 4899, 'Bring existing dog board forward; omit coin callback remnant'),
]


def main():
    assert not DEST.exists(), 'Never overwrite an existing review candidate'
    assert sha(SOURCE) == EXPECTED
    OUT.mkdir(exist_ok=True)
    (OUT / 'qa').mkdir(exist_ok=True)
    protected_paths = [SOURCE, ROOT / 'course-assets/probability-and-prediction/probability-and-prediction.mp4',
                       ROOT / 'lessons/probability-and-prediction.md',
                       *sorted((ROOT / 'course-assets/probability-and-prediction').glob('*.jpg'))]
    protected = {str(p): sha(p) for p in protected_paths}
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    pcm = np.frombuffer(subprocess.check_output([
        ff, '-v', 'error', '-i', str(SOURCE), '-vn', '-ac', '1', '-ar', str(RATE),
        '-f', 'f32le', 'pipe:1']), np.float32).copy()
    keeps = []
    cursor = 0
    for a, b, _, _ in CUTS:
        keeps.append((cursor, a))
        cursor = b
    keeps.append((cursor, 6184))
    parts, spans, joins = [], [], []
    cursor = 0
    for i, (a, b) in enumerate(keeps):
        x = pcm[a * SPF:b * SPF].copy()
        # Five-millisecond ramps only within measured quiet shoulders.
        if i:
            x[:240] *= np.linspace(0, 1, 240)
            joins.append({'frame': cursor, 'seconds': cursor / FPS, 'label': CUTS[i - 1][2]})
        if i < len(keeps) - 1:
            x[-240:] *= np.linspace(1, 0, 240)
        parts.append(x)
        spans.append({'source': [a, b], 'output': [cursor, cursor + b - a]})
        cursor += b - a
    audio = np.concatenate(parts)
    assert len(audio) == cursor * SPF
    with wave.open(str(OUT / 'edited.wav'), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(np.clip(audio * 32768, -32768, 32767).astype('<i2').tobytes())
    override_reader = Reader(SOURCE)
    override_frames = {n: override_reader.at(n) for n in sorted({r[2] for r in OVERRIDES})}
    override_reader.c.release()
    manifest = dict(source=str(SOURCE), source_sha256=EXPECTED, candidate=str(DEST),
                    fps=FPS, frames=cursor, duration=cursor / FPS, removed_seconds=(6184 - cursor) / FPS,
                    cuts=[dict(source_frames=[a, b], source_seconds=[a / FPS, b / FPS], label=l, words=w)
                          for a, b, l, w in CUTS], timeline=spans, joins=joins,
                    picture_overrides=[dict(source_frames=[a, b], use_source_frame=n, reason=r)
                                       for a, b, n, r in OVERRIDES], protected=protected,
                    audio='Original mono 48kHz narration, synchronized picture/audio cuts, 5ms ramps in quiet shoulders. No added pauses or replacement voice.',
                    scope='Six approved redundancy suggestions plus coin-list removal and retaining only Spot/22%. Adjacent approved cuts combined.',
                    source_limitation='One additional H.264 encode from finished v9; no pristine assembly recreated.',
                    retained='Pascal/Fermat history, calculations, knowledge-change insight, dog context/Spot probability, repeat animation, complete standard close.',
                    publication='Review candidate only. No installed course file or website change.')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    cmd = [ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1280x720', '-r', '30',
           '-i', 'pipe:0', '-i', str(OUT / 'edited.wav'), '-map', '0:v', '-map', '1:a',
           '-c:v', 'libx264', '-preset', 'fast', '-crf', '16', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(DEST)]
    encoder = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    rd = Reader(SOURCE)
    count = 0
    for a, b in keeps:
        for n in range(a, b):
            frame = rd.at(n)
            override = next((row for row in OVERRIDES if row[0] <= n < row[1]), None)
            if override:
                frame = override_frames[override[2]]
            encoder.stdin.write(frame.tobytes())
            count += 1
            if count % 1000 == 0:
                print(f'Rendered {count}/{cursor}', flush=True)
    encoder.stdin.close()
    assert encoder.wait() == 0
    rd.c.release()
    assert count == cursor
    assert all(sha(Path(p)) == h for p, h in protected.items())
    manifest['render_sha256'] = sha(DEST)
    manifest['bytes'] = DEST.stat().st_size
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'candidate': str(DEST), 'duration': cursor / FPS,
                      'removed_seconds': (6184 - cursor) / FPS}), flush=True)


if __name__ == '__main__':
    main()
