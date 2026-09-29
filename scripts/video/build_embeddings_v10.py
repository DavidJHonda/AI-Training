#!/usr/bin/env python3
"""Approved mystery-drink and matching-profile animations, with all v9 fixes."""
import argparse,json,subprocess,functools
from pathlib import Path
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg
import build_embeddings_v9 as v9
from editspec_build import sha

b=v9.base
ROOT=b.ROOT
SRC=b.SRC
DEST=ROOT/'Prompts/embeddings-v10.mp4'
OUT=ROOT/'video-audit/embeddings-cutaways-2026-09-29-v10'
ASSETS=ROOT/'scripts/video/assets/embeddings-cutaways-2026-09-29'
MYSTERY=(2589,2877) # 1:26.3 to 1:35.9
MATCH=(3489,3684)   # 1:56.3 to 2:02.8
SPANS=[b.TASTE,MYSTERY,MATCH,b.DIAGRAM,b.BOARD]
FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
VALUES=[9,1,10,2,3,8]
LABELS=['Sweet','Bitter','Fizz','Heat','Caffeine','Dark']
COLORS=['#b8293f','#0e8f86','#1652f0','#a9760c','#4f2fc4','#27353c']
PALES=['#f7e7eb','#e3f2ef','#e7edfc','#f4eddf','#eee8f7','#e8ebed']
INK='#172429';PURPLE='#6e51ff';BG='#f5f3fb';S=2

def ease(t):
    t=max(0,min(1,t));return t*t*(3-2*t)

@functools.lru_cache(None)
def font(size,bold=False):
    f=ImageFont.truetype(str(FONT),round(size*S))
    if bold:f.set_variation_by_axes([700])
    return f

def txt(d,xy,text,size=28,color=INK,bold=False,anchor='mm'):
    d.text(tuple(round(v*S) for v in xy),text,font=font(size,bold),fill=color,anchor=anchor)

def box(d,r,fill,outline=None,width=1,radius=15):
    d.rounded_rectangle(tuple(round(v*S) for v in r),radius=radius*S,fill=fill,outline=outline,width=width*S)

