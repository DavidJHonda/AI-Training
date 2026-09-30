#!/usr/bin/env python3
"""Verify the encoded v3 visual repair and retain review evidence."""
import json
import sys
from pathlib import Path

import av
import cv2
import numpy as np
from PIL import Image, ImageDraw

import build_wheres_the_line_v3 as b
import transition_guard


def main():
    cv2.setNumThreads(2)
    manifest=json.loads((b.OUT/'edit-manifest.json').read_text())
    out=b.OUT/'encoded';out.mkdir(exist_ok=True)
    want={f+d for f in b.BOUNDARIES for d in [-1,0,1,15]}
    want|={3044,3316,3522,3786,4569,4907,5132,5408,5681,6058,3230,3710,4060,4770,5290}
    untouched={0,232,635,1500,2400,2850,3950,4300,5830,5900,6058}
    got={};pts=[];sample=[]
    with av.open(str(b.DEST)) as c:
        stream=c.streams.video[0];stream.codec_context.thread_count=2
        assert str(stream.average_rate)=='30'
        for n,f in enumerate(c.decode(video=0)):
            pts.append(float(f.pts*f.time_base))
            if n in want or n%150==0 or n in untouched:
                im=f.to_ndarray(format='bgr24')
                if n in want:cv2.imwrite(str(out/f'{n:06}.jpg'),im)
                if n in untouched:got[n]=f.to_ndarray(format='yuv420p')
                if n%150==0:sample.append((n,Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))))
    count=len(pts);assert count==b.TOTAL
    deltas=np.diff(pts);assert np.max(np.abs(deltas-1/30))<1e-6
    diff=[]
    with av.open(str(b.SOURCE)) as c:
        c.streams.video[0].codec_context.thread_count=2
        for n,f in enumerate(c.decode(video=0)):
            if n in untouched:
                x=f.to_ndarray(format='yuv420p').astype(np.int16)
                y=got[n].astype(np.int16)
                diff.append(dict(frame=n,mean_absolute_error=float(np.abs(x-y).mean()),
                                 mean_luma_shift=float((y[:720]-x[:720]).mean())))
    assert max(x['mean_absolute_error'] for x in diff)<3
    assert max(abs(x['mean_luma_shift']) for x in diff)<1
    for start in range(0,len(sample),12):
        sheet=Image.new('RGB',(1440,1200),'white');draw=ImageDraw.Draw(sheet)
        for i,(n,im) in enumerate(sample[start:start+12]):
            im=im.resize((480,270));x=(i%3)*480;y=(i//3)*300
            sheet.paste(im,(x,y));draw.text((x+10,y+275),f'{n/30:06.2f}s / frame {n}',fill='black')
        sheet.save(out/f'sheet-{start//12:02}.jpg',quality=90)
    assert b.audio_hash(b.SOURCE)==b.audio_hash(b.DEST)
    assert b.audio_hash(b.SOURCE,True)==b.audio_hash(b.DEST,True)
    assert all(b.sha(Path(p))==v for p,v in manifest['protected_hashes'].items())
    qa=dict(decoded_frames=count,fps=30,duration=count/30,pts_max_error=float(np.max(np.abs(deltas-1/30))),
        unchanged_picture_samples=diff,audio_packets_identical=True,decoded_audio_identical=True,
        source_unchanged=True,ring_stroke_design_px=4,
        board_runs_seconds={'uses':[10.4,13.0,4.5],'moves':[340/30,14.0,458/30]},
        listening='No direct audition; audio is bit-identical to installed source.',
        motion='Full sequential decode with sampled frames and every-frame transition strips; continuous playback not auditioned.')
    (b.OUT/'qa.json').write_text(json.dumps(qa,indent=2)+'\n')
    sys.argv=['transition_guard.py',str(b.DEST),'--outdir',str(b.OUT/'transitions')]
    for frame,label in sorted(b.BOUNDARIES.items()):sys.argv+=['--boundary',f'{frame}:{label}']
    transition_guard.main()
    print(json.dumps(qa,indent=2))


if __name__=='__main__':main()
