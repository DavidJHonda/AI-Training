#!/usr/bin/env python3
"""Targeted encoded-file checks for the three approved playlist changes."""
from pathlib import Path
import json
import re
import subprocess

import cv2
import numpy as np

from build_ai_is_different_v17 import ROOT,OUT,DEST,PREVIOUS_OUT,PREVIOUS
from editspec_build import readwav,sha,SPF


def main():
    m=json.loads((OUT/'edit-manifest.json').read_text())
    old=readwav(PREVIOUS_OUT/'edited.wav');new=readwav(OUT/'edited.wav')
    assert np.array_equal(new,np.r_[old[:5722*SPF],old[5973*SPF:]])
    assert len(new)==7824*SPF
    for p,digest in m['protected_hashes'].items():assert sha(p)==digest,p
    for key in ['rules','cooking']:
        a=json.loads((PREVIOUS_OUT/f'leg-{key}.json').read_text())
        b=json.loads((OUT/f'leg-{key}.json').read_text())
        assert sha(a.pop('image'))==sha(b.pop('image'));assert a==b
    oldm=json.loads((PREVIOUS_OUT/'edit-manifest.json').read_text())
    assert m['close']=={**oldm['close'],'start_frame':oldm['close']['start_frame']-251}
    cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
    for row in m['boundaries']:cmd+=['--boundary',f"{row['frame']}:{row['label']}"]
    subprocess.run(cmd,check=True)
    wanted=[5260,5261,5276,5455,5470,5721,5722,5737,5740,5755,5978,6515,6516,6531,7606,7607,7622,7823]
    folder=OUT/'encoded-frames';folder.mkdir(exist_ok=True)
    cap=cv2.VideoCapture(str(DEST));i=0;frames={}
    while True:
        ok,im=cap.read()
        if not ok:break
        if i in wanted:
            frames[i]=im.copy();cv2.imwrite(str(folder/f'{i:05d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,94])
        i+=1
    cap.release();assert i==7824
    tiles=[]
    for f in wanted:
        im=cv2.resize(frames[f],(426,240));cv2.rectangle(im,(0,0),(426,24),(250,245,250),-1)
        cv2.putText(im,f'{f/30:.3f}s f{f}',(8,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,0),1);tiles.append(im)
    cv2.imwrite(str(OUT/'playlist-repair-frames.jpg'),cv2.vconcat([cv2.hconcat(tiles[k:k+3]) for k in range(0,len(tiles),3)]))
    # Measure the new join on the encoded stream, not just the PCM assembly.
    import imageio_ffmpeg
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    r=subprocess.run([ff,'-hide_banner','-i',str(DEST),'-af','silencedetect=noise=-45dB:d=0.15','-f','null','-'],capture_output=True,text=True)
    assert r.returncode==0;(OUT/'silencedetect.txt').write_text(r.stderr)
    starts=re.findall(r'silence_start: ([\d.]+)',r.stderr)
    ends=re.findall(r'silence_end: ([\d.]+) \| silence_duration: ([\d.]+)',r.stderr)
    gaps=[{'start':float(s),'end':float(e),'duration':float(d)} for s,(e,d) in zip(starts,ends)]
    join=next(x for x in gaps if x['start']<5722/30<x['end'])
    subprocess.run([ff,'-v','error','-ss','172','-i',str(DEST),'-t','48','-c:v','libx264','-preset','fast','-crf','20','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/'playlist-review.mp4')],check=True)
    subprocess.run([ff,'-v','error','-ss','184','-i',str(DEST),'-t','14','-vn','-ac','1','-ar','16000',str(OUT/'join-check.wav')],check=True)
    from faster_whisper import WhisperModel
    class StableMel(np.ndarray):
        def __matmul__(self,x):return np.einsum('ij,jk->ik',np.asarray(self),x,optimize=False)
    model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
    model.feature_extractor.mel_filters=model.feature_extractor.mel_filters.view(StableMel)
    segs,_=model.transcribe(str(OUT/'join-check.wav'),beam_size=5)
    transcript=[{'start':s.start+184,'end':s.end+184,'text':s.text.strip()} for s in segs]
    (OUT/'join-transcript.json').write_text(json.dumps(transcript,indent=2))
    result={'candidate_sha256':sha(DEST),'frames':i,'duration':i/30,
      'audio_exactly_v16_minus_251_frame_song_list':True,'rules_cooking_specs_and_assets_unchanged':True,
      'close_unchanged_except_timeline_shift':True,'protected_sources_unchanged':True,
      'board_introduction':5261/30,'on_the_right':5740/30,'playlist_board_end':6516/30,
      'new_join_gap':join,'join_transcript':transcript,'listening':'Not performed; waveform, ASR and frame checks only.'}
    (OUT/'qa.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
