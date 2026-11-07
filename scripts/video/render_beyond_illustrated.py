#!/usr/bin/env python3
"""Illustrated Beyond boards. Default output is review-only; canonical install is separate."""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageOps
from editorial_typography import face, draw_board_title, draw_inner_title
from editorial_takeaway import draw_takeaway_band
from render_editorial_ai_chat import BOARDS, wrap, add_sheet_shadow

ROOT=Path(__file__).resolve().parents[2]
ART=ROOT/'scripts/video/assets/beyond-the-first-answer-illustrated-2026-11-07'
INK='#3a3550'; PURPLE='#4f2fc4'; BLUE='#1858df'; BORDER='#dcd5f2'

def measure(text,width,size=29):
    return wrap(ImageDraw.Draw(Image.new('RGB',(1,1))),text,face('medium',size),width)

def shell(board,bottom):
    footer=bottom+40
    im=Image.new('RGB',(1600,footer+128),'white')
    d=ImageDraw.Draw(im);d.rounded_rectangle((0,0,1599,im.height-1),22,fill='#eae7fd')
    draw_board_title(d,board.title)
    draw_takeaway_band(im,top=footer,left=40,right=1560,text=board.takeaway,font=face('medium',32))
    return im

def card(im,x,y,w,h,slug,half,art_h):
    add_sheet_shadow(im,(x,y,x+w,y+h))
    panel=Image.new('RGB',(w,h),'white')
    with Image.open(ART/f'{slug}.png') as source:
        art=source.convert('RGB'); piece=art.crop((0,half*art.height//2,art.width,(half+1)*art.height//2))
        panel.paste(ImageOps.fit(piece,(w,art_h),method=Image.Resampling.LANCZOS),(0,0))
    mask=Image.new('L',panel.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),14,fill=255)
    im.paste(panel,(x,y),mask)
    ImageDraw.Draw(im).rounded_rectangle((x,y,x+w,y+h),14,outline=BORDER,width=1)

def text_lines(d,lines,x,y,size=29,leading=41):
    for line in lines:
        d.text((x,y),line,font=face('medium',size),fill=INK,anchor='la');y+=leading
    return y

def render_pair(board):
    lines=[measure(t.text,676) for t in board.turns]
    h=339+32+52+max(map(len,lines))*41+34
    bottom=127+h
    eqtop=bottom+32
    im=shell(board,eqtop+134 if board.slug=='profit' else bottom)
    for i,(x,c,label) in enumerate([(40,PURPLE,'You'),(816,BLUE,'AI')]):
        card(im,x,127,744,h,board.slug,i,339);d=ImageDraw.Draw(im)
        draw_inner_title(d,(x+34,498),label,fill=c)
        end=text_lines(d,lines[i],x+34,550)
        assert end+12<bottom
    if board.slug=='profit':
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((40,eqtop,1560,eqtop+134),14,fill='white',outline=BORDER,width=1)
        for cx,amount,label,color in [(315,'$300','Sales',BLUE),(800,'$150','Costs',PURPLE),(1285,'$150','Profit','#008b80')]:
            d.text((cx,eqtop+12),amount,font=face('bold',52),fill=color,anchor='ma')
            d.text((cx,eqtop+80),label,font=face('medium',29),fill=INK,anchor='ma')
        for cx,symbol in [(558,'−'),(1043,'=')]:
            d.text((cx,eqtop+34),symbol,font=face('medium',44),fill=INK,anchor='ma')
    return im

def bubble_height(text,width,size=29):
    return 35+44+len(measure(text,width-48,size))*round(size*1.414)

def bubble(im,turn,left,right,y,width,size=29):
    human=turn.role=='YOU'; x=right-width if human else left
    d=ImageDraw.Draw(im)
    d.text((x+width if human else x,y), 'YOU' if human else 'AI',font=face('heavy',19),fill=PURPLE if human else BLUE,anchor='ra' if human else 'la')
    y+=35
    lines=measure(turn.text,width-48,size);leading=round(size*1.414)
    h=44+len(lines)*leading
    d.rounded_rectangle((x,y,x+width,y+h),14,fill='#f1edff' if human else '#f5f7fc',outline='#dfd9f4' if human else '#dce5f6',width=1)
    text_lines(d,lines,x+24,y+22,size,leading)
    return y+h

def render_iteration(board):
    bw=612
    heights=[339+32+52+sum(bubble_height(t.text,bw) for t in board.turns[i:i+2])+28+34 for i in (0,2)]
    h=max(heights);im=shell(board,127+h)
    for i,(x,title,c) in enumerate([(40,'Early Round',PURPLE),(816,'Later Round',BLUE)]):
        card(im,x,127,744,h,board.slug,i,339)
        draw_inner_title(ImageDraw.Draw(im),(x+34,498),title,fill=c)
        y=550
        for turn in board.turns[i*2:i*2+2]:
            y=bubble(im,turn,x+34,x+710,y,bw)+28
        assert y-28+12<127+h
    return im

def render_summer(board):
    bw=832;size=32
    chat_h=68+sum(bubble_height(t.text,bw,size) for t in board.turns)+3*28
    im=shell(board,127+chat_h)
    add_sheet_shadow(im,(552,127,1560,127+chat_h))
    d=ImageDraw.Draw(im);d.rounded_rectangle((552,127,1560,127+chat_h),18,fill='white',outline=BORDER,width=1)
    y=161;positions=[]
    for turn in board.turns:
        positions.append(y);y=bubble(im,turn,586,1526,y,bw,size)+28
    assert y-28+20<127+chat_h
    for i,(top,title,caption,c) in enumerate([(127,'Your strengths','Dogs and teaching math',PURPLE),(positions[2]-34,'Possible directions','Pet care\nMath tutoring\nNeighborhood errands',BLUE)]):
        n=len(caption.splitlines());h=240+32+52+n*41+34
        card(im,40,top,480,h,board.slug,i,240)
        d=ImageDraw.Draw(im)
        draw_inner_title(d,(74,top+272),title,fill=c,size=36)
        text_lines(d,caption.splitlines(),74,top+324)
        assert top+h<127+chat_h
    return im

def render(board):
    if board.slug in ('profit','college'):return render_pair(board)
    if board.slug=='iteration':return render_iteration(board)
    return render_summer(board)

def credit(im):
    ImageDraw.Draw(im).text((1560,im.height-10),'besmarterthanthetool.com',font=face('medium',20),fill='#625c7a',anchor='rd')
    return im

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'tmp/beyond-illustrated-review');a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    for board in BOARDS:
        im=credit(render(board)); path=a.output/f'beyond-the-first-answer-{board.slug}.jpg'
        im.save(path,quality=95,subsampling=0,optimize=True)
        im.resize((880,round(im.height*.55)),Image.Resampling.LANCZOS).save(a.output/f'{board.slug}-880.jpg',quality=95)
        print(f'{board.slug}: {im.width}x{im.height}')
