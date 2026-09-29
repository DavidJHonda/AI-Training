#!/usr/bin/env python3
"""Decode the actual candidate; validate packet/PCM identity and all prepared states."""
import hashlib,json,subprocess
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
from build_what_is_ai_v9 import ROOT,SRC,DEST,OUT,TOTAL
from editspec_build import sha

def audio_hash(path,pcm=False):
    mode=['-c:a','pcm_s16le','-f','s16le'] if pcm else ['-c:a','copy','-f','data']
    r=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(path),'-map','0:a:0',*mode,'pipe:1'],capture_output=True,check=True)
    return hashlib.sha256(r.stdout).hexdigest()

def sheets(items,prefix,cols=3,rows=4):
    for i in range(0,len(items),cols*rows):
      cells=[]
      for n,im in items[i:i+cols*rows]:
        t=cv2.resize(im,(480,270));cv2.rectangle(t,(0,0),(160,25),(255,255,255),-1)
        cv2.putText(t,f'{n/30:.2f}s / f{n}',(6,18),0,.5,(0,0,0),1);cells.append(t)
      while len(cells)%cols:cells.append(np.full_like(cells[0],255))
      cv2.imwrite(str(OUT/f'{prefix}-{i//(cols*rows):02d}.jpg'),np.vstack([np.hstack(cells[j:j+cols]) for j in range(0,len(cells),cols)]))

def main():
    m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(DEST)==m['candidate_sha256']
    hashes={k:audio_hash(p,pcm) for k,p,pcm in [('source_packets',SRC,False),('candidate_packets',DEST,False),('source_pcm',SRC,True),('candidate_pcm',DEST,True)]}
    assert hashes['source_packets']==hashes['candidate_packets']
    assert hashes['source_pcm']==hashes['candidate_pcm']
    (OUT/'encoded').mkdir(exist_ok=True)
    wanted=set(m['preview_frames']);cap=cv2.VideoCapture(str(DEST));assert cap.get(cv2.CAP_PROP_FPS)==30
    n=0;states=[];full=[];changed=[];edge=[]
    edgeframes={f for b in m['boundaries'] for f in [b-1,b,b+1]}
    while True:
      ok,im=cap.read()
      if not ok:break
      assert im.shape==(720,1280,3)
      if n in wanted:
        ref=cv2.imread(str(OUT/'preview'/f'{n:05d}.jpg'));mad=float(np.abs(im.astype(float)-ref).mean());assert mad<5,(n,mad)
        states.append(dict(frame=n,mad=mad));cv2.imwrite(str(OUT/'encoded'/f'{n:05d}.jpg'),im)
      if n%120==0 or n==TOTAL-1:full.append((n,im.copy()))
      if 4095<=n<4374 and n%15==0:changed.append((n,im.copy()))
      if n in edgeframes:edge.append((n,im.copy()))
      n+=1
    cap.release();assert n==TOTAL
    assert all(sha(Path(p))==h for p,h in m['protected'].items())
    intervals=m['board_intervals'];merged=[]
    for a,b,key in intervals:
      if merged and merged[-1][1]==a:merged[-1][1]=b
      else:merged.append([a,b])
    qa=dict(candidate_sha256=sha(DEST),decoded_frames=n,fps=30,duration=n/30,audio_hashes=hashes,audio_packets_identical=True,
      decoded_audio_identical=True,prepared_states_checked=len(states),max_encoded_state_mad=max(s['mad'] for s in states),
      source_assets_unchanged=True,board_runs_frames=merged,longest_board_run_seconds=max((b-a)/30 for a,b in merged),
      listening='Not directly auditioned. Audio packet-copy and decoded PCM verified identical to raw version 5.',states=states)
    (OUT/'qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    sheets(full,'encoded-full');sheets(changed,'encoded-movie');sheets(edge,'encoded-boundaries')
    args=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST)]
    for b in m['boundaries']:args+=['--boundary',f'{b}:visual-change']
    subprocess.run([*args,'--outdir',str(OUT/'guard')],check=True)
    print(json.dumps({k:v for k,v in qa.items() if k!='states'},indent=2))

if __name__=='__main__':main()
