#!/usr/bin/env python3
"""Approved 2026-09-30 Your Choices repair; new review candidate only."""
from pathlib import Path
import sys, json, hashlib, subprocess, wave, argparse
import cv2
import numpy as np
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts/video'))
from audio_gap_review import decode_audio, write_wav, dbfs
from gemini_mark import clean_frame, glyph_mask
from make_close_board import compose_canonical_for_video

parser=argparse.ArgumentParser()
parser.add_argument('--version',type=int,default=3)
VERSION=parser.parse_args().version
A = ROOT/f'video-audit/your-choices-build-2026-09-30-v{VERSION}'
DEST = ROOT/f'Prompts/your-choices-v{VERSION}.mp4'
SOURCES = {'roll1': ROOT/'Prompts/your-choices-1.mp4',
           'roll2': ROOT/'Prompts/your-choices-2.mp4',
           'installed': ROOT/'course-assets/your-choices/your-choices.mp4'}
FPS=30; RATE=44100; SPF=1470; W=1280; H=720
FF=imageio_ffmpeg.get_ffmpeg_exe()
# All cuts are inside measured low-energy gaps, not at ASR word boundaries.
LEGS=[('roll2',0,342),('roll1',452,722),('roll2',580,1365),
      ('installed',1217,3545),('installed',3675,4863)]
COLORS=['#4f2fc4','#1652f0','#0e8f86','#a9760c']
FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
INK='#202938'; MUTED='#637081'; PAPER='#fafaf6'

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def font(size,weight=600):
    f=ImageFont.truetype(str(FONT),size*2)
    f.set_variation_by_axes([weight]);return f

def paper():
    im=Image.new('RGB',(2560,1440),PAPER);d=ImageDraw.Draw(im)
    for x in range(28,2560,40):
        for y in range(28,1440,40):d.ellipse((x,y,x+2,y+2),fill='#e1e5e4')
    return im

def txt(d,xy,s,size=26,color=INK,weight=600,anchor='mm'):
    d.text(tuple(v*2 for v in xy),s,font=font(size,weight),fill=color,anchor=anchor)
def line(d,coords,fill,width=3):d.line([tuple(v*2 for v in p) for p in coords],fill=fill,width=width*2,joint='curve')
def rr(d,box,fill,outline=None,width=3,r=20):
    d.rounded_rectangle(tuple(v*2 for v in box),radius=r*2,fill=fill,outline=outline,width=width*2)
def circ(d,x,y,r,fill,outline=None,width=3):d.ellipse(((x-r)*2,(y-r)*2,(x+r)*2,(y+r)*2),fill=fill,outline=outline,width=width*2)
def icon(d,x,y,kind,color):
    if kind==0:
        rr(d,(x-27,y-21,x+27,y+21),None,color,3,5)
        line(d,[(x-27,y-8),(x+27,y-8)],color)
        for k in range(3):circ(d,x-17+k*8,y-15,1.5,color)
    elif kind==1:
        for k in range(3):rr(d,(x-25+k*5,y-23+k*16,x+15+k*5,y-14+k*16),color,r=3)
    elif kind==2:
        line(d,[(x-27,y+14),(x,y-14),(x+27,y+14)],color)
        for xx,yy in [(x-27,y+14),(x,y-14),(x+27,y+14)]:circ(d,xx,yy,7,PAPER,color)
    else:
        circ(d,x-5,y-5,20,None,color)
        line(d,[(x+10,y+10),(x+29,y+29)],color,5)

def overview(stage=3,mode='intro'):
    im=paper();d=ImageDraw.Draw(im)
    title={'intro':'Start with an app. Know your choices.',
           'available':'Your first choice is the app.',
           'reassure':'Understand each choice when it appears.',
           'recap':'App. Model. Reasoning. Research.'}[mode]
    txt(d,(640,73),title,34,weight=750)
    rr(d,(440,150,840,268),'#ffffff',COLORS[0],3,26)
    icon(d,504,209,0,COLORS[0]);txt(d,(645,192),'App',30,COLORS[0],750)
    txt(d,(648,233),'Your home base',20,MUTED,500)
    labels=['Model','Reasoning','Research']
    subs=['Which model','How much effort','Whether to research']
    for i,x in enumerate([260,640,1020]):
        if i>=stage:continue
        c=COLORS[i+1]
        line(d,[(640,270),(640,307),(x,307),(x,355)],'#aebbbf',3)
        circ(d,x,416,58,'#ffffff',c,3);icon(d,x,416,i+1,c)
        txt(d,(x,509),labels[i],30,c,750);txt(d,(x,550),subs[i],20,MUTED,500)
    footer='Available choices depend on the app and your subscription.'
    if mode=='reassure':footer='You do not need to see every choice.'
    if mode=='recap':footer='Use the default when it works.'
    txt(d,(640,644),footer,24,INK,550)
    return cv2.cvtColor(np.array(im.resize((W,H),Image.Resampling.LANCZOS)),cv2.COLOR_RGB2BGR)

