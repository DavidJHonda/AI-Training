import sys,json,math
from pathlib import Path
from PIL import Image,ImageDraw
import cv2
sys.path.insert(0,str(Path.cwd()/'scripts/video'))
from build_tokens_v9 import mapping
p=Path('video-audit/tokens-repair-2026-09-27-v9');m=json.loads((p/'edit-manifest.json').read_text());v=json.loads((p/'verification.json').read_text())
# Every prepared board state plus corrected-chart samples and narration cuts.
old=json.loads(Path('video-audit/tokens-build-2026-09-22/edit-manifest.json').read_text());want=set();reverse={f:i for i,f in enumerate(mapping())}
for s in m['prepared_states']:
 key=s['key'];local=s['local_frame']
 if key=='5-splits':want.add(6198+local);continue
 for row in old['timeline']:
  if row.get('visual')==key and row['kind']!='room_tone':
   n=old['boards'][key]['src_in']+local
   if row['source_start']<=n<row['source_start']+row['end_frame']-row['start_frame']:
    want.add(reverse[row['start_frame']+n-row['source_start']]);break
want|={3720,3750,3795,3975,4035,4050,6284,6285,6425,6426,7180,7181,7186,7187,7834,8156}
files=[]
for f in v['encoded_frames']:
 if int(Path(f).name.split('-')[0]) in want:files.append(Path(f))
for page,start in enumerate(range(0,len(files),12)):
 sheet=Image.new('RGB',(1280,4*264),'white');d=ImageDraw.Draw(sheet)
 for j,f in enumerate(files[start:start+12]):
  im=Image.open(f).resize((426,240));x=(j%3)*426;y=(j//3)*264;sheet.paste(im,(x,y));d.text((x+4,y+242),f.stem,fill='black')
 sheet.save(p/f'encoded-sheet-{page}.jpg',quality=93)
# Every-frame strips, packed at native 320px tile resolution.
g=json.loads((p/'guard/transition-guard.json').read_text())
for page,start in enumerate(range(0,len(g['boundaries']),3)):
 rows=g['boundaries'][start:start+3];sheet=Image.new('RGB',(2560,750*len(rows)),'white');d=ImageDraw.Draw(sheet)
 for j,row in enumerate(rows):
  d.text((8,j*750+4),str(row['frame'])+' '+row['label'],fill='black');sheet.paste(Image.open(p/'guard'/row['strip']),(0,j*750+25))
 sheet.save(p/f'guard-sheet-{page}.jpg',quality=90)
print('Board/scene sheets:',math.ceil(len(files)/12),'Guard sheets:',math.ceil(len(g['boundaries'])/3))
