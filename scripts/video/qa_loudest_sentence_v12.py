#!/usr/bin/env python3
import hashlib,json,subprocess,sys
import av,cv2,numpy as np
from PIL import Image,ImageDraw
from cut_loudest_sentence_v12 import ROOT,OUT,SOURCE,DEST,A,CUT0,CUT1,B,SHIFT
from build_remove_doubter import FF,pcm,Boards

def video_packets(path):
 with av.open(str(path)) as c:
  return {round(p.pts/512):(hashlib.sha256(bytes(p)).hexdigest(),p.dts) for p in c.demux(c.streams.video[0]) if p.dts is not None}
s=video_packets(SOURCE);d=video_packets(DEST);assert len(d)==8302
n=0
for f,(h,t) in s.items():
 if A<=f<B:continue
 target=f-SHIFT if f>=B else f
 assert d[target]==(h,t-SHIFT*512 if f>=B else t);n+=1
wav=ROOT/'video-audit/remove-doubter-2026-10-22/loudest-voices-v10-audio.wav'
x=pcm(wav);left=x[:CUT0*1600].copy();right=x[CUT1*1600:].copy();left[-240:]*=(1-np.arange(240)/240)[:,None];right[:240]*=(np.arange(240)/240)[:,None]
expected=np.concatenate([left,right]);actual=pcm(DEST)[:len(expected)];assert actual.shape==expected.shape
corr=float(np.corrcoef(actual.ravel(),expected.ravel())[0,1]);assert corr>.995
join=CUT0*1600
board=Boards().full();errors=[];selected=[];wanted={596,597,707,708,709,716,717,730,8301};timestamps=[]
with av.open(str(DEST)) as c:
 assert float(c.streams.video[0].average_rate)==30
 for f,im in enumerate(c.decode(video=0)):
  timestamps.append(float(im.pts*im.time_base))
  if A<=f<B-SHIFT or f in wanted:
   ar=im.to_ndarray(format='bgr24')
   if A<=f<B-SHIFT:errors.append(float(np.abs(cv2.resize(ar,(320,180)).astype(np.int16)-cv2.resize(board,(320,180)).astype(np.int16)).mean()))
   if f in wanted:selected.append((f,ar))
assert len(timestamps)==8302 and max(errors)<5
assert np.max(np.abs(np.diff(timestamps)-1/30))<.0001
sheet=Image.new('RGB',(1280,((len(selected)+2)//3)*264),'white');draw=ImageDraw.Draw(sheet)
for i,(f,im) in enumerate(selected):
 x=i%3*426;y=i//3*264;sheet.paste(Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)).resize((426,240)),(x,y));draw.text((x+5,y+243),f'{f/30:.3f}s / f{f}',fill='black')
sheet.save(OUT/'cut-review.jpg')
subprocess.run([sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--boundary',str(A),'--boundary',str(CUT0),'--boundary',str(B-SHIFT),'--outdir',str(OUT/'transitions'),'--max-island','12'],check=True)
qa={'frames':8302,'duration':8302/30,'copied_video_packets_verified':n,'native_board_frames_verified':len(errors),'audio_correlation':corr,'join_seconds':CUT0/30,'join_sample_step':float(np.abs(actual[join]-actual[join-1]).max()),'join_before_rms_db':float(20*np.log10(np.sqrt(np.mean(actual[join-480:join]**2))+1e-12)),'join_after_rms_db':float(20*np.log10(np.sqrt(np.mean(actual[join:join+480]**2))+1e-12)),'listening':'Not performed; review the new join using the review page.'}
(OUT/'qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa,indent=2))
subprocess.run([FF,'-v','error','-n','-i',str(DEST),'-t','34','-vn','-c:a','copy',str(OUT/'opening-audio.m4a')],check=True)
