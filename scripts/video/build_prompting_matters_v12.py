#!/usr/bin/env python3
"""Remove the approved four-qualities recap; retain all other source content."""
from pathlib import Path
import hashlib
import json
import subprocess
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Prompts/prompting-matters-recap-source-20261026.mp4'
DEST = ROOT / 'Prompts/prompting-matters-v12.mp4'
OUT = ROOT / 'video-audit/prompting-matters-recap-cut-2026-10-26'
SOURCE_SHA = '0c3e63b271877b449c6aca57bea490a9ddbf5c6bf7c76e5236ab33cdc2986d1f'
FPS, FRAMES, CUT_START, CUT_END = 30, 6936, 797, 1480


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    assert sha(SOURCE) == SOURCE_SHA, 'Source changed'
    assert not DEST.exists(), 'Never overwrite a review candidate'
    OUT.mkdir(parents=True, exist_ok=True)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    # Both cut points lie in existing low-level room tone. Exact matching picture
    # and PCM trims preserve sync; no new pause, speed change, or audio graft.
    start, end, duration = CUT_START / FPS, CUT_END / FPS, FRAMES / FPS
    graph = (
        f'[0:v]split=2[v0][v1];[0:a]asplit=2[a0][a1];'
        f'[v0]trim=end_frame={CUT_START},setpts=PTS-STARTPTS[vpre];'
        f'[v1]trim=start_frame={CUT_END}:end_frame={FRAMES},setpts=PTS-STARTPTS[vpost];'
        f'[a0]atrim=end={start:.12f},asetpts=PTS-STARTPTS[apre];'
        f'[a1]atrim=start={end:.12f}:end={duration:.12f},asetpts=PTS-STARTPTS[apost];'
        '[vpre][apre][vpost][apost]concat=n=2:v=1:a=1[v][a]'
    )
    cmd = [ff, '-v', 'warning', '-n', '-i', str(SOURCE), '-filter_complex', graph,
           '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '16',
           '-preset', 'medium', '-threads', '2', '-pix_fmt', 'yuv420p',
           '-r', '30', '-fps_mode', 'cfr', '-video_track_timescale', '90000',
           '-profile:v', 'high', '-level:v', '3.1',
           '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(DEST)]
    subprocess.run(cmd, check=True)
    manifest = dict(source=str(SOURCE), source_sha256=SOURCE_SHA,
                    candidate=str(DEST), candidate_sha256=sha(DEST), fps=FPS,
                    source_frames=FRAMES, output_frames=FRAMES-(CUT_END-CUT_START),
                    cut_source_frames=[CUT_START,CUT_END], cut_source_seconds=[start,end],
                    duration_seconds=(FRAMES-(CUT_END-CUT_START))/FPS,
                    removed_seconds=(CUT_END-CUT_START)/FPS,
                    output_join_frame=CUT_START,
                    retained_source_frames=[[0,CUT_START],[CUT_END,FRAMES]],
                    removed_narration='A good question is always the foundation. Prompting adds the instructions. First, stay open-minded, meaning you haven’t picked the answer in advance. It must be specific, providing enough detail to get an answer that fits. A good question is on target, asking about the actual problem. Finally, keep it open-ended, leaving room for an unexpected answer.',
                    join_words=['We call that prompting.', 'Packaging your question for AI comes down to four specific moves.'],
                    treatment='Remove recap picture and narration. Preserve all retained frames, examples, highlights, camera moves, close and timing. No added pauses.',
                    source_limitation='Current finished source; one further H.264 CRF16 encode and AAC encode for the cut.',
                    status='Review candidate only; canonical video and website reference unchanged.')
    assert sha(SOURCE) == SOURCE_SHA
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__ == '__main__':
    main()
