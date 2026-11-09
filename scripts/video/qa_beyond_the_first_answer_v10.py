#!/usr/bin/env python3
"""Verify the new overview and that v8's remaining picture sequence survives."""
import json,subprocess
import cv2,numpy as np
from PIL import Image,ImageDraw
import build_beyond_the_first_answer_v10 as b

def psnr(a,c):
    mse=float(np.mean((a.astype(np.float32)-c.astype(np.float32))**2))
    return 99 if mse==0 else float(10*np.log10(255**2/mse))

def main():
    cap=cv2.VideoCapture(str(b.DEST));old=cv2.VideoCapture(str(b.v8.DEST))
    assert cap.get(cv2.CAP_PROP_FPS)==24
    checks=[];pictures=[];n=0;images=b.art()
    sample={b.CUT+i for i in (0,24,60,108,156,191)}|{b.CUT-1,b.CUT+b.INSERT,b.CUT+b.INSERT+7,b.TOTAL-1}
    while True:
        ok,im=cap.read()
        if not ok:break
        if not b.CUT<=n<b.CUT+b.INSERT:
            ok,ref=old.read();assert ok
            if n%24==0 or n in sample:
                if b.CUT+b.INSERT<=n<657+b.INSERT:ref=cv2.imread(str(b.v8.AUDIT/'previews'/'thought-partner-0657.jpg'))
                metric=psnr(im,ref);assert metric>32,(n,metric)
                checks.append(dict(frame=n,kind='retained-v8',psnr=metric))
        elif n in sample:
            metric=psnr(im,b.overview(n-b.CUT,images));assert metric>32,(n,metric)
            checks.append(dict(frame=n,kind='overview',psnr=metric))
        if n in sample:
            p=b.AUDIT/f'encoded-{n:04d}.jpg';cv2.imwrite(str(p),im);pictures.append((n,p))
            if n==b.CUT+24:cv2.imwrite(str(b.AUDIT/'poster.jpg'),im)
        n+=1
    assert n==b.TOTAL and not old.grab();cap.release();old.release()
    sheet=Image.new('RGB',(1280,384*((len(pictures)+1)//2)),'white');draw=ImageDraw.Draw(sheet)
    for i,(frame,p) in enumerate(pictures):
        x=i%2*640;y=i//2*384;sheet.paste(Image.open(p).resize((640,360)),(x,y));draw.text((x+8,y+362),f'Frame {frame} / {frame/24:.3f}s',fill='black')
    sheet.save(b.AUDIT/'encoded-contact.jpg',quality=95)
    x=b.decode_audio(b.AUDIT/'assembled-audio.wav');y=b.decode_audio(b.DEST)
    y=y[:len(x)];assert len(y)==len(x)
    # AAC is freshly encoded once because narration has been inserted.
    corr=float(np.corrcoef(x,y)[0,1]);assert corr>.99,corr
    qa=dict(frames=n,duration=n/24,checked_states=checks,minimum_psnr=min(c['psnr'] for c in checks),audio_correlation=corr,limitations='No listening pass; ASR does not certify voice continuity or cadence.')
    (b.AUDIT/'qa.json').write_text(json.dumps(qa,indent=2))
    subprocess.run([b.v8.base.FF,'-y','-v','error','-i',str(b.DEST),'-ss','23','-t','18','-vn','-c:a','pcm_s16le',str(b.AUDIT/'intro-encoded.wav')],check=True)
    subprocess.run([b.v8.base.FF,'-y','-v','error','-i',str(b.DEST),'-t','45','-c','copy',str(b.AUDIT/'intro-preview.mp4')],check=True)
    print(json.dumps({k:v for k,v in qa.items() if k!='checked_states'},indent=2))

if __name__=='__main__':main()
