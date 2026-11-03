#!/usr/bin/env python3
"""Approved roll-8 repair with two roll-6 passages; review candidate, not installed."""
from pathlib import Path
import sys,json,subprocess,argparse
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
from editspec_build import Build,Reader,fr,sha,readwav,writewav,SPF,SR
from build_creative_thinking_v8 import BoardRenderer
from gemini_mark import clean_frame,glyph_mask
from make_close_board import close_board_asset,compose_canonical_for_video
from ken_burns_path import smoothstep
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/when-you-need-more-build-v7-2026-11-03'
DEST=ROOT/'Prompts/when-you-need-more-v7.mp4'
A=ROOT/'course-assets/when-you-need-more';FF=imageio_ffmpeg.get_ffmpeg_exe()
S={n:ROOT/f'Prompts/when-you-need-more-{n}.mp4' for n in [6,7,8,9]}
HASH={6:'dcc1e98c74e2240e71a4c473e63586f112add731a490b995ad57e300fcc32031',7:'92bee671a535e622201245e082bc82c784eadda9c6bf123fb4c70644b8e8242f',8:'08045f766b6f1f805460162f5464c40286a1820d084df7b1f6ff8c9ac5d082ea',9:'500dfab3d7399f4ecdd6bb439abd5416f65d8529972a722a71c307712db42774'}
FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
FONTS={n:ImageFont.truetype(str(FONT),n) for n in [17,18,20,22,24,26,28,30,34,38]}

def prepare():
 assert not DEST.exists(),'Never overwrite a candidate'
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 for n,p in S.items():assert sha(p)==HASH[n],p
 b=Build(ROOT,S[8],OUT,DEST,protected=[S[6],S[7],S[9],*A.glob('*.jpg'),A/'when-you-need-more.mp4',ROOT/'lessons/when-you-need-more.md'])
 b.tall_margin=False
 audio={}
 for n in [6,8]:
  wav=OUT/f'roll-{n}.wav'
  if not wav.exists():subprocess.run([FF,'-v','error','-i',str(S[n]),'-vn','-ar',str(SR),'-ac','1','-c:a','pcm_s16le',str(wav)],check=True)
  audio[n]=readwav(wav)
 pieces=[];timeline=[];cursor=0
 for n,a,z,gain,label in [(8,0,61.75,0,'opening and model'),(8,69.08,78.72,0,'model versus thinking'),(6,114.60,159.05,1.0,'complete thinking passage'),(8,108.15,133.48,0,'research intro and regular chat'),(6,219.50,239.60,1.0,'report and physics comparison'),(8,155.17,160.1333333,0,'two-line close')]:
  s,e=fr(a),fr(z);x=audio[n][s*SPF:e*SPF].copy()*10**(gain/20)
  timeline.append(dict(roll=n,source_start=s,source_end=e,start_frame=cursor,end_frame=cursor+e-s,gain_db=gain,label=label));pieces.append(x);cursor+=e-s
 close=timeline[-1]['start_frame'];tail=max(0,230-(cursor-close))
 seed=audio[8][round(78.55*SR):round(78.65*SR)].copy();seed-=seed.mean();loop=np.r_[seed,seed[::-1]]
 # Five-ms ramps only at real audio cuts. Uninterrupted speech is untouched.
 for i,x in enumerate(pieces):
  tone=np.resize(loop,len(x));r=np.linspace(0,1,240)
  if i:x[:240]=x[:240]*r+tone[:240]*(1-r)
  x[-240:]=x[-240:]*(1-r)+tone[-240:]*r
 pieces.append(np.resize(loop,tail*SPF));timeline.append(dict(kind='room_tone',start_frame=cursor,end_frame=cursor+tail,label='standard close settling tail'));cursor+=tail
 joined=np.concatenate(pieces);assert np.abs(joined).max()<32767
 writewav(OUT/'edited.wav',joined)
 def ot(n,t):
  sf=fr(t)
  for r in timeline:
   if r.get('roll')==n and r['source_start']<=sf<r['source_end']:return r['start_frame']+sf-r['source_start']
  raise ValueError((n,t))
 model=(fr(46.1),timeline[0]['end_frame']);think=(ot(6,121.84),timeline[2]['end_frame']);research=(ot(8,123.8),timeline[4]['end_frame'])
 # Measured canonical card bounds and inset example regions; all unchanged JPGs.
 configs=[('model','choose-tool',model,914,[(48.12,0,False),(50.12,0,True),(52.90,1,False),(55.50,1,True)],8,700),('thinking','thinking',think,996,[(125.14,0,False),(132.84,0,True),(138.08,1,False),(150.52,1,True)],6,784),('research','research',research,1037,[(126.48,0,False),(127.76,0,True),(220.02,1,False),(226.54,1,True)],None,743)]
 for key,asset,(start,end),bottom,events,roll,example_y in configs:
  targets=[]
  for t,side,example in events:
   n=roll or (8 if side==0 else 6);x0,x1=(40,784) if side==0 else (816,1560)
   rect=[x0+24,example_y,x1-24,bottom-24] if example else [x0,118,x1,bottom]
   targets.append(dict(label=('left' if side==0 else 'right')+(' example' if example else ' complete card'),at=ot(n,t)/30,rects=[rect],color=['#4f2fc4','#1652f0'][side],radius=14))
  b.board(key,A/f'when-you-need-more-{asset}.jpg',start,end,'compact',targets,push=False,min_open=0 if key=='model' else 60)
 compose_canonical_for_video(close_board_asset('choosemodel'),OUT/'close.png','#ffffff')
 visuals=[]
 def v(a,z,label,kind='source',roll=8,sa=None,se=None,patch=None):
  assert not visuals or visuals[-1]['end_frame']==a,(a,visuals[-1])
  visuals.append(dict(start_frame=a,end_frame=z,label=label,kind=kind,roll=roll,source_start=fr(sa) if sa is not None else a,source_end=fr(se) if se is not None else z,patch=patch))
 v(0,fr(6.1),'drawn conversation phone',roll=7,sa=0,se=5.9333)
 v(fr(6.1),fr(15.2),'plan options sources with simplified labels',sa=7.8,se=15.25,patch='tasks')
 v(fr(15.2),fr(23.5),'optional three-choice overview','overview')
 v(fr(23.5),fr(29.1666667),'drawn phone and optional switches')
 v(fr(29.1666667),model[0],'app LLM and answer animation with repaired labels',sa=29.8,se=46.1,patch='app')
 v(*model,'Which Model','model')
 v(model[1],timeline[2]['start_frame'],'hourglass thinking bridge',roll=9,sa=108.933333,se=115.5)
 v(timeline[2]['start_frame'],think[0],'clock and nonhuman thinking distinction',roll=7,sa=81.0666667,se=88.3)
 v(*think,'How Much Thinking','thinking')
 r0=think[1];r1=r0+fr(8.3)
 v(r0,r1,'drawn documents and web network',roll=8,sa=147.0,se=155.3)
 v(r1,research[0],'web lookup drawing',roll=7,sa=129.1,se=136.7)
 v(*research,'How Much Research','research')
 v(close,cursor,'standard close','close')
 m=dict(output=str(DEST),frames=cursor,duration=cursor/30,fps=30,audio_timeline=timeline,visual_timeline=visuals,boards=b.boards,close=dict(start_frame=close,prehold=48,push=150,settle=32),protected_hashes=b.hashes,source_hashes=HASH,narration_approval='User: Build it please, after the roll-8 repair recommendation. Minor opening paraphrases accepted with that plan.',added_instructional_pause_frames=0,added_closing_tail_frames=tail,donor_gain_db=1.0,donor_loudness='roll 8 -20.19 LUFS; roll 6 -21.30 LUFS measured on comparable speech',audio_peak_dbfs=float(20*np.log10(np.abs(joined).max()/32768)),listening='Direct listening unavailable; join cadence and voice continuity require user audition.',longest_unbroken_board_seconds=(think[1]-think[0])/30)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 return m

