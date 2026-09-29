#!/usr/bin/env python3
"""Validate v11's one audio cut, preserved visual treatment and immediate ring."""
import json,subprocess,wave,hashlib
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
from build_what_is_ai_v11 import ROOT,SRC,PREV,OUT,DEST,KEEP,SPF,SR
from editspec_build import Reader,sha
from build_embeddings_v7 import Renderer

def pcm(path):
    with wave.open(str(path)) as w:
        assert w.getframerate()==SR and w.getnchannels()==1
        return np.frombuffer(w.readframes(w.getnframes()),np.int16)

def main():
    m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(DEST)==m['candidate_sha256']
    source=pcm(OUT/'source-native.wav');source=np.pad(source,(0,max(0,5477*SPF-len(source))))[:5477*SPF]
    expected=np.concatenate([source[a*SPF:b*SPF] for a,b in KEEP]);actual=pcm(OUT/'edited.wav')
    assert np.array_equal(actual,expected)
    assert hashlib.sha256(actual.tobytes()).hexdigest()==m['audio_pcm_sha256']
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    result=subprocess.run([ff,'-v','error','-i',str(DEST),'-map','0:a:0','-c:a','pcm_s16le','-ar',str(SR),'-f','s16le','pipe:1'],capture_output=True,check=True)
    decoded=np.frombuffer(result.stdout,np.int16)[:len(expected)].astype(float)
    assert len(decoded)==len(expected)
    ref=expected.astype(float);snr=float(10*np.log10(np.sum(ref**2)/np.sum((decoded-ref)**2)))
    assert snr>30,snr
    (OUT/'encoded').mkdir(exist_ok=True)
    cap=cv2.VideoCapture(str(DEST));assert cap.get(cv2.CAP_PROP_FPS)==30
    prior=Reader(ROOT/'Prompts/what-is-ai-v10.mp4');wanted=set(m['preview_frames']);n=0;states=[];retained=[];cells=[]
    changed=lambda sf:1440<=sf<1451 or 4991<=sf<5051
    while True:
        ok,im=cap.read()
        if not ok:break
        assert im.shape==(720,1280,3)
        sf=m['source_frame_mapping'][n]
        if n in wanted:
            cv2.imwrite(str(OUT/'encoded'/f'{n:05d}.jpg'),im)
            prepared=cv2.imread(str(OUT/'preview'/f'{n:05d}.jpg'))
            mad=float(np.abs(im.astype(float)-prepared).mean());assert mad<5,(n,mad)
            states.append(dict(frame=n,mad=mad))
        if n%120==0:
            if not changed(sf):
                old=prior.at(sf);mad=float(np.abs(im.astype(float)-old).mean());assert mad<5,(n,mad)
                retained.append(dict(frame=n,source_frame=sf,mad=mad))
            small=cv2.resize(im,(480,270));cv2.rectangle(small,(0,0),(170,25),(255,255,255),-1)
            cv2.putText(small,f'{n/30:.2f}s / f{n}',(7,18),0,.5,(0,0,0),1);cells.append(small)
        n+=1
    cap.release();prior.c.release();assert n==m['frames']==4667
    for i in range(0,len(cells),12):
        group=cells[i:i+12]
        while len(group)%3:group.append(np.full_like(group[0],255))
        cv2.imwrite(str(OUT/f'encoded-sheet-{i//12}.jpg'),np.vstack([np.hstack(group[j:j+3]) for j in range(0,len(group),3)]))
    # Confirm the ring is on in the exact first returned frame, not merely later.
    spec=json.loads((OUT/'leg-picks-summary.json').read_text());assert spec['rings'][0]['start']==0
    r=Renderer(spec);ringed,base,geo=r.at(0);assert geo
    encoded=cv2.imread(str(OUT/'encoded/04181.jpg'))
    mask=np.max(np.abs(ringed.astype(int)-base.astype(int)),axis=2)>50
    ring_error=float(np.abs(encoded.astype(float)-ringed).mean(axis=2)[mask].mean())
    no_ring_error=float(np.abs(encoded.astype(float)-base).mean(axis=2)[mask].mean())
    assert ring_error<no_ring_error*.5,(ring_error,no_ring_error)
    args=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST)]
    for f in m['boundaries']:args+=['--boundary',f'{f}:edit']
    subprocess.run([*args,'--outdir',str(OUT/'guard')],check=True)
    sil=subprocess.run([ff,'-v','info','-i',str(DEST),'-af','silencedetect=noise=-38dB:d=0.08','-f','null','-'],capture_output=True,text=True,check=True)
    (OUT/'encoded-silences.txt').write_text(sil.stderr)
    assert all(sha(Path(path))==h for path,h in m['protected'].items())
    report=dict(candidate_sha256=sha(DEST),frames=n,fps=30,duration=n/30,cut_seconds=27,
        exact_preencode_pcm_cut=True,encoded_audio_snr_db=snr,prepared_states=len(states),
        retained_frames_checked=len(retained),max_retained_visual_mad=max(x['mad'] for x in retained),
        immediate_highlight_frame=4181,immediate_highlight_time=4181/30,
        first_frame_ring_error=ring_error,first_frame_unringed_error=no_ring_error,
        protected_unchanged=True,states=states,retained_visuals=retained,
        listening='Not directly auditioned; no listening pass is implied by PCM, silence, or transition checks.')
    (OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['states','retained_visuals']},indent=2))

if __name__=='__main__':main()
