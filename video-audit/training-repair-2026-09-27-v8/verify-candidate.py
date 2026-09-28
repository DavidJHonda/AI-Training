from pathlib import Path
import cv2,json,subprocess,numpy as np,sys,hashlib,wave
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/video'))
from build_training_v7 import Renderer
from editspec_build import Reader
cv2.setNumThreads(1)
m=json.loads((OUT/'edit-manifest.json').read_text());video=Path(m['output']);source=Path(m['source_snapshot']);ff=imageio_ffmpeg.get_ffmpeg_exe()
pics=json.loads((OUT/'frame-map.json').read_text())
def pcm(p):return np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','s16le','-']),dtype='<i2')
original=pcm(source);encoded=pcm(video)
with wave.open(str(OUT/'edited.wav')) as w:edited=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2')
expected=np.concatenate([original[a*1600:b*1600] for a,b in [r['source_frames'] for r in m['rows']]])
assert len(edited)==8132*1600
allowed=np.zeros(len(edited),bool)
for s in m['audio_seams']:j=s['output_frame']*1600;allowed[j-240:j+240]=True
assert np.array_equal(edited[~allowed],expected[~allowed])
assert 0<=len(encoded)-len(edited)<1024
signal=edited.astype(float);actual=encoded[:len(edited)].astype(float);error=actual-signal
snr=20*np.log10(np.linalg.norm(signal)/np.linalg.norm(error));assert snr>25,snr
encoded_gaps=[]
for s in m['audio_seams']:
 j=s['output_frame']*1600
 window=actual[j-48000:j+48000].reshape(-1,480)
 levels=20*np.log10(np.sqrt(np.mean(window*window,axis=1))/32768+1e-12)
 lo=hi=100
 while lo>0 and levels[lo-1]<-35:lo-=1
 while hi<len(levels) and levels[hi]<-35:hi+=1
 encoded_gaps.append(dict(frame=s['output_frame'],seconds=s['output_seconds'],quiet_gap_seconds=(hi-lo)/100,interval=[s['output_seconds']+(lo-100)/100,s['output_seconds']+(hi-100)/100]))
samples=json.loads((OUT/'preview-samples.json').read_text());byframe={x['frame']:x for x in samples}
renderers={k:Renderer(s) for k,s in m['boards'].items()}
for key,r in renderers.items():
 motion=[f for f,(k,local,sf) in enumerate(pics) if k==key and local>0 and r.cameras[local]!=r.cameras[local-1] and r.geometry(local)[1]]
 if motion:
  for f in [motion[len(motion)//3],motion[2*len(motion)//3]]:
   local=pics[f][1];im,base,geo=r.at(local)
   cv2.imwrite(str(OUT/'preview'/f'{f:05d}-{key}-base.png'),base)
   x=dict(frame=f,key=key,local=local,rings=geo,during_camera_motion=True);samples.append(x);byframe[f]=x
frames=OUT/'encoded-frames';frames.mkdir(exist_ok=True)
selected=set(byframe)|{m['total_frames']-1}
for b in m['boundaries']:selected.update([b['frame']-1,b['frame'],b['frame']+1])
for b in m['notebook_interleaves']:selected.update([b['start']+30,b['end']-30])
needed={n for key,n,sf in pics if key=='drawing'};donors={};src=Reader(source)
for n in sorted(needed):donors[n]=src.at(n)
src.c.release();src=Reader(source)
cap=cv2.VideoCapture(str(video));assert cap.get(cv2.CAP_PROP_FPS)==30
assert [int(cap.get(x)) for x in [cv2.CAP_PROP_FRAME_WIDTH,cv2.CAP_PROP_FRAME_HEIGHT]]==[1280,720]
n=0;unchanged=[];donor_errors=[];preview_errors=[];close=[]
while True:
 ok,im=cap.read()
 if not ok:break
 key,local,sf=pics[n]
 if n in selected:cv2.imwrite(str(frames/f'{n:05d}.png'),im)
 if key=='drawing':donor_errors.append(cv2.norm(im,donors[local],cv2.NORM_L1)/im.size)
 elif key=='source':
  if local<src.n:src.c.release();src=Reader(source)
  base=src.at(local);e=cv2.norm(im,base,cv2.NORM_L1)/im.size;unchanged.append(e)
  if sf>=8402:close.append(e)
 if n in byframe:
  x=byframe[n];ref=renderers[x['key']].at(x['local'])[0];preview_errors.append(cv2.norm(im,ref,cv2.NORM_L1)/im.size)
 n+=1
cap.release();src.c.release();assert n==8132
assert max(donor_errors)<5;assert max(unchanged)<5;assert max(preview_errors)<5
widths=[]
for x in samples:
 if not x['rings']:continue
 im=cv2.imread(str(frames/f"{x['frame']:05d}.png")).astype(float)
 base=cv2.imread(str(OUT/'preview'/f"{x['frame']:05d}-{x['key']}-base.png")).astype(float)
 for ring in x['rings']:
  l,t,r,b=ring['centerline'];cx=int(round((l+r)/2));cy=int(round((t+b)/2));col=np.array(ring['color_bgr']);results={};integrated={}
  for side,ys,xs in [('top',slice(round(t)-6,round(t)+7),cx),('bottom',slice(round(b)-6,round(b)+7),cx),('left',cy,slice(round(l)-6,round(l)+7)),('right',cy,slice(round(r)-6,round(r)+7))]:
   bg=base[ys,xs];vec=col-bg;delta=im[ys,xs]-bg;contrast=np.linalg.norm(vec,axis=1)
   alpha=np.where(contrast>50,np.clip(np.sum(delta*vec,axis=1)/np.maximum(np.sum(vec*vec,axis=1),1),0,1),0)
   results[side]=int((alpha>.5).sum());integrated[side]=round(float(alpha.sum()),3)
  row=dict(frame=x['frame'],key=x['key'],moving=x.get('during_camera_motion',False),half_coverage_pixels=results,integrated_coverage_pixels=integrated)
  widths.append(row);assert all(w==4 for w in results.values()),row
verification=dict(frames=n,fps=30,size=[1280,720],duration=n/30,
 audio=dict(samples=len(edited),samples_per_frame=1600,unaltered_outside_quiet_5ms_edges=True,encoded_padding_samples=len(encoded)-len(edited),encoded_snr_db=float(snr),encoded_seam_gaps=encoded_gaps,auditioned=False),
 ring_measurements=widths,ring_state_count=len(widths),all_measured_sides_4px=True,
 board_runs=m['board_runs'],duration_method='Frame-indexed spans including all zooms, pans and holds; actual decoded boundary frames retained for visual confirmation.',
 longest_board_seconds=m['longest_board_seconds'],longest_board_chain_seconds=m['longest_board_chain_seconds'],
 encoding_errors=dict(retained_picture_max=float(max(unchanged)),retained_picture_mean=float(np.mean(unchanged)),close_mean=float(np.mean(close)),drawing_max=float(max(donor_errors)),board_preview_max=float(max(preview_errors))),
 protected_files_unchanged={p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in m['protected_hashes'].items()},
 checks_not_done=['Real-time full playback/listening','Audible cadence and voice continuity at new and existing joins','Mobile/player playback','Manual scrutiny of every encoded frame'])
assert all(verification['protected_files_unchanged'].values())
(OUT/'verification.json').write_text(json.dumps(verification,indent=2));print(json.dumps({k:v for k,v in verification.items() if k not in ['ring_measurements','protected_files_unchanged','board_runs']},indent=2))
