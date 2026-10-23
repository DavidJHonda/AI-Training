#!/usr/bin/env python3
"""Approved consolidation: v8 + In Your Hands v6, one encode, review only."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/loudest-voices-build-v9-2026-10-22'
DEST = ROOT / 'Prompts/loudest-voices-v9.mp4'
SOURCES = [
    (ROOT / 'Prompts/loudest-voices-v8.mp4', 'd553d341c258f1420b8a5927f6a6cdd2652a12b1f0d6fafe5d55f66089b497a4'),
    (ROOT / 'Prompts/in-your-hands-v6.mp4', '721e0738684fa09007104865ef0ca292dac2951a93766d04e7db8bcfbde2151c'),
]
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, RATE = 30, 48000
SEGMENTS = [(0, 0, 6488), (1, 1074, 3477), (1, 5019, 5508)]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    assert not DEST.exists(), 'Never overwrite a review candidate; use a new version.'
    OUT.mkdir(parents=True, exist_ok=True)
    protected = [ROOT/'index.html', ROOT/'lessons/loudest-voices.md',
                 ROOT/'course-assets/loudest-voices/loudest-voices.mp4',
                 ROOT/'course-assets/in-your-hands/in-your-hands.mp4',
                 ROOT/'course-assets/loudest-voices/loudest-voices-close.jpg']
    before = {str(p.relative_to(ROOT)):sha(p) for p in protected}
    for p, expected in SOURCES:
        assert sha(p) == expected, f'Source changed: {p}'
    canvas = OUT/'close-canvas.png'
    subprocess.run([sys.executable, str(ROOT/'scripts/video/make_close_board.py'),
                    '--lesson', 'whatpeoplesay', '--out', str(canvas)], check=True)
    graph = []
    for i, (src, start, end) in enumerate(SEGMENTS):
        n = end-start
        if i < 2:
            graph.append(f'[{src}:v]trim=start_frame={start}:end_frame={end},settb=1/30,setpts=N,setsar=1[v{i}]')
        fades = ''
        # Only 5 ms at new joins, inside quiet handles. No change to spoken pacing.
        if i > 0:
            fades += ',afade=t=in:st=0:d=0.005'
        if i < 2:
            fades += f',afade=t=out:st={n/FPS-0.005:.12f}:d=0.005'
        graph.append(f'[{src}:a]atrim=start_sample={start*1600}:end_sample={end*1600},asetpts=PTS-STARTPTS{fades}[a{i}]')
    graph.append("[2:v]zoompan=z='if(lt(on,48),1,if(lt(on,198),1+0.2*(on-48)/149,1.2))':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=489:s=1280x720:fps=30,settb=1/30,setpts=N,setsar=1[v2]")
    graph.append('[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]')
    filters = ';'.join(graph)
    (OUT/'filtergraph.txt').write_text(filters+'\n')
    command = [FF,'-hide_banner','-loglevel','warning','-n',
               '-i',str(SOURCES[0][0]),'-i',str(SOURCES[1][0]),'-i',str(canvas),
               '-filter_complex',filters,'-map','[v]','-map','[a]',
               '-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-r','30',
               '-c:a','aac','-b:a','192k','-ar',str(RATE),'-movflags','+faststart',str(DEST)]
    subprocess.run(command, check=True)
    timeline=[]; offset=0
    for src,start,end in SEGMENTS:
        timeline.append({'source':str(SOURCES[src][0].relative_to(ROOT)),
                         'source_start_frame':start,'source_end_frame':end,
                         'output_start_frame':offset,'output_end_frame':offset+end-start})
        offset+=end-start
    assert offset == 9380
    assert before == {str(p.relative_to(ROOT)):sha(p) for p in protected}
    manifest={'authorization':'David: Yes, build it. Approved prior 5:13 splice plan.',
              'candidate':str(DEST.relative_to(ROOT)),'sha256':sha(DEST),
              'sources':[{'path':str(p.relative_to(ROOT)),'sha256':h} for p,h in SOURCES],
              'timeline':timeline,'frames':offset,'fps':FPS,'duration':offset/FPS,
              'boundaries':[{'frame':6488,'label':'habits-to-in-your-hands'},
                            {'frame':8891,'label':'comparison-to-close'}],
              'audio':'Source PCM cut on exact samples; 5 ms quiet-handle edge fades; AAC encoded once; no loudness or pacing changes.',
              'close':{'asset':'course-assets/loudest-voices/loudest-voices-close.jpg',
                       'sha256':before['course-assets/loudest-voices/loudest-voices-close.jpg'],
                       'hold_frames':48,'push_frames':150,'settle_frames':291,'end_zoom':1.2},
              'protected':before,'status':'candidate built; verification pending; not installed'}
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Built {DEST}: {offset} frames, {offset/FPS:.3f} s',flush=True)

if __name__ == '__main__':
    main()
