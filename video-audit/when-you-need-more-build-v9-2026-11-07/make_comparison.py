"""39-second before/after excerpt with surrounding narration; v8 left, v9 right."""
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/video'))
import build_when_you_need_more_v9 as b

filters=[]
for index,start,end in [(0,60,80),(1,114,133)]:
    for stream in [0,1]:
        filters.append(f'[{stream}:v]trim=start={start}:end={end},setpts=PTS-STARTPTS,scale=640:360[v{stream}{index}]')
    filters.append(f'[v0{index}][v1{index}]hstack=inputs=2[p{index}]')
    filters.append(f'[1:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{index}]')
filters.append('[p0][a0][p1][a1]concat=n=2:v=1:a=1[v][a]')
destination=b.OUT/'before-left-after-right.mp4'
assert not destination.exists()
subprocess.run([b.base.FF,'-v','error','-i',str(b.LIVE),'-i',str(b.DEST),
    '-filter_complex',';'.join(filters),'-map','[v]','-map','[a]',
    '-c:v','libx264','-crf','18','-preset','fast','-threads','4','-pix_fmt','yuv420p',
    '-c:a','aac','-b:a','160k','-movflags','+faststart',str(destination)],check=True)
print(destination)
