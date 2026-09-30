#!/usr/bin/env python3
"""Approved visual-only pacing pass, current finished source; all audio copied.
Native animated interface cutaways; source animation retained under clearer labels.
"""
from pathlib import Path
import hashlib,json,subprocess,sys,math
import av,cv2,imageio_ffmpeg,numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'course-assets/curious-and-flexible/curious-and-flexible.mp4'
OUT=ROOT/'video-audit/curious-and-flexible-build-2026-09-30-v6'
ASSETS=ROOT/'scripts/video/assets/curious-flexible-cutaways-2026-09-30'
DEST=ROOT/'Prompts/curious-and-flexible-v6.mp4'
EXPECTED='3764e14eecdd6efe6a6e1fa94eb1ef860659dab444337590fa9205884cf76126'
FF=imageio_ffmpeg.get_ffmpeg_exe();N=6376;W,H=1280,720
CUTS=[(2220,2340,'feature'),(2880,3090,'source'),(4170,4380,'need'),(4620,4770,'familiar'),(5010,5160,'compare'),(3426,3662,'newsletter')]
CHANGED=sorted([(1105,1285,'chat-cleanup'),*CUTS,(5569,6073,'diagram-labels')])
BOUNDARIES={f:f'{name}-{side}' for a,b,name in CHANGED for f,side in [(a,'in'),(b,'out')]}
FONT='/System/Library/Fonts/Supplemental/Arial.ttf';BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
NAVY='#1b2153';PURPLE='#4f2fc4';BLUE='#1652f0';TEAL='#0e8f86';GOLD='#f2cf5b';MUTED='#687088'
fonts={}
def ft(n,b=False):
 k=(n,b)
 if k not in fonts:fonts[k]=ImageFont.truetype(BOLD if b else FONT,n)
 return fonts[k]
def txt(d,xy,t,size=24,color=NAVY,b=False,anchor=None):d.text(xy,t,font=ft(size,b),fill=color,anchor=anchor)
def box(d,r,fill='white',outline=None,radius=18,width=2):d.rounded_rectangle(r,radius=radius,fill=fill,outline=outline,width=width)
def line(d,a,b,c='#dce0ec',w=2):d.line([a,b],fill=c,width=w)
def check(d,x,y,color=TEAL):d.line([(x,y+7),(x+7,y+14),(x+23,y-6)],fill=color,width=4)
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def audio_hash(p,decoded=False):
 cmd=[FF,'-v','error','-i',str(p),'-map','0:a:0','-c:a','pcm_s16le' if decoded else 'copy','-f','hash','-hash','sha256','-']
 return subprocess.check_output(cmd,text=True).strip()
def canvas(title,sub):
 im=Image.new('RGB',(W,H),'#f4f2fb');d=ImageDraw.Draw(im)
 d.rectangle((0,0,W,8),fill=PURPLE)
 txt(d,(64,45),title,40,b=True);txt(d,(66,98),sub,23,MUTED)
 box(d,(58,150,1228,675),'#e4e2ed',radius=25);box(d,(52,143,1222,668),'white',radius=25)
 return im

def browser(d,title):
 box(d,(88,175,1187,232),'#f0f1f7',radius=13)
 for i,c in enumerate(['#c1b7ef','#c1cceb','#b8dcd4']):d.ellipse((108+i*23,195,119+i*23,206),fill=c)
 txt(d,(202,187),title,24,b=True)

def arrow(d,x0,y,x1,c=PURPLE):
 line(d,(x0,y),(x1,y),c,4);d.polygon([(x1,y),(x1-12,y-8),(x1-12,y+8)],fill=c)

def sheet(d,x,y,w,title,tag):
 box(d,(x+4,y+5,x+w+4,y+264),'#e8eaf2',radius=15)
 box(d,(x,y,x+w,y+259),'#fafbff',outline='#d8dce9',radius=15)
 txt(d,(x+23,y+20),title,25,b=True)
 box(d,(x+23,y+61,x+w-23,y+97),'#e9e4ff',radius=8);txt(d,(x+36,y+65),tag,20,PURPLE,b=True)
 for j,t in enumerate(['Describe the cell membrane.','Explain the nucleus’s role.','Compare two cell types.']):
  txt(d,(x+24,y+119+j*36),f'{j+1}. {t}',19,MUTED)

