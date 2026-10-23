"""Canonical Evaluation Matters EE-FLOW, using Check the Claim geometry."""
from pathlib import Path
import json
from PIL import Image, ImageDraw
from editorial_typography import (face, draw_board_title, draw_inner_title,
                                  tracked_width, INNER_TITLE_TRACKING)
from render_embrace_editorial_batch import (wrap, cover, rounded_mask, accent_wash,
    mix_with_white, centered_lines, arrow, PURPLE, BLUE, TEAL, BODY, MUTED, WHITE)

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'tmp/evaluation-flow'
ASSETS=ROOT/'scripts/video/assets/evaluation-flow'
OUTPUT=ROOT/'course-assets/evaluation-matters/evaluation-matters-process.jpg'
STEPS=(
    ('Do a Quick Review', 'Read. Understand. Validate.', 'review.png', PURPLE),
    ('Take a Closer Look', 'If needed, dig deeper. Choose the checks that fit.', 'closer.png', BLUE),
    ('Make Your Move', 'Decide what to do with the answer.', 'move.png', TEAL),
)


def render(board_title, steps, assets, output, out, step_number=None):
    out.mkdir(parents=True,exist_ok=True)
    title_font=face('bold',40)
    body_font=face('medium',29)
    measure=ImageDraw.Draw(Image.new('RGB',(1,1)))
    bodies=[]
    for title,body,_,_ in steps:
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
    if step_number is None:
        draw_board_title(d,board_title)
    else:
        # Same 58px circle and 26px heavy numeral as the overview markers.
        d.ellipse((40,39,98,97),fill=PURPLE)
        d.text((69,68),str(step_number),font=face('heavy',26),fill=WHITE,anchor='mm')
        draw_board_title(d,board_title,x=118)
    d.rounded_rectangle((40,127,1560,stage_bottom),radius=14,fill=WHITE)
    lefts=(70,585,1100)
    geometry=[]
    for i,((title,body,asset,accent),lines,left) in enumerate(zip(steps,bodies,lefts),1):
        panel=Image.open(assets/asset).convert('RGB')
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
    d.text((1560,im.height-10),'besmarterthanthetool.com',font=face('medium',20),fill='#625c7a',anchor='rd')
    path=output
    im.save(path,quality=95,subsampling=0,optimize=True)
    im.resize((880,round(im.height*880/1600)),Image.Resampling.LANCZOS).save(out/'lesson-size.png')
    (out/'geometry.json').write_text(json.dumps({'format':'EE-FLOW','size':im.size,
        'title':board_title,'takeaway':None,'steps':geometry},indent=2)+'\n')
    print(path,im.size,[len(lines) for lines in bodies])

def main():
    render('How to Evaluate an AI Answer', STEPS, ASSETS, OUTPUT, OUT)

if __name__=='__main__': main()
