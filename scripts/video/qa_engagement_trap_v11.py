#!/usr/bin/env python3
"""Encoded-candidate checks for Engagement Trap v11; not a listening substitute."""
from pathlib import Path
import json,subprocess,hashlib,wave,sys
import numpy as np,cv2,imageio_ffmpeg
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];O=ROOT/'video-audit/engagement-trap-build-2026-09-29-v11'
m=json.loads((O/'edit-manifest.json').read_text());v=Path(m['candidate']);FF=imageio_ffmpeg.get_ffmpeg_exe()
def read(p):
 with wave.open(str(p)) as w:return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
subprocess.run([FF,'-v','error','-y','-i',str(v),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(O/'candidate.wav')],check=True)
a=read(O/'candidate.wav');b=read(O/'edited.wav');src=read(O/'source.wav');q=[]
for row in m['audio_rows']:
 s,e=row['output_start']*1600,row['output_end']*1600;x=a[s:e];y=b[s:e]
 corr=float(np.corrcoef(x,y)[0,1]);assert len(x)==len(y) and corr>.995,(row,corr)
 kept=src[row['source_start']*1600+240:row['source_end']*1600-240]
 assert np.array_equal(kept,y[240:-240])
 q.append(dict(**row,correlation=corr,unaltered_pcm=True))
# Decode output sequentially with ffmpeg; save current-state and transition samples.
interesting=set(m['declared_boundaries'])|{n-1 for n in m['declared_boundaries']}|{m['total_frames']-1}
for r in m['visual_rows']:
 interesting|={r['output_start']+2,min(r['output_start']+60,r['output_end']-1),r['output_end']-1}
p=subprocess.Popen([FF,'-v','error','-i',str(v),'-map','0:v','-an','-fps_mode','passthrough','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
D=O/'encoded';D.mkdir(exist_ok=True);tiles=[];n=0
while True:
 raw=p.stdout.read(1280*720*3)
 if not raw:break
 assert len(raw)==1280*720*3
 im=np.frombuffer(raw,np.uint8).reshape(720,1280,3)
 if n in interesting:cv2.imwrite(str(D/f'{n:05d}.jpg'),im)
 if n%120==0 or n in interesting:
  tile=Image.new('RGB',(384,240),'white');thumb=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));thumb.thumbnail((384,216));tile.paste(thumb,(0,24));ImageDraw.Draw(tile).text((5,5),f'{n/30:.3f}s | f{n}',fill='black');tiles.append(tile)
 n+=1
assert p.wait()==0 and n==m['total_frames'],(n,m['total_frames'])
for j in range(0,len(tiles),20):
 sheet=Image.new('RGB',(1536,1200),'#eee')
 for k,t in enumerate(tiles[j:j+20]):sheet.paste(t,((k%4)*384,(k//4)*240))
 sheet.save(O/f'qa-sheet-{j//20+1:02d}.jpg')
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in m['protected'].items())
# Record 40-ms RMS around each splice for low-floor discontinuity checks.
seams=[]
for cut in m['audio_cuts']:
 k=cut['output_frame']*1600;db=lambda z:float(20*np.log10(np.sqrt(np.mean((z/32768)**2))+1e-12))
 seams.append(dict(frame=cut['output_frame'],seconds=cut['output_frame']/30,before_db=db(b[k-960:k]),after_db=db(b[k:k+960])))
result=dict(decoded_frames=n,duration=n/30,audio_rows=q,audio_join_levels=seams,aac_padding_samples=len(a)-len(b),protected_unchanged=True,listening='Not performed',continuous_motion_review='Not performed',candidate_sha256=hashlib.sha256(v.read_bytes()).hexdigest())
(O/'qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(v),'--outdir',str(O/'transitions')]
for f in m['declared_boundaries']:cmd+=['--boundary',f'{f}:edit']
subprocess.run(cmd,check=True)
