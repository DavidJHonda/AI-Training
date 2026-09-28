import sys,json,subprocess
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
sys.path.insert(0,str(Path.cwd()/'scripts/video'))
from build_tokens_v9 import *
m=json.loads((OUT/'edit-manifest.json').read_text())
snapshot,old,renderers,specs,mapped,chart=setup()
rd=Reader(snapshot);cap=cv2.VideoCapture(str(DEST));fps=cap.get(cv2.CAP_PROP_FPS)
count=0;errs=[];graphics=0;board_samples=0;previews=[];ring_checks=[];sample_frames=set()
(OUT/'encoded').mkdir(exist_ok=True)
for s in m['prepared_states']:
 for out,n in enumerate(mapping()):
  if mapped[n] and mapped[n][0]==s['key']:
   local=out-SPLITS_IN if s['key']=='5-splits' else mapped[n][1]
   if local==s['local_frame']:sample_frames.add(out);break
sample_frames|={output_frame(n) for n in range(3720,4070,15)}
boundaries=[309,945,975,1947,3423,3453,3715,4070,4319,5450,6168,6198,6285,6426,7181,7187,7804,7834,8037]
save_frames=set(sample_frames)
for f in boundaries:
 save_frames|={f-1,f,f+1}
 sample_frames|=set(range(f-12,f+13))
source_map=mapping()
while True:
 ok,im=cap.read()
 if not ok:break
 n=source_map[count];item=mapped[n];geo=[];base=None
 if item and count%30!=0 and count not in sample_frames:
  count+=1;continue
 if item:
  key,local=item
  if key=='5-splits':local=count-SPLITS_IN
  ref,base,geo=renderers[key].at(local);board_samples+=1
 else:ref=chart.at(rd.at(n),n)[0];graphics+=1
 err=float(np.abs(im.astype(np.int16)-ref.astype(np.int16)).mean());errs.append(err)
 if count in save_frames:
  name=item[0] if item else 'original-graphic'
  p=OUT/'encoded'/f'{count:05d}-{name}.jpg';cv2.imwrite(str(p),im);previews.append(str(p))
  # Equivalent solid-pixel coverage across straight sides. Uses the measured
  # rendered ring geometry and unchanged board pixels as background reference.
  for g in geo:
   x0,y0,x1,y1=g['box'];color=np.array(g['color_bgr'],float);rows=[]
   for axis,pos,start,end in [('x',x0,y0,y1),('x',x1,y0,y1),('y',y0,x0,x1),('y',y1,x0,x1)]:
    vals=[]
    for along in np.linspace(start+.25*(end-start),start+.75*(end-start),7):
     c=int(round(pos));a=int(round(along))
     if axis=='x':bg=base[a,c-7:c+8].astype(float);pixels=im[a,c-7:c+8].astype(float)
     else:bg=base[c-7:c+8,a].astype(float);pixels=im[c-7:c+8,a].astype(float)
     vector=color-bg;den=(vector*vector).sum(axis=1)
     coverage=np.clip(((pixels-bg)*vector).sum(axis=1)/np.maximum(den,1),0,1)
     vals.append(float(coverage.sum()))
    rows.append(float(np.median(vals)))
   ring_checks.append(dict(frame=count,board=item[0],effective_side_widths=rows))
 count+=1
cap.release();rd.c.release()
assert count==8157 and fps==30,(count,fps)
assert max(errs)<5,max(errs)
a=readwav(OUT/'source.wav');e=readwav(OUT/'edited.wav');cursor=0
for i,(start,end) in enumerate(KEEP):
 length=(end-start)*SPF;lo=240 if i else 0;hi=length-(240 if i<len(KEEP)-1 else 0)
 assert np.array_equal(e[cursor+lo:cursor+hi],a[start*SPF+lo:start*SPF+hi]);cursor+=length
ff=imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff,'-v','error','-i',str(DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le','-y',str(OUT/'encoded.wav')],check=True)
encoded=readwav(OUT/'encoded.wav');assert abs(len(encoded)-len(e))<1024
enc=encoded[:len(e)].astype(float);ref=e.astype(float)
snr=float(10*np.log10(np.mean(ref*ref)/np.mean((enc-ref)**2)));corr=float(np.corrcoef(enc,ref)[0,1]);assert snr>25 and corr>.99,(snr,corr)
assert all(sha(Path(p))==v for p,v in m['protected'].items())
result=dict(decoded_frames=count,fps=fps,duration=count/fps,all_frames_decoded=True,board_frames_reference_compared=board_samples,all_original_graphic_frames_compared=True,original_graphic_frames_compared=graphics,maximum_pixel_mae=max(errs),mean_pixel_mae=float(np.mean(errs)),pcm_exact_outside_5ms_join_ramps=True,encoded_audio_snr_db=snr,encoded_audio_correlation=corr,protected_files_unchanged=True,ring_checks=ring_checks,candidate_sha256=sha(DEST),encoded_frames=previews)
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print({k:v for k,v in result.items() if k not in ['encoded_frames','ring_checks']},flush=True)
cmd=[sys.executable,'scripts/video/transition_guard.py',str(DEST),'--outdir',str(OUT/'guard')]
for f in boundaries:cmd+=['--boundary',str(f)+':edit-boundary']
subprocess.run(cmd,check=True)
