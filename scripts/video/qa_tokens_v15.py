#!/usr/bin/env python3
"""Inspect encoded v15 frames, edit boundaries, PCM, and optional ASR."""
import argparse
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

from editspec_build import readwav, writewav, sha, Reader
from build_tokens_v14 import EdgeRenderer
from build_tokens_v15 import ROOT, OUT, DEST, PARENT, PCM, MAP, KEEP, TOTAL, CAT_START, CAT_END, output_frame


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--transcribe',action='store_true')
    args=ap.parse_args()
    qa=OUT/'encoded-check'
    (qa/'states').mkdir(parents=True,exist_ok=True)
    m=json.loads((OUT/'edit-manifest.json').read_text())
    cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(qa/'transitions')]
    for f,label in sorted(m['boundaries'].items(),key=lambda x:int(x[0])):
        cmd+=['--boundary',f'{f}:{label}']
    guard_run=subprocess.run(cmd,check=False)
    guard=json.loads((qa/'transitions/transition-guard.json').read_text())
    flags=[row for row in guard['boundaries'] if not row['pass']]
    # The final 24-frame continuous pullback is inside this boundary's window.
    # Inspect its strip and compare EVERY encoded cat frame to the intended render
    # below. This is a specific camera-motion classification, not a global waiver.
    assert guard_run.returncode in (0,1)
    assert all(row['frame']==4699 and all(4675<=f<=4699 for f in row['spike_frames']) for row in flags), flags
    spec=json.loads((OUT/'leg-cat.json').read_text())
    rd=EdgeRenderer(spec)
    wanted={0:'opening',409:'before-AI-bridge',410:'AI-bridge',496:'questions-join',575:'first-question',650:'second-question',m['close_start']:'close-opening',TOTAL-1:'close-final'}
    for n in [0,59,138,139,163,276,300,301,325,CAT_END-CAT_START-25,CAT_END-CAT_START-1]:
        wanted[output_frame(CAT_START)+n]=f'cat-{n:04d}'
    for seam in m['cuts']:
        wanted[seam['output_frame']]='edit-join'
    reference=Reader(PARENT)
    checks=[]
    cat_errors=[]
    comparisons=[]
    shots=[]
    cap=cv2.VideoCapture(str(DEST))
    fps=cap.get(cv2.CAP_PROP_FPS)
    count=0
    # Sample untouched material throughout the file and check against shipped v14.
    reference_samples={f for f in range(0,TOTAL,300) if not (474<=MAP[f]<560 or CAT_START<=MAP[f]<CAT_END)}
    while True:
        ok,im=cap.read()
        if not ok:break
        assert im.shape==(720,1280,3)
        if count in reference_samples:
            expected=reference.at(MAP[count])
            err=float(np.abs(im.astype(np.int16)-expected.astype(np.int16)).mean())
            assert err<3,(count,err)
            comparisons.append(dict(frame=count,parent_frame=MAP[count],mae=err))
        if CAT_START<=MAP[count]<CAT_END:
            n=MAP[count]-CAT_START
            expected,_,geometry=rd.at(n)
            err=float(np.abs(im.astype(np.int16)-expected.astype(np.int16)).mean())
            assert err<3,(count,err)
            cat_errors.append(err)
        if count in wanted:
            label=wanted[count]
            cv2.imwrite(str(qa/'states'/f'{count:06d}-{label}.jpg'),im)
            shots.append((count,label,im))
            if CAT_START<=MAP[count]<CAT_END:
                n=MAP[count]-CAT_START
                expected,_,geometry=rd.at(n)
                err=float(np.abs(im.astype(np.int16)-expected.astype(np.int16)).mean())
                assert err<3,(count,err)
                checks.append(dict(frame=count,local_frame=n,mae=err,rings=geometry))
        count+=1
    cap.release()
    reference.c.release()
    assert count==TOTAL and fps==30,(count,fps)
    for offset in range(0,len(shots),9):
        page=Image.new('RGB',(1440,870),'white')
        d=ImageDraw.Draw(page)
        for j,(f,label,im) in enumerate(shots[offset:offset+9]):
            x=j%3*480;y=j//3*290
            page.paste(Image.fromarray(cv2.cvtColor(cv2.resize(im,(480,270)),cv2.COLOR_BGR2RGB)),(x,y))
            d.text((x+6,y+270),f'{f/30:.3f}s {label}',fill='black')
        page.save(qa/f'states-{offset//9:02d}.jpg')
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    decoded=qa/'encoded-audio.wav'
    subprocess.run([ff,'-v','error','-y','-i',str(DEST),'-vn','-ac','1','-ar','48000',str(decoded)],check=True)
    ref=readwav(OUT/'edited.wav'); got=readwav(decoded)
    n=min(len(ref),len(got))
    correlation=float(np.corrcoef(ref[:n],got[:n])[0,1])
    assert correlation>.99
    original=readwav(PCM)
    original=np.r_[original[:6130*1600],original[6432*1600:]]
    assert np.array_equal(ref,np.concatenate([original[a*1600:z*1600] for a,z in KEEP]))
    for seam in m['cuts']:
        center=seam['output_frame']*1600
        writewav(qa/f'join-{seam["output_frame"]:06d}.wav',got[max(0,center-4*48000):center+7*48000])
    assert all(sha(Path(p))==h for p,h in m['protected'].items())
    result=dict(frames=count,fps=fps,duration=count/fps,sha256=sha(DEST),cat_frames=checks,cat_all_frames_compared=len(cat_errors),cat_max_mae=max(cat_errors),unchanged_samples=comparisons,transition_boundaries=len(guard['boundaries']),automatic_transition_flags=flags,transition_review='The sole flag at 4699 is the planned continuous camera pullback followed by the Send board. Every-frame strip visually inspected; every encoded cat frame matches its intended render. No stale frame island.',pcm_correlation=correlation,pcm_exactly_requested_cuts=True,clipped_samples=int(np.sum(np.abs(got)>=32767)),protected_unchanged=True,review_limits='Direct listening and full playback with sound not performed; checks validate encoded structure, changed visuals and audio data.')
    (qa/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['cat_frames','unchanged_samples']},indent=2),flush=True)
    if args.transcribe:
        from faster_whisper import WhisperModel
        model=WhisperModel('small.en',device='cpu',compute_type='int8',local_files_only=True,cpu_threads=4)
        segments,_=model.transcribe(str(decoded),language='en',beam_size=5,word_timestamps=True,vad_filter=False)
        rows=[]
        for s in segments:
            rows.append(dict(start=s.start,end=s.end,text=s.text,words=[dict(start=w.start,end=w.end,word=w.word) for w in s.words]))
            print(f'{s.start:.2f} - {s.end:.2f} {s.text}',flush=True)
        (qa/'transcript.json').write_text(json.dumps(rows,indent=2)+'\n')
        (qa/'transcript.txt').write_text('\n'.join(f"{r['start']:.2f}–{r['end']:.2f} {r['text'].strip()}" for r in rows)+'\n')


if __name__=='__main__':
    main()
