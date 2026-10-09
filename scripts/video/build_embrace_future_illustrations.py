#!/usr/bin/env python3
"""Approved Learning Illustration Pass. Replace three shots; retain source AAC and untouched GOPs."""
from pathlib import Path
import argparse,json,hashlib,subprocess
from fractions import Fraction
import av,cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/embrace-the-future-illustration-updates-2026-10-08'
ASSETS=OUT/'assets';PREVIEW=OUT/'previews';FF=imageio_ffmpeg.get_ffmpeg_exe()
FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
SOURCES={
'rise-of-agents':dict(id='P1',source_version=7,version=8,sha='c7377765375cf8092f1ef45a4c76b6db8513d287edd556835f9a2a2f95eb03b4',frames=5112,start=3369,end=3633,encode_start=3369,encode_end=3869,changes=[3487,3512],crf=16),
'data-centers':dict(id='P2',source_version=5,version=6,sha='ce5dc2cf8d75bf50740dcf79476d4c5db022ab3bb7060f3e209187fd325dd284',frames=6694,start=2122,end=2244,encode_start=2122,encode_end=2244,changes=[],crf=18),
'work-changes':dict(id='P3',source_version=5,version=6,sha='e6794cd9de7a220298ed996d143aad45eef721b63468309492e73096fbbf085f',frames=9848,start=9316,end=9611,encode_start=9316,encode_end=9611,changes=[9416,9480],crf=16)}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(n):return ImageFont.truetype(str(FONT),n)
def text(d,xy,s,n=32,fill='#203335'):d.text(xy,s,font=font(n),fill=fill)
def photo(name):return Image.open(ASSETS/(name+'.png')).convert('RGB')
def project(base,overlay,points,transparent=False):
 arr=np.array(base);w,h=base.size;ow,oh=overlay.size
 H=cv2.getPerspectiveTransform(np.float32([(0,0),(ow-1,0),(ow-1,oh-1),(0,oh-1)]),np.float32(points))
 rgba=np.array(overlay.convert('RGBA'));warped=cv2.warpPerspective(rgba[:,:,:3],H,(w,h),flags=cv2.INTER_CUBIC)
 mask=cv2.warpPerspective(rgba[:,:,3],H,(w,h)).astype(float)[:,:,None]/255
 return Image.fromarray(np.uint8(np.clip(warped*mask+arr*(1-mask),0,255)))
def editor(state):
 im=Image.new('RGB',(1000,640),'#142332');d=ImageDraw.Draw(im)
 text(d,(32,18),'Friday highlights',38,'white')
 im.paste(ImageOps.fit(photo('basketball'),(936,330),method=Image.Resampling.LANCZOS,centering=(0.5,0)),(32,78));d=ImageDraw.Draw(im)
 for j in range(8):
  x=32+j*117;d.rectangle((x,429,x+109,470),fill='#36596d' if j!=3 else '#73b9b0')
 d.line((450,418,450,480),fill='white',width=4)
 text(d,(32,497),'CAPTION',22,'#9db6c6')
 text(d,(32,544),'30 points on Friday.' if state==2 else 'Friday highlights',48,'#9de2cf' if state==2 else 'white')
 return im

def agents(state):
 base=photo('agents');w,h=base.size
 # Exact screen quad measured on the generated photograph.
 pts=np.float32([(1001,141),(1484,215),(1415,553),(937,442)])*np.float32([w/1672,h/941])
 im=project(base,editor(state),pts).resize((1280,720),Image.Resampling.LANCZOS)
 d=ImageDraw.Draw(im);d.rounded_rectangle((28,456,623,683),radius=16,fill='#f5f8f6')
 text(d,(52,476),'CAPTION',22,'#526568')
 text(d,(52,516),'Friday highlights',34,'#526568' if state==2 else '#203335')
 if state==2:
  d.line((52,542,337,542),fill='#74817d',width=2)
  d.rounded_rectangle((43,564,607,666),radius=10,outline='#137d77',width=4)
  text(d,(61,594),'30 points on Friday.',37,'#137d77')
 else:
  text(d,(52,593),'Review the reel and caption.',25,'#526568')
  if state==1:d.rounded_rectangle((42,509,605,569),radius=10,outline='#137d77',width=4)
 return im

