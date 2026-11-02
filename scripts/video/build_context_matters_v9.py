#!/usr/bin/env python3
"""Narrow Outside the Window replacement using the approved two-card board and take 2.
Corrects the v8 ring-width discrepancy. No installation. Preserves the installed source outside the identified replacement.
"""
from pathlib import Path
import hashlib,json,subprocess,sys,wave
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Build
import ken_burns_path as kb
from build_context_matters_v5 import exact_ring

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/context-matters-outside-replacement-2026-11-02/v9'
SRC=ROOT/'course-assets/context-matters/context-matters.mp4'
DONOR=ROOT/'Prompts/context-matters-2.mp4'
BOARD=ROOT/'course-assets/context-matters/context-matters-outside-the-window.jpg'
DEST=ROOT/'Prompts/context-matters-v9.mp4'
FF=imageio_ffmpeg.get_ffmpeg_exe(); FPS=30; SR=48000; SPF=1600
VIS_IN=5129; AUDIO_IN=5220; RESUME=6381; TOTAL=7461
D_IN=1367; D_OUT=2015; INSERT=D_OUT-D_IN
BOARD_N=AUDIO_IN-VIS_IN+INSERT; EXPECTED=TOTAL-(RESUME-AUDIO_IN)+INSERT
HASHES={SRC:'4405f5a30e8daddf2698b933f150171c58277d8be8cc8b57fa08c0c70f7cb967',DONOR:'a38e28754aa7756a6daa6ee3c692c441079cf8e44ab982b41f68935709216923',BOARD:'69f265a321912ee0b010bf1cf0c8daeed784791d6777371a98273b7d811cc887'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):subprocess.run(args,check=True,cwd=ROOT)
def pcm(src,filters=None):
 args=[FF,'-v','error','-i',str(src),'-vn','-ac','1','-ar',str(SR)]
 if filters:args+=['-af',filters]
 args+=['-f','f32le','-'];r=subprocess.run(args,stdout=subprocess.PIPE,check=True)
 return np.frombuffer(r.stdout,dtype='<f4').copy()
