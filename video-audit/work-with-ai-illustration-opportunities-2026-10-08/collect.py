from pathlib import Path
import re,json,hashlib,cv2,concurrent.futures
ROOT=Path.cwd(); OUT=ROOT/'video-audit/work-with-ai-illustration-opportunities-2026-10-08'
slugs=['work-with-ai-opener','ai-is-different','where-ai-works-best','your-home-base','questions-matter','art-of-prompting','context-window','evaluate-the-results','critical-thinking']
def collect(slug):
 p=ROOT/'course-assets'/slug/(slug+'.mp4'); dest=OUT/slug;dest.mkdir(exist_ok=True)
 cap=cv2.VideoCapture(str(p));fps=cap.get(cv2.CAP_PROP_FPS);n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));cells=[];sheet=0;i=0;target=0
 while True:
  ok,frame=cap.read()
  if not ok:break
  if i>=target:
   t=i/fps; target+=round(fps*6)
   cell=cv2.resize(frame,(384,216)); cell=cv2.copyMakeBorder(cell,24,0,0,0,cv2.BORDER_CONSTANT,value=(30,30,30));cv2.putText(cell,f'{int(t)//60}:{t%60:05.2f}',(8,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1,cv2.LINE_AA);cells.append(cell)
   if len(cells)==20:
    cv2.imwrite(str(dest/f'sheet-{sheet:02}.jpg'),cv2.vconcat([cv2.hconcat(cells[k:k+4]) for k in range(0,20,4)]));sheet+=1;cells=[]
  i+=1
 if cells:
  while len(cells)%4:cells.append(cells[-1]*0)
  cv2.imwrite(str(dest/f'sheet-{sheet:02}.jpg'),cv2.vconcat([cv2.hconcat(cells[k:k+4]) for k in range(0,len(cells),4)]))
 cap.release()
 meta={'slug':slug,'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'fps':fps,'frames':n,'decoded_frames':i,'duration':n/fps,'sample_interval_seconds':6}
 (dest/'source.json').write_text(json.dumps(meta,indent=2)); print(json.dumps(meta),flush=True);return meta
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: rows=list(ex.map(collect,slugs))
(OUT/'sources.json').write_text(json.dumps(rows,indent=2))
