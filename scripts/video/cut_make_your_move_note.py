#!/usr/bin/env python3
"""Remove the Nate and Luke note from the approved Make Your Move video.

Run with .video-venv/bin/python. Retains a source backup; writes a review candidate.
The live video is replaced only after the candidate is checked.
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
AUDIT = ROOT / 'video-audit/make-your-move-note-cut'
SOURCE = ROOT / 'archive/make-your-move/make-your-move-before-note-cut-20260925.mp4'
OUTPUT = AUDIT / 'make-your-move-without-note.mp4'
FPS = 30
CUT_START, CUT_END, ORIGINAL_FRAMES = 1074, 1905, 9877

def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    if not SOURCE.exists():
        shutil.copy2(ROOT / 'course-assets/make-your-move/make-your-move.mp4', SOURCE)
    cap = cv2.VideoCapture(str(SOURCE))
    assert int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) == ORIGINAL_FRAMES
    assert cap.get(cv2.CAP_PROP_FPS) == FPS
    cap.release()
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    start, end = CUT_START/FPS, CUT_END/FPS
    graph = (
        f'[0:v]trim=end_frame={CUT_START},setpts=PTS-STARTPTS[v0];'
        f'[0:a]atrim=end={start},asetpts=PTS-STARTPTS[a0];'
        f'[0:v]trim=start_frame={CUT_END},setpts=PTS-STARTPTS[v1];'
        f'[0:a]atrim=start={end}:end={ORIGINAL_FRAMES/FPS},asetpts=PTS-STARTPTS[a1];'
        '[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]'
    )
    subprocess.run([ffmpeg, '-y', '-hide_banner', '-loglevel', 'error', '-i', str(SOURCE),
        '-filter_complex', graph, '-map', '[v]', '-map', '[a]',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-threads', '4',
        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
        '-movflags', '+faststart', str(OUTPUT)], check=True)
    # Check amplitude across the new join in the encoded output.
    pcm = subprocess.run([ffmpeg, '-hide_banner', '-loglevel', 'error', '-ss', str(start-.1),
        '-i', str(OUTPUT), '-t', '0.2', '-f', 'f32le', '-ac', '1', '-ar', '44100', '-'],
        capture_output=True, check=True).stdout
    samples = np.frombuffer(pcm, dtype=np.float32)
    rms = float(np.sqrt(np.mean(samples*samples)))
    manifest = {
        'source': str(SOURCE.relative_to(ROOT)),
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'candidate': str(OUTPUT.relative_to(ROOT)),
        'fps': FPS, 'original_frames': ORIGINAL_FRAMES,
        'removed_frames_half_open': [CUT_START, CUT_END],
        'removed_seconds': [start, end],
        'expected_frames': ORIGINAL_FRAMES-(CUT_END-CUT_START),
        'duration_seconds': (ORIGINAL_FRAMES-(CUT_END-CUT_START))/FPS,
        'seam_rms_dbfs_200ms': 20*float(np.log10(max(rms,1e-12))),
        'notes': ['Nate and Luke note scene (0:35.80-1:03.50) removed at its scene cuts.',
                  '"...put those skills to work in the real world." joins "When thinking about how AI will change careers".'],
    }
    (AUDIT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))

if __name__ == '__main__':
    main()
