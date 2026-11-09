"""Video-only, landscape token demonstration approved November 9, 2026.

Times are on the accepted v12 timeline. Values come from the lesson's
ANSWER_BUILD_STATES. A selected token travels from its row into the reply.
"""
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = Path(__file__).resolve().parent / 'assets/fonts/PlusJakartaSans-wght.ttf'
S = 2
BG = '#fffdf9'
INK = '#191329'
MUTED = '#625970'
PURPLE = '#7955dc'
PALE = '#eee8f7'
TOKENS = ['You', 'could', 'name', 'him', 'Spot', '.']
OPTIONS = [
    [('You',18),('A',14),('Great',9),('Other',59)],
    [('could',32),('can',26),('should',14),('Other',28)],
    [('name',48),('call',29),('try',8),('Other',15)],
    [('him',35),('your',28),('the',12),('Other',25)],
    [('Spot',22),('Max',17),('Buddy',14),('Other',47)],
    [('.',72),('!',8),(',',5),('Other',15)],
]
# Reveal chart, select its first row, begin flight, finish flight.
EVENTS = [
    (3172,3680,3692,3705),
    (3747,3919,3930,3941),
    (3943,3945,3951,3961),
    (3963,3970,3976,3984),
    (4030,4715,4727,4739),
    (4780,4849,4854,4867),
]

@lru_cache(maxsize=96)
def font(size, weight=600):
    f = ImageFont.truetype(str(FONT), round(size*S))
    f.set_variation_by_axes([weight])
    return f

def width(text, size=46, weight=700):
    return font(size, weight).getlength(text)/S

def positions():
    # Stable line breaks prevent already-written tokens from moving.
    x=80; p=[]
    for token in TOKENS[:3]:
        p.append((x,300));x += width(token)+width(' ')
    x=80
    for token in TOKENS[3:]:
        if token=='.': x-=width(' ')
        p.append((x,380));x+=width(token)+width(' ')
    assert p[2][0]+width('name') < 600
    assert p[5][0]+width('.') < 600
    return p

POSITIONS=positions()

def ease(t):
    t=max(0,min(1,t));return t*t*(3-2*t)

def signature(f):
    stage=-1
    for i,(show,selected,start,end) in enumerate(EVENTS):
        if f>=show:stage=i
    if stage<0:return (-1,0,0,0)
    show,selected,start,end=EVENTS[stage]
    progress=min(1,max(0,(f-start)/(end-start)))
    bars=min(1,max(0,(f-show)/8)) if stage else 1
    return (stage, int(f>=selected), progress, bars)

@lru_cache(maxsize=48)
def render_state(state):
    stage,selected,progress,bars=state
    im=Image.new('RGB',(1280*S,720*S),BG);d=ImageDraw.Draw(im)
    def text(x,y,t,size=30,weight=600,color=INK):
        d.text((round(x*S),round(y*S)),t,font=font(size,weight),fill=color,anchor='lt')
    def box(x0,y0,x1,y1,fill,radius=8,outline=None,stroke=0):
        d.rounded_rectangle(tuple(round(v*S) for v in (x0,y0,x1,y1)),radius=radius*S,fill=fill,outline=outline,width=stroke*S)
    text(80,57,'What should I name my new dog?',40,700)
    d.line((80*S,143*S,1200*S,143*S),fill='#ded8e8',width=2*S)
    text(80,225,'Reply so far',22,600,MUTED)
    text(710,225,'What could come next?',22,600,MUTED)
    written=0 if stage<0 else stage+int(progress>=1)
    if not written and not (selected and progress>0):
        text(80,304,'No tokens yet',32,500,MUTED)
    for i in range(written):
        x,y=POSITIONS[i];token=TOKENS[i]
        if i==written-1:box(x-7,y-10,x+width(token)+7,y+53,'#eae2ff',6)
        text(x,y,token,46,700)
    if written<len(TOKENS) and not (selected and 0<progress<1):
        x,y=POSITIONS[written]
        if written==0:x=80;y=371
        d.line((x*S,(y+52)*S,(x+57)*S,(y+52)*S),fill=PURPLE,width=3*S)
    if stage<0:
        text(710,304,'Ready to predict',28,500,MUTED)
    else:
        opts=OPTIONS[stage]
        for j,(token,pct) in enumerate(opts[:3]):
            y=300+j*80
            if j==0 and selected:
                box(692,y-18,1212,y+48,None,10,PURPLE,4)
            # Keep the source word while a separate copy travels into the reply.
            text(710,y,token,30,700)
            box(862,y+8,1118,y+24,PALE,8)
            oldpct=OPTIONS[stage-1][j][1] if stage else pct
            value=oldpct+(pct-oldpct)*ease(bars)
            box(862,y+8,862+256*value/100,y+24,PURPLE,8)
            label=f'{pct}%'
            text(1200-width(label,26,700),y+2,label,26,700)
        text(710,544,f'All other tokens combined: {opts[3][1]}%',21,500,MUTED)
        text(710,582,'Illustrative probabilities',18,500,MUTED)
        if selected and 0<=progress<1:
            q=ease(progress);tx,ty=POSITIONS[stage]
            x=710+(tx-710)*q;y=300+(ty-300)*q+90*np.sin(np.pi*q)
            fs=30+16*q;token=TOKENS[stage];w=width(token,fs,700)
            box(x-9,y-10,x+w+9,y+fs+7,'#eae2ff',6)
            text(x,y,token,fs,700)
    return np.array(im.resize((1280,720),Image.Resampling.LANCZOS))[:,:,::-1].copy()

def render(f):
    return render_state(signature(f)).copy()
