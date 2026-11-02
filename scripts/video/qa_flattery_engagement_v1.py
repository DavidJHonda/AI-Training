#!/usr/bin/env python3
"""Check the actual merged candidate, not only its planned edit map."""
import json,re,subprocess,sys
from pathlib import Path
import av,cv2,numpy as np
from PIL import Image,ImageDraw
from faster_whisper import WhisperModel
from build_flattery_engagement_v1 import ROOT,OUT,DEST,SOURCES,FPS,SR,SPF,sha,close_frame

def main():
 qa=OUT/'qa';qa.mkdir(exist_ok=True)
 m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(DEST)==m['candidate_sha256']
 import imageio_ffmpeg
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(qa/'transitions')]
 for b in m['boundaries']:cmd+=['--boundary',f"{b['frame']}:{b['label']}"]
 subprocess.run(cmd,check=True)
 refs={}
 for key,(path,expected) in SOURCES.items():
  assert sha(path)==expected
  cap=cv2.VideoCapture(str(path));frames=[]
  while True:
   ok,f=cap.read()
   if not ok:break
   frames.append(cv2.resize(f,(80,45),interpolation=cv2.INTER_AREA))
  cap.release();refs[key]=np.stack(frames)
 close_start=m['close']['start_frame'];canvas=cv2.imread(str(OUT/'canvas-close.png'))
 frames={};pts=[];diff=[]
 wanted=set(range(0,m['frames'],300))|{m['frames']-1,close_start,close_start+48,close_start+198}
 for b in m['boundaries']:wanted.update(range(b['frame']-1,b['frame']+2))
 with av.open(str(DEST)) as c:
  for n,frame in enumerate(c.decode(video=0)):
   assert (frame.width,frame.height)==(1280,720)
   pts.append(float(frame.pts*frame.time_base));f=frame.to_ndarray(format='bgr24')
   small=cv2.resize(f,(80,45),interpolation=cv2.INTER_AREA)
   if n<close_start:
    seg=next(s for s in m['segments'][:3] if s['output_frames'][0]<=n<s['output_frames'][1])
    sf=seg['source_frames'][0]+n-seg['output_frames'][0]
    if 10561<=n<10563:sf=3766
    expected=refs[seg['source']][sf]
   else:expected=cv2.resize(close_frame(canvas,n-close_start),(80,45),interpolation=cv2.INTER_AREA)
   mae=float(np.abs(small.astype(float)-expected.astype(float)).mean());diff.append(mae)
   assert mae<3.5,(n,mae)
   if n in wanted:frames[n]=f.copy()
 assert len(pts)==m['frames'] and np.allclose(np.diff(pts),1/FPS,atol=1e-6)
 print('All frames, presentation times, and source mappings verified.',flush=True)
 paths=[]
 for offset in range(0,len(frames),16):
  sheet=Image.new('RGB',(1600,960),'white');draw=ImageDraw.Draw(sheet)
  for k,n in enumerate(sorted(frames)[offset:offset+16]):
   tile=Image.fromarray(cv2.cvtColor(frames[n],cv2.COLOR_BGR2RGB)).resize((400,225))
   x=k%4*400;y=k//4*240;sheet.paste(tile,(x,y));draw.text((x+5,y+227),f'{n//1800}:{n/30%60:05.2f} / frame {n}',fill='black')
  path=qa/f'overview-{offset//16+1}.jpg';sheet.save(path,quality=94);paths.append(str(path))
 cv2.imwrite(str(qa/'final-frame.jpg'),frames[m['frames']-1])
 def audio(path):
  return np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(path),'-vn','-ac','1','-ar',str(SR),'-f','f32le','pipe:1']),'<f4')
 actual=audio(DEST);expected=audio(OUT/'edited.wav');assert len(expected)==m['frames']*SPF
 corr=float(np.corrcoef(actual[:len(expected)],expected)[0,1]);assert corr>.999
 result=subprocess.run([ff,'-hide_banner','-i',str(DEST),'-af','silencedetect=noise=-38dB:d=0.08','-vn','-f','null','-'],capture_output=True,text=True,check=True)
 (qa/'silences.txt').write_text(result.stderr)
 gaps=[(float(a),float(b)) for a,b in re.findall(r'silence_start: ([\d.]+).*?silence_end: ([\d.]+)',result.stderr,re.S)]
 join_gaps=[]
 for b in m['audio_joins']:
  t=b['seconds'];gap=next((g for g in gaps if g[0]<=t<=g[1]),None);assert gap,(t,gaps)
  join_gaps.append(dict(time=t,quiet_interval=gap,duration=gap[1]-gap[0]))
 print('Encoded audio and all four quiet joins verified.',flush=True)
 model=WhisperModel('base.en',device='cpu',compute_type='int8',local_files_only=True)
 segments,_=model.transcribe(str(DEST),beam_size=5,word_timestamps=True)
 rows=[dict(start=s.start,end=s.end,text=s.text.strip(),words=[dict(start=w.start,end=w.end,word=w.word) for w in s.words]) for s in segments]
 (qa/'transcript.json').write_text(json.dumps(rows,indent=2)+'\n');(qa/'transcript.txt').write_text('\n'.join(f"{s['start']:.2f}-{s['end']:.2f} {s['text']}" for s in rows)+'\n')
 text=' '.join(s['text'].lower() for s in rows).replace('-',' ')
 retained=['great gatsby','human feedback','sycophancy','it has not disappeared','ask for the gaps','use a rubric','be direct with me','engagement trap','only one ended there','infinite scroll','missing page break','conversation continues','ad impressions','look for specifics','know what you came for','choose what happens next']
 for phrase in retained:assert phrase in text,phrase
 for phrase in ['half a million','lifetimes','meta,','settlement','17.1','useful feedback points to the work']:
  assert phrase not in text,phrase
 clips=[]
 for label,t,d in [('flattery-to-engagement',7661/30-7,20),('scroll-to-ai',10561/30-6,21),('combined-closing',close_start/30-5,m['duration_seconds']-close_start/30+5)]:
  p=qa/f'{label}.mp4';subprocess.run([ff,'-y','-v','error','-ss',str(t),'-i',str(DEST),'-t',str(d),'-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',str(p)],check=True);clips.append(str(p))
 assert all(sha(p)==h for p,h in m['protected'].items())
 report=dict(candidate=str(DEST),sha256=sha(DEST),frames=len(pts),fps=30,duration_seconds=len(pts)/30,maximum_picture_thumbnail_mae=max(diff),all_frame_mappings_verified=True,encoded_audio_correlation=corr,join_gaps=join_gaps,retained_narration_checks=retained,deleted_narration_absent=True,protected_files_unchanged=True,overview_sheets=paths,clips=clips,perceptual_listening=False,continuous_motion_playback=False,visual_frame_inspection='Pending',shipping_status='Review candidate only; not installed or published.')
 (qa/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