def sprites():
    source=Image.open(ASSETS/'cans.png').convert('RGBA');w,h=source.size;ans=[]
    for a,z in [(0,w//2),(w//2,w)]:
        cut=source.crop((a,0,z,h))
        # Ignore nearly transparent generation specks when centering each can.
        bb=cut.getchannel('A').point(lambda p:255 if p>96 else 0).getbbox()
        bb=(max(0,bb[0]-2),max(0,bb[1]-2),min(cut.width,bb[2]+2),min(cut.height,bb[3]+2))
        cut=cut.crop(bb)
        ans.append(cut)
    return ans

@functools.lru_cache(None)
def sprite(which,height):
    im=CANS[which];return im.resize((round(im.width*height*S/im.height),round(height*S)),Image.Resampling.LANCZOS)

def can(im,which,cx,top,height,opacity=1,silhouette=False):
    item=sprite(which,height).copy()
    if silhouette:
        a=item.getchannel('A');item=Image.new('RGBA',item.size,'#d9d5e8');item.putalpha(a)
    if opacity<1:item.putalpha(item.getchannel('A').point(lambda x:round(x*opacity)))
    im.alpha_composite(item,(round(cx*S-item.width/2),round(top*S)))

def tiles(d,x,y,width,step,height,size,labelsize,active=(),labels=True):
    for k,(value,label,color,pale) in enumerate(zip(VALUES,LABELS,COLORS,PALES)):
        left=x+k*step
        if labels:txt(d,(left+width/2,y-31),label,labelsize,color,True)
        box(d,(left,y,left+width,y+height),pale)
        if k in active:box(d,(left-4,y-4,left+width+4,y+height+4),None,color,4)
        txt(d,(left+width/2,y+height/2-2),str(value),size,color,True)

def animation(t,kind):
    im=Image.new('RGBA',(1280*S,720*S),BG);d=ImageDraw.Draw(im)
    if kind=='mystery':
        since=t-MYSTERY[0]/30;lift=ease(since/.55)
        reveal=ease((t-94.80)/.23)
        txt(d,(640,76),'Which drink is this?',40,INK,True)
        can(im,0,640,140,225,1-reveal,True)
        if reveal:can(im,0,640,140+12*(1-reveal),225,reveal)
        d=ImageDraw.Draw(im)
        if reveal<.8:txt(d,(640,255),'?',76,PURPLE,True)
        y=322+112*lift
        active=(() if t<89.38 else (0,) if t<90.64 else (1,) if t<91.90 else (2,) if t<93.04 else (0,1,2))
        tiles(d,103,y,150,185,112,49,23,active)
        if reveal>.8:txt(d,(640,622),'Coke',35,INK,True)
    else:
        since=t-MATCH[0]/30;align=ease((t-116.66)/1.5)
        txt(d,(640,74),'Two drinks. The same profile.',38,INK,True)
        can(im,0,330,143,228);can(im,1,950,143,228)
        d=ImageDraw.Draw(im)
        txt(d,(330,401),'Coke',26,'#b8293f',True)
        txt(d,(950,401),'Pepsi',26,'#1652f0',True)
        tiles(d,80,491,72,83,90,38,17)
        tiles(d,713,491+24*(1-align),72,83,90,38,17)
        if t>=117.88:txt(d,(640,535),'=',49,PURPLE,True)
        if t>=119.28:txt(d,(640,642),'The first six numbers cannot tell them apart.',27,INK,True)
    return cv2.cvtColor(np.asarray(im.convert('RGB').resize((1280,720),Image.Resampling.LANCZOS)),cv2.COLOR_RGB2BGR)

CANS=sprites()

def changed(i):return any(a<=i<z for a,z in SPANS)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    b.DEST=DEST;b.OUT=OUT
    renderer,old=b.setup()
    protected={str(p):sha(p) for p in [SRC,ROOT/'lessons/embeddings.md',ASSETS/'cans.png',*sorted((ROOT/'course-assets/embeddings').glob('*.jpg'))]}
    wanted={1500,4200,5377,5770,7996}
    for a,z in [MYSTERY,MATCH]:wanted|={a,a+5,a+18,a+45,(a+z)//2,z-1,z}
    wanted|={round(t*30) for t in [89.4,90.67,91.93,94.8,95.07,116.67,117.9,118.3,119.3,121.6]}
    if args.prepare_only:
        for n in sorted(wanted):
            kind='mystery' if MYSTERY[0]<=n<MYSTERY[1] else 'match' if MATCH[0]<=n<MATCH[1] else None
            if kind:cv2.imwrite(str(OUT/'preview'/f'{n:05d}.jpg'),animation(n/30,kind))
        print('Prepared animation previews');return
    assert not DEST.exists(),'Never overwrite a review candidate'
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
        '-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16',
        '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    cap=cv2.VideoCapture(str(SRC));i=0
    while True:
        ok,im=cap.read()
        if not ok:break
        if MYSTERY[0]<=i<MYSTERY[1]:
            native=im;im=animation(i/30,'mystery')
            # Lift into the isolated profile from the existing table; no hold added.
            q=ease((i-MYSTERY[0]+1)/10)
            if q<1:im=cv2.addWeighted(native,1-q,im,q,0)
        elif MATCH[0]<=i<MATCH[1]:im=animation(i/30,'match')
        elif b.TASTE[0]<=i<b.TASTE[1]:im=v9.taste(im)
        elif b.DIAGRAM[0]<=i<b.DIAGRAM[1]:im=b.diagram(im)
        elif b.BOARD[0]<=i<b.BOARD[1]:im=renderer.at(i-b.BOARD[0])[0]
        if i in wanted:cv2.imwrite(str(OUT/'preview'/f'{i:05d}.jpg'),im)
        proc.stdin.write(im.tobytes());i+=1
        if i%1500==0:print('Frames',i,flush=True)
    cap.release();proc.stdin.close();assert proc.wait()==0;assert i==b.FRAMES
    assert all(sha(Path(p))==h for p,h in protected.items())
    manifest=dict(source=str(SRC),source_sha256=b.EXPECTED,candidate=str(DEST),render_sha256=sha(DEST),frames=i,fps=30,duration=i/30,
        scope='Approved v9 repairs plus both user-approved cutaway animations. Build only, no shipping.',
        changed_spans=[dict(start=a,end=z) for a,z in SPANS],
        boundaries=sorted(set(old['boundaries']+[v for span in SPANS for v in span])),
        protected=protected,audio='Source AAC copied unchanged; no new audio joins.',
        cutaways=[dict(name='Mystery drink',start=MYSTERY[0],end=MYSTERY[1],values=VALUES,
                      spoken_onsets={'Sweet 9':89.38,'Bitter 1':90.64,'Fizz 10':91.90,'Coke reveal':94.80}),
                  dict(name='Matching six-number profiles',start=MATCH[0],end=MATCH[1],values={'Coke':VALUES,'Pepsi':VALUES})],
        board_runs_seconds=[(MYSTERY[0]-1930)/30,(MATCH[0]-MYSTERY[1])/30,(4116-MATCH[1])/30],
        source_limitation='Original raw rolls absent. Rebuilt directly from site v7 and canonical comparison board, not re-encoded from v9.',
        generated_asset=str(ASSETS/'cans.png'),generation_prompt=str(ASSETS/'PROMPT.txt'),
        unperformed='End-to-end listening and continuous audiovisual playback not performed.')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(DEST,flush=True)

if __name__=='__main__':main()
