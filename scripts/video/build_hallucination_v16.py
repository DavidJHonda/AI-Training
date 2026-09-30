#!/usr/bin/env python3
"""Approved roll-3 production edit. Video-only; AAC packets and timing preserved."""
from pathlib import Path
import argparse, collections, hashlib, json, subprocess
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from editspec_build import Build, Reader, sha
from ken_burns_path import draw_ring, ring_px, hex_bgr
from gemini_mark import clean_frame, glyph_mask

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/hallucination-3.mp4'
DEST=ROOT/'Prompts/hallucination-v16.mp4'
OUT=ROOT/'video-audit/hallucination-build-2026-09-30-v16'
ASSETS=ROOT/'course-assets/hallucination'
FPS=30; TOTAL=8369; CLOSE=8051
cv2.setNumThreads(2)
FONTS={}
REFS={}
def font(size,bold=False):
    key=(size,bold)
    if key not in FONTS:FONTS[key]=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial'+(' Bold' if bold else '')+'.ttf',size)
    return FONTS[key]
def text(d,xy,s,size=18,fill='#172f48',bold=False,anchor='mm'):
    d.text(xy,s,font=font(size,bold),fill=fill,anchor=anchor)
def fr(t):return round(t*FPS)

BOARDS=[
 dict(key='example',file='hallucination-example.jpg',start=0,end=1483,
      rings=[(2.28,[606,202,1520,337],'#4f2fc4'),(8.26,[80,402,987,617],'#6e51ff'),(25.18,[40,697,1560,785],'#6e51ff'),(27.80,[80,402,987,617],'#6e51ff')]),
 dict(key='why',file='hallucination-why-ai-makes-things-up.jpg',start=2243,end=3532,
      rings=[(t,[x0,127,x1,831],c) for t,x0,x1,c in [(80.94,40,405,'#4f2fc4'),(90.66,405,800,'#1652f0'),(98.52,800,1195,'#0e8f86'),(106.62,1195,1560,'#a9760c')]]),
 dict(key='pizza',file='hallucination-glue-on-pizza.jpg',start=4274,end=4615,
      rings=[(144.4667,[34,111,1353,985],'#6e51ff'),(150.36,[34,1018,1353,1095],'#6e51ff')]),
 dict(key='check',file='hallucination-check-claim.jpg',start=4914,end=6179,
      rings=[(t,[x0,127,x1,738],c) for t,x0,x1,c in [(179.06,40,540,'#4f2fc4'),(184.74,540,1060,'#1652f0'),(190.80,1060,1560,'#0e8f86')]]),
]

def strength(patch,bg,reference):
    # The original glyph locations distinguish fading lettering from paper dots.
    ref=cv2.cvtColor(reference,cv2.COLOR_BGR2GRAY)
    ink=ref<110
    if not np.any(ink):return 0.0
    current=cv2.cvtColor(patch,cv2.COLOR_BGR2GRAY)
    contrast=np.mean(bg)-np.median(current[ink])
    full=np.mean(bg)-np.median(ref[ink])
    return float(np.clip(contrast/max(full,1),0,1))


def relabel(im,rect,lines,sample=None,reference=2100,opaque=False,fade=None,blank=None):
    x0,y0,x1,y1=rect;old=im[y0:y1,x0:x1].copy()
    if sample is None:bg=np.median(old[[0,-1],:,:].reshape(-1,3),axis=0)
    else:
        a,b,c,d=sample;bg=np.median(im[b:d,a:c].reshape(-1,3),axis=0)
    alpha=1.0 if opaque else strength(old,bg,REFS[reference][y0:y1,x0:x1])
    if fade is not None:alpha=fade
    base=np.full(old.shape,np.rint(bg),np.uint8)
    layer=Image.fromarray(cv2.cvtColor(base,cv2.COLOR_BGR2RGB));draw=ImageDraw.Draw(layer)
    for x,y,s,size,color,bold in lines:text(draw,(x-x0,y-y0),s,size,color,bold)
    painted=cv2.cvtColor(np.array(layer),cv2.COLOR_RGB2BGR)
    backdrop=REFS[blank][y0:y1,x0:x1] if blank is not None else base
    im[y0:y1,x0:x1]=cv2.addWeighted(painted,alpha,backdrop,1-alpha,0)