BASE={}
def ui(name,n,total):
 t=n/30
 if name not in BASE:
  titles={'feature':('Notice a new ability','A familiar tool gains a new way to help.'),'source':('One reliable source','Check occasionally. Keep the useful changes.'),'need':('Start with work you actually do','A new feature needs a real job.'),'familiar':('Use a task you already know','Same material. Same request. A fair comparison.'),'compare':('Newer does not mean better','Compare the work, then decide.'),'newsletter':('Let useful changes come to you','One source. An occasional check.')}
  im=canvas(*titles[name]);d=ImageDraw.Draw(im)
  if name=='feature':
   browser(d,'AI workspace')
   box(d,(88,252,356,623),'#f5f3fb',radius=15);txt(d,(110,277),'Your recent work',22,b=True)
   for j,s in enumerate(['Class notes','Practice questions','Project outline']):
    box(d,(108,320+j*76,335,378+j*76),'white',radius=9);txt(d,(124,337+j*76),s,20)
   txt(d,(395,272),'What would you like to work on?',28,b=True)
   box(d,(396,333,1151,455),'#f9faff',outline='#d9dfed',radius=13)
   txt(d,(419,357),'Help me study from these notes.',26)
   txt(d,(421,405),'Ask a question...',22,MUTED)
   box(d,(396,487,697,567),'#f3f1fa',radius=13);txt(d,(420,513),'Type a question',25)
  elif name in ('source','newsletter'):
   browser(d,'Inbox')
   box(d,(89,254,329,623),'#f6f4fb',radius=14)
   txt(d,(117,280),'Inbox',28,b=True);txt(d,(117,337),'Saved',23,MUTED);txt(d,(117,389),'Later',23,MUTED)
   txt(d,(117,558),'One good source',19,PURPLE,b=True)
   txt(d,(365,266),'Weekly AI Updates',31,b=True)
   txt(d,(365,312),'A source you trust',21,MUTED)
   line(d,(365,354),(1146,354))
   for j,(a,b) in enumerate([('What changed','A useful new capability'),('Where to try it','Official release notes'),('Worth your time?','See whether it fits your work')]):
    y=378+j*78;d.ellipse((366,y+7,377,y+18),fill=TEAL)
    txt(d,(395,y),a,24,b=True);txt(d,(395,y+32),b,21,MUTED)
  elif name=='need':
   browser(d,'Study session')
   sheet(d,105,281,432,'Cell biology notes','Tomorrow’s quiz')
   txt(d,(577,275),'A task you already have',27,b=True)
   box(d,(577,329,1153,441),'#eee9ff',radius=17)
   txt(d,(600,347),'Turn these notes into',26,PURPLE,b=True)
   txt(d,(600,383),'practice questions.',26,PURPLE,b=True)
   txt(d,(577,483),'AI works from your notes',23,MUTED)
  elif name=='familiar':
   browser(d,'Compare on familiar work')
   sheet(d,113,276,427,'Completed assignment','Cell biology')
   sheet(d,733,276,427,'Try the new feature','The same assignment')
   arrow(d,578,408,692)
   txt(d,(636,340),'SAME',19,PURPLE,True,'mm');txt(d,(636,366),'TASK',19,PURPLE,True,'mm')
   txt(d,(128,579),'You know what a good result looks like.',28,b=True)
  elif name=='compare':
   browser(d,'Review the results')
   for x,title in [(109,'Current approach'),(657,'New approach')]:
    box(d,(x,263,x+511,400),'#f7f7fc',outline='#dde0eb',radius=14);txt(d,(x+25,283),title,26,b=True)
    txt(d,(x+25,329),'The same assignment',22,MUTED)
    snippet = 'Controls what enters and leaves.' if x==109 else 'Manages movement into and out.'
    txt(d,(x+25,366),snippet,21)
   labels=['Quality','Time','Effort','Reliability']
   for j,label in enumerate(labels):
    x=109+j*278;box(d,(x,445,x+252,548),'#f4f2fb',radius=15);txt(d,(x+126,474),label,26,NAVY,True,'mm')
   txt(d,(640,593),'Which works better for this task?',28,NAVY,True,'mm')
  BASE[name]=im
 im=BASE[name].copy();d=ImageDraw.Draw(im)
 if name=='feature':
  q=ease((t-.4)/.7)
  x=728;box(d,(x,487,1151,567),'#e8e1ff',outline=PURPLE,width=3,radius=13)
  txt(d,(x+24,513),'Ask about a file',25,PURPLE,True)
  box(d,(1034,458,1139,495),GOLD,radius=12);txt(d,(1087,476),'NEW',19,NAVY,True,'mm')
  # A visible attachment appears after the newly revealed feature.
  if t>.9:
   box(d,(747,587,1138,630),'#f6f3ff',radius=9);txt(d,(764,596),'Attached: class-notes.pdf',21,PURPLE)
  # Deliberate cursor motion shows which control changed.
  cx=round(1100-130*q);cy=round(610-57*q)
  d.polygon([(cx,cy),(cx,cy+28),(cx+8,cy+20),(cx+19,cy+32),(cx+25,cy+26),(cx+14,cy+15),(cx+26,cy+14)],fill=NAVY)
 elif name in ('source','newsletter'):
  y=378+min(2,int(t/2.0))*78
  d.rounded_rectangle((351,y-9,1164,y+68),radius=12,outline=TEAL,width=3)
  if t>2.1:
   box(d,(990,263,1153,313),'#e6f5ee',radius=12);check(d,1006,283);txt(d,(1041,275),'Saved',22,TEAL,True)
 elif name=='need':
  if t>.6:
   q=ease((t-.6)/1.0)
   box(d,(577,531,1153,606),'#e8f5ef',radius=13)
   txt(d,(603,553),'Practice set from your class notes',24,TEAL,True)
   d.line([(601,594),(601+int(522*q),594)],fill=TEAL,width=4)
 elif name=='familiar':
  if t>1.0:check(d,497,491)
  if t>2.0:check(d,1117,491)
 elif name=='compare':
  j=min(3,int(t/.95));x=109+j*278
  d.rounded_rectangle((x,445,x+252,548),radius=15,outline=PURPLE,width=3)
  txt(d,(x+126,516),'Compare',19,PURPLE,False,'mm')
 return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)

