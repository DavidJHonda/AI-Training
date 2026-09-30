#!/usr/bin/env python3
"""Approved narrow repair of the public-identical Hallucination v12.

Retains v14 repairs; restores Stanford step 3 and adds a same-narrator
Check the Match cue before the pizza source-support explanation.
The available source is the finished v12; no pristine raw roll survives locally.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import wave
from editspec_build import Build

import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'course-assets/hallucination/hallucination.mp4'
OUT = ROOT / 'video-audit/hallucination-v15-2026-09-30'
DEST = ROOT / 'Prompts/hallucination-v15.mp4'
EXPECTED = '1c7189c1aedafb057d1740e60d469a55209c3350ad3de504dc363f3bcf44c253'
FPS, RATE, TOTAL = 30, 48000, 8412
FF = imageio_ffmpeg.get_ffmpeg_exe()
CUTS = [(1451, 1555), (3490, 3838)]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def wav(path, samples):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(np.clip(np.rint(samples), -32768, 32767).astype('<i2').tobytes())


def main():
    assert sha(SRC) == EXPECTED, 'Source changed; do not apply old timings'
    assert not DEST.exists(), 'Use a new version; never overwrite a candidate'
    OUT.mkdir(exist_ok=True)
    protected = [ROOT / 'index.html', ROOT / 'lessons/hallucination.md', SRC]
    protected += list(SRC.parent.glob('*.jpg'))
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    pcm = subprocess.check_output([FF, '-v', 'error', '-i', str(SRC), '-vn',
                                   '-ac', '1', '-ar', str(RATE), '-f', 's16le', '-'])
    audio = np.frombuffer(pcm, dtype='<i2').astype(np.float64)
    factor = RATE // FPS
    spans = [(0,1451), (1555,3490), (3838,7740), (5991,6030), (7740,TOTAL)]
    edited = np.concatenate([audio[a*factor:b*factor] for a,b in spans])
    seams = [1451, 3386, 7288, 7327]
    # Four milliseconds of interpolation wholly within the measured quiet
    # troughs. No speech sample is faded and duration/sample count is unchanged.
    for frame in seams:
        sample = frame * factor
        edited[sample-96:sample+96] = np.linspace(edited[sample-96], edited[sample+95], 192)
    wav(OUT / 'edited.wav', edited)
    for i, seam in enumerate(seams, 1):
        wav(OUT / f'join-{i}.wav', edited[(seam-90)*factor:(seam+180)*factor])

    # Exact canonical board; fixed delivery-size stroke drawn after resizing.
    builder = Build(ROOT, SRC, OUT, DEST)
    canvas, cw, ch, ox, oy = builder.compose(SRC.parent/'hallucination-check-claim.jpg', 'check')
    board_specs = {}
    for key, count, onset in [('stanford',157,0), ('pizza',444,71)]:
        spec = dict(density='compact',image=str(canvas),fps=FPS,out_w=1280,out_h=720,upscale=3,
                    beats=[dict(label='full-view',frames=count,**{'from':[800,450,1600],'to':[800,450,1600]})],
                    rings=[dict(start=onset,end=count,rect=[1060,188,500,611],
                                color='#0e8f86',pad=0,radius=18)])
        path=OUT/f'leg-{key}.json'; path.write_text(json.dumps(spec,indent=2)+'\n')
        subprocess.run([str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/ken_burns_path.py'),
                        str(path),str(OUT/f'{key}.mkv')],check=True)
        board_specs[key]=spec

    # Half-open frame ranges. The first two fields are the original narration
    # timeline; the next two identify the picture source. Retimes are visual only.
    rows = [
        (0,1451,0,1451,'keep opening'),
        (1555,3490,1555,3490,'keep mixed-facts explanation and Why board'),
        (3838,3847,3847,3848,'start-clone ALL ERRORS, remove orphan monitor'),
        (3847,6102,3847,6102,'keep error distinction, pizza, checking introduction'),
        (6102,6312,1209,1419,'disappearing paper supports invented-study check'),
        (6312,6890,6312,6890,'return to Find the Source'),
        (6890,7047,0,157,'board:stanford'),
        (7047,7295,7184,7295,'UNVERIFIED != FACT over verification nuance'),
        (7295,7680,7295,7680,'keep pizza application through finding Reddit source'),
        (7680,7740,0,60,'board:pizza'),
        (5991,6030,60,99,'board:pizza'),
        (7740,8085,99,444,'board:pizza'),
        (8085,TOTAL,8085,TOTAL,'keep standard close'),
    ]
    graph, timeline, cursor = [], [], 0
    for i,(a,b,va,vb,label) in enumerate(rows):
        count=b-a
        input_index = {'board:stanford':2,'board:pizza':3}.get(label,0)
        chain=f'[{input_index}:v]trim=start_frame={va}:end_frame={vb},setpts=PTS-STARTPTS'
        if vb-va == 1:
            chain += f',loop=loop={count-1}:size=1:start=0,setpts=N/({FPS}*TB)'
        elif vb-va != count:
            chain += f',setpts=PTS*{count}/{vb-va},fps={FPS}'
        chain += f',trim=end_frame={count},setpts=N/({FPS}*TB),setsar=1[v{i}]'
        graph.append(chain)
        timeline.append(dict(start_frame=cursor,end_frame=cursor+count,
                             source_audio=[a,b],source_video=[va,vb],video_input=input_index,label=label))
        cursor += count
    assert cursor == 7999 and len(edited) == cursor*factor
    graph.append(''.join(f'[v{i}]' for i in range(len(rows)))+
                 f'concat=n={len(rows)}:v=1:a=0,format=yuv420p[v]')
    (OUT/'filter.txt').write_text(';\n'.join(graph)+'\n')
    temp=OUT/'rendering.mp4'
    assert not temp.exists(), 'Remove only failed render scratch before retrying'
    cmd=[FF,'-v','warning','-threads','2','-i',str(SRC),'-i',str(OUT/'edited.wav'),
         '-i',str(OUT/'stanford.mkv'),'-i',str(OUT/'pizza.mkv'),
         '-filter_complex_threads','2','-filter_complex_script',str(OUT/'filter.txt'),
         '-map','[v]','-map','1:a','-c:v','libx264','-threads','2','-preset','fast',
         '-crf','16','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','aac','-b:a','192k',
         '-movflags','+faststart',str(temp)]
    (OUT/'command.json').write_text(json.dumps(cmd,indent=2)+'\n')
    subprocess.run(cmd,check=True)
    assert all(sha(ROOT/p)==h for p,h in hashes.items()), 'Protected source changed'
    temp.rename(DEST)
    manifest=dict(candidate=str(DEST),candidate_sha256=sha(DEST),source=str(SRC),
                  source_sha256=EXPECTED,source_limitation='finished v12; raw generation absent',
                  fps=FPS,total_frames=cursor,duration=cursor/FPS,
                  cuts=[dict(source_frames=[a,b],seconds=[a/FPS,b/FPS]) for a,b in CUTS],
                  timeline=timeline,audio_join_output_frames=seams,
                  audio_smoothing='4 ms linear bridge in quiet troughs; no duration change',
                  added_pauses=[],protected_hashes=hashes,board_specs=board_specs,
                  narration_graft=dict(text='and check the match',source_frames=[5991,6030],
                                       output_frames=[7288,7327],insertion_source_frame=7740),
                  scope='v14 repairs retained; restore Stanford step 3 and add spoken/visual step 3 cue for pizza',
                  listening_status='not auditioned; contextual join WAVs provided')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Built {DEST}: {cursor} frames, {cursor/FPS:.3f} seconds',flush=True)


if __name__=='__main__':
    main()