def model_diagram():
    im=paper();d=ImageDraw.Draw(im)
    txt(d,(640,88),'One app can offer a family of models.',36,weight=750)
    rr(d,(175,165,1105,596),'#ffffff','#bec9cf',3,28)
    line(d,[(175,220),(1105,220)],'#bec9cf',2)
    for k,c in enumerate(COLORS[:3]):circ(d,204+k*20,193,5,c)
    txt(d,(640,194),'Your app',20,MUTED,600)
    for x,name,sub,c in [(410,'Everyday','Most tasks',COLORS[1]),(870,'More capable','Difficult work',COLORS[0])]:
        circ(d,x,343,58,PAPER,c);icon(d,x,343,1,c)
        txt(d,(x,445),name,31,c,750);txt(d,(x,493),sub,23,MUTED,500)
    txt(d,(640,652),'Choose the model that fits the task.',25,weight=550)
    return cv2.cvtColor(np.array(im.resize((W,H),Image.Resampling.LANCZOS)),cv2.COLOR_RGB2BGR)

def board(file,active=None):
    im=Image.open(file).convert('RGB');sw,sh=im.size
    scale=min(W/sw,H/sh);nw,nh=round(sw*scale),round(sh*scale)
    x,y=(W-nw)//2,(H-nh)//2
    canvas=Image.new('RGB',(W,H),im.getpixel((15,15)))
    canvas.paste(im.resize((nw,nh),Image.Resampling.LANCZOS),(x,y))
    if active is not None:
        d=ImageDraw.Draw(canvas);left=40 if active==0 else 816;right=784 if active==0 else 1560
        bottom=797 if sh==837 else 840
        rect=(round(x+left*scale),round(y+127*scale),round(x+right*scale),round(y+bottom*scale))
        color=COLORS[active] if sh==837 else COLORS[active+2]
        d.rounded_rectangle(rect,radius=10,outline=color,width=4)
    return cv2.cvtColor(np.array(canvas),cv2.COLOR_RGB2BGR)

class Reader:
    def __init__(self,p):self.cap=cv2.VideoCapture(str(p));self.i=-1;self.frame=None
    def get(self,n):
        assert n>=self.i,(n,self.i)
        while self.i<n:
            ok,self.frame=self.cap.read();assert ok,(n,self.i);self.i+=1
        return self.frame.copy()

