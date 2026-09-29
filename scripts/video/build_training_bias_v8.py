#!/usr/bin/env python3
"""Approved visual pacing repair over the SHA-locked live v7. Audio packet copied."""
import argparse, hashlib, json, shutil, subprocess
from pathlib import Path
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from ken_burns_path import draw_ring, hex_bgr, ring_px
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/training-bias-build-2026-09-29-v8'
DEST=ROOT/'Prompts/training-bias-v8.mp4'
LIVE=ROOT/'course-assets/training-bias/training-bias.mp4'
EXPECTED='0423a1b5f34337d130fbb1ff9392fa45ffab98d09426b47da68c8b99bc9917cd'
SOURCE=Path('/private/tmp/training-bias-v7-0423a1b5f343.mp4')
OLD=ROOT/'video-audit/training-bias-comparison-2026-09-21/build-v6'
FPS=30; TOTAL=7830
cv2.setNumThreads(1)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def cap(p): return cv2.VideoCapture(str(p),cv2.CAP_FFMPEG,[cv2.CAP_PROP_N_THREADS,1])
class Reader:
 def __init__(self): self.c=cap(SOURCE); self.n=-1; self.im=None
 def at(self,n):
  assert n>=self.n
  while self.n<n:
   ok,self.im=self.c.read(); assert ok,n; self.n+=1
  return self.im

# Half-open output spans; timeline stays identical to v7.
PATCHES=[
 dict(name='data-shapes-default',start=1980,end=2100,kind='donor',source_start=1482,source_end=1644),
 dict(name='cow-shortcut-callback',start=2490,end=2628,kind='donor',source_start=570,source_end=656),
 dict(name='questions-introduction',start=3368,end=3531,kind='donor',source_start=3366,source_end=3367),
 dict(name='broader-picture-callback',start=4290,end=4458,kind='donor',source_start=3240,source_end=3367),
 dict(name='retrieve-introduction',start=6038,end=6230,kind='diagram',scene='retrieve'),
 dict(name='context-not-retraining',start=6870,end=7178,kind='diagram',scene='context'),
]
BOARDS=[dict(key='skew',start=1670,end=2628,asset='how-bias-happens'),dict(key='questions',start=3531,end=4290,asset='questions-to-ask'),dict(key='rag',start=6230,end=6870,asset='rag')]
ORIG_START={'skew':1670,'questions':3368,'rag':6038}
COL={'ink':'#1b2153','muted':'#596274','purple':'#4f2fc4','blue':'#1652f0','teal':'#0e8f86','gold':'#fff0b5','line':'#deddeb','bg':'#f8f8fc'}
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'; BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
S=2

