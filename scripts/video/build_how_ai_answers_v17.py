#!/usr/bin/env python3
"""Approved roll-2 edit: preserve motion, repair context, trim three asides.

All times are pristine source times. Review candidate only; no course install.
"""
from pathlib import Path
import argparse, functools, json, subprocess
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from editspec_build import Reader, sha
from build_embeddings_v7 import Renderer
from make_close_board import compose_canonical_for_video
from gemini_mark import clean_frame, glyph_mask

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/how-ai-answers-2.mp4'
DEST=ROOT/'Prompts/how-ai-answers-v19.mp4'
OUT=ROOT/'video-audit/how-ai-answers-motion-v19-2026-11-10'
EXPECTED='009393ffb3e9fbcae7e0ffd463527ebee3014e7bbf712af953a09f5733d16820'
FPS=30; SR=48000; SPF=1600
CUTS=[(1602,1908),(3071,3393),(3855,4281)]
KEEP=[(0,1602),(1908,3071),(3393,3855),(4281,5715)]
MAP=[f for a,b in KEEP for f in range(a,b)]
TOTAL=len(MAP)
INK='#141126'; BLUE='#1652f0'; PURPLE='#4f2fc4'; TEAL='#0e8f86'
FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
QUESTION='What should I name my new dog?'
ASSETS={
 'before':ROOT/'course-assets/how-ai-answers/how-ai-answers-before-answer-begins.jpg',
 'context':ROOT/'course-assets/how-ai-answers/how-ai-answers-same-token-context.jpg',
 'close':ROOT/'course-assets/how-ai-answers/how-ai-answers-close.jpg',
 **{n:ROOT/f'gemini-notebook/how-ai-answers/assets/how-ai-answers-{n}.jpg' for n in ['first-prediction','you-selected','name-prediction','spot-selected']}}
BOUNDARIES=[150,357,496,1101,1602,1916,2082,2691,3071,3393,3855,4281,4851,5152,5436,5457]

def oframe(f):
 for a,b in KEEP:
  if a<=f<b:return sum(z-x for x,z in KEEP if z<=a)+f-a
 # A removed source frame at a splice maps to the start of its surviving successor.
 return sum(b-a for a,b in KEEP if b<=f)

@functools.lru_cache(None)
def font(size,weight=600):
 f=ImageFont.truetype(str(FONT),size);f.set_variation_by_axes([weight]);return f

def text(im,s,xy,size=30,color=INK,weight=600,anchor=None):
 d=ImageDraw.Draw(im);d.text(xy,s,font=font(size,weight),fill=color,anchor=anchor)

def rr(im,box,fill='white',outline=None,width=2,r=16):
 ImageDraw.Draw(im).rounded_rectangle(tuple(map(round,box)),radius=r,fill=fill,outline=outline,width=width)

def bgr(im):return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)
def pil(im):return Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
def ease(v):v=np.clip(v,0,1);return v*v*(3-2*v)

def blank():return Image.new('RGB',(1280,720),'white')

def ring(im,box,color=BLUE):
 # Draw at 2x so a four-pixel stroke retains a clean antialiased edge.
 overlay=Image.new('RGBA',(2560,1440));d=ImageDraw.Draw(overlay)
 d.rounded_rectangle(tuple(round(v*2) for v in box),radius=22,outline=color,width=8)
 im.alpha_composite(overlay.resize((1280,720),Image.Resampling.LANCZOS))

def header(im,title):text(im,title,(80,46),38,INK,800)
def question(im,y=125):
 text(im,'You',(80,y),24,BLUE,700)
 text(im,QUESTION,(245,y-4),30,INK,650)

