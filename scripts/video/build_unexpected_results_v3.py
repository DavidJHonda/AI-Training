#!/usr/bin/env python3
"""Approved label-only repair; preserve every original AAC packet and untouched GOP."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

import av
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/unexpected-results-labels-2026-09-30-v3'
SRC = ROOT / 'course-assets/unexpected-results/unexpected-results.mp4'
DEST = ROOT / 'Prompts/unexpected-results-v3.mp4'
EXPECTED = '1aadfdf5f509be580e4ceb70789a52da017474a1c9cda00b2be6dc0b12a5730a'
START, END = 972, 1596
FF = imageio_ffmpeg.get_ffmpeg_exe()
cv2.setNumThreads(1)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def frames(path, stop=None):
    with av.open(str(path)) as c:
        c.streams.video[0].codec_context.thread_count = 1
        for n, frame in enumerate(c.decode(video=0)):
            if stop is not None and n >= stop:
                break
            yield n, frame.to_ndarray(format='bgr24')


class Labels:
    def __init__(self, ledger, blank, breeding):
        self.ledger_rois = [(322, 123, 713, 153), (858, 124, 980, 153)]
        self.ledger_mask = np.zeros((720, 1280), np.uint8)
        for x0, y0, x1, y1 in self.ledger_rois:
            piece = ledger[y0:y1, x0:x1]
            # Dark handwriting only: preserve the green check behind the date.
            ink = (piece.max(axis=2) < 175).astype(np.uint8) * 255
            self.ledger_mask[y0:y1, x0:x1] = cv2.dilate(ink, np.ones((3, 3), np.uint8))

        self.breeding = breeding
        self.blank = blank
        self.box = (255, 468, 450, 519)
        x0, y0, x1, y1 = self.box
        mask = np.zeros((720, 1280), np.uint8)
        old = breeding[y0:y1, x0:x1]
        ink = (old.min(axis=2) < 185).astype(np.uint8) * 255
        mask[y0:y1, x0:x1] = cv2.dilate(ink, np.ones((3, 3), np.uint8))
        self.glyph_mask = mask
        clean = cv2.inpaint(breeding, mask, 3, cv2.INPAINT_TELEA)
        im = Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB))
        d = ImageDraw.Draw(im)
        bold = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 19)
        regular = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 18)
        d.text((263, 470), 'Can survive', font=bold, fill=(87, 83, 14))
        d.text((263, 495), 'Can keep breeding', font=regular, fill=(85, 91, 86))
        edited = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        self.text_delta = edited.astype(np.float32) - clean.astype(np.float32)
        # Estimate source fade from original glyph pixels against pre-reveal paper.
        ys, xs = np.where(mask > 0)
        self.ys, self.xs = ys, xs
        self.base = blank[ys, xs].astype(np.float32)
        self.full_delta = breeding[ys, xs].astype(np.float32) - self.base
        self.denominator = float((self.full_delta ** 2).sum())
        self.opacity_log = []
        cv2.imwrite(str(OUT / 'breeding-corrected-reference.png'), edited)
        cv2.imwrite(str(OUT / 'ledger-glyph-mask.png'), self.ledger_mask)
        cv2.imwrite(str(OUT / 'breeding-glyph-mask.png'), mask)

    def render(self, frame, n):
        if 972 <= n < 1205:
            result = cv2.inpaint(frame, self.ledger_mask, 3, cv2.INPAINT_TELEA)
            im = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
            d = ImageDraw.Draw(im)
            font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf', 26)
            datefont = ImageFont.truetype('/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf', 21)
            d.text((326, 124), 'Rat tails collected', font=font, fill=(43, 43, 34))
            d.text((861, 127), 'Hanoi, 1902', font=datefont, fill=(43, 43, 34))
            return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        if 1425 <= n < 1596:
            now = frame[self.ys, self.xs].astype(np.float32) - self.base
            alpha = float(np.clip((now * self.full_delta).sum() / self.denominator, 0, 1))
            if alpha < 0.025:
                alpha = 0.0
            self.opacity_log.append({'frame': n, 'opacity': round(alpha, 5)})
            if not alpha:
                return frame
            # Remove source glyphs on each actual frame: the source text and
            # box do not have perfectly identical fade curves. A single static
            # delta leaves pale traces during the exit dissolve.
            clean = cv2.inpaint(frame, self.glyph_mask, 3, cv2.INPAINT_TELEA)
            return np.clip(np.rint(clean.astype(np.float32) + self.text_delta * alpha), 0, 255).astype(np.uint8)
        return frame


def prepare():
    OUT.mkdir(exist_ok=True)
    assert sha(SRC) == EXPECTED, 'Published source changed; do not rebuild against another release'
    wanted = {972, 1080, 1204, 1425, 1434, 1440, 1450, 1455, 1470, 1500, 1560, 1590, 1595}
    samples = {n: im for n, im in frames(SRC, END) if n in wanted}
    labels = Labels(samples[1080], samples[1425], samples[1560])
    for n, im in samples.items():
        cv2.imwrite(str(OUT / f'preview-{n:05}.png'), labels.render(im, n))
    labels.opacity_log = []
    return labels


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--preview', action='store_true')
    args = ap.parse_args()
    labels = prepare()
    if args.preview:
        return
    assert not DEST.exists(), 'Never overwrite a review candidate'
    protected = {str(p): sha(p) for p in [SRC, ROOT / 'lessons/unexpected-results.md',
                 *sorted(SRC.parent.glob('*.jpg'))]}
    leg = OUT / 'leg-labels.mp4'
    cmd = [FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pixel_format', 'bgr24',
           '-video_size', '1280x720', '-framerate', '30', '-i', '-', '-an',
           '-c:v', 'libx264', '-threads', '2', '-crf', '18', '-preset', 'medium',
           '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level:v', '3.1',
           '-force_key_frames', '7.766666667,16.1', '-video_track_timescale', '15360', str(leg)]
    with (OUT / 'encode.log').open('w') as log:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=log)
        for n, im in frames(SRC, END):
            if n >= START:
                proc.stdin.write(labels.render(im, n).tobytes())
        proc.stdin.close()
        assert proc.wait() == 0
    print('Changed section encoded', flush=True)

    source = av.open(str(SRC))
    video, audio = source.streams.video[0], source.streams.audio[0]
    packets, keys = [], []
    for p in source.demux(video, audio):
        if p.dts is None:
            continue
        isvideo = p.stream.type == 'video'
        f = round(float(p.pts * p.time_base) * 30) if isvideo else None
        if isvideo and p.is_keyframe:
            keys.append(f)
        if isvideo and START <= f < END:
            continue
        packets.append((isvideo, p))
    assert START in keys and END in keys
    replacement = av.open(str(leg))
    stream = replacement.streams.video[0]
    assert stream.time_base == video.time_base
    assert stream.codec_context.extradata == video.codec_context.extradata, (
        stream.codec_context.extradata.hex(), video.codec_context.extradata.hex())
    count = 0
    for p in replacement.demux(stream):
        if p.dts is None:
            continue
        p.pts += START * 512
        p.dts += START * 512
        packets.append((True, p))
        count += 1
    assert count == END - START
    packets.sort(key=lambda x: (x[1].dts * x[1].time_base, not x[0]))
    with av.open(str(DEST), 'w', options={'movflags': '+faststart'}) as output:
        ov = output.add_stream_from_template(video)
        oa = output.add_stream_from_template(audio)
        for isvideo, packet in packets:
            packet.stream = ov if isvideo else oa
            output.mux(packet)
    manifest = dict(
        scope='Approved two visual label corrections; no narration, pause, board, or timing changes.',
        source=str(SRC), source_sha256=EXPECTED, candidate=str(DEST), candidate_sha256=sha(DEST),
        source_limitation='Raw generations unavailable; changed GOPs encoded once from published v2.',
        method='Re-encode frames 972–1595 inclusive. Remux all other video packets and all AAC packets unchanged.',
        fps=30, frames=7172, duration=7172 / 30,
        encoded_span=[START, END],
        label_changes=[dict(frames=[972, 1205], old='GOVERNMENT LEDGER – Q4 RESULTS / 12/04/2023',
                            new='Rat tails collected / Hanoi, 1902'),
                       dict(frames=[1425, 1596], old='Full lifespan / Survives tail loss intact',
                            new='Can survive / Can keep breeding',
                            animation='Measured original text opacity; retain source fade-in and fade-out.')],
        boundaries=[dict(frame=f, label=l) for f, l in [(972, 'ledger-in'), (1205, 'ledger-out'),
                    (1425, 'breeding-label-fade'), (1596, 'breeding-out')]],
        codec_extradata_identical=True, protected_hashes=protected,
        status='Review candidate only; not installed, committed, or published.')
    assert all(sha(p) == h for p, h in protected.items())
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (OUT / 'label-opacity.json').write_text(json.dumps(labels.opacity_log, indent=2) + '\n')
    print(DEST, flush=True)


if __name__ == '__main__':
    main()
