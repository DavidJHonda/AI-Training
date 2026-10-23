#!/usr/bin/env python3
"""Show the canonical actions board during its spoken introduction; visual only."""
from pathlib import Path
import hashlib,json,subprocess,sys
import av,cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/make-your-move-v11.mp4'
DEST=ROOT/'Prompts/make-your-move-v12.mp4'
OUT=ROOT/'video-audit/make-your-move-actions-intro-v12-2026-10-23'
BOARD=ROOT/'course-assets/make-your-move/make-your-move-actions.jpg'
START,END,TOTAL=3011,3341,5431
EXPECTED='bd537212dbfb94d6cf96611c33d056f58aea78fb6ac65e370758843e9763929d'
FF=imageio_ffmpeg.get_ffmpeg_exe()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def packets(p,kind):
 with av.open(str(p)) as c:
  s=c.streams.video[0] if kind=='video' else c.streams.audio[0]
  return [(q.pts,q.dts,q.duration,str(q.time_base),hashlib.sha256(bytes(q)).hexdigest()) for q in c.demux(s) if q.dts is not None and (kind=='audio' or not START*512<=q.pts<END*512)]
def main():
 cv2.setNumThreads(2);OUT.mkdir(exist_ok=True)
 assert sha(SRC)==EXPECTED and not DEST.exists()
 protected={str(p):sha(p) for p in [SRC,BOARD,ROOT/'course-assets/make-your-move/make-your-move.mp4',ROOT/'index.html']}
 cap=cv2.VideoCapture(str(SRC));cap.set(cv2.CAP_PROP_POS_FRAMES,END);ok,ref=cap.read();cap.release();assert ok
 im=cv2.imread(str(BOARD));h,w=im.shape[:2];height=720;width=round(w*height/h);x=(1280-width)//2
 canvas=np.full((720,1280,3),ref[360,0],np.uint8)
 canvas[:,x:x+width]=cv2.resize(im,(width,height),interpolation=cv2.INTER_AREA)
 cv2.imwrite(str(OUT/'actions-full.png'),canvas)
 leg=OUT/'intro-picture.mp4'
 subprocess.run([FF,'-v','error','-y','-loop','1','-framerate','30','-i',str(OUT/'actions-full.png'),'-frames:v',str(END-START),'-an','-c:v','libx264','-profile:v','high','-level:v','3.1','-crf','16','-preset','fast','-threads','2','-pix_fmt','yuv420p','-video_track_timescale','15360',str(leg)],check=True)
 source=av.open(str(SRC));v=source.streams.video[0];a=source.streams.audio[0]
 patch=av.open(str(leg));pv=patch.streams.video[0]
 assert pv.codec_context.extradata==v.codec_context.extradata,'Codec configuration mismatch'
 assert pv.frames==END-START
 items=[]
 for q in source.demux(v,a):
  if q.dts is None:continue
  if q.stream.type=='video' and START*512<=q.pts<END*512:continue
  items.append((q.stream.type,q))
 for q in patch.demux(pv):
  if q.dts is None:continue
  q.pts+=START*512;q.dts+=START*512;items.append(('video',q))
 items.sort(key=lambda item:item[1].dts*item[1].time_base)
 with av.open(str(DEST),'w',options={'movflags':'+faststart'}) as c:
  ov=c.add_stream_from_template(v);oa=c.add_stream_from_template(a)
  for kind,q in items:q.stream=ov if kind=='video' else oa;c.mux(q)
 source.close();patch.close()
 assert packets(SRC,'audio')==packets(DEST,'audio'),'Audio changed'
 assert packets(SRC,'video')==packets(DEST,'video'),'Unaffected packets changed'
 checks={START-1,START,START+1,3120,END-1,END,END+1,3429,TOTAL-1}
 ca=av.open(str(SRC));cb=av.open(str(DEST));n=0;max_mad=0
 for n,(fa,fb) in enumerate(zip(ca.decode(video=0),cb.decode(video=0))):
  assert fa.pts==fb.pts and fa.time_base==fb.time_base
  ya=fa.to_ndarray(format='yuv420p');yb=fb.to_ndarray(format='yuv420p')
  if not START<=n<END:assert np.array_equal(ya,yb),('Unaffected pixels changed',n)
  else:
   actual=fb.to_ndarray(format='bgr24');mad=float(np.mean(np.abs(actual.astype(float)-canvas.astype(float))));max_mad=max(max_mad,mad);assert mad<3
  if n in checks:cv2.imwrite(str(OUT/f'frame-{n:05d}.jpg'),fb.to_ndarray(format='bgr24'))
 assert n+1==TOTAL
 ca.close();cb.close()
 with av.open(str(DEST)) as c:assert c.streams.video[0].frames==TOTAL
 assert all(sha(p)==h for p,h in protected.items())
 m=dict(source=str(SRC),source_sha256=EXPECTED,candidate=str(DEST),candidate_sha256=sha(DEST),board=str(BOARD),board_sha256=sha(BOARD),changed_frames=[START,END],changed_seconds=[START/30,END/30],frames=TOTAL,fps=30,duration=TOTAL/30,board_placement=[x,0,width,720],audio_packets_and_timestamps_identical=True,unaffected_video_packets_and_decoded_frames_identical=True,changed_board_max_mean_pixel_error=max_mad,scope='Owner-requested actions introduction only. Complete unmarked board replaces city drawing; existing action highlights and camera continue unchanged.',protected_hashes=protected,status='Review candidate; not installed or published')
 (OUT/'verification.json').write_text(json.dumps(m,indent=2)+'\n')
 subprocess.run([sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--boundary',f'{START}:actions-intro-board','--boundary',f'{END}:existing-board-treatment','--outdir',str(OUT/'transitions')],check=True)
 print(json.dumps(m,indent=2))
if __name__=='__main__':main()
