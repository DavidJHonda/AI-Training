#!/usr/bin/env python3
"""Check encoded timing, audio alignment, board states, and all declared seams."""
import json,subprocess
import cv2,numpy as np
from build_big_downside_v7 import OUT,DEST,ROOT,FF,lesson_signature
from editspec_build import readwav,sha,SPF
from build_creative_thinking_v8 import BoardRenderer

m=json.loads((OUT/'edit-manifest.json').read_text())
assert sha(DEST)==m['render_sha256']
(OUT/'encoded-preview').mkdir(exist_ok=True)
subprocess.run([FF,'-v','error','-y','-i',str(DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'encoded.wav')],check=True)
expected=readwav(OUT/'edited.wav');encoded=readwav(OUT/'encoded.wav')
assert abs(len(encoded)-len(expected))<=1024,(len(encoded),len(expected))
n=min(len(encoded),len(expected));corr=float(np.corrcoef(expected[:n],encoded[:n])[0,1]);assert corr>.995,corr
targets={0,m['total_frames']-1};boards={k:BoardRenderer(OUT/f'leg-{k}.json') for k in m['boards']}
for k,br in boards.items():
 s=m['boards'][k]['src_in'];targets.add(s)
 for r in br.rings:
  f=s+r[0]+10
  if any(x['visual']==k and x['start_frame']<=f<x['end_frame'] for x in m['timeline']):targets.add(f)
for b in m['boundaries']:targets.update([b['frame']-1,b['frame']])
c=cv2.VideoCapture(str(DEST));assert c.get(cv2.CAP_PROP_FPS)==30
i=0;diffs=[];contact=[]
while True:
 ok,im=c.read()
 if not ok:break
 assert im.shape==(720,1280,3)
 if i in targets:
  cv2.imwrite(str(OUT/'encoded-preview'/f'{i:06}.jpg'),im)
  r=next(r for r in m['timeline'] if r['start_frame']<=i<r['end_frame'])
  if r['visual'] in boards:
   k=r['visual'];ref=boards[k].frame(i-m['boards'][k]['src_in'])
   d=float(np.abs(im.astype(float)-ref.astype(float)).mean());assert d<4,(i,d);diffs.append(dict(frame=i,board=k,MAD=d))
 if i%240==0 or i==m['total_frames']-1:
  cell=cv2.resize(im,(384,216));cv2.putText(cell,f'{i/30:.2f}s',(8,24),cv2.FONT_HERSHEY_SIMPLEX,.65,(0,0,230),2);contact.append(cell)
 i+=1
c.release();assert i==m['total_frames'],(i,m['total_frames'])
while len(contact)%4:contact.append(np.full_like(contact[0],255))
cv2.imwrite(str(OUT/'encoded-overview.jpg'),cv2.vconcat([cv2.hconcat(contact[j:j+4]) for j in range(0,len(contact),4)]))
q=dict(decoded_frames=i,duration=i/30,fps=30,size=[1280,720],audio_correlation=corr,audio_sample_difference=len(encoded)-len(expected),board_samples=diffs,protected_unchanged={p:sha(p)==h for p,h in m['protected_hashes'].items()},listening='Not performed; no direct audio perception. ASR/PCM metrics do not certify listening.',motion='Sequential decode and sampled frames only; real-time viewing unperformed.')
q['lesson_scope_unchanged']=lesson_signature((ROOT/'index.html').read_text())==m['lesson_scope_sha256']
assert all(v for p,v in q['protected_unchanged'].items() if p!=str(ROOT/'index.html'))
assert q['lesson_scope_unchanged']
(OUT/'qa.json').write_text(json.dumps(q,indent=2));print(json.dumps({k:v for k,v in q.items() if k not in ['board_samples','protected_unchanged']},indent=2),flush=True)
cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions'),'--cut-threshold','8']
for b in m['boundaries']:cmd+=['--boundary',str(b['frame'])+':'+b['label']]
subprocess.run(cmd,check=True)
