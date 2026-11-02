#!/usr/bin/env python3
import json,subprocess,wave
from pathlib import Path
import cv2,numpy as np
from faster_whisper import WhisperModel
from repair_flattery_trap_v17 import OUT,SRC,DEST,FF,SR,stream_hash

def decode(p):return np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-ac','1','-ar',str(SR),'-f','f32le','-']),'<f4')
def main():
 old=decode(SRC);new=decode(DEST)
 with wave.open(str(OUT/'edited.wav'),'rb') as w:planned=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(float)/32768
 corr=float(np.corrcoef(new[:len(planned)],planned)[0,1]);assert corr>.998
 i,j=round(232.699*SR),round(232.704*SR)
 before=float(abs(np.diff(old[i:j])).max());after=float(abs(np.diff(new[i:j])).max());assert after<before*.2,(before,after)
 cap=cv2.VideoCapture(str(DEST));frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));fps=cap.get(cv2.CAP_PROP_FPS);cap.release();assert frames==7264 and fps==30
 assert stream_hash(SRC)==stream_hash(DEST)
 tail=OUT/'verified-ending.wav';subprocess.run([FF,'-v','error','-ss','227','-i',str(DEST),'-t','12','-vn','-ac','1','-ar','16000',str(tail)],check=True)
 model=WhisperModel('base.en',device='cpu',compute_type='int8',local_files_only=True,cpu_threads=4);segs,_=model.transcribe(str(tail),beam_size=5)
 rows=[dict(start=s.start+227,end=s.end+227,text=s.text.strip()) for s in segs];text=' '.join(s['text'] for s in rows).lower()
 for phrase in ['useful feedback points to the work','look for specifics','not approval']:assert phrase in text,phrase
 (OUT/'ending-transcript.json').write_text(json.dumps(rows,indent=2)+'\n')
 q=dict(candidate=str(DEST),video_packets_identical=True,frames=frames,fps=fps,duration_seconds=frames/fps,encoded_audio_correlation=corr,encoded_attack_jump_before=before,encoded_attack_jump_after=after,encoded_attack_reduction_db=float(20*np.log10(after/before)),both_closing_lines_verified=True,one_second_pause_and_picture_unchanged=True,perceptual_listening=False,installed=False)
 (OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
if __name__=='__main__':main()