def opening(t,rd):
 if t<5:
  # Hold the intact drawing through the native fade into the replaced prompt scene.
  im,method=clean_frame(rd.at(min(round(t*30),120)),glyph_mask());assert method
  return im
 if t<11.9:
  im=blank();text(im,'How does the answer begin?',(640,120),40,INK,800,'mm')
  rr(im,(100,270,820,420),outline=TEAL)
  text(im,'Your question',(130,293),22,TEAL,700)
  text(im,QUESTION,(130,340),30,INK,650)
  if t>=7.2:
   p=ease((t-7.2)/.65);x=round(955+40*(1-p))
   rr(im,(x,270,x+210,420),outline=PURPLE)
   text(im,'First answer',(x+105,315),24,PURPLE,700,'mm')
   text(im,'token',(x+105,350),24,PURPLE,700,'mm')
   ImageDraw.Draw(im).line((845,345,x-25,345),fill=TEAL,width=4)
   ImageDraw.Draw(im).polygon([(x-25,345),(x-38,337),(x-38,353)],fill=TEAL)
  return bgr(im)
 # Keep the source's staggered word reveals, removing only title/sub-label noise.
 raw,method=clean_frame(rd.at(round(t*30)),glyph_mask());assert method;im=pil(raw)
 # Clone clean paper from the same frame over the original heading.
 im.paste(im.crop((0,520,1280,655)).resize((1280,270)),(0,0))
 text(im,'Tokens',(640,205),40,INK,800,'mm')
 # Inpaint each small T-index inside its own tile; borders and words stay intact.
 a=bgr(im);mask=np.zeros(a.shape[:2],np.uint8)
 for cx in [272,400,507,596,713,821,927,1026]:mask[376:415,cx-23:cx+23]=255
 a=cv2.inpaint(a,mask,4,cv2.INPAINT_TELEA)
 # Remove the late technical caption without touching the moving token tiles.
 a[445:515,200:1080]=a[550:620,200:1080]
 return a

def vector_bridge(t):
 im=blank();header(im,'From your question to the first token')
 text(im,QUESTION,(80,160),36,INK,700)
 rr(im,(120,350,215,450),PURPLE,r=15);text(im,'?',(167,399),48,'white',800,'mm')
 text(im,'Last token',(167,490),22,PURPLE,650,'mm')
 p=ease((t-64.35)/1.8)
 # The changing position makes the vector-to-prediction handoff visible.
 vx=350+300*p
 text(im,'Updated vector',(vx+80,295),24,TEAL,700,'mm')
 for k,h in enumerate([53,89,38,110,70]):
  x=vx+k*34;rr(im,(x,455-h,x+21,455),TEAL,r=7)
 if t>=65.2:
  rr(im,(870,275,1200,510),outline='#d8d1f2')
  text(im,'Possible next tokens',(1035,312),23,INK,700,'mm')
  for j,w in enumerate(['You','A','Great']):
   if t>=65.45+j*.5:text(im,w,(890,345+j*47),30,PURPLE,700)
 return bgr(im)

def loop_time(t):
 # Measured first visible frames: source 117.167,120.500,123.833.
 # Map each ~0.5s native reveal onto its spoken word, preserving the transitions.
 return float(np.interp(t,LOOP_AUDIO,LOOP_PICTURE))

LOOP_AUDIO=[113.1,119.68,120.08,122.00,122.38,123.28,123.82,125.6,128.5]
LOOP_PICTURE=[116.4,117.1,117.65,120.433,121.0,123.766,124.333,125.6,126.1]

