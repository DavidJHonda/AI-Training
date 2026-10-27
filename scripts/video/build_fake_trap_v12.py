"""Two approved lesson-alignment cuts; retain v11 everywhere else."""
from pathlib import Path
import hashlib
import json
import subprocess

import av
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'video-audit/fake-trap-shortening-2026-10-27'
SOURCE = ROOT/'Prompts/fake-trap-v11.mp4'
DEST = ROOT/'Prompts/fake-trap-v12.mp4'
SOURCE_SHA = '7614d463682dff720a84b84561bb97ac02e0e9eb71192bcfd134bc849b827664'
FPS, SR, SPF, N = 30, 48000, 1600, 7655
CUTS = [(546, 615), (4123, 4414)]
KEEPS = [(0, 546), (615, 4123), (4414, N)]
JOINS = [546, 4054]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    assert sha(SOURCE) == SOURCE_SHA
    assert not DEST.exists(), 'Never overwrite a candidate.'
    OUT.mkdir(exist_ok=True)
    protected = {str(p): sha(p) for p in [SOURCE, ROOT/'index.html',
        ROOT/'lessons/fake-trap.md', *sorted((ROOT/'course-assets/fake-trap').glob('*'))] if p.is_file()}
    with av.open(str(SOURCE)) as c:
        assert c.streams.audio[0].rate == SR
        channels = c.streams.audio[0].channels
    filters = []
    for i, (a, b) in enumerate(KEEPS):
        filters += [f'[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v{i}]',
            f'[0:a]atrim=start_sample={a*SPF}:end_sample={b*SPF},asetpts=PTS-STARTPTS[a{i}]']
    filters.append('[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]')
    command = [imageio_ffmpeg.get_ffmpeg_exe(), '-n', '-v', 'warning', '-i', str(SOURCE),
        '-filter_complex', ';'.join(filters), '-map', '[v]', '-map', '[a]',
        '-c:v', 'libx264', '-crf', '16', '-preset', 'fast', '-threads', '4',
        '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '192k',
        '-movflags', '+faststart', '-video_track_timescale', '15360', str(DEST)]
    subprocess.run(command, check=True)
    assert all(sha(p) == h for p, h in protected.items())
    manifest = dict(source=str(SOURCE), source_sha256=SOURCE_SHA, candidate=str(DEST),
        candidate_sha256=sha(DEST), fps=FPS, frames=7295, duration_seconds=7295/FPS,
        removed_seconds=12, channels=channels,
        approval='Go ahead and make those two cuts. Keep the detector explanation and the earlier shortening decisions, then check the joins.',
        cuts=[dict(source_frames=[a,b], source_seconds=[a/FPS,b/FPS], description=label)
            for (a,b),label in zip(CUTS, ['Imagine how this plays out.',
                'To find the truth… Check the source, not the pixels… Shift your focus… and its board'])],
        keeps=KEEPS, output_join_frames=JOINS, output_join_seconds=[n/FPS for n in JOINS],
        removed_board_source_frames=[4123,4414], added_pauses=[], audio_processing='Cuts only; no fades, gain, speed changes, or added silence.',
        source_limitation='Finished v11 is the available source; video and audio encoded once for this edit.',
        board_treatment='Remove Check the Source, Not the Pixels completely. Preserve all remaining framing, rings, camera motion, scenes and standard close.',
        protected=protected, status='Review candidate; not installed or published.', command=command)
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:manifest[k] for k in ['candidate','frames','duration_seconds','output_join_seconds']},indent=2))


if __name__ == '__main__':
    main()
