#!/usr/bin/env python3
"""Decode and verify the final Your Choices repair candidate."""
from pathlib import Path
import json,sys,subprocess,hashlib
import cv2,numpy as np
from PIL import Image,ImageDraw
from audio_gap_review import decode_audio,dbfs
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'video-audit/your-choices-build-2026-09-30-v4'
m=json.loads((A/'edit-manifest.json').read_text())
dest=Path(m['candidate']);ff=imageio_ffmpeg.get_ffmpeg_exe()
bounds={b['frame']:b['label'] for b in m['visual_boundaries']}
for x in m['audio_joins']:bounds.setdefault(x['frame'],'audio-graft')
cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(dest),'--outdir',str(A/'transitions')]
for f,label in sorted(bounds.items()):cmd+=['--boundary',f'{f}:{label}']
subprocess.run(cmd,check=True)

wanted={0:'opening',149:'app',342:'availability-start',605:'all-four',612:'dials-entry',616:'dials-after',1250:'reassurance'}
for leg in m['legs']:
    if leg['source']!='installed':continue
    a,b=leg['source_frames'];o=leg['output_frames'][0]
    for f,label in [(1293,'tool-full'),(1450,'app-ring'),(1980,'model-ring'),(2160,'model-diagram'),(2820,'how-full'),(3080,'reasoning-ring'),(3750,'research-ring'),(4400,'recap'),(4497,'close-start'),(4545,'close-push-start'),(4695,'close-settled'),(4862,'final')]:
        if a<=f<b:wanted[o+f-a]=label
for f,label in bounds.items():
    wanted.setdefault(f-1,f'boundary-{f}-before')
    wanted.setdefault(f,f'boundary-{f}-after')
c=cv2.VideoCapture(str(dest));n=0;shots={};sheets=[]
while True:
    ok,im=c.read()
    if not ok:break
    if n in wanted:
        shots[wanted[n]]=im.copy();cv2.imwrite(str(A/(wanted[n]+'.jpg')),im)
    if n%120==0:
        tile=cv2.resize(im,(480,270));cv2.putText(tile,f'{n/30:.2f}s',(8,25),cv2.FONT_HERSHEY_SIMPLEX,.75,(0,0,220),2);sheets.append(tile)
    n+=1
assert n==m['decoded_frames']==4913
for i in range(0,len(sheets),12):
    group=sheets[i:i+12]
    while len(group)%3:group.append(np.full_like(group[0],255))
    cv2.imwrite(str(A/f'contact-{i//12}.jpg'),cv2.vconcat([cv2.hconcat(group[j:j+3]) for j in range(0,len(group),3)]))

def payload_hash(p):
    b=subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a','-c','copy','-f','data','-'])
    return hashlib.sha256(b).hexdigest()
same_audio=payload_hash(dest)==payload_hash(ROOT/'Prompts/your-choices-v3.mp4')
assert same_audio,'v4 is a four-frame picture repair only; audio must match v3'
audio=decode_audio(dest)
audition=[]
for s in m['audio_joins']:
    i=round(s['time']*44100)
    audition.append(dict(time=s['time'],gap_rms_dbfs=dbfs(audio[i-441:i+441])))
settled_delta=float(np.abs(shots['close-settled'].astype(float)-shots['final'].astype(float)).mean())
assert settled_delta<.5,settled_delta
result=dict(frames=n,duration=n/30,audio_packets_identical_to_v3=same_audio,
            final_close_settled_mean_pixel_delta=settled_delta,peak_amplitude=float(np.abs(audio).max()),
            joins=audition,transition_boundaries=len(bounds),normal_speed_listening=False)
(A/'qa-results.json').write_text(json.dumps(result,indent=2)+'\n')
# Compare the exact before/after frames of every declared visual boundary.
tiles=[]
for f,label in bounds.items():
    before=cv2.imread(str(A/(wanted[f-1]+'.jpg')));after=cv2.imread(str(A/(wanted[f]+'.jpg')))
    row=np.full((205,720,3),255,np.uint8)
    row[25:,:360]=cv2.resize(before,(360,180));row[25:,360:]=cv2.resize(after,(360,180))
    cv2.putText(row,f'{f/30:.2f}s {label}',(8,18),cv2.FONT_HERSHEY_SIMPLEX,.48,(30,30,30),1)
    tiles.append(row)
for i in range(0,len(tiles),6):cv2.imwrite(str(A/f'boundary-summary-{i//6}.jpg'),cv2.vconcat(tiles[i:i+6]))
print(json.dumps(result,indent=2))
