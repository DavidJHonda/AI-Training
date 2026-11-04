#!/usr/bin/env python3
"""Narrow current-roadmap swap; retain v8's timeline and copy its audio."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import cv2
import imageio_ffmpeg
from editspec_build import Build

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/navigate-opener-roadmap-2026-11-04'
SOURCE = ROOT / 'Prompts/navigate-the-future-opener-v8.mp4'
DEST = ROOT / 'Prompts/navigate-the-future-opener-v10.mp4'
ASSET = ROOT / 'course-assets/navigate-the-future-opener/navigate-the-future-opener-section-map.jpg'
OLD_SPEC = ROOT / 'video-audit/opener-navigate-v5-2026-09-24/build/leg-map.json'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd):
    subprocess.run(list(map(str, cmd)), cwd=ROOT, check=True)


def main():
    assert not DEST.exists(), 'Never overwrite a review candidate'
    assert sha(SOURCE) == 'b5e18774098d38492e47bc32d9352e00acaae96dd0636fa82282c982e3ffe867'
    OUT.mkdir(parents=True, exist_ok=True)
    assert cv2.imread(str(ASSET)).shape[:2] == (789, 1600)
    canvas, cw, ch, ox, oy = Build.compose(SimpleNamespace(out=OUT), ASSET, 'map')
    assert (cw, ch, ox, oy) == (1600, 900, 0, 55)
    spec = json.loads(OLD_SPEC.read_text())
    spec['image'] = str(canvas)
    plan = OUT / 'leg-map.json'
    plan.write_text(json.dumps(spec, indent=2) + '\n')
    leg = OUT / 'leg-map.mkv'
    run([sys.executable, ROOT / 'scripts/video/ken_burns_path.py', plan, leg])
    # v8 begins this shot with seven held frames of the first clean map frame.
    # Preserve that hold, the original 1018-frame camera, and its 141-frame cutaway.
    filters = [
        '[0:v]trim=end_frame=3092,settb=1/30,setpts=N/(30*TB),setsar=1[a]',
        '[1:v]trim=end_frame=456,settb=1/30,setpts=N/(30*TB),tpad=start=7:start_mode=clone,settb=1/30,setpts=N/(30*TB),setsar=1[b]',
        '[0:v]trim=start_frame=3555:end_frame=3696,settb=1/30,setpts=N/(30*TB),setsar=1[c]',
        '[1:v]trim=start_frame=597:end_frame=1018,settb=1/30,setpts=N/(30*TB),setsar=1[d]',
        '[0:v]trim=start_frame=4117:end_frame=4370,settb=1/30,setpts=N/(30*TB),setsar=1[e]',
        '[a][b][c][d][e]concat=n=5:v=1:a=0,format=yuv420p[v]',
    ]
    run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-i', SOURCE, '-i', leg,
         '-filter_complex', ';'.join(filters), '-map', '[v]', '-map', '0:a:0',
         '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-r', '30',
         '-c:a', 'copy', '-movflags', '+faststart', DEST])
    manifest = dict(
        scope='Only replace the two roadmap visual spans with the current canonical board.',
        source=str(SOURCE.relative_to(ROOT)), source_sha256=sha(SOURCE),
        candidate=str(DEST.relative_to(ROOT)), candidate_sha256=sha(DEST),
        asset=str(ASSET.relative_to(ROOT)), asset_sha256=sha(ASSET),
        original_camera_and_rings=str(OLD_SPEC.relative_to(ROOT)),
        canvas_dimensions=[cw, ch], canvas_offset=[ox, oy],
        replacement_frames=[[3092, 3555], [3696, 4117]],
        replacement_seconds=[[3092 / 30, 3555 / 30], [3696 / 30, 4117 / 30]],
        ring_onsets=dict(argument=3247, monsters=3473, personal=3725, banner=4039),
        preserved_cutaway_frames=[3555, 3696], frames=4370, fps=30,
        audio='Original AAC stream copied without re-encoding. Spoken old section title remains.',
        limitations=['One video encode from the surviving finished v8 source.',
                     'Narrow visual repair; no whole-video listening review.',
                     'Review candidate; not installed or published.'])
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(DEST, flush=True)


if __name__ == '__main__':
    main()
