"""Purpose-built explanatory animations for the approved Hallucination board breaks.
All text is schematic or quoted from the lesson's explicitly invented answer.
No numerical probabilities, fabricated paper, or new research claim is supplied.
"""
from functools import lru_cache
import math
import numpy as np,cv2
from PIL import Image,ImageDraw
from editorial_typography import face
S=2;BG='#f6f4fc';INK='#202638';MUTED='#687084';BLUE='#1652f0';PURPLE='#4f2fc4';TEAL='#0e8f86';RED='#c44143'
@lru_cache(None)
def f(size,bold=False):return face('bold' if bold else 'medium',round(size*S))
class Scene:
 def __init__(self):self.im=Image.new('RGB',(1280*S,720*S),BG);self.d=ImageDraw.Draw(self.im)
 def rect(self,r,fill='white',outline=None,width=1,radius=16):self.d.rounded_rectangle(tuple(round(x*S) for x in r),radius=round(radius*S),fill=fill,outline=outline,width=round(width*S))
 def line(self,pts,fill=INK,width=2):self.d.line([(round(x*S),round(y*S)) for x,y in pts],fill=fill,width=round(width*S))
 def circle(self,r,fill=None,outline=None,width=1):self.d.ellipse(tuple(round(x*S) for x in r),fill=fill,outline=outline,width=round(width*S))
 def text(self,xy,s,size=24,color=INK,bold=False,anchor='la'):self.d.text(tuple(round(x*S) for x in xy),s,font=f(size,bold),fill=color,anchor=anchor)
 def cursor(self,x,y):
  pts=[(x,y),(x+5,y+32),(x+12,y+24),(x+20,y+39),(x+27,y+35),(x+18,y+20),(x+30,y+19)]
  self.d.polygon([(round(a*S),round(b*S)) for a,b in pts],fill=INK,outline='white',width=2*S)
 def browser(self,r,label):
  x,y,w,h=r;self.rect((x+5,y+8,x+w+5,y+h+8),'#e2deef');self.rect((x,y,x+w,y+h),'white','#d8d3e5');self.line([(x,y+48),(x+w,y+48)],'#e4e0ed',1)
  for i,c in enumerate(['#d4cce5','#c9d6f1','#b9ded7']):self.circle((x+20+i*18,y+20,x+28+i*18,y+28),c)
  self.text((x+92,y+15),label,15,MUTED)
 def arrow(self,a,b,color=TEAL,width=3):
  self.line([a,b],color,width);ang=math.atan2(b[1]-a[1],b[0]-a[0]);self.line([(b[0]-14*math.cos(ang-.5),b[1]-14*math.sin(ang-.5)),b,(b[0]-14*math.cos(ang+.5),b[1]-14*math.sin(ang+.5))],color,width)
 def finish(self):return cv2.cvtColor(np.array(self.im.resize((1280,720),Image.Resampling.LANCZOS)),cv2.COLOR_RGB2BGR)

def credible(t):
 c=Scene();c.text((64,38),'Why it sounds credible',38,bold=True);c.browser((100,122,760,486),"AI's answer — invented study")
 rows=[('Stanford University','Familiar name'),('1,200 students','A credible-sounding sample'),('18% improvement','A precise result'),('Below 60 dB','A careful-sounding detail')]
 onsets=[31.22,33.4,36.5,39.98];active=max([i for i,s in enumerate(onsets) if t>=s],default=-1)
 for i,(value,_) in enumerate(rows):
  y=216+i*84
  if i==active:
   q=min(1,(t-onsets[i])/.35);c.rect((136,y-5,136+646*q,y+51),'#fff0ae',radius=6)
  c.text((154,y),value,31,INK,i==active)
 c.text((133,563),'Details from the fabricated answer',17,MUTED)
 if active>=0:
  y=238+active*84;c.line([(795,y),(937,352)],PURPLE,2);c.circle((929,274,1137,482),'white',PURPLE,4);c.line([(1110,454),(1180,524)],PURPLE,14)
  value,caption=rows[active];zoom=['Stanford','1,200','18%','60 dB'][active]
  c.text((1033,372),zoom,38,PURPLE,True,'mm');c.text((1033,411),'Real university' if active==0 else 'Claimed detail',15,MUTED,False,'mm')
  c.text((1000,580),caption,17,MUTED,False,'mm')
 else:
  c.text((1012,339),'Looks specific.',24,PURPLE,True,'mm');c.text((1012,384),'Where is the paper?',21,MUTED,False,'mm')
 return c.finish()

