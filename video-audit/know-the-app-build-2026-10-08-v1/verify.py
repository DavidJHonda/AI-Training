from pathlib import Path
import cv2,json,subprocess,hashlib,imageio_ffmpeg
ROOT=Path.cwd();OUT=Path(__file__).resolve().parent;M=json.loads((OUT/'edit-manifest.json').read_text());p=Path(M['output']);cap=cv2.VideoCapture(str(p));fps=cap.get(cv2.CAP_PROP_FPS);reported=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));n=0;cells=[];cuts={b['frame'] for b in M['boundaries']};frames={}
while True:
 ok,im=cap.read()
 if not ok:break
 if n%180==0:
  cell=cv2.resize(im,(384,216));cell=cv2.copyMakeBorder(cell,24,0,0,0,cv2.BORDER_CONSTANT,value=(30,30,30));cv2.putText(cell,f'{n/30:.2f}s / f{n}',(8,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1);cells.append(cell)
 if n in {k+d for k in cuts for d in [-1,0,1]}:frames[n]=im.copy()
 last=im;n+=1
cap.release();assert n==reported==M['total_frames'],(n,reported)
for j in range(0,len(cells),20):
 cc=cells[j:j+20]
 while len(cc)%4:cc.append(cc[-1]*0)
 cv2.imwrite(str(OUT/f'candidate-sheet-{j//20}.jpg'),cv2.vconcat([cv2.hconcat(cc[k:k+4]) for k in range(0,len(cc),4)]))
cv2.imwrite(str(OUT/'final-frame.jpg'),last)
strips=[]
for k in sorted(cuts):
 row=[]
 for f in [k-1,k,k+1]:
  cell=cv2.resize(frames[f],(384,216));cv2.putText(cell,f'f{f}',(8,20),cv2.FONT_HERSHEY_SIMPLEX,.55,(0,0,220),2);row.append(cell)
 strips.append(cv2.hconcat(row))
for j in range(0,len(strips),7):cv2.imwrite(str(OUT/f'joins-{j//7}.jpg'),cv2.vconcat(strips[j:j+7]))
ff=imageio_ffmpeg.get_ffmpeg_exe()
def audio_hash(path):
 r=subprocess.run([ff,'-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-'],capture_output=True,text=True,check=True);return r.stdout.strip()
h1=audio_hash(Path(M['source']));h2=audio_hash(p);assert h1==h2
q=dict(frames=n,fps=fps,duration=n/fps,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),audio_stream_identical=h1==h2,audio_hash=h2,board_assets_unchanged=all(hashlib.sha256((ROOT/b['asset']).read_bytes()).hexdigest()==b['sha256'] for b in M['boards'].values()),continuous_audiovisual_review=False)
(OUT/'qa.json').write_text(json.dumps(q,indent=2));print(q,flush=True)
cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(p),'--outdir',str(OUT/'transitions')]
for b in M['boundaries']:cmd+=['--boundary',f'{b["frame"]}:{b["label"]}']
subprocess.run(cmd,check=True)
