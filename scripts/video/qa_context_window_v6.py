#!/usr/bin/env python3
"""Verify the narrow Context Window label repair and save encoded evidence."""
from pathlib import Path
import hashlib, json, subprocess
import av, cv2, imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/context-window-label-repair-2026-09-29'
SRC=ROOT/'Prompts/context-window-v5.mp4'
DST=OUT/'working.mp4'

def packet_hash(path):
    h=hashlib.sha256(); n=0
    with av.open(str(path)) as c:
        for p in c.demux(c.streams.audio[0]):
            if p.size:h.update(bytes(p));n+=1
    return {'sha256':h.hexdigest(),'packets':n}

def main():
    sa,da=packet_hash(SRC),packet_hash(DST)
    assert sa==da,'Audio changed'
    cap=cv2.VideoCapture(str(DST));i=0
    wanted={2040,6555,6556,6570,6609,6709,6790,6800,6850,6871,6872,6907,6915,6927,6931,6940,6960,7065,7080,7095,7112,7113,7460}
    while True:
        ok,im=cap.read()
        if not ok:break
        if i in wanted:cv2.imwrite(str(OUT/f'encoded-{i}.jpg'),im)
        i+=1
    cap.release();assert i==7461
    d={'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(DST.read_bytes()).hexdigest(),'frames':i,'fps':30,'duration_seconds':i/30,'audio_unchanged':True,'audio':da,'edit_span_frames':[6556,7113],'edit_span_seconds':[6556/30,7113/30]}
    (OUT/'qa.json').write_text(json.dumps(d,indent=2)+'\n')
    subprocess.run([str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DST),'--boundary','6556:original-to-repaired-animation','--boundary','7113:animation-to-close','--outdir',str(OUT/'transitions')],check=True)
    print(json.dumps(d,indent=2))

if __name__=='__main__':main()
