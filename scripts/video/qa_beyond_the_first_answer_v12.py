#!/usr/bin/env python3
"""Check new overview timings and preserve v11's surrounding video/audio."""
import json,subprocess
import cv2,numpy as np
from PIL import Image,ImageDraw
import build_beyond_the_first_answer_v12 as b

def psnr(a,c):
    mse=float(np.mean((a.astype(np.float32)-c.astype(np.float32))**2))
    return 99 if mse==0 else float(10*np.log10(255**2/mse))

def main():
    cap=cv2.VideoCapture(str(b.DEST));old=cv2.VideoCapture(str(b.old.DEST))
    assert cap.get(cv2.CAP_PROP_FPS)==24
    images=b.old.prev.art();checks=[];pictures=[];n=0
    samples={b.JOIN-1,b.JOIN,b.JOIN+b.OVERVIEW-1,b.JOIN+b.OVERVIEW,b.TOTAL-1}|{b.JOIN+int(np.ceil(t*24))+4 for t in b.ONSETS}
    while True:
        ok,im=cap.read()
        if not ok:break
        if n==b.JOIN:
            for _ in range(b.old.prev.INSERT):assert old.grab()
        if b.JOIN<=n<b.JOIN+b.OVERVIEW:
            ref=b.overview(n-b.JOIN,images) if n in samples else None;kind='new-overview'
        else:
            ok,ref=old.read();assert ok;kind='retained-v11'
        if n in samples or (kind=='retained-v11' and n%24==0):
            metric=psnr(im,ref);assert metric>32,(n,metric)
            checks.append(dict(frame=n,kind=kind,psnr=metric))
        if n in samples:
            p=b.AUDIT/f'encoded-{n:04d}.jpg';cv2.imwrite(str(p),im);pictures.append((n,p))
        n+=1
    assert n==b.TOTAL and not old.grab();cap.release();old.release()
    sheet=Image.new('RGB',(1280,384*((len(pictures)+1)//2)),'white');draw=ImageDraw.Draw(sheet)
    for i,(frame,p) in enumerate(pictures):
        x=i%2*640;y=i//2*384;sheet.paste(Image.open(p).resize((640,360)),(x,y));draw.text((x+8,y+362),f'Frame {frame} / {frame/24:.3f}s',fill='black')
    sheet.save(b.AUDIT/'encoded-contact.jpg',quality=95)
    x=b.old.prev.decode_audio(b.AUDIT/'assembled-audio.wav');y=b.old.prev.decode_audio(b.DEST)[:len(x)]
    assert len(y)==len(x)
    corr=float(np.corrcoef(x,y)[0,1]);assert corr>.99
    qa=dict(frames=n,duration=n/24,checked_states=checks,minimum_psnr=min(c['psnr'] for c in checks),audio_correlation=corr,limitations='No listening pass. Source recording kept at natural speed; joins require listening review.')
    (b.AUDIT/'qa.json').write_text(json.dumps(qa,indent=2))
    subprocess.run([b.FF,'-y','-v','error','-i',str(b.DEST),'-ss','30','-t','21','-vn','-c:a','pcm_s16le',str(b.AUDIT/'join-encoded.wav')],check=True)
    subprocess.run([b.FF,'-y','-v','error','-i',str(b.DEST),'-t','52','-c','copy',str(b.AUDIT/'intro-preview.mp4')],check=True)
    print(json.dumps({k:v for k,v in qa.items() if k!='checked_states'},indent=2))

if __name__=='__main__':main()
