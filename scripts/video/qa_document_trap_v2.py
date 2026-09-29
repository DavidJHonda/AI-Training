#!/usr/bin/env python3
"""Verify encoded v2 timing/audio and preservation outside approved visual spans."""
from pathlib import Path
import hashlib,json
from fractions import Fraction
import av,cv2,numpy as np
from build_document_trap_v2 import SRC,DEST,OUT,EXPECTED,sha,INSERT,LABEL,NOTE
cv2.setNumThreads(2)

def audio_info(path):
    h=hashlib.sha256();count=0
    with av.open(str(path)) as c:
        st=c.streams.audio[0]
        for packet in c.demux(st):
            if packet.size:
                h.update(bytes(packet));count+=1
    return dict(packet_sha256=h.hexdigest(),packets=count)

def main():
    assert sha(SRC)==EXPECTED
    sa,da=audio_info(SRC),audio_info(DEST);assert sa==da,(sa,da)
    a=cv2.VideoCapture(str(SRC));b=cv2.VideoCapture(str(DEST));i=0;stats=[];samples={2595,2655,2714,3570,3600,3650,3951,4020,4082,6779}
    while True:
        ok,x=a.read();ok2,y=b.read();assert ok==ok2,i
        if not ok:break
        changed=any(lo<=i<hi for lo,hi in [INSERT,LABEL,NOTE])
        if i%30==0 and not changed:
            mse=float(np.mean((x.astype(float)-y.astype(float))**2));stats.append(mse)
        if i in samples:cv2.imwrite(str(OUT/'qa'/f'encoded-{i:05d}.jpg'),y)
        i+=1
    a.release();b.release();assert i==6780
    pts=[]
    with av.open(str(DEST)) as c:
        st=c.streams.video[0];tb=st.time_base
        for p in c.demux(st):
            if p.pts is not None:pts.append(p.pts)
    deltas=sorted(set(np.diff(sorted(pts)).tolist()))
    assert len(pts)==6780 and len(deltas)==1 and deltas[0]*tb==Fraction(1,30)
    assert max(stats)<50, max(stats) # compression error, not a content alteration
    result=dict(decoded_frames=i,seconds=i/30,audio_identical=True,audio=da,video_pts_delta_ticks=deltas,timebase=str(tb),
                unchanged_sample_count=len(stats),unchanged_mean_mse=float(np.mean(stats)),unchanged_max_mse=max(stats),
                source_sha256=EXPECTED,output_sha256=sha(DEST),status='Visual checks only; original narration defects remain.')
    (OUT/'qa'/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
