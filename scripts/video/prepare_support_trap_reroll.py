#!/usr/bin/env python3
"""Prepare Support Trap reroll JPGs without modifying page assets or videos."""
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
 ("support-trap-1-comparison.jpg","support-trap-comparison-v2.jpg",False),
 ("support-trap-2-role.jpg","support-trap-real-vs-missing-v2.jpg",True),
 ("support-trap-3-danger.jpg","support-trap-danger-v2.jpg",True),
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
    audit=ROOT/"video-audit/support-trap-reroll-materials-2026-09-07"
    audit.mkdir(parents=True,exist_ok=True)
    html=(ROOT/"index.html").read_text()
    protected=[ROOT/"index.html",ROOT/"videos/support-trap.mp4"]+[ROOT/"illustrations"/s for _,s,_ in SOURCES]
    original={str(p):sha(p) for p in protected}
    rows=[]
    for name,source,upload in SOURCES:
        src=ROOT/"illustrations"/source;target=ROOT/"lessons"/name
        assert "illustrations/"+source in html
        shutil.copy2(src,target)
        with Image.open(target) as im:w,h=im.size
        rows.append(dict(file=str(target.relative_to(ROOT)),source=str(src.relative_to(ROOT)),
                         notebook_upload=upload,sha256=sha(target),source_sha256=sha(src),width=w,height=h))
    im,geometry=render_comparison()
    path=ROOT/"lessons/support-trap-1-comparison-notebook.jpg"
    im.save(path,quality=95,subsampling=0,optimize=True)
    rows.insert(1,dict(file=str(path.relative_to(ROOT)),source="scripts/video/prepare_support_trap_reroll.py",
                      notebook_upload=True,sha256=sha(path),width=im.width,height=im.height,
                      purpose="Face-free upload surrogate; replace with illustrated comparison in final video.",
                      geometry=geometry))
    pill,sticky=close_board_copy("supporttrap")
    md=ROOT/"lessons/support-trap.md";prompt=ROOT/"Prompts/support-trap-video-prompt.txt"
    assert pill in md.read_text() and sticky in md.read_text()
    close=ROOT/"lessons/support-trap-4-close.jpg"
    with Image.open(close) as im:
        assert im.size==(3840,2160)
    rows.append(dict(file=str(close.relative_to(ROOT)),source="index.html:CLOSE_BOARDS.supporttrap",
                     notebook_upload=True,sha256=sha(close),width=3840,height=2160,pill=pill,sticky=sticky,
                     note="Existing current close verified and retained; no redesign."))
    words=len(prompt.read_text().split());assert words<=500
    assert all(sha(Path(p))==h for p,h in original.items())
    entry=dict(lesson="support-trap",section_id="supporttrap",prepared="2026-09-07",
               markdown=str(md.relative_to(ROOT)),markdown_sha256=sha(md),markdown_words=len(md.read_text().split()),
               prompt=str(prompt.relative_to(ROOT)),prompt_sha256=sha(prompt),prompt_words=words,boards=rows)
    manifest=ROOT/"Prompts/AVOID-TRAPS-SOURCE-MANIFEST.json"
    data=json.loads(manifest.read_text())
    data["lessons"]=[entry if e["lesson"]=="support-trap" else e for e in data["lessons"]]
    # Mechanical update only; preserve all other lesson entries.
    manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
    (audit/"manifest.json").write_text(json.dumps(dict(**entry,protected_unchanged=original),ensure_ascii=False,indent=2)+"\n")
    sheet=Image.new("RGB",(1600,1300),"white");d=ImageDraw.Draw(sheet)
    for i,row in enumerate(rows):
        img=Image.open(ROOT/row["file"]);img.thumbnail((510,570))
        x=(i%3)*533;y=(i//3)*650
        d.text((x+8,y+8),Path(row["file"]).name,fill="black")
        d.text((x+8,y+28),"UPLOAD" if row["notebook_upload"] else "POST ONLY",fill="black")
        sheet.paste(img,(x+8,y+58))
    sheet.save(audit/"contact-sheet.jpg",quality=90)
    print(json.dumps({"prompt_words":words,"md_words":entry["markdown_words"],"boards":rows},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
