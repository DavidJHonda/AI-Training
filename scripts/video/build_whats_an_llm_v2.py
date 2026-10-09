#!/usr/bin/env python3
"""Approved roll-2 build with whole-sentence donors and number-free explanatory motion."""
from pathlib import Path
import json,subprocess,sys,wave,math
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
from editspec_build import Build,Reader,sha,fr,readwav,writewav,SPF
from build_creative_thinking_v8 import BoardRenderer
from make_close_board import close_board_asset,compose_canonical_for_video
from gemini_mark import clean_frame,glyph_mask
from ken_burns_path import smoothstep
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/whats-an-llm-build-2026-10-09-v2'
DEST=ROOT/'Prompts/whats-an-llm-v2.mp4'
SRC={n:ROOT/f'Prompts/whats-an-llm-{n}.mp4' for n in (1,2,3)}
EXPECTED={1:'17dd7671b8dd5711a0a10d6235b5aa1938a11e44a3d73ddf9ed7f93a4b3bc997',2:'6e04134d507bb9352cf70fadc436e203812f4b22dd8800c17aa6ec446d7bd1d2',3:'36745eedb15e40835c09d04d1abddf0c205913359b1dd67582d5ed24fd592a41'}
FF=imageio_ffmpeg.get_ffmpeg_exe();FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
# Frame-aligned, measured silent cuts; no new pauses. base[718:847] replaced by roll3[949:1133].
AUDIO=[(2,0,718,0,'Base opening'),(3,949,1133,-.2,'Complete Language definition'),(2,847,2031,0,'Base through time example'),(1,2681,2748,-.4,'Better late than → never'),(2,2031,4570,0,'Base remainder and close')]
def om(f):
 assert not 718<f<847,f
 return f+(55 if f>=847 else 0)+(67 if f>=2031 else 0)
def tm(s):return om(fr(s))/30

