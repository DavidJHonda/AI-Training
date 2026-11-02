from pathlib import Path
import cv2,json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
files=[R/'Prompts'/f'flattery-engagement{s}.mp4' for s in ['','-1','-2','-3']]
rows=[]
for p in files:
 if not p.exists():continue
 cap=cv2.VideoCapture(str(p));fps=cap.get(cv2.CAP_PROP_FPS);count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));duration=count/fps
 row={'file':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fps':fps,'frames':count,'duration':duration,'width':int(cap.get(3)),'height':int(cap.get(4))}
 frames=[];idx=0;step=round(fps*15)
 while True:
  ok,f=cap.read()
  if not ok:break
  if idx%step==0:
   im=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB));im.thumbnail((360,203));frames.append((idx/fps,im))
  idx+=1
 cap.release()
 for chunk in range(0,len(frames),20):
  batch=frames[chunk:chunk+20];sheet=Image.new('RGB',(1440,235*((len(batch)+3)//4)),'white');d=ImageDraw.Draw(sheet)
  for j,(t,im) in enumerate(batch):
   x=(j%4)*360;y=(j//4)*235;sheet.paste(im,(x,y+26));d.text((x+6,y+5),f'{p.stem} {int(t)//60}:{int(t)%60:02}',fill='black')
  sheet.save(OUT/f'{p.stem}-sheet-{chunk//20+1}.jpg',quality=85)
 rows.append(row)
(OUT/'sources.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
boards=sorted((R/'course-assets/flattery-engagement').glob('*.jpg'))
sheet=Image.new('RGB',(1200,1000),'white')
for j,p in enumerate(boards):
 im=Image.open(p);im.thumbnail((395,470));sheet.paste(im,((j%3)*400,(j//3)*500+25));ImageDraw.Draw(sheet).text(((j%3)*400+4,(j//3)*500+5),p.stem.replace('flattery-engagement-',''),fill='black')
sheet.save(OUT/'canonical-boards.jpg',quality=90)