def tokens(t):
 c=Scene();c.text((64,38),'Predicting the next token',38,bold=True);c.text((66,94),'Illustrative sequence',17,MUTED)
 c.browser((96,158,1088,220),'Generated text')
 c.rect((149,247,229,316),'#ebe5fc');c.text((189,282),'A',34,PURPLE,True,'mm')
 c.rect((245,247,408,316),'#ebe5fc');c.text((326,282),'study',34,PURPLE,True,'mm')
 choices=[('found',BLUE),('reported','#b8c4dc'),('examined','#c7cedc')]
 for i,(word,col) in enumerate(choices):
  x=190+335*i;c.rect((x,455,x+265,534),'white',col,3 if i==0 else 1);c.text((x+132,493),word,27,col,i==0,'mm')
 if t<1.7:c.arrow((323,441),(483,330),BLUE)
 else:
  c.rect((426,247,616,316),'#e2eaff',BLUE,2);c.text((521,282),'found',34,BLUE,True,'mm');c.rect((636,261,640,302),BLUE,radius=0)
 c.text((640,609),'The next token follows learned patterns.',26,INK,False,'mm')
 return c.finish()

def plausible(t):
 c=Scene();c.text((64,38),'Fluent wording does not verify a fact',36,bold=True)
 c.browser((70,172,625,364),'The answer')
 c.text((108,270),'“A study found an',31,bold=True);c.text((108,324),'18% improvement.”',31,bold=True)
 c.text((108,448),'Claim from the invented example',17,MUTED)
 c.arrow((727,352),(835,352),PURPLE)
 c.rect((882,202,1142,495),'white','#b5accb',2,radius=6)
 c.text((1012,280),'Original study?',23,INK,True,'mm')
 if t<2:
  for i,w in enumerate([165,184,141]):c.rect((920,334+i*31,920+w,342+i*31),'#d9dce4',radius=3)
 else:
  c.text((1012,377),'?',82,RED,True,'mm');c.text((1012,463),'Not found',22,RED,True,'mm')
 c.text((640,612),'Plausible language is not evidence.',29,PURPLE,True,'mm')
 return c.finish()

def comparison(t):
 c=Scene();c.text((64,38),'Check the evidence yourself',38,bold=True)
 c.browser((60,144,685,450),'Original source');c.browser((823,236,399,292),"AI's claim")
 for i,w in enumerate([270,250,284,222]):c.rect((859,320+i*37,859+w,330+i*37),'#d9deea',radius=4)
 if t<2.3:
  c.rect((199,337,605,400),BLUE,radius=12);c.text((402,368),'Open original source',24,'white',True,'mm')
  q=min(1,t/1.7);x=705-(705-454)*q;y=553-(553-369)*q;c.cursor(x,y)
  if t>1.7:c.circle((441,355,470,384),None,TEAL,3)
  footer='Open the source itself.'
 else:
  c.text((96,226),'Original article',27,bold=True)
  for i,w in enumerate([574,539,568,497,566,537,498]):
   y=293+i*35
   if i in [2,3] and t>=4.0:
    q=min(1,(t-4)/1.0);c.rect((89,y-8,89+591*q,y+20),'#fff0ae',radius=4)
   c.rect((98,y,98+w,y+9),'#bfc7d3' if i in [2,3] else '#dce0e8',radius=4)
  if t<7:
   c.cursor(626,368);footer='Read the relevant passage in context.'
  else:
   c.arrow((690,388),(825,388),TEAL,4);c.rect((849,383,1173,441),None,TEAL,3,radius=9);footer='Does this passage support the claim?'
 c.text((640,652),footer,29,TEAL if t>=7 else INK,True,'mm')
 return c.finish()
