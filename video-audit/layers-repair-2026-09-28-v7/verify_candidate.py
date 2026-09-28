import sys,json,subprocess
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
sys.path.insert(0,str(Path.cwd()/'scripts/video'))
from build_layers_v7 import *
m=json.loads((OUT/'edit-manifest.json').read_text());snapshot,old,frames,mapped,specs,renderers,drawing=setup()
rd=Reader(snapshot);cap=cv2.VideoCapture(str(DEST));assert cap.get(cv2.CAP_PROP_FPS)==30;assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
(OUT/'encoded').mkdir(exist_ok=True)
save={s['output_frame'] for s in m['prepared_states']}|{0,len(frames)-1}
for b in m['boundaries']:save|={b-1,b,b+1}
for t in [2,46,49,60,63,76,79,81,103,107,136,140,150,155,160,166,170,178,185,190,195]:save.add(round(t*30))
checks=set(save)
for b in m['boundaries']:checks|=set(range(b-12,b+13))
count=0;errors=[];graphics=0;board_samples=0;drawings=0;preview=[];rings=[]
while True:
 ok,im=cap.read()
 if not ok:break
 item=mapped[count];base=None;geo=[]
 if item and item[0]!='drawing' and count%30!=0 and count not in checks:count+=1;continue
 if not item:ref=rd.at(frames[count]);graphics+=1
 elif item[0]=='drawing':ref=drawing;drawings+=1
 else:ref,base,geo=renderers[item[0]].at(item[1]);board_samples+=1
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
cap.release();rd.c.release();assert count==m['frames'];assert max(errors)<5,max(errors)
a=readwav(OUT/'source.wav');e=readwav(OUT/'edited.wav');d=readwav(OUT/'donor-matched.wav')
assert np.array_equal(e[:INSERT*SPF-FADE],a[:INSERT*SPF-FADE])
assert np.array_equal(e[(INSERT+EXTRA)*SPF+FADE:],a[INSERT*SPF+FADE:TOTAL*SPF])
assert np.array_equal(e[INSERT*SPF+FADE:(INSERT+EXTRA)*SPF-FADE],d[FADE:-FADE])
ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-v','error','-i',str(DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le','-y',str(OUT/'encoded.wav')],check=True)
enc=readwav(OUT/'encoded.wav');assert abs(len(enc)-len(e))<1024;enc=enc[:len(e)]
snr=float(10*np.log10(np.mean(e*e)/np.mean((enc-e)**2)));corr=float(np.corrcoef(enc,e)[0,1]);assert snr>25 and corr>.99
assert all(sha(Path(p))==h for p,h in m['protected'].items())
result=dict(decoded_frames=count,fps=30,duration=count/30,graphics_frames_compared=graphics,drawing_reuse_frames_compared=drawings,board_frames_compared=board_samples,maximum_pixel_mae=max(errors),mean_pixel_mae=float(np.mean(errors)),source_pcm_exact_outside_join_ramps=True,donor_pcm_exact_to_matched_clip_outside_join_ramps=True,encoded_audio_snr_db=snr,encoded_audio_correlation=corr,protected_files_unchanged=True,candidate_sha256=sha(DEST),encoded_frames=preview,ring_checks=rings)
(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items() if k not in ['encoded_frames','ring_checks']},flush=True)
subprocess.run([ff,'-v','error','-i',str(DEST),'-ss','102','-t','16','-vn','-ac','1','-ar','48000','-c:a','libmp3lame','-b:a','192k','-y',str(OUT/'join-review.mp3')],check=True)
r=subprocess.run([ff,'-v','info','-i',str(DEST),'-ss','102','-t','16','-vn','-af','silencedetect=noise=-35dB:d=0.10','-f','null','-'],capture_output=True,text=True,check=True);(OUT/'silence-detection.log').write_text(r.stderr)
cmd=[sys.executable,'scripts/video/transition_guard.py',str(DEST),'--outdir',str(OUT/'guard')]
for b in m['boundaries']:cmd+=['--boundary',str(b)+':original-or-new-boundary']
r=subprocess.run(cmd);print('Guard status',r.returncode,'— inspect all strips and any motion flags.',flush=True)
