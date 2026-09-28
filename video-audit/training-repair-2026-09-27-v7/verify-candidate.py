from pathlib import Path
import cv2,json,subprocess,numpy as np,sys,hashlib
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/video'))
from build_training_v7 import mapping,Renderer
cv2.setNumThreads(1)
m=json.loads((OUT/'edit-manifest.json').read_text());video=Path(m['output']);source=Path(m['source_snapshot']);ff=imageio_ffmpeg.get_ffmpeg_exe()
old=json.loads((ROOT/'video-audit/training-comparison-2026-09-22/build-v6/edit-manifest.json').read_text());mapped=mapping(old)
def audiohash(p,decoded):
 return subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a:0','-c:a','pcm_s16le' if decoded else 'copy','-f','hash','-hash','sha256','-'],text=True).strip()
audio={k:audiohash(p,decoded) for k,p,decoded in [('packet_source',source,False),('packet_candidate',video,False),('pcm_source',source,True),('pcm_candidate',video,True)]}
assert audio['packet_source']==audio['packet_candidate'];assert audio['pcm_source']==audio['pcm_candidate']
samples=json.loads((OUT/'preview-samples.json').read_text());byframe={x['frame']:x for x in samples}
# Include actual encoded ring widths during camera moves as well as settled states.
renderers={k:Renderer(s) for k,s in m['boards'].items()}
for key,r in renderers.items():
 motion=[f for f,item in enumerate(mapped) if item and item[0]==key and item[1]>0 and r.cameras[item[1]]!=r.cameras[item[1]-1] and r.geometry(item[1])[1] and not any(b['start']<=f<b['end'] for b in m['notebook_interleaves'])]
 if motion:
  for f in [motion[len(motion)//3],motion[2*len(motion)//3]]:
   local=mapped[f][1];im,base,geo=r.at(local)
   cv2.imwrite(str(OUT/'preview'/f'{f:05d}-{key}-base.png'),base)
   x=dict(frame=f,key=key,local=local,rings=geo,during_camera_motion=True);samples.append(x);byframe[f]=x
frames=OUT/'encoded-frames';frames.mkdir(exist_ok=True)
selected=set(byframe)|{m['total_frames']-1}
for b in m['boundaries']:selected.update([b['frame']-1,b['frame'],b['frame']+1])
for b in m['notebook_interleaves']:selected.update([b['start']+30,b['end']-30])
# Donor comparison uses decoded, hash-verified source frames.
donors={};cap=cv2.VideoCapture(str(source));needed={f for b in m['notebook_interleaves'] for f in range(b['donor_start'],b['donor_end'])}
for f in range(max(needed)+1):
 ok,im=cap.read();assert ok
 if f in needed:donors[f]=im
cap.release()
cap=cv2.VideoCapture(str(video));src=cv2.VideoCapture(str(source));assert cap.get(cv2.CAP_PROP_FPS)==30
assert [int(cap.get(x)) for x in [cv2.CAP_PROP_FRAME_WIDTH,cv2.CAP_PROP_FRAME_HEIGHT]]==[1280,720]
n=0;unchanged=[];donor_errors=[];preview_errors=[];close=[]
while True:
 ok,im=cap.read();ok2,base=src.read();assert ok==ok2
 if not ok:break
 if n in selected:cv2.imwrite(str(frames/f'{n:05d}.png'),im)
 br=next((b for b in m['notebook_interleaves'] if b['start']<=n<b['end']),None)
 if br:
  donor=donors[min(br['donor_start']+n-br['start'],br['donor_end']-1)]
  donor_errors.append(cv2.norm(im,donor,cv2.NORM_L1)/im.size)
 elif mapped[n] is None:
  e=cv2.norm(im,base,cv2.NORM_L1)/im.size;unchanged.append(e)
  if n>=8402:close.append(e)
 if n in byframe:
  x=byframe[n];ref=renderers[x['key']].at(x['local'])[0];preview_errors.append(cv2.norm(im,ref,cv2.NORM_L1)/im.size)
 n+=1
cap.release();src.release();assert n==8696
assert max(donor_errors)<5;assert max(unchanged)<5;assert max(preview_errors)<5
widths=[]
for x in samples:
 if not x['rings']:continue
 im=cv2.imread(str(frames/f"{x['frame']:05d}.png")).astype(float)
 base=cv2.imread(str(OUT/'preview'/f"{x['frame']:05d}-{x['key']}-base.png")).astype(float)
 for ring in x['rings']:
  l,t,r,b=ring['centerline'];cx=int(round((l+r)/2));cy=int(round((t+b)/2));col=np.array(ring['color_bgr']);results={};integrated={}
  for side,ys,xs in [('top',slice(round(t)-6,round(t)+7),cx),('bottom',slice(round(b)-6,round(b)+7),cx),('left',cy,slice(round(l)-6,round(l)+7)),('right',cy,slice(round(r)-6,round(r)+7))]:
   bg=base[ys,xs];vec=col-bg;delta=im[ys,xs]-bg
   # Ignore canonical accent pixels already nearly identical to the ring color: their coverage is not identifiable.
   contrast=np.linalg.norm(vec,axis=1)
   alpha=np.where(contrast>50,np.clip(np.sum(delta*vec,axis=1)/np.maximum(np.sum(vec*vec,axis=1),1),0,1),0)
   results[side]=int((alpha>.5).sum());integrated[side]=round(float(alpha.sum()),3)
  row=dict(frame=x['frame'],key=x['key'],moving=x.get('during_camera_motion',False),half_coverage_pixels=results,integrated_coverage_pixels=integrated)
  widths.append(row)
  assert all(w==4 for w in results.values()),row
verification=dict(frames=n,fps=30,size=[1280,720],duration=n/30,audio=audio,audio_packets_identical=True,decoded_audio_identical=True,
 ring_measurements=widths,ring_state_count=len(widths),all_measured_sides_4px=True,
 board_runs=m['board_runs'],duration_method='Frame-indexed edit spans including zooms, pans and inherited picture holds; encoded seam frames retained for visual confirmation.',
 longest_board_seconds=m['longest_board_seconds'],longest_board_chain_seconds=m['longest_board_chain_seconds'],
 encoding_errors=dict(retained_picture_max=float(max(unchanged)),retained_picture_mean=float(np.mean(unchanged)),close_mean=float(np.mean(close)),drawing_max=float(max(donor_errors)),board_preview_max=float(max(preview_errors))),
 protected_files_unchanged={p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in m['protected_hashes'].items()},
 checks_not_done=['Real-time full playback/listening','Audible quality of existing grafts','Mobile/player playback','Manual scrutiny of every encoded frame'])
assert all(verification['protected_files_unchanged'].values())
(OUT/'verification.json').write_text(json.dumps(verification,indent=2));print(json.dumps({k:v for k,v in verification.items() if k not in ['ring_measurements','protected_files_unchanged','board_runs']},indent=2))
