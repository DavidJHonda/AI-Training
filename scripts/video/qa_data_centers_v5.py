#!/usr/bin/env python3
"""Verify copied packets, complete decode, caption frames, and visual boundaries."""
import hashlib
import json
import subprocess
import sys
import av
import cv2
import numpy as np
from build_data_centers_v5 import SRC, DEST, OUT, SPANS, PATCHES, FF, sha

def signatures(path,kind):
    with av.open(str(path)) as c:
        s=next(s for s in c.streams if s.type==kind)
        return [(p.pts,p.dts,p.duration,str(p.time_base),hashlib.sha256(bytes(p)).hexdigest())
                for p in c.demux(s) if p.dts is not None]

def frames(path):
    with av.open(str(path)) as c:
        c.streams.video[0].codec_context.thread_count=1
        for f in c.decode(video=0): yield f.pts, f.to_ndarray(format='bgr24')

def main():
    a1=signatures(SRC,'audio');a2=signatures(DEST,'audio');assert a1==a2
    v1=signatures(SRC,'video');v2=signatures(DEST,'video')
    keep=lambda s:[r for r in s if not any(a<=r[0]/512<b for a,b,_ in SPANS)]
    assert keep(v1)==keep(v2)
    selected={250,289,290,292,298,300,307,315,360,465,474,480,489,494,499,500,
              5466,5467,5470,5476,5485,5520,5545,5550,5560,5575,5591,5716,5717,6693}
    count=identical=0;cells=[];aa=frames(SRC);bb=frames(DEST)
    for n,((pa,a),(pb,b)) in enumerate(zip(aa,bb)):
        assert pa==pb==n*512
        edited=any(lo<=n<hi for lo,hi,_ in SPANS)
        if not edited: assert np.array_equal(a,b),n;identical+=1
        if n in selected:
            cv2.imwrite(str(OUT/f'encoded-{n:05}.png'),b)
            tile=cv2.resize(b,(480,270));cv2.putText(tile,f'f{n} / {n/30:.2f}s',(8,24),0,.65,(0,0,255),2);cells.append(tile)
        count+=1
    assert next(aa,None) is None and next(bb,None) is None
    assert count==6694 and identical==6194
    for k in range(0,len(cells),12):
        part=cells[k:k+12]
        while len(part)%3:part.append(part[-1]*0)
        cv2.imwrite(str(OUT/f'encoded-sheet-{k//12}.jpg'),cv2.vconcat([cv2.hconcat(part[j:j+3]) for j in range(0,len(part),3)]))
    decoded=[]
    for path in (SRC,DEST):
        raw=subprocess.check_output([FF,'-v','error','-i',str(path),'-map','0:a:0','-f','s16le','-'])
        decoded.append({'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    assert decoded[0]==decoded[1]
    result=dict(candidate_sha256=sha(DEST),frames=count,fps=30,duration_seconds=count/30,
                pixel_identical_frames_outside_encoded_gops=identical,encoded_gop_frames=500,
                unaffected_video_packets_identical=True,audio_packets_and_timestamps_identical=True,
                decoded_audio=decoded,direct_listening_performed=False,encoded_frames_inspected=sorted(selected))
    (OUT/'qa.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    # Single-thread decoder avoids the slow auto-thread behavior on this host.
    wrapper="import cv2,runpy; old=cv2.VideoCapture; cv2.VideoCapture=lambda p:old(p,cv2.CAP_FFMPEG,[cv2.CAP_PROP_N_THREADS,1]); runpy.run_path('scripts/video/transition_guard.py',run_name='__main__')"
    cmd=[sys.executable,'-c',wrapper,str(DEST),'--outdir',str(OUT/'guard')]
    for lo,hi,name in SPANS+PATCHES:
        for f,suffix in [(lo,'-in'),(hi,'-out')]:cmd+=['--boundary',f'{f}:{name}{suffix}']
    subprocess.run(cmd,check=True)

if __name__=='__main__':main()
