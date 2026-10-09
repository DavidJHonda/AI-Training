from pathlib import Path
import cv2,json
ROOT=Path.cwd();OUT=ROOT/'video-audit/build-your-skills-illustration-opportunities-2026-10-08'
jobs={'people-skills':list(range(0,29,2)),'curious-and-flexible':list(range(0,36,2)),'make-your-move':list(range(270,280))}
bounds={}
for slug,times in jobs.items():
 cap=cv2.VideoCapture(str(ROOT/'course-assets'/slug/(slug+'.mp4')));dest=OUT/slug/'detail';dest.mkdir(exist_ok=True);cells=[];prev=None;cuts=[]
 for i in range((max(times)+1)*30):
  ok,f=cap.read()
  if not ok:break
  small=cv2.resize(f,(160,90)).astype('float32')
  if prev is not None:
   delta=abs(small-prev).mean()
   if delta>15 and i>min(times)*30:cuts.append([i,round(float(delta),2)])
  prev=small
  if i%30==0 and i//30 in times:
   t=i//30;cv2.imwrite(str(dest/f'{t:03}.jpg'),f);cell=cv2.resize(f,(426,240));cell=cv2.copyMakeBorder(cell,24,0,0,0,cv2.BORDER_CONSTANT,value=(30,30,30));cv2.putText(cell,f'{t//60}:{t%60:02}',(8,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1);cells.append(cell)
 while len(cells)%3:cells.append(cells[-1]*0)
 cv2.imwrite(str(dest/'sequence.jpg'),cv2.vconcat([cv2.hconcat(cells[k:k+3]) for k in range(0,len(cells),3)]));cap.release();bounds[slug]=cuts
(OUT/'detail-boundaries.json').write_text(json.dumps(bounds,indent=2));print(json.dumps(bounds))
