#!/usr/bin/env python3
"""Approved narrow visual revision. Preserve v2 timing and packet-copy its audio.
The accepted finished master is the visual baseline to preserve all approved
camera/mark-cleanup treatments. Raw rolls remain available, but rebuilding their
unaffected legs would expand this narrow repair. One YUV-preserving video encode.
"""
from pathlib import Path
import hashlib,json,subprocess,sys
import av,cv2,imageio_ffmpeg,numpy as np
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'course-assets/next-level-moves/next-level-moves.mp4'
EXPECTED='bb128f1ddae843fa9f5a32154455adabb0a1d933842c278e38b01996abb7fc1c'
OUT=ROOT/'video-audit/next-level-moves-visual-repair-2026-09-30-v3'
ASSETS=ROOT/'scripts/video/assets/next-level-moves-2026-09-30'
DEST=ROOT/'Prompts/next-level-moves-v3.mp4'
FF=imageio_ffmpeg.get_ffmpeg_exe()
FPS,TOTAL,W,H=30,9206,1280,720
SPANS={'history':(1287,1529),'tutoring':(2100,2310),'profit':(4260,5001),'lawn':(8010,8340)}
BOUNDARIES={f:f'{name}-{side}' for name,(a,b) in SPANS.items() for f,side in [(a,'in'),(b,'out')]}
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
S=2
INK='#1b2153';MUTED='#687487';BG='#f7f8fb';GREEN='#0f7a4a';AMBER='#a9760c';TEAL='#0e8f86'

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def audio_hash(p,decoded=False):
 args=[FF,'-v','error','-i',str(p),'-map','0:a:0']+(['-c:a','pcm_s16le'] if decoded else ['-c:a','copy'])
 return subprocess.check_output(args+['-f','hash','-hash','sha256','-'],text=True).strip()

def ease(x):
 x=max(0,min(1,x));return x*x*(3-2*x)

