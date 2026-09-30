#!/usr/bin/env python3
"""V6: preserve the approved v5 edit, start the diagram after its inherited text dissolve."""
import hashlib
import json
import subprocess
import sys
import wave
from pathlib import Path

import av
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from make_close_board import close_board_asset, compose_canonical_for_video

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'course-assets/creative-thinking/creative-thinking.mp4'
OUT = ROOT / 'video-audit/creative-thinking-repair-2026-09-30-v6'
DEST = ROOT / 'Prompts/creative-thinking-v6.mp4'
EXPECTED = '7c457ead1ec33f4a3239a3b925e5ba4cd552378cede06927d267ecf6d0cfa55f'
FF = imageio_ffmpeg.get_ffmpeg_exe()
SPANS = [(0, 2930), (3092, 3144), (3168, 5207)]
CUTS = [(2930, 3092), (3144, 3168)]
TOTAL = 5021
CLOSE = 4940
BOUNDARIES = {
    2844: 'corrected-AI-diagram',
    2930: 'cut-similar-answers-and-equalized-baseline',
    2982: 'cut-entirely-picture-continuous',
    3066: 'retimed-missing-angle-to-original-hands',
    4104: 'connect-unrelated-things-cutaway',
    4224: 'return-to-practice-board',
    4754: 'canonical-white-close',
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def writewav(path, samples):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(48000)
        w.writeframes(np.clip(samples, -32768, 32767).astype(np.int16).tobytes())


def main():
    cv2.setNumThreads(2)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'preview').mkdir(exist_ok=True)
    assert not DEST.exists(), 'Never overwrite a review candidate.'
    assert sha(SOURCE) == EXPECTED
    protected = {str(p): sha(p) for p in [SOURCE, ROOT/'lessons/creative-thinking.md',
        *sorted((ROOT/'course-assets/creative-thinking').glob('*.jpg'))]}
    subprocess.run([FF, '-y', '-v', 'error', '-i', str(SOURCE), '-vn', '-ac', '1',
                    '-ar', '48000', '-c:a', 'pcm_s16le', str(OUT/'source.wav')], check=True)
    with wave.open(str(OUT/'source.wav')) as w:
        original = np.frombuffer(w.readframes(w.getnframes()), np.int16).copy()
    parts = [original[s*1600:e*1600].astype(float) for s, e in SPANS]
    # Preserve all audio except the deleted spans and 4 ms shoulders at the two joins.
    ramp = np.linspace(0, 1, 192)
    room = np.resize(original[round(97.68*48000):round(97.73*48000)].astype(float), 192)
    for i in range(len(parts)-1):
        parts[i][-192:] = parts[i][-192:]*(1-ramp) + room*ramp
        parts[i+1][:192] = parts[i+1][:192]*ramp + room*(1-ramp)
    audio = np.concatenate(parts)
    assert len(audio) == TOTAL*1600
    writewav(OUT/'edited.wav', audio)
    writewav(OUT/'join-check.wav', audio[94*48000:108*48000])

    # Retain the missing-angle animation continuously across the short word cut.
    # Cache planar YUV frames so unaffected footage never incurs an RGB round trip.
    donor = {}
    with av.open(str(SOURCE)) as container:
        container.streams.video[0].codec_context.thread_count = 2
        for n, frame in enumerate(container.decode(video=0)):
            if n == 2844:
                paper = frame.to_ndarray(format='bgr24')
            if 3092 <= n < 3372:
                donor[n] = frame.to_ndarray(format='yuv420p').copy()
            if n >= 3372:
                break
    assert len(donor) == 280
    title = Image.fromarray(cv2.cvtColor(paper, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(title)
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf', 32)
    draw.text((640, 92), 'AI gives polished answers', fill=(46, 78, 91), font=font, anchor='mt')
    title = cv2.cvtColor(np.array(title), cv2.COLOR_RGB2BGR)
    compose_canonical_for_video(close_board_asset('creativethinking'), OUT/'close.png', '#ffffff')
    close = cv2.imread(str(OUT/'close.png'))

    proc = subprocess.Popen([FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'yuv420p',
        '-s', '1280x720', '-r', '30', '-i', 'pipe:0', '-i', str(OUT/'edited.wav'),
        '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-profile:v', 'high',
        '-level:v', '3.1', '-crf', '16', '-preset', 'fast', '-threads', '2',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
        str(DEST)], stdin=subprocess.PIPE)
    wants = {f+d for f in BOUNDARIES for d in [-1, 0, 15]} | {2880, 2920, 2995, 4130, 4802, 4952, 5020}
    written = 0
    with av.open(str(SOURCE)) as container:
        container.streams.video[0].codec_context.thread_count = 2
        for n, frame in enumerate(container.decode(video=0)):
            if any(s <= n < e for s, e in CUTS):
                continue
            raw = frame.to_ndarray(format='yuv420p')
            if 2844 <= n < 2930:
                im = frame.to_ndarray(format='bgr24')
                # Exact blank paper from this scene removes the obsolete heading;
                # retain the original diagram's reveal and all other picture content.
                im[82:128, 250:1060] = title[82:128, 250:1060]
                im[530:585, 400:900] = paper[530:585, 400:900]
                raw = av.VideoFrame.from_ndarray(im, format='bgr24').to_ndarray(format='yuv420p')
            elif 2930 <= written < 3066:
                d = 3135 + round((written-2930)*116/135)
                raw = donor[d]
            elif 4290 <= n < 4410:
                raw = donor[3252+n-4290]
            elif n >= CLOSE:
                t = n-CLOSE
                u = min(1., max(0., (t-48)/149))
                z = 1 + .2*u*u*(3-2*u)
                h, w = close.shape[:2]
                cw, ch = round(w/z), round(h/z)
                x, y = (w-cw)//2, (h-ch)//2
                im = cv2.resize(close[y:y+ch, x:x+cw], (1280, 720), interpolation=cv2.INTER_AREA)
                raw = av.VideoFrame.from_ndarray(im, format='bgr24').to_ndarray(format='yuv420p')
            if written in wants:
                im = av.VideoFrame.from_ndarray(raw, format='yuv420p').to_ndarray(format='bgr24')
                cv2.imwrite(str(OUT/'preview'/f'{written:06d}.jpg'), im)
            proc.stdin.write(raw.tobytes())
            written += 1
            if written % 1500 == 0:
                print(f'Rendered {written}/{TOTAL}', flush=True)
    proc.stdin.close()
    assert proc.wait() == 0 and written == TOTAL
    assert all(sha(p) == h for p, h in protected.items())
    manifest = dict(source=str(SOURCE), source_sha256=EXPECTED, candidate=str(DEST),
        candidate_sha256=sha(DEST), source_frames=5207, output_frames=written, fps=30,
        duration=written/30, retained_source_frame_spans=SPANS, cuts_source_frames=CUTS,
        removed_words=['and everyone using the same AI gets similar answers. With the baseline equalized,', 'entirely'],
        edited_sentence='Today, AI gives polished answers in seconds. The professional advantage moves to the person who can notice what is missing, connect ideas from different places, and choose the better direction.',
        audio_join_fades_ms=4, added_pause_frames=0, boundaries=BOUNDARIES,
        illustration=dict(source_frames=[3252,3372], output_frames=[4104,4224], purpose='Connect ideas from different domains'),
        retimed_animation=dict(source_frames=[3135,3252], output_frames=[2930,3066]),
        close=dict(canonical_asset=str(close_board_asset('creativethinking')), output_start=4754, hold_frames=48, push_frames=150, scale=1.2),
        protected_hashes=protected, protected_files_unchanged=True,
        scope='Targeted approved repair; pre-existing long board runs, Macintosh photo, and inherited ring widths remain.',
        listening='Not auditioned; owner listening review required for the two audio joins.')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print('COMPLETE', DEST, flush=True)


if __name__ == '__main__':
    main()