def main():
 if DEST.exists():raise SystemExit(f'Refusing to overwrite {DEST}')
 for p,h in HASHES.items():assert sha(p)==h,(p,'source changed')
 OUT.mkdir(exist_ok=True,parents=True)
 b=Build(ROOT,SRC,OUT,DEST,protected=[DONOR,BOARD])
 canvas,cw,ch,ox,oy=b.compose(BOARD,'outside')
 # A stationary compact view: the delivered body copy is about 21 source-rendered pixels.
 intro=AUDIO_IN-VIS_IN
 onsets=[45.90,54.14,63.38]
 ring_frames=[intro+round(t*FPS)-D_IN for t in onsets]
 rects=[[40,118,744,631],[816,118,744,631],[40,789,1520,88]]
 colors=['#0e8f86','#4f2fc4','#6e51ff']
 labels=['Files, Websites, and Other Apps','Earlier Conversations','Takeaway']
 rings=[]
 for i,(r,c,label) in enumerate(zip(rects,colors,labels)):
  rings.append(dict(start=ring_frames[i],end=ring_frames[i+1] if i<2 else BOARD_N,rect=[r[0]+ox,r[1]+oy,r[2],r[3]],color=c,pad=0,radius=14,label=label))
 spec={'image':str(canvas),'fps':30,'out_w':1280,'out_h':720,'upscale':2,'beats':[{'label':'full-board','frames':BOARD_N,'from':[cw/2,ch/2,float(cw)],'to':[cw/2,ch/2,float(cw)]}],'rings':rings}
 plan=OUT/'outside-plan.json';plan.write_text(json.dumps(spec,indent=2)+'\n')
 # The exact-width implementation already used by Context Matters v5 avoids
 # OpenCV's odd-width line rounding (nominal 4 px otherwise becomes 5 px).
 kb.draw_ring=exact_ring
 for args in [[str(plan),'--preview',str(OUT/'preview')],[str(plan),str(OUT/'leg-outside.mkv')]]:
  sys.argv=['ken_burns_path.py',*args];kb.main()
 base=pcm(SRC)[:TOTAL*SPF]
 # The donor is about 4 LU quieter than the surrounding source. Limit only this
 # inserted passage; preserve the installed source's audio elsewhere exactly in PCM.
 donor_filter=f'aresample={SR},atrim=start_sample={D_IN*SPF}:end_sample={D_OUT*SPF},asetpts=PTS-STARTPTS,volume=4dB,alimiter=limit=0.91201084:level=false:attack=5:release=50:latency=true,apad,atrim=end_sample={INSERT*SPF}'
 donor=pcm(DONOR,donor_filter);assert len(donor)==INSERT*SPF
 audio=np.concatenate([base[:AUDIO_IN*SPF],donor,base[RESUME*SPF:]])
 # Five-millisecond edge ramps confined to measured silence at both joins.
 fade=240
 for boundary in [AUDIO_IN*SPF,(AUDIO_IN+INSERT)*SPF]:
  audio[boundary-fade:boundary]*=np.linspace(1,0,fade,endpoint=False)
  audio[boundary:boundary+fade]*=np.linspace(0,1,fade,endpoint=False)
 assert len(audio)==EXPECTED*SPF
 assert np.array_equal(audio[:AUDIO_IN*SPF-fade],base[:AUDIO_IN*SPF-fade])
 assert np.array_equal(audio[(AUDIO_IN+INSERT)*SPF+fade:],base[RESUME*SPF+fade:])
 wav=OUT/'assembled.wav'
 with wave.open(str(wav),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(audio,-1,1)*32767).astype('<i2').tobytes())
 graph=f'[0:v]trim=start_frame=0:end_frame={VIS_IN},settb=1/30,setpts=N[v0];[1:v]trim=start_frame=0:end_frame={BOARD_N},settb=1/30,setpts=N[v1];[0:v]trim=start_frame={RESUME}:end_frame={TOTAL},settb=1/30,setpts=N[v2];[v0][v1][v2]concat=n=3:v=1:a=0,format=yuv420p[v]'
 run([FF,'-v','error','-y','-i',str(SRC),'-i',str(OUT/'leg-outside.mkv'),'-i',str(wav),'-filter_complex',graph,'-map','[v]','-map','2:a:0','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(DEST)])
 cap=cv2.VideoCapture(str(DEST));n=0
 while cap.read()[0]:n+=1
 cap.release();assert n==EXPECTED,(n,EXPECTED)
 for p,h in HASHES.items():assert sha(p)==h,(p,'modified unexpectedly')
 manifest={'scope':'narrow approved Outside the Window narration and board replacement','candidate':str(DEST.relative_to(ROOT)),'candidate_sha256':sha(DEST),'protected_sources':{str(p.relative_to(ROOT)):h for p,h in HASHES.items()},'source_visual_replace_frames':[VIS_IN,RESUME],'source_audio_replace_frames':[AUDIO_IN,RESUME],'donor_audio_frames':[D_IN,D_OUT],'donor_source':'Prompts/context-matters-2.mp4','output_board_frames':[VIS_IN,VIS_IN+BOARD_N],'output_audio_join_frames':[AUDIO_IN,AUDIO_IN+INSERT],'output_frames':n,'duration':n/FPS,'duration_change_seconds':(n-TOTAL)/FPS,'density':'compact','camera':'stationary full board; exact canonical asset on padded 16:9 canvas','ring_width_output_px':4,'ring_output_frames':[{**r,'start':r['start']+VIS_IN,'end':r['end']+VIS_IN} for r in rings],'donor_gain_db':4,'donor_peak_limiter_dbfs':-0.8,'join_ramp_ms':5,'added_pause_seconds':0,'natural_join_gaps_seconds':[0.575,0.4505],'unchanged_source_pcm_outside_joins':True,'listening':'Not auditioned by assistant; requires owner listening review at both voice joins. ASR and signal checks are not listening.','installed':False}
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(f'Built {DEST}: {n} frames, {n/FPS:.3f}s; protected sources unchanged.',flush=True)
if __name__=='__main__':main()
