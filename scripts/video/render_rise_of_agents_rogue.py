#!/usr/bin/env python3
"""Render the approved single-case Rogue Agents board from native layout and retained course art."""
from pathlib import Path
from PIL import Image, ImageDraw
from editorial_typography import face, draw_board_title
from editorial_takeaway import draw_takeaway_band, TAKEAWAY_TEXT_SIZE
from render_embrace_editorial_batch import wrap, multiline, draw_shadow, FRAME, PURPLE, BODY

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT/'scripts/video/assets/rise-of-agents-repair-2026-09-30/pocketos-art.png'
DEST = ROOT/'course-assets/rise-of-agents/rise-of-agents-rogue.jpg'
QUOTE = (40, 552, 1560, 640)

def render():
    # Keep 36px of vertical padding around the image and text.
    im=Image.new('RGB',(1600,680),'white');d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,1599,679),radius=22,fill=FRAME)
    draw_board_title(d,'Rogue Agents')
    draw_shadow(im,(40,127,1560,512),14);d=ImageDraw.Draw(im)
    d.rounded_rectangle((40,127,1560,512),radius=14,fill='white',outline='#d8d1f2',width=1)
    art=Image.open(ART).convert('RGB').resize((690,313),Image.Resampling.LANCZOS)
    im.paste(art,(76,163));d=ImageDraw.Draw(im)
    d.rounded_rectangle((836,163,1304,224),radius=25,fill='#e9e3fb')
    d.text((1070,193),'APRIL 2026 · POCKETOS',font=face('heavy',29),fill=PURPLE,anchor='mm')
    body='Blocked by a permissions error, an AI coding agent found a master key in another file and deleted the company’s live database and its backups in nine seconds.'
    lines=wrap(d,body,face('medium',32),640)
    multiline(d,(836,257),lines,face('medium',32),BODY,43)
    assert 257+len(lines)*43 <= 476
    draw_takeaway_band(im,top=QUOTE[1],left=QUOTE[0],right=QUOTE[2],
        text='The agent wrote “I violated every principle I was given.”',
        font=face('medium',TAKEAWAY_TEXT_SIZE))
    d=ImageDraw.Draw(im)
    d.text((1560,670),'besmarterthanthetool.com',font=face('medium',20),fill='#625c7a',anchor='rd')
    return im

if __name__=='__main__':
    render().save(DEST,quality=96,subsampling=0)
    print(DEST)
