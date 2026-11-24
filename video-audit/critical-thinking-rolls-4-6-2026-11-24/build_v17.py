"""Build the approved version 5 edit. Source times below are seconds at 30 fps."""
import argparse
import os
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/video"))
from make_close_board import compose_canonical_for_video
from gemini_mark import glyph_mask, inpaint_corner

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROLL = ROOT / "Prompts/critical-thinking-5.mp4"
DONOR = ROOT / "Prompts/critical-thinking-v16.mp4"
DEST = ROOT / "Prompts/critical-thinking-v17.mp4"
ASSETS = ROOT / "course-assets/critical-thinking"
FONT = ROOT / "scripts/video/assets/fonts/PlusJakartaSans-wght.ttf"
FPS, W, H, RATE = 30, 1280, 720, 48000
# The encoded stereo track has 0.828 s of existing quiet at -40 dB.
# Allow for the extra 38 ms exposed by resampling and AAC encoding.
EXTENSION = 2 - 0.828
# Map output time to the unchanged source clocks. The inserted room tone holds the question.
SPANS = [
    ("raw", 0, 34.70), ("raw", 44.60, 47.75), ("quiet", 0, EXTENSION),
    ("raw", 47.75, 100.90), ("donor", 83.86, 89.70),
    ("raw", 109.91, 223.80), ("tail", 0, 1.40)
]

def pcm(path):
    data = subprocess.check_output([FF, "-v", "error", "-i", str(path), "-map", "0:a", "-ac", "2",
                                    "-ar", str(RATE), "-f", "f32le", "-"])
    return np.frombuffer(data, np.float32).reshape(-1, 2)

