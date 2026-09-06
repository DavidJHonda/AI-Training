"""Inspect final frames, highlights and audio at every approved edit boundary."""
from pathlib import Path
import json
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw

import build_your_choices_2_review as build
from audio_gap_review import decode_audio, dbfs, write_wav

AUDIT = build.AUDIT
OUTPUT = build.OUTPUT
QA = AUDIT/'qa'
QA.mkdir(parents=True, exist_ok=True)
legs = build.teaching_legs()
requests = {30: 'opening', build.mapped(build.END)-1: 'literal-final-frame'}
cursor = build.mapped(build.CUTS[1][1])
for leg in legs:
    for state in leg.states:
        requests[cursor+min(35,state.frames-1)] = leg.name+'-'+state.label
        cursor += state.frames
cap = cv2.VideoCapture(str(OUTPUT))
images = []
count=0
while True:
    ok, frame=cap.read()
    if not ok: break
    if count in requests:
        label=requests[count]
        path=QA/(label+'.png')
        cv2.imwrite(str(path),frame)
        images.append((count,label,Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))))
    count+=1
cap.release()
assert count==build.mapped(build.END)
for offset in range(0,len(images),4):
    group=images[offset:offset+4]
    sheet=Image.new('RGB',(1280,390*((len(group)+1)//2)),'white')
    draw=ImageDraw.Draw(sheet)
    for i,(f,label,im) in enumerate(group):
        x=(i%2)*640;y=(i//2)*390
        draw.text((x+8,y+6),f'{f/30:.2f}s {label}',fill='black')
        sheet.paste(im.resize((640,360)),(x,y+27))
    sheet.save(QA/f'states-{offset//4:02}.jpg')

audio=decode_audio(OUTPUT)
clips=[]
seams=[]
for i,(start,end) in enumerate(build.CUTS,1):
    seam=build.mapped(start)/30
    a,b=round((seam-2.5)*44100),round((seam+3.5)*44100)
    clip=audio[a:b]
    write_wav(QA/f'audio-cut-{i}.wav',clip)
    clips.extend((clip,np.zeros(11025,dtype=np.float32)))
    center=round(seam*44100)
    seams.append({'cut':i,'output_time':seam,
                  'seam_20ms_dbfs':dbfs(audio[center-441:center+441]),
                  'sample_step':float(abs(audio[center]-audio[center-1]))})
write_wav(QA/'all-cut-boundaries.wav',np.concatenate(clips))
(QA/'audio-seams.json').write_text(json.dumps(seams,indent=2)+'\n')
print('Decoded frames:',count,'; duration:',count/30)
print(json.dumps(seams,indent=2))
