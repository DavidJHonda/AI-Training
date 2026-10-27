#!/usr/bin/env python3
"""Verify the encoded v15 frame mapping, audio edits, joins, and retained teaching."""
import json
import re
import subprocess
import sys
import wave

import av
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw
from faster_whisper import WhisperModel

from build_engagement_trap_v15 import OUT, ROOT, SOURCE, DEST, FPS, SR, SPF, N, sha


def main():
    qa = OUT/'qa'; qa.mkdir(exist_ok=True)
    m = json.loads((OUT/'edit-manifest.json').read_text())
    mapping = np.load(OUT/'picture-source-frames.npy')
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(qa/'transitions')]
    for b in m['boundaries']:
        cmd += ['--boundary',f"{b['frame']}:{b['label']}"]
    subprocess.run(cmd,check=True)
    reference = np.empty((N,45,80,3),dtype=np.uint8)
    cap = cv2.VideoCapture(str(SOURCE))
    for n in range(N):
        ok,f = cap.read(); assert ok,n
        reference[n] = cv2.resize(f,(80,45),interpolation=cv2.INTER_AREA)
        if n == N-1:
            final_source = f.copy()
    cap.release()
    lo,hi = m['replacement_animation']['output_frames']
    wanted = set(range(0,len(mapping),120)) | set(range(lo,hi,15)) | {len(mapping)-1,lo,hi-1,hi}
    for b in m['boundaries']:
        wanted.update([b['frame']-1,b['frame'],b['frame']+1])
    frames, pts, differences = {},[],[]
    with av.open(str(DEST)) as container:
        for i,frame in enumerate(container.decode(video=0)):
            assert (frame.width,frame.height)==(1280,720)
            pts.append(float(frame.pts*frame.time_base))
            f = frame.to_ndarray(format='bgr24')
            small = cv2.resize(f,(80,45),interpolation=cv2.INTER_AREA)
            difference = float(np.abs(small.astype(np.int16)-reference[mapping[i]].astype(np.int16)).mean())
            differences.append(difference)
            assert difference<3,(i,difference)
            if i in wanted:
                frames[i]=f.copy()
    assert len(pts)==7148 and np.allclose(np.diff(pts),1/FPS,atol=1e-6)
    final_mae=float(np.abs(frames[7147].astype(float)-final_source.astype(float)).mean())
    assert final_mae<3
    assert not np.any((mapping>=4368)&(mapping<4755))
    print('Full decode and all 7,148 picture mappings verified.',flush=True)
    def sheets(name,indices):
        paths=[]
        for offset in range(0,len(indices),16):
            im=Image.new('RGB',(1600,960),'white'); d=ImageDraw.Draw(im)
            for k,n in enumerate(indices[offset:offset+16]):
                tile=Image.fromarray(cv2.cvtColor(frames[n],cv2.COLOR_BGR2RGB)).resize((400,225))
                x,y=k%4*400,k//4*240; im.paste(tile,(x,y))
                d.text((x+6,y+227),f'{n/FPS:.2f}s / frame {n} / source {mapping[n]}',fill='black')
            path=qa/f'{name}-{offset//16+1}.jpg';im.save(path,quality=95);paths.append(str(path))
        return paths
    overview=sheets('overview',sorted(n for n in frames if n%120==0 or n==7147))
    animation=sheets('animation',sorted(n for n in frames if lo<=n<hi))
    cv2.imwrite(str(qa/'final-frame.jpg'),frames[7147])
    raw=subprocess.check_output([ff,'-v','error','-i',str(DEST),'-vn','-ac','1','-ar',str(SR),'-f','f32le','pipe:1'])
    actual=np.frombuffer(raw,'<f4')
    with wave.open(str(OUT/'edited.wav'),'rb') as w:
        expected=np.frombuffer(w.readframes(w.getnframes()),'<i2')/32768
    assert len(expected)==7148*SPF and len(actual)>=len(expected)
    corr=float(np.corrcoef(actual[:len(expected)],expected)[0,1]); assert corr>.999
    result=subprocess.run([ff,'-hide_banner','-i',str(DEST),'-af','silencedetect=noise=-38dB:d=0.08',
        '-vn','-f','null','-'],capture_output=True,text=True,check=True)
    (qa/'silences.txt').write_text(result.stderr)
    gaps=[(float(a),float(b)) for a,b in re.findall(r'silence_start: ([\d.]+).*?silence_end: ([\d.]+)',result.stderr,re.S)]
    join_gaps=[]
    for j in m['audio_joins']:
        t=j['seconds']; gap=next((g for g in gaps if g[0]<=t<=g[1]),None)
        assert gap is not None,(t,gaps)
        join_gaps.append(dict(join=t,quiet_interval=gap,duration=gap[1]-gap[0]))
    print('Encoded audio correlation and both quiet joins verified.',flush=True)
    model=WhisperModel('base.en',device='cpu',compute_type='int8',local_files_only=True)
    segments,_=model.transcribe(str(DEST),beam_size=5,word_timestamps=True)
    transcript=[dict(start=s.start,end=s.end,text=s.text.strip(),
        words=[dict(start=w.start,end=w.end,word=w.word) for w in s.words]) for s in segments]
    (qa/'transcript.json').write_text(json.dumps(transcript,indent=2)+'\n')
    (qa/'transcript.txt').write_text('\n'.join(f"{s['start']:.2f}-{s['end']:.2f} {s['text']}" for s in transcript)+'\n')
    text=' '.join(s['text'].lower() for s in transcript).replace('-',' ')
    for phrase in ['you ask an ai a quick question','successfully using ai requires','recognizing the exact moment','you are finished, but the reply']:
        assert phrase not in text,phrase
    for phrase in ['this extra help may be useful','missing page break','conversation continues','follow up task','engineered outcome','know what you came for','choose what happens next']:
        assert phrase in text,phrase
    clips=[]
    for name,start,duration in [('opening-join',1.5,9),('retained-ai-bridge-and-join',lo/FPS-2,16)]:
        path=qa/f'{name}.mp4'
        subprocess.run([ff,'-y','-v','error','-ss',str(start),'-i',str(DEST),'-t',str(duration),
            '-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',str(path)],check=True)
        clips.append(str(path))
    assert sha(DEST)==m['candidate_sha256']
    assert all(sha(p)==h for p,h in m['protected'].items())
    summary=dict(candidate=str(DEST),sha256=sha(DEST),decoded_frames=len(pts),fps=FPS,
        duration=len(pts)/FPS,removed_seconds=22.8,picture_frames_compared=len(differences),
        maximum_thumbnail_mae=max(differences),final_frame_mae=final_mae,
        deleted_illustration_frames_present=False,encoded_audio_correlation=corr,
        join_gaps=join_gaps,transcript_checks='PASS',protected_files_unchanged=True,
        overview_sheets=overview,animation_sheets=animation,review_clips=clips,
        manual_visual_review='Pending inspection of sheets and boundary strips.',
        perceptual_listening='Not performed by agent; supplied encoded review clips for owner audition.')
    (qa/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['decoded_frames','duration','maximum_thumbnail_mae','encoded_audio_correlation','join_gaps','transcript_checks']},indent=2),flush=True)


if __name__=='__main__':
    main()
