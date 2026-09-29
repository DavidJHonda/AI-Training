from pathlib import Path
import cv2,json
from PIL import Image,ImageDraw
outroot=Path(__file__).parent
for n in (1,2,3):
 p=Path('Prompts')/f'why-learn-ai-{n}.mp4';out=outroot/p.stem;out.mkdir(exist_ok=True)
 cap=cv2.VideoCapture(str(p));fps=cap.get(cv2.CAP_PROP_FPS);samples=[];cuts=[];prev=None;idx=0
 while True:
  ok,f=cap.read()
  if not ok:break
  if idx%round(fps*8)==0:
   im=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB));im.save(out/f'frame-{idx:06d}.jpg',quality=90)
   samples.append((idx/fps,im.resize((400,225))))
  small=cv2.cvtColor(cv2.resize(f,(160,90)),cv2.COLOR_BGR2GRAY).astype('int16')
  if prev is not None and abs(small-prev).mean()>12:cuts.append(idx/fps)
  prev=small;idx+=1
 cap.release()
 for i in range(0,len(samples),12):
  page=Image.new('RGB',(1600,780),'white');d=ImageDraw.Draw(page)
  for j,(t,im) in enumerate(samples[i:i+12]):
   x=(j%4)*400;y=(j//4)*260;page.paste(im,(x,y+30));d.text((x+8,y+8),f'Roll {n} {int(t)//60}:{t%60:05.2f}',fill='black')
  page.save(out/f'sheet-{i//12:02d}.jpg',quality=90)
 (out/'video.json').write_text(json.dumps({'fps':fps,'frames':idx,'duration':idx/fps,'scene_cuts':cuts},indent=2))
 print(p.name,idx/fps,'s',len(samples),'frames sampled',flush=True)
