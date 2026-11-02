#!/usr/bin/env python3
"""Verify encoded frames, preserved PCM, speech cuts and transition timing."""
from pathlib import Path
import json
import subprocess
import sys
import re
import av
import cv2
import imageio_ffmpeg
import numpy as np
import build_does_school_matter_v13 as b
from editspec_build import sha

def main():
    out=b.OUT; m=json.loads((out/'edit-manifest.json').read_text())
    v=b.Visuals();errors=[];times=[]
    sample={3013,3035,3307,3373,3460,3550,3600,3710,3900,b.TAKEAWAY,b.CLOSE,b.TOTAL-1}
    with av.open(str(b.DEST)) as c:
        assert c.streams.video[0].average_rate==30
        for n,f in enumerate(c.decode(video=0)):
            actual=f.to_ndarray(format='bgr24');expected=v.at(n)
            errors.append(float(np.abs(actual.astype(np.int16)-expected.astype(np.int16)).mean()))
            times.append(float(f.pts*f.time_base))
            if n in sample:cv2.imwrite(str(out/'preview'/f'encoded-{n:05d}.jpg'),actual)
    assert len(errors)==b.TOTAL and max(errors)<7
    assert np.max(np.abs(np.diff(times)-1/30))<1e-6
    actual=b.pcm(b.DEST);expected=b.pcm(out/'edited.wav');source=b.pcm(b.SOURCE)
    corr=float(np.corrcoef(actual[:len(expected)],expected)[0,1]);assert corr>.995
    assert np.array_equal(expected[:3373*1600-240],source[:3373*1600-240])
    assert np.array_equal(expected[b.TAIL*1600+240:],source[3835*1600+240:4251*1600])
    assert all(sha(Path(p))==h for p,h in m['protected'].items())
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    r=subprocess.run([ff,'-hide_banner','-i',str(b.DEST),'-vn','-af',
        'silencedetect=noise=-35dB:d=0.1','-f','null','-'],capture_output=True,text=True,check=True)
    (out/'encoded-silences.txt').write_text(r.stderr)
    starts=re.findall(r'silence_start: ([\d.]+)',r.stderr)
    ends=re.findall(r'silence_end: ([\d.]+) \| silence_duration: ([\d.]+)',r.stderr)
    gaps=[dict(start=float(s),end=float(e),duration=float(d)) for s,(e,d) in zip(starts,ends)]
    seams=[dict(frame=n,time=n/30,gap=next((g for g in gaps if g['start']<=n/30<=g['end']),None))
           for n in m['audio_seam_frames']]
    assert all(s['gap'] for s in seams)
    from faster_whisper import WhisperModel
    class StableMel(np.ndarray):
        def __matmul__(self,x):return np.einsum('ij,jk->ik',np.asarray(self),x,optimize=False)
    model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
    model.feature_extractor.mel_filters=model.feature_extractor.mel_filters.view(StableMel)
    # Transcribe encoded audio across the replacement and both external joins.
    audio=np.frombuffer(subprocess.check_output([ff,'-v','error','-ss','106','-i',str(b.DEST),
        '-vn','-ac','1','-ar','16000','-f','f32le','pipe:1']),np.float32)
    segs,_=model.transcribe(audio,beam_size=5,word_timestamps=True)
    transcript=[dict(start=s.start+106,end=s.end+106,text=s.text.strip()) for s in segs]
    (out/'replacement-transcript.json').write_text(json.dumps(transcript,indent=2)+'\n')
    (out/'replacement-transcript.txt').write_text('\n'.join(f"{s['start']:.2f}-{s['end']:.2f} {s['text']}" for s in transcript)+'\n')
    text=' '.join(s['text'] for s in transcript).lower()
    for phrase in ['thinking critically','question the claims you hear','weigh the available evidence','make informed decisions','school is where']:
        assert phrase in text,phrase
    for phrase in ['mechanical','basics are in place','baseline tools','evaluating reality']:
        assert phrase not in text,phrase
    assert text.count('school is where')==1
    report=dict(candidate_sha256=sha(b.DEST),frames=len(errors),duration=len(errors)/30,
        max_frame_MAE=max(errors),mean_frame_MAE=float(np.mean(errors)),continuous_pts=True,
        audio_correlation=corr,unchanged_body_and_tail_PCM=True,protected_sources_unchanged=True,
        audio_seams=seams,required_words_present=True,removed_phrases_absent=True,
        limitation='No direct listening; wording, waveform, frame and timing checks only.')
    (out/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    command=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(out/'transitions')]
    grouped={}
    for item in m['boundaries']:
        grouped.setdefault(item['frame'],[]).append(item['label'])
    for frame,labels in sorted(grouped.items()):
        command+=['--boundary',f"{frame}:{'+'.join(labels)}"]
    subprocess.run(command,check=True)

if __name__=='__main__':main()
