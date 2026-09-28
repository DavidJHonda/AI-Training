from pathlib import Path
from PIL import Image,ImageDraw
import json,math
p=Path('video-audit/embeddings-repair-2026-09-27-v7');m=json.loads((p/'edit-manifest.json').read_text());v=json.loads((p/'verification.json').read_text());wanted=set()
for key in m['specs']:
 rows=[s for s in m['prepared_states'] if s['key']==key];ns={rows[0]['local_frame'],rows[-1]['local_frame']}
 for r in m['specs'][key]['rings']:ns.add(r['start']+15)
 if key=='bd4':
  c=0
  for b in m['specs'][key]['beats']:ns.add(c+b['frames']-1);c+=b['frames']
 wanted|={s['output_frame'] for s in rows if s['local_frame'] in ns}
wanted|={3194,3195,7525,7526,7527,7634,7635,7996}
files=[Path(f) for f in v['encoded_frames'] if int(Path(f).name.split('-')[0]) in wanted]
for page,start in enumerate(range(0,len(files),12)):
 sheet=Image.new('RGB',(1280,1056),'white');d=ImageDraw.Draw(sheet)
 for j,f in enumerate(files[start:start+12]):
  x=j%3*426;y=j//3*264;sheet.paste(Image.open(f).resize((426,240)),(x,y));d.text((x+4,y+242),f.stem,fill='black')
 sheet.save(p/f'encoded-sheet-{page}.jpg',quality=94)
g=json.loads((p/'guard/transition-guard.json').read_text())
for page,start in enumerate(range(0,len(g['boundaries']),3)):
 rows=g['boundaries'][start:start+3];sheet=Image.new('RGB',(2560,750*len(rows)),'white');d=ImageDraw.Draw(sheet)
 for j,r in enumerate(rows):d.text((8,j*750+4),str(r['frame']),fill='black');sheet.paste(Image.open(p/'guard'/r['strip']),(0,j*750+25))
 sheet.save(p/f'guard-sheet-{page}.jpg',quality=90)
print('Encoded sheets',math.ceil(len(files)/12),'Guard sheets',math.ceil(len(g['boundaries'])/3))