def prepare():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 for n,p in SRC.items():assert sha(p)==EXPECTED[n],p
 protected=list((ROOT/'course-assets/whats-an-llm').glob('*.jpg'))+[ROOT/'course-assets/whats-an-llm/whats-an-llm.mp4']
 b=Build(ROOT,SRC[2],OUT,DEST,protected=protected+[SRC[1],SRC[3]])
 audio={}
 for n,p in SRC.items():
  wav=OUT/f'roll-{n}.wav'
  if not wav.exists():subprocess.run([FF,'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000',str(wav)],check=True)
  audio[n]=readwav(wav)
 rows=[];parts=[];cursor=0;cut_levels=[]
 for i,(n,s,e,gain,label) in enumerate(AUDIO):
  a=audio[n][s*SPF:e*SPF].copy()*10**(gain/20)
  for f in (s,e):
   if f==0 or f*SPF>=len(audio[n]):continue
   v=audio[n][f*SPF-480:f*SPF+480]/32768
   cut_levels.append(dict(roll=n,frame=f,dbfs=float(20*np.log10(max(1e-10,np.sqrt(np.mean(v*v)))))))
  # Crossfade only 5 ms at graft joins, all inside measured silence.
  if i:a[:240]*=np.linspace(0,1,240)
  if i<len(AUDIO)-1:a[-240:]*=np.linspace(1,0,240)
  parts.append(a);rows.append(dict(roll=n,source=str(SRC[n]),source_start=s,source_end=e,start_frame=cursor,end_frame=cursor+e-s,gain_db=gain,label=label));cursor+=e-s
 writewav(OUT/'edited.wav',np.concatenate(parts));assert cursor==4692
 def board(key,start,end,asset,targets):
  b.board(key,ROOT/f'course-assets/whats-an-llm/whats-an-llm-{asset}.jpg',om(start),om(end),'compact',targets,push=False)
 def target(label,t,rect,color):return dict(label=label,at=t,rects=[rect],color=color,radius=18)
 board('definition',510,1084,'llm',[
  target('Large',tm(19.72),(40,127,525,689),'#1652f0'),
  target('Language', (718+fr(31.90)-949)/30,(558,127,1042,689),'#0e8f86'),
  target('Model',tm(28.88),(1075,127,1559,689),'#4f2fc4'),
  target('App / engine',tm(32.42),(40,728,1560,818),'#6e51ff')])
 board('familiar',1423,1675,'patterns',[target('One Familiar Pattern',tm(51.46),(40,127,780,864),'#4f2fc4')])
 board('everywhere',1788,2040,'patterns',[target('Patterns Are Everywhere',tm(62.44),(821,127,1560,864),'#0e8f86')])
 board('loop',3218,3778,'one-word-at-a-time',[
  target('Jelly',tm(110.38),(40,158,486,455),'#4f2fc4'),
  target('For',tm(115.8),(577,158,1024,455),'#4f2fc4'),
  target('Lunch',tm(118.0),(1114,158,1560,455),'#4f2fc4'),
  target('Repeat',tm(121.66),(40,493,1560,581),'#6e51ff')])
 specs=[(0,220,'source','Opening devices'),(220,510,'app','App and underlying model'),(510,1084,'definition','Definition board'),(1084,1423,'training','Training before use'),(1423,1675,'familiar','Jelly pattern'),(1675,1788,'source','Human familiarity / trained model'),(1788,2040,'everywhere','Star, time, never'),(2040,2388,'broader','Patterns beyond phrases'),(2388,2958,'context','Learned patterns and changed input'),(2958,3052,'source','Drawn phone'),(3052,3218,'phone','Tap and next suggestion'),(3218,3778,'loop','Canonical next-word loop'),(3778,4281,'growing','Growing context and alternative continuations'),(4281,4570,'close','Canonical close')]
 timeline=[dict(start_frame=om(s),end_frame=om(e),base_start=s,base_end=e,visual=v,label=lab) for s,e,v,lab in specs]
 assert all(x['end_frame']==y['start_frame'] for x,y in zip(timeline,timeline[1:]))
 compose_canonical_for_video(close_board_asset('aihistory'),OUT/'close.png','#ffffff')
 boundaries={r['start_frame']:r['label'] for r in timeline[1:]}
 for r in rows[1:]:boundaries.setdefault(r['start_frame'],r['label'])
 m=dict(candidate=str(DEST),fps=30,total_frames=cursor,duration=cursor/30,sources={str(p):EXPECTED[n] for n,p in SRC.items()},audio=rows,timeline=timeline,boards=b.boards,boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],cut_levels=cut_levels,protected_hashes=b.hashes,close=dict(start_frame=om(4281),hold_frames=48,push_frames=150,zoom=1.2,settled_frames=289-198),scope='Owner-approved full production of roll 2, two whole-sentence grafts, canonical boards, corrected supporting scenes; review candidate only.',optional_cut='Mental-library sentence retained; optional cut was not necessary.',listening='Not auditioned: direct audio perception unavailable. Graft wording and levels checked; final audible review remains required.')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 return b,{k:BoardRenderer(OUT/f'leg-{k}.json') for k in b.boards},m

# Purpose-built process visuals: few words, animated relationships, no probabilities or token mechanics.
BG='#f6f5f1';INK='#252a3b';MUTED='#647181';PURPLE='#6544bd';TEAL='#148d84';LINE='#cad2dc'
fonts={s:ImageFont.truetype(str(FONT),s) for s in (20,24,26,28,30,32,36,42,48,56)}
def canvas(label):
 im=Image.new('RGB',(1280,720),BG);d=ImageDraw.Draw(im)
 d.text((70,56),label,font=fonts[24],fill=MUTED);return im,d
def text(d,xy,s,size=32,color=INK,anchor=None):d.text(xy,s,font=fonts[size],fill=color,anchor=anchor)
def box(d,rect,s,accent=PURPLE,size=32,fill='white'):
 d.rounded_rectangle(rect,radius=20,fill=fill,outline=accent,width=3)
 x0,y0,x1,y1=rect;d.multiline_text(((x0+x1)/2,(y0+y1)/2),s,font=fonts[size],fill=INK,anchor='mm',align='center',spacing=12)
