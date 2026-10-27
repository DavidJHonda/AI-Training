#!/usr/bin/env python3
"""Verify the encoded v15 recap cut and unchanged retained content."""
import json, subprocess, sys
from pathlib import Path
import cv2
import numpy as np
import build_support_trap_v15 as b

def main():
    m = json.loads((b.OUT/'v15-edit-manifest.json').read_text())
    qa = b.OUT/'v15-qa'
    qa.mkdir(exist_ok=True)
    cap = cv2.VideoCapture(str(b.DEST))
    source = cv2.VideoCapture(str(b.SOURCE))
    captures = {}
    wants = {0,8030,1720,1721,1722,1736,1740,1800,3378,3757}
    wants.update(range(0,8031,300))
    n = 0
    times = []
    while True:
        ok,im = cap.read()
        if not ok:
            break
        times.append(cap.get(cv2.CAP_PROP_POS_MSEC))
        if n in wants:
            captures[n] = im
        n += 1
    cap.release()
    assert n == 8031,n
    assert np.allclose(np.diff(times),1000/30,atol=.002)
    errors = []
    for f,im in captures.items():
        source_f = f if f < 1721 else f+128
        source.set(cv2.CAP_PROP_POS_FRAMES,source_f)
        ok,old = source.read()
        assert ok
        error = float(np.abs(old.astype(float)-im.astype(float)).mean())
        assert error < 3,(f,error)
        errors.append(dict(frame=f,source_frame=source_f,mean_absolute_error=error))
    source.release()
    cv2.imwrite(str(qa/'final-frame.jpg'),captures[8030])
    cells = []
    for f in [1720,1721,1722,1736,1740,1800]:
        im = cv2.resize(captures[f],(640,360))
        cv2.rectangle(im,(0,0),(640,30),(255,255,255),-1)
        cv2.putText(im,f'{f/30:.3f}s / frame {f}',(8,22),0,.65,(0,0,0),1)
        cells.append(im)
    cv2.imwrite(str(qa/'join-context.jpg'),np.vstack([np.hstack(cells[i:i+2]) for i in range(0,6,2)]))
    expected = np.fromfile(b.OUT/'v15-edited-audio.f32',dtype='<f4')
    original = b.pcm(b.SOURCE)
    plain = np.concatenate([original[a*b.SPF:z*b.SPF] for a,z in b.SPANS])
    seam = 1721*b.SPF
    assert np.array_equal(expected[:seam-240],plain[:seam-240])
    assert np.array_equal(expected[seam+240:],plain[seam+240:])
    encoded = b.pcm(b.DEST)
    assert abs(len(encoded)-len(expected)) <= 1024
    length = min(len(encoded),len(expected))
    corr = float(np.corrcoef(encoded[:length],expected[:length])[0,1])
    assert corr > .995,corr
    handles = []
    for f in [1721,1849]:
        x = original[f*b.SPF-240:f*b.SPF+240]
        handles.append(dict(frame=f,dbfs=float(20*np.log10(np.sqrt(np.mean(x*x))+1e-12))))
    assert all(x['dbfs'] < -45 for x in handles),handles
    command = [sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(qa/'transitions')]
    for row in m['boundaries']:
        command += ['--boundary',f'{row["frame"]}:{row["label"]}']
    subprocess.run(command,check=True)
    clip = qa/'join-review.wav'
    subprocess.run([b.FF,'-y','-v','error','-ss','53','-t','13','-i',str(b.DEST),
        '-vn','-ar','16000','-ac','1',str(clip)],check=True)
    from faster_whisper import WhisperModel
    model = WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
    segments,_ = model.transcribe(str(clip),language='en',beam_size=5,word_timestamps=True,vad_filter=False)
    transcript = [dict(start=s.start+53,end=s.end+53,text=s.text,
        words=[dict(start=w.start+53,end=w.end+53,word=w.word) for w in s.words]) for s in segments]
    (qa/'join-transcript.json').write_text(json.dumps(transcript,indent=2)+'\n')
    text = ' '.join(s['text'] for s in transcript).lower()
    assert 'kinder' in text and 'mistaking supportive words for support' in text,text
    assert 'alters your day' not in text and 'the other cannot act' not in text,text
    unchanged = all(b.sha(Path(p)) == h for p,h in m['protected_files'].items())
    assert unchanged
    results = dict(decoded_frames=n,duration=n/30,uniform_frame_timing=True,
        sampled_visual_comparisons=errors,retained_audio_identical_before_encoding_except_5ms_edges=True,
        encoded_audio_correlation=corr,quiet_handles=handles,protected_files_unchanged=unchanged,
        candidate_sha256=b.sha(b.DEST),join_transcript=transcript,
        listening='Not performed; narrow candidate requires perceptual listening at 0:57.37. No full-playback or shipping certification.')
    (qa/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:results[k] for k in ['decoded_frames','duration','encoded_audio_correlation','quiet_handles','protected_files_unchanged','join_transcript']},indent=2),flush=True)

if __name__ == '__main__':
    main()