def diagram(scene,t):
 im=Image.new('RGB',(1280*S,720*S),COL['bg']); d=ImageDraw.Draw(im)
 def box(rect,fill='white',outline=None,r=22,width=2):d.rounded_rectangle(tuple(int(x*S) for x in rect),radius=r*S,fill=fill,outline=outline,width=width*S)
 def text(x,y,s,size=30,color='ink',bold=False,anchor=None):d.text((x*S,y*S),s,font=ImageFont.truetype(BOLD if bold else FONT,size*S),fill=COL.get(color,color),anchor=anchor)
 def arrow(a,b,color='teal'):
  c=COL[color];x,y=a;xx,yy=b;d.line((x*S,y*S,xx*S,yy*S),fill=c,width=4*S)
  if xx!=x:d.polygon([(xx*S,yy*S),((xx-12)*S,(yy-8)*S),((xx-12)*S,(yy+8)*S)],fill=c)
  else:d.polygon([(xx*S,yy*S),((xx-8)*S,(yy-12)*S),((xx+8)*S,(yy-12)*S)],fill=c)
 text(64,58,'LOOKING BEYOND TRAINING' if scene=='retrieve' else 'CONTEXT IS NOT TRAINING',18,'purple',True)
 text(64,103,'AI can retrieve outside information.' if scene=='retrieve' else 'New information. Same trained weights.',42,bold=True)
 if scene=='retrieve':
  for rect,title,subtitle in [((64,245,375,500),'Your question','What do I need to know?'),((484,245,795,500),'Outside sources','Find relevant information'),((904,245,1215,500),'Active context','Material for this answer')]:
   box(rect,outline=COL['line']);text(rect[0]+24,278,title,27,bold=True);text(rect[0]+24,445,subtitle,19,'muted')
  box((92,345,345,410),'#eeebff');text(118,366,'?',32,'purple',True)
  for j in range(3):
   x=510+j*73;box((x,335,x+57,413),'#e5f4f2',r=8)
   for y in [356,369,382]:d.line((int((x+12)*S),y*S,int((x+44)*S),y*S),fill=COL['teal'],width=2*S)
  box((930,336,1190,416),'#eaf0ff',r=10);text(949,359,'Question + sources',22,'blue',True)
  arrow((390,373),(466,373));arrow((810,373),(888,373))
  text(64,587,'Retrieve first. Then use what was found.',28,'muted')
 else:
  box((64,228,570,554),outline=COL['blue']);text(91,255,'Active context',30,'blue',True)
  box((92,315,542,378),'#edf2ff',r=12);text(118,332,'Your question',25,bold=True)
  # On "It just places the material...", reveal the retrieved block in context.
  p=max(0,min(1,(t-5.3)/.75));p=p*p*(3-2*p)
  if p>0:
   y=421+int(22*(1-p));box((92,y,542,y+80),'#dff3ef',r=12);text(118,y+24,'Retrieved information',25,'teal',True)
  else:
   box((92,421,542,501),'#f4f6fb',outline='#e2e6ef',r=12)
  box((686,228,1215,554),outline=COL['purple']);text(714,255,'Model',30,'purple',True)
  box((716,315,1185,458),'#eeebff',r=15);text(950,346,'Trained weights',29,'purple',True,'mt')
  text(950,405,'UNCHANGED',22,'purple',True,'mt')
  text(950,493,'Uses the context to write an answer',22,'muted',False,'mt')
  arrow((590,391),(666,391),'blue')
  arrow((950,560),(950,596),'purple');box((848,605,1052,657),'white',outline=COL['line'],r=12);text(950,619,'Answer',23,bold=True,anchor='mt')
  text(64,604,'More to read for this response.',26,'muted')
 return cv2.cvtColor(np.asarray(im.resize((1280,720),Image.Resampling.LANCZOS)),cv2.COLOR_RGB2BGR)

def board_states(b):
 asset=ROOT/f"course-assets/training-bias/training-bias-{b['asset']}.jpg"
 raw=cv2.imread(str(asset));h,w=raw.shape[:2];assert w==1600 and h<=900
 canvas=np.full((900,1600,3),tuple(int(x) for x in raw[4,4]),np.uint8);oy=(900-h)//2
 # Same canonical asset placement as the original compact board.
 canvas[oy:oy+h]=raw
 spec=json.loads((OLD/f"leg-{b['key']}.json").read_text());base=cv2.resize(canvas,(1280,720),interpolation=cv2.INTER_AREA)
 frames=[base]
 for r in spec['rings']:
  x,y,w,h=r['rect'];t=ring_px();up=4
  pil=Image.fromarray(cv2.cvtColor(base,cv2.COLOR_BGR2RGB)).resize((1280*up,720*up),Image.Resampling.NEAREST)
  pen=ImageDraw.Draw(pil)
  pen.rounded_rectangle(tuple(round(v*up) for v in (x*.8-t,y*.8-t,(x+w)*.8+t,(y+h)*.8+t)),radius=round((r['radius']*.8+t)*up),outline=r['color'],width=t*up)
  im=cv2.cvtColor(np.asarray(pil.resize((1280,720),Image.Resampling.LANCZOS)),cv2.COLOR_RGB2BGR)
  frames.append(im)
 return spec,frames