# Local video overlays change labels while leaving source moving dots, arrows,
# pulses and method tiles in place. They are not replacement still frames.
def diagram(frame,n):
 im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(im)
 # Wait for the source's own reveal rather than drawing on its opening paper.
 if np.count_nonzero(cv2.cvtColor(frame[205:240,190:340],cv2.COLOR_BGR2GRAY)<160)<100:return frame
 def label(rect,text,size=23,b=False):
  x0,y0,x1,y1=rect
  # Native panel paper, sampled away from printed pixels.
  sample=frame[y0:y1,x0:x1]
  color=tuple(int(v) for v in np.percentile(sample.reshape(-1,3),75,axis=0)[::-1])
  d.rectangle(rect,fill=color);txt(d,((x0+x1)/2,(y0+y1)/2),text,size,NAVY,b,'mm')
 label((164,249,379,279),'Find possibilities',23)
 label((517,249,767,279),'Test what helps',23)
 label((916,249,1124,279),'Keep what works',23)
 label((918,343,1123,370),'Your task',24)
 label((918,396,1123,423),'Your method',24)
 # Original adopted tile stays in the foreground once it appears.
 if np.mean(frame[457:473,917:950,2]-frame[457:473,917:950,0].astype(float))<15:
  label((917,451,1125,477),'Useful new tool',22)
 # Preserve animated foreground method tile over rewritten evaluation text.
 label((542,348,755,477),'',22)
 for y,tx in [(354,'Real need'),(434,'Familiar task'),(464,'Better results')]:txt(d,(640,y),tx,23,NAVY,False,'mm')
 result=cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)
 hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
 mask=cv2.inRange(hsv,(15,110,100),(40,255,255));mask[:330]=0;mask[490:]=0;mask[:,:490]=0;mask[:,790:]=0
 contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
 for c in contours:
  x,y,w,h=cv2.boundingRect(c)
  if cv2.contourArea(c)>70 and w<200 and h<100:
   front=np.zeros((720,1280),np.uint8)
   cv2.drawContours(front,[cv2.convexHull(c)],-1,255,-1)
   result[front>0]=frame[front>0]
 return result

def chat(frame):
 # Fixed camera scene: remove only the knot glyph; retain the notebook artwork.
 roi=frame[263:323,260:323].copy()
 gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
 mask=(gray<120).astype('uint8')*255
 mask=cv2.dilate(mask,np.ones((3,3),np.uint8))
 result=frame.copy();result[263:323,260:323]=cv2.inpaint(roi,mask,3,cv2.INPAINT_TELEA)
 return result

