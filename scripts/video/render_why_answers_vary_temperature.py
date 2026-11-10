#!/usr/bin/env python3
"""Canonical worked-example board using docs/components/boards/README.md.

1600 px lavender shell; 56 px tracked title; 40 px column headings;
27 px / 38 px column explanations (owner-requested size reduction);
29 px row labels; 27 px percentages (owner-requested 20% reduction);
content-derived height and 40 px bottom margins.
Video motion stays in TemperatureScene.
"""
from pathlib import Path
from PIL import Image, ImageDraw
from editorial_typography import draw_board_title, draw_inner_title, face
from course_credit import save_course_image

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'course-assets/why-answers-vary/why-answers-vary-temperature.jpg'
ROWS = [('Spot',22,36,16),('Max',17,21,14),('Buddy',14,15,13),
        ('Rex',9,6,10),('Biscuit',6,3,8),('All other tokens',32,19,39)]
# One scale for every bar; percentages remain the source of the exact values.
BAR_MAX = 40
ROW_SPACING = 112.5
ROW_TOP = 421
FRAME, INK, MUTED = '#eae7fd', '#0e0a1f', '#625c7a'


def render():
    table_bottom = round(ROW_TOP + (len(ROWS) - 1) * ROW_SPACING + 76)
    sheet_bottom = table_bottom + 40
    image = Image.new('RGB', (1600, sheet_bottom + 40), FRAME)
    d = ImageDraw.Draw(image)
    draw_board_title(d, 'How Temperature Changes the Odds')
    d.rounded_rectangle((40,118,1560,sheet_bottom), radius=22, fill='white')
    d.rounded_rectangle((80,150,1520,236), radius=14, fill='#f3f0ff', outline='#d9d3eb', width=2)
    d.text((720,193),'You could name him',font=face('bold',34),fill=INK,anchor='rm')
    d.rounded_rectangle((740,170,892,218),radius=9,fill='white',outline='#d9d0fb',width=2)
    d.text((816,191),'?',font=face('bold',32),fill='#6e51ff',anchor='mm')
    columns = [
        (322,'Low Temperature','#1652f0','#edf2fe',['Concentrates the odds']),
        (732,'Starting Odds','#4f2fc4','#eeebfc',['From training and context']),
        (1142,'High Temperature','#c41f28','#fceeed',['Spreads the odds']),
    ]
    for x,title,accent,tint,lines in columns:
        d.rounded_rectangle((x,266,x+378,table_bottom),radius=14,fill=tint)
        draw_inner_title(d,(x+189,280),title,fill=accent,anchor='ma')
        for j,line in enumerate(lines):
            assert d.textlength(line,font=face('medium',27)) < 354
            d.text((x+189,342+j*38),line,font=face('medium',27),fill=INK,anchor='mt')
    for i,row in enumerate(ROWS):
        y = ROW_TOP+i*ROW_SPACING
        if row[0]=='All other tokens':
            d.text((96,y+8),'All other',font=face('bold',32),fill=INK,anchor='lt')
            d.text((96,y+46),'tokens',font=face('bold',32),fill=INK,anchor='lt')
        else:
            d.text((96,y+8),row[0],font=face('bold',32),fill=INK,anchor='lt')
        for c,(x,_,accent,_,_) in enumerate(columns):
            value=row[(2,1,3)[c]]
            d.text((x+189,y+4),f'{value}%',font=face('bold',27),fill=accent,anchor='mt')
            d.rounded_rectangle((x+28,y+47,x+350,y+63),radius=8,fill='white')
            d.rounded_rectangle((x+28,y+47,x+28+322*value/BAR_MAX,y+63),radius=8,fill=accent)
    save_course_image(image,OUTPUT,quality=95,subsampling=0,optimize=True)
    print(f'{OUTPUT}: {image.size}')

if __name__=='__main__':
    render()
