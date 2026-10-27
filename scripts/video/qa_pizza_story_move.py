#!/usr/bin/env python3
"""Decode review candidates and check timeline, retained frames and audio joins."""
import json, subprocess, sys
import av, cv2, numpy as np
from build_pizza_story_move import ROOT, OUT, FF, SR, SPF, sha, source, read_frame

def check(slug):
    work=OUT/slug
    m=json.loads((work/'edit-manifest.json').read_text())
    dest=m['candidate']; assert sha(dest)==m['sha256']
    for key,s in m['sources'].items(): assert sha(source(key))==s['sha256']
    wanted=set(range(0,m['frames'],120))|{m['frames']-1}
    for r in m['timeline']:
        a,b=r['output_frames']; wanted.update([a,min(a+15,b-1),b-1])
    samples=[]; pts=[]; captures={}; rowix=0
    (work/'frames').mkdir(exist_ok=True)
    with av.open(dest) as c:
        for i,f in enumerate(c.decode(video=0)):
            pts.append(float(f.pts*f.time_base))
            if i not in wanted: continue
            while i>=m['timeline'][rowix]['output_frames'][1]:rowix+=1
            r=m['timeline'][rowix]; key=r['source']
            if key not in captures: captures[key]=cv2.VideoCapture(str(source(key)))
            sf=r['source_frames'][0]+i-r['output_frames'][0]
            if r['clean_head'] is not None: sf=max(sf,r['clean_head'])
            expected=read_frame(captures[key],sf);actual=f.to_ndarray(format='bgr24')
            mse=float(np.mean((actual.astype(float)-expected.astype(float))**2))
            psnr=99 if mse==0 else 10*np.log10(255**2/mse)
            samples.append(dict(frame=i,source=key,source_frame=sf,psnr=float(psnr)))
            cv2.imwrite(str(work/'frames'/f'{i:05}.jpg'),actual)
    for c in captures.values():c.release()
    assert len(pts)==m['frames'],(len(pts),m['frames'])
    assert np.max(np.abs(np.diff(pts)-1/30))<1e-6
    assert min(x['psnr'] for x in samples)>32
    raw=subprocess.check_output([FF,'-v','error','-i',dest,'-vn','-ac','1','-ar',str(SR),'-f','f32le','-'])
    enc=np.frombuffer(raw,'<f4');master=np.fromfile(work/'edited.f32','<f4')
    assert len(master)==m['frames']*SPF and 0<=len(enc)-len(master)<2048
    enc=enc[:len(master)];snr=float(10*np.log10(np.sum(master**2)/np.sum((master-enc)**2)))
    assert snr>25
    joins=[]
    for j in m['boundaries']:
        k=j['frame']*SPF
        rms=float(20*np.log10(max(np.sqrt(np.mean(enc[k-480:k+480]**2)),1e-12)))
        assert rms<-45,(j,rms)
        joins.append(dict(**j,seconds=j['frame']/30,encoded_join_rms_dbfs=rms))
        start=max(0,j['frame']/30-4)
        subprocess.run([FF,'-v','error','-n','-ss',str(start),'-i',dest,'-t','8',
            '-c:v','libx264','-threads','2','-preset','fast','-crf','18','-c:a','aac',
            str(work/f'join-{j["frame"]}.mp4')],check=True)
    args=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),dest,'--outdir',str(work/'transitions')]
    for j in m['boundaries']:args+=['--boundary',f'{j["frame"]}:{j["label"]}']
    subprocess.run(args,check=True)
    q=dict(frames=len(pts),duration=m['frames']/30,frame_samples=samples,
           minimum_psnr=min(x['psnr'] for x in samples),audio_snr_db=snr,joins=joins,
           source_hashes_unchanged=True,subjective_listening_performed=False,
           continuous_playback_performed=False)
    (work/'qa.json').write_text(json.dumps(q,indent=2)+'\n')
    print(slug,len(pts),'frames; PSNR',q['minimum_psnr'],'audio SNR',snr,flush=True)

if __name__=='__main__':
    cv2.setNumThreads(2)
    for slug in ['hallucination','does-ai-think']:check(slug)