def arrow(d,a,z,color=TEAL,progress=1):
 end=(a[0]+(z[0]-a[0])*progress,a[1]+(z[1]-a[1])*progress);d.line([a,end],fill=color,width=4)
 theta=math.atan2(z[1]-a[1],z[0]-a[0]);p1=(end[0]-14*math.cos(theta-.45),end[1]-14*math.sin(theta-.45));p2=(end[0]-14*math.cos(theta+.45),end[1]-14*math.sin(theta+.45));d.polygon([end,p1,p2],fill=color)
def progress(t,start,dur=.65):return smoothstep(float(np.clip((t-start)/dur,0,1)))
def source_time(f):
 if f<718:return f/30
 if f<902:return 24.8
 if f<2086:return (f-55)/30
 if f<2153:return 67.8
 return (f-122)/30

def diagram(kind,t):
 if kind=='app':
  im,d=canvas('The app and the model')
  d.rounded_rectangle((85,190,555,495),radius=24,fill='white',outline=LINE,width=3)
  d.rounded_rectangle((115,226,410,283),radius=15,fill='#e8e2f6');text(d,(138,238),'Your question',28)
  d.rounded_rectangle((195,321,520,379),radius=15,fill='#dceee9');text(d,(216,333),'An answer',28)
  text(d,(320,548),'The app',36,anchor='mm')
  if t>=10.18:
   arrow(d,(575,343),(730,343),progress=progress(t,10.18));box(d,(760,240,1180,450),'Large Language\nModel',TEAL,36);text(d,(970,548),'LLM',36,TEAL,anchor='mm')
 elif kind=='training':
  im,d=canvas('Before you ask a question')
  for i,y in enumerate([210,252,294]):
   x=110+i*42;d.rounded_rectangle((x,y,x+230,y+210),radius=8,fill='white',outline=LINE,width=2)
   for j in range(5):d.line((x+25,y+38+j*27,x+175-(j%2)*30,y+38+j*27),fill='#aab6c2',width=4)
  text(d,(250,580),'Many examples',32,anchor='mm')
  arrow(d,(475,374),(740,374),progress=progress(t,38))
  box(d,(775,254,1160,490),'Learned\npatterns',TEAL,42)
  text(d,(970,580),'Training',32,anchor='mm')
 elif kind=='broader':
  im,d=canvas('Patterns go beyond familiar phrases')
  # Documents are examples of language uses, not a recreated course board.
  labels=['Explain an idea','Solve a problem','Write code','Spelling patterns']
  subs=['Because…\nFor example…','First…\nThen…','if ready:\n    begin()','receive\nrecieve']
  for i in range(4):
   if t<[68,75,76.5,78][i]:continue
   x=65+i*304;d.rounded_rectangle((x,220,x+266,522),radius=12,fill='white',outline=LINE,width=2)
   d.rectangle((x+20,240,x+25,310),fill=[PURPLE,TEAL,PURPLE,TEAL][i]);text(d,(x+42,274),str(i+1),30,MUTED)
   d.multiline_text((x+24,353),subs[i],font=fonts[28],fill=INK,spacing=20)
   text(d,(x+133,569),labels[i],24,anchor='mm')
 elif kind=='context':
  if t<90.22:
   im,d=canvas('Building an answer')
   box(d,(75,220,500,340),'Words already there',PURPLE,30)
   box(d,(75,440,500,560),'Learned patterns',TEAL,30)
   arrow(d,(525,280),(770,376),progress=progress(t,82));arrow(d,(525,500),(770,404),progress=progress(t,82))
   if t>=85:box(d,(795,312,1195,470),'A likely next word',PURPLE,30)
   if t>=87:text(d,(640,635),'Choose a word. Add it. Repeat.',32,anchor='mm')
  else:
   im,d=canvas('The words already there change what might come next')
   text(d,(90,238),'Peanut butter and…',36)
   if t>=94.3:arrow(d,(750,264),(910,264));box(d,(940,214,1190,318),'jelly',PURPLE,36)
   if t>=95.78:
    text(d,(90,430),'Peanut butter and banana…',36);d.line((473,484,652,484),fill=TEAL,width=4)
   if t>=97.6:arrow(d,(750,456),(910,456));box(d,(940,407,1190,510),'sandwich',TEAL,36)
 elif kind=='phone':
  im,d=canvas('A familiar version: predictive text')
  d.rounded_rectangle((255,145,1025,634),radius=34,fill='#252a3b');d.rounded_rectangle((278,167,1002,610),radius=20,fill='white')
  added=t>=103.4;text(d,(320,240),'I want to buy peanut butter and'+(' jelly' if added else ''),26)
  choices=['for','with','today'] if added else ['jelly','honey','banana']
  for i,w in enumerate(choices):
   rect=(319+i*215,356,514+i*215,429);box(d,rect,w,TEAL if i==0 else LINE,28,fill='#dceee9' if i==0 else BG)
  if not added:d.ellipse((387,439,419,471),fill=TEAL)
  for row in range(2):
   for col in range(10):d.rounded_rectangle((316+col*64,490+row*43,368+col*64,522+row*43),radius=5,fill='#e7e9ee')
 elif kind=='growing':
  if t<137.86:
   im,d=canvas('Each new word becomes part of the next input')
   added=t>=128.5
   box(d,(80,180,1195,300),'The curious cat'+(' jumped' if added else ''),PURPLE,36)
   arrow(d,(640,325),(640,405),progress=progress(t,126.2))
   box(d,(405,435,875,535),'Predict the next word',TEAL,30)
   if t>=129.5:
    arrow(d,(890,485),(1158,485));arrow(d,(1158,485),(1158,320));text(d,(640,627),'Add the word, then use the updated sentence.',28,anchor='mm')
  else:
   im,d=canvas('Same starting text. Different possible answers.')
   box(d,(75,282,570,418),'The curious cat jumped…',PURPLE,30)
   for y,s in [(227,'onto the couch'),(490,'over the fence')]:
    arrow(d,(598,350),(820,y),progress=progress(t,138.3 if y==227 else 139.4));
    if t>=(138.3 if y==227 else 139.4):box(d,(846,y-52,1210,y+52),s,TEAL,30)
 else:raise ValueError(kind)
 return cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)