def loop(t,rd):
 raw=rd.at(round(loop_time(t)*30))
 # Work on the original moving token strip and vector, not a still recreation.
 raw[181:212,230:1050]=(252,252,252)
 # Find the dark vector box beneath the row and replace its jargon label.
 mask=(raw[315:570,:,0]<90)&(raw[315:570,:,1]<100)&(raw[315:570,:,2]<100)
 contours,_=cv2.findContours(mask.astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 for c in contours:
  x,y,w,h=cv2.boundingRect(c);y+=315
  if w>200 and h>65:
   col=tuple(int(v) for v in raw[y+15,x+12,::-1]);p=pil(raw)
   rr(p,(x+8,y+4,x+w-8,y+29),col,r=0)
   text(p,'Updated vector',(x+w/2,y+16),18,'#7be4e5',650,'mm');raw=bgr(p)
 # All useful motion fits in this crop; technical headers and the engine mark do not.
 crop=raw[175:530,195:1085]
 im=blank();header(im,'Building the answer');question(im)
 text(im,'AI’s Answer',(80,215),24,BLUE,700)
 im.paste(pil(cv2.resize(crop,(1120,447),interpolation=cv2.INTER_CUBIC)),(80,255))
 return bgr(im)

def finish(t,rd):
 if t>=181.2:
  im=blank();question(im,235);text(im,'AI’s Answer',(80,355),24,BLUE,700)
  text(im,'You could name him Spot.',(245,350),36,INK,700);return bgr(im)
 # Preserve the source's period reveal, shifted to the spoken word.
 st=float(np.interp(t,[171.733,175.8,176.32,177.0,178.0,180.9,181.2],
                      [173.05,174.4,175.05,177.4,179.5,180.4,180.4]))
 raw=rd.at(round(st*30));im=blank();header(im,'Finishing the answer');question(im)
 text(im,'AI’s Answer',(80,220),24,BLUE,700)
 # Preserve the original tiles, omitting their index labels and EOS tile.
 # The row shifts left when EOS arrives; use its actual border contours.
 hsv=cv2.cvtColor(raw,cv2.COLOR_BGR2HSV)
 m=cv2.inRange(hsv,np.array([75,65,80]),np.array([105,255,255]));m[:200]=0;m[335:]=0
 cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 boxes=sorted([cv2.boundingRect(c) for c in cs if cv2.boundingRect(c)[2]>55 and cv2.boundingRect(c)[3]>65])
 # Stable five words plus the source's fading period. Crop individually to separate EOS.
 for j,(x,y,w,h) in enumerate(boxes[:6]):
  tile=pil(raw[y:y+h,x:x+w]);d=ImageDraw.Draw(tile)
  d.rectangle((6,7,w-7,32),fill=(252,252,252))
  if j==5:d.rectangle((6,h-32,w-7,h-7),fill=(252,252,252))
  tile=tile.resize((145,145),Image.Resampling.LANCZOS)
  im.paste(tile,(80+j*160,285))
 if t>=177.72:
  p=ease((t-177.72)/.5);y=round(520+20*(1-p))
  rr(im,(400,y,880,y+90),'#232d32',outline='#a9760c',width=3)
  text(im,'End-of-answer token',(640,y+45),28,'#ffce70',700,'mm')
 return bgr(im)

def setup():
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 specs={};renderers={}
 for key,start,end in [('before',496,1101),('context',1101,1916)]:
  a=cv2.imread(str(ASSETS[key]));h,w=a.shape[:2]
  cw=max(w,round(h*16/9));ch=round(cw*9/16);canvas=np.full((ch,cw,3),(250,249,250),np.uint8)
  ox=(cw-w)//2;oy=(ch-h)//2;canvas[oy:oy+h,ox:ox+w]=a
  path=OUT/f'{key}-canvas.png';cv2.imwrite(str(path),canvas)
  rings=[]
  if key=='before':
   for i,(s,e,color) in enumerate([(21.72,23.62,PURPLE),(23.62,25.28,BLUE),(25.28,27.56,TEAL),(27.56,35.74,'#0f7a4a')]):
    rings.append(dict(start=round(s*30)-start,end=round(e*30)-start,rect=[ox+64+i*368,oy+310,362,537],color=color,pad=0,radius=15))
  else:
   for s,e,x in [(39.24,46.94,40),(46.94,53.4,816)]:rings.append(dict(start=round(s*30)-start,end=round(e*30)-start,rect=[ox+x,oy+118,744,398],color=PURPLE,pad=0,radius=15))
  spec=dict(image=str(path),fps=30,out_w=1280,out_h=720,upscale=1,
    beats=[dict(label='Full current board',frames=end-start,**{'from':[cw/2,ch/2,cw]},to=[cw/2,ch/2,cw])],rings=rings)
  specs[key]=spec;renderers[key]=Renderer(spec)
  (OUT/f'{key}-spec.json').write_text(json.dumps(spec,indent=2))
 close=OUT/'close-canvas.png';compose_canonical_for_video(ASSETS['close'],close,'#ffffff')
 spec=dict(image=str(close),fps=30,out_w=1280,out_h=720,upscale=1,rings=[],beats=[
  dict(label='Full close',frames=48,**{'from':[1920,1080,3840]},to=[1920,1080,3840]),
  dict(label='Push',frames=150,to=[1920,1080,3200]),
  dict(label='Settle',frames=5715-5457-198,to=[1920,1080,3200])])
 renderers['close']=Renderer(spec);specs['close']=spec
 imgs={k:Image.open(p).convert('RGBA') for k,p in ASSETS.items() if k not in ['before','context','close']}
 return renderers,imgs,specs

def chart(t,imgs):
 key='first-prediction' if t<89.67 else 'you-selected' if t<113 else 'name-prediction' if t<161.667 else 'spot-selected'
 im=imgs[key].copy()
 cues=[(76.58,78.30,0),(78.30,80.74,1),(80.74,82.2,2),(82.2,88.8,3),
       (153.28,154.86,0),(154.86,156.96,1),(156.96,158.88,2),(158.88,161.64,3)]
 for a,b,row in cues:
  if a<=t<b:
   ring(im,[106,286+108*row,1174,382+108*row] if row<3 else [98,615,440,655])
 if 96.54<=t<101.9:ring(im,[263,145,355,201],PURPLE)
 return bgr(im.convert('RGB'))

def render(s,rd,renderers,imgs):
 t=s/30
 if s<496:return opening(t,rd)
 if s<1101:return renderers['before'].at(s-496)[0]
 if s<1916:return renderers['context'].at(s-1101)[0]
 if s<2082:return vector_bridge(t)
 if s<3071:return chart(t,imgs)
 if s<3855:return loop(t,rd)
 if s<5152:return chart(t,imgs)
 if s<5457:return finish(t,rd)
 return renderers['close'].at(s-5457)[0]

def audio():
 p=OUT/'source.f32'
 if not p.exists():subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(SRC),'-vn','-ar','48000','-ac','1','-f','f32le',str(p)],check=True)
 src=np.fromfile(p,np.float32);parts=[src[a*SPF:b*SPF].copy() for a,b in KEEP]
 # Five-ms ramps only at the three silence-to-silence cut seams. No new pauses.
 for j in range(len(parts)-1):
  parts[j][-240:]*=np.linspace(1,0,240);parts[j+1][:240]*=np.linspace(0,1,240)
 a=np.concatenate(parts);assert len(a)==TOTAL*SPF;a.tofile(OUT/'edited.f32')
 return [dict(source_frames=list(c),output_frame=oframe(c[0])) for c in CUTS]

