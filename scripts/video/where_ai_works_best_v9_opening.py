"""Approved v9 opener: source-roll label repair and one extra second for the donor clause."""
from pathlib import Path
import json, subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/where-ai-works-best-v9-2026-09-29'
R3=ROOT/'Prompts/where-ai-works-best-3.mp4'
# Audio: replace R3 [91,141) with R1 [3306,3386): +30 frames.
CUT_IN,CUT_OUT,DONOR_IN,DONOR_OUT=91,141,3306,3386
DELTA=(DONOR_OUT-DONOR_IN)-(CUT_OUT-CUT_IN)

def opening_clip(path):
    if path.exists(): return
    cap=cv2.VideoCapture(str(R3)); frames=[]
    for i in range(403):
        ok,im=cap.read(); assert ok; frames.append(im)
    cap.release()
    # Track the original text's small entrance translation and its opacity.
    ref=frames[180]; gray=cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY)
    template=gray[179:226,300:402]
    glyph=(template<225).astype(np.uint8)
    glyph=cv2.dilate(glyph,np.ones((3,3),np.uint8))
    ink=(template<90)
    scale=4
    masks=[]
    for text,size,font,y in [('Essay Ideas',18,'Arial Bold.ttf',0),('Brainstorming',13,'Arial.ttf',30)]:
        canvas=Image.new('L',(120*scale,55*scale))
        d=ImageDraw.Draw(canvas)
        f=ImageFont.truetype('/System/Library/Fonts/Supplemental/'+font,size*scale)
        d.text((0,y*scale),text,font=f,fill=255,anchor='lt')
        masks.append(np.asarray(canvas.resize((120,55),Image.Resampling.LANCZOS))/255.)
    records=[]; patched=[]
    for i,original in enumerate(frames):
        im=original.copy()
        if i>=104:
            g=cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
            search=g[145:250,270:440]
            response=cv2.matchTemplate(search,template,cv2.TM_CCOEFF_NORMED)
            _,score,_,loc=cv2.minMaxLoc(response)
            x,y=270+loc[0],145+loc[1]
            roi=g[y:y+47,x:x+102]
            bg=float(np.median(roi[template>245]))
            opacity=float(np.clip(np.median((bg-roi[ink])/(250.-template[ink])),0,1))
            if score>.25 and opacity>.015:
                # Repair glyphs only, retaining the card, icon, connector, and background motion.
                mask=np.zeros(g.shape,np.uint8)
                mask[y:y+47,x:x+102]=glyph*255
                im=cv2.inpaint(im,mask,3,cv2.INPAINT_TELEA)
                nx,ny=x-15,y+3
                area=im[ny:ny+55,nx:nx+120].astype(float)
                for a,color in zip(masks,[35.,112.]):
                    alpha=(a*opacity)[...,None]
                    area=area*(1-alpha)+color*alpha
                im[ny:ny+55,nx:nx+120]=np.clip(area+.5,0,255).astype(np.uint8)
                records.append(dict(frame=i,xy=[x,y],score=round(score,4),opacity=round(opacity,4)))
        patched.append(im)
    # Slow only the original Essay emphasis: all original frames remain in order.
    # Repeat the fully drawn, highlighted Essay frame at 150 for 30 extra frames.
    # Schedule's emphasis and all later motion then follow the revised narration.
    mapping=list(range(151))+[150]*DELTA+list(range(151,403))
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    p=subprocess.Popen([ff,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-c:v','ffv1','-level','3',str(path)],stdin=subprocess.PIPE)
    for f in mapping:p.stdin.write(patched[f].tobytes())
    p.stdin.close();assert p.wait()==0
    (OUT/'opening-label-tracking.json').write_text(json.dumps(records,indent=2))
    cells=[]
    for i in [106,108,110,112,114,116,120,135,150,180,240,270,300,330,360,402]:
        crop=patched[i][130:285,170:425].copy()
        cv2.putText(crop,str(i),(3,150),0,.5,(0,0,255),1);cells.append(crop)
    cv2.imwrite(str(OUT/'label-repair-sheet.png'),np.vstack([np.hstack(cells[k:k+4]) for k in range(0,len(cells),4)]))
    cv2.imwrite(str(OUT/'opening-label-settled.png'),patched[180])
    print('Opening clip:',len(mapping),'frames; tracked label:',len(records),'frames',flush=True)

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    opening_clip(OUT/'r3-opening-patched.mkv')
