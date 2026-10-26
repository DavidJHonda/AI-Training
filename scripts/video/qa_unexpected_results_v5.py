#!/usr/bin/env python3
"""Check the final combined encode; do not confuse ASR with listening."""
import json
import subprocess
import sys
import wave
from pathlib import Path

import av
import cv2
import numpy as np
from PIL import Image, ImageDraw

from build_unexpected_results_v5 import OUT, DEST, FF, SR, SPF, sha, Picture


def main():
    cv2.setNumThreads(2)
    m=json.loads((OUT/'edit-manifest.json').read_text())
    assert sha(DEST)==m['candidate_sha256']
    assert all(sha(p)==h for p,h in m['protected_hashes'].items())
    wanted={0,m['frames']-1}
    for row in m['rows']:
        wanted.update((row['start'],row['start']+30,row['end']-1))
    for f in m['boundaries']:
        wanted.update((f-1,f,f+1))
    wanted.update(range(0,m['frames'],180))
    wanted.update((3710,3750,4250,4320,4400,5828,5876,6025,6147))
    folder=OUT/'encoded-frames'
    folder.mkdir(exist_ok=True)
    pts=[]
    tiles=[]
    comparison=[]
    pic=Picture(m['rows'])
    with av.open(str(DEST)) as c:
        v=c.streams.video[0]
        v.thread_count=2
        assert v.average_rate==30 and (v.width,v.height)==(1280,720)
        for i,f in enumerate(c.decode(v)):
            pts.append(f.pts)
            if i in wanted:
                im=f.to_ndarray(format='bgr24')
                cv2.imwrite(str(folder/f'{i:05d}.jpg'),im)
                row=next(r for r in m['rows'] if r['start']<=i<r['end'])
                expected,kind=pic.draw(row,i)
                error=float(cv2.absdiff(im,expected).mean())
                assert error<6,(i,error,kind)
                comparison.append(dict(frame=i,kind=kind,mean_absolute_error=error))
            if i%180==0 or i==m['frames']-1:
                tile=Image.new('RGB',(320,204),'white')
                tile.paste(f.to_image().resize((320,180)),(0,0))
                ImageDraw.Draw(tile).text((5,184),f'{i/30:.2f}s / f{i}',fill='black')
                tiles.append(tile)
    assert len(pts)==m['frames'] and len(set(np.diff(pts)))==1
    for page in range((len(tiles)+19)//20):
        batch=tiles[page*20:(page+1)*20]
        sheet=Image.new('RGB',(1280,204*((len(batch)+3)//4)),'white')
        for j,t in enumerate(batch):sheet.paste(t,((j%4)*320,(j//4)*204))
        sheet.save(OUT/f'contact-sheet-{page+1}.jpg')
    encoded=np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(DEST),
        '-vn','-ac','1','-ar',str(SR),'-f','f32le','-']),np.float32)
    with wave.open(str(OUT/'edited.wav')) as w:
        expected=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768
    assert 0<=len(encoded)-len(expected)<1024
    assert np.max(np.abs(encoded))<1
    joins=[]
    reel=[]
    for r in m['rows'][1:]:
        if r['kind']=='close-hold':continue
        f=r['start'];s=f*SPF;lo=max(0,s-2*SR);hi=min(len(expected),s+2*SR)
        corr=float(np.corrcoef(encoded[lo:hi],expected[lo:hi])[0,1])
        assert corr>.99,(r['kind'],corr)
        q=encoded[s-480:s+480]
        db=20*np.log10(max(float(np.sqrt(np.mean(q*q))),1e-12))
        assert db<-40,(r['kind'],db)
        joins.append(dict(frame=f,seconds=f/30,kind=r['kind'],correlation=corr,rms_db=db))
        reel.extend((encoded[lo:hi],np.zeros(SR//2,np.float32)))
    with wave.open(str(OUT/'join-review.wav'),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
        w.writeframes(np.rint(np.concatenate(reel)*32767).astype('<i2').tobytes())
    silence=subprocess.run([FF,'-hide_banner','-i',str(DEST),'-af',
        'silencedetect=noise=-40dB:d=0.12','-f','null','-'],capture_output=True,text=True,check=True)
    (OUT/'silence-detection.txt').write_text(silence.stderr)
    report=dict(candidate_sha256=sha(DEST),decoded_frames=len(pts),fps=30,
        duration_seconds=m['duration_seconds'],pts_deltas=sorted(set(np.diff(pts).tolist())),
        protected_files_unchanged=True,sampled_picture_checks=comparison,
        encoded_audio_peak=float(np.max(np.abs(encoded))),audio_joins=joins,
        longest_board_run_seconds=m['longest_board_run_seconds'],
        direct_listening_performed=False,continuous_audiovisual_playback_performed=False,
        listening_reel='join-review.wav: two seconds each side, then half-second reel-only separators')
    (OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
    command=[sys.executable,str(Path(__file__).with_name('transition_guard.py')),str(DEST),
             '--outdir',str(OUT/'transitions')]
    for f in m['boundaries']:command+=['--boundary',f'{f}:combined-edit']
    result=subprocess.run(command,check=False)
    report['transition_guard_exit_code']=result.returncode
    (OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Checked',len(pts),'frames; minimum join correlation',min(j['correlation'] for j in joins),
          '; transition guard',result.returncode,flush=True)


if __name__=='__main__':main()
