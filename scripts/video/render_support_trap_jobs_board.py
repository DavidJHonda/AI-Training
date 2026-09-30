#!/usr/bin/env python3
"""Compose the new three-jobs board using course typography and generated art."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageOps
from editorial_typography import face,draw_board_title,draw_inner_title
from editorial_takeaway import draw_takeaway_band
ROOT=Path(__file__).resolve().parents[2]
ASSET=ROOT/'scripts/video/assets/support-trap-jobs-2026-09-30/art-strip.png'
DEST=ROOT/'course-assets/support-trap/support-trap-jobs.jpg'
CARDS=[
 dict(title='Ordinary Venting',accent='#0e8f86',body='Put an everyday frustration into words to cool down before you share.',outcome='The job may end in the chat.'),
 dict(title='Preparation',accent='#1652f0',body='Draft an email, rehearse a hard conversation, or make a study plan.',outcome='Then act outside the chat.'),
 dict(title='Danger',accent='#c41f28',body='If someone may be unsafe, leave the chat and reach a person who can act.',outcome='Leave the chat. Get help.'),
]
def lines(d,text,font,width):
 out=[];line=''
 for word in text.split():
  t=(line+' '+word).strip()
  if line and d.textlength(t,font=font)>width:out.append(line);line=word
  else:line=t
 return out+[line]
def paragraph(d,text,x,y,width,size,weight,color,leading):
 ls=lines(d,text,face(weight,size),width)
 for line in ls:d.text((x,y),line,font=face(weight,size),fill=color);y+=leading
 return y,ls

def main():
 im=Image.new('RGB',(1600,1020),'white');d=ImageDraw.Draw(im);d.rounded_rectangle((0,0,1599,1019),22,fill='#eae7fd')
 draw_board_title(d,'Where AI Fits in Emotional Support')
 art=Image.open(ASSET).convert('RGB');geometry=[]
 for i,(x,card) in enumerate(zip([40,557,1075],CARDS)):
  right=[525,1043,1560][i];w=right-x
  d.rounded_rectangle((x,128,right,852),18,fill='white')
  panel=art.crop((round(i*art.width/3),0,round((i+1)*art.width/3),art.height))
  panel=ImageOps.fit(panel,(w,320),method=Image.Resampling.LANCZOS,centering=(.5,.55))
  mask=Image.new('L',(w,320),0);md=ImageDraw.Draw(mask);md.rounded_rectangle((0,0,w-1,339),18,fill=255)
  im.paste(panel,(x,128),mask)
  draw_inner_title(d,(x+32,480),card['title'],fill=card['accent'])
  bottom,body_lines=paragraph(d,card['body'],x+32,546,w-64,32,'medium','#36324b',44)
  assert bottom<=722,(card['title'],bottom,body_lines)
  d.line((x+32,730,right-32,730),fill='#e3def0',width=2)
  bottom,outcome_lines=paragraph(d,card['outcome'],x+32,750,w-64,30,'bold',card['accent'],42)
  assert bottom<=834,(card['title'],bottom,outcome_lines)
  geometry.append(dict(**card,bounds=[x,128,right,852],body_lines=body_lines,outcome_lines=outcome_lines))
 draw_takeaway_band(im,top=892,left=40,right=1560,text='Use AI to prepare for people, not replace them.',font=face('medium',32))
 d.text((1560,1008),'besmarterthanthetool.com',font=face('medium',20),fill='#625c7a',anchor='rd')
 im.save(DEST,quality=95,subsampling=0)
 meta=dict(title='Where AI Fits in Emotional Support',size=list(im.size),output=str(DEST),sha256=hashlib.sha256(DEST.read_bytes()).hexdigest(),art_source=str(ASSET),cards=geometry,takeaway='Use AI to prepare for people, not replace them.',banner=[40,892,1560,980])
 (ASSET.parent/'board-spec.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta,indent=2))
if __name__=='__main__':main()