def repair_mixed(im,n):
    cards=[(207,240,623,364,'Stanford University','Real university',True),
           (657,240,1074,364,'2022 study','Invented study',False),
           (207,388,623,512,'1,200 participants','Invented sample',False),
           (657,388,1074,512,'Claimed 18% improvement','Invented result',False)]
    for x0,y0,x1,y1,title,sub,real in cards:
        old=im[y0:y1,x0:x1].copy();bg=np.median(im[y0:y1,180:195].reshape(-1,3),axis=0)
        alpha=float(np.clip((n-1640)/24,0,1))
        base=np.full(old.shape,np.rint(bg),np.uint8)
        layer=Image.fromarray(cv2.cvtColor(base,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(layer)
        c='#2ba770' if real else '#c54b45';fill='#eff7f0' if real else '#fbefeb'
        w=x1-x0;h=y1-y0
        d.rounded_rectangle((1,1,w-2,h-2),radius=12,fill=fill,outline=c,width=2)
        d.ellipse((21,40,61,80),fill='#dcf0e3' if real else '#f9ddd7',outline=c,width=2)
        if real:d.line([(31,59),(39,67),(52,49)],fill=c,width=3)
        else:text(d,(41,60),'!',25,c,True)
        text(d,(79,45),title,20 if real else 19,'#232323',True,'lm')
        text(d,(79,77),sub,17,c,False,'lm')
        im[y0:y1,x0:x1]=cv2.addWeighted(cv2.cvtColor(np.array(layer),cv2.COLOR_RGB2BGR),alpha,REFS[1640][y0:y1,x0:x1],1-alpha,0)
    return im


def repair_paper(im,n):
    fade=float(np.clip((n-2022)/24,0,1))
    relabel(im,(280,212,1002,292),[
        (640,227,'ILLUSTRATIVE PAPER',13,'#21384b',True),
        (640,252,'Research-sounding language',21,'#202323',True),
        (640,279,'No original study supports these claims',14,'#555b5c',False)],(269,211,284,292),fade=fade,blank=2022)
    red=n>=2154
    color='#c54b45' if red else '#202323'
    relabel(im,(703,380,956,412),[(829,397,'Claimed sample: 1,200',14,color,red)],fade=fade,blank=2022)
    relabel(im,(702,438,957,472),[(829,455,'Claimed recall gain: +18%',14,color,red)],fade=fade,blank=2022)
    return im


def repair_stanford(im,n):
    if 6255<=n<6574:
        relabel(im,(301,489,478,518),[(388,504,'Claimed study',14,'#202020',False)],(472,478,487,488),reference=6420,fade=float(np.clip((n-6274)/24,0,1)*np.clip((6574-n)/14,0,1)))
    if 6550<=n<7092:
        # Source marks Find Source green even while its search is still running.
        # Preserve the pill geometry, but distinguish searching from not found.
        rect=(489,76,791,141);x0,y0,x1,y1=rect
        patch=im[y0:y1,x0:x1].copy();bg=np.median(im[79:85,505:515].reshape(-1,3),axis=0)
        # Copy only the pill footprint, retaining the source paper around its corners.
        layer=Image.fromarray(cv2.cvtColor(patch,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(layer)
        failed=n>=6820;c='#c64b48' if failed else '#4e81a3'
        d.rounded_rectangle((2,2,299,62),radius=15,fill='#fafcf9',outline=c,width=2)
        d.ellipse((29,14,65,50),fill=c)
        text(d,(47,32),'2',19,'white',True)
        text(d,(176,32),'Source not found' if failed else 'Searching...',19,'#303337',True)
        patched=cv2.cvtColor(np.array(layer),cv2.COLOR_RGB2BGR)
        fade=float(np.clip((7092-n)/16,0,1))
        im[y0:y1,x0:x1]=cv2.addWeighted(patched,fade,REFS[7100][y0:y1,x0:x1],1-fade,0)
    return im

class Production:
    def __init__(self):
        protected=[ROOT/'lessons/hallucination.md',ASSETS/'hallucination.mp4',*sorted(ASSETS.glob('*.jpg'))]
        self.b=Build(ROOT,SRC,OUT,DEST,protected=protected)
        assert self.b.hashes[str(SRC)]=='34768db69bf30e0102db14c8a1e2796567617d7b58733a05711873ce8307ca22'
        self.cache={};self.mask=glyph_mask();self.counts=collections.Counter()
        reader=Reader(SRC)
        for frame in [1640,1740,2022,2100,6420,7100]:REFS[frame]=reader.at(frame)
        for board in BOARDS:
            p,cw,ch,ox,oy=self.b.compose(ASSETS/board['file'],board['key'])
            canvas=cv2.imread(str(p));up=cv2.resize(canvas,(cw*3,ch*3),interpolation=cv2.INTER_LANCZOS4)
            base=cv2.resize(up,(1280,720),interpolation=cv2.INTER_AREA);states=[(board['start'],base)]
            sx,sy=1280/cw,720/ch
            for t,rect,color in board['rings']:
                im=base.copy();x0,y0,x1,y1=rect
                draw_ring(im,(x0+ox)*sx-2,(y0+oy)*sy-2,(x1+ox)*sx+2,(y1+oy)*sy+2,hex_bgr(color),18*sx+2,ring_px(720))
                states.append((fr(t),im))
            self.cache[board['key']]=states
        self.b.make_close('hallucination')
    def frame(self,im,n):
        for b in BOARDS:
            if b['start']<=n<b['end']:
                states=self.cache[b['key']]
                return next(pic for start,pic in reversed(states) if start<=n)
        if n>=CLOSE:
            img=self.b.close_img;h,w=img.shape[:2];q=np.clip((n-CLOSE-48)/149,0,1);z=1+.2*q*q*(3-2*q)
            ww=w/z;hh=ww*9/16
            return cv2.warpAffine(img,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
        im,how=clean_frame(im,self.mask);self.counts[str(how)]+=1
        if 1640<=n<1861:im=repair_mixed(im,n)
        if 2022<=n<2243:im=repair_paper(im,n)
        if 6255<=n<7092:im=repair_stanford(im,n)
        return im
    def preview(self):
        numbers=set([0,68,248,755,834,1482,1483,1639,1640,1645,1650,1665,1695,1740,1770,1815,1860,1861,2022,2028,2040,2100,2154,2190,2242,2243,4274,4334,4511,4614,4615,4616,4914,6178,6179,6270,6280,6290,6300,6420,6550,6560,6567,6568,6570,6600,6630,6810,6820,6840,7091,7092,7095,7100,7800,8050,8051,8099,8249,8368])
        for b in BOARDS:
            numbers.add(b['start'])
            for t,_,_ in b['rings']:numbers.update([fr(t)-1,fr(t)])
        r=Reader(SRC);thumbs=[]
        for n in sorted(numbers):
            im=self.frame(r.at(n),n);cv2.imwrite(str(OUT/'preview'/f'{n:05d}.png'),im)
            tile=cv2.resize(im,(320,180),interpolation=cv2.INTER_AREA);tile=cv2.copyMakeBorder(tile,24,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255));cv2.putText(tile,f'f{n}  {n/30:.3f}s',(5,17),cv2.FONT_HERSHEY_SIMPLEX,.46,(20,20,20),1,cv2.LINE_AA);thumbs.append(tile)
        while len(thumbs)%4:thumbs.append(np.full_like(thumbs[0],255))
        for k in range(0,len(thumbs),24):cv2.imwrite(str(OUT/f'preview-{k//24+1}.jpg'),cv2.vconcat([cv2.hconcat(thumbs[i:i+4]) for i in range(k,min(k+24,len(thumbs)),4)]))
        print('Previews ready',flush=True)
    def render(self):
        assert not DEST.exists(),'Candidate exists; do not overwrite reviewed candidates'
        ff=imageio_ffmpeg.get_ffmpeg_exe();temp=OUT/'render.tmp.mp4';log=open(OUT/'encode.log','w')
        cmd=[ff,'-y','-v','warning','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(temp)]
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log);r=Reader(SRC)
        try:
            for n in range(TOTAL):
                p.stdin.write(self.frame(r.at(n),n).tobytes())
                if n%900==0:print(f'Rendered {n}/{TOTAL}',flush=True)
            p.stdin.close();assert p.wait()==0
        finally:log.close()
        assert all(sha(Path(k))==v for k,v in self.b.hashes.items()),'Protected input changed'
        assert not DEST.exists();temp.rename(DEST)
        m=dict(source=str(SRC),output=str(DEST),source_sha256=sha(SRC),output_sha256=sha(DEST),fps=FPS,total_frames=TOTAL,duration=TOTAL/FPS,audio='AAC packet stream copy; no edits, pauses, grafts, or retiming',boards=BOARDS,ring_stroke_px=ring_px(720),density='Compact full views; complete canonical illustrations',close=dict(start=CLOSE,prehold=48,push=150,tail=120,zoom=1.2),repairs=dict(mixed=[1640,1861],paper=[2022,2243],study_label=[6255,6574],search_status=[6550,7092]),corner_counts=dict(self.counts),protected_hashes=self.b.hashes,scope='Candidate only; not installed or published')
        (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
        print(f'Built {DEST}',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');a=parser.parse_args()
    b=Production();b.preview() if a.preview else b.render()
