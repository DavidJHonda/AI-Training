from pathlib import Path
import json,hashlib,wave,subprocess,sys
import cv2,numpy as np,av,imageio_ffmpeg
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
m=json.loads((OUT/'edit-manifest.json').read_text());p=Path(m['output']);qa=OUT/'qa';qa.mkdir(exist_ok=True)
cv2.setNumThreads(2)
# Independent decoded frame count, presentation timestamp cadence, and final frame.
c=av.open(str(p));stream=c.streams.video[0];pts=[];count=0;sample=[];last=None;special={}
for key,B in m['boards'].items():
 first=min(r['start_frame'] for r in m['visual_timeline'] if r['visual']==key);special[first]=key+'-full-open'
 for i,state in enumerate(B['states']):special[state['at']+35]=f'{key}-state-{i}'
for offset,label in [(0,'close-in'),(47,'close-hold'),(198,'close-settled')]:special[m['close']['start_frame']+offset]=label
for r in m['visual_timeline']:
 if r['visual']=='citation':special[r['start_frame']+60]='citation'
for frame in c.decode(video=0):
 pts.append(int(frame.pts));im=frame.to_ndarray(format='bgr24');count+=1;idx=count-1
 if idx in special:cv2.imwrite(str(qa/(special[idx]+'.jpg')),im)
 if idx%240==0:
  cell=Image.new('RGB',(480,295),'white');cell.paste(Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)).resize((480,270)));ImageDraw.Draw(cell).text((8,275),f'{idx/30:.2f}s / frame {idx}',fill='black');sample.append(cell)
 last=im
assert count==m['total_frames'],(count,m['total_frames']);assert last is not None
cv2.imwrite(str(qa/'final-frame.jpg'),last)
for offset in range(0,len(sample),16):
 cells=sample[offset:offset+16];sheet=Image.new('RGB',(1920,295*((len(cells)+3)//4)),'white')
 for i,im in enumerate(cells):sheet.paste(im,((i%4)*480,(i//4)*295))
 sheet.save(qa/f'overview-{offset//16}.jpg')
delta=np.diff(pts);vals,counts=np.unique(delta,return_counts=True)
assert len(vals)==1,dict(zip(vals.tolist(),counts.tolist()))
ff=imageio_ffmpeg.get_ffmpeg_exe();wav=qa/'encoded.wav'
subprocess.run([ff,'-v','error','-y','-i',str(p),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(wav)],check=True)
with wave.open(str(wav)) as w:a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float);ns=len(a)
with wave.open(str(OUT/'edited.wav')) as w:b=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
n=min(len(a),len(b));corr=float(np.corrcoef(a[:n],b[:n])[0,1]);assert corr>.995,corr
assert abs(ns/48000-count/30)<.05,(ns/48000,count/30)
checks={'candidate':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'decoded_frames':count,'width':stream.width,'height':stream.height,'fps':str(stream.average_rate),'video_time_base':str(stream.time_base),'pts_delta_histogram':dict(zip(map(str,vals.tolist()),counts.tolist())),'duration':count/30,'audio_duration':ns/48000,'audio_correlation_to_assembly':corr,'peak_encoded_dbfs':float(20*np.log10(max(abs(a))/32768)),'protected_unchanged':{s:hashlib.sha256(Path(s).read_bytes()).hexdigest()==h for s,h in m['protected'].items()},'direct_listening':False}
assert all(checks['protected_unchanged'].values())
(qa/'verification.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2),flush=True)
# Actual encoded audio splice context for final review.
for i,r in enumerate(m['audio_timeline'][1:],1):
 t=r['start_frame']/30
 subprocess.run([ff,'-v','error','-y','-i',str(p),'-ss',str(max(0,t-3)),'-t','8','-vn','-c:a','pcm_s16le',str(qa/f'join-{i}-{t:.2f}s.wav')],check=True)
# All edited visual boundaries plus opening correction's natural scene boundary.
boundaries={r['start_frame']:r['visual']+'-'+str(r['reason']) for r in m['visual_timeline'][1:]};boundaries[249]='opening-label-repair-ends'
cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(p),'--outdir',str(qa/'transitions')]
for f,label in sorted(boundaries.items()):cmd+=['--boundary',f'{f}:{label}']
r=subprocess.run(cmd,capture_output=True,text=True);(qa/'transition-command.log').write_text(r.stdout+r.stderr);print(r.stdout[-2000:],flush=True)
print('Transition guard exit:',r.returncode,flush=True)
