#!/usr/bin/env python3
"""Check frame mapping, native board replacements, audio edits, and every changed boundary."""
import json,subprocess,sys
import av,cv2,numpy as np
from PIL import Image,ImageDraw
from build_remove_doubter import ROOT,OUT,FF,SOURCES,PLANS,Renderer,sha,pcm,frames

def main():
 render=Renderer()
 for name,plan in PLANS.items():
  m=json.loads((OUT/f'{name}-manifest.json').read_text());dest=ROOT/m['candidate']
  audio=pcm(dest);expected=pcm(OUT/f'{name}-audio.wav');audio=audio[:len(expected)]
  assert audio.shape==expected.shape
  corr=float(np.corrcoef(audio.ravel(),expected.ravel())[0,1]);assert corr>.995,corr
  seams=[]
  for leg in m['timeline'][1:]:
   f=leg['output_start_frame'];s=f*1600
   seams.append({'frame':f,'time':f/30,'step':float(np.abs(audio[s]-audio[s-1]).max()),'rms_before_db':float(20*np.log10(np.sqrt(np.mean(audio[s-480:s]**2))+1e-12)),'rms_after_db':float(20*np.log10(np.sqrt(np.mean(audio[s:s+480]**2))+1e-12))})
  cap=cv2.VideoCapture(str(dest));errs=[];n=0;replaced=0;samples=[]
  wanted={0,m['frames']-1,*[b['frame']+15 for b in m['boundaries']]}
  if name.startswith('loudest'):wanted.update([2219,2223,2224,2230,2233,2234,2240,m['frames']-291])
  for i,(src,start,end) in enumerate(plan):
   for k,ref in frames(SOURCES[src][0]):
    if k<start:continue
    if k>=end:break
    replacement=render.replacement(src,k,name.startswith('loudest') and i==len(plan)-1)
    if replacement is not None:ref=replacement;replaced+=1
    ok,im=cap.read();assert ok
    err=float(np.abs(cv2.resize(im,(320,180)).astype(np.int16)-cv2.resize(ref,(320,180)).astype(np.int16)).mean());errs.append(err)
    if n in wanted:samples.append((n,im.copy()))
    n+=1
  assert not cap.read()[0];cap.release();assert n==m['frames']
  assert max(errs)<8,max(errs)
  with av.open(str(dest)) as c:
   v=c.streams.video[0];assert (v.width,v.height,float(v.average_rate))==(1280,720,30)
   pts=np.array([float(f.pts*f.time_base) for f in c.decode(video=0)])
   assert np.max(np.abs(np.diff(pts)-1/30))<.0001
  sheet=Image.new('RGB',(1280,((len(samples)+2)//3)*264),'white');d=ImageDraw.Draw(sheet)
  for i,(f,im) in enumerate(samples):
   x=i%3*426;y=i//3*264
   sheet.paste(Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)).resize((426,240)),(x,y));d.text((x+6,y+242),f'{f/30:.3f}s / f{f}',fill='black')
   cv2.imwrite(str(OUT/f'{name}-frame-{f}.jpg'),im)
  sheet.save(OUT/f'{name}-contact.jpg')
  cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(dest),'--outdir',str(OUT/f'{name}-transitions'),'--max-island','12','--handle','18']
  for b in m['boundaries']:cmd+=['--boundary',str(b['frame'])+':'+b['label']]
  subprocess.run(cmd,check=True)
  for p,h in SOURCES.values():assert sha(p)==h
  installed={'course-assets/loudest-voices/loudest-voices.mp4':SOURCES['lv'][1],'course-assets/embrace-the-future-opener/embrace-the-future-opener.mp4':SOURCES['opener'][1]}
  for p,h in installed.items():assert sha(ROOT/p)==h
  result={'candidate':m['candidate'],'frames':n,'duration':n/30,'all_frames_compared':n,'board_replacement_frames':replaced,'mean_frame_error':float(np.mean(errs)),'max_frame_error':max(errs),'audio_correlation':corr,'audio_rms_error':float(np.sqrt(np.mean((audio-expected)**2))),'audio_peak_dbfs':float(20*np.log10(np.abs(audio).max())),'seams':seams,'sources_and_installed_videos_unchanged':True,'listening':'Not performed; frame checks, transcription, and PCM analysis do not certify audible cadence.'}
  (OUT/f'{name}-qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