def working(state,large=True):
 im=Image.new('RGBA',(600,560),(249,247,238,255) if large else (0,0,0,0));d=ImageDraw.Draw(im)
 if large:
  for y in range(122,550,47):d.line((25,y,575,y),fill='#dedfd7',width=1)
 text(d,(30,20),['FIRST ATTEMPT','CHECK THE STEP','REVISE AND CHECK'][state] if large else '',25,'#526568')
 text(d,(30,75),'3(x + 2) = 15',46)
 text(d,(30,149),'3x + 2 = 15',41,'#526568' if state==2 else '#203335')
 if state:
  d.line((28,180,331,180),fill='#aa5b3a',width=3)
  text(d,(30,219),'3 × 2 = 6',36,'#a35b27')
 if state>=2:
  text(d,(30,295),'3x + 6 = 15',43,'#137d77')
  text(d,(30,362),'3x = 9',41,'#137d77')
  text(d,(30,427),'x = 3',44,'#137d77')
  text(d,(30,502),'Check: 3(3 + 2) = 15',28,'#137d77')
 return im

def study(state):
 im=photo('study_before' if state==0 else 'study');w,h=im.size
 # Keep typesetting on the visible left part of the notebook, clear of the pencil hand.
 pts=np.float32([(760,756),(993,663),(1138,810),(978,875)])*np.float32([w/1672,h/941])
 im=project(im,working(state,False),pts).resize((1280,720),Image.Resampling.LANCZOS)
 # Magnified notebook excerpt: exact same working, readable at delivery resolution.
 page=working(state).resize((420,392),Image.Resampling.LANCZOS)
 im.paste(page,(25,299));d=ImageDraw.Draw(im)
 d.rectangle((25,299,445,691),outline='#d7d8cb',width=2)
 return im
CACHE={('P1',i):agents(i) for i in range(3)}
CACHE.update({('P3',i):study(i) for i in range(3)})
CACHE['P2',0]=photo('facility').resize((1280,720),Image.Resampling.LANCZOS)
def state_at(cfg,n):return sum(n>=f for f in cfg['changes'])
def render(cfg,n):
 im=CACHE[cfg['id'],state_at(cfg,n)]
 if cfg['id']=='P2':
  t=(n-cfg['start'])/(cfg['end']-cfg['start']-1);scale=1+0.025*t
  w,h=im.size;cw,ch=w/scale,h/scale
  im=im.crop(((w-cw)/2,(h-ch)/2,(w+cw)/2,(h+ch)/2)).resize((w,h),Image.Resampling.LANCZOS)
 return np.array(im)
def paths(slug,cfg):return ROOT/f'course-assets/{slug}/{slug}.mp4',ROOT/f'Prompts/{slug}-v{cfg["version"]}.mp4'
def build(slug,cfg):
 src,dst=paths(slug,cfg);assert sha(src)==cfg['sha'];assert not dst.exists(),dst
 protected={str(p):sha(p) for p in [src,ROOT/f'lessons/{slug}.md',*sorted(src.parent.glob('*.jpg'))]}
 leg=OUT/f'{slug}-leg.mp4';log=(OUT/f'{slug}-encode.log').open('w')
 cmd=[FF,'-v','error','-y','-f','rawvideo','-pixel_format','yuv420p','-video_size','1280x720','-framerate','30','-i','-', '-an','-c:v','libx264','-threads','2','-preset',('medium' if cfg['id']=='P2' else 'fast'),'-crf',str(cfg['crf']),'-profile:v','high','-level:v','3.1','-video_track_timescale','15360',str(leg)]
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
 manifest=dict(cfg,source=str(src),candidate=str(dst),candidate_sha256=sha(dst),protected_hashes=protected,scope='Approved supporting shot only; audio/timing/boards/close retained.',audio='Original AAC packet bytes and timestamps remuxed.',source_limitation='Finished approved source; one reencode only for the intersecting GOPs. All other video packets copied.',approval='Owner agreed to the three-proposal review on 2026-10-08.',status='Review candidate; not installed or shipped')
 (OUT/f'{slug}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('BUILT',dst,flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--build',choices=list(SOURCES));args=ap.parse_args()
 if args.preview:
  for (pid,state),im in CACHE.items():im.save(PREVIEW/f'{pid}-state-{state}.jpg',quality=96)
 if args.build:build(args.build,SOURCES[args.build])
