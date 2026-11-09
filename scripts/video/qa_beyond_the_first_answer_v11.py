#!/usr/bin/env python3
"""Check the approved opening, preserved tail, and encoded audio of v11."""
import json,subprocess
import cv2,numpy as np
from PIL import Image,ImageDraw
import build_beyond_the_first_answer_v11 as b

def psnr(a,c):
    mse=float(np.mean((a.astype(np.float32)-c.astype(np.float32))**2))
    return 99 if mse==0 else float(10*np.log10(255**2/mse))

def main():
    mapping,source=b.intro_frames()
    cap=cv2.VideoCapture(str(b.DEST));old=cv2.VideoCapture(str(b.prev.DEST))
    assert cap.get(cv2.CAP_PROP_FPS)==24
    for _ in range(b.prev.CUT):assert old.grab()
    checks=[];pictures=[];n=0
    sample={48,240,432,624,756,b.JOIN-1,b.JOIN,b.JOIN+24,b.JOIN+60,b.JOIN+108,b.JOIN+156,b.JOIN+191,b.JOIN+192,b.TOTAL-1}
    while True:
        ok,im=cap.read()
        if not ok:break
        if n<b.JOIN:
            ref=cv2.imdecode(source[mapping[n]],cv2.IMREAD_COLOR) if n%24==0 or n in sample else None
            kind='v2-opening'
        else:
            ok,ref=old.read();assert ok;kind='v10-retained'
        if n%24==0 or n in sample:
            metric=psnr(im,ref);assert metric>32,(n,metric)
            checks.append(dict(frame=n,kind=kind,psnr=metric))
        if n in sample:
            p=b.AUDIT/f'encoded-{n:04d}.jpg';cv2.imwrite(str(p),im);pictures.append((n,p))
            if n==b.JOIN+24:cv2.imwrite(str(b.AUDIT/'poster.jpg'),im)
        n+=1
    assert n==b.TOTAL and not old.grab();cap.release();old.release()
    for label,rows in [('opening',pictures[:6]),('overview-and-close',pictures[6:])]:
        sheet=Image.new('RGB',(1280,384*((len(rows)+1)//2)),'white');draw=ImageDraw.Draw(sheet)
        for i,(frame,p) in enumerate(rows):
            x=i%2*640;y=i//2*384;sheet.paste(Image.open(p).resize((640,360)),(x,y));draw.text((x+8,y+362),f'Frame {frame} / {frame/24:.3f}s',fill='black')
        sheet.save(b.AUDIT/f'encoded-{label}.jpg',quality=95)
    x=b.prev.decode_audio(b.AUDIT/'assembled-audio.wav');y=b.prev.decode_audio(b.DEST)[:len(x)]
    assert len(y)==len(x)
    corr=float(np.corrcoef(x,y)[0,1]);assert corr>.99
    qa=dict(frames=n,duration=n/24,checked_states=checks,minimum_psnr=min(c['psnr'] for c in checks),audio_correlation=corr,limitations='No listening pass; narration seam requires listening review.')
    (b.AUDIT/'qa.json').write_text(json.dumps(qa,indent=2))
    subprocess.run([b.FF,'-y','-v','error','-i',str(b.DEST),'-t','50','-vn','-c:a','pcm_s16le',str(b.AUDIT/'intro-encoded.wav')],check=True)
    subprocess.run([b.FF,'-y','-v','error','-i',str(b.DEST),'-t','50','-c','copy',str(b.AUDIT/'intro-preview.mp4')],check=True)
    print(json.dumps({k:v for k,v in qa.items() if k!='checked_states'},indent=2))

if __name__=='__main__':main()
