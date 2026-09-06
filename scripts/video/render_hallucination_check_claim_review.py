"""Review-only EE-FLOW. No lesson, prep, or video asset is replaced."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
from editorial_typography import (face, draw_board_title, draw_inner_title,
                                  tracked_width, INNER_TITLE_TRACKING)
from render_embrace_editorial_batch import (wrap, cover, rounded_mask, accent_wash,
    mix_with_white, centered_lines, arrow, PURPLE, BLUE, TEAL, BODY, MUTED, WHITE)

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'board-review-hallucination'
STEPS=(
    ('Notice the Claim', 'Something doesn’t add up. Identify the fact, number, or study you want to check.', 'notice-claim.png', PURPLE),
    ('Find the Source', 'Look for the original study, article, or document. A citation alone isn’t proof.', 'find-source.png', BLUE),
    ('Check the Match', 'Does the source exist, and does it actually support what AI said?', 'check-match.png', TEAL),
)

def main():
    title_font=face('bold',40)
    body_font=face('medium',29)
    measure=ImageDraw.Draw(Image.new('RGB',(1,1)))
    bodies=[]
    for title,body,_,_ in STEPS:
        assert '\u2014' not in title+body
        assert tracked_width(measure,title,title_font,INNER_TITLE_TRACKING)<=430
        bodies.append(wrap(measure,body,body_font,420))
    art_width=430;art_height=round(art_width*9/16)
    art_top=175;marker_y=art_top+art_height+45
    title_y=marker_y+49;body_y=title_y+59
    stage_bottom=body_y+max(map(len,bodies))*41+45
    im=Image.new('RGB',(1600,stage_bottom+40),WHITE)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,1599,im.height-1),radius=22,fill='#eae7fd')
    draw_board_title(d,'Check the Claim')
    d.rounded_rectangle((40,127,1560,stage_bottom),radius=14,fill=WHITE)
    lefts=(70,585,1100)
    geometry=[]
    for i,((title,body,asset,accent),lines,left) in enumerate(zip(STEPS,bodies,lefts),1):
        panel=Image.open(OUT/'assets'/asset).convert('RGB')
        art=accent_wash(cover(panel,(art_width,art_height)),accent)
        im.paste(art,(left,art_top),rounded_mask((art_width,art_height),14))
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((left,art_top,left+art_width,art_top+art_height),radius=14,
            outline=mix_with_white(accent,.22),width=1)
        center=left+art_width//2
        d.ellipse((center-29,marker_y-29,center+29,marker_y+29),fill=accent)
        d.text((center,marker_y),str(i),font=face('heavy',26),fill=WHITE,anchor='mm')
        draw_inner_title(d,(center,title_y),title,fill=accent,anchor='ma')
        centered_lines(d,center,body_y,lines,body_font,BODY,41)
        geometry.append({'title':title,'body':body,'accent':accent,
            'illustration_bounds':[left,art_top,left+art_width,art_top+art_height],
            'complete_step_bounds':[left,art_top,left+art_width,stage_bottom-20]})
    for left,right in zip(lefts,lefts[1:]):
        arrow(d,(left+art_width+12,art_top+art_height//2),
            (right-12,art_top+art_height//2),MUTED)
    path=OUT/'check-the-claim.jpg'
    im.save(path,quality=95,subsampling=0,optimize=True)
    im.resize((880,round(im.height*880/1600)),Image.Resampling.LANCZOS).save(OUT/'check-the-claim-lesson-size.png')
    (OUT/'geometry.json').write_text(json.dumps({'format':'EE-FLOW','size':im.size,
        'title':'Check the Claim','takeaway':None,'steps':geometry},indent=2)+'\n')
    print(path,im.size,[len(lines) for lines in bodies])

if __name__=='__main__': main()
