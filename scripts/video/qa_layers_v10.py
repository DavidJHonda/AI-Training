#!/usr/bin/env python3
"""Verify the encoded narrow repair, source identities, audio and join states."""
import json, hashlib, subprocess
import cv2, numpy as np, imageio_ffmpeg
from build_layers_v10 import OUT,DEST,BASE,ROOT,TOTAL,CHANGED,BOUNDARIES
from editspec_build import Reader,sha

def audio_hash(path,decoded=False):
    fmt=['-c:a','pcm_s16le','-f','s16le'] if decoded else ['-c:a','copy','-f','adts']
    b=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(path),'-map','0:a:0',*fmt,'pipe:1'],capture_output=True,check=True).stdout
    return hashlib.sha256(b).hexdigest()

def main():
    m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(DEST)==m['final_sha256']
    assert all(sha(p)==h for p,h in m['protected'].items())
    audio={kind:[audio_hash(BASE,decoded),audio_hash(DEST,decoded)] for kind,decoded in [('aac',False),('pcm',True)]}
    assert all(a==b for a,b in audio.values())
    previews={int(p.stem):p for p in (OUT/'preview').glob('*.png')}
    (OUT/'encoded').mkdir(exist_ok=True)
    cap=cv2.VideoCapture(str(DEST));rd=Reader(BASE);n=0;retained=[];changed=[];samples=[]
    while True:
        ok,im=cap.read()
        if not ok:break
        assert im.shape==(720,1280,3)
        different=any(a<=n<b for a,b in CHANGED)
        if not different and (n%15==0 or n==TOTAL-1):
            ref=rd.at(n);mad=float(np.abs(im.astype(float)-ref).mean());retained.append((n,mad));assert mad<5,(n,mad)
        if n in previews:
            ref=cv2.imread(str(previews[n]));mad=float(np.abs(im.astype(float)-ref).mean());changed.append((n,mad));assert mad<5,(n,mad)
            cv2.imwrite(str(OUT/'encoded'/f'{n:05d}.jpg'),im)
        if different and n%15==0:
            samples.append((n,cv2.resize(im,(384,216))))
        n+=1
    fps=cap.get(cv2.CAP_PROP_FPS);cap.release();rd.c.release();assert n==TOTAL and fps==30
    for j in range(0,len(samples),20):
        sheet=np.full((5*240,4*384,3),255,np.uint8)
        for k,(f,im) in enumerate(samples[j:j+20]):
            x=k%4*384;y=k//4*240;sheet[y:y+216,x:x+384]=im
            cv2.putText(sheet,f'{f/30:.3f}s / frame {f}',(x+5,y+234),cv2.FONT_HERSHEY_SIMPLEX,.5,(40,40,40),1,cv2.LINE_AA)
        cv2.imwrite(str(OUT/f'encoded-motion-{j//20}.jpg'),sheet)
    tracks=json.loads((OUT/'balance-tracking.json').read_text())
    errors=[z['error'] for row in tracks.values() for z in row.values() if z['error'] is not None]
    qa=dict(frames=n,fps=fps,duration=n/fps,audio_hashes=audio,aac_exact=True,pcm_exact=True,
            retained_samples=len(retained),retained_max_mad=max(v for _,v in retained),
            preview_samples=len(changed),preview_max_mad=max(v for _,v in changed),
            balance_tracking_median_error_px=float(np.median(errors)),balance_tracking_max_error_px=max(errors),
            source_hashes_unchanged=True,continuous_listening_performed=False)
    (OUT/'qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2),flush=True)
    # Guard the changed spans and internal source scene transitions; unchanged
    # parts have encoded comparisons rather than a claimed new full review.
    boundaries=sorted(set(BOUNDARIES+[2546,3216,5150,5416]))
    args=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'guard')]
    for f in boundaries:args+=['--boundary',f'{f}:visual-repair']
    result=subprocess.run(args,capture_output=True,text=True)
    (OUT/'guard-run.txt').write_text(result.stdout+result.stderr)
    print('Transition guard exit:',result.returncode,flush=True)

if __name__=='__main__':main()
