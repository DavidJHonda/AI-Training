#!/usr/bin/env python3
"""Prepare Support Trap reroll JPGs without modifying page assets or videos."""

try:
    from .course_credit import save_course_image
except ImportError:
    from course_credit import save_course_image


try:
    from .course_asset_paths import asset_path, asset_dir
except ImportError:
    from course_asset_paths import asset_path, asset_dir

import hashlib,json,shutil
from pathlib import Path
from PIL import Image,ImageDraw
from editorial_typography import face,draw_board_title,draw_inner_title
from editorial_takeaway import draw_takeaway_band,TAKEAWAY_HEIGHT
from render_embrace_editorial_batch import wrap,multiline,BLUE,AMBER,FRAME,WHITE,BODY,PURPLE,mix_with_white
from make_close_board import close_board_copy

ROOT=Path(__file__).resolve().parents[2]
# Same words, order, accents, and conclusions as the illustrated page board.
TITLE="Supportive Words versus Support"
SCENARIO="“I’ve been eating lunch alone for like two weeks.”"
SIDES=(
 ("PERSON","Your Older Sister","“Come sit with me and Jess tomorrow. We’re at the table by the windows.”",
  (("HEARD YOU","And did something."),("TOMORROW","She will look for you."),("CHANGED","Tomorrow’s lunch.")),BLUE),
 ("AI","The Chatbot","“I’m sorry. Eating alone can feel isolating. Would you like strategies for connecting with classmates?”",
  (("FOUND","Caring words."),("TOMORROW","It cannot show up."),("CHANGED","Nothing outside the chat.")),AMBER),
)
TAKEAWAY="Supportive language is not the same as support."
SOURCES=(
 ("support-trap-comparison.jpg","support-trap-comparison-v2.jpg",False),
 ("support-trap-role.jpg","support-trap-real-vs-missing-v2.jpg",True),
 ("support-trap-danger.jpg","support-trap-danger-v2.jpg",True),
)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def render_comparison():
    # Text-only export using the existing Editorial typography and comparison
    # structure. No raster alteration, face masking, or fabricated illustration.
    measure=ImageDraw.Draw(Image.new("RGB",(1,1)))
    body=face("medium",29);label=face("heavy",20);scenario_font=face("medium",32)
    answers=[wrap(measure,s[2],body,676) for s in SIDES]
    sections=[[wrap(measure,t,body,676) for _,t in s[3]] for s in SIDES]
    max_answer=max(map(len,answers));peers=[max(len(s[i]) for s in sections) for i in range(3)]
    scenario_top=112;scenario_bottom=239;top=271
    # Pill, title, answer, and three measured teaching groups; no art header.
    answer_y=top+138
    section_y=answer_y+max_answer*41+40
    bottom=section_y+sum(40+n*41+(38 if i<2 else 0) for i,n in enumerate(peers))+34
    footer=bottom+40
    im=Image.new("RGB",(1600,footer+TAKEAWAY_HEIGHT+40),WHITE);d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,1599,im.height-1),radius=22,fill=FRAME)
    draw_board_title(d,TITLE)
    d.rounded_rectangle((40,scenario_top,1560,scenario_bottom),radius=18,fill=WHITE)
    d.rectangle((40,scenario_top+18,47,scenario_bottom-18),fill=PURPLE)
    d.text((72,scenario_top+20),"THE SCENARIO",font=label,fill=PURPLE)
    d.text((72,scenario_top+54),SCENARIO,font=scenario_font,fill=BODY)
    geometry=[]
    for idx,(side,x) in enumerate(zip(SIDES,(40,816))):
        role,title,answer,groups,accent=side
        d.rounded_rectangle((x,top,x+744,bottom),radius=18,fill=WHITE,outline=mix_with_white(accent,.2),width=1)
        px=x+34;py=top+32
        pw=round(d.textlength(role,font=label))+28
        d.rounded_rectangle((px,py,px+pw,py+30),radius=15,fill=mix_with_white(accent,.12))
        d.text((px+14,py+15),role,font=label,fill=accent,anchor="lm")
        draw_inner_title(d,(px,py+40),title,fill=accent)
        multiline(d,(px,answer_y),answers[idx],body,BODY,41)
        y=section_y
        for i,((heading,_),lines) in enumerate(zip(groups,sections[idx])):
            d.text((px,y),heading,font=label,fill=accent)
            multiline(d,(px,y+40),lines,body,BODY,41)
            y+=40+peers[i]*41+(38 if i<2 else 0)
        assert y+34==bottom
        geometry.append({"title":title,"bounds":[x,top,x+744,bottom],"accent":accent})
    draw_takeaway_band(im,top=footer,left=40,right=1560,text=TAKEAWAY,font=face("medium",30))
    return im,geometry
def main():
    raise SystemExit("Retired preparation workflow. Rebuild Support Trap from its current lesson under scripts/video/PREPARATION.md; do not reuse the September 7 kit.")

if __name__=="__main__":main()
