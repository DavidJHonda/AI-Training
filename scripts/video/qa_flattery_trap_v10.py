#!/usr/bin/env python3
"""Verify decoded frame identity outside edits, AAC identity, and timeline."""
from pathlib import Path
import hashlib
import json
import subprocess
import av
import cv2
import numpy as np
from build_flattery_trap_v10 import ROOT, OUT, SRC, DEST, SPANS, FF, sha

def packet_signature(path, kind):
    with av.open(str(path)) as c:
        stream = next(s for s in c.streams if s.type == kind)
        return [(p.pts,p.dts,p.duration,str(p.time_base),hashlib.sha256(bytes(p)).hexdigest())
                for p in c.demux(stream) if p.dts is not None]

def main():
    audio1=packet_signature(SRC,'audio'); audio2=packet_signature(DEST,'audio')
    assert audio1 == audio2, 'Audio packet bytes or timestamps changed'
    v1=packet_signature(SRC,'video'); v2=packet_signature(DEST,'video')
    keep=lambda packets: [p for p in packets if not any(a<=p[0]/512<b for a,b,_ in SPANS)]
    assert keep(v1)==keep(v2), 'Unedited compressed video packets changed'
    ca=cv2.VideoCapture(str(SRC)); cb=cv2.VideoCapture(str(DEST))
    assert ca.get(cv2.CAP_PROP_FPS)==cb.get(cv2.CAP_PROP_FPS)==30
    unchanged=changed=count=0; saved=[]
    checks={f for a,b,_ in SPANS for f in (a-1,a,a+1,(a+b)//2,b-2,b-1,b)}
    while True:
        oka,a=ca.read();okb,b=cb.read();assert oka==okb
        if not oka: break
        edited=any(x<=count<y for x,y,_ in SPANS)
        same=np.array_equal(a,b)
        if not edited:
            assert same, ('Unexpected pixel change outside the two scenes',count)
            unchanged+=1
        else:
            assert not same
            changed+=1
        if count in checks:
            cv2.imwrite(str(OUT/f'encoded-{count:05}.png'),b);saved.append(count)
        count+=1
    assert count==9431 and changed==290
    decoded_audio=[]
    for path in (SRC,DEST):
        raw=subprocess.check_output([FF,'-v','error','-i',str(path),'-map','0:a:0','-f','s16le','-'])
        decoded_audio.append({'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    assert decoded_audio[0]==decoded_audio[1]
    report={'candidate_sha256':sha(DEST),'frames':count,'fps':30,'duration_seconds':count/30,
            'changed_frames':changed,'unchanged_frames_pixel_identical':unchanged,
            'all_audio_packets_and_timestamps_identical':True,'audio_packets':len(audio1),
            'decoded_audio':decoded_audio,'unaffected_video_packets_identical':True,
            'saved_encoded_frames':saved,'direct_listening_performed':False}
    (OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
