import sys,json,subprocess
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
sys.path.insert(0,str(Path.cwd()/'scripts/video'))
from build_embeddings_v7 import *
m=json.loads((OUT/'edit-manifest.json').read_text());snapshot,old,renderers,specs,mapped=setup()
rd=Reader(snapshot);cap=cv2.VideoCapture(str(DEST));fps=cap.get(cv2.CAP_PROP_FPS)
assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
count=0;errors=[];graphics=0;board_samples=0;preview=[];rings=[]
(OUT/'encoded').mkdir(exist_ok=True)
save={s['output_frame'] for s in m['prepared_states']};save|={0,7996,7525,7526,7527,7634,7635,7636}
for f in m['boundaries']:save|={f-1,f,f+1}
for n in [1470,1680,4500,6150,7530,7680,7770,7950]:
 if any(a<=n<b for a,b in KEEP):save.add(output_frame(n))
checks=set(save)
for f in m['boundaries']:checks|=set(range(f-12,f+13))
frames=mapping()
while True:
 ok,im=cap.read()
 if not ok:break
 n=frames[count];item=mapped[n];geo=[];base=None
 if item and count%30!=0 and count not in checks:
  count+=1;continue
 if item:
  ref,base,geo=renderers[item[0]].at(item[1]);board_samples+=1
 else:ref=rd.at(n);graphics+=1
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
cap.release();rd.c.release();assert count==7997 and fps==30;assert max(errors)<5,max(errors)
a=readwav(OUT/'source.wav');e=readwav(OUT/'edited.wav');cursor=0
for i,(start,end) in enumerate(AUDIO_KEEP):
 length=end-start;lo=240 if i else 0;hi=length-(240 if i<len(AUDIO_KEEP)-1 else 0)
 assert np.array_equal(e[cursor+lo:cursor+hi],a[start+lo:start+hi]);cursor+=length
ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-v','error','-i',str(DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le','-y',str(OUT/'encoded.wav')],check=True)
enc=readwav(OUT/'encoded.wav');assert abs(len(enc)-len(e))<1024;enc=enc[:len(e)]
snr=float(10*np.log10(np.mean(e*e)/np.mean((enc-e)**2)));corr=float(np.corrcoef(enc,e)[0,1]);assert snr>25 and corr>.99
assert all(sha(Path(p))==h for p,h in m['protected'].items())
result=dict(decoded_frames=count,fps=fps,duration=count/fps,all_original_graphics_compared=True,graphics_frames_compared=graphics,board_frames_compared=board_samples,maximum_pixel_mae=max(errors),mean_pixel_mae=float(np.mean(errors)),pcm_exact_outside_5ms_ramps=True,encoded_audio_snr_db=snr,encoded_audio_correlation=corr,protected_files_unchanged=True,candidate_sha256=sha(DEST),encoded_frames=preview,ring_checks=rings)
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k not in ['encoded_frames','ring_checks']},flush=True)
# Save the two exact encoded join excerpts for the owner's listening review.
for label,start,dur in [('recap-join',103,8),('phrase-join',248.5,5.5)]:
 subprocess.run([ff,'-v','error','-i',str(DEST),'-ss',str(start),'-t',str(dur),'-vn','-ac','1','-ar','48000','-c:a','libmp3lame','-b:a','192k','-y',str(OUT/(label+'.mp3'))],check=True)
cmd=[sys.executable,'scripts/video/transition_guard.py',str(DEST),'--outdir',str(OUT/'guard')]
for f in m['boundaries']:cmd+=['--boundary',str(f)+':retained-or-new-splice']
subprocess.run(cmd,check=True)
