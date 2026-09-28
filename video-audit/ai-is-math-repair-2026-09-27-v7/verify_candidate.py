import sys,json,subprocess
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
sys.path.insert(0,str(Path.cwd()/'scripts/video'))
from build_ai_is_math_v7 import *
m=json.loads((OUT/'edit-manifest.json').read_text());snapshot=Path(m['snapshot']);r=Render(snapshot)
cap=cv2.VideoCapture(str(DEST));count=0;errors=[];saved=[];src=Reader(snapshot)
samples={p['output_frame']:p for p in m['previews']};(OUT/'encoded').mkdir(exist_ok=True)
while True:
 ok,im=cap.read()
 if not ok:break
 n=count if count<CUT[0] else count+CUT[1]-CUT[0]
 row=next(row for row in ROWS if row[0]<=n<row[1])
 if count in samples or row[2]=='close':
  expected=src.at(n) if row[2]=='close' else r.frame(n,row)
  errors.append(float(np.abs(im.astype(float)-expected).mean()))
 if count in samples:
  p=OUT/'encoded'/f'{count:05d}-{row[2]}.png';cv2.imwrite(str(p),im);saved.append(str(p))
 if count==m['frames']-1:cv2.imwrite(str(OUT/'encoded/last.png'),im)
 count+=1
assert count==m['frames'];assert max(errors)<4,max(errors)
a=readwav(OUT/'source.wav');e=readwav(OUT/'edited.wav');cut=CUT[0]*SPF;b=CUT[1]*SPF;fade=240
assert np.array_equal(e[:cut-fade],a[:cut-fade]);assert np.array_equal(e[cut+fade:],a[b+fade:TOTAL*SPF])
assert all(sha(Path(p))==v for p,v in m['protected'].items())
result=dict(decoded_frames=count,fps=cap.get(cv2.CAP_PROP_FPS),maximum_sample_reference_mae=max(errors),comparison_samples=len(errors),all_240_close_frames_compared=True,pcm_exact_outside_5ms_join=True,protected_files_unchanged=True,candidate_sha256=sha(DEST),encoded_frames=saved)
(OUT/'verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k!='encoded_frames'},indent=2))
cmd=[sys.executable,'scripts/video/transition_guard.py',str(DEST),'--outdir',str(OUT/'guard')]
for row in m['timeline'][1:]:cmd+=['--boundary',str(row['output'][0])+':'+row['key']]
subprocess.run(cmd,check=True)
