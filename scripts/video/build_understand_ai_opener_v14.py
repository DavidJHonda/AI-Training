#!/usr/bin/env python3
"""Narrow roadmap update and removal of the retired math-workload promise."""
from pathlib import Path
import hashlib
import json
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np

import build_understand_ai_opener_v12 as board_renderer
from editspec_build import Build

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Prompts/understand-ai-opener-v13.mp4'
EXPECTED = 'e914ab971a630018a2c92edb67d19ddfb4a97c38f52cfbee6194ef2975e77f79'
ASSET = ROOT / 'course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg'
OUT = ROOT / 'video-audit/understand-ai-opener-roadmap-2026-10-22'
DEST = ROOT / 'Prompts/understand-ai-opener-v14.mp4'
FPS, TOTAL, SR = 30, 4441, 48000
CUT_START, CUT_END = 4106, 4166
MAP_START, MAP_END = 2423, 4174
BREAK_START, BREAK_END = 3235, 3561


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare_states():
    build = Build(ROOT, SOURCE, OUT, DEST, protected=[ASSET])
    canvas, cw, ch, ox, oy = build.compose(ASSET, 'map')
    assert (cw, ch, ox, oy) == (2096, 1180, 248, 44)
    spec = json.loads((ROOT / 'video-audit/understand-ai-opener-repair-2026-09-27-v12/leg-map.json').read_text())
    spec['image'] = str(canvas)
    spec['provenance']['sha256'] = sha(ASSET)
    (OUT / 'leg-map.json').write_text(json.dumps(spec, indent=2) + '\n')
    board_renderer.OUT = OUT
    return board_renderer.render_states(spec, 'map')


def main():
    assert sha(SOURCE) == EXPECTED
    assert not DEST.exists(), 'Never overwrite a review candidate.'
    OUT.mkdir(parents=True, exist_ok=True)
    states = prepare_states()
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    # Keep the source mono channel and sample rate. The only audio change is
    # the two-second cut and a 5 ms blend between quiet handles at its seam.
    raw = subprocess.check_output([ff, '-v', 'error', '-i', str(SOURCE), '-vn',
        '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'])
    original = np.frombuffer(raw, dtype=np.float32).reshape(-1, 1)
    a, b = CUT_START * SR // FPS, CUT_END * SR // FPS
    edited = np.concatenate([original[:a], original[b:]])
    fade = SR // 200
    mix = np.linspace(0, 1, fade, dtype=np.float32)[:, None]
    edited[a-fade:a] = original[a-fade:a]*(1-mix) + original[b-fade:b]*mix
    output_frames = TOTAL - (CUT_END-CUT_START)
    edited = edited[:output_frames*SR//FPS]
    audio_path = OUT / 'edited-audio.f32'
    edited.astype('<f4').tofile(audio_path)
    command = [ff, '-n', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', '1280x720', '-r', str(FPS), '-i', 'pipe:0', '-f', 'f32le',
        '-ar', str(SR), '-ac', '1', '-i', str(audio_path), '-map', '0:v:0',
        '-map', '1:a:0', '-c:v', 'libx264', '-crf', '16', '-preset', 'fast',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
        '-movflags', '+faststart', str(DEST)]
    manifest = dict(scope='User-authorized narrow repair; review candidate, not shipped.',
        approval='Fix the video too. Remove that clause and replace the roadmap with the updated version.',
        source=str(SOURCE), source_sha256=EXPECTED, output=str(DEST),
        asset=str(ASSET), asset_sha256=sha(ASSET), fps=FPS,
        source_frames=TOTAL, output_frames=output_frames, duration=output_frames/FPS,
        cut_source_frames=[CUT_START, CUT_END],
        cut_source_seconds=[CUT_START/FPS, CUT_END/FPS],
        removed_words='and just how much math goes into it.',
        audio='Mono 48 kHz; two-second cut; 5 ms quiet-handle blend; AAC re-encode.',
        board_plan=dict(title='Understand AI', density='compact', camera='Existing static full view',
            highlighting='Existing five row onsets and fixed 4 px outlines',
            source_spans=[[MAP_START, BREAK_START], [BREAK_END, MAP_END]],
            output_spans=[[MAP_START, BREAK_START], [BREAK_END, MAP_END-60]],
            animation_break='Existing text -> tokens -> numbers animation retained, frames 3235–3560'),
        boundaries=[dict(frame=MAP_START, label='updated-map-entry'),
                    dict(frame=BREAK_START, label='map-to-token-animation'),
                    dict(frame=BREAK_END, label='token-animation-to-map'),
                    dict(frame=CUT_START, label='removed-clause-audio-seam'),
                    dict(frame=MAP_END-60, label='map-to-preserved-close')],
        limitations=['Uses the existing finished v13; original raw generation is unavailable.',
                    'Retained picture and audio re-encoded once.',
                    'No new full audiovisual review or real-time listening claimed.'],
        encode_command=command)
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    proc = subprocess.Popen(command, stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(str(SOURCE))
    count = written = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if not CUT_START <= count < CUT_END:
            if MAP_START <= count < MAP_END and not BREAK_START <= count < BREAK_END:
                frame = next(im for s, e, im in states if s <= count-MAP_START < e)
            proc.stdin.write(frame.tobytes())
            written += 1
        count += 1
        if count % 900 == 0:
            print(f'Decoded {count}/{TOTAL}; wrote {written} frames', flush=True)
    cap.release()
    proc.stdin.close()
    assert proc.wait() == 0
    assert (count, written) == (TOTAL, output_frames)
    assert sha(SOURCE) == EXPECTED
    assert sha(ASSET) == manifest['asset_sha256']
    manifest['render_sha256'] = sha(DEST)
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    audio_path.unlink()
    print(DEST, flush=True)


if __name__ == '__main__':
    cv2.setNumThreads(1)
    main()
