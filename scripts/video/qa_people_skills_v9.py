#!/usr/bin/env python3
"""Check the encoded v9 against its approved picture/audio assembly."""
import json, subprocess, sys, wave
import av, cv2, numpy as np
from imageio_ffmpeg import get_ffmpeg_exe
from build_people_skills_v9 import ROOT, OUT, DEST, Picture, sha, SR, SPF

def readwav(path):
    with wave.open(str(path)) as w:
        assert w.getnchannels() == 1 and w.getframerate() == SR
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)

def main():
    m=json.loads((OUT/'edit-manifest.json').read_text()); total=m['total_frames']
    assert sha(DEST)==m['render_sha256']
    assert all(sha(p)==h for p,h in m['protected_hashes'].items())
    folder=OUT/'encoded-frames';folder.mkdir(exist_ok=True)
    wanted=set(range(0,total,120))|{total-1}
    boundaries=m['declared_boundaries']
    for b in boundaries:
        wanted.update(f for f in [b['frame']-1,b['frame'],b['frame']+1,b['frame']+30] if 0<=f<total)
    # Include the last question frame so the frozen pause has its exact predecessor.
    for r in m['timeline']:
        if r['kind']=='room_tone':wanted.add(r['start_frame']-1)
    picture=Picture(m);ri=0;samples=[];pts=[]
    with av.open(str(DEST)) as container:
        stream=container.streams.video[0]
        for f,frame in enumerate(container.decode(stream)):
            pts.append(float(frame.pts*frame.time_base))
            if f not in wanted:continue
            while f>=m['timeline'][ri]['end_frame']:ri+=1
            row=m['timeline'][ri];expected=picture.draw(row,f)
            actual=frame.to_ndarray(format='bgr24')
            mse=np.mean((actual.astype(float)-expected.astype(float))**2)
            score=99 if not mse else float(10*np.log10(255**2/mse))
            samples.append(dict(frame=f,time=f/30,visual=row.get('visual',row['kind']),psnr=score))
            cv2.imwrite(str(folder/f'f{f:05d}.jpg'),actual,[cv2.IMWRITE_JPEG_QUALITY,94])
    assert len(pts)==total,(len(pts),total)
    cadence=float(np.max(np.abs(np.diff(pts)-1/30)));assert cadence<1e-6
    assert min(x['psnr'] for x in samples)>30
    subprocess.run([get_ffmpeg_exe(),'-v','error','-y','-i',str(DEST),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(OUT/'encoded.wav')],check=True)
    audio=readwav(OUT/'encoded.wav');master=readwav(OUT/'edited.wav')
    assert 0<=len(audio)-len(master)<2048
    audio=audio[:len(master)];snr=float(10*np.log10(np.sum(master**2)/np.sum((audio-master)**2)));assert snr>25
    joins=[]
    for r in m['timeline'][1:]:
        at=r['start_frame']*SPF;left=max(0,at-4*SR);right=min(len(audio),at+4*SR);h=480
        data=audio[left:right];rms=np.sqrt((data[:len(data)//h*h].reshape(-1,h)**2).mean(1))/32768
        quiet=20*np.log10(np.maximum(rms,1e-12))<-38;mid=int((at-left)/h);a=b=mid
        while a>0 and quiet[a-1]:a-=1
        while b<len(quiet) and quiet[b]:b+=1
        joins.append(dict(time=r['start_frame']/30,label=r['label'],quiet_gap_seconds=(b-a)/100,edge_delta=float(abs(audio[at]-audio[at-1]))))
    q=dict(candidate=str(DEST),sha256=sha(DEST),frames=len(pts),duration=total/30,fps=30,pts_max_error=cadence,
           sampled_frames=samples,min_psnr=min(x['psnr'] for x in samples),audio_master_snr_db=snr,
           audio_peak_dbfs=float(20*np.log10(np.max(abs(audio))/32768)),joins=joins,
           source_hashes_unchanged=True,direct_listening_performed=False,continuous_playback_performed=False)
    (OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n')
    cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
    for b in boundaries:
        if b['frame']>0 and b['frame']+12<total:cmd+=['--boundary',f"{b['frame']}:{b['label']}"]
    guard=subprocess.run(cmd)
    if guard.returncode:
        review_path=OUT/'manual-visual-review.json'
        review=json.loads(review_path.read_text()) if review_path.exists() else {}
        raw=json.loads((OUT/'transitions/transition-guard.json').read_text())
        failed={b['frame'] for b in raw['boundaries'] if not b['pass']}
        resolved={b['frame'] for b in review.get('resolved_flags',[])}
        assert review.get('candidate_sha256')==sha(DEST) and review.get('visual_transition_review_pass') and failed==resolved, 'Transition flags need visual review'
        print('Transition guard flags resolved by hash-matched visual review:',sorted(resolved))
    print(json.dumps({k:v for k,v in q.items() if k not in ['sampled_frames','joins']},indent=2))

if __name__=='__main__':
    cv2.setNumThreads(2)
    main()
