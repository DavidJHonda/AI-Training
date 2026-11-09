#!/usr/bin/env python3
"""Technical checks for the exact v17 candidate; does not certify listening."""
from pathlib import Path
import json, subprocess,sys
import cv2,numpy as np,av,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/transformer-build-v17-2026-11-09';VIDEO=ROOT/'Prompts/transformer-v17.mp4'
m=json.loads((OUT/'edit-manifest.json').read_text());ff=imageio_ffmpeg.get_ffmpeg_exe();py=str(ROOT/'.video-venv/bin/python')
# Guard every audio assembly seam and every replacement/donor visual edge.
args=[py,str(ROOT/'scripts/video/transition_guard.py'),str(VIDEO),'--outdir',str(OUT/'transitions')]
for n in m['boundaries']:args+=['--boundary',f'{n}:declared-edge']
subprocess.run(args,check=True)
preview=OUT/'encoded';preview.mkdir(exist_ok=True);want={s['frame']:s for s in m['prepared_states']};actual=[];tiles=[];n=0;cap=cv2.VideoCapture(str(VIDEO));shape=None
for v in m['supporting_visuals']:
 for f in [v['start'],(v['start']+v['end'])//2,v['end']-1]:want.setdefault(f,dict(path=None,board=v['tag']))
want[m['frame_count']-1]=dict(path=None,board='final-close')
while True:
 ok,im=cap.read()
 if not ok:break
 shape=im.shape
 if n in want:
  s=want[n];p=preview/f'{n:05d}-{s["board"]}.jpg';cv2.imwrite(str(p),im)
  mae=float(np.abs(im.astype(float)-cv2.imread(s['path']).astype(float)).mean()) if s.get('path') else None
  actual.append(dict(frame=n,key=s['board'],mae_to_preencode_jpeg=mae,path=str(p)))
 if n%120==0 or n==m['frame_count']-1:
  tile=cv2.resize(im,(320,180));cv2.rectangle(tile,(0,0),(320,19),(255,255,255),-1);cv2.putText(tile,f'{n/30:.2f}s',(6,14),0,.4,(0,0,0),1);tiles.append(tile)
 last=im;n+=1
cap.release();assert n==m['frame_count'],(n,m['frame_count']);assert shape==(720,1280,3)
for i in range(0,len(tiles),20):
 batch=tiles[i:i+20];batch += [np.full_like(batch[0],255)]*(20-len(batch));cv2.imwrite(str(OUT/f'encoded-sheet-{i//20}.jpg'),cv2.vconcat([cv2.hconcat(batch[j:j+4]) for j in range(0,20,4)]))
# Independent standard close endpoint reconstruction from generated canonical canvas.
close=cv2.imread(str(OUT/'close.png'));h,w=close.shape[:2];ww=w/1.2;hh=ww*9/16
expected=cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
# Compare geometry as well as pixels. RGB-to-4:2:0 conversion in this encoder
# shifts near-white channels by 1-4 levels; both ffmpeg and OpenCV reproduce it.
last_mae=float(np.abs(last.astype(float)-expected.astype(float)).mean())
last_corr=float(np.corrcoef(last.ravel(),expected.ravel())[0,1])
assert last_mae<4 and last_corr>.998,(last_mae,last_corr)
errors=[s['mae_to_preencode_jpeg'] for s in actual if s['mae_to_preencode_jpeg'] is not None];assert max(errors)<4,max(errors)
# Speech waveform correlation catches timing/truncation, not cadence or voices.
def audio(p):return np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(p),'-vn','-ar','48000','-ac','1','-f','f32le','-']),np.float32)
a=audio(VIDEO);b=audio(OUT/'edited.wav');size=min(len(a),len(b));corr=float(np.corrcoef(a[:size],b[:size])[0,1]);assert corr>.995,corr;assert abs(len(a)-len(b))<2048
sil=subprocess.run([ff,'-v','info','-i',str(VIDEO),'-vn','-af','silencedetect=noise=-40dB:d=0.15','-f','null','-'],capture_output=True,text=True,check=True).stderr
(OUT/'silence-detection.txt').write_text('\n'.join(x for x in sil.splitlines() if 'silence_' in x)+'\n')
with av.open(str(VIDEO)) as c:streams=[dict(type=s.type,codec=s.codec_context.name,time_base=str(s.time_base),duration=s.duration,frames=s.frames) for s in c.streams]
from editspec_build import sha
assert sha(VIDEO)==m['candidate_sha256'];assert all(sha(Path(p))==h for p,h in m['protected'].items())
result=dict(decoded_frames=n,expected_frames=m['frame_count'],duration=n/30,streams=streams,prepared_state_count=len(errors),max_board_frame_mae=max(errors),final_close_mae=last_mae,audio_correlation=corr,audio_sample_count=len(a),planned_audio_samples=len(b),candidate_sha256=sha(VIDEO),protected_files_unchanged=True,direct_listening=False,encoded_states=actual)
(OUT/'technical-qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='encoded_states'},indent=2),flush=True)
