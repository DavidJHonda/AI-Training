"""Verify encoded cut boundaries, frame mapping, retained audio, and transcript."""
import json
import subprocess
import sys

import av
import cv2
import imageio_ffmpeg
import numpy as np
from faster_whisper import WhisperModel

from build_fake_trap_v12 import OUT, ROOT, SOURCE, DEST, FPS, SR, SPF, N, CUTS, KEEPS, JOINS, sha


def main():
    qa = OUT/'qa'; qa.mkdir(exist_ok=True)
    m = json.loads((OUT/'manifest.json').read_text())
    mapping = np.concatenate([np.arange(a,b) for a,b in KEEPS])
    assert len(mapping) == 7295
    for a,b in CUTS:
        assert not np.any((mapping >= a) & (mapping < b))
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(qa/'transitions')]
    for f,label in zip(JOINS,['opening-to-principal','detector-to-emotions']):
        cmd += ['--boundary',f'{f}:{label}']
    subprocess.run(cmd,check=True)
    reference = np.empty((N,45,80,3),np.uint8)
    cap = cv2.VideoCapture(str(SOURCE))
    for n in range(N):
        ok,f = cap.read(); assert ok,n
        reference[n] = cv2.resize(f,(80,45),interpolation=cv2.INTER_AREA)
    cap.release()
    diffs,pts = [],[]
    with av.open(str(DEST)) as container:
        for i,frame in enumerate(container.decode(video=0)):
            assert (frame.width,frame.height) == (1280,720)
            pts.append(float(frame.pts*frame.time_base))
            small = cv2.resize(frame.to_ndarray(format='bgr24'),(80,45),interpolation=cv2.INTER_AREA)
            diff = float(np.abs(small.astype(np.int16)-reference[mapping[i]].astype(np.int16)).mean())
            diffs.append(diff); assert diff < 3,(i,diff)
    assert len(pts) == len(mapping) and np.allclose(np.diff(pts),1/FPS,atol=1e-6)
    assert np.array_equal(mapping[-274:],np.arange(N-274,N))
    print('All 7,295 frames, timestamps, and complete closing sequence verified.',flush=True)
    def decode(path):
        raw = subprocess.check_output([ff,'-v','error','-i',str(path),'-vn','-ar',str(SR),
            '-ac',str(m['channels']),'-f','f32le','pipe:1'])
        return np.frombuffer(raw,'<f4').reshape(-1,m['channels'])
    source = decode(SOURCE)
    expected = np.concatenate([source[a*SPF:b*SPF] for a,b in KEEPS])
    actual = decode(DEST)
    assert len(actual) >= len(expected)
    actual = actual[:len(expected)]
    corr = float(np.corrcoef(actual.reshape(-1),expected.reshape(-1))[0,1]); assert corr > .999
    mono = actual.mean(axis=1)
    step=480
    rms = np.sqrt(np.mean(mono[:len(mono)//step*step].reshape(-1,step)**2,axis=1))
    db = 20*np.log10(rms+1e-12)
    stats=[]
    for j in JOINS:
        s=j*SPF; k=s//step
        assert db[k] < -40,(j,db[k])
        lo,hi=k,k
        while lo>0 and db[lo-1]<-40:lo-=1
        while hi+1<len(db) and db[hi+1]<-40:hi+=1
        windows=[]
        for a,b in [(s-480,s),(s,s+480)]:
            windows.append(float(20*np.log10(np.sqrt(np.mean(actual[a:b]**2))+1e-12)))
        stats.append(dict(join_seconds=j/FPS,quiet_interval=[lo*.01,(hi+1)*.01],
            quiet_duration=(hi+1-lo)*.01,left_right_10ms_dbfs=windows,
            sample_jump=float(np.max(np.abs(actual[s]-actual[s-1])))))
    print('Encoded audio matches retained source; both splice points are quiet.',flush=True)
    clips=[]
    for j,name in zip(JOINS,['opening-join','detector-to-emotions-join']):
        clip=qa/f'{name}.mp4'
        subprocess.run([ff,'-y','-v','error','-ss',str(j/FPS-5),'-i',str(DEST),'-t','12',
            '-c:v','libx264','-crf','18','-preset','fast','-r','30','-c:a','aac','-b:a','192k',
            '-movflags','+faststart',str(clip)],check=True)
        clips.append(str(clip))
    model=WhisperModel('base.en',device='cpu',compute_type='int8',local_files_only=True)
    segments,_=model.transcribe(str(DEST),beam_size=5,word_timestamps=True)
    transcript=[dict(start=s.start,end=s.end,text=s.text.strip(),
        words=[dict(start=w.start,end=w.end,word=w.word) for w in s.words]) for s in segments]
    (qa/'transcript.json').write_text(json.dumps(transcript,indent=2)+'\n')
    (qa/'transcript.txt').write_text('\n'.join(f"{s['start']:.2f}-{s['end']:.2f} {s['text']}" for s in transcript)+'\n')
    words=' '.join(s['text'].lower() for s in transcript)
    for phrase in ['imagine how this plays out','to find the truth','shift your focus','your eyes still work','you did nothing wrong']:
        assert phrase not in words,phrase
    for phrase in ['different tools','independent investigation','fakes travel quickly','source','context','corroboration',
        'does not count as independent confirmation','sender does not control','unverified is your answer',
        'do not screenshot','seeing or hearing']:
        assert phrase in words,phrase
    assert words.count('check the source, not the pixels') == 1
    assert sha(DEST) == m['candidate_sha256']
    assert all(sha(p)==h for p,h in m['protected'].items())
    summary=dict(candidate=str(DEST),sha256=sha(DEST),decoded_frames=len(pts),fps=FPS,
        duration_seconds=len(pts)/FPS,removed_seconds=12,frames_compared=len(diffs),
        maximum_thumbnail_mae=max(diffs),complete_close_preserved=True,
        removed_board_frames_present=False,encoded_audio_correlation=corr,join_stats=stats,
        transcript_checks='PASS',protected_files_unchanged=True,review_clips=clips,
        visual_review='Boundary strips pending agent inspection.',
        perceptual_listening='Not performed; signal measurements and ASR do not certify audible cadence.')
    (qa/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__':
    main()
