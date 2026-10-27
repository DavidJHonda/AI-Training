#!/usr/bin/env python3
"""Replace the shortened Sycophancy board; copy all other video and all audio."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

import av
import cv2
import imageio_ffmpeg
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ken_burns_path as kb

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/flattery-trap-board-v13-2026-10-27'
SRC = ROOT / 'Prompts/flattery-trap-v12.mp4'
DEST = ROOT / 'Prompts/flattery-trap-v13.mp4'
ASSET = ROOT / 'course-assets/flattery-trap/flattery-trap-sycophancy.jpg'
SOURCE_HASH = '216955359bc279aca9097bd3792797c5512ce959ae246edbf78ddca173cc9c1c'
START, END, RING = 4000, 4317, 4152
FRAMES, FPS = 7954, 30
FF = imageio_ffmpeg.get_ffmpeg_exe()


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def prepare():
    OUT.mkdir(parents=True, exist_ok=True)
    assert sha(SRC) == SOURCE_HASH
    board = cv2.imread(str(ASSET))
    assert board.shape[:2] == (479, 1600)
    # Same full-width fit as v12. Only vertical padding changes with board height.
    ref = cv2.imread(str(OUT / 'source-4000.jpg'))
    assert ref is not None
    background = np.median(ref[:30, 30:1250], axis=(0, 1)).astype(np.uint8)
    canvas = np.full((900, 1600, 3), background, np.uint8)
    canvas[210:689] = board
    cv2.imwrite(str(OUT / 'canvas-sycophancy.png'), canvas)
    full = cv2.resize(canvas, (1280, 720), interpolation=cv2.INTER_AREA)
    ringed = full.copy()
    # Complete white response card, measured on the current asset; fixed 4px stroke.
    rect = [40, 127, 1560, 439]
    x0, y0, x1, y1 = rect
    kb.draw_ring(ringed, x0*.8-2, (y0+210)*.8-2,
                 x1*.8+2, (y1+210)*.8+2,
                 kb.hex_bgr('#4f2fc4'), 16*.8+2, kb.ring_px(720))
    cv2.imwrite(str(OUT / 'preview-full.jpg'), full)
    cv2.imwrite(str(OUT / 'preview-highlight.jpg'), ringed)
    return full, ringed, rect


def main():
    full, ringed, rect = prepare()
    if '--preview' in sys.argv:
        return
    assert not DEST.exists(), 'Never overwrite a review candidate'
    asset_hash = sha(ASSET)
    leg = OUT / 'leg-sycophancy.mp4'
    cmd = [FF, '-v', 'error', '-y', '-f', 'rawvideo', '-pixel_format', 'bgr24',
           '-video_size', '1280x720', '-framerate', '30', '-i', '-', '-an',
           '-c:v', 'libx264', '-threads', '2', '-crf', '16', '-preset', 'fast',
           '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level:v', '3.1',
           '-video_track_timescale', '15360', str(leg)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(START, END):
        proc.stdin.write((full if f < RING else ringed).tobytes())
    proc.stdin.close()
    assert proc.wait() == 0

    source = av.open(str(SRC))
    video, audio = source.streams.video[0], source.streams.audio[0]
    packets, keys = [], []
    for p in source.demux(video, audio):
        if p.dts is None:
            continue
        isvideo = p.stream.type == 'video'
        f = round(float(p.pts*p.time_base)*FPS) if isvideo else None
        if isvideo and p.is_keyframe:
            keys.append(f)
        if isvideo and START <= f < END:
            continue
        packets.append((isvideo, p))
    assert START in keys and END in keys, 'Replacement requires complete GOP boundaries'
    replacement = av.open(str(leg))
    rv = replacement.streams.video[0]
    assert rv.time_base == video.time_base
    assert rv.codec_context.extradata == video.codec_context.extradata
    count = 0
    for p in replacement.demux(rv):
        if p.dts is None:
            continue
        p.pts += START*512
        p.dts += START*512
        packets.append((True, p))
        count += 1
    assert count == END-START
    packets.sort(key=lambda row: (row[1].dts*row[1].time_base, not row[0]))
    with av.open(str(DEST), 'w', options={'movflags': '+faststart'}) as output:
        ov = output.add_stream_from_template(video)
        oa = output.add_stream_from_template(audio)
        for isvideo, p in packets:
            p.stream = ov if isvideo else oa
            output.mux(p)
    replacement.close()
    source.close()
    assert sha(SRC) == SOURCE_HASH and sha(ASSET) == asset_hash
    manifest = {
        'scope': 'Current shortened Sycophancy board only. Lesson diff requires no narration cuts.',
        'source': str(SRC), 'source_sha256': SOURCE_HASH,
        'candidate': str(DEST), 'candidate_sha256': sha(DEST),
        'asset': str(ASSET), 'asset_sha256': asset_hash,
        'asset_dimensions': [1600, 479], 'canvas_dimensions': [1600, 900],
        'offset': [0, 210], 'card_bounds_xyxy': rect,
        'source_and_output_span_frames': [START, END],
        'source_and_output_span_seconds': [START/FPS, END/FPS],
        'highlight_start_frame': RING, 'highlight_color': '#4f2fc4', 'ring_px': 4,
        'density': 'compact', 'camera': 'Full board, static, no crop or zoom',
        'frames': FRAMES, 'fps': FPS, 'duration_seconds': FRAMES/FPS,
        'added_pause_seconds': 0, 'audio_edits': [],
        'method': 'Encode one complete-GOP board span; remux every other video packet and every AAC packet unchanged.',
        'source_limitation': 'Original raw rolls unavailable; stable finished v12 used. Unaffected spans are not re-encoded.',
        'boundaries': [[START, 'new-board-in'], [RING, 'response-highlight'], [END, 'original-rollback-scene']],
        'direct_listening_performed': False, 'continuous_playback_performed': False,
        'installed': False, 'published': False,
    }
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