def rms_voiced(samples):
    levels = np.sqrt(np.mean(np.square(samples[:len(samples)//960*960].reshape(-1,960,2)),axis=(1,2)))
    return np.median(levels[levels > 0.015])

def make_sound(tmp, spans):
    raw = pcm(ROLL)
    has_donor = any(source == "donor" for source, _, _ in spans)
    donor = pcm(DONOR) if has_donor else None
    tone = raw[round(47.55*RATE):round(48.02*RATE)]
    # Alternate directions for seamless joins inside this quiet section.
    loop = np.concatenate([tone,tone[::-1]])
    if has_donor:
        gain = rms_voiced(raw[94*RATE:100*RATE])/rms_voiced(donor[84*RATE:89*RATE])
    track = []
    for source, a, b in spans:
        if source in ("quiet","tail"):
            size = round((b-a)*RATE)
            take = np.tile(loop, (1+size//len(loop),1))[:size].copy()
        else:
            samples = donor if source == "donor" else raw
            take = samples[round(a*RATE):round(b*RATE)].copy()
            if source == "donor":
                take *= min(gain, 0.97 / np.max(np.abs(take)))
        ramp = np.linspace(0,1,240)[:,None]
        take[:240] *= ramp
        take[-240:] *= ramp[::-1]
        track.append(take)
    sound = np.concatenate(track)
    with wave.open(str(tmp / "audio.wav"), "wb") as wav:
        wav.setparams((2,2,RATE,0,'NONE',''))
        wav.writeframes((np.clip(sound,-1,1)*32767).astype('<i2').tobytes())
    return len(sound)/RATE

def face(size, weight=700):
    font = ImageFont.truetype(str(FONT),size)
    font.set_variation_by_axes([weight])
    return font

def title_card(mode):
    im = Image.new('RGB',(W,H),'#f7f4ed')
    draw = ImageDraw.Draw(im)
    if mode == "question":
        draw.text((W/2,H/2),"What’s your first reaction?",font=face(70),fill='#17162b',anchor='mm')
    else:
        draw.text((640,130),"Three headlines. One study.",font=face(56),fill='#17162b',anchor='mm')
        for y,headline in [(266,'Slim by Chocolate'),(344,'Has the world gone coco?'),(422,'Why You Must Eat Chocolate Daily')]:
            draw.text((640,y),headline,font=face(40,500),fill='#343044',anchor='mm')
        draw.line((312,507,968,507),fill='#b5a99b',width=2)
        draw.text((640,575),'Institute of Diet and Health',font=face(35),fill='#292638',anchor='mm')
    return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)

def board(name, rect=None, color=None):
    im=Image.open(ASSETS/('critical-thinking-'+name+'.jpg')).convert('RGB')
    scale=min(W/im.width,H/im.height)
    size=(round(im.width*scale),round(im.height*scale))
    x,y=(W-size[0])//2,(H-size[1])//2
    canvas=Image.new('RGB',(W,H),im.getpixel((2,2)))
    canvas.paste(im.resize(size,Image.Resampling.LANCZOS),(x,y))
    if rect:
        left,top,right,bottom=rect
        ImageDraw.Draw(canvas).rounded_rectangle((x+round(left*scale),y+round(top*scale),x+round(right*scale),y+round(bottom*scale)),radius=12,outline=color,width=4)
    return cv2.cvtColor(np.asarray(canvas),cv2.COLOR_RGB2BGR)

class Reader:
    def __init__(self,path):
        self.cap=cv2.VideoCapture(str(path))
        self.idx=-100
    def at(self,t):
        idx=round(t*FPS)
        if idx!=self.idx:
            if idx!=self.idx+1:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES,idx)
            ok,self.frame=self.cap.read()
            if not ok: raise RuntimeError(f"Missing frame {idx}")
            self.idx=idx
        return self.frame

def build(tmp, version, destination):
    revised = version == 18
    spans = [("same_voice", 104.30, 109.91) if source == "donor" and revised else (source,a,b)
             for source,a,b in SPANS]
    duration=make_sound(tmp, spans)
    raw,donor=Reader(ROLL),Reader(DONOR)
    if revised:
        from headline_graphic import HeadlineGraphic
        clippings = HeadlineGraphic(raw, FONT)
    mask=glyph_mask()
    question,headlines=title_card("question"),title_card("headlines")
    reaction=[board("two-reactions"),board("two-reactions",(42,126,783,818),"#c41f28"),board("two-reactions",(817,126,1558,818),"#0f7a4a")]
    equation=[board("equation"),board("equation",(90,80,750,376),"#1652f0"),board("equation",(850,80,1510,376),"#0e8f86")]
    cards=[board("three-questions")]
    for x,color in [(40,"#4f2fc4"),(557,"#1652f0"),(1075,"#0e8f86")]:
        cards.append(board("three-questions",(x,127,x+484,610),color))
    compose_canonical_for_video(ASSETS/"critical-thinking-close.jpg",tmp/"close.png","#ffffff")
    close=cv2.imread(str(tmp/"close.png"))
    study_overview=donor.at(83.5).copy()
    study_end=donor.at(89.2).copy()
    ends=np.cumsum([b-a for _,a,b in spans])
    close_start=ends[-3]+217.8-109.91
    frame_count=round(duration*FPS)
    cmd=[FF,"-v","error","-n","-f","rawvideo","-pix_fmt","bgr24","-s","1280x720","-r","30","-i","pipe:0","-i",str(tmp/"audio.wav"),"-c:v","libx264","-threads","4","-preset","veryfast","-crf","17","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",str(tmp/"review.mp4")]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for i in range(frame_count):
        t=i/FPS
        k=min(int(np.searchsorted(ends,t,side="right")),len(SPANS)-1)
        source,a,_=spans[k]
        s=a+t-(ends[k-1] if k else 0)
        if t >= close_start:
            progress=np.clip((t-close_start-1.6)/5,0,1)
            zoom=1+.2*(progress**2*(3-2*progress))
            w,h=round(3840/zoom),round(2160/zoom)
            x,y=(3840-w)//2,(2160-h)//2
            frame=cv2.resize(close[y:y+h,x:x+w],(W,H),interpolation=cv2.INTER_AREA)
        elif source=="quiet":
            frame=reaction[0] if revised else question
        elif source=="same_voice":
            frame=donor.at(83.86+(s-104.30))
        elif source=="donor":
            frame=donor.at(s)
        elif 24.0<=s<35:
            frame=clippings.frame(s-24.0) if revised else headlines
        elif 44<=s<48.203447:
            frame=reaction[0] if revised else question
        elif 48.203447<=s<65.35:
            frame=reaction[0 if s<49.7 else 1 if s<55.75 else 2]
        elif 93.55<=s<=101:
            frame=study_overview
        elif 109.90<=s<112.2:
            frame=study_end
        elif 156.6<=s<185.65:
            frame=equation[0 if s<162.2 or s>=179.2 else 1 if s<171 else 2]
        elif 193.7<=s<218:
            frame=cards[0 if s<202.2 else 1 if s<206.8 else 2 if s<212 else 3]
        else:
            frame=inpaint_corner(raw.at(s),mask)
        p.stdin.write(frame.tobytes())
    p.stdin.close()
    if p.wait(): raise RuntimeError("Candidate encode failed")
    # Hard link on the same filesystem so an existing candidate cannot be replaced.
    os.link(tmp/"review.mp4", destination)
    print(f"{destination}: {frame_count} frames, {duration:.3f}s",flush=True)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--version",type=int,choices=(17,18),default=17)
    version=parser.parse_args().version
    destination=DEST.with_name(f"critical-thinking-v{version}.mp4")
    if destination.exists(): sys.exit(f"Already exists: {destination}")
    with tempfile.TemporaryDirectory(dir=destination.parent) as tmp:
        build(Path(tmp), version, destination)