def render_frame(frame,n):
 for a,b,name in CUTS:
  if a<=n<b:return ui(name,n-a,b-a)
 if 1105<=n<1285:return chat(frame)
 if 5569<=n<6073:return diagram(frame,n)
 return frame

def preview():
 OUT.mkdir(exist_ok=True);ASSETS.mkdir(parents=True,exist_ok=True)
 for a,b,name in CUTS:
  for k in [0,(b-a)//2,b-a-1]:cv2.imwrite(str(OUT/f'preview-{name}-{k:03d}.jpg'),ui(name,k,b-a))
  cv2.imwrite(str(ASSETS/f'{name}.png'),ui(name,(b-a)//2,b-a))
 for n in [1110,1140,1260,5580,5640,5700,5760,5820,5880,5940,6000,6060]:
  f=cv2.imread(str(OUT/f'source-{n:05d}.jpg'))
  if f is not None:cv2.imwrite(str(OUT/f'preview-native-{n:05d}.jpg'),render_frame(f,n))
 (ASSETS/'README.md').write_text('Native animated interface examples for Curious & Flexible. Generated deterministically by scripts/video/build_curious_flexible_v6.py using Pillow; no stock photographs or external product UI. PNGs are representative states; the video includes cursor, selection, and progress motion. The five inserts illustrate the approved habits, using one cell-biology assignment for the evaluation examples. Newsletter is also used at the inter-board hand-off. No ImageGen prompts or assets were used.\n')
 print('Previews ready',flush=True)

def main():
 cv2.setNumThreads(2);preview()
 if '--preview' in sys.argv:return
 assert sha(SRC)==EXPECTED;assert not DEST.exists(),'Never overwrite a review candidate'
 protected={str(p):sha(p) for p in [SRC,*SRC.parent.glob('*.jpg'),ROOT/'lessons/curious-and-flexible.md']}
 proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','yuv420p','-s','1280x720','-r','30','-i','pipe:0','-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-profile:v','high','-level:v','3.1','-crf','16','-preset','fast','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 count=0
 with av.open(str(SRC)) as inp:
  inp.streams.video[0].codec_context.thread_count=2
  for n,f in enumerate(inp.decode(video=0)):
   if any(a<=n<b for a,b,_ in CHANGED):
    im=render_frame(f.to_ndarray(format='bgr24'),n)
    raw=av.VideoFrame.from_ndarray(im,format='bgr24').to_ndarray(format='yuv420p')
   else:raw=f.to_ndarray(format='yuv420p')
   proc.stdin.write(raw.tobytes());count+=1
   if count%1500==0:print(f'Rendered {count}/{N}',flush=True)
 proc.stdin.close();assert proc.wait()==0;assert count==N
 assert audio_hash(SRC)==audio_hash(DEST);assert audio_hash(SRC,True)==audio_hash(DEST,True)
 assert all(sha(p)==h for p,h in protected.items())
 m=dict(scope='Approved visual pacing and supporting graphic cleanup; candidate only',approval='User: Build please',source=str(SRC),source_sha256=EXPECTED,candidate=str(DEST),candidate_sha256=sha(DEST),frames=N,fps=30,duration=N/30,protected=protected,protected_files_unchanged=True,audio_packets_identical=True,decoded_audio_identical=True,source_limitation='Original raw generations absent. One visual encode from verified finished source; unchanged source frames remain YUV before encode.',changed_spans=[dict(start=a,end=b,label=label) for a,b,label in CHANGED],boundaries=BOUNDARIES,board_runs=[[1671,2220],[2340,2880],[3090,3426],[3662,4170],[4380,4620],[4770,5010],[5160,5569]],longest_board_seconds=18.3,added_pauses=[],narration_changes=[],asset_generator=str(Path(__file__).resolve()),listening='Not listened by ear. Audio identity verified; source listening limitations persist.',retained='Basketball animation, current canonical boards and dense pans, update/focus/student scenes, final diagram motion, course close.',notes=['Native UI cutaways as approved alternative to student photographs.','Clean native newsletter fallback replaces illegible handwritten email scene.','Final diagram original moving markers, arrows, pulses, and adoption retained.','Existing board highlights preserved, including legacy ring widths.'])
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('BUILT',DEST,flush=True)
if __name__=='__main__':main()
