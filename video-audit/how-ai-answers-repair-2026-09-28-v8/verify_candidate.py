import sys,json,subprocess,hashlib
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
sys.path.insert(0,str(Path.cwd()/'scripts/video'))
from build_how_ai_answers_v8 import *
m=json.loads((OUT/'edit-manifest.json').read_text());snap,boards,specs,rs,mapped,reuse=setup()
rd=Reader(snap);donor_ids=sorted({x[1] for x in mapped if x and x[0] not in rs});donors={f:rd.at(f).copy() for f in donor_ids};rd.c.release();rd=Reader(snap)
cap=cv2.VideoCapture(str(DEST));assert cap.get(cv2.CAP_PROP_FPS)==30;assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
(OUT/'encoded').mkdir(exist_ok=True)
save={s['output_frame'] for s in m['prepared_states']}|{0,TOTAL-1}
for b in m['boundaries']:save|={b-1,b,b+1}
for t in [2,10,12,55,57,84,87,89,92,96,100,126,127,130,133,134,168,171,174,176,180,183,186,195,200,229,231,232,240,245,249,253]:save.add(round(t*30))
# Show donor playback, including freeze point; compare every donor frame below.
for f in range(fr(125.7),fr(127.1),10):save.add(f)
checks=set(save)
for b in m['boundaries']:checks|=set(range(b-20,b+21))
count=0;errors=[];graphics=0;board_samples=0;drawings=0;preview=[];rings=[]
while True:
 ok,im=cap.read()
 if not ok:break
 item=mapped[count];base=None;geo=[]
 if item and item[0] in rs and count%30!=0 and count not in checks:count+=1;continue
 if not item:ref=rd.at(count);graphics+=1
 elif item[0] not in rs:ref=donors[item[1]];drawings+=1
 else:ref,base,geo=rs[item[0]].at(item[1]);board_samples+=1
 errors.append(float(np.abs(im.astype(np.int16)-ref.astype(np.int16)).mean()))
 if count in save:
  name=item[0] if item else 'original';p=OUT/'encoded'/f'{count:05d}-{name}.jpg';cv2.imwrite(str(p),im);preview.append(str(p))
  for g in geo:
   x0,y0,x1,y1=g['box'];color=np.array(g['color_bgr'],float);sides=[]
   for axis,pos,start,end in [('x',x0,y0,y1),('x',x1,y0,y1),('y',y0,x0,x1),('y',y1,x0,x1)]:
    vals=[]
    for along in np.linspace(start+.3*(end-start),start+.7*(end-start),7):
     c=int(round(pos));a=int(round(along))
     if axis=='x':bg=base[a,c-7:c+8].astype(float);pixels=im[a,c-7:c+8].astype(float)
     else:bg=base[c-7:c+8,a].astype(float);pixels=im[c-7:c+8,a].astype(float)
     vector=color-bg;den=(vector*vector).sum(axis=1)
     if np.min(den)<3600:continue
     vals.append(float(np.clip(((pixels-bg)*vector).sum(axis=1)/den,0,1).sum()))
    sides.append(float(np.median(vals)) if vals else None)
   rings.append(dict(frame=count,board=item[0],effective_side_widths=sides))
 count+=1
cap.release();rd.c.release();assert count==TOTAL;assert max(errors)<5,max(errors)
# Copy-stream and PCM identities certify unchanged audio, not perceptual quality.
ff=imageio_ffmpeg.get_ffmpeg_exe();ah={};ph={}
for key,path in [('source',snap),('candidate',DEST)]:
 raw=subprocess.check_output([ff,'-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1']);ah[key]=hashlib.sha256(raw).hexdigest()
 pcm=subprocess.check_output([ff,'-v','error','-i',str(path),'-map','0:a:0','-f','s16le','-acodec','pcm_s16le','pipe:1']);ph[key]=hashlib.sha256(pcm).hexdigest()
assert ah['source']==ah['candidate'] and ph['source']==ph['candidate']
assert all(sha(Path(p))==h for p,h in m['protected'].items())
widths=[v for r in rings for v in r['effective_side_widths'] if v is not None]
# Every active ring is checked by Renderer bounds assertions during render. Confirm complete group camera coverage in settled views.
camera_checks=[]
for key,rects in [('b1',[[80,280,414,872],[448,280,782,872],[816,280,1150,872],[1184,280,1518,872]]),('b3',[[80,280,600,958],[1000,280,1520,958]])]:
 ox,oy=boards[key]['canvas_offset'];r=rs[key]
 for sec,rect in zip(([18,23,28,35] if key=='b1' else [110,140]),rects):
  from ken_burns_path import window
  cx,cy,cw=r.cameras[fr(sec)-SPANS[key][0]];x,y,w,h=window(cx,cy,cw,16/9,r.iw,r.ih)
  rx,ry,rz,rw=rect;assert x<=rx+ox and y<=ry+oy and x+w>=rz+ox and y+h>=rw+oy
  camera_checks.append({'board':key,'seconds':sec,'complete_group_visible':True})
result=dict(decoded_frames=count,fps=30,duration=count/30,graphics_frames_compared=graphics,drawing_reuse_frames_compared=drawings,board_frames_compared=board_samples,maximum_pixel_mae=max(errors),mean_pixel_mae=float(np.mean(errors)),audio_stream_sha256=ah,decoded_audio_sha256=ph,audio_stream_identical=True,decoded_audio_identical=True,protected_files_unchanged=True,candidate_sha256=sha(DEST),encoded_frames=preview,ring_checks=rings,ring_width_summary=dict(sides=len(widths),median=float(np.median(widths)),minimum=min(widths),maximum=max(widths)),complete_group_camera_checks=camera_checks)
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k not in ['encoded_frames','ring_checks']},flush=True)
cmd=[sys.executable,'scripts/video/transition_guard.py',str(DEST),'--outdir',str(OUT/'guard'),'--handle','20','--max-island','20']
for b in m['boundaries']:cmd+=['--boundary',str(b)+':source-or-repair-cut']
r=subprocess.run(cmd);print('Guard status',r.returncode,'— inspect all strips and motion.',flush=True)
