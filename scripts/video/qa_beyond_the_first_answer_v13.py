#!/usr/bin/env python3
"""Verify v13 title and unchanged timing, audio payload, and retained picture states."""
import json, subprocess, sys
import cv2, numpy as np
from PIL import Image,ImageDraw
import build_beyond_the_first_answer_v13 as b

def main():
    cap=cv2.VideoCapture(str(b.DEST));old=cv2.VideoCapture(str(b.prev.DEST))
    assert cap.get(cv2.CAP_PROP_FPS)==24
    samples={b.START-1,b.START,b.START+28,b.END-1,b.END,b.END+24,b.TOTAL-1}
    pictures=[];checks=[];n=0
    while True:
        ok,im=cap.read()
        if not ok:break
        ok,ref=old.read();assert ok
        changed=b.START<=n<b.END
        if changed and n in samples:ref=cv2.imread(str(b.AUDIT/f'expected-{n}.png'))
        if (not changed and n%24==0) or n in samples:
            mse=float(np.mean((im.astype(np.float32)-ref.astype(np.float32))**2))
            metric=99 if mse==0 else float(10*np.log10(255**2/mse))
            assert metric>32,(n,metric)
            checks.append(dict(frame=n,kind='new-title' if changed else 'retained-v12',psnr=metric))
        if n in samples:
            p=b.AUDIT/f'encoded-{n}.jpg';cv2.imwrite(str(p),im);pictures.append((n,p))
        n+=1
    assert n==b.TOTAL and not old.grab();cap.release();old.release()
    sheet=Image.new('RGB',(1280,384*((len(pictures)+1)//2)),'white');draw=ImageDraw.Draw(sheet)
    for i,(frame,p) in enumerate(pictures):
        x=i%2*640;y=i//2*384;sheet.paste(Image.open(p).resize((640,360)),(x,y));draw.text((x+8,y+362),f'Frame {frame} / {frame/24:.3f}s',fill='black')
    sheet.save(b.AUDIT/'encoded-contact.jpg',quality=95)
    audio=b.base.audio_sha(b.DEST);assert audio==b.base.audio_sha(b.prev.DEST)
    qa=dict(frames=n,fps=24,duration=n/24,checked_states=checks,minimum_psnr=min(c['psnr'] for c in checks),audio_payload_sha256=audio,audio_packets_identical=True)
    (b.AUDIT/'qa.json').write_text(json.dumps(qa,indent=2))
    subprocess.run([sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--boundary',f'{b.START}:iteration-title','--boundary',f'{b.END}:iteration-definition','--outdir',str(b.AUDIT/'transitions')],check=True)
    print(json.dumps({k:v for k,v in qa.items() if k!='checked_states'},indent=2))

if __name__=='__main__':main()
