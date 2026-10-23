#!/usr/bin/env python3
import hashlib,json,subprocess,sys
import av,cv2,numpy as np
from PIL import Image,ImageDraw
from fix_loudest_opening_v11 import ROOT,OUT,SOURCE,DEST,A,START,B
from build_remove_doubter import Boards,frames

def packets(path):
 result={'video':{},'audio':{}}
 with av.open(str(path)) as c:
  for p in c.demux():
   if p.dts is None:continue
   result[p.stream.type][(p.pts,p.dts,p.duration,str(p.time_base))]=hashlib.sha256(bytes(p)).hexdigest()
 return result
s=packets(SOURCE);d=packets(DEST)
assert s['audio']==d['audio']
assert {k[0] for k in s['video']}=={k[0] for k in d['video']}
unchanged=0
for k,h in s['video'].items():
 f=round(k[0]/512)
 if not A<=f<B:assert d['video'][k]==h;unchanged+=1
assert unchanged==8115
board=Boards().full();errs=[];selected=[]
wanted={START-1,START,START+1,660,675,690,711,712,713,872,873}
for n,im in frames(DEST):
 if START<=n<873:
  err=float(np.abs(cv2.resize(im,(640,360)).astype(np.int16)-cv2.resize(board,(640,360)).astype(np.int16)).mean());errs.append(err)
 if n in wanted:selected.append((n,im.copy()))
 if n>=873:break
assert max(errs)<5,max(errs)
sheet=Image.new('RGB',(1280,((len(selected)+2)//3)*264),'white');draw=ImageDraw.Draw(sheet)
for i,(n,im) in enumerate(selected):
 x=i%3*426;y=i//3*264;sheet.paste(Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)).resize((426,240)),(x,y));draw.text((x+5,y+243),f'{n/30:.3f}s / f{n}',fill='black')
sheet.save(OUT/'opening-after.jpg')
cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions'),'--max-island','12']
for f in [A,START,619,B,873]:cmd+=['--boundary',str(f)]
subprocess.run(cmd,check=True)
qa={'frames':len(d['video']),'unchanged_video_packets':unchanged,'audio_packets_identical':len(d['audio']),'board_verified_all_frames':[START,873],'max_board_frame_error':max(errs),'transition_guard':'pass','duration_seconds':8458/30}
(OUT/'qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa,indent=2))
