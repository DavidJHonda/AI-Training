#!/usr/bin/env python3
"""Two approved sentence-boundary cuts from the current Layers video."""
from pathlib import Path
import hashlib, json, subprocess
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/layers-tighten-v13-2026-11-09'
SOURCE = ROOT / 'Prompts/layers-v12.mp4'
DEST = ROOT / 'Prompts/layers-v13.mp4'
FPS = 30
SPF = 1600
SPANS = [(0, 1653), (1953, 2388), (2991, 6183)]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    assert not DEST.exists(), 'Never overwrite a review candidate'
    expected = '42fb10fd979dd5567d8a9ae2105507a87b7f7cc0610ff20e1095fbd7ce5bcbb6'
    assert sha(SOURCE) == expected
    assert sha(ROOT / 'course-assets/layers/layers.mp4') == expected
    graph = []
    timeline = []
    cursor = 0
    for i, (a, b) in enumerate(SPANS):
        graph += [f'[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v{i}]',
                  f'[0:a]atrim=start_sample={a*SPF}:end_sample={b*SPF},asetpts=PTS-STARTPTS[a{i}]']
        timeline.append(dict(source_frames=[a,b],output_frames=[cursor,cursor+b-a]))
        cursor += b-a
    graph.append(''.join(f'[v{i}][a{i}]' for i in range(3)) + 'concat=n=3:v=1:a=1[v][a]')
    manifest = dict(source=str(SOURCE),source_sha256=expected,candidate=str(DEST),
        approval='User agreed to both trims and requested: Can you update the video now?',
        scope='Narrow pacing edit: remove repeated layer explanation and numeric readout.',
        cuts=[dict(seconds=[55.1,65.1],words='Within each layer ... what your words mean together.'),
              dict(seconds=[79.6,99.7],words='Each row of data ... finishing at .19 and negative 1.12.')],
        retained_takeaway='The numbers that come out are not the numbers that went in. Attention and transformation update the numbers at each layer.',
        timeline=timeline,frames=cursor,fps=FPS,duration=cursor/FPS,boundaries=[1653,2088],
        board_plan=dict(title='How Layers Update the Numbers',
            camera='Retain full-board opening, cut to existing complete number-row zoom, retain pullback for takeaway.',
            highlights='Retain layer-diagram outline, final-number card outline, then takeaway outline.',
            reason='Numeric comparison remains visible without reading individual values.',
            added_pauses=0),
        source_limit='Retained v12 is the source. The original temporary snapshot required by its reconstruction pipeline no longer exists. One high-quality encode from v12; no intermediate lossy renders.',
        direct_listening=False,installed=False)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-n','-i',str(SOURCE),
        '-filter_complex',';'.join(graph),'-map','[v]','-map','[a]',
        '-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],check=True)
    assert sha(SOURCE)==expected
    assert sha(ROOT/'course-assets/layers/layers.mp4')==expected
    manifest['candidate_sha256']=sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(DEST,flush=True)

if __name__=='__main__':
    main()
