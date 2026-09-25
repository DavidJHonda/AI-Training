#!/usr/bin/env python3
"""Mute the breath after "hunting for them" (2:01) in the approved Curious & Flexible video.

Run with .video-venv/bin/python after cut_curious_and_flexible_filters.py.
Retains a source backup; video is stream-copied, only the audio is re-encoded.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / 'video-audit/curious-and-flexible-breath-mute'
SOURCE = ROOT / 'archive/curious-and-flexible/curious-and-flexible-before-breath-mute-20260925.mp4'
OUTPUT = AUDIT / 'curious-and-flexible-breath-muted.mp4'
# Speech ends 121.28; the inhale runs to a puff at 122.04-122.10; digital silence follows.
MUTE_START, MUTE_END, FADE = 121.30, 122.14, 0.03

def rms_db(path, start, dur):
    pcm = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-loglevel', 'error',
        '-ss', str(start), '-i', str(path), '-t', str(dur), '-f', 'f32le', '-ac', '1', '-ar', '48000', '-'],
        capture_output=True, check=True).stdout
    s = np.frombuffer(pcm, dtype=np.float32)
    return 20*float(np.log10(max(float(np.sqrt(np.mean(s*s))), 1e-12)))

def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    if not SOURCE.exists():
        shutil.copy2(ROOT / 'course-assets/curious-and-flexible/curious-and-flexible.mp4', SOURCE)
    # Gain ramps to 0 over FADE after MUTE_START and back to 1 over FADE before MUTE_END.
    a, b, f = MUTE_START, MUTE_END, FADE
    gain = (f"if(lt(t,{a}),1,if(lt(t,{a+f}),1-(t-{a})/{f},"
            f"if(lt(t,{b-f}),0,if(lt(t,{b}),(t-{b-f})/{f},1))))")
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-hide_banner', '-loglevel', 'error',
        '-i', str(SOURCE), '-map', '0:v', '-map', '0:a', '-c:v', 'copy',
        '-af', f"volume='{gain}':eval=frame", '-c:a', 'aac', '-b:a', '192k',
        '-movflags', '+faststart', str(OUTPUT)], check=True)
    manifest = {
        'source': str(SOURCE.relative_to(ROOT)),
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'candidate': str(OUTPUT.relative_to(ROOT)),
        'muted_seconds': [MUTE_START, MUTE_END], 'fade_seconds': FADE,
        'breath_rms_dbfs_before': rms_db(SOURCE, MUTE_START+f, MUTE_END-MUTE_START-2*f),
        'breath_rms_dbfs_after': rms_db(OUTPUT, MUTE_START+f, MUTE_END-MUTE_START-2*f),
        'notes': ['Video stream copied; duration and frames unchanged.'],
    }
    (AUDIT/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps(manifest, indent=2))

if __name__ == '__main__':
    main()