def frame(f,r,b,boards,reader,close,counts):
 v=r['visual']
 if v in boards:return boards[v].frame(f-r['start_frame'])
 if v=='close':
  n=f-r['start_frame'];z=1+.2*smoothstep(float(np.clip((n-48)/149,0,1)));h,w=close.shape[:2];ww=w/z;hh=ww*9/16
  return cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
 if v=='source':
  sf=r['base_start']+f-r['start_frame'];im=reader.at(sf);im,how=clean_frame(im,glyph_mask());counts[how]=counts.get(how,0)+1;return im
 return diagram(v,source_time(f))

def render(preview=False):
 cv2.setNumThreads(2);b,boards,m=prepare();close=cv2.imread(str(OUT/'close.png'));reader=Reader(SRC[2]);counts={}
 if preview:
  for key,br in boards.items():
   wants=[0]+[x['start']+3 for x in br.spec['rings']]
   for n in wants:cv2.imwrite(str(OUT/'preview'/f'{key}-{n}.jpg'),br.frame(n))
  for v,t in [('app',15),('training',44),('broader',78.8),('context',86),('context',98),('phone',105),('growing',133),('growing',141)]:cv2.imwrite(str(OUT/'preview'/f'{v}-{t}.jpg'),diagram(v,t))
  return
 assert not DEST.exists(),'Never overwrite a candidate'
 log=open(OUT/'encode.log','w');p=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','17','-preset','fast','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-metadata','title=What’s an LLM?','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE,stderr=log)
 try:
  for r in m['timeline']:
   for f in range(r['start_frame'],r['end_frame']):
    im=frame(f,r,b,boards,reader,close,counts)
    if f%180==0:cv2.imwrite(str(OUT/'preview'/f'output-{f:05}.jpg'),im)
    p.stdin.write(im.tobytes())
   print(r['end_frame'],r['label'],flush=True)
 finally:p.stdin.close();reader.c.release()
 assert p.wait()==0;log.close()
 m['corner_cleanup']=counts;m['candidate_sha256']=sha(DEST);m['protected_unchanged']={p:sha(p)==h for p,h in b.hashes.items()};assert all(m['protected_unchanged'].values());(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('COMPLETE',DEST,flush=True)
if __name__=='__main__':render('--preview' in sys.argv)
