#!/usr/bin/env python3
"""Remove the spoken retired title, retaining the approved current roadmap."""
import json
import subprocess
import numpy as np
from build_navigate_opener_v10 import ROOT, SOURCE, ASSET, FFMPEG, sha, run

OUT = ROOT / 'video-audit/navigate-opener-title-cut-2026-11-04'
DEST = ROOT / 'Prompts/navigate-the-future-opener-v11.mp4'
BASE = ROOT / 'Prompts/navigate-the-future-opener-v10.mp4'
LEG = ROOT / 'video-audit/navigate-opener-roadmap-2026-11-04/leg-map.mkv'
A, B, TOTAL = 3189, 3234, 4370
SR, SPF = 48000, 1600


def main():
    assert not DEST.exists(), 'Never overwrite an existing candidate'
    assert sha(SOURCE) == 'b5e18774098d38492e47bc32d9352e00acaae96dd0636fa82282c982e3ffe867'
    assert sha(BASE) == 'af48a28fee2ab3cb66b25a0b980a8ec267d234cd1086091ff4de97010ea66500'
    assert sha(ASSET) == 'b2f455c16b2d25d1e2bd5117b4b3ca9a8520af16c50b6b4958b2821370e9227b'
    OUT.mkdir(exist_ok=True)
    raw = subprocess.check_output([FFMPEG, '-v', 'error', '-i', str(SOURCE),
                                   '-vn', '-ar', str(SR), '-ac', '2', '-f', 'f32le', '-'])
    pcm = np.frombuffer(raw, dtype='<f4').reshape(-1, 2)
    before, after = pcm[:A * SPF].copy(), pcm[B * SPF:TOTAL * SPF].copy()
    fade = 240  # 5 ms, entirely within the measured quiet handles.
    before[-fade:] *= np.linspace(1, 0, fade)[:, None]
    after[:fade] *= np.linspace(0, 1, fade)[:, None]
    audio = OUT / 'edited-audio.f32'
    np.concatenate([before, after]).astype('<f4').tofile(audio)
    # Reassemble v10 from the v8 source and its lossless map leg, then apply
    # the exact same 45-frame cut to picture and audio. Only one video encode.
    filters = [
        '[0:v]trim=end_frame=3092,settb=1/30,setpts=N/(30*TB),setsar=1[a]',
        '[1:v]trim=end_frame=456,settb=1/30,setpts=N/(30*TB),tpad=start=7:start_mode=clone,settb=1/30,setpts=N/(30*TB),setsar=1[b]',
        '[0:v]trim=start_frame=3555:end_frame=3696,settb=1/30,setpts=N/(30*TB),setsar=1[c]',
        '[1:v]trim=start_frame=597:end_frame=1018,settb=1/30,setpts=N/(30*TB),setsar=1[d]',
        '[0:v]trim=start_frame=4117:end_frame=4370,settb=1/30,setpts=N/(30*TB),setsar=1[e]',
        '[a][b][c][d][e]concat=n=5:v=1:a=0,split=2[pre][post]',
        f'[pre]trim=end_frame={A},settb=1/30,setpts=N/(30*TB)[p]',
        f'[post]trim=start_frame={B},settb=1/30,setpts=N/(30*TB)[q]',
        '[p][q]concat=n=2:v=1:a=0,format=yuv420p[v]',
    ]
    run([FFMPEG, '-hide_banner', '-loglevel', 'error', '-i', SOURCE, '-i', LEG,
         '-f', 'f32le', '-ar', SR, '-ac', 2, '-i', audio,
         '-filter_complex', ';'.join(filters), '-map', '[v]', '-map', '2:a:0',
         '-c:v', 'libx264', '-crf', 18, '-preset', 'medium', '-r', 30,
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', DEST])
    manifest = dict(scope='Remove only the spoken words Embrace the Future, preserving the current roadmap repair.',
                    source=str(SOURCE.relative_to(ROOT)), source_sha256=sha(SOURCE),
                    prior_candidate=str(BASE.relative_to(ROOT)), prior_candidate_sha256=sha(BASE),
                    map_leg=str(LEG.relative_to(ROOT)), map_leg_sha256=sha(LEG),
                    candidate=str(DEST.relative_to(ROOT)), candidate_sha256=sha(DEST),
                    cut_source_frames=[A, B], cut_source_seconds=[A / 30, B / 30],
                    removed_seconds=(B - A) / 30, output_frames=TOTAL - (B - A), fps=30,
                    sentence='This roadmap shows what we’ll explore in this section.',
                    quiet_handles_seconds=[[106.195292, 106.457562], [107.631187, 108.209437]],
                    resulting_gap_seconds=(A / 30 - 106.195292) + (108.209437 - B / 30),
                    ring_onsets=dict(argument=3202, monsters=3428, personal=3680, banner=3994),
                    cutaway_frames=[3510,3651], close_start_frame=4072,
                    audio='Frame-aligned cut; 5 ms fades in quiet handles; one AAC encode, no level adjustment.',
                    status='Review candidate, not installed or published.')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    run([FFMPEG, '-v', 'error', '-ss', 103, '-i', DEST, '-t', 7,
         '-vn', '-c:a', 'pcm_s16le', OUT / 'after.wav'])
    print(DEST)


if __name__ == '__main__':
    main()
