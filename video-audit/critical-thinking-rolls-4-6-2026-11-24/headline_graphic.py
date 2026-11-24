"""Animate clippings from roll 5 back to their common study."""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1280, 720
INK, RED = '#332923', '#a84530'

def ease(t):
    x = float(np.clip(t, 0, 1))
    return x*x*(3-2*x)

def paper_from_frame(frame, corners, width, height):
    # The coordinates refer to the half-size layout used for art direction.
    quad = np.float32(corners)*2
    dst = np.float32([(0,0),(width-1,0),(width-1,height-1),(0,height-1)])
    mat = cv2.getPerspectiveTransform(quad,dst)
    patch = cv2.warpPerspective(frame,mat,(width,height),flags=cv2.INTER_CUBIC)
    return Image.fromarray(cv2.cvtColor(patch,cv2.COLOR_BGR2RGB)).convert('RGBA')

def rotated_paper(paper, angle):
    tile = Image.new('RGBA',(paper.width+44,paper.height+44))
    shade = Image.new('RGBA',tile.size)
    ImageDraw.Draw(shade).rectangle((23,26,paper.width+23,paper.height+26),fill=(45,31,18,80))
    tile.alpha_composite(shade.filter(ImageFilter.GaussianBlur(6)))
    tile.alpha_composite(paper,(20,18))
    return tile.rotate(angle,Image.Resampling.BICUBIC,expand=True)

class HeadlineGraphic:
    def __init__(self, reader, font_file):
        press = reader.at(14)
        shape = reader.at(19)
        self.clips = [
            rotated_paper(paper_from_frame(press,[(38,71),(294,4),(340,213),(85,274)],347,227),4),
            rotated_paper(paper_from_frame(press,[(370,87),(595,125),(550,338),(328,290)],340,226),-3),
            rotated_paper(paper_from_frame(shape,[(114,54),(527,46),(528,299),(126,312)],360,225),2),
        ]
        rnd = np.random.default_rng(5)
        grain = rnd.normal(0,2.1,(H,W,1))
        self.base = Image.fromarray(np.clip(np.array([232,222,202])+grain,0,255).astype(np.uint8)).convert('RGBA')
        def font(size,weight):
            f=ImageFont.truetype(str(font_file),size)
            f.set_variation_by_axes([weight])
            return f
        self.page=Image.new('RGBA',(978,212),'#fffdf3')
        p=ImageDraw.Draw(self.page)
        p.rectangle((0,0,9,211),fill='#374f58')
        p.text((39,27),'Institute of Diet and Health',font=font(47,760),fill=INK)
        p.line((40,101,935,101),fill='#d3c3a9',width=2)
        self.claim=Image.new('RGBA',self.page.size)
        c=ImageDraw.Draw(self.claim)
        c.text((40,128),'The study claimed dark chocolate could help people lose weight faster.',
               font=font(25,550),fill=INK)
        self.shadow=Image.new('RGBA',(1010,248))
        ImageDraw.Draw(self.shadow).rectangle((15,15,994,226),fill=(49,36,18,75))
        self.shadow=self.shadow.filter(ImageFilter.GaussianBlur(7))
        self.final=None

    def frame(self,t):
        # The paper arrives as the narrator says “study”; its claim follows the attribution.
        if t>=8.5 and self.final is not None:
            return self.final
        canvas=self.base.copy()
        draw=ImageDraw.Draw(canvas)
        for center,start in [(233,1.5),(635,1.75),(1034,2.0)]:
            points=[(center,299),(center,338),(640,383),(640,426)]
            progress=ease((t-start)/1.65)
            for a,b in zip(points,points[1:]):
                width=3
                # Draw each segment in sequence.
                length_fraction=[0.22,0.56,0.22][points.index(a)]
                f=np.clip(progress/length_fraction,0,1)
                if f>0:
                    draw.line((a,(round(a[0]+(b[0]-a[0])*f),round(a[1]+(b[1]-a[1])*f))),fill=RED,width=width)
                progress-=length_fraction
        for i,(clip,cx) in enumerate(zip(self.clips,[233,635,1034])):
            arrival=ease((t-i*.23)/.7)
            y=round(60-370*(1-arrival))
            canvas.alpha_composite(clip,(round(cx-clip.width/2),y))
        rise=ease((t-2.15)/1.05)
        y=round(423+(1-rise)*350)
        canvas.alpha_composite(self.shadow,(135,y-9))
        canvas.alpha_composite(self.page,(151,y))
        fade=ease((t-5.15)/.75)
        if fade>0:
            canvas.alpha_composite(Image.blend(Image.new('RGBA',self.claim.size),self.claim,fade),(151,y))
        frame=cv2.cvtColor(np.asarray(canvas),cv2.COLOR_RGBA2BGR)
        if t>=8.5:
            self.final=frame
        return frame
