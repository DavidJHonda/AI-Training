#!/usr/bin/env python3
"""Validate every encoded frame, preserved PCM, and roadmap joins for v8."""
import json
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw

from build_build_your_skills_opener_v8 import OUT, DEST, BASE, EXPECTED, FF, SPF
from build_work_with_ai_opener_fola_review import read, sha
from editspec_build import Reader

m = json.loads((OUT/'edit-manifest.json').read_text())
subprocess.run([FF,'-v','error','-y','-i',str(DEST),'-vn','-ac','1','-ar','48000',
                '-c:a','pcm_s16le',str(OUT/'candidate.wav')],check=True)
planned, actual, base = [read(OUT/f'{n}.wav') for n in ['edited','candidate','base']]
audio = []
for r in m['audio_rows']:
    a,b=r['output_start']*SPF,r['output_end']*SPF
    corr=float(np.corrcoef(planned[a:b],actual[a:b])[0,1])
    assert corr>.995
    q=dict(source=r['source'],output_frames=[r['output_start'],r['output_end']],correlation=corr)
    if r['source']=='base':
        diff=float(abs(planned[a+240:b-240]-base[r['start']*SPF+240:r['end']*SPF-240]).max())
        assert diff==0
        q['unchanged_pcm_max_difference']=diff
    audio.append(q)

wanted=[0,500,1000,1707,1881,1882,1983,1984,1993,1994,2200,2322,2323,2333,2334,2900,2901,3424,3425,3643,3644,4000,4454]
cap=cv2.VideoCapture(str(DEST)); source=Reader(BASE); tiles=[]; measures=[];n=0
encoded=OUT/'encoded';encoded.mkdir(exist_ok=True)
for row in m['visual_rows']:
    ref=source if row['kind']=='base' else Reader(row['file'])
    diffs=[]
    for j in range(row['end']-row['start']):
        ok,f=cap.read();assert ok,n
        expected=ref.at(row['source_start']+j)
        diff=float(abs(cv2.resize(f,(320,180)).astype(float)-cv2.resize(expected,(320,180)).astype(float)).mean())
        diffs.append(diff)
        assert diff<4,(n,diff)
        if n in wanted:
            cv2.imwrite(str(encoded/f'{n:05d}.jpg'),f)
            im=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).resize((384,216))
            tile=Image.new('RGB',(384,240),'white');tile.paste(im,(0,24))
            ImageDraw.Draw(tile).text((5,5),f'{n/30:.3f}s | frame {n}',fill='black');tiles.append(tile)
        n+=1
    measures.append(dict(start=row['start'],end=row['end'],kind=row['kind'],
                         compared_frames=len(diffs),maximum_frame_mean_absolute_error=max(diffs)))
assert n==4455 and not cap.read()[0]
for k in range(0,len(tiles),12):
    batch=tiles[k:k+12]; sheet=Image.new('RGB',(1536,240*((len(batch)+3)//4)),'#eee')
    for j,t in enumerate(batch):sheet.paste(t,(j%4*384,j//4*240))
    sheet.save(OUT/f'qa-sheet-{k//12+1}.jpg')
for p,h in EXPECTED.items():assert sha(p)==h
q=dict(decoded_frames=n,duration=n/30,audio=audio,visual_comparisons=measures,
       aac_padding_samples=len(actual)-len(planned),protected_inputs_unchanged=True,
       peak_audio_dbfs=float(20*np.log10(abs(actual).max())),direct_listening_performed=False)
(OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n')
print(json.dumps(q,indent=2))