def main():
 global OUT,DEST
 ap=argparse.ArgumentParser();ap.add_argument('--preview-only',action='store_true');ap.add_argument('--version',type=int,default=19);args=ap.parse_args()
 OUT=ROOT/f'video-audit/how-ai-answers-motion-v{args.version}-2026-11-10'
 DEST=ROOT/f'Prompts/how-ai-answers-v{args.version}.mp4'
 assert not DEST.exists(),'Choose a new version; preserve existing candidates and their evidence'
 assert sha(SRC)==EXPECTED
 renderers,imgs,specs=setup()
 protected={str(p):sha(p) for p in [SRC,ROOT/'index.html',ROOT/'lessons/how-ai-answers.md',ROOT/'course-assets/how-ai-answers/how-ai-answers.mp4',*ASSETS.values()]}
 samples=[0,120,270,420,490,550,680,740,790,885,1180,1410,1550,1950,2020,2100,2300,2370,2440,2570,2800,2950,3400,3570,3600,3675,3720,3800,4350,4620,4700,4820,4900,5200,5295,5355,5420,5445,5500,5714]
 rd=Reader(SRC)
 for s in samples:
  im=render(s,rd,renderers,imgs);cv2.imwrite(str(OUT/'preview'/f'{oframe(s):05d}-s{s}.png'),im)
 rd.c.release()
 cuts=audio()
 manifest=dict(source=str(SRC),source_sha256=EXPECTED,candidate=str(DEST),fps=30,frames=TOTAL,duration_seconds=TOTAL/30,
  keep_source_frames=KEEP,cuts=cuts,boundaries=sorted(set(oframe(f) for f in BOUNDARIES if 0<oframe(f)<TOTAL)),
  assets={k:dict(path=str(v),sha256=sha(v)) for k,v in ASSETS.items()},protected=protected,
  scope='Approved preservation-first roll-2 build; three narration cuts, repaired motion and exact current course boards.',
  loop_retime=dict(output_source_seconds=LOOP_AUDIO,picture_source_seconds=LOOP_PICTURE),
  added_pause_seconds=0,board_specs=specs,listening_performed=False,continuous_playback_performed=False,publication='Review candidate only')
 (OUT/'edit-plan.json').write_text(json.dumps(manifest,indent=2))
 if args.preview_only:return
 assert not DEST.exists(),'Never overwrite a review candidate'
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
  '-f','f32le','-ar','48000','-ac','1','-i',str(OUT/'edited.f32'),'-map','0:v','-map','1:a',
  '-c:v','libx264','-threads','4','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 rd=Reader(SRC)
 for n,s in enumerate(MAP):
  proc.stdin.write(render(s,rd,renderers,imgs).tobytes())
  if n%600==599:print(f'Rendered {n+1}/{TOTAL}',flush=True)
 proc.stdin.close();assert proc.wait()==0;rd.c.release()
 assert all(sha(Path(p))==v for p,v in protected.items())
 manifest['candidate_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2))
 print(DEST,flush=True)

if __name__=='__main__':main()
