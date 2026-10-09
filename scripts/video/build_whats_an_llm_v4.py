#!/usr/bin/env python3
"""Restore Notebook artwork and animations; retain v3 audio, timing and canonical boards."""
import json
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import build_whats_an_llm_v3 as prior
base=prior.base
base.OUT=base.ROOT/'video-audit/whats-an-llm-build-2026-10-09-v4'
base.DEST=base.ROOT/'Prompts/whats-an-llm-v4.mp4'
prepare_prior=base.prepare
frame_prior=base.frame
readers={}
MASK=base.glyph_mask()
FONT=ImageFont.truetype(str(base.FONT),24)
DONORS={
 'app':dict(roll=3,source_seconds=[5.5,15.1],purpose='Laptop revealing illustrated gears; preserves two Notebook shots and their movement.'),
 'training':dict(roll=3,source_seconds=[87.8,94.2],purpose='Illustrated books establish scale of training examples, under the existing training-before-use narration.'),
 'broader':dict(roll=1,source_seconds=[57,64],purpose='Interlocking pieces with text preserve Notebook visual language for learned patterns beyond familiar phrases.'),
 'context':dict(roll=3,source_seconds=[118,144.4],purpose='Original input, learned-pattern network, word choices and changing context animation; only labels and numerical panel corrected.'),
 'phone':dict(roll=3,source_seconds=[151,159.8],purpose='Original predictive-keyboard animation: sunny is selected, then and/with/outside suggestions appear.'),
 'growing':dict(roll=2,source_seconds=[125.933333,142.7],purpose='Original word feedback loop and branching continuations; simplify headings and remove numerical odds.')}

def prepare():
 b,boards,m=prepare_prior()
 for r in m['timeline']:
  if r['visual'] in DONORS:r['notebook_donor']=DONORS[r['visual']]
 m['scope']='Owner-approved visual-only restoration of engaging Notebook graphics; v3 narration, duration, canonical boards and close preserved.'
 m['visual_repair']='Same-frame paper clones remove only labels/percentage panel details, followed by concise replacement labels; original drawings, networks, arrows, word movement and branching preserved.'
 m['retiming']={'context_output_to_source_seconds':[[83.666667,118],[87,121],[90,124],[94.18,125],[97.3,126.5],[99.56,133.4],[101.3,142],[102.666667,144.4]],'phone_output_to_source_seconds':[[105.8,151],[107.46,156],[111.333333,159.8]]}
 (base.OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 return b,boards,m

def get_source(key,roll,sf):
 if key not in readers:readers[key]=base.Reader(base.SRC[roll])
 return readers[key].at(sf)

def paper(im,rect,donor_x):
 # Same-frame horizontal paper clone: preserve row-wise texture/lighting, feather edges.
 x0,y0,x1,y1=rect;patch=np.repeat(np.median(im[y0:y1,donor_x:donor_x+8],axis=1)[:,None,:],x1-x0,axis=1)
 a=np.ones((y1-y0,x1-x0));r=np.linspace(0,1,3)
 a[:3]*=r[:,None];a[-3:]*=r[::-1,None];a[:,:3]*=r;a[:,-3:]*=r[::-1]
 im[y0:y1,x0:x1]=np.rint(im[y0:y1,x0:x1]*(1-a[:,:,None])+patch*a[:,:,None]).astype(np.uint8)

def label(im,xy,words,color='#373c39',size=24):
 p=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(p)
 d.text(xy,words,font=FONT if size==24 else ImageFont.truetype(str(base.FONT),size),fill=color,anchor='mm')
 return cv2.cvtColor(np.array(p),cv2.COLOR_RGB2BGR)

def frame(f,r,b,boards,reader,close,counts):
 v=r['visual']
 if v not in DONORS:return frame_prior(f,r,b,boards,reader,close,counts)
 spec=DONORS[v];u=(f-r['start_frame'])/max(1,r['end_frame']-r['start_frame']-1)
 t=spec['source_seconds'][0]+u*(spec['source_seconds'][1]-spec['source_seconds'][0])
 if v=='context':t=float(np.interp(f/30,[83.666667,87,90,94.18,97.3,99.56,101.3,102.666667],[118,121,124,125,126.5,133.4,142,144.4]))
 if v=='phone':t=float(np.interp(f/30,[105.8,107.46,111.333333],[151,156,159.8]))
 if v=='growing':t=(f-122)/30
 im=get_source(v,spec['roll'],round(t*30))
 if v=='context':
  paper(im,(470,108,810,139),1030);im=label(im,(640,123),'Words already there',size=22)
  if t>=122:
   paper(im,(707,284,1090,313),1093);im=label(im,(905,298),'Possible next words',size=22)
   paper(im,(700,315,1090,544),1093)
   words=['jelly','butter','honey','sandwich'] if t<139 else ['sandwich','smoothie','bread','jelly']
   for i,w in enumerate(words):im=label(im,(895,340+i*49),w,color='#b57b2e' if i==0 else '#30322c',size=28)
 if v=='growing':
  paper(im,(250,248,435,281),455);im=label(im,(345,265),'Words so far',size=22)
  if t<138.6:
   paper(im,(792,220,1090,254),1110);im=label(im,(946,238),'Predict the next word',color='#7b2630',size=23)
   if t>=133.6:paper(im,(844,343,1050,378),1080)
  else:
   # Branch scene uses a different layout. Do not touch its sentence or arrows.
   im=get_source(v,spec['roll'],round(t*30))
   paper(im,(473,94,828,128),930);im=label(im,(650,111),'Different possible answers',color='#7b2630',size=23)
 im,how=base.clean_frame(im,MASK);counts[how]=counts.get(how,0)+1
 return im

base.prepare=prepare;base.frame=frame
if __name__=='__main__':
 if '--preview' in base.sys.argv:
  b,boards,m=prepare();close=cv2.imread(str(base.OUT/'close.png'));reader=base.Reader(base.SRC[2]);counts={}
  times=[8,11,15,39,44,48,73,77,82,85,88,92,95,98,100,102,106,108,110,131,134,137,140,142,144,146]
  for t in times:
   f=round(t*30);r=next(r for r in m['timeline'] if r['start_frame']<=f<r['end_frame'])
   cv2.imwrite(str(base.OUT/'preview'/f'check-{f:05}.jpg'),frame(f,r,b,boards,reader,close,counts))
 else:base.render()
