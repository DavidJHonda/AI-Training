"""Document Trap v8 review cut. All speech, including the short joins, is from roll 2."""
import json
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from shutil import copyfileobj

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from editspec_build import Build, FPS, H, SPF, SR, W, fr, sha
from ken_burns_path import draw_ring, hex_bgr, ring_px
from make_close_board import compose_canonical_for_video
from gemini_mark import glyph_mask, inpaint_corner

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'course-assets/document-trap'
AUDIT = ROOT / 'video-audit/document-trap-v8-2026-11-12'
OUT = ROOT / 'Prompts/document-trap-v8.mp4'
ROLL = {i: ROOT / f'Prompts/document-trap-{i}.mp4' for i in (2, 3)}
FF = imageio_ffmpeg.get_ffmpeg_exe()
FONT = ROOT / 'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
# Audio clips are sample-accurate seconds in roll 2. Picture shots within a row use
# relative seconds; movie in/out points are independent of speech and exclusive at the end.
def movie(roll, a, b): return (roll, a, b)
ROWS = [
 ('Opening: league, question, five, memory, rulebook', [(0,35.80)], [
 (0,movie(3,0,5.8)),(6.23,movie(3,6,12.7)),(11.93,movie(3,13.7,18.67)),
 (15.57,movie(3,19.1,23.1)),(20.73,movie(3,24.0,32.75)),
 (28.21,movie(3,33.4,37.2)),(32.10,movie(3,37.7,42.7))]),
 ('Tournament exception', [(35.80,43.0)],[(0,movie(3,33.5,36.7)),(3.88,'comparison')]),
 ('Incomplete answer', [(43.0,50.64)],[(0,'incomplete')]),
 ('What uploading means',[(50.64,67.24)],[(0,movie(2,50.64,61.90)),(11.26,movie(2,61.90,67.24))]),
 ('Long-file explanation: might, from the same narrator',[(67.24,70.596),(62.795,63.064),(70.932,75.33)],[(0,movie(2,67.24,75.33))]),
 ('What was missing from the question',[(75.33,92.88)],[(0,movie(2,75.33,84.7)),(9.37,'first-answer')]),
 ('Revised tournament question',[(103.84,110.89)],[(0,'prompt')]),
 ('Answer to the revised question',[(110.89,119.66)],[(0,'prompt-answer')]),
 ('Four tips overview',[(130.25,139.26)],[(0,'tips')]),
 ('Name the section',[(139.26,148.02)],[(0,'tip1')]),
 ('Ask one thing',[(148.02,150.33)],[(0,'tip2')],1.0),
 ('Share what matters by pasting only the relevant section',[(157.27,159.49),(169.019,169.21),(163.07,164.855)],[(0,'tip3')],.70),
 ('Ask for the quote and check it',[(166.06,176.81)],[(0,'tip4'),(6.08,movie(2,177.4,182.07))]),
 ('The moves do not guarantee a complete answer',[(176.81,182.72)],[(0,movie(2,180.0,185.91))]),
 ('Examples beyond the court: can hide conditions',[(185.90,197.44),(200.178,200.326),(198.067,202.44)],[(0,movie(2,187.50,191.25)),(5.75,movie(2,191.3,194.0))]),
 ('Canonical close',[(205.97,212.03)],[(0,'close')]),
]

def rgb_frame(im): return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)

@lru_cache(None)
def font(size,weight):
    f=ImageFont.truetype(str(FONT),size)
    f.set_variation_by_axes([weight])
    return f

def graphic(key):
    im=Image.new('RGB',(W,H),'#f4f1fc'); d=ImageDraw.Draw(im)
    navy='#201b35'; violet='#5237ae'
    def label(x,y,text,size,weight=650,color=navy): d.text((x,y),text,font=font(size,weight),fill=color,anchor='lt')
    if key=='comparison':
        label(82,83,'In this league’s rulebook',54,780)
        for x,name,n,accent in [(82,'Regular season','5','#5136a4'),(660,'Tournament','6','#17635a')]:
            d.rounded_rectangle((x,208,x+535,580),24,fill='white')
            label(x+44,253,name,36,700,accent);label(x+44,343,n,130,780,accent);label(x+157,409,'fouls',50)
    elif key=='first-answer':
        label(82,83,'Why the first answer said five',52,780)
        for x in (82,711):
            d.rounded_rectangle((x,211,x+485,555),24,fill='white')
        label(118,252,'In the rulebook',36,740)
        label(118,362,'Regular season: 5 fouls',31,680,violet)
        label(118,455,'Tournament: 6 fouls',31,680,'#17635a')
        label(747,252,'In the first answer',36,740)
        label(747,362,'Regular season: 5 fouls',31,680,violet)
        label(747,455,'Tournament rule missed',31,550,'#615b70')
        d.line((583,382,688,382),fill=violet,width=5)
        d.polygon([(689,382),(670,370),(670,394)],fill=violet)
    else:
        label(84,76,'The revised question',52,780)
        d.rounded_rectangle((84,184,1196,434),26,fill='white')
        d.rounded_rectangle((84,215,94,402),5,fill=violet)
        label(124,233,'In tournament games, how many fouls are allowed?',39,650)
        label(124,328,'Quote the rule and any exceptions.',39,650)
        if key=='prompt-answer':
            d.rounded_rectangle((84,483,1196,631),20,fill='#e1f2ed')
            label(124,510,'In this league’s tournament games',27,690,'#185c51')
            label(124,558,'Six fouls.',42,780,'#184e45')
    return rgb_frame(im)

