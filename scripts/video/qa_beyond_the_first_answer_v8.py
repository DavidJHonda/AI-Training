#!/usr/bin/env python3
"""Sequentially inspect the encoded cinematic candidate against prepared frames."""
from pathlib import Path
import json,sys
import cv2
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_beyond_the_first_answer_v8 as b
out=b.AUDIT/'encoded';out.mkdir(exist_ok=True)
points={int(p.stem.rsplit('-',1)[1]):p for p in (b.AUDIT/'previews').glob('*.jpg')}
cap=cv2.VideoCapture(str(b.DEST));n=0;metrics=[];samples=[]
while True:
 ok,im=cap.read()
 if not ok:break
 if n in points:
  ref=points[n];label=ref.stem.rsplit('-',1)[0];expected=cv2.imread(str(ref))
  mse=float(np.mean((im.astype(np.float32)-expected.astype(np.float32))**2));psnr=99 if mse==0 else float(10*np.log10(255**2/mse))
  assert psnr>30,(n,label,psnr)
  target=out/f'{n:04d}-{label}.jpg';cv2.imwrite(str(target),im,[cv2.IMWRITE_JPEG_QUALITY,96]);samples.append((n,label,target));metrics.append(dict(frame=n,label=label,psnr=round(psnr,2)))
  if n==705:cv2.imwrite(str(b.AUDIT/'poster.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,96])
 n+=1
cap.release();assert n==b.TOTAL
for label in sorted({label for n,label,p in samples}):
 rows=[row for row in samples if row[1]==label];sheet=Image.new('RGB',(1280,384*((len(rows)+1)//2)),'white');d=ImageDraw.Draw(sheet)
 for i,(frame,_,p) in enumerate(rows):
  x=i%2*640;y=i//2*384;sheet.paste(Image.open(p).resize((640,360)),(x,y));d.text((x+5,y+362),f'{frame/24:.3f}s / frame {frame} / {label}',fill='black')
 sheet.save(b.AUDIT/f'encoded-{label}.jpg',quality=95)
(b.AUDIT/'encoded-state-check.json').write_text(json.dumps(dict(decoded_frames=n,checked_states=metrics,minimum_psnr=min(x['psnr'] for x in metrics)),indent=2)+'\n')
print(f'Passed: {n} decoded frames, {len(metrics)} sampled states, minimum PSNR {min(x["psnr"] for x in metrics):.2f}')
