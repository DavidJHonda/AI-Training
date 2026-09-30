#!/usr/bin/env python3
"""Approved two-scene visual correction. Preserve audio and unaffected H.264 GOPs."""
from pathlib import Path
import argparse,hashlib,json,subprocess
import cv2
import av
import imageio_ffmpeg
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/honesty-and-privacy-build-2026-09-30-v5'
SRC=ROOT/'course-assets/honesty-and-privacy/honesty-and-privacy.mp4'
DEST=ROOT/'Prompts/honesty-and-privacy-v5.mp4'
EXPECTED='4207c924c8e9738f6a450662774fbac4df3c5c106dd99b721e6506baa5bdb47a'
SPANS=[(3054,3704,'context'),(6258,6716,'retention')]
FF=imageio_ffmpeg.get_ffmpeg_exe()
cv2.setNumThreads(1)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def frames(stop=7200):
 with av.open(str(SRC)) as c:
  c.streams.video[0].codec_context.thread_count=2
  for n,f in enumerate(c.decode(video=0)):
   if n>=stop:break
   yield n,f.to_ndarray(format='bgr24')
def font(s):return ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold.ttf',s)
def center(d,box,text,size=25,color='#254e3b'):
 x0,y0,x1,y1=box;f=font(size)
 d.text(((x0+x1)/2,(y0+y1)/2),text,font=f,fill=color,anchor='mm')
