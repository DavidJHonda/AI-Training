#!/usr/bin/env python3
"""Inspect the encoded v16 candidate; reports do not certify listening."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import wave

import cv2
import numpy as np

from build_ai_is_different_v16 import OUT,DEST,ROOT
from editspec_build import readwav,SPF,sha


def transcribe():
    from faster_whisper import WhisperModel
    class StableMel(np.ndarray):
        def __matmul__(self,other):
            return np.einsum('ij,jk->ik',np.asarray(self),other,optimize=False)
    model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
    model.feature_extractor.mel_filters=model.feature_extractor.mel_filters.view(StableMel)
    segments,info=model.transcribe(str(DEST),beam_size=5,word_timestamps=True,vad_filter=True)
    rows=[];words=[]
    for seg in segments:
        rows.append({'start':seg.start,'end':seg.end,'text':seg.text.strip()})
        words.extend({'start':w.start,'end':w.end,'word':w.word.strip()} for w in seg.words or [])
    (OUT/'encoded-transcript.json').write_text(json.dumps({'source':str(DEST),'duration':info.duration,'segments':rows,'words':words},indent=2))
    (OUT/'encoded-transcript.txt').write_text('\n'.join(f"{r['start']:7.2f}-{r['end']:7.2f}  {r['text']}" for r in rows)+'\n')
    print(f'Encoded transcript: {len(words)} words',flush=True)


def verify():
    m=json.loads((OUT/'edit-manifest.json').read_text())
    assert sha(DEST)==m['render_sha256']
    for p,digest in m['protected_hashes'].items():assert sha(p)==digest,p
    audio=readwav(OUT/'edited.wav');assert len(audio)==m['total_frames']*SPF
    base=readwav(OUT/'source.wav')
    # Outside the three 5ms audio seam fades, unchanged base spans must be exact.
    assert np.array_equal(audio[:5722*SPF-240],base[:5722*SPF-240])
    assert np.array_equal(audio[5973*SPF+240:7858*SPF-240],base[5951*SPF+240:7836*SPF-240])
    bounds=m['boundaries']
    cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
    for b in bounds:cmd.extend(['--boundary',f"{b['frame']}:{b['label']}"])
    subprocess.run(cmd,check=True)
    wanted={0,m['total_frames']-1,*range(0,m['total_frames'],180)}
    for b in bounds:wanted.update([b['frame']-1,b['frame'],b['frame']+15])
    for board in m['boards'].values():
        wanted.add(board['src_in']+30)
        for state in board['states']:wanted.add(state['spoken_onset_source_frame']+15)
    # Denser sequences for retained animation, donor transitions, and closing move.
    for s,e in [(110,119),(129,136),(199,208),(225.5,238.4),(238.4,243.9),(253,261.9),(261.9,269.1)]:
        wanted.update(range(round(s*30),round(e*30),15))
    folder=OUT/'encoded-frames';folder.mkdir(exist_ok=True)
    cap=cv2.VideoCapture(str(DEST));assert cap.isOpened();fps=cap.get(cv2.CAP_PROP_FPS)
    cells=[];count=0;shape=None
    while True:
        ok,im=cap.read()
        if not ok:break
        shape=im.shape
        if count in wanted:
            cv2.imwrite(str(folder/f'{count:05d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,91])
        if count%180==0 or count==m['total_frames']-1:
            tile=cv2.resize(im,(426,240));cv2.rectangle(tile,(0,0),(426,24),(245,240,250),-1)
            cv2.putText(tile,f'{count/30:.2f}s  f{count}',(8,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(45,30,35),1)
            cells.append(tile)
        count+=1
    cap.release();assert count==m['total_frames'];assert shape==(720,1280,3);assert fps==30
    for s in range(0,len(cells),18):
        items=cells[s:s+18]
        while len(items)%3:items.append(np.full_like(items[0],255))
        sheet=cv2.vconcat([cv2.hconcat(items[i:i+3]) for i in range(0,len(items),3)])
        cv2.imwrite(str(OUT/f'encoded-sheet-{s//18}.jpg'),sheet)
    # Context strips show actual outgoing/destination frames at all splices.
    tiles=[]
    for b in bounds:
        for delta in [-1,0,15]:
            f=b['frame']+delta;im=cv2.imread(str(folder/f'{f:05d}.jpg'))
            tile=cv2.resize(im,(426,240));cv2.rectangle(tile,(0,0),(426,24),(245,240,250),-1)
            cv2.putText(tile,f'{f/30:.3f}s {delta:+d}f',(8,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(45,30,35),1)
            tiles.append(tile)
    for s in range(0,len(tiles),18):
        items=tiles[s:s+18]
        cv2.imwrite(str(OUT/f'boundary-summary-{s//18}.jpg'),cv2.vconcat([cv2.hconcat(items[i:i+3]) for i in range(0,len(items),3)]))
    board_runs=[]
    for row in m['timeline']:
        if row['visual'] not in m['boards']:continue
        if board_runs and board_runs[-1]['end_frame']==row['start_frame'] and board_runs[-1]['board']==row['visual']:
            board_runs[-1]['end_frame']=row['end_frame']
        else:board_runs.append({'board':row['visual'],'start_frame':row['start_frame'],'end_frame':row['end_frame']})
    for run in board_runs:run['seconds']=(run['end_frame']-run['start_frame'])/30
    checks={'candidate_sha256':sha(DEST),'decoded_frames':count,'duration':count/30,'fps':fps,
            'resolution':[shape[1],shape[0]],'edited_audio_samples':len(audio),'unchanged_base_pcm_exact':True,
            'protected_hashes_unchanged':True,'board_runs':board_runs,
            'longest_board_hold_seconds':max(x['seconds'] for x in board_runs),
            'listening':'Not performed; transcription and waveform checks only.'}
    (OUT/'qa.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--transcribe',action='store_true');a=p.parse_args()
    transcribe() if a.transcribe else verify()
