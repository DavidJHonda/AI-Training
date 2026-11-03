#!/usr/bin/env python3
"""Verify the two-example video against its cut plan and retained source packets."""
import sys,json,hashlib,subprocess
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_loudest_voices_v13 import *
from PIL import Image,ImageDraw
m=json.loads((OUT/'edit-manifest.json').read_text())
def packets(p):
 with av.open(str(p)) as c:
  return {round(p.pts/512):(hashlib.sha256(bytes(p)).hexdigest(),p.dts) for p in c.demux(c.streams.video[0]) if p.dts is not None}
s=packets(SOURCE);d=packets(DEST);verified=0
assert len(d)==FRAMES
for n,(h,t) in s.items():
 if A<=n<B:continue
 shift=SHIFT if n>=B else 0
 assert d[n-shift]==(h,t-shift*512);verified+=1
actual=pcm(DEST)[:FRAMES*1600];expected=np.fromfile(OUT/'edited-audio.f32',np.float32).reshape(-1,2)
assert actual.shape==expected.shape
corr=float(np.corrcoef(actual.ravel(),expected.ravel())[0,1]);assert corr>.995
joins=[]
for row in m['timeline'][1:]:
 n=row['output_start_frame'];k=n*1600
 joins.append({'frame':n,'seconds':n/30,'sample_step':float(np.max(np.abs(actual[k]-actual[k-1]))),'rms_10ms_db':float(20*np.log10(np.sqrt(np.mean(actual[k-240:k+240]**2))+1e-12))})
# Compare every newly rendered board frame against its expected canonical state.
expected_states={k:board_frame(k) for k in (None,0,1)};want={3064,3300,3395,3396,3500,3667,3673,3800,3959,3960,4023,FRAMES-1};images=[];pts=[];errors=[]
with av.open(str(DEST)) as c:
 for n,im in enumerate(c.decode(video=0)):
  pts.append(float(im.pts*im.time_base))
  if A<=n<3960:
   row=next(r for r in m['timeline'] if r['output_start_frame']<=n<r['output_end_frame'])
   src=n-row['output_start_frame']+row['source_start_frame']
   state=None if src<3566 else 0 if src<4442 else 1
   ar=im.to_ndarray(format='bgr24');ref=expected_states[state]
   errors.append(float(np.abs(ar.astype(np.int16)-ref.astype(np.int16)).mean()))
  if n in want:images.append((n,im.to_image()))
assert len(pts)==FRAMES and np.max(np.abs(np.diff(pts)-1/30))<.00001
assert max(errors)<5
sheet=Image.new('RGB',(1280,((len(images)+2)//3)*264),'white');draw=ImageDraw.Draw(sheet)
for i,(n,im) in enumerate(images):
 x=i%3*426;y=i//3*264;sheet.paste(im.resize((426,240)),(x,y));draw.text((x+5,y+243),f'{n/30:.3f}s / f{n}',fill='black')
sheet.save(OUT/'candidate-sheet.jpg')
for n,im in images:
 if n in [3300,3500,3800,3960]:im.save(OUT/f'frame-{n}.jpg')
qa={'frames':len(pts),'duration':len(pts)/30,'copied_video_packets_verified':verified,'board_frames_checked':len(errors),'board_max_mean_pixel_error':max(errors),'audio_correlation_to_planned_edit':corr,'joins':joins,'listening':'Not performed. Manual listening review of three joins remains required.'}
(OUT/'qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa,indent=2))
args=[sys.executable,'scripts/video/transition_guard.py',str(DEST),'--outdir',str(OUT/'transitions')]
for n in m['boundaries']:args+=['--boundary',str(n)]
subprocess.run(args,check=True)
subprocess.run([FF,'-v','error','-y','-i',str(DEST),'-ss','98','-t','50','-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/'changed-section.mp4')],check=True)
