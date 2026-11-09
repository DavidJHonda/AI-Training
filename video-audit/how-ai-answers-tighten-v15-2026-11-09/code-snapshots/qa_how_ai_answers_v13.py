#!/usr/bin/env python3
"""Inspect encoded v13 pictures, preserved spans, joins, timing and decoded PCM."""
import json, subprocess, sys, wave
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw
from build_how_ai_answers_v13 import OUT,DEST,BASE,FF,MAPPING,TOTAL,DEMO,ROOT,EXTRA_HOLDS
from editspec_build import sha

def sheet(files,path,columns=3,width=426):
    height=round(width*9/16);stride=height+28
    im=Image.new('RGB',(columns*width,((len(files)+columns-1)//columns)*stride),'white');d=ImageDraw.Draw(im)
    for n,p in enumerate(files):
        x=(n%columns)*width;y=(n//columns)*stride
        im.paste(Image.open(p).resize((width,height)),(x,y));d.text((x+8,y+height+5),p.stem,fill='black')
    im.save(path)

def main():
    cv2.setNumThreads(2)
    m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(DEST)==m['candidate_sha256']
    encoded=OUT/'encoded';encoded.mkdir(exist_ok=True)
    sample_paths={int(p.stem):p for p in (OUT/'expected').glob('*.png')}
    cap=cv2.VideoCapture(str(DEST));base=cv2.VideoCapture(str(BASE))
    assert cap.get(cv2.CAP_PROP_FPS)==30
    assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
    errors=[];detail_errors=[];retained=[];n=0;frames_by_n={};bgr_min_std=1e9
    for f in range(6448):
        ok,bi=base.read();assert ok
        if n==TOTAL or MAPPING[n]!=f:continue
        ok,im=cap.read();assert ok
        bgr_min_std=min(bgr_min_std,float(im.std()))
        if n in sample_paths:
            expected=cv2.imread(str(sample_paths[n]));mae=float(np.mean(cv2.absdiff(im,expected)))
            # The established BGR-to-YUV encode has a measured uniform
            # channel offset (new scene median [-4,-2,-3] on 0..255).
            # Bound both absolute difference and detail after that offset.
            diff=im.astype(float)-expected
            detail=float(np.abs(diff-np.median(diff,axis=(0,1))).mean())
            errors.append(mae);detail_errors.append(detail)
            assert mae<4 and detail<2.5,(n,mae,detail)
            cv2.imwrite(str(encoded/f'{n:05d}.png'),im);frames_by_n[n]=im
        if n%30==0 and not DEMO[0]<=f<DEMO[1] and not 1766<=f<2247 and not any(a<=f<b for a,b,_ in EXTRA_HOLDS):
            retained.append(float(np.mean(cv2.absdiff(im,bi))))
        n+=1
    assert n==TOTAL and not cap.read()[0]
    cap.release();base.release();assert max(retained)<3 and bgr_min_std>5
    decoded=np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(DEST),'-vn','-ar','48000','-ac','2','-f','f32le','pipe:1']),np.float32).reshape(-1,2)
    ref=np.fromfile(OUT/'assembled-audio.f32',np.float32).reshape(-1,2)
    decoded=decoded[:len(ref)];assert len(decoded)==len(ref)==TOTAL*1600
    corr=float(np.corrcoef(ref.ravel(),decoded.ravel())[0,1]);snr=float(10*np.log10(np.mean(ref**2)/np.mean((ref-decoded)**2)))
    assert corr>.999 and snr>25,(corr,snr)
    assert np.max(np.abs(decoded))<1
    context=OUT/'join-audio';context.mkdir(exist_ok=True)
    for i,j in enumerate(m['cuts']):
        t=j['output_seconds'];clip=decoded[max(0,round((t-3)*48000)):round((t+4)*48000)].mean(axis=1)
        with wave.open(str(context/f'join-{i+1}-{t:.3f}s.wav'),'wb') as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(48000);w.writeframes((clip*32767).astype('int16').tobytes())
    result=subprocess.run([FF,'-v','error','-i',str(DEST),'-f','null','-'],capture_output=True,text=True)
    assert result.returncode==0 and not result.stderr,result.stderr
    args=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'guard')]
    for f in m['boundaries']:args+=['--boundary',str(f)]
    subprocess.run(args,check=True)
    for p,h in m['protected'].items():assert sha(Path(p))==h,p
    key=[m['demo_output_frames'][0],*[e['output_frames'][-1] for e in m['scene_events']],TOTAL-1]
    sheet([encoded/f'{f:05d}.png' for f in key],OUT/'encoded-states.jpg',2,640)
    joins=[j['output_frame'] for j in m['cuts']]
    sheet([encoded/f'{f+o:05d}.png' for f in joins for o in (-1,0,25)],OUT/'encoded-joins.jpg')
    flights=[]
    for e in m['scene_events']:
        a,b=e['output_frames'][2:];flights.extend([encoded/f'{f:05d}.png' for f in (a,(a+b)//2,b)])
    sheet(flights,OUT/'encoded-flights.jpg')
    # Use a settled dog-name prediction as the review poster.
    poster=min(sample_paths,key=lambda k:abs(MAPPING[k]-4300))
    cv2.imwrite(str(OUT/'poster.jpg'),frames_by_n[poster])
    qa=dict(frames=TOTAL,fps=30,duration_seconds=TOTAL/30,full_av_decode='passed',
        expected_frame_samples=len(errors),max_expected_frame_mae=max(errors),max_detail_mae=max(detail_errors),
        retained_frame_samples=len(retained),max_retained_frame_mae=max(retained),
        minimum_frame_std=bgr_min_std,audio_correlation=corr,audio_snr_db=snr,
        protected_hashes='passed',listening_performed=False,continuous_playback_performed=False)
    (OUT/'qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa),flush=True)

if __name__=='__main__':main()
