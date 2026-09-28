from pathlib import Path
from PIL import Image,ImageDraw
import json,math
p=Path(__file__).resolve().parent
v=json.loads((p/'verification.json').read_text())
frames=sorted(v['encoded_frames'])
for k,start in enumerate(range(0,len(frames),24)):
 group=frames[start:start+24];sheet=Image.new('RGB',(1600,math.ceil(len(group)/4)*255),'white');d=ImageDraw.Draw(sheet)
 for i,f in enumerate(group):
  im=Image.open(f);im.thumbnail((400,225));x=i%4*400;y=i//4*255;sheet.paste(im,(x,y+30));name=Path(f).stem;n=int(name.split('-')[0]);d.text((x+4,y+5),f'{n/30:.2f}s {name}',fill='black')
 sheet.save(p/f'encoded-sheet-{k}.jpg',quality=92)
strips=sorted((p/'guard').glob('boundary-*.jpg'))
for k,start in enumerate(range(0,len(strips),3)):
 ims=[]
 for f in strips[start:start+3]:
  im=Image.open(f);im.thumbnail((1500,1200));ims.append((f,im.copy()))
 sheet=Image.new('RGB',(1500,sum(im.height+30 for f,im in ims)),'white');d=ImageDraw.Draw(sheet);y=0
 for f,im in ims:d.text((4,y+5),f.name,fill='black');sheet.paste(im,(0,y+30));y+=im.height+30
 sheet.save(p/f'guard-sheet-{k}.jpg',quality=93)
print('encoded sheets',math.ceil(len(frames)/24),'guard sheets',math.ceil(len(strips)/3))
