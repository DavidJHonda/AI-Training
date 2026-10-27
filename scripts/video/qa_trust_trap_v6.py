#!/usr/bin/env python3
"""Check actual encoded Trust Trap v6; no perceptual listening claim."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import wave

import av
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/trust-trap-build-v6-2026-10-27'
QA = OUT / 'qa'


def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576), b''):
            h.update(b)
    return h.hexdigest()


def main():
    m = json.loads((OUT/'edit-manifest.json').read_text())
    video = Path(m['candidate'])
    QA.mkdir(exist_ok=True)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [str(ROOT/'.video-venv/bin/python'), str(ROOT/'scripts/video/transition_guard.py'),
        str(video), '--outdir', str(QA/'transitions')]
    for b in m['boundaries']:
        cmd += ['--boundary', f"{b['frame']}:{b['label']}"]
    subprocess.run(cmd, check=True)
    print('Transition guard complete', flush=True)
    mapping = np.load(OUT/'picture-source-frames.npy')
    wanted = set(range(0, m['frames'], 120)) | {m['frames']-1, 0}
    for b in m['boundaries']:
        wanted.update([b['frame']-1,b['frame'],b['frame']+1])
    retime = m['diagram_retime']['output_frames']
    wanted.update(range(retime[0], retime[1]+1, 6))
    frames, pts = {}, []
    with av.open(str(video)) as container:
        for i, f in enumerate(container.decode(video=0)):
            pts.append(float(f.pts*f.time_base))
            if i in wanted:
                frames[i] = f.to_ndarray(format='bgr24')
    assert len(pts) == m['frames']
    delta = np.diff(pts)
    assert np.allclose(delta, 1/30, atol=1e-6)
    (QA/'frames').mkdir(exist_ok=True)
    for f in [0, m['frames']-1, 1493, 2679, 2988, retime[0], retime[1]]:
        if f not in frames:
            continue
        cv2.imwrite(str(QA/'frames'/f'frame-{f:05d}.jpg'), frames[f], [cv2.IMWRITE_JPEG_QUALITY, 96])
    overview = sorted(f for f in frames if f % 120 == 0 or f == m['frames']-1)
    sheets = []
    for start in range(0, len(overview), 16):
        subset = overview[start:start+16]
        im = Image.new('RGB',(1600,960),'white');d=ImageDraw.Draw(im)
        for i,n in enumerate(subset):
            tile=Image.fromarray(cv2.cvtColor(frames[n],cv2.COLOR_BGR2RGB)).resize((400,225))
            x,y=i%4*400,i//4*240;im.paste(tile,(x,y))
            d.text((x+5,y+226),f'{n/30:.2f}s / source {mapping[n]/30:.2f}s',fill='black')
        path=QA/f'overview-{start//16+1}.jpg';im.save(path,quality=94);sheets.append(str(path))
    ref = cv2.VideoCapture(m['source'])
    diffs=[]
    for n in overview:
        ref.set(cv2.CAP_PROP_POS_FRAMES,int(mapping[n]));ok,f=ref.read();assert ok
        diffs.append(dict(output_frame=n,source_frame=int(mapping[n]),
            mean_absolute_difference=float(np.mean(np.abs(f.astype(float)-frames[n].astype(float))))))
    ref.release()
    assert max(d['mean_absolute_difference'] for d in diffs)<5
    decoded=subprocess.check_output([ff,'-v','error','-i',str(video),'-vn','-ac','1','-ar','48000','-f','f32le','pipe:1'])
    actual=np.frombuffer(decoded,'<f4')
    with wave.open(str(OUT/'edited.wav'),'rb') as w:
        expected=np.frombuffer(w.readframes(w.getnframes()),'<i2')/32768
    actual=actual[:len(expected)];assert len(actual)==len(expected)
    corr=float(np.corrcoef(actual,expected)[0,1]);assert corr>.999
    silence=subprocess.run([ff,'-hide_banner','-i',str(video),'-af',
        'silencedetect=noise=-42dB:d=0.12','-f','null','-'],capture_output=True,text=True,check=True)
    lines=[l for l in silence.stderr.splitlines() if 'silence_' in l]
    (QA/'silences.txt').write_text('\n'.join(lines)+'\n')
    gaps=[];s=None
    for l in lines:
        match=re.search(r'silence_start: ([\d.]+)',l)
        if match:s=float(match.group(1))
        match=re.search(r'silence_end: ([\d.]+)',l)
        if match and s is not None:
            gaps.append([s,float(match.group(1))]);s=None
    join_gaps=[]
    for j in m['audio_joins']:
        t=j['seconds'];gap=next((g for g in gaps if g[0]<=t<=g[1]),None)
        assert gap is not None, (t,gaps)
        join_gaps.append(dict(join=t,quiet_interval=gap,duration=gap[1]-gap[0]))
    print('Frame, picture mapping, PCM and gap checks complete',flush=True)
    model=WhisperModel('base.en',device='cpu',compute_type='int8',local_files_only=True)
    segments,info=model.transcribe(str(video),beam_size=5,word_timestamps=True)
    rows=[dict(start=s.start,end=s.end,text=s.text.strip(),
        words=[dict(start=w.start,end=w.end,word=w.word) for w in s.words]) for s in segments]
    (QA/'transcript.json').write_text(json.dumps(rows,indent=2)+'\n')
    (QA/'transcript.txt').write_text('\n'.join(f"{r['start']:.2f}-{r['end']:.2f} {r['text']}" for r in rows)+'\n')
    text=' '.join(r['text'] for r in rows).lower()
    assert 'trust trap' in text, text
    assert 'mind trap' not in text
    for phrase in ['this graphic breaks down','no inner life','distinctly different action','prepare intensely']:
        assert phrase not in text,phrase
    for phrase in ['picking a college','eliza','personal context','picking a movie','checklists','trade-offs','real people','for decisions that matter','you make the call']:
        assert phrase in text,phrase
    # Focused clips are made from the encoded candidate, not the pre-encode plan.
    clips=[('word-repair',47,10),('graphic-introduction',joins_time(m,0)-2,5),
        ('inner-life-cut',joins_time(m,1)-2,5),('decision-diagram',retime[0]/30-3,11),
        ('ending',m['close']['output_frames'][0]/30-3,m['duration']-m['close']['output_frames'][0]/30+3)]
    for name,start,duration in clips:
        subprocess.run([ff,'-v','error','-ss',str(start),'-i',str(video),'-t',str(duration),
            '-c:v','libx264','-preset','fast','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',
            str(QA/(name+'.mp4'))],check=True)
    assert sha(video)==m['candidate_sha256']
    assert all(sha(p)==h for p,h in m['protected'].items())
    summary=dict(candidate=str(video),sha256=sha(video),frames=len(pts),duration=m['duration'],
        removed_seconds=m['removed_seconds'],pts_delta_range=[float(delta.min()),float(delta.max())],
        picture_comparisons=diffs,encoded_audio_correlation=corr,join_gaps=join_gaps,
        transcript_checks='PASS',source_hashes_unchanged=True,contact_sheets=sheets,
        user_approved_word_preview=True,perceptual_listening='Not performed by agent; fresh assembled joins supplied in focused clips.',
        visual_inspection='Pending manual review of saved frames and transition strips.')
    (QA/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['frames','duration','removed_seconds','encoded_audio_correlation','join_gaps','transcript_checks']},indent=2),flush=True)


def joins_time(m,index):
    return m['audio_joins'][index]['seconds']


if __name__=='__main__':
    main()
