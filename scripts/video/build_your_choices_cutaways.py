#!/usr/bin/env python3
"""Your Choices: break the two board runs with Notebook drawings from the 2026-09-26 rolls (Edit Spec 8b).

David, 2026-09-26: "The live video shows boards only from :40 to 2:22. What I want is some graphics we can use
during some of that time, to make the videos more engaging." Plan approved the same day ("build it"): six
cutaways from Prompts/your-choices-1.mp4 and -2.mp4 under the live narration they were drawn for, hard cuts,
board treatment and rings untouched (they are baked into the live file), audio packet-copied.

Visual-only retrofit on the live file (the 2026-09-25 age-rules cut): every output frame is the live frame
except inside the six spans below, which take donor frames (corner mark cleaned). One re-encode.

Usage:
  .video-venv/bin/python scripts/video/build_your_choices_cutaways.py
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import cv2
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from gemini_mark import clean_frame, glyph_mask  # noqa: E402

FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
W, H = 1280, 720
LIVE = ROOT / 'course-assets/your-choices/your-choices.mp4'
ROLL1 = ROOT / 'Prompts/your-choices-1.mp4'
ROLL2 = ROOT / 'Prompts/your-choices-2.mp4'
AUDIT = ROOT / 'video-audit/your-choices-cutaways-2026-09-26'
DEST = ROOT / 'Prompts/your-choices-cutaways.mp4'

# Research panel of Roll 2's Reasoning/Research diagram: 16:9 window clear of the Reasoning panel
# (its right border is at x 604) and of the corner mark.
RESEARCH_CROP = (617, 260, 1257, 620)

# Output frames are live frames (half-open). src_end is exclusive; frames past it hold src_end - 1.
# Onsets: faster-whisper base.en word timestamps on the live file (live frame = t * 30.006).
CUTS = [
    dict(label='dials', out=(1218, 1292), src=ROLL2, src_start=584, src_end=658,
         narration='0:40.6 "Let\'s look at the first two configuration choices" (board returns 2.8 s before the Which App? ring)'),
    dict(label='monitor', out=(1489, 1668), src=ROLL2, src_start=2320, src_end=2517,
         narration='0:49.6 "Choose the app that is available to you and naturally fits the tools and workflows you use the most."'),
    dict(label='model-picker', out=(2128, 2267), src=ROLL1, src_start=3248, src_end=3388,
         narration='1:10.9 "Some apps offer a family of models, giving you a range of processing power to select from."'),
    dict(label='advanced-work', out=(3229, 3435), src=ROLL2, src_start=756, src_end=966,
         narration='1:47.6 "You want to dial up this setting for math, code, planning, and any problem that requires distinct sequential steps."'),
    dict(label='routine', out=(3435, 3549), src=ROLL2, src_start=658, src_end=754,
         narration='1:54.5 "Keep this at the default setting for routine, straightforward work" (last 18 frames hold)'),
    dict(label='research-sources', out=(3851, 4065), src=ROLL2, src_start=1232, src_end=1376, crop=RESEARCH_CROP,
         narration='2:08.4 "searches external data, compares various sources against each other, and returns a formally cited report." '
                   '(Research half of the diagram; last 70 frames hold)'),
]


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def payload_hash(path: Path, stream: str = 'a') -> str:
    data = subprocess.check_output([FF, '-v', 'error', '-i', str(path), '-map', f'0:{stream}', '-c', 'copy', '-f', 'data', '-'])
    return hashlib.sha256(data).hexdigest()


def read_frames(path: Path, wanted: set[int]) -> dict[int, 'cv2.Mat']:
    """Sequential decode (CAP_PROP seeks are unreliable on these files)."""
    cap, out, i = cv2.VideoCapture(str(path)), {}, -1
    last = max(wanted)
    while i < last:
        ok, im = cap.read()
        assert ok, (path, i + 1)
        i += 1
        if i in wanted:
            out[i] = im
    cap.release()
    return out


def learn_mask(path: Path):
    cap, samples, i = cv2.VideoCapture(str(path)), [], -1
    while True:
        ok, im = cap.read()
        if not ok:
            break
        i += 1
        if i % 15 == 0:
            samples.append(im)
    cap.release()
    return glyph_mask(samples)


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    assert not DEST.exists(), f'{DEST} exists; version-suffix a rebuild instead of overwriting'
    live_sha = sha(LIVE)
    hashes = {str(p): sha(p) for p in (ROLL1, ROLL2)}

    spans = sorted(c['out'] for c in CUTS)
    assert all(a[1] <= b[0] for a, b in zip(spans, spans[1:])), 'cutaways overlap'

    # Donor frames, corner mark cleaned with each roll's own glyph mask.
    donor, counts = {}, {}
    for roll in (ROLL1, ROLL2):
        cuts = [c for c in CUTS if c['src'] == roll]
        wanted = {f for c in cuts for f in range(c['src_start'], c['src_end'])}
        frames = read_frames(roll, wanted)
        mask = learn_mask(roll)
        for c in cuts:
            seq, tally = [], {'clone': 0, 'inpaint': 0, 'declined': 0}
            for f in range(c['src_start'], c['src_end']):
                im, how = clean_frame(frames[f], mask)
                tally[how or 'declined'] += 1
                if 'crop' in c:
                    x0, y0, x1, y1 = c['crop']
                    im = cv2.resize(im[y0:y1, x0:x1], (W, H), interpolation=cv2.INTER_LANCZOS4)
                seq.append(im)
            donor[c['label']], counts[c['label']] = seq, tally

    by_frame = {}
    for c in CUTS:
        seq = donor[c['label']]
        for k, f in enumerate(range(*c['out'])):
            by_frame[f] = seq[min(k, len(seq) - 1)]

    # One pass: live frames, donor frames inside the spans; live audio packet-copied.
    tmp = AUDIT / 'video-only.mkv'
    tmp.unlink(missing_ok=True)
    p = subprocess.Popen([FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0',
                          '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '3.1', '-crf', '16', '-preset', 'fast',
                          '-pix_fmt', 'yuv420p', str(tmp)], stdin=subprocess.PIPE)
    cap, total = cv2.VideoCapture(str(LIVE)), 0
    while True:
        ok, im = cap.read()
        if not ok:
            break
        p.stdin.write(by_frame.get(total, im).tobytes())
        total += 1
    cap.release()
    p.stdin.close()
    assert p.wait() == 0
    assert max(c['out'][1] for c in CUTS) <= total
    subprocess.run([FF, '-v', 'error', '-i', str(tmp), '-i', str(LIVE), '-map', '0:v', '-map', '1:a', '-c', 'copy',
                    '-movflags', '+faststart', str(DEST)], check=True)
    tmp.unlink()

    # Verify the encoded candidate.
    cap, frames = cv2.VideoCapture(str(DEST)), 0
    while cap.grab():
        frames += 1
    cap.release()
    audio_identical = payload_hash(LIVE) == payload_hash(DEST)
    assert frames == total, (frames, total)
    assert audio_identical
    assert sha(LIVE) == live_sha and all(sha(k) == v for k, v in hashes.items())

    board_runs = []
    edges = [1218] + [e for s in spans for e in s] + [4309]   # live board span: 0:40.6 -> close at 2:23.6
    for a, b in zip(edges[::2], edges[1::2]):
        if b > a:
            board_runs.append(dict(start_s=round(a / 30.006, 2), end_s=round(b / 30.006, 2), seconds=round((b - a) / 30.006, 1)))
    manifest = {
        'candidate': str(DEST), 'candidate_sha256': sha(DEST), 'live': str(LIVE), 'live_sha256': live_sha,
        'donors': hashes, 'decoded_frames': frames, 'audio_packets_identical': audio_identical,
        'cutaways': [dict(label=c['label'], out_frames=list(c['out']),
                          out_seconds=[round(c['out'][0] / 30.006, 2), round(c['out'][1] / 30.006, 2)],
                          source=str(c['src']), source_frames=[c['src_start'], c['src_end']],
                          held_frames=max(0, (c['out'][1] - c['out'][0]) - (c['src_end'] - c['src_start'])),
                          crop=c.get('crop'), corner_mark=counts[c['label']], narration=c['narration']) for c in CUTS],
        'board_runs_after': board_runs,
        'scope': 'visual-only; live audio packet-copied; rings and boards as shipped',
    }
    (AUDIT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')

    bounds = []
    for c in CUTS:
        bounds += ['--boundary', f"{c['out'][0]}:to-{c['label']}"]
        if c['out'][1] not in {d['out'][0] for d in CUTS}:
            bounds += ['--boundary', f"{c['out'][1]}:{c['label']}-to-board"]
    guard = subprocess.run([sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST), *bounds,
                            '--outdir', str(AUDIT / 'transitions')])
    print('COMPLETE', DEST, 'frames', frames, 'audio identical', audio_identical, 'guard', guard.returncode, flush=True)
    print(json.dumps(counts), json.dumps(board_runs))


if __name__ == '__main__':
    main()
