import sys,json,subprocess,re
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
sys.path.insert(0,str(Path.cwd()/'scripts/video'))
from build_transformer_v12 import *
m=json.loads((OUT/'edit-manifest.json').read_text());snapshot,old,rows,frames,mapped,specs,renderers=setup()
rd=Reader(snapshot);cap=cv2.VideoCapture(str(DEST));fps=cap.get(cv2.CAP_PROP_FPS)
assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
(OUT/'encoded').mkdir(exist_ok=True)
save={s['output_frame'] for s in m['prepared_states']};save|={0,len(frames)-1}
for f in m['boundaries']:save|={f-1,f,f+1}
# Every retained illustration scene plus all audio seams and board highlight states.
for sec in [6,12,20,40,55,85,90,105,138,143,169,175,180,185,190,218,222,225]:save.add(output_frame(round(sec*30)))
checks=set(save)
for f in m['boundaries']:checks|=set(range(max(0,f-12),min(len(frames),f+13)))
count=0;errors=[];graphics=0;board_samples=0;preview=[];rings=[]
while True:
 ok,im=cap.read()
 if not ok:break
 f=frames[count];item=mapped[count];geo=[];base=None
 if item and count%30!=0 and count not in checks:count+=1;continue
 if item:ref,base,geo=renderers[item[0]].at(item[1]);board_samples+=1
 else:ref=rd.at(f);graphics+=1
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
     coverage=np.clip(((pixels-bg)*vector).sum(axis=1)/den,0,1);vals.append(float(coverage.sum()))
    sides.append(float(np.median(vals)) if vals else None)
   rings.append(dict(frame=count,board=item[0],effective_side_widths=sides))
 count+=1
cap.release();rd.c.release();assert count==m['frames'] and fps==30;assert max(errors)<5,max(errors)
a=readwav(OUT/'source.wav');e=readwav(OUT/'edited.wav')
for i,r in enumerate(rows):
 start=r['start_frame']*SPF;end=r['end_frame']*SPF;src=r['source_start']*SPF;length=end-start
 lo=FADE if i else 0;hi=length-(FADE if i<len(rows)-1 else 0)
 assert np.array_equal(e[start+lo:start+hi],a[src+lo:src+hi])
ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-v','error','-i',str(DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le','-y',str(OUT/'encoded.wav')],check=True)
enc=readwav(OUT/'encoded.wav');assert abs(len(enc)-len(e))<1024;enc=enc[:len(e)]
snr=float(10*np.log10(np.mean(e*e)/np.mean((enc-e)**2)));corr=float(np.corrcoef(enc,e)[0,1]);assert snr>25 and corr>.99
assert all(sha(Path(p))==h for p,h in m['protected'].items())
result=dict(decoded_frames=count,fps=fps,duration=count/fps,all_original_graphics_compared=True,graphics_frames_compared=graphics,board_frames_compared=board_samples,maximum_pixel_mae=max(errors),mean_pixel_mae=float(np.mean(errors)),pcm_exact_to_source_mapping_outside_5ms_ramps=True,encoded_audio_snr_db=snr,encoded_audio_correlation=corr,protected_files_unchanged=True,candidate_sha256=sha(DEST),encoded_frames=preview,ring_checks=rings)
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k not in ['encoded_frames','ring_checks']},flush=True)
# Exact encoded review excerpt and measured quiet gaps in the repaired passage.
subprocess.run([ff,'-v','error','-i',str(DEST),'-ss','145','-t','30','-vn','-ac','1','-ar','48000','-c:a','libmp3lame','-b:a','192k','-y',str(OUT/'repaired-section.mp3')],check=True)
r=subprocess.run([ff,'-v','info','-i',str(DEST),'-ss','145','-t','30','-vn','-af','silencedetect=noise=-35dB:d=0.10','-f','null','-'],capture_output=True,text=True,check=True)
(OUT/'silence-detection.log').write_text(r.stderr)
seams=[]
for row in rows[1:]:
 t=row['start_frame']/FPS;n=row['start_frame']*SPF
 seams.append(dict(output_seconds=t,label=row['label'],peak_step_at_pcm_join=float(abs(e[n]-e[n-1])),pre_20ms_rms=float(np.sqrt(np.mean(e[n-960:n]**2))),post_20ms_rms=float(np.sqrt(np.mean(e[n:n+960]**2)))))
(OUT/'audio-seams.json').write_text(json.dumps(seams,indent=2)+'\n')
cmd=[sys.executable,'scripts/video/transition_guard.py',str(DEST),'--outdir',str(OUT/'guard')]
for f in m['boundaries']:cmd+=['--boundary',str(f)+':retained-or-reread-splice']
subprocess.run(cmd,check=True)
