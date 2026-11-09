#!/usr/bin/env python3
"""Check actual v15 edit mapping, edited boards, audio, and all new joins."""
import json,subprocess,sys
import cv2,numpy as np
from PIL import Image,ImageDraw
import build_beyond_the_first_answer_v15 as b

def main():
    plan=json.loads((b.AUDIT/'edit-manifest.json').read_text())
    cap=cv2.VideoCapture(str(b.DEST));old=cv2.VideoCapture(str(b.SOURCE))
    assert cap.get(cv2.CAP_PROP_FPS)==24
    expected={int(p.stem.split('-')[-1]):p for p in b.AUDIT.glob('expected-*.png')}
    oldpos=0;checks=[];pictures=[]
    for n,source_n in enumerate(b.MAPPING):
        while oldpos<source_n:assert old.grab();oldpos+=1
        ok,ref=old.read();assert ok;oldpos+=1
        ok,im=cap.read();assert ok
        # These boards restart their 2% push after the removed preambles.
        moved=(1774<=source_n<2519) or (3112<=source_n<3886)
        if n in expected:ref=cv2.imread(str(expected[n]))
        if n in expected or (not moved and n%24==0):
            mse=float(np.mean((im.astype(np.float32)-ref.astype(np.float32))**2))
            metric=99 if mse==0 else float(10*np.log10(255**2/mse))
            assert metric>32,(n,source_n,metric)
            checks.append(dict(frame=n,source_frame=source_n,psnr=metric,kind='render-reference' if n in expected else 'retained-v14'))
        if n in expected:
            p=b.AUDIT/f'encoded-{n}.jpg';cv2.imwrite(str(p),im);pictures.append((n,p))
    assert not cap.grab() and not old.grab();cap.release();old.release()
    sheet=Image.new('RGB',(1280,384*((len(pictures)+1)//2)),'white');draw=ImageDraw.Draw(sheet)
    for i,(frame,p) in enumerate(pictures):
        x=i%2*640;y=i//2*384;sheet.paste(Image.open(p).resize((640,360)),(x,y));draw.text((x+8,y+362),f'Frame {frame} / {frame/24:.3f}s',fill='black')
    sheet.save(b.AUDIT/'encoded-contact.jpg',quality=95)
    x=b.old.prev.old.prev.decode_audio(b.AUDIT/'assembled-audio.wav')
    y=b.old.prev.old.prev.decode_audio(b.DEST)[:len(x)]
    assert len(x)==len(y)==b.TOTAL*2000
    corr=float(np.corrcoef(x,y)[0,1]);assert corr>.999
    joins=[]
    for n in b.JOINS:
        k=n*2000;span=y[k-4800:k+4800]
        # 10 ms immediately around each splice must remain quiet after AAC encoding.
        rms=float(np.sqrt(np.mean(y[k-240:k+240]**2)))
        assert rms<.003
        joins.append(dict(frame=n,seconds=n/24,join_rms_dbfs=float(20*np.log10(max(rms,1e-10)))))
    qa=dict(frames=b.TOTAL,fps=24,duration=b.TOTAL/24,checked_states=checks,minimum_psnr=min(c['psnr'] for c in checks),audio_correlation=corr,joins=joins)
    (b.AUDIT/'qa.json').write_text(json.dumps(qa,indent=2))
    boundaries={n:label for n,(_,_,label) in zip(b.JOINS,b.CUTS)}
    for slug,(a,z) in plan['board_spans'].items():boundaries.setdefault(a,'enter-'+slug);boundaries.setdefault(z,'exit-'+slug)
    boundaries[b.output_frame(b.old.START)]='iteration-title';boundaries[b.output_frame(b.old.END)]='iteration-definition'
    subprocess.run([sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),*[item for n,label in sorted(boundaries.items()) for item in ('--boundary',f'{n}:{label}')],'--outdir',str(b.AUDIT/'transitions')],check=True)
    for label,a,z in [('thought-partner-joins',44,66),('learn-join',96,113)]:
        subprocess.run([b.FF,'-y','-v','error','-i',str(b.DEST),'-ss',str(a),'-t',str(z-a),'-vn','-c:a','pcm_s16le',str(b.AUDIT/f'{label}.wav')],check=True)
    print(json.dumps({k:v for k,v in qa.items() if k!='checked_states'},indent=2))

if __name__=='__main__':main()
