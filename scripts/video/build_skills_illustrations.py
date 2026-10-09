#!/usr/bin/env python3
"""Build Your Skills Learning Illustration Pass: approved visual-only replacements."""
from pathlib import Path
import argparse,json,hashlib,subprocess
from fractions import Fraction
import av,cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/build-your-skills-illustration-updates-2026-10-08'
ASSETS=OUT/'assets';PREVIEW=OUT/'previews';FF=imageio_ffmpeg.get_ffmpeg_exe()
FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
SOURCES={
'people-skills':dict(id='P1',version=7,sha='dc2a346a75558d408d02f0ed2e30979780c6968c59f76bfbe34d5342c57ef18f',frames=3830,start=0,end=798,encode_start=0,encode_end=798,changes=[233,344,387,419,464],crf=18),
'curious-and-flexible':dict(id='P2',version=11,sha='f34ee905c30cea0e839e9f0bb0ed390575dd2aff4d7801ec619c43906b1fdecf',frames=6376,start=0,end=911,encode_start=0,encode_end=911,changes=[306,593,719],crf=16),
'make-your-move':dict(id='P3',version=10,sha='b0093c677628a758faf67e5388ffd30f8d95f4e2543ca28a7b572bc20cbd1cfc',frames=8825,start=8167,end=8343,encode_start=8167,encode_end=8343,changes=[],crf=16)}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(n):return ImageFont.truetype(str(FONT),n)
def text(d,xy,s,n=32,fill='#203335'):d.text(xy,s,font=font(n),fill=fill)
PHOTOS={}
def photo(name):
 if name not in PHOTOS:PHOTOS[name]=ImageOps.fit(Image.open(ASSETS/(name+'.png')).convert('RGB'),(1280,720),method=Image.Resampling.LANCZOS)
 return PHOTOS[name]
def push(im,t,anchor=(.5,.5),amount=.025):
 scale=1+amount*max(0,min(1,t));w,h=im.size;cw,ch=w/scale,h/scale
 x=(w-cw)*anchor[0];y=(h-ch)*anchor[1]
 return im.crop((x,y,x+cw,y+ch)).resize((w,h),Image.Resampling.LANCZOS)
def render(cfg,n):
 if cfg['id']=='P1':
  if n<233:name,a,b='people_start',0,233
  elif n<344:name,a,b='people_suggest',233,344
  elif n<464:name,a,b='people_interrupt',344,464
  else:name,a,b='people_quiet',464,798
  im=push(photo(name),(n-a)/(b-a),(.7,.35));d=ImageDraw.Draw(im)
  if 387<=n<464:
   d.rounded_rectangle((42,572,705,685),radius=15,fill='#f8f6ed')
   text(d,(64,580),'“We are done.”',32)
   if n>=419:text(d,(64,630),'“No more suggestions.”',32)
 elif cfg['id']=='P2':
  if n<306:name,a,b='basketball_start',0,306
  elif n<719:name,a,b='basketball_blocked',306,719
  else:name,a,b='basketball_pass',719,911
  im=push(photo(name),(n-a)/(b-a),(.5,.4),.018);d=ImageDraw.Draw(im)
  if 593<=n<719:
   # Highlight the open receiver on the spoken curiosity cue; adjusted for the gentle push.
   t=(n-306)/(719-306);scale=1+.018*t
   box=[640+(x-640)*scale if i%2==0 else 288+(x-288)*scale for i,x in enumerate((420,154,522,410))]
   d.rounded_rectangle(tuple(round(x) for x in box),radius=16,outline='#38aa9b',width=4)
  if n>=593:
   d.rounded_rectangle((390,558,1239,686),radius=15,fill='#f7f8f3')
   text(d,(413,570),'Curious: look for another play',31,'#176b62')
   if n>=719:text(d,(413,626),'Flexible: change the play',31,'#176b62')
 else:im=push(photo('donation'),(n-cfg['start'])/(cfg['end']-cfg['start']-1),(.8,.5),.035)
 return np.array(im)
