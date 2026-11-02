#!/usr/bin/env python3
"""Verify the one-second insertion and that everything around it is preserved."""
import json,subprocess,re,wave,hashlib
from pathlib import Path
import av,cv2,numpy as np
from PIL import Image,ImageDraw
from faster_whisper import WhisperModel
from build_flattery_trap_v16 import base,CUT,EXTRA
ROOT,OUT,DEST,FF=base.ROOT,base.OUT,base.DEST,base.FF
OLD=ROOT/'video-audit/flattery-trap-borders-close-2026-11-02/build-v15'
def pcm(p):
 with wave.open(str(p),'rb') as w:return np.frombuffer(w.readframes(w.getnframes()),'<i2')
def main():
 qa=OUT/'qa';qa.mkdir(exist_ok=True)
 m=json.loads((OUT/'edit-manifest.json').read_text());assert base.sha(DEST)==m['candidate_sha256']
 expected=np.load(OUT/'expected-thumbnails.npy',mmap_mode='r');old=np.load(OLD/'expected-thumbnails.npy',mmap_mode='r')
 assert np.array_equal(expected[:CUT],old[:CUT])
 assert np.all(expected[CUT:CUT+EXTRA]==old[CUT-1])
 assert np.array_equal(expected[CUT+EXTRA:],old[CUT:])
 audio=pcm(OUT/'edited.wav');oldaudio=pcm(OLD/'edited.wav');pos=CUT*base.SPF
 assert len(audio)==len(oldaudio)+48000
 assert np.array_equal(audio[:pos],oldaudio[:pos]) and np.array_equal(audio[pos+48000:],oldaudio[pos:])
 pts=[];maxerr=0;frames={};wanted=[CUT-15,CUT-1,CUT,CUT+15,CUT+29,CUT+30,CUT+31,base.total-1]
 with av.open(str(DEST)) as c:
  for n,fr in enumerate(c.decode(video=0)):
   pts.append(float(fr.pts*fr.time_base));im=fr.to_ndarray(format='bgr24')
   err=float(np.abs(cv2.resize(im,(80,45),interpolation=cv2.INTER_AREA).astype(float)-expected[n].astype(float)).mean());maxerr=max(maxerr,err);assert err<3.5,(n,err)
   if n in wanted:frames[n]=im
 assert len(pts)==base.total==7264 and np.allclose(np.diff(pts),1/30,atol=1e-6)
 dec=np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(DEST),'-vn','-ac','1','-ar','48000','-f','f32le','-']),'<f4')
 corr=float(np.corrcoef(dec[:len(audio)],audio.astype(float)/32768)[0,1]);assert corr>.998
 silence=subprocess.run([FF,'-hide_banner','-i',str(DEST),'-vn','-af','silencedetect=noise=-38dB:d=0.08','-f','null','-'],capture_output=True,text=True,check=True)
 (qa/'silences.txt').write_text(silence.stderr)
 gaps=[(float(a),float(b)) for a,b in re.findall(r'silence_start: ([\d.]+).*?silence_end: ([\d.]+)',silence.stderr,re.S)]
 gap=next((a,b) for a,b in gaps if a<=231.6 and b>=232.6)
 assert abs((gap[1]-gap[0])-1.554583)<.03,gap
 subprocess.run([base.sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(qa/'transitions'),'--boundary',f'{CUT}:pause-start','--boundary',f'{CUT+EXTRA}:close-start'],check=True)
 sheet=Image.new('RGB',(1280,420),'white');d=ImageDraw.Draw(sheet)
 for i,n in enumerate(wanted):
  x=i%4*320;y=i//4*210;sheet.paste(Image.fromarray(cv2.cvtColor(frames[n],cv2.COLOR_BGR2RGB)).resize((320,180)),(x,y));d.text((x+4,y+184),f'{n/30:.3f}s f{n}',fill='black')
 sheet.save(qa/'pause-and-close.jpg');cv2.imwrite(str(qa/'final-frame.jpg'),frames[base.total-1])
 subprocess.run([FF,'-v','error','-ss','225','-i',str(DEST),'-vn','-ar','16000','-ac','1',str(qa/'ending.wav')],check=True)
 model=WhisperModel('base.en',device='cpu',compute_type='int8',local_files_only=True,cpu_threads=4);segs,_=model.transcribe(str(qa/'ending.wav'),beam_size=5)
 rows=[dict(start=s.start+225,end=s.end+225,text=s.text.strip()) for s in segs];(qa/'ending-transcript.json').write_text(json.dumps(rows,indent=2)+'\n')
 text=' '.join(s['text'] for s in rows).lower()
 for phrase in ['improve the work','not approve of you','useful feedback points to the work','look for specifics','not approval']:assert phrase in text,phrase
 protected={p:base.sha(p)==h for p,h in m['protected'].items()};assert all(v for p,v in protected.items() if p not in [str(ROOT/'index.html'),str(ROOT/'course-assets/manifest.json')])
 report=dict(candidate=str(DEST),sha256=base.sha(DEST),duration_seconds=base.total/30,frames=len(pts),added_seconds=1,hold_frames=30,all_other_rendered_thumbnails_identical=True,all_other_edited_audio_identical=True,encoded_frame_timing_verified=True,max_thumbnail_mae=maxerr,encoded_audio_correlation=corr,measured_closing_gap=gap,measured_closing_gap_seconds=gap[1]-gap[0],new_boundaries_pass=True,closing_words_verified=True,visual_inspection='Pending',perceptual_listening=False,continuous_playback=False,installed=False,published=False)
 (qa/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
 subprocess.run([FF,'-v','error','-ss','225','-i',str(DEST),'-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',str(qa/'ending.mp4')],check=True)
if __name__=='__main__':main()
