from pathlib import Path
import sys,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'scripts/video'))
from build_how_ai_answers_v9 import OUT,DEST,TOTAL,CUT_A,CUT_B,REMOVED,TITLE_START
from editspec_build import Reader,sha
from build_embeddings_v7 import Renderer
m=json.loads((OUT/'edit-manifest.json').read_text())
spec=json.loads((OUT/'leg-b2.json').read_text());r=Renderer(spec)
title=cv2.imread(str(OUT/'inference-title.png'));previous=Reader(ROOT/'Prompts/how-ai-answers-v8.mp4')
cap=cv2.VideoCapture(str(DEST));assert cap.get(cv2.CAP_PROP_FPS)==30
assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
(OUT/'encoded').mkdir(exist_ok=True)
save={0,2251,2252,2400,2516,2517,6100,TITLE_START-1,TITLE_START,TITLE_START+30,CUT_A-1,CUT_A,CUT_A+1,CUT_A+9,CUT_A+10,CUT_A+30,TOTAL-1}
for b in m['boundaries']:save|={b-1,b,b+1}
checks=set(save)|set(range(0,TOTAL,60))
for b in m['boundaries']:checks.update(range(b-20,b+21))
checks.update(range(2252,2517));checks.update(range(TITLE_START,TOTAL))
errors=[];paths=[];counts={'banner':0,'title':0,'unchanged':0};n=0
while True:
 ok,im=cap.read()
 if not ok:break
 if n in checks:
  sf=n if n<CUT_A else n+REMOVED
  if 2252<=n<2517:ref,_,_=r.at(n-1472);label='banner'
  elif TITLE_START<=n<CUT_A:ref=title;label='title'
  else:ref=previous.at(max(7319,sf) if n>=CUT_A else sf);label='unchanged'
  e=float(np.abs(im.astype(np.int16)-ref.astype(np.int16)).mean());errors.append(e);counts[label]+=1
  if n in save:
   p=OUT/'encoded'/f'{n:05d}-{label}.jpg';cv2.imwrite(str(p),im);paths.append(str(p))
 n+=1
cap.release();previous.c.release();assert n==TOTAL;assert max(errors)<5,max(errors)
ff=imageio_ffmpeg.get_ffmpeg_exe()
raw=subprocess.check_output([ff,'-v','error','-i',str(DEST),'-vn','-ar','48000','-ac','2','-f','f32le','pipe:1'])
a=np.frombuffer(raw,np.float32).reshape(-1,2)[:TOTAL*1600];ref=np.fromfile(OUT/'audio-reference.f32',np.float32).reshape(-1,2)
assert a.shape==ref.shape
snr=float(10*np.log10(np.sum(ref.astype(float)**2)/np.sum((a-ref).astype(float)**2)));corr=float(np.corrcoef(a[::10,0],ref[::10,0])[0,1]);assert corr>.999
join=CUT_A*1600
quiet=[]
for t in np.arange(CUT_A/30-.15,CUT_A/30+.65,.05):
 q=a[round(t*48000):round((t+.05)*48000)];quiet.append({'start':round(float(t),3),'rms_dbfs':round(float(20*np.log10(np.sqrt(np.mean(q*q))+1e-12)),2)})
assert all(sha(Path(p))==h for p,h in m['protected'].items())
result=dict(decoded_frames=n,duration=n/30,fps=30,frame_comparisons=counts,max_pixel_mae=max(errors),mean_pixel_mae=float(np.mean(errors)),audio_reference_correlation=corr,audio_reference_snr_db=snr,join_output_seconds=CUT_A/30,join_rms=quiet,protected_files_unchanged=True,candidate_sha256=sha(DEST),encoded_frames=paths,listening_performed=False)
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k not in ['encoded_frames','join_rms']},flush=True)
old=json.loads((ROOT/'video-audit/understand-ai-section-review-2026-09-27/transcripts/how-ai-answers.json').read_text())
segs=[]
for s in old['segments']:
 if s['end']<=CUT_A/30:segs.append(s)
 elif s['start']>=CUT_B/30:segs.append(dict(start=s['start']-REMOVED/30,end=s['end']-REMOVED/30,text=s['text']))
(OUT/'transcript-mapped.json').write_text(json.dumps({'method':'Source ASR segments mapped through exact approved cuts; approximate timestamps, not fresh ASR.','segments':segs},indent=2)+'\n')
(OUT/'transcript-mapped.txt').write_text('\n'.join(f"{s['start']:.2f}–{s['end']:.2f} {s['text']}" for s in segs)+'\n')
cmd=[sys.executable,'scripts/video/transition_guard.py',str(DEST),'--outdir',str(OUT/'guard'),'--handle','20','--max-island','20']
for b in m['boundaries']:cmd+=['--boundary',str(b)+':repair-cut']
subprocess.run(cmd,check=True)
