#!/usr/bin/env python3
"""Approved Doubter removal; two review candidates, original voice, native board pixels."""
from pathlib import Path
import json, hashlib, subprocess, sys, shutil, wave
import av, cv2, numpy as np, imageio_ffmpeg
import build_loudest_voices_v8 as old
from ken_burns_path import draw_ring, hex_bgr
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/remove-doubter-2026-10-22'
FF=imageio_ffmpeg.get_ffmpeg_exe()
cv2.setNumThreads(1)
SOURCES={
 'lv':(ROOT/'Prompts/loudest-voices-v8.mp4','d553d341c258f1420b8a5927f6a6cdd2652a12b1f0d6fafe5d55f66089b497a4'),
 'hands':(ROOT/'Prompts/in-your-hands-v6.mp4','721e0738684fa09007104865ef0ca292dac2951a93766d04e7db8bcfbde2151c'),
 'opener':(OUT/'opener-source-v5.mp4','fd185a172e88b4fe4828b0290923eb113d1074368a1e2ed892b7604b9d38f2fd')}
PLANS={
 'loudest-voices-v10': [('lv',0,2751),('lv',3612,3823),('lv',3884,6488),('hands',1074,3477),('hands',5019,5508)],
 'embrace-the-future-opener-v6':[('opener',0,1062),('opener',1209,1429),('opener',1531,6168)]}
# Source-timeline events; the Hinton quotation starts at 2224, eliminating the 10-frame biography flash.
LV_EVENTS=[712,873,1191,1500,1905,2080,2224,2570,3630,3709,3771,3892,4142]
OP_EVENTS=[1209,1337,1540]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pcm(p):return np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-ac','2','-ar','48000','-f','f32le','-']),np.float32).reshape(-1,2)
def frames(p):
 with av.open(str(p)) as c:
  c.streams.video[0].codec_context.thread_count=1
  for n,f in enumerate(c.decode(video=0)):yield n,f.to_ndarray(format='bgr24')
class Boards(old.Boards):
 def __init__(self):
  layout=json.loads((ROOT/'scripts/video/assets/loudest-two-experts/layout.json').read_text())
  old.CARDS=[c['bounds'] for c in layout['cards']];old.SECTIONS=[c['sections'] for c in layout['cards']]
  old.COLORS=[c['accent'] for c in layout['cards']]
  old.EVENTS=[(873,0,0),(1191,0,1),(1500,0,2),(1905,1,0),(2224,1,1),(2570,1,2)]
  old.SUMMARY=[(3630,[0,1]),(3709,[0]),(3771,[1]),(3892,[0,1])]
  super().__init__()
class Renderer:
 def __init__(self):
  self.boards=Boards();self.opener=cv2.resize(cv2.imread(str(ROOT/'course-assets/embrace-the-future-opener/embrace-the-future-opener-voices.jpg')),(1280,720),interpolation=cv2.INTER_LANCZOS4)
  self.op_states={}
  for state,rects in [('positive',[(125,322,747,367),(125,470,835,515)]),('negative',[(125,396,733,441),(125,542,564,587)])]:
   im=self.opener.copy()
   for a,b,c,d in rects:draw_ring(im,(a-18)*.8,(b-9)*.8,(c+18)*.8,(d+9)*.8,hex_bgr('#f2cf5b'),12,4)
   self.op_states[state]=im
  canvas=OUT/'close-canvas.png'
  if not canvas.exists():subprocess.run([sys.executable,str(ROOT/'scripts/video/make_close_board.py'),'--lesson','whatpeoplesay','--out',str(canvas)],check=True)
  self.close=cv2.imread(str(canvas))
 def replacement(self,src,n,closing=False):
  if closing:
   k=n-5019;z=1 if k<48 else (1+.2*(k-48)/149 if k<198 else 1.2)
   h,w=self.close.shape[:2];cw=int(w/z);ch=int(h/z);x=(w-cw)//2;y=(h-ch)//2
   return cv2.resize(self.close[y:y+ch,x:x+cw],(1280,720),interpolation=cv2.INTER_LANCZOS4)
  if src=='lv' and (712<=n<2080 or 2224<=n<2751 or 3612<=n<4142):return self.boards.render(n)
  if src=='opener' and 1209<=n<1540:return self.op_states['positive' if n<1337 else 'negative']
  return None

def main():
 OUT.mkdir(exist_ok=True)
 live=ROOT/'course-assets/embrace-the-future-opener/embrace-the-future-opener.mp4'
 if not SOURCES['opener'][0].exists():
  assert sha(live)==SOURCES['opener'][1];shutil.copyfile(live,SOURCES['opener'][0])
 for p,h in SOURCES.values():assert sha(p)==h,(p,'changed')
 render=Renderer();audios={k:pcm(p) for k,(p,h) in SOURCES.items()}
 for name,plan in PLANS.items():
  dest=ROOT/'Prompts'/f'{name}.mp4';assert not dest.exists(),'Do not overwrite a review candidate'
  audio=[];timeline=[];boundaries=[];offset=0
  for i,(src,start,end) in enumerate(plan):
   a=audios[src][start*1600:end*1600].copy()
   if i:a[:240]*=(np.arange(240)/240)[:,None];boundaries.append({'frame':offset,'label':f'audio-join-{i}'})
   if i<len(plan)-1:a[-240:]*=(1-np.arange(240)/240)[:,None]
   audio.append(a)
   timeline.append({'source_key':src,'source':str(SOURCES[src][0].relative_to(ROOT)),'source_start_frame':start,'source_end_frame':end,'output_start_frame':offset,'output_end_frame':offset+end-start})
   for n in (LV_EVENTS if src=='lv' else OP_EVENTS if src=='opener' else []):
    if start<=n<end and offset+n-start>0:boundaries.append({'frame':offset+n-start,'label':f'{src}-visual-{n}'})
   offset+=end-start
  sound=np.concatenate(audio);wav=OUT/f'{name}-audio.wav'
  with wave.open(str(wav),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(48000);w.writeframes((np.clip(sound,-1,1)*32767).astype('<i2').tobytes())
  cmd=[FF,'-hide_banner','-loglevel','warning','-n','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','30','-i','-','-i',str(wav),'-map','0:v','-map','1:a','-c:v','libx264','-threads','4','-crf','18','-preset','medium','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',str(dest)]
  with (OUT/f'{name}-encode.log').open('w') as log:
   proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
   for i,(src,start,end) in enumerate(plan):
    print(name,src,start,end,flush=True)
    for n,im in frames(SOURCES[src][0]):
     if n<start:continue
     if n>=end:break
     replacement=render.replacement(src,n,name.startswith('loudest') and i==len(plan)-1)
     proc.stdin.write((im if replacement is None else replacement).tobytes())
   proc.stdin.close();assert proc.wait()==0
  unique={b['frame']:b for b in boundaries}
  manifest={'candidate':str(dest.relative_to(ROOT)),'sha256':sha(dest),'frames':offset,'fps':30,'duration':offset/30,'timeline':timeline,'boundaries':sorted(unique.values(),key=lambda b:b['frame']), 'source_hashes':{str(p.relative_to(ROOT)):h for p,h in SOURCES.values()},'audio':'Original stereo PCM; frame-aligned cuts, 5 ms fades only in quiet handles, one AAC encode. No synthesized narration.', 'video':'One additional H264 encode from surviving finished sources. Untouched scenes retain source framing and timing.', 'status':'Review candidate; not installed'}
  (OUT/f'{name}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
  print('COMPLETE',name,offset,offset/30,flush=True)
if __name__=='__main__':main()
