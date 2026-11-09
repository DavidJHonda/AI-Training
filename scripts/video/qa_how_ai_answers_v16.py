#!/usr/bin/env python3
"""Verify encoded cues, pause, retained picture and narration in v16."""
import json,subprocess,sys,wave
from pathlib import Path
import cv2,numpy as np
from build_how_ai_answers_v16 import OUT,DEST,SOURCE,ROOT,FF,TOTAL,PAUSE_AT,ADDED,CUES,source_frame,out_frame
from editspec_build import sha
from qa_how_ai_answers_v13 import sheet

def main():
    cv2.setNumThreads(2)
    m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(DEST)==m['candidate_sha256']
    expected={int(p.stem):p for p in (OUT/'expected').glob('*.png')};enc=OUT/'encoded';enc.mkdir(exist_ok=True)
    cap=cv2.VideoCapture(str(DEST));src=cv2.VideoCapture(str(SOURCE));n0=-1;old=None
    assert cap.get(cv2.CAP_PROP_FPS)==30
    errors=[];retained=[];minstd=1e9
    for n in range(TOTAL):
        ok,im=cap.read();assert ok,n
        s=source_frame(n)
        if s is not None:
            while n0<s:ok,old=src.read();assert ok;n0+=1
        if n in expected:
            ref=cv2.imread(str(expected[n]));mae=float(cv2.absdiff(im,ref).mean());errors.append(mae);assert mae<4,(n,mae)
            cv2.imwrite(str(enc/f'{n:05d}.png'),im)
        changed=s is None or 1657<=s<1684 or 2047<=s<PAUSE_AT or any(a<=s<b for a,b,_,_ in CUES)
        if not changed and n%45==0:
            mae=float(cv2.absdiff(im,old).mean());retained.append(mae);assert mae<2,(n,mae)
        minstd=min(minstd,float(cv2.resize(im,(160,90)).std()))
    assert not cap.read()[0];cap.release();src.release();assert minstd>5
    print('Frame and retained-picture checks passed',flush=True)
    decoded=np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(DEST),'-vn','-ar','48000','-ac','2','-f','f32le','pipe:1']),np.float32).reshape(-1,2)
    ref=np.fromfile(OUT/'assembled-audio.f32',np.float32).reshape(-1,2);decoded=decoded[:len(ref)]
    assert len(decoded)==TOTAL*1600
    corr=float(np.corrcoef(ref.ravel(),decoded.ravel())[0,1]);snr=float(10*np.log10(np.mean(ref**2)/np.mean((ref-decoded)**2)))
    assert corr>.999 and snr>25
    before=np.fromfile(ROOT/'video-audit/how-ai-answers-tighten-v15-2026-11-09/assembled-audio.f32',np.float32).reshape(-1,2)
    k=PAUSE_AT*1600;assert np.array_equal(before[:k],ref[:k]) and np.array_equal(before[k:],ref[k+ADDED*1600:])
    # Encoded local gap below -40dB, 10ms bins, surrounding the insertion.
    bins=np.sqrt(np.mean(decoded[:len(decoded)//480*480].reshape(-1,480,2)**2,axis=(1,2)))
    mid=round((PAUSE_AT/30+.3)*100);l=mid;r=mid
    while bins[l-1]<.01:l-=1
    while bins[r]<.01:r+=1
    gap=[l/100,r/100];assert .75<gap[1]-gap[0]<1.25,gap
    for label,a,b in [('pause-context',65,72),('first-choices',72,84),('name-choices',108,119)]:
        clip=decoded[round(a*48000):round(b*48000)].mean(axis=1)
        with wave.open(str(OUT/f'{label}.wav'),'wb') as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes((clip*32767).astype('int16').tobytes())
    check=subprocess.run([FF,'-v','error','-i',str(DEST),'-f','null','-'],capture_output=True,text=True)
    assert check.returncode==0 and not check.stderr
    args=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'guard')]
    for f in m['boundaries']:args+=['--boundary',str(f)]
    subprocess.run(args,check=True)
    cue_files=[enc/f'{out_frame((a+b)//2):05d}.png' for a,b,_,_ in CUES]
    sheet(cue_files,OUT/'encoded-choices.jpg',2,640)
    sheet([enc/f'{n:05d}.png' for n in [1680,2046,PAUSE_AT,PAUSE_AT+ADDED-1,PAUSE_AT+ADDED,out_frame(2055)]],OUT/'encoded-pause-banner.jpg',2,640)
    cv2.imwrite(str(OUT/'poster.jpg'),cv2.imread(str(cue_files[3])))
    assert all(sha(Path(p))==h for p,h in m['protected'].items())
    q=dict(frames=TOTAL,fps=30,duration_seconds=TOTAL/30,full_av_decode='passed',expected_frame_samples=len(errors),max_expected_mae=max(errors),
        retained_samples=len(retained),max_retained_mae=max(retained),audio_correlation=corr,audio_snr_db=snr,
        retained_pcm_identical=True,encoded_pause_below_minus40db=gap,pause_duration_seconds=gap[1]-gap[0],
        protected_hashes='passed',listening_performed=False,continuous_playback_performed=False)
    (OUT/'qa.json').write_text(json.dumps(q,indent=2));print(json.dumps(q),flush=True)

if __name__=='__main__':main()
