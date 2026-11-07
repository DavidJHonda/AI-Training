#!/usr/bin/env python3
"""Run full decode/seam/audio QA against v8, excluding only two new passages."""
import build_when_you_need_more_v9 as candidate
import qa_when_you_need_more_v8 as checks
from PIL import Image,ImageDraw

def scene_sheets():
    frames=[f for r in candidate.INSERTS for f in range(r['start'],r['end'],15)]
    for page in range((len(frames)+15)//16):
        sheet=Image.new('RGB',(1280,800),'white');draw=ImageDraw.Draw(sheet)
        for j,f in enumerate(frames[page*16:(page+1)*16]):
            x=j%4*320;y=j//4*200
            im=Image.open(candidate.OUT/'encoded'/f'frame-{f:05d}.jpg').resize((320,180))
            sheet.paste(im,(x,y));draw.text((x+5,y+182),f'{f/30:.2f}s / frame {f}',fill='black')
        sheet.save(candidate.OUT/f'encoded-scenes-{page}.jpg')

if __name__=='__main__':
    checks.b=candidate
    checks.main()
    scene_sheets()