def main():
    A.mkdir(parents=True,exist_ok=True)
    assert not DEST.exists(),'Never overwrite a review candidate'
    hashes={k:sha(p) for k,p in SOURCES.items()}
    total=sum(b-a for _,a,b in LEGS)
    audio={k:decode_audio(p) for k,p in SOURCES.items()}
    gains={'roll1':2.77,'roll2':2.77,'installed':0.0}
    pieces=[];manifest=[];cursor=0
    for key,a,b in LEGS:
        part=audio[key][a*SPF:b*SPF].copy()*10**(gains[key]/20)
        assert len(part)==(b-a)*SPF
        pieces.append(part)
        manifest.append(dict(source=key,source_frames=[a,b],output_frames=[cursor,cursor+b-a],gain_db=gains[key]))
        cursor+=b-a
    joined=np.concatenate(pieces)
    # Symmetric 5 ms low-level seam smoothing; no time removed or silence added.
    seams=[]
    for leg in manifest[1:]:
        f=leg['output_frames'][0];s=f*SPF;n=220
        original=joined[s-n:s+n].copy()
        bridge=np.linspace(joined[s-n],joined[s+n-1],2*n)
        mix=np.sin(np.linspace(0,np.pi,2*n))**2
        joined[s-n:s+n]=original*(1-mix)+bridge*mix
        seams.append(dict(frame=f,time=f/FPS,before_dbfs=dbfs(joined[s-1323:s]),after_dbfs=dbfs(joined[s:s+1323]),sample_jump=float(abs(joined[s]-joined[s-1]))))
    assert np.max(np.abs(joined))<.999,'Audio clipping'
    write_wav(A/'assembled.wav',joined)
    for k,seam in enumerate(seams):
        s=round(seam['time']*RATE);write_wav(A/f'join-{k+1}.wav',joined[max(0,s-3*RATE):s+4*RATE])
    graphics={(mode,n):overview(n,mode) for mode in ['intro','available','reassure','recap'] for n in range(4)}
    model=model_diagram();cv2.imwrite(str(A/'model-diagram.png'),model)
    for mode in ['intro','available','reassure','recap']:cv2.imwrite(str(A/f'overview-{mode}.png'),graphics[(mode,3)])
    boards={}
    for name,file in [('tool','your-choices-choose-tool.jpg'),('how','your-choices-choose-how.jpg')]:
        for active in [None,0,1]:boards[(name,active)]=board(ROOT/'course-assets/your-choices'/file,active)
    compose_canonical_for_video(ROOT/'course-assets/your-choices/your-choices-close.jpg',A/'close-canvas.png','#ffffff')
    close=cv2.imread(str(A/'close-canvas.png'))
    mask=glyph_mask();mark_counts={}
    def cleaned(im):
        result,how=clean_frame(im,mask);mark_counts[str(how)]=mark_counts.get(str(how),0)+1;return result
    music=Reader(SOURCES['installed']);roll2=Reader(SOURCES['roll2']);installed=Reader(SOURCES['installed'])
    # The app graphic is established, rather than opening mid-dissolve.
    app_frame=cleaned(roll2.get(200))
    opening_frames=[]
    for f in range(342):
        if f<149:im=music.get(f)
        elif f<200:im=app_frame.copy()
        else:im=cleaned(roll2.get(f))
        opening_frames.append(im)
    p=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
                        '-i',str(A/'assembled.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','16','-preset','fast',
                        '-pix_fmt','yuv420p','-profile:v','high','-level:v','3.1','-c:a','aac','-b:a','192k',
                        '-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    boundaries=[];prev_label=None;frame_no=0
    retained=[(1489,1668),(3229,3435),(3435,3549),(3851,4065)]
    for key,a,b in LEGS:
        for f in range(a,b):
            if key=='roll2' and a==0:
                im=opening_frames[f];label='music-app' if f<149 else 'ai-app'
            elif key=='roll1':
                # Reveal each optional choice at the words that name it.
                stage=0 if f<585 else 1 if f<620 else 2 if f<694 else 3
                im=graphics[('intro',stage)];label='four-choice-reveal'
            elif key=='roll2':
                if f<970:
                    # The audio starts four frames before the source's dials cut.
                    # Start-clone the destination picture; retain every audio sample.
                    im=cleaned(roll2.get(max(584,f)));label='defaults-and-harder-work'
                else:
                    mode='available' if f<1182 else 'reassure'
                    im=graphics[(mode,3)];label='available-controls'
            else:
                im=installed.get(max(1218,f))
                if f<1292:label='four-dials'
                elif 2128<=f<2267:im=model;label='generic-model-family'
                elif any(x<=f<y for x,y in retained):label='retained-cutaway-'+str(next(x for x,y in retained if x<=f<y))
                elif f<2819:
                    active=None if f<1378 else 0 if f<1890 else 1
                    im=boards[('tool',active)];label='choose-tool'
                elif f<4309:
                    active=None if f<3015 else 0 if f<3680 else 1
                    im=boards[('how',active)];label='choose-how'
                elif f<4497:im=graphics[('recap',3)];label='four-choice-recap'
                else:
                    q=f-4497;u=min(1,max(0,(q-48)/149));u=u*u*(3-2*u);z=1+.2*u
                    cw,ch=round(3840/z),round(2160/z);x,y=(3840-cw)//2,(2160-ch)//2
                    im=cv2.resize(close[y:y+ch,x:x+cw],(W,H),interpolation=cv2.INTER_AREA);label='canonical-close'
            if label!=prev_label and frame_no>0:boundaries.append(dict(frame=frame_no,label=label))
            prev_label=label;p.stdin.write(im.tobytes());frame_no+=1
            if frame_no%900==0:print('rendered',frame_no,'/',total,flush=True)
    p.stdin.close();assert p.wait()==0;assert frame_no==total
    result=dict(candidate=str(DEST),candidate_sha256=sha(DEST),source_hashes=hashes,legs=manifest,
                decoded_frames=frame_no,duration=frame_no/FPS,audio_joins=seams,visual_boundaries=boundaries,
                mark_cleanup=mark_counts,ring_px=4,pauses_added=0,
                approval='User: Build please (2026-09-30)',scope='Approved evaluation repair; review only',
                source_limitation='Retained cutaways use installed composite because its exact edit has no pristine full-length equivalent.')
    (A/'edit-manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    assert all(sha(SOURCES[k])==v for k,v in hashes.items())
    print('BUILT',DEST,frame_no,frame_no/FPS,flush=True)

if __name__=='__main__':main()
