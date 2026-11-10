from pathlib import Path
import cv2,numpy as np,json,hashlib
root=Path('/Users/davidobrien/Developer/AI-Training');out=root/'video-audit/how-ai-answers-donor-plan-2026-11-10'
for roll in [5,6,7]:
 p=root/f'Prompts/how-ai-answers-{roll}.mp4';c=cv2.VideoCapture(str(p));fps=c.get(cv2.CAP_PROP_FPS);n=0;prev=None;cuts=[];tiles=[]
 d=out/f'roll-{roll}';d.mkdir(exist_ok=True)
 while True:
  ok,im=c.read()
  if not ok:break
  small=cv2.cvtColor(cv2.resize(im,(160,90)),cv2.COLOR_BGR2GRAY).astype(np.int16)
  delta=0 if prev is None else float(np.abs(small-prev).mean())
  if delta>12:cuts.append({'frame':n,'seconds':n/fps,'difference':delta})
  if n%round(fps*8)==0:
   cv2.imwrite(str(d/f'{n:06d}.jpg'),im)
   tile=cv2.resize(im,(384,216));cv2.rectangle(tile,(0,0),(384,25),(255,255,255),-1);cv2.putText(tile,f'Roll {roll} | {n/fps:.1f}s | frame {n}',(5,18),0,.5,(0,0,140),1,cv2.LINE_AA);tiles.append(tile)
  prev=small;n+=1
 c.release()
 for j in range(0,len(tiles),12):
  part=tiles[j:j+12]
  while len(part)<12:part.append(np.full((216,384,3),255,np.uint8))
  cv2.imwrite(str(out/f'roll-{roll}-sheet-{j//12}.jpg'),cv2.vconcat([cv2.hconcat(part[k:k+3]) for k in range(0,12,3)]))
 meta={'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fps':fps,'frames':n,'duration':n/fps,'cuts':cuts}
 (d/'scan.json').write_text(json.dumps(meta,indent=2));print(roll,n/fps,'seconds',len(cuts),'cuts',flush=True)
