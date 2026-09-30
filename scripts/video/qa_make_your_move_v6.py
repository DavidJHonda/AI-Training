#!/usr/bin/env python3
"""Inspect the actual encoded v6 candidate, including both changed audio joins."""
import json
import subprocess
from pathlib import Path

import av
import cv2
import numpy as np
from faster_whisper import WhisperModel

import build_make_your_move_v6 as b

def main():
    cv2.setNumThreads(2)
    out=b.OUT/'encoded-qa';out.mkdir(exist_ok=True)
    m=json.loads((b.OUT/'edit-manifest.json').read_text())
    wanted={0,m['total_frames']-1,749,750,751,853,854,855}
    for cfg in m['boards']:
        for s in cfg['states']:wanted.add(b.mapped(s['at'])+1)
    for p in m['cutaways']:
        a,z=p['output_span'];wanted.update([a,(a+z)//2,z-1,z])
    shots=[];pts=[];last=None
    with av.open(str(b.DEST)) as c:
        st=c.streams.video[0];st.codec_context.thread_count=2;rate=str(st.average_rate)
        for n,f in enumerate(c.decode(video=0)):
            pts.append(float(f.pts*f.time_base));last=f
            if n in wanted:
                im=f.to_ndarray(format='bgr24');cv2.imwrite(str(out/f'frame-{n:06d}.png'),im)
                tile=cv2.resize(im,(640,360));cv2.putText(tile,f'f{n} {n/30:.2f}s',(8,20),cv2.FONT_HERSHEY_SIMPLEX,.55,(0,0,220),1)
                shots.append(tile)
    for k in range(0,len(shots),8):
        group=shots[k:k+8]
        while len(group)%2:group.append(np.zeros_like(group[0]))
        cv2.imwrite(str(out/f'sheet-{k//8:02d}.jpg'),cv2.vconcat([cv2.hconcat(group[i:i+2]) for i in range(0,len(group),2)]))
    assert len(pts)==m['total_frames'] and rate=='30'
    assert all(abs(pts[i]-i/30)<.00001 for i in range(len(pts)))
    scan=subprocess.run([b.FF,'-hide_banner','-i',str(b.DEST),'-af',
        'silencedetect=noise=-40dB:d=0.15,ebur128=peak=true','-vf','blackdetect=d=0.1:pix_th=0.1','-f','null','-'],capture_output=True,text=True)
    (out/'technical-scan.txt').write_text(scan.stderr);assert scan.returncode==0
    raw=subprocess.check_output([b.FF,'-v','error','-i',str(b.DEST),'-f','f32le','-ar','48000','-ac','1','-'])
    a=np.frombuffer(raw,np.float32);expected=np.fromfile(b.OUT/'edited-audio.f32',np.float32)
    a=a[:len(expected)];assert len(a)==len(expected)
    corr=float(np.corrcoef(a,expected)[0,1]);snr=float(10*np.log10(np.sum(expected**2)/np.sum((a-expected)**2)))
    assert corr>.99 and np.max(abs(a))<1
    model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
    transcripts={}
    for name,start,end in [('opening-join',23,35),('teacher-graft',66,80),('close',280,294.166667)]:
        clip=out/(name+'.wav')
        subprocess.run([b.FF,'-v','error','-i',str(b.DEST),'-ss',str(start),'-t',str(end-start),'-ar','16000','-ac','1','-y',str(clip)],check=True)
        segs,_=model.transcribe(str(clip),language='en',word_timestamps=True)
        transcripts[name]=[dict(start=s.start+start,end=s.end+start,text=s.text) for s in segs]
        print(name,json.dumps(transcripts[name]),flush=True)
    text=' '.join(s['text'] for s in transcripts['teacher-graft']).lower()
    assert 'core responsibilities' in text and 'untouched' not in text and 'knowing' in text
    opening=' '.join(s['text'] for s in transcripts['opening-join']).lower()
    assert 'with them' in opening and 'when thinking' in opening and 'theory' not in opening
    close=' '.join(s['text'] for s in transcripts['close']).lower()
    assert 'smarter than the tool' in close and 'keep learning' in close and 'make your move' in close
    qa=dict(candidate_sha256=b.sha(b.DEST),decoded_frames=len(pts),fps=rate,continuous_timestamps=True,
            duration=len(pts)/30,decode_exit_code=scan.returncode,audio_sample_peak_dbfs=float(20*np.log10(np.max(abs(a)))),
            audio_samples_at_or_above_full_scale=int(np.sum(abs(a)>=1)),audio_to_planned_pcm_correlation=corr,
            audio_to_planned_pcm_snr_db=snr,transcripts=transcripts,
            black_detected='black_start:' in scan.stderr,listening='Not auditioned; transcript and signal checks only')
    (out/'verification.json').write_text(json.dumps(qa,indent=2)+'\n')
    print(json.dumps({k:v for k,v in qa.items() if k!='transcripts'},indent=2),flush=True)
    print(scan.stderr[-900:],flush=True)

if __name__=='__main__':main()
