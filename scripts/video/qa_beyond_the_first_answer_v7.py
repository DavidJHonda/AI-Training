#!/usr/bin/env python3
"""Sequential encoded-state comparison and review stills for the v7 candidate."""
from pathlib import Path
import json,sys
import cv2
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_beyond_the_first_answer_v7 as b

boards,close=b.prepare()
out=b.AUDIT/'encoded';out.mkdir(exist_ok=True)
points={n:slug for slug,board in boards.items() for n in [board['span'][0],board['span'][1]-1,*[r['start']+min(24,(r['end']-r['start'])//2) for r in board['rings']]]}
points.update({n:'close' for n in [5612,5650,5770,5831]})
for a,z,s,e,name,why in b.INSERTS:
 for n in [a,a+(z-a)//4,a+(z-a)//2,a+3*(z-a)//4,z-1]:points[n]=name
for n in [0,720,1100,2200,3500,3600,4430,4500,4700]:points[n]='retained-source'
cap=cv2.VideoCapture(str(b.DEST));n=0;metrics=[];samples=[]
while True:
 ok,im=cap.read()
 if not ok:break
 if n in points:
  label=points[n];p=out/f'{n:04d}-{label}.jpg';cv2.imwrite(str(p),im,[cv2.IMWRITE_JPEG_QUALITY,96]);samples.append((n,label,p))
  expected=b.close_frame(close,n) if label=='close' else b.board_frame(boards[label],n) if label in boards else None
  if expected is not None:
   mse=float(np.mean((im.astype(np.float32)-expected.astype(np.float32))**2));psnr=99 if mse==0 else 10*np.log10(255**2/mse)
   assert psnr>34,(n,psnr)
   metrics.append(dict(frame=n,label=label,psnr=round(float(psnr),2)))
  if n==1402:cv2.imwrite(str(b.AUDIT/'poster.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,96])
 n+=1
cap.release();assert n==5832;decoded_count=n
for group in ['summer-business','profit','college','iteration','close','group-project','thought-partner','lawn-mowing-finances','retained-source']:
 files=[(n,label,p) for n,label,p in samples if label==group];sheet=Image.new('RGB',(1280,384*((len(files)+1)//2)),'white');d=ImageDraw.Draw(sheet)
 for i,(n,label,p) in enumerate(files):
  x=i%2*640;y=i//2*384;sheet.paste(Image.open(p).resize((640,360)),(x,y));d.text((x+5,y+363),f'{n/24:.3f}s / frame {n} / {label}',fill='black')
 sheet.save(b.AUDIT/f'encoded-{group}.jpg',quality=95)
(b.AUDIT/'encoded-state-check.json').write_text(json.dumps(dict(frames_decoded=decoded_count,checked_states=metrics,minimum_psnr=min(m['psnr'] for m in metrics)),indent=2)+'\n')
print('Checked',len(metrics),'encoded board/closing states; minimum PSNR',min(m['psnr'] for m in metrics))
