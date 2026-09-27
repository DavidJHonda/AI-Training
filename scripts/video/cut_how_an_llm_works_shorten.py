#!/usr/bin/env python3
"""Remove ten redundant restatement sentences from the shipped How an LLM Works video.

Run with .video-venv/bin/python. Retains a source backup; writes a review candidate.
The live video is replaced only after the candidate is checked.

Each cut removes the same number of frames from picture and sound. Audio cut points sit
inside measured sentence pauses (10 ms RMS below -50 dBFS). Picture cut points normally
match; three are offset so the picture changes on an existing scene boundary:
  4  removes exactly the numerical-network drawing (frames 4675-5004)
  5  leaves the tokens drawing at 198.2 s so Same Word. Different Odds. shows in full
     view for ~1.2 s before the left-card dive (no splice into the zoom)
  9  keeps One Word at a Time up to its natural scene end
  10 removes exactly the training-versus-answering drawing (frames 10766-11200)

The banner highlight on Same Word. Different Odds. (source frame 8475) belonged to the
deleted sentence under cut 8; its surviving frames hold the preceding jelly-ring state.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / 'video-audit/how-an-llm-works-shorten-2026-09-25'
SOURCE = ROOT / 'archive/how-an-llm-works/how-an-llm-works-before-shorten-20260925.mp4'
SOURCE_SHA = '5f3f2674150905c7b14d4ecf3dad2850d361ea5c4a87ff085fe47de2202d83ad'
OUTPUT = AUDIT / 'how-an-llm-works-shortened-v2.mp4'
FPS = 30
ORIGINAL_FRAMES = 11488

# (audio_start_seconds, video_start_frame, removed_frames, deleted sentence)
CUTS = [
    (46.615, 1398, 256, 'This flowchart shows the mechanical loop ... how the model actually learns.'),
    (112.420, 3373, 216, 'This continuous cycle ... is what training means in the context of AI.'),
    (128.705, 3861, 174, "The training process has established this sequence as a high probability pattern ..."),
    (155.833, 4675, 329, 'It is important to note that pattern recognition ... ongoing training loop.'),
    (198.945, 5946, 204, "Answering a prompt is actually an active mathematical calculation ... exact numbers."),
    (226.390, 6792, 111, "They aren't fixed mathematical constants shared by every AI model."),
    (239.290, 7179, 190, 'The model is simply calculating the most likely continuation ...'),
    (282.640, 8479, 209, 'The surrounding context words are the primary variables ...'),
    (339.410, 10187, 251, 'This constant cycle of adding a word ... central engine of text generation.'),
    (358.665, 10766, 434, 'This entire generation process connects ... calculate what comes next.'),
]

# (source_start_frame, source_end_frame, still_frame): hold still_frame over the span.
FREEZES = [(8475, 8479, 8474), (8688, 8701, 8474)]


def keep_ranges(starts, total):
    """Complement of [start, start+length) spans within [0, total)."""
    ranges, cursor = [], 0
    for start, length in starts:
        ranges.append((cursor, start))
        cursor = start + length
    ranges.append((cursor, total))
    return ranges


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    if not SOURCE.exists():
        shutil.copy2(ROOT / 'course-assets/how-an-llm-works/how-an-llm-works.mp4', SOURCE)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
    cap = cv2.VideoCapture(str(SOURCE))
    assert int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) == ORIGINAL_FRAMES
    assert cap.get(cv2.CAP_PROP_FPS) == FPS
    cap.release()
    if OUTPUT.exists():
        raise SystemExit(f'refusing to overwrite {OUTPUT}')

    vkeep = keep_ranges([(v, n) for _, v, n, _ in CUTS], ORIGINAL_FRAMES)
    akeep = keep_ranges([(a, n / FPS) for a, _, n, _ in CUTS], ORIGINAL_FRAMES / FPS)
    parts = []
    vpieces = []
    for s, e in vkeep:
        for fs, fe, still in FREEZES:
            if s <= fs < e:
                assert fe <= e
                vpieces += [(s, fs, None), (fs, fe, still)]
                s = fe
        vpieces.append((s, e, None))
    for i, (s, e, still) in enumerate(vpieces):
        if still is None:
            parts.append(f'[0:v]trim=start_frame={s}:end_frame={e},setpts=PTS-STARTPTS[v{i}]')
        else:
            parts.append(f'[0:v]trim=start_frame={still}:end_frame={still + 1},'
                         f'loop=loop={e - s - 1}:size=1:start=0,setpts=N/{FPS}/TB[v{i}]')
    for i, (s, e) in enumerate(akeep):
        parts.append(f'[0:a]atrim=start={s:.6f}:end={e:.6f},asetpts=PTS-STARTPTS[a{i}]')
    nv, na = len(vpieces), len(akeep)
    parts.append(''.join(f'[v{i}]' for i in range(nv)) + f'concat=n={nv}:v=1:a=0[v]')
    parts.append(''.join(f'[a{i}]' for i in range(na)) + f'concat=n={na}:v=0:a=1[a]')
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg, '-y', '-hide_banner', '-loglevel', 'error', '-i', str(SOURCE),
        '-filter_complex', ';'.join(parts), '-map', '[v]', '-map', '[a]',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-threads', '4',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
        '-movflags', '+faststart', str(OUTPUT)], check=True)

    # Output-time position of each audio join, and RMS across it in the encoded file.
    joins, removed = [], 0.0
    for a, v, frames, sentence in CUTS:
        t = a - removed
        pcm = subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-ss', str(t - .1),
            '-i', str(OUTPUT), '-t', '0.2', '-f', 'f32le', '-ac', '1', '-ar', '44100', '-'],
            capture_output=True, check=True).stdout
        samples = np.frombuffer(pcm, dtype=np.float32)
        rms = float(np.sqrt(np.mean(samples * samples)))
        joins.append({
            'deleted': sentence,
            'source_audio_seconds': [a, round(a + frames / FPS, 3)],
            'source_video_frames_half_open': [v, v + frames],
            'output_join_seconds': round(t, 3),
            'output_video_join_frame': v - round(removed * FPS),
            'seam_rms_dbfs_200ms': round(20 * float(np.log10(max(rms, 1e-12))), 1),
        })
        removed += frames / FPS

    total_removed = sum(c[2] for c in CUTS)
    manifest = {
        'source': str(SOURCE.relative_to(ROOT)),
        'source_sha256': SOURCE_SHA,
        'candidate': str(OUTPUT.relative_to(ROOT)),
        'candidate_sha256': hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        'fps': FPS, 'original_frames': ORIGINAL_FRAMES,
        'removed_frames': total_removed,
        'freezes_source_frames': FREEZES,
        'expected_frames': ORIGINAL_FRAMES - total_removed,
        'duration_seconds': round((ORIGINAL_FRAMES - total_removed) / FPS, 3),
        'cuts': joins,
    }
    (AUDIT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
