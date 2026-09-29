#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,subprocess,wave
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
from editspec_build import Reader
from build_opener_work_fola_review import read
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/work-with-ai-opener-hybrid-2026-09-29-v11'
m=json.loads((OUT/'edit-manifest.json').read_text());v=Path(m['candidate']);framesdir=OUT/'encoded';framesdir.mkdir(exist_ok=True)
ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-v','error','-y','-i',str(v),'-vn','-ar','48000','-ac','1','-c:a','pcm_s16le',str(OUT/'candidate.wav')],check=True)
planned=read(OUT/'edited.wav');actual=read(OUT/'candidate.wav');rows=[]
for r in m['audio_rows']:
 a,b=r['output_start']*1600,r['output_end']*1600; x=actual[a:b];y=planned[a:b]
 rows.append({'label':r['label'],'corr':float(np.corrcoef(x,y)[0,1]),'samples':len(x),'planned_samples':len(y)})
 assert len(x)==len(y) and rows[-1]['corr']>.995
cap=cv2.VideoCapture(str(v));i=0;tiles=[];wanted=set([0,195,1503,2627,2628,2663,2800,2927,2928,2965,3000,3142,3143,3200,3250,3400,3562,3563,3574,3650,3742,3743,3791,3941,4095]);samples=[];src=Reader(ROOT/'course-assets/work-with-ai-opener/work-with-ai-opener.mp4')
while True:
 ok,f=cap.read()
 if not ok:break
 if i%60==0 or i in wanted:
  if i in wanted:cv2.imwrite(str(framesdir/f'{i:05d}.jpg'),f)
  if i%120==0 or i in wanted:
   im=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB));im.thumbnail((384,216));t=Image.new('RGB',(384,240),'white');t.paste(im,(0,24));ImageDraw.Draw(t).text((5,5),f'{i/30:.3f}s | f{i}',fill='black');tiles.append(t)
 if i<2628 and i%150==0 or i>=3743 and (i-3743)%75==0 or i==4095:
  sn=i if i<2628 else i-3743+4384;sf=src.at(sn);samples.append({'output_frame':i,'source_frame':sn,'mean_abs_diff':float(np.abs(f.astype(float)-sf.astype(float)).mean())})
 i+=1
assert i==m['total_frames']
for j in range(0,len(tiles),20):
 sh=Image.new('RGB',(1536,1200),'#eee')
 for k,t in enumerate(tiles[j:j+20]):sh.paste(t,((k%4)*384,(k//4)*240))
 sh.save(OUT/f'qa-sheet-{j//20+1}.jpg')
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==s for p,s in m['protected'].items())
# Untouched planned PCM is bit-identical outside the 5ms join treatment.
base=read(OUT/'live.wav');pcm=[]
for r in m['audio_rows']:
 if r['source']=='live':
  a=r['output_start']*1600;b=r['output_end']*1600; x=planned[a+240:b-240];y=base[r['start']*1600+240:r['end']*1600-240]
  pcm.append({'label':r['label'],'max_diff':float(np.max(abs(x-y)))});assert np.max(abs(x-y))<1/32768
q={'decoded_frames':i,'duration':i/30,'audio_rows':rows,'unchanged_visual_samples':samples,'unchanged_planned_pcm':pcm,'protected_unchanged':True,'aac_padding_samples':len(actual)-len(planned),'listening':'Not performed'}
(OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
