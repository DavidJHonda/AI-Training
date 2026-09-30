#!/usr/bin/env python3
"""Check new candidate against v2 and inspect the repaired board-return span."""
import json
from fractions import Fraction
import cv2,av,numpy as np
from build_document_trap_v3 import base,OUT,DEST,START,END
from qa_document_trap_v2 import audio_info
cv2.setNumThreads(2)

def main():
    qa=OUT/'qa';qa.mkdir(exist_ok=True)
    audio=audio_info(DEST);assert audio==audio_info(base.DEST)==audio_info(base.SRC)
    a=cv2.VideoCapture(str(base.DEST));b=cv2.VideoCapture(str(DEST));n=0;outside=[];inside=[];hold=None
    wanted={START-1,START,5850,5900,END-1,END,END+30,6779}
    while True:
        ok,x=a.read();ok2,y=b.read();assert ok==ok2,n
        if not ok:break
        if n==START-1:hold=y.copy()
        if START<=n<END:
            inside.append(float(np.mean((y.astype(float)-hold.astype(float))**2)))
        elif n%30==0:
            outside.append(float(np.mean((x.astype(float)-y.astype(float))**2)))
        if n in wanted:cv2.imwrite(str(qa/f'encoded-{n}.jpg'),y)
        n+=1
    a.release();b.release();assert n==6780
    assert max(outside)<50,max(outside)
    assert len(inside)==124 and max(inside)<50,max(inside)
    pts=[]
    with av.open(str(DEST)) as c:
        s=c.streams.video[0];tb=s.time_base
        for p in c.demux(s):
            if p.pts is not None:pts.append(p.pts)
    diffs=sorted(set(np.diff(sorted(pts)).tolist()))
    assert len(pts)==6780 and len(diffs)==1 and diffs[0]*tb==Fraction(1,30)
    result=dict(decoded_frames=n,duration=n/30,audio_identical_to_v2_and_original=True,audio=audio,
        unchanged_samples=len(outside),unchanged_max_mse=max(outside),quote_hold_frames=len(inside),quote_hold_max_mse=max(inside),
        uniform_frame_timing=True,output_sha256=base.sha(DEST))
    (qa/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