def paths(slug,cfg):return ROOT/f'course-assets/{slug}/{slug}.mp4',ROOT/f'Prompts/{slug}-v{cfg["version"]}.mp4'
def build(slug,cfg):
 src,dst=paths(slug,cfg);assert sha(src)==cfg['sha'];assert not dst.exists(),dst
 protected={str(p):sha(p) for p in [src,ROOT/f'lessons/{slug}.md',*sorted(src.parent.glob('*.jpg'))]}
 leg=OUT/f'{slug}-leg.mp4';log=(OUT/f'{slug}-encode.log').open('w')
 cmd=[FF,'-v','error','-y','-f','rawvideo','-pixel_format','yuv420p','-video_size','1280x720','-framerate','30','-i','-', '-an','-c:v','libx264','-threads','2','-preset',('medium' if cfg['id']=='P1' else 'fast'),'-crf',str(cfg['crf']),'-profile:v','high','-level:v','3.1','-video_track_timescale','15360',str(leg)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
 with av.open(str(src)) as c:
  for n,f in enumerate(c.decode(video=0)):
   if cfg['encode_start']<=n<cfg['encode_end']:
    if cfg['start']<=n<cfg['end']:
     frame=av.VideoFrame.from_ndarray(render(cfg,n),format='rgb24').reformat(format='yuv420p')
     arr=frame.to_ndarray(format='yuv420p')
    else:arr=f.to_ndarray(format='yuv420p')
    proc.stdin.write(arr.tobytes())
  assert n+1==cfg['frames']
 proc.stdin.close();assert proc.wait()==0;log.close()
 source=av.open(str(src));v=source.streams.video[0];a=source.streams.audio[0]
 replacement=av.open(str(leg));rv=replacement.streams.video[0]
 assert v.time_base==rv.time_base
 assert v.codec_context.extradata==rv.codec_context.extradata,('codec mismatch',v.codec_context.extradata.hex(),rv.codec_context.extradata.hex())
 packets=[];keys=[]
 for p in source.demux(v,a):
  if p.dts is None:continue
  video=p.stream.type=='video';fn=round(p.pts*p.time_base*30) if video else None
  if video and p.is_keyframe:keys.append(fn)
  if video and cfg['encode_start']<=fn<cfg['encode_end']:continue
  packets.append((video,p))
 assert cfg['encode_start'] in keys and cfg['encode_end'] in keys
 count=0;offset=round(Fraction(cfg['encode_start'],30)/v.time_base)
 for p in replacement.demux(rv):
  if p.dts is None:continue
  p.pts+=offset;p.dts+=offset;packets.append((True,p));count+=1
 assert count==cfg['encode_end']-cfg['encode_start']
 packets.sort(key=lambda x:(x[1].dts*x[1].time_base,not x[0]))
 with av.open(str(dst),'w',options={'movflags':'+faststart'}) as o:
  ov=o.add_stream_from_template(v);oa=o.add_stream_from_template(a)
  for video,p in packets:p.stream=ov if video else oa;o.mux(p)
 assert all(sha(p)==h for p,h in protected.items())
 manifest=dict(cfg,source=str(src),candidate=str(dst),candidate_sha256=sha(dst),protected_hashes=protected,scope='Approved supporting shot only; audio/timing/boards/close retained.',audio='Original AAC packet bytes and timestamps remuxed.',source_limitation='Finished approved source; replacement intervals align exactly to existing GOP boundaries. Only new scenes encoded; every unaffected video packet copied.',approval='Owner requested ship them on the three-proposal Build Your Skills review, 2026-10-08; authorizes building and local shipping of these exact changes.',status='Built candidate; verification pending')
 (OUT/f'{slug}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('BUILT',dst,flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--build',choices=list(SOURCES));args=ap.parse_args()
 if args.preview:
  for slug,cfg in SOURCES.items():
   for n in [cfg['start'],*cfg['changes'],cfg['end']-1]:
    Image.fromarray(render(cfg,n)).save(PREVIEW/f'{cfg["id"]}-{n:05}.jpg',quality=96)
 if args.build:build(args.build,SOURCES[args.build])
