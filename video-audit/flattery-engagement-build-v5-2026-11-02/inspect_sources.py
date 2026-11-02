from pathlib import Path
import cv2,numpy as np,json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent
files={n:R/f'Prompts/flattery-engagement-{n}.mp4' for n in [1,2,3]}
files['feedback']=R/'Prompts/flattery-engagement/archive/flattery-engagement-feedback-source-v13.mp4'
results={}
for k,p in files.items():
 cap=cv2.VideoCapture(str(p));prev=None;frames=[];cuts=[];idx=0; grabs={}
 while True:
  ok,f=cap.read()
  if not ok:break
  small=cv2.cvtColor(cv2.resize(f,(160,90)),cv2.COLOR_BGR2GRAY).astype(np.int16)
  diff=float(np.abs(small-prev).mean()) if prev is not None else 0
  if diff>10:cuts.append({'frame':idx,'time':idx/30,'diff':diff});grabs[idx]=f.copy()
  if idx%300==0:grabs[idx]=f.copy()
  prev=small;idx+=1
 cap.release();results[str(k)]=cuts
 # A representative half-second after each cut plus the 10s samples.
 selected=sorted(grabs)
 for offset in range(0,len(selected),20):
  batch=selected[offset:offset+20];sheet=Image.new('RGB',(1600,245*((len(batch)+3)//4)),'white');d=ImageDraw.Draw(sheet)
  for j,n in enumerate(batch):
   im=Image.fromarray(cv2.cvtColor(grabs[n],cv2.COLOR_BGR2RGB));im=im.resize((400,225));x=j%4*400;y=j//4*245;sheet.paste(im,(x,y+20));d.text((x+5,y+3),f'{k}  {n/30:.3f}s / f{n}',fill='black')
  sheet.save(O/f'source-{k}-{offset//20+1}.jpg',quality=88)
 print(k,'frames',idx,'cuts',[round(c['time'],3) for c in cuts],flush=True)
(O/'scene-cuts.json').write_text(json.dumps(results,indent=2)+'\n')
