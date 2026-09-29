#!/usr/bin/env python3
"""Check the encoded v9 file against its hash-pinned v8 source."""
import hashlib
import json
from pathlib import Path
import subprocess
import cv2
import numpy as np
import av
from PIL import Image, ImageDraw
from build_art_of_prompting_v9 import ROOT, OUT, SOURCE, DEST, SPANS, SHA, sha


def audio_signature(path):
    h=hashlib.sha256();packets=0;pts=[]
    with av.open(str(path)) as c:
        stream=c.streams.audio[0]
        for packet in c.demux(stream):
            if packet.size:
                h.update(bytes(packet));packets+=1;pts.append([packet.pts,packet.duration])
    return {'sha256':h.hexdigest(),'packets':packets,'pts':pts}


def main():
    assert sha(SOURCE)==SHA
    a,b=audio_signature(SOURCE),audio_signature(DEST)
    assert a==b,'Audio bytes or timestamps changed'
    a.pop('pts')
    src=cv2.VideoCapture(str(SOURCE));dst=cv2.VideoCapture(str(DEST))
    fps=dst.get(cv2.CAP_PROP_FPS);assert fps==30
    targets={3446,3447,3590,3729,3730,4303,4304,4391,4392,4397,4403,4488,4489,4888,6466,6467,6514,6664,6935}
    (OUT/'encoded').mkdir(exist_ok=True)
    i=0;max_diff=0;max_at=None
    while True:
        oka,fa=src.read();okb,fb=dst.read()
        assert oka==okb,(i,oka,okb)
        if not oka:break
        assert fb.shape==(720,1280,3)
        if not any(start<=i<end for start,end in SPANS):
            diff=np.abs(cv2.resize(fa,(160,90)).astype(float)-cv2.resize(fb,(160,90))).mean()
            if diff>max_diff:max_diff=float(diff);max_at=i
        if i in targets:cv2.imwrite(str(OUT/'encoded'/f'f{i:05}.jpg'),fb)
        i+=1
    src.release();dst.release()
    assert i==6936,i
    assert max_diff<3,(max_diff,max_at)
    close=[]
    for n in (6467,6514,6664,6935):
        im=cv2.imread(str(OUT/'encoded'/f'f{n:05}.jpg'))
        mask=(np.max(im,axis=2)<80).astype(np.uint8)
        _,_,stats,_=cv2.connectedComponentsWithStats(mask)
        box=max(stats[1:],key=lambda x:x[4]).tolist()
        close.append({'frame':n,'pill_bbox':box,'background_rgb':im[10,10][::-1].tolist()})
    # H.264 chroma quantization and JPEG audit export can move nominal white
    # by a few levels. Reject a tint beyond that small encode tolerance.
    assert all(min(x['background_rgb'])>=250 and
               max(x['background_rgb'])-min(x['background_rgb'])<=4 for x in close)
    ratio=close[-1]['pill_bbox'][2]/close[0]['pill_bbox'][2]
    assert abs(ratio-1.2)<.005,ratio
    record={'frames':i,'fps':fps,'duration':i/fps,'audio_byte_and_timestamp_identical':True,
            'audio':a,'unaffected_max_mae_160x90':max_diff,'unaffected_max_mae_frame':max_at,
            'close':close,'close_ratio':ratio,'source_still_matches':sha(SOURCE)==SHA,
            'canonical_live_unchanged':sha(ROOT/'course-assets/art-of-prompting/art-of-prompting.mp4')==SHA}
    (OUT/'verification.json').write_text(json.dumps(record,indent=2)+'\n')
    files=sorted((OUT/'encoded').glob('*.jpg'))
    for start in range(0,len(files),6):
        part=files[start:start+6];sheet=Image.new('RGB',(1280,390*((len(part)+1)//2)),'white');draw=ImageDraw.Draw(sheet)
        for j,f in enumerate(part):
            x=j%2*640;y=j//2*390
            draw.text((x+5,y+5),f.stem,fill='black');sheet.paste(Image.open(f).resize((640,360)),(x,y+25))
        sheet.save(OUT/f'encoded-sheet-{start//6}.jpg')
    old=json.loads((ROOT/'video-audit/art-of-prompting-live-review-2026-09-29/guard/transition-guard.json').read_text())
    bounds={b['frame']:b['label'] for b in old['boundaries']}
    bounds.update({3447:'document-cleanup-in',4304:'weak-caption-in',4489:'weak-caption-out'})
    cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'guard')]
    for frame,label in sorted(bounds.items()):cmd+=['--boundary',f'{frame}:{label}']
    subprocess.run(cmd,check=True)
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