def make_boards(work):
    build=Build(ROOT,ROLL[2],work,OUT)
    boards={k:graphic(k) for k in ('comparison','first-answer','prompt','prompt-answer')}
    for key,filename in [('incomplete','uploaded'),('tips','moves')]:
        p,_,_,ox,oy=build.compose(ASSETS/f'document-trap-{filename}.jpg',key)
        img=cv2.imread(str(p))
        boards[key]=cv2.resize(img,(W,H),interpolation=cv2.INTER_AREA)
        if key=='tips':
            for i,(x0,y0,x1,y1,color) in enumerate([
              (40,128,784,679,'#4f2fc4'),(816,128,1560,679,'#1652f0'),
              (40,708,784,1259,'#0e8f86'),(816,708,1560,1259,'#a9760c')],1):
                x0+=ox;x1+=ox;y0+=oy;y1+=oy
                width=round(Build.fit_w(x1-x0,y1-y0));height=round(width*H/W)
                left=(x1+x0-width)//2;top=(y1+y0-height)//2
                # Stage the whole card alone; a crop of the full board would leave
                # half a neighboring heading at the edge of a widescreen frame.
                stage=np.empty((height,width,3),dtype=np.uint8)
                stage[:]=img[oy+100,ox+12]
                pad=5
                stage[y0-top-pad:y1-top+pad,x0-left-pad:x1-left+pad]=img[y0-pad:y1+pad,x0-pad:x1+pad]
                pic=cv2.resize(stage,(W,H),interpolation=cv2.INTER_CUBIC)
                s=W/width;stroke=ring_px(H);half=stroke/2
                draw_ring(pic,(x0-left)*s-half,(y0-top)*s-half,(x1-left)*s+half,(y1-top)*s+half,
                          hex_bgr(color),14*s+half,stroke)
                boards[f'tip{i}']=pic
    compose_canonical_for_video(ASSETS/'document-trap-close.jpg',work/'close.png','#ffffff')
    boards['close']=cv2.resize(cv2.imread(str(work/'close.png')),(W,H),interpolation=cv2.INTER_AREA)
    return boards

def main():
    if OUT.exists(): raise FileExistsError(OUT)
    cv2.setNumThreads(2); AUDIT.mkdir(exist_ok=True,parents=True)
    with tempfile.TemporaryDirectory() as tmp:
        work=Path(tmp)
        x=np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(ROLL[2]),'-vn','-ar',str(SR),'-ac','1','-f','f32le','-']),'<f4')
        pieces=[];rows=[];cursor=0
        for label,clips,shots,*tail in ROWS:
            chunks=[]
            for a,b in clips:
                y=x[round(a*SR):round(b*SR)].copy()
                # 4 ms de-click; unopened beginning has no ramp.
                if cursor or chunks: y[:192]*=np.linspace(0,1,192)
                y[-192:]*=np.linspace(1,0,192);chunks.append(y)
            sound=np.concatenate(chunks);n=int(np.ceil(len(sound)/SPF))+fr(tail[0] if tail else 0)
            pieces.append(np.pad(sound,(0,n*SPF-len(sound))))
            rows.append(dict(label=label,start_frame=cursor,frames=n,roll_2_audio=clips,shots=shots));cursor+=n
        np.concatenate(pieces).tofile(work/'voice.f32')
        boards=make_boards(work); mask=glyph_mask()
        dest=work/'encoded.mp4'
        args=[FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
              '-f','f32le','-ar',str(SR),'-ac','1','-i',str(work/'voice.f32'),'-c:v','libx264',
              '-preset','fast','-threads','4','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
              '-movflags','+faststart',str(dest)]
        proc=subprocess.Popen(args,stdin=subprocess.PIPE)
        try:
            for row in rows:
                shots=row['shots']
                for j,(t,pic) in enumerate(shots):
                    end=fr(shots[j+1][0]) if j+1<len(shots) else row['frames']
                    n=end-fr(t);assert n>0
                    if isinstance(pic,str):
                        raw=boards[pic].tobytes()
                        for _ in range(n):proc.stdin.write(raw)
                    else:
                        roll,a,b=pic;lo,hi=fr(a),fr(b);c=cv2.VideoCapture(str(ROLL[roll]))
                        c.set(cv2.CAP_PROP_POS_FRAMES,lo);current=lo-1
                        for k in range(n):
                            goal=lo+k*(hi-lo)//n
                            while current<goal:
                                ok,frame=c.read();assert ok;current+=1
                            proc.stdin.write(inpaint_corner(frame,mask).tobytes())
                        c.release()
                print(row['label'],flush=True)
        finally:proc.stdin.close()
        if proc.wait():raise RuntimeError('Failed to encode')
        with OUT.open('xb') as destfile,dest.open('rb') as source:copyfileobj(source,destfile)
        inputs=[*ROLL.values(),*(ASSETS/f'document-trap-{k}.jpg' for k in ['uploaded','moves','close'])]
        manifest=dict(candidate=str(OUT.relative_to(ROOT)),sha256=sha(OUT),frames=cursor,seconds=cursor/FPS,
                      inputs={str(p.relative_to(ROOT)):sha(p) for p in inputs},timeline=rows)
        (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        print(f'{OUT}: {cursor/FPS:.3f}s',flush=True)

if __name__=='__main__':main()
