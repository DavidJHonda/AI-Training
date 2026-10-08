from pathlib import Path
import cv2,concurrent.futures
ROOT=Path.cwd();OUT=ROOT/'video-audit/work-with-ai-illustration-opportunities-2026-10-08'
jobs={'art-of-prompting':[(104,124),(142,149)],'context-window':[(184,202)],'evaluate-the-results':[(168,178),(230,238)],'where-ai-works-best':[(72,86),(105,118)],'your-home-base':[(164,184)]}
def run(item):
 slug,spans=item;cap=cv2.VideoCapture(str(ROOT/'course-assets'/slug/(slug+'.mp4')));fps=cap.get(cv2.CAP_PROP_FPS);targets={round(t*fps):t for a,b in spans for t in range(a,b)};dest=OUT/slug/'detail';dest.mkdir(exist_ok=True);i=0;cells={a:[] for a,b in spans}
 while i<=max(targets):
  ok,f=cap.read()
  if not ok:break
  if i in targets:
   t=targets[i];cv2.imwrite(str(dest/f'{t:03}.jpg'),f,[cv2.IMWRITE_JPEG_QUALITY,90]);cell=cv2.resize(f,(426,240));cell=cv2.copyMakeBorder(cell,24,0,0,0,cv2.BORDER_CONSTANT,value=(30,30,30));cv2.putText(cell,f'{t//60}:{t%60:02}',(8,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1)
   for a,b in spans:
    if a<=t<b:cells[a].append(cell)
  i+=1
 for a,cc in cells.items():
  while len(cc)%3:cc.append(cc[-1]*0)
  cv2.imwrite(str(dest/f'sequence-{a}.jpg'),cv2.vconcat([cv2.hconcat(cc[k:k+3]) for k in range(0,len(cc),3)]))
 cap.release();print(slug,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(run,jobs.items()))
