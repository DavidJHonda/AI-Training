#!/usr/bin/env python3
"""Approved narrow visual repair; frozen finished source, unchanged audio/timing."""
import hashlib,json,subprocess,sys,types
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import Build
from ken_burns_path import window,draw_ring,hex_bgr,ring_px
cv2.setNumThreads(1)
OUT=ROOT/'video-audit/fake-trap-repair-2026-09-29-v8'
SRC=ROOT/'Prompts/fake-trap-v6-source.mp4'; DEST=ROOT/'Prompts/fake-trap-v8.mp4'
SOURCE_SHA='8fffe6bdf9de2fc9e8b6736a18b2235f5b54e6992ec8fd1873a3bdd7195ab24e'
FF=imageio_ffmpeg.get_ffmpeg_exe(); FPS=30;TOTAL=9240
DONORS=[dict(name='principal-phone',source=[612,732],output=[1317,1437]),dict(name='context-date',source=[6060,6234],output=[5010,5184])]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def cap(p):return cv2.VideoCapture(str(p),cv2.CAP_FFMPEG,[cv2.CAP_PROP_N_THREADS,2])
def audio_sha(p):
 data=subprocess.check_output([FF,'-v','error','-i',str(p),'-map','0:a','-c','copy','-f','data','-'])
 return hashlib.sha256(data).hexdigest()
def static_render(image,camera,rings=()):
 img=cv2.imread(str(image));ih,iw=img.shape[:2];up=3;ow,oh=1280,720
 big=cv2.resize(img,(iw*up,ih*up),interpolation=cv2.INTER_LANCZOS4)
 x,y,w,h=window(*camera,ow/oh,iw,ih);X,Y,W,H=[round(v*up) for v in (x,y,w,h)]
 f=cv2.resize(big[Y:Y+H,X:X+W],(ow,oh),interpolation=cv2.INTER_AREA if W>ow else cv2.INTER_LANCZOS4)
 for r in rings:
  rx,ry,rw,rh=r['rect']; scale=ow/w;t=ring_px(oh);half=t/2;pad=r.get('pad',0)
  # Rasterize at 4x so OpenCV's inclusive integer stroke does not inflate
  # the requested 4 px to 6 colored pixels in the delivery frame.
  ss=4;mask=np.zeros((oh*ss,ow*ss,3),np.uint8)
  draw_ring(mask,((rx-pad-x)*scale-half)*ss,((ry-pad-y)*scale-half)*ss,((rx+rw+pad-x)*scale+half)*ss,((ry+rh+pad-y)*scale+half)*ss,(255,255,255),(r.get('radius',0)*scale+half)*ss,t*ss)
  alpha=cv2.resize(mask[:,:,0],(ow,oh),interpolation=cv2.INTER_AREA).astype('float32')[:,:,None]/255
  f=np.rint(f.astype('float32')*(1-alpha)+np.array(hex_bgr(r['color']),dtype='float32')*alpha).astype('uint8')
 return f

def main():
 OUT.mkdir(exist_ok=True);assert sha(SRC)==SOURCE_SHA;assert not DEST.exists(), 'Never overwrite a candidate'
 old=json.loads((ROOT/'video-audit/fake-trap-materials-test-2026-09-20/build-v5/edit-manifest.json').read_text())
 assets={k:ROOT/'course-assets/fake-trap'/f'fake-trap-{k}.jpg' for k in ('comparison','checks')}
 protected={str(p):sha(p) for p in [ROOT/'index.html',ROOT/'course-assets/fake-trap/fake-trap.mp4',*assets.values()]}
 canvases={k:Build.compose(types.SimpleNamespace(out=OUT),p,k) for k,p in assets.items()}
 assert canvases['comparison'][1:]==(2824,1590,612,60);assert canvases['checks'][1:]==(1600,900,0,40)
 # Independent sequential decode creates bounded, lossless visual donors from the frozen source.
 dc=cap(SRC);writers={d['name']:cv2.VideoWriter(str(OUT/(d['name']+'.mkv')),cv2.VideoWriter_fourcc(*'FFV1'),FPS,(1280,720)) for d in DONORS}
 assert all(w.isOpened() for w in writers.values())
 idx=0
 while idx<6234 and dc.grab():
  for d in DONORS:
   if d['source'][0]<=idx<d['source'][1]:
    ok,f=dc.retrieve();assert ok;writers[d['name']].write(f)
  idx+=1
 dc.release()
 for w in writers.values():w.release()
 assert idx==6234
 print('Lossless donor clips ready',flush=True)
 checks=old['boards']['checks'];rings=checks['rings']
 states={name:static_render(canvases['checks'][0],[800,450,1600],rs) for name,rs in [('unmarked',[]),('source',[rings[0]]),('context',[rings[1]]),('corroboration',[rings[2]])]}
 right=static_render(canvases['comparison'][0],[1800.0,846.5,2094.7301587301586])
 for name,f in states.items():cv2.imwrite(str(OUT/f'checks-{name}.png'),f)
 cv2.imwrite(str(OUT/'comparison-return.png'),right)
 # Exactly one final video encode; AAC packets are copied directly from the frozen source.
 cmd=[FF,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','2','-crf','16','-preset','medium','-profile:v','high','-level:v','3.1','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);base=cap(SRC);donor_caps={d['name']:cap(OUT/(d['name']+'.mkv')) for d in DONORS};n=0
 while base.grab():
  donor=next((d for d in DONORS if d['output'][0]<=n<d['output'][1]),None)
  if donor:
   ok,f=donor_caps[donor['name']].read();assert ok
  elif 1437<=n<1459:f=right
  elif 4742<=n<5686:
   name='unmarked' if n<4819 or n>=5421 else ('source' if n<4988 else ('context' if n<5221 else 'corroboration'))
   f=states[name]
  else:
   ok,f=base.retrieve();assert ok
  proc.stdin.write(f.tobytes());n+=1
  if n%1800==0:print(f'Encoded {n}/{TOTAL}',flush=True)
 base.release()
 for c in donor_caps.values():c.release()
 proc.stdin.close();assert proc.wait()==0;assert n==TOTAL
 ac=cap(DEST);decoded=0
 while ac.grab():decoded+=1
 fps=ac.get(cv2.CAP_PROP_FPS);ac.release();assert decoded==TOTAL and fps==FPS
 audio=audio_sha(DEST);assert audio==audio_sha(SRC)
 assert sha(SRC)==SOURCE_SHA and all(sha(p)==s for p,s in protected.items())
 manifest=dict(candidate=str(DEST),candidate_sha256=sha(DEST),source=str(SRC),source_sha256=SOURCE_SHA,scope='Narrow visual repair; approved narration and timing retained',total_frames=decoded,fps=fps,duration=decoded/fps,audio_packet_sha256=audio,audio_packets_identical=True,donors=DONORS,changed_spans=[[1317,1459],[4742,5686]],comparison_return_unmarked=[1437,1459],checks=dict(span=[4742,5686],cutaway=[5010,5184],ring_onsets=[4819,4988,5221],last_ring_end=5421,ring_px=ring_px(720),density='compact'),board_run_seconds=dict(comparison=[17.1,20.0],checks=[268/30,502/30],reasons_unchanged=647/30),protected_hashes=protected,encode_command=cmd)
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({k:manifest[k] for k in ('candidate','candidate_sha256','total_frames','audio_packets_identical')},indent=2),flush=True)
if __name__=='__main__':main()
