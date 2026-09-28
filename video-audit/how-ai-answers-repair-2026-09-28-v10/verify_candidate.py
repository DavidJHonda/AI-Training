from pathlib import Path
import sys,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'scripts/video'))
from build_how_ai_answers_v10 import OUT,DEST,TOTAL,INSERT,ADDED,RING_START
from editspec_build import Reader,sha
from build_embeddings_v7 import Renderer
m=json.loads((OUT/'edit-manifest.json').read_text());b1=Renderer(json.loads((OUT/'leg-b1.json').read_text()));qr=Renderer(json.loads((OUT/'leg-question.json').read_text()))
previous=Reader(ROOT/'Prompts/how-ai-answers-v9.mp4');cap=cv2.VideoCapture(str(DEST));assert cap.get(cv2.CAP_PROP_FPS)==30
assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
(OUT/'encoded').mkdir(exist_ok=True)
save={0,1288,1350,1471,2400,INSERT-1,INSERT,RING_START-1,RING_START,RING_START+15,INSERT+ADDED-1,INSERT+ADDED,INSERT+ADDED+1,3200,3227,3250,3270,TOTAL-1}
for b in m['boundaries']:save|={b-1,b,b+1}
checks=set(save)|set(range(0,TOTAL,60))
for b in m['boundaries']:checks.update(range(b-20,b+21))
checks.update(range(1288,1472));checks.update(range(INSERT,INSERT+ADDED));checks.update(range(m['close_output_start'],TOTAL))
errors=[];paths=[];counts={'banner':0,'question':0,'retained':0};n=0;ring_checks=[]
while True:
 ok,im=cap.read()
 if not ok:break
 if n in checks:
  geo=[];bg=None
  if 1288<=n<1472:ref,bg,geo=b1.at(n-400);label='banner'
  elif INSERT<=n<INSERT+ADDED:ref,bg,geo=qr.at(n-INSERT);label='question'
  else:ref=previous.at(n if n<INSERT else n-ADDED);label='retained'
  e=float(np.abs(im.astype(np.int16)-ref.astype(np.int16)).mean());errors.append(e);counts[label]+=1
  if n in save:
   p=OUT/'encoded'/f'{n:05d}-{label}.jpg';cv2.imwrite(str(p),im);paths.append(str(p))
  if n in [1350,RING_START+15]:
   for g in geo:
    x0,y0,x1,y1=g['box'];color=np.array(g['color_bgr'],float);widths=[]
    for axis,pos,start,end in [('x',x0,y0,y1),('x',x1,y0,y1),('y',y0,x0,x1),('y',y1,x0,x1)]:
     vals=[]
     for along in np.linspace(start+.3*(end-start),start+.7*(end-start),7):
      c=int(round(pos));a=int(round(along))
      if axis=='x':base=bg[a,c-7:c+8].astype(float);px=im[a,c-7:c+8].astype(float)
      else:base=bg[c-7:c+8,a].astype(float);px=im[c-7:c+8,a].astype(float)
      vec=color-base;den=(vec*vec).sum(axis=1)
      if np.min(den)<3600:continue
      vals.append(float(np.clip(((px-base)*vec).sum(axis=1)/den,0,1).sum()))
     widths.append(float(np.median(vals)) if vals else None)
    ring_checks.append(dict(frame=n,label=label,encoded_side_widths=widths,bounds=g['box']))
 n+=1
cap.release();previous.c.release();assert n==TOTAL;assert max(errors)<5,max(errors)
ff=imageio_ffmpeg.get_ffmpeg_exe();raw=subprocess.check_output([ff,'-v','error','-i',str(DEST),'-vn','-ar','48000','-ac','2','-f','f32le','pipe:1'])
a=np.frombuffer(raw,np.float32).reshape(-1,2)[:TOTAL*1600];ref=np.fromfile(OUT/'audio-reference.f32',np.float32).reshape(-1,2);assert a.shape==ref.shape
snr=float(10*np.log10(np.sum(ref.astype(float)**2)/np.sum((a-ref).astype(float)**2)));corr=float(np.corrcoef(a[::10,0],ref[::10,0])[0,1]);assert corr>.999
joins=[]
for f in [INSERT,INSERT+ADDED,m['close_output_start']]:
 rows=[]
 for t in np.arange(f/30-.1,f/30+.15,.05):
  q=a[round(t*48000):round((t+.05)*48000)];rows.append(dict(start=round(float(t),3),rms_dbfs=round(float(20*np.log10(np.sqrt(np.mean(q*q))+1e-12)),2)))
 joins.append(dict(output_frame=f,output_seconds=f/30,rms_windows=rows))
assert all(sha(Path(p))==h for p,h in m['protected'].items())
result=dict(decoded_frames=n,duration=n/30,fps=30,frame_comparisons=counts,max_pixel_mae=max(errors),mean_pixel_mae=float(np.mean(errors)),audio_reference_correlation=corr,audio_reference_snr_db=snr,audio_joins=joins,ring_checks=ring_checks,protected_files_unchanged=True,candidate_sha256=sha(DEST),encoded_frames=paths,listening_performed=False)
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k not in ['encoded_frames','audio_joins']},flush=True)
old=json.loads((ROOT/'video-audit/how-ai-answers-repair-2026-09-28-v9/transcript-mapped.json').read_text());segs=[]
for s in old['segments']:
 shift=ADDED/30 if s['start']>=INSERT/30 else 0
 segs.append(dict(start=s['start']+shift,end=s['end']+shift,text=s['text']))
segs.append(dict(start=INSERT/30+.15,end=INSERT/30+1.8,text='What should I name my new dog?'))
segs.sort(key=lambda s:s['start'])
(OUT/'transcript-mapped.json').write_text(json.dumps({'method':'Previously retained source ASR mapped through insertion; approximate timings. Fresh changed-span ASR separately.','segments':segs},indent=2)+'\n')
(OUT/'transcript-mapped.txt').write_text('\n'.join(f"{s['start']:.2f}–{s['end']:.2f} {s['text']}" for s in segs)+'\n')
cmd=[sys.executable,'scripts/video/transition_guard.py',str(DEST),'--outdir',str(OUT/'guard'),'--handle','20','--max-island','20']
for b in m['boundaries']:cmd+=['--boundary',str(b)+':repair-boundary']
subprocess.run(cmd,check=True)