def patch_frame(im,which,sf):
 pic=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(pic);t=sf/30
 def box(rect,txt,size=22,bg='#f7faf7',ink='#295264'):
  d.rectangle(rect,fill=bg);x0,y0,x1,y1=rect;d.multiline_text(((x0+x1)/2,(y0+y1)/2),txt,font=FONTS[size],fill=ink,anchor='mm',align='center',spacing=8)
 if which=='tasks':
  box((485,91,797,123),'When a task asks more',20,bg='#fffdfc')
  box((175,232,424,273),'A complicated plan',22)
  for r,txt in [((199,299,397,332),'Steps'),((199,370,397,405),'Constraints'),((199,442,397,475),'Schedule')]:box(r,txt,20,bg='#e3eff0')
  if t>=8.8:
   box((518,231,765,273),'Weigh options',22)
   box((550,309,730,338),'Option A',20,bg='#f0f3ee');box((550,432,730,462),'Option B',20,bg='#f5eeeb')
  if t>=9.3:
   box((855,231,1111,273),'Compare sources',22)
   for r,txt in [((860,306,927,334),'Site 1'),((951,306,1016,334),'Site 2'),((1040,306,1106,334),'Site 3')]:box(r,txt,17,bg='#fffdf6')
   box((901,458,1068,494),'Bring it together',18,bg='#3e7086',ink='white')
  # These are separate task examples, not a compulsory workflow.
  box((445,391,489,419),'',18);box((789,391,835,419),'',18)
 elif which=='app':
  box((440,100,1107,159),'',30,bg='#fcfdfb')
  d.line((440,157,1117,157),fill='#a3cbd0',width=1)
  d.text((640,128),'AI app',font=FONTS[30],fill='#295264',anchor='mm')
  if t>=31.5:box((249,198,529,229),'Your question',24)
  if t>=33.3:
   # Repair the entire menu overlap, then retain the source network's native motion.
   d.rectangle((635,158,1108,612),fill='#fcfdfb')
   panel_bg=tuple(int(v) for v in im[325,665,::-1])
   d.rounded_rectangle((640,184,1091,599),radius=35,fill=panel_bg,outline='#4d92a1',width=2)
   pic.paste(Image.fromarray(cv2.cvtColor(im[320:495,660:1070],cv2.COLOR_BGR2RGB)),(660,320))
   d.text((865,248),'LLM',font=FONTS[30],fill='#b8e0e7',anchor='mm')
   if t>=37:
    d.multiline_text((865,540),'Different models,\ndifferent capabilities',font=FONTS[22],fill='#b8e0e7',anchor='mm',align='center',spacing=8)
  if t>=35:
   box((229,360,530,466),'An answer\nfrom the model',24,bg='#fbfdfb')
 return cv2.cvtColor(np.array(pic),cv2.COLOR_RGB2BGR)

