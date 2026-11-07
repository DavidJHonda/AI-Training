#!/usr/bin/env python3
"""Verify encoded v8, preserved AAC/timing, all seams, and retained pictures."""
import hashlib
import json
import subprocess
import av
import cv2
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import build_when_you_need_more_v8 as b
from editspec_build import sha

def audio_signature(path):
    digest=hashlib.sha256();times=[]
    with av.open(str(path)) as container:
        for packet in container.demux(audio=0):
            if packet.size:
                digest.update(bytes(packet));times.append([packet.pts,packet.dts,packet.duration,str(packet.time_base)])
    return dict(sha256=digest.hexdigest(),timings=times)

def main():
    cv2.setNumThreads(2);m=json.loads((b.OUT/'edit-manifest.json').read_text());out=b.OUT/'encoded';out.mkdir(exist_ok=True)
    source_audio=audio_signature(b.LIVE);candidate_audio=audio_signature(b.DEST)
    assert source_audio==candidate_audio,'AAC bytes or packet timing changed'
    samples=set(range(0,m['frames'],180))|{m['frames']-1}
    for row in b.INSERTS:
        samples.update(range(row['start'],row['end'],15))
    for edge in m['boundaries']:
        samples.update(range(edge['frame']-2,edge['frame']+3))
    live=cv2.VideoCapture(str(b.LIVE));errors=[];n=0;pts=[]
    with av.open(str(b.DEST)) as container:
        assert container.streams.video[0].average_rate==30
        for i,frame in enumerate(container.decode(video=0)):
            im=frame.to_ndarray(format='bgr24');assert im.shape==(720,1280,3)
            ok,old=live.read();assert ok
            if not any(row['start']<=i<row['end'] for row in b.INSERTS):
                small=cv2.resize(im,(320,180)).astype(float);ref=cv2.resize(old,(320,180)).astype(float)
                errors.append(float(np.abs(small-ref).mean()))
            if i in samples:cv2.imwrite(str(out/f'frame-{i:05d}.jpg'),im)
            pts.append(float(frame.pts*frame.time_base));n+=1
    assert n==5069 and not live.read()[0];live.release()
    assert np.max(np.abs(np.diff(pts)-1/30))<1e-6
    assert max(errors)<3,(max(errors),'retained picture mismatch')
    assert all(sha(path)==digest for path,digest in m['protected_hashes'].items())
    args=[str(b.ROOT/'.video-venv/bin/python'),str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),
          '--outdir',str(b.OUT/'transitions')]
    for edge in m['boundaries']:args.extend(['--boundary',f'{edge["frame"]}:{edge["label"]}'])
    subprocess.run(args,check=True)
    font=ImageFont.truetype(str(b.base.FONT),15)
    sets={'overview':[f for f in sorted(samples) if f%180==0 or f==5068],
          'inserts':[f for f in sorted(samples) if any(r['start']<=f<r['end'] for r in b.INSERTS) and f%15==0]}
    for name,frames in sets.items():
        for page in range((len(frames)+15)//16):
            sheet=Image.new('RGB',(1280,800),'white');draw=ImageDraw.Draw(sheet)
            for j,f in enumerate(frames[page*16:(page+1)*16]):
                x=j%4*320;y=j//4*200;im=Image.open(out/f'frame-{f:05d}.jpg').resize((320,180));sheet.paste(im,(x,y))
                draw.text((x+5,y+181),f'{f/30:.2f}s / frame {f}',font=font,fill='black')
            sheet.save(b.OUT/f'encoded-{name}-{page}.jpg')
    result=dict(frames=n,duration=n/30,fps=30,continuous_video_timestamps=True,
                audio_packet_bytes_and_timings_identical=True,audio_sha256=source_audio['sha256'],
                retained_picture_max_MAE=max(errors),retained_picture_mean_MAE=float(np.mean(errors)),
                protected_files_unchanged=True,transition_boundaries=len(m['boundaries']),
                limitation='No continuous audiovisual listening. Encoded frame-sequence inspection and technical checks only.')
    (b.OUT/'qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