def setup():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 assert sha(LIVE)==EXPECTED,'Live source changed; do not silently build from a different release.'
 if not SOURCE.exists():shutil.copyfile(LIVE,SOURCE)
 assert sha(SOURCE)==EXPECTED
 protected=[LIVE,ROOT/'lessons/training-bias.md',*sorted((ROOT/'course-assets/training-bias').glob('*.jpg'))]
 old_manifest=json.loads((OLD/'edit-manifest.json').read_text())
 geometry={}
 for b in BOARDS:
  old=old_manifest['boards'][b['key']];assert sha(ROOT/old['asset'])==old['sha256']
  geometry[b['key']]={k:old[k] for k in ['asset','sha256','canvas_offset','states','rings']}
  geometry[b['key']].update(canvas_size=[1600,900],output_scale=.8,stroke_output_px=ring_px(),density='compact')
 m=dict(board_geometry=geometry,scope='Approved visual-only pacing pass; user: Build it please.',source=str(SOURCE),source_sha256=EXPECTED,source_limitation='Raw roll absent. One video re-encode from verified finished v7; AAC copied.',candidate=str(DEST),fps=30,frames=TOTAL,duration=261,patches=PATCHES,boards=BOARDS,protected_hashes={str(p):sha(p) for p in protected},narration_changes=[],pause_changes=[],audio='compressed AAC packet copy',unchanged_chat_frames=[4754,5470],unchanged_close_frames=[7550,7830],preserved_rag_animation=[7178,7550],new_diagram='Code-native diagram rendered by this script; retrieved information enters context while weights remain unchanged.')
 return m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 m=setup();boards={b['key']:board_states(b) for b in BOARDS}
 for scene,ts in [('retrieve',[0,4]),('context',[0,6.5,9.8])]:
  for t in ts:cv2.imwrite(str(OUT/'preview'/f'{scene}-{t}.png'),diagram(scene,t))
 for key,(spec,states) in boards.items():
  for i,im in enumerate(states):cv2.imwrite(str(OUT/'preview'/f'{key}-{i}.jpg'),im)
 # All patch transitions and canonical-board ring changes are declared for output QA.
 bounds={}
 for p in PATCHES:
  bounds[p['start']]=p['name']+'-in';bounds[p['end']]=p['name']+'-out'
 for b in BOARDS:
  bounds[b['start']]=b['key']+'-board-in';bounds[b['end']]=b['key']+'-board-out'
  for r in boards[b['key']][0]['rings']:
   f=ORIG_START[b['key']]+r['start']
   if b['start']<f<b['end'] and not any(p['start']<=f<p['end'] for p in PATCHES):bounds[f]=b['key']+'-ring'
 m['boundaries']=[dict(frame=f,label=l) for f,l in sorted(bounds.items())]
 m['changed_spans']=[[1670,2628],[3368,4458],[6038,7178]]
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
 if args.prepare_only:return
 assert not DEST.exists(),'Never overwrite a review candidate'
 ff=imageio_ffmpeg.get_ffmpeg_exe();cmd=[ff,'-hide_banner','-loglevel','error','-threads','1','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-threads','1','-i',str(SOURCE),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','2','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=(OUT/'encode.log').open('w'))
 src=Reader();donor=None;active=None
 for n in range(TOTAL):
  im=src.at(n);patch=next((p for p in PATCHES if p['start']<=n<p['end']),None)
  if patch:
   if patch['kind']=='donor':
    if active!=patch['name']:
     if donor:donor.c.release()
     donor=Reader();active=patch['name']
    u=(n-patch['start'])/max(1,patch['end']-patch['start']-1)
    f=round(patch['source_start']+u*(patch['source_end']-patch['source_start']-1));im=donor.at(f)
   else: im=diagram(patch['scene'],(n-patch['start'])/FPS)
  else:
   b=next((b for b in BOARDS if b['start']<=n<b['end']),None)
   if b:
    spec,states=boards[b['key']];local=n-ORIG_START[b['key']];idx=next((j+1 for j,r in enumerate(spec['rings']) if r['start']<=local<r['end']),0);im=states[idx]
  proc.stdin.write(im.tobytes())
  if n%900==0:print(f'Rendered {n}/{TOTAL}',flush=True)
 proc.stdin.close();assert proc.wait()==0
 src.c.release()
 if donor:donor.c.release()
 assert all(sha(p)==h for p,h in m['protected_hashes'].items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));print(DEST,flush=True)
if __name__=='__main__':main()