def overview(bg,f):
 pic=Image.fromarray(cv2.cvtColor(bg,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(pic)
 d.text((640,135),'Depending on your app and subscription',font=FONTS[30],fill='#293e4b',anchor='mm')
 names=[('Model','Which LLM'),('Thinking','Time on the task'),('Research','Compare sources')]
 for i,(name,sub) in enumerate(names):
  x=115+i*355;col=['#4f2fc4','#1652f0','#0e8f86'][i]
  d.rounded_rectangle((x,265,x+330,485),radius=24,fill='#ffffff',outline=col,width=3)
  d.text((x+165,345),name,font=FONTS[38],fill=col,anchor='mm');d.text((x+165,411),sub,font=FONTS[22],fill='#35434e',anchor='mm')
 return cv2.cvtColor(np.array(pic),cv2.COLOR_RGB2BGR)

class Pictures:
 def __init__(self,m):
  self.m=m;self.boards={k:BoardRenderer(OUT/f'leg-{k}.json') for k in m['boards']};self.close=cv2.imread(str(OUT/'close.png'));self.mask=glyph_mask();self.counts={'clone':0,'inpaint':0,'declined':0};self.rd=None;self.rowid=None
  rd=Reader(S[8]);self.bg=rd.at(0);rd.c.release();self.bg,_=clean_frame(self.bg,self.mask)
 def frame(self,row,f):
  kind=row['kind'];j=f-row['start_frame'];n=row['end_frame']-row['start_frame']
  if kind in self.boards:return self.boards[kind].frame(f-self.m['boards'][kind]['src_in'])
  if kind=='overview':return overview(self.bg,f)
  if kind=='close':
   z=1+.2*smoothstep(float(np.clip((j-48)/149,0,1)));h,w=self.close.shape[:2];ww=w/z;hh=ww*9/16
   return cv2.warpAffine(self.close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  if self.rowid!=row['start_frame']:
   if self.rd:self.rd.c.release()
   self.rd=Reader(S[row['roll']]);self.rowid=row['start_frame']
  sf=row['source_start']+round(j*(row['source_end']-row['source_start']-1)/max(1,n-1));im=self.rd.at(sf)
  im,how=clean_frame(im,self.mask);self.counts[how or 'declined']+=1
  if row['patch']:im=patch_frame(im,row['patch'],sf)
  return im

def render(m,preview=False):
 p=Pictures(m)
 if preview:
  for row in m['visual_timeline']:
   for f in [row['start_frame'],(row['start_frame']+row['end_frame'])//2,row['end_frame']-1]:cv2.imwrite(str(OUT/'preview'/f'frame-{f:05}.jpg'),p.frame(row,f))
  return
 assert not DEST.exists()
 proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','17','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for row in m['visual_timeline']:
  for f in range(row['start_frame'],row['end_frame']):
   im=p.frame(row,f);proc.stdin.write(im.tobytes())
   if f%240==0:cv2.imwrite(str(OUT/'preview'/f'output-{f:05}.jpg'),im)
  print(row['end_frame'],m['frames'],row['label'],flush=True)
 proc.stdin.close();assert proc.wait()==0
 m.update(candidate_sha256=sha(DEST),corner_cleaning=p.counts,protected_unchanged={k:sha(k)==v for k,v in m['protected_hashes'].items()})
 assert all(m['protected_unchanged'].values());assert p.counts['declined']==0
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('BUILT',DEST,flush=True)
if __name__=='__main__':
 cv2.setNumThreads(2);ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--render-prepared',action='store_true');args=ap.parse_args()
 m=json.loads((OUT/'edit-manifest.json').read_text()) if args.render_prepared else prepare();render(m,args.preview)
