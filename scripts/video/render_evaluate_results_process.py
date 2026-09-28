#!/usr/bin/env python3
"""Render the evaluation overview and four stage boards with unchanged teaching copy.

Current replacement for the four historical render_evaluate_results_* scripts.
Video camera/ring coordinates must be reviewed before using these layouts in video.
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw
from editorial_typography import face, draw_board_title
from editorial_takeaway import draw_takeaway_band
from render_evaluate_results_quick_pass import CARD_COPY as QUICK
from render_evaluate_results_decide import CARDS as DECIDE
from render_evaluate_results_dig import CARDS as DIG
from render_evaluate_results_move import CARD_COPY as MOVE

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'course-assets/evaluate-the-results'
BG, INK, BODY, PURPLE, LINE = '#eae7fd', '#0e0a1f', '#3a3550', '#4f2fc4', '#655f87'
STAGES = (
    ('quick-pass', 'Quick Pass', tuple(zip(('Read', 'Understand', 'Validate'), QUICK)), 'Before you use it: read, understand, validate.'),
    ('decide', 'Dig Deeper?', DECIDE, 'Give the answer the attention it deserves.'),
    ('dig', 'Dig Deeper', DIG, 'Use AI to help you check. You decide whether the answer holds up.'),
    ('move', 'Your Move', tuple(zip(('Use It', 'Fix It', 'Walk Away'), MOVE)), 'The tool answers. You evaluate.'),
)


def wrap(draw, text, font, width):
    result, line = [], ''
    for word in text.split():
        trial = (line + ' ' + word).strip()
        if line and draw.textlength(trial, font=font) > width:
            result.append(line)
            line = word
        else:
            line = trial
    if line:
        result.append(line)
    return result


def block(draw, xy, lines, font, color, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=color, anchor='lt')
        y += leading
    return y


def arrow(draw, points, color=LINE, width=2, tip=9):
    draw.line(points, fill=color, width=width, joint='curve')
    x, y = points[-1]
    px, py = points[-2]
    a = math.atan2(y-py, x-px)
    draw.line([(x-tip*math.cos(a-.65), y-tip*math.sin(a-.65)), (x,y),
               (x-tip*math.cos(a+.65), y-tip*math.sin(a+.65))], fill=color, width=width)


def mini(draw, active):
    # No revision loop: only the full overview connects Fix It back to Quick Pass.
    y, h = 82, 48
    nodes = [(860,990,'Quick Pass'), (1030,1200,'Dig Deeper?'),
             (1240,1370,'Dig Deeper'), (1410,1560,'Your Move')]
    for i,(x0,x1,label) in enumerate(nodes):
        fill, color = (PURPLE,'white') if i==active else ('white',LINE)
        if i==1:
            draw.polygon([(x0,y),(1115,y-48),(x1,y),(1115,y+48)],fill=fill,outline='#cbc3f3')
            draw.text((1115,y-12),'Dig',font=face('bold',20),fill=color,anchor='mm')
            draw.text((1115,y+12),'Deeper?',font=face('bold',20),fill=color,anchor='mm')
        else:
            draw.rounded_rectangle((x0,y-h/2,x1,y+h/2),9,fill,outline='#cbc3f3')
            draw.text(((x0+x1)/2,y),label,font=face('bold',17),fill=color,anchor='mm')
    for start,end in ((992,1025),(1203,1235),(1373,1405)):
        arrow(draw,[(start,y),(end,y)],tip=6)
    arrow(draw,[(1115,34),(1115,23),(1485,23),(1485,54)],tip=6)
    draw.rectangle((1290,11,1327,34),fill=BG)
    draw.text((1308,22),'No',font=face('bold',16),fill=LINE,anchor='mm')
    draw.text((1218,56),'Yes',font=face('bold',16),fill=LINE,anchor='mm')


def save(image, suffix):
    draw = ImageDraw.Draw(image)
    draw.text((1560,image.height-10),'besmarterthanthetool.com',font=face('medium',20),fill='#625c7a',anchor='rd')
    path=OUT/f'evaluate-the-results-{suffix}.jpg'
    image.save(path,quality=95,subsampling=0,optimize=True)
    print(path.name, image.size)


def stage_board(index):
    suffix,title,items,takeaway=STAGES[index]
    scratch=ImageDraw.Draw(Image.new('RGB',(1,1)))
    title_face, body_face=face('bold',36),face('medium',30)
    rows=[items[:3]] + ([items[3:]] if len(items)>3 else [])
    plans=[]
    top=184
    for row in rows:
        cells=[]
        for heading,body in row:
            heads=wrap(scratch,heading,title_face,420)
            lines=wrap(scratch,body,body_face,420)
            cells.append((heads,lines))
        height=max(64+len(h)*44+18+len(b)*40 for h,b in cells)
        plans.append((top,height,cells))
        top+=height+28
    footer=top+12
    image=Image.new('RGB',(1600,footer+128),BG)
    draw=ImageDraw.Draw(image)
    draw_board_title(draw,title,y=58)
    mini(draw,index)
    for top,height,cells in plans:
        left=(1600-(len(cells)*488+(len(cells)-1)*28))/2
        for heads,lines in cells:
            draw.rounded_rectangle((left,top,left+488,top+height),16,'white')
            end=block(draw,(left+34,top+34),heads,title_face,PURPLE,44)
            block(draw,(left+34,end+18),lines,body_face,BODY,40)
            left+=516
    draw_takeaway_band(image,top=footer,left=40,right=1560,text=takeaway,font=face('medium',32))
    save(image,suffix)


def overview():
    image=Image.new('RGB',(1600,800),BG)
    draw=ImageDraw.Draw(image)
    draw_board_title(draw,'How to Evaluate an AI Answer')
    draw.rounded_rectangle((40,126,1560,750),18,'white')
    nodes=[(80,340,380,480,'Quick Pass'),
           (840,340,1140,480,'Dig Deeper'),
           (1220,340,1520,480,'Your Move')]
    for x0,y0,x1,y1,title in nodes:
        draw.rounded_rectangle((x0,y0,x1,y1),18,BG)
        center=(x0+x1)/2
        cues={
            'Quick Pass': ('Read. Understand.', 'Validate.'),
            'Dig Deeper': ('Choose the checks', 'that fit.'),
        }.get(title)
        draw.text((center,376 if cues else 410),title,font=face('bold',36),fill=PURPLE,anchor='mm')
        if cues:
            for i,line in enumerate(cues):
                draw.text((center,424+i*28),line,font=face('medium',24),fill=BODY,anchor='mm')
    draw.polygon([(430,410),(610,280),(790,410),(610,540)],fill=BG,outline='#cec5fc')
    draw.text((610,388),'Dig',font=face('bold',36),fill=PURPLE,anchor='mm')
    draw.text((610,432),'Deeper?',font=face('bold',36),fill=PURPLE,anchor='mm')
    arrow(draw,[(380,410),(418,410)])
    arrow(draw,[(790,410),(828,410)])
    draw.text((809,377),'Yes',font=face('bold',24),fill=LINE,anchor='mm')
    arrow(draw,[(1140,410),(1208,410)])
    arrow(draw,[(610,280),(610,218),(1370,218),(1370,330)])
    draw.rectangle((948,198,1038,238),fill='white')
    draw.text((993,218),'No',font=face('bold',24),fill=LINE,anchor='mm')
    # Three parallel outcomes; only Fix It returns to the beginning.
    draw.line([(1370,480),(1370,565),(890,565)],fill=LINE,width=2)
    for center,label in ((890,'Fix It'),(1130,'Use It'),(1370,'Walk Away')):
        arrow(draw,[(center,565),(center,598)])
        draw.rounded_rectangle((center-105,605,center+105,669),32,'white',outline='#cec5fc',width=2)
        draw.text((center,637),label,font=face('bold',27),fill=INK,anchor='mm')
    arrow(draw,[(785,637),(230,637),(230,492)],color=PURPLE,width=3)
    draw.rectangle((327,613,565,661),fill='white')
    draw.text((446,637),'Check the fix',font=face('bold',25),fill=PURPLE,anchor='mm')
    save(image,'process')


if __name__=='__main__':
    overview()
    for i in range(4):
        stage_board(i)
