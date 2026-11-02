#!/usr/bin/env python3
"""Verify encoded frames, audio joins and narration for the five approved cuts."""
import json
import subprocess
import sys

import av
import cv2
import numpy as np
from PIL import Image, ImageDraw
from faster_whisper import WhisperModel

from build_support_trap_v16 import ROOT, OUT, SOURCE, DEST, SHA, SPANS, FRAMES, FPS, SPF, FF, sha, pcm


def main():
    qa = OUT/'qa'
    qa.mkdir(exist_ok=True)
    m = json.loads((OUT/'edit-manifest.json').read_text())
    assert sha(SOURCE) == SHA and sha(DEST) == m['candidate_sha256']
    command = [sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),
        '--outdir',str(qa/'transitions')]
    for b in m['boundaries']:
        command += ['--boundary',f"{b['frame']}:{b['label']}"]
    subprocess.run(command,check=True)
    cap = cv2.VideoCapture(str(SOURCE))
    refs = []
    while True:
        ok, im = cap.read()
        if not ok:
            break
        refs.append(cv2.resize(im,(80,45),interpolation=cv2.INTER_AREA))
    cap.release()
    source_frames = [f for a,b in SPANS for f in range(a,b)]
    wanted = set(range(0,FRAMES,300)) | {FRAMES-1}
    for b in m['audio_joins']:
        wanted.update([b['frame']-1,b['frame'],b['frame']+15])
    frames, pts, errors = {}, [], []
    with av.open(str(DEST)) as container:
        for n, frame in enumerate(container.decode(video=0)):
            assert (frame.width,frame.height) == (1280,720)
            pts.append(float(frame.pts*frame.time_base))
            im = frame.to_ndarray(format='bgr24')
            sf = source_frames[n]
            if 1832 <= sf < 1839:
                sf = 1831
            if 5359 <= sf < 5366:
                sf = 5203
            small = cv2.resize(im,(80,45),interpolation=cv2.INTER_AREA)
            error = float(np.abs(small.astype(float)-refs[sf].astype(float)).mean())
            assert error < 3.5, (n,sf,error)
            errors.append(error)
            if n in wanted:
                frames[n] = im.copy()
    assert len(pts) == FRAMES and np.allclose(np.diff(pts),1/FPS,atol=1e-6)
    print('All frame mappings and presentation times verified.',flush=True)
    images = []
    for offset in range(0,len(frames),12):
        sheet = Image.new('RGB',(1280,1020),'white')
        draw = ImageDraw.Draw(sheet)
        for i,n in enumerate(sorted(frames)[offset:offset+12]):
            x,y = i%3*426, i//3*255
            tile = Image.fromarray(cv2.cvtColor(frames[n],cv2.COLOR_BGR2RGB)).resize((426,240))
            sheet.paste(tile,(x,y+15))
            draw.text((x+4,y),f'{n//1800}:{n/30%60:05.2f} / frame {n}',fill='black')
        path = qa/f'overview-{offset//12+1}.jpg'
        sheet.save(path,quality=94)
        images.append(str(path))
    cv2.imwrite(str(qa/'final-frame.jpg'),frames[FRAMES-1])
    join_sheet = Image.new('RGB',(1280,1275),'white')
    draw = ImageDraw.Draw(join_sheet)
    for i,b in enumerate(m['audio_joins']):
        for j,n in enumerate([b['frame']-1,b['frame'],b['frame']+15]):
            tile=Image.fromarray(cv2.cvtColor(frames[n],cv2.COLOR_BGR2RGB)).resize((426,240))
            join_sheet.paste(tile,(j*426,i*255+15))
            draw.text((j*426+4,i*255),f"Join {i+1} / {n/30:.3f}s",fill='black')
    join_sheet.save(qa/'joins.jpg',quality=94)
    original = pcm(SOURCE)
    expected = np.fromfile(OUT/'edited-audio.f32',dtype='<f4')
    plain = np.concatenate([original[a*SPF:b*SPF] for a,b in SPANS])
    assert len(expected) == FRAMES*SPF
    mask = np.ones(len(expected),dtype=bool)
    for b in m['audio_joins']:
        n=b['frame']*SPF
        mask[n-240:n+240]=False
    assert np.array_equal(expected[mask],plain[mask])
    encoded = pcm(DEST)
    assert abs(len(encoded)-len(expected)) <= 1024
    length = min(len(encoded),len(expected))
    corr = float(np.corrcoef(encoded[:length],expected[:length])[0,1])
    assert corr > .999
    # Locate the encoded quiet region containing each edit, in 10 ms windows.
    block = 480
    rms = np.sqrt(np.mean(encoded[:len(encoded)//block*block].reshape(-1,block)**2,axis=1))
    quiet = 20*np.log10(rms+1e-12) < -38
    joins = []
    for b in m['audio_joins']:
        k=int(b['seconds']*100)
        assert quiet[k], (b,rms[k])
        a=z=k
        while a>0 and quiet[a-1]: a-=1
        while z+1<len(quiet) and quiet[z+1]: z+=1
        joins.append(dict(seconds=b['seconds'],quiet_start=a/100,quiet_end=(z+1)/100,
            quiet_duration=(z+1-a)/100))
    print('Retained audio and encoded quiet joins verified.',flush=True)
    model=WhisperModel('base.en',device='cpu',compute_type='int8',local_files_only=True)
    segments,_=model.transcribe(str(DEST),language='en',beam_size=5,word_timestamps=True)
    rows=[dict(start=s.start,end=s.end,text=s.text.strip(),
        words=[dict(start=w.start,end=w.end,word=w.word) for w in s.words]) for s in segments]
    (qa/'transcript.json').write_text(json.dumps(rows,indent=2)+'\n')
    (qa/'transcript.txt').write_text('\n'.join(f"{s['start']:.2f}-{s['end']:.2f} {s['text']}" for s in rows)+'\n')
    text=' '.join(s['text'].lower() for s in rows)
    retained=['mistaking supportive words for support','the rule','prepare for people',
        'ordinary venting','preparation','the next story discusses suicide',
        'it could not alert her family','it could not contact her therapist',
        'this is a protocol chart','step one','step two','step three',
        'safety always outranks secrecy','get ready for people']
    normalized=text.replace('step 1','step one').replace('step 2','step two').replace('step 3','step three')
    for phrase in retained:
        assert phrase in normalized,phrase
    removed=['what is ai actually good for','what is permanently missing',
        'polishing a text message','lacking any real','carries zero real',
        'the protocol comes down','your very next move']
    for phrase in removed:
        assert phrase not in normalized,phrase
    assert all(sha(p)==h for p,h in m['protected'].items())
    result=dict(candidate=str(DEST),candidate_sha256=sha(DEST),frames=FRAMES,
        duration_seconds=FRAMES/FPS,saved_seconds=m['saved_seconds'],
        all_frame_mappings_verified=True,maximum_thumbnail_mae=max(errors),
        uniform_frame_timing=True,retained_audio_identical_except_5ms_fades=True,
        encoded_audio_correlation=corr,joins=joins,
        retained_narration_checks=retained,removed_narration_checks=removed,
        safety_board_transition_retained=True,protected_files_unchanged=True,
        overview_sheets=images,visual_inspection='Pending',
        perceptual_listening=False,continuous_playback=False,
        status='Review candidate only; not installed or published.')
    (qa/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    main()