def rgb(a):return Image.fromarray(cv2.cvtColor(a,cv2.COLOR_BGR2RGB))
def bgr(a):return cv2.cvtColor(np.array(a),cv2.COLOR_RGB2BGR)
class Patch:
 def __init__(self,samples):
  self.blank=samples[3054]
  self.retblank=samples[6258]
  self.retfull=samples[6288]
  self.top=(510,34,925,130)
  self.warning=(465,520,825,580)
  self.record=(848,219,1218,444)
  self.policy=(808,444,1258,577)
  im=rgb(self.retfull);d=ImageDraw.Draw(im)
  # The old record panel and its later purge animation occupy exactly this box.
  d.rectangle(self.record,fill=(247,252,249))
  d.rounded_rectangle((860,222,1211,419),radius=24,fill='#283c3d',outline='#416c55',width=2)
  center(d,(868,245,1203,308),'A copy may remain',25,'#f6faf2')
  for y,w in [(335,247),(360,190)]:d.rounded_rectangle((909,y,909+w,y+8),radius=4,fill='#b4c4b9')
  d.rounded_rectangle((834,455,1215,561),radius=14,fill='#edf3eb',outline='#9aaf99',width=2)
  center(d,(840,465,1209,505),'Retention and deletion',23)
  center(d,(840,505,1209,548),'depend on the service',23)
  self.retnew=bgr(im)
  self.labels={}
  for label in ['Needs context','Useful context','Share only what is needed']:
   im=rgb(self.blank);d=ImageDraw.Draw(im)
   d.rounded_rectangle((520,47,916,117),radius=25,fill='#f5faf4',outline='#648969',width=2)
   center(d,(524,48,912,117),label,24 if len(label)<20 else 23)
   self.labels[label]=bgr(im)
 def render(self,frame,n):
  out=frame.copy()
  if 3054<=n<3704:
   # Follow the original entrance fade; the final label follows the rule of thumb.
   label='Needs context' if n<3426 else ('Useful context' if n<3562 else 'Share only what is needed')
   alpha=min(1,max(0,(n-3057)/18))
   x0,y0,x1,y1=self.top
   out[y0:y1,x0:x1]=np.rint(self.blank[y0:y1,x0:x1]*(1-alpha)+self.labels[label][y0:y1,x0:x1]*alpha).astype('uint8')
   # This region contains only the unsupported warning; keep other moving elements.
   x0,y0,x1,y1=self.warning
   out[y0:y1,x0:x1]=self.blank[y0:y1,x0:x1]
  if 6258<=n<6522:
   # Measured scene entrance using its title against the actual blank first frame.
   roi=(slice(33,75),slice(270,1020))
   base=self.retblank[roi].astype(float);full=self.retfull[roi].astype(float)-base
   alpha=float(np.clip(((frame[roi]-base)*full).sum()/(full*full).sum(),0,1))
   for x0,y0,x1,y1 in [self.record,self.policy]:
    out[y0:y1,x0:x1]=np.rint(self.retblank[y0:y1,x0:x1]*(1-alpha)+self.retnew[y0:y1,x0:x1]*alpha).astype('uint8')
  return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
 OUT.mkdir(exist_ok=True)
 assert sha(SRC)==EXPECTED
 samples={n:f for n,f in frames(6290) if n in {3054,6258,6288}}
 patch=Patch(samples)
 wanted={3054,3070,3084,3234,3414,3444,3504,3564,3594,3684,3703,6258,6273,6288,6333,6363,6438,6483,6521}
 if args.preview:
  for n,f in frames(6522):
   if n in wanted:cv2.imwrite(str(OUT/f'preview-{n:05}.jpg'),patch.render(f,n))
  return
 assert not DEST.exists(),'Never overwrite a candidate'
 protected={str(p):sha(p) for p in [SRC,ROOT/'lessons/honesty-and-privacy.md',*SRC.parent.glob('*.jpg')]}
 procs=[];logs=[]
 for a,b,name in SPANS:
  log=(OUT/f'encode-{name}.log').open('w');logs.append(log)
  cmd=[FF,'-v','error','-y','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','30','-i','-','-an','-c:v','libx264','-threads','2','-crf','16','-preset','fast','-vf','setsar=1','-pix_fmt','yuv420p','-profile:v','high','-level:v','3.1','-video_track_timescale','15360',str(OUT/f'leg-{name}.mp4')]
  procs.append(subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log))
 for n,f in frames(6716):
  for i,(a,b,name) in enumerate(SPANS):
   if a<=n<b:
    result=patch.render(f,n);procs[i].stdin.write(result.tobytes())
    if n in wanted:cv2.imwrite(str(OUT/f'preview-{n:05}.jpg'),result)
 for p in procs:p.stdin.close();assert p.wait()==0
 for log in logs:log.close()
 print('Encoded changed GOPs',flush=True)
 source=av.open(str(SRC));video=source.streams.video[0];audio=source.streams.audio[0]
 packets=[];keys=[]
 for p in source.demux(video,audio):
  if p.dts is None:continue
  iv=p.stream.type=='video';n=round(float(p.pts*p.time_base)*30) if iv else None
  if iv and p.is_keyframe:keys.append(n)
  if iv and any(a<=n<b for a,b,_ in SPANS):continue
  packets.append((iv,p))
 legs=[]
 for a,b,name in SPANS:
  assert a in keys and b in keys
  c=av.open(str(OUT/f'leg-{name}.mp4'));legs.append(c);v=c.streams.video[0]
  assert v.time_base==video.time_base
  assert v.codec_context.extradata==video.codec_context.extradata,(v.codec_context.extradata.hex(),video.codec_context.extradata.hex())
  count=0
  for p in c.demux(v):
   if p.dts is None:continue
   p.pts+=a*512;p.dts+=a*512;packets.append((True,p));count+=1
  assert count==b-a
 packets.sort(key=lambda x:(x[1].dts*x[1].time_base,not x[0]))
 with av.open(str(DEST),'w',options={'movflags':'+faststart'}) as out:
  ov=out.add_stream_from_template(video);oa=out.add_stream_from_template(audio)
  for iv,p in packets:p.stream=ov if iv else oa;out.mux(p)
 assert all(sha(p)==h for p,h in protected.items())
 manifest=dict(source=str(SRC),source_sha256=EXPECTED,candidate=str(DEST),candidate_sha256=sha(DEST),frames=7200,fps=30,duration=240,
  scope='User approved build after evaluation; narrow two-diagram correction. No audio, pause, course board or timeline changes.',
  source_limitation='Raw rolls unavailable. Encode changed GOPs once from current finished release; copy unaffected video packets and all audio packets.',
  encoded_spans=SPANS,visual_spans=[[3054,3704],[6258,6522]],label_changes=['Needs context','Useful context','Share only what is needed','A copy may remain','Retention and deletion depend on the service'],
  boundaries=[dict(frame=n,label=l) for n,l in [(3054,'context-in'),(3426,'useful-context'),(3562,'minimum-context'),(3704,'context-out'),(6258,'retention-in'),(6522,'retention-out'),(6716,'GOP-copy-resumes')]],protected_hashes=protected,status='Review candidate only; not shipped or published')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
