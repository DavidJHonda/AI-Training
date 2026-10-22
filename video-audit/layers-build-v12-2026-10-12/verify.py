from pathlib import Path
import sys,json,subprocess,hashlib
import cv2,numpy as np,imageio_ffmpeg
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import Reader,sha
m=json.loads((OUT/'edit-manifest.json').read_text());dest=Path(m['output']);base=Path(m['base'])
assert sha(dest)==m['render_sha256']
assert all(sha(Path(p))==h for p,h in m['protected'].items())
def old_frame(n):return n if n<3376 else n-30 if n<4645 else n-82
samples=[0,1000,2700,3215,3216,3290,3375,3376,3377,3382,3529,3530,3539,3809,3984,4205,4222,4223,4334,4445,4446,4497,4644,4645,4779,4780,4792,4793,5300,6050,6182]
(OUT/'encoded').mkdir(exist_ok=True)
cap=cv2.VideoCapture(str(dest));ref=Reader(base);n=0;comparisons=[];tiles=[]
while True:
 ok,im=cap.read()
 if not ok:break
 assert im.shape==(720,1280,3)
 if not 3216<=n<4793 and (n%30==0 or n==6182):
  delta=float(np.abs(im.astype(float)-ref.at(old_frame(n))).mean());comparisons.append([n,delta])
  assert delta<5,(n,delta)
 if n in samples:
  cv2.imwrite(str(OUT/'encoded'/f'{n:05d}.jpg'),im)
 if 3216<=n<4793 and (n%60==0 or n in samples):
  tile=np.full((240,384,3),255,np.uint8);tile[:216]=cv2.resize(im,(384,216))
  cv2.putText(tile,f'{n/30:.3f}s / {n}',(8,233),cv2.FONT_HERSHEY_SIMPLEX,.5,(40,40,40),1,cv2.LINE_AA);tiles.append(tile)
 n+=1
fps=cap.get(cv2.CAP_PROP_FPS);cap.release();ref.c.release();assert n==6183 and fps==30
for j in range(0,len(tiles),16):
 page=tiles[j:j+16]
 page += [np.full((240,384,3),255,np.uint8)]*(16-len(page))
 cv2.imwrite(str(OUT/f'motion-{j//16}.jpg'),cv2.vconcat([cv2.hconcat(page[i:i+4]) for i in range(0,16,4)]))
ff=imageio_ffmpeg.get_ffmpeg_exe()
def decode(p):return np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(p),'-vn','-ar','48000','-ac','1','-f','f32le','-']),np.float32)
a=decode(base);b=decode(dest);assembled=decode(OUT/'assembled.wav');spf=1600;audio=[]
for ns,ne,os,oe in [(0,3376,0,3376),(3530,4645,3500,4615),(4780,6183,4698,6101)]:
 x=a[os*spf:oe*spf];y=b[ns*spf:ne*spf]
 assert len(x)==len(y);corr=float(np.corrcoef(x,y)[0,1]);assert corr>.995
 audio.append(dict(output_frames=[ns,ne],base_frames=[os,oe],correlation=corr,rms_error=float(np.sqrt(np.mean((x-y)**2)))))
donors=[]
for g in m['grafts']:
 s,e=g['output_frames'];x=b[s*spf:e*spf];donors.append(dict(name=g['name'],peak=float(abs(x).max()),samples_over_one=int((abs(x)>=1).sum())))
 assert abs(x).max()<1
def aac_hash(p):return hashlib.sha256(subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-'])).hexdigest()
prior=ROOT/'Prompts/layers-v11.mp4';ah=aac_hash(dest);assert ah==aac_hash(prior)
for name in ['encoded-transcript.json','encoded-transcript.txt']:
 (OUT/name).write_bytes((OUT.parent/'layers-build-v11-2026-10-12'/name).read_bytes())
qa=dict(aac_hash=ah,transcript_provenance='v11 encoded audio; v12 AAC verified byte-identical',frames=n,fps=fps,duration=n/fps,retained_visual_samples=len(comparisons),retained_max_mad=max(v for _,v in comparisons),
 audio_unchanged_spans=audio,donors=donors,base_peak=float(abs(a).max()),encoded_peak=float(abs(b).max()),
 source_hashes_unchanged=True,direct_listening=False,full_real_time_viewing=False)
(OUT/'qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa,indent=2),flush=True)
args=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(dest),'--outdir',str(OUT/'guard')]
for row in m['boundaries']:
 if 0<row['frame']<6183:args += ['--boundary',f"{row['frame']}:{row['label']}"]
r=subprocess.run(args,capture_output=True,text=True);(OUT/'guard-run.txt').write_text(r.stdout+r.stderr);print('Guard exit',r.returncode,flush=True)