def photo(im,n,length):
 z=1+.025*ease(n/(length-1));ih,iw=im.shape[:2]
 cw=min(iw,ih*W/H)/z;ch=cw*H/W
 mat=np.float32([[cw/W,0,(iw-cw)/2],[0,ch/H,(ih-ch)/2]])
 return cv2.warpAffine(im,mat,(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)

FONTS={}
def font(size,bold=False):
 key=(size,bold)
 if key not in FONTS:FONTS[key]=ImageFont.truetype(BOLD if bold else FONT,size*S)
 return FONTS[key]

def text(d,xy,s,size=30,color=INK,bold=False,anchor=None):
 d.text(tuple(v*S for v in xy),s,font=font(size,bold),fill=color,anchor=anchor)

def rect(d,box,fill,r=0):
 box=tuple(round(v*S) for v in box)
 if r:d.rounded_rectangle(box,radius=r*S,fill=fill)
 else:d.rectangle(box,fill=fill)

def layer(im,t,onset,paint,fade=.33):
 a=ease((t-onset)/fade)
 if a<=0:return
 lay=Image.new('RGBA',im.size);paint(ImageDraw.Draw(lay))
 if a<1:lay.putalpha(lay.getchannel('A').point(lambda p:round(p*a)))
 im.alpha_composite(lay)

def profit_frame(n):
 # Word cues mapped from roll1-words.json through v2's preceding +4.2 s.
 t=n/FPS
 im=Image.new('RGBA',(W*S,H*S),BG);d=ImageDraw.Draw(im)
 text(d,(80,51),'THE LAWN-MOWING EXAMPLE',21,MUTED,True)
 text(d,(80,90),'Where the money goes',49,INK,True)
 # A single open equation stage, not a new course-card layout.
 for x,label in [(242,'Sales'),(642,'Costs'),(1042,'Profit')]:text(d,(x,205),label,29,MUTED,True,'mm')
 text(d,(442,297),'−',56,MUTED,False,'mm');text(d,(842,297),'=',54,MUTED,False,'mm')
 for x,label in [(242,'Money in'),(642,'Every cost'),(1042,'Money left')]:text(d,(x,294),label,32,MUTED,False,'mm')
 # Units appear on the actual narrated figures; the resulting $300 at its cue.
 layer(im,t,148.68,lambda q:text(q,(242,374),'10 lawns × $30',25,INK,False,'mm'))
 def sales(q):
  rect(q,(120,247,364,344),BG);text(q,(242,294),'$300',72,INK,True,'mm')
  rect(q,(80,506,1200,550),'#e1e6ef',12)
  rect(q,(80,506,80+1120*ease((t-152.44)/.65),550),INK,12)
  text(q,(80,568),'$300 collected from customers',25,INK)
 layer(im,t,152.44,sales)
 layer(im,t,153.68,lambda q:text(q,(642,363),'3 friends × $40',25,AMBER,False,'mm'))
 layer(im,t,156.94,lambda q:text(q,(642,398),'$120 labor',28,AMBER,True,'mm'))
 layer(im,t,158.70,lambda q:text(q,(642,433),'+ $30 gas & supplies',25,AMBER,False,'mm'))
 def costs(q):
  rect(q,(520,247,764,344),BG);text(q,(642,294),'$150',72,AMBER,True,'mm')
  # 120 and 30 represent the two actual expense amounts, out of 300 sales.
  rect(q,(80,506,528,550),AMBER,12);rect(q,(516,506,528,550),AMBER);rect(q,(528,506,640,550),'#d4aa50')
  rect(q,(80,562,1200,612),BG)
  text(q,(304,581),'Labor $120',24,AMBER,True,'mm')
  text(q,(586,623),'Supplies $30',23,AMBER,False,'mm')
 layer(im,t,162.68,costs)
 def result(q):
  rect(q,(910,247,1174,344),BG);text(q,(1042,294),'$150',72,GREEN,True,'mm')
  text(q,(1042,374),'Money left over',25,GREEN,False,'mm')
  rect(q,(640,506,1200,550),GREEN,12);rect(q,(640,506,653,550),GREEN)
  text(q,(920,581),'Profit $150',24,GREEN,True,'mm')
 layer(im,t,164.78,result)
 return cv2.cvtColor(np.asarray(im.convert('RGB').resize((W,H),Image.Resampling.LANCZOS)),cv2.COLOR_RGB2BGR)

def expected_frame(name,n,photos):
 a,b=SPANS[name]
 return profit_frame(n) if name=='profit' else photo(photos[name],n-a,b-a)

def main():
 cv2.setNumThreads(2);OUT.mkdir(exist_ok=True);(OUT/'render-preview').mkdir(exist_ok=True)
 assert not DEST.exists(),'Never overwrite a review candidate.'
 assert sha(SOURCE)==EXPECTED
 photos={k:cv2.imread(str(ASSETS/f'{k}.png')) for k in ['history','tutoring','lawn']}
 assert all(v is not None for v in photos.values())
 protected={str(p):sha(p) for p in [SOURCE,ROOT/'lessons/next-level-moves.md',*sorted((ROOT/'course-assets/next-level-moves').glob('*.jpg'))]}
 proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','yuv420p','-s','1280x720','-r','30','-i','pipe:0','-i',str(SOURCE),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-profile:v','high','-level:v','3.1','-crf','15','-preset','fast','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 wants={x for f in BOUNDARIES for x in [f-1,f,f+15]}|{round(t*30) for t in [145,149.5,153,157.5,160.5,163.5,166,270]}|{TOTAL-1}
 count=0
 with av.open(str(SOURCE)) as c:
  c.streams.video[0].codec_context.thread_count=2
  for n,frame in enumerate(c.decode(video=0)):
   assert frame.format.name=='yuv420p' and (frame.width,frame.height)==(W,H)
   raw=frame.to_ndarray(format='yuv420p')
   which=next((k for k,(a,b) in SPANS.items() if a<=n<b),None)
   if which:
    raw=av.VideoFrame.from_ndarray(expected_frame(which,n,photos),format='bgr24').to_ndarray(format='yuv420p')
   if n in wants:cv2.imwrite(str(OUT/'render-preview'/f'{n:06d}.jpg'),av.VideoFrame.from_ndarray(raw,format='yuv420p').to_ndarray(format='bgr24'))
   proc.stdin.write(raw.tobytes());count+=1
   if count%1500==0:print(f'Rendered {count}/{TOTAL}',flush=True)
 proc.stdin.close();assert proc.wait()==0 and count==TOTAL
 assert audio_hash(SOURCE)==audio_hash(DEST)
 assert audio_hash(SOURCE,True)==audio_hash(DEST,True)
 assert all(sha(p)==h for p,h in protected.items())
 m=dict(scope='Narrow visual revision approved by user: Build please',candidate=str(DEST),source=str(SOURCE),source_sha256=EXPECTED,candidate_sha256=sha(DEST),fps=FPS,total_frames=TOTAL,duration=TOTAL/FPS,
 source_note='Accepted finished v2 master retained as narrow-repair baseline; raw rolls exist. One extra video encode, planar YUV preserved on unaffected frames; audio stream copied.',
 changed_spans={k:dict(frames=[a,b],seconds=[a/FPS,b/FPS]) for k,(a,b) in SPANS.items()},boundaries=[dict(frame=f,label=s) for f,s in BOUNDARIES.items()],
 asset_hashes={p.name:sha(p) for p in ASSETS.glob('*.png')},image_generation='Built-in image_gen; prompts.json alongside assets',narration_changes=[],added_pauses=[],audio_packets_identical=True,decoded_audio_identical=True,protected_hashes=protected,protected_files_unchanged=True,
 profit_reveal_cues={'example':148.68,'sales_300':152.44,'labor_3x40':153.68,'labor_120':156.94,'supplies_30':158.70,'costs_150':162.68,'profit_150':164.78},
 board_runs={'summer':[15-0.033333,95.633333-77],'profit':[142-123.466667,175.5-166.7],'college':[24.2],'iteration':[267-251.466667,296.066667-278]},longest_board_run_seconds=24.2,longest_board_run_exception='College conversation retained as approved.',
 listening='No new audio edits; whole-file listening remains unperformed.',status='Review candidate; not installed or published')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('COMPLETE',DEST,flush=True)

if __name__=='__main__':main()
