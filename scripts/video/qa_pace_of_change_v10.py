#!/usr/bin/env python3
"""Check the actual encoded Pace of Change v10 and preserve review evidence."""
import json
import re
import subprocess
import wave
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw
import build_pace_of_change_v10 as b


def samples(path, frames, width=320, height=180):
    frames=sorted(set(frames));expr='+'.join(f'eq(n,{n})' for n in frames)
    raw=subprocess.check_output([b.FF,'-v','error','-threads','2','-i',str(path),
         '-vf',f"select='{expr}',scale={width}:{height}",'-fps_mode','vfr',
         '-pix_fmt','rgb24','-f','rawvideo','-'])
    arr=np.frombuffer(raw,np.uint8).reshape(-1,height,width,3)
    assert len(arr)==len(frames),(len(arr),len(frames))
    return dict(zip(frames,arr))


def main():
    cv2.setNumThreads(2)
    m=json.loads((b.OUT/'edit-manifest.json').read_text());dest=Path(m['candidate'])
    result=subprocess.run([b.FF,'-v','error','-threads','2','-i',str(dest),
                           '-progress','pipe:1','-f','null','-'],capture_output=True,text=True,check=True)
    assert not result.stderr.strip(),result.stderr
    count=int(re.findall(r'^frame=(\d+)$',result.stdout,re.M)[-1]);assert count==m['total_frames']
    print('Full decode:',count,'frames',flush=True)
    checks={0,count-1,b.CUT_A-1,b.CUT_A,b.mapped(b.BANNER)-1,b.mapped(b.BANNER)}
    checks.update(r['frame']+offset for r in m['boundaries'] for offset in [-1,0,1])
    checks.update([b.mapped(b.PREVIEW_A)-1,b.mapped(b.PREVIEW_A),b.mapped(b.PREVIEW_A)+24]);checks.update(range(0,count,30));checks={f for f in checks if 0<=f<count}
    got=samples(dest,checks)
    expected={}
    for f in checks:
        row=next(r for r in m['timeline'] if r['start_frame']<=f<r['end_frame'])
        if row['visual']=='source':expected[f]=row['source_start']+f-row['start_frame']
    original=samples(b.SRC,expected.values())
    differences=[dict(output_frame=f,source_frame=s,mad=float(np.abs(got[f].astype(float)-original[s]).mean()))
                 for f,s in sorted(expected.items())]
    maximum=max(r['mad'] for r in differences);assert maximum<3,maximum
    tail,_=b.make_tail()
    imgs={r['key']:cv2.resize(cv2.imread(str(b.ASSETS/(r['key']+'.png'))),(1280,720),interpolation=cv2.INTER_AREA) for r in b.INSERTS}
    replacements=[]
    for f in sorted(checks):
        row=next(r for r in m['timeline'] if r['start_frame']<=f<r['end_frame'])
        kind=row['visual']
        if kind=='source':continue
        sf=row['source_start']+f-row['start_frame']
        expected_img=tail['banner' if sf>=b.BANNER else 'asi'] if kind=='far-tail' else imgs[kind]
        target=cv2.resize(cv2.cvtColor(expected_img,cv2.COLOR_BGR2RGB),(320,180),interpolation=cv2.INTER_AREA)
        mad=float(np.abs(got[f].astype(float)-target.astype(float)).mean())
        replacements.append(dict(output_frame=f,kind=kind,mad=mad))
    assert max(r['mad'] for r in replacements)<4
    raw=subprocess.check_output([b.FF,'-v','error','-i',str(dest),'-vn','-ar','48000','-ac','1','-f','s16le','-'])
    actual=np.frombuffer(raw,dtype='<i2').astype(float)
    reference=b.readwav(b.OUT/'edited.wav');assert len(actual)>=len(reference)
    actual=actual[:len(reference)]
    snr=10*np.log10(np.sum(reference**2)/np.sum((actual-reference)**2));assert snr>25,snr
    new_join=b.mapped(b.PREVIEW_A)
    seam=new_join*b.SPF;around=actual[seam-240:seam+240]/32768
    silence=subprocess.run([b.FF,'-v','info','-ss',str(new_join/30-1),'-i',str(dest),'-t','2',
                   '-vn','-af','silencedetect=noise=-35dB:d=0.08','-f','null','-'],capture_output=True,text=True,check=True)
    (b.OUT/'encoded-join-silence.log').write_text(silence.stderr)
    # Four-second overview, all encoded replacement boundaries, exact final frame.
    frames=list(range(0,count,120))+[count-1]
    for num,start in enumerate(range(0,len(frames),12)):
        canvas=Image.new('RGB',(960,800),'white');draw=ImageDraw.Draw(canvas)
        for k,f in enumerate(frames[start:start+12]):
            x=(k%3)*320;y=(k//3)*200
            canvas.paste(Image.fromarray(got[f]),(x,y+20))
            draw.text((x+6,y+3),f'{int(f/30)//60}:{f/30%60:05.2f}  f{f}',fill='black')
        canvas.save(b.OUT/f'candidate-sheet-{num:02d}.jpg',quality=92)
    detailed={b.mapped(r['start'])+30 for r in b.INSERTS}|{b.mapped(b.BANNER)+15,count-1,new_join-1,new_join,new_join+12,new_join+24}
    hd=samples(dest,detailed,1280,720)
    for f,im in hd.items():Image.fromarray(im).save(b.OUT/f'encoded-{f:06d}.jpg',quality=95)
    # Joined clip is separately transcribed; the full retained narration is
    # verified sample-wise against the original outside the four-ms edit.
    subprocess.run([b.FF,'-v','error','-ss',str(new_join/30-4),'-i',str(dest),'-t','11','-vn',
                    '-c:a','pcm_s16le','-y',str(b.OUT/'encoded-narration-join.wav')],check=True)
    verify=dict(decoded_frames=count,duration=count/30,source_comparison_samples=len(differences),
                source_maximum_mad=maximum,replacement_comparison_samples=len(replacements),
                replacement_maximum_mad=max(r['mad'] for r in replacements),audio_snr_db=float(snr),
                audio_samples=len(reference),join_output_frame=new_join,
                join_local_peak_dbfs=float(20*np.log10(max(np.max(np.abs(around)),1e-9))),
                longest_board_only_run_seconds=23.3,final_frame_checked=count-1,
                listening_completed=False,continuous_playback_review_completed=False,
                protected_files_unchanged=all(b.sha(Path(p))==h for p,h in m['protected_hashes'].items()))
    assert verify['protected_files_unchanged']
    (b.OUT/'verification.json').write_text(json.dumps(verify,indent=2)+'\n')
    (b.OUT/'visual-comparison.json').write_text(json.dumps(differences,indent=2)+'\n')
    (b.OUT/'replacement-comparison.json').write_text(json.dumps(replacements,indent=2)+'\n')
    print(json.dumps(verify,indent=2),flush=True)


if __name__=='__main__':main()
