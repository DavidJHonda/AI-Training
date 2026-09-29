#!/usr/bin/env python3
"""Local label-only repair of the existing Context Window animation.

Tracks the original animated text panels; replaces their interior lettering.
Original timing, movement, imagery, narration and closing sequence are retained.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
cv2.setNumThreads(2)

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/context-window-v5.mp4'
OUT = ROOT / 'video-audit/context-window-label-repair-2026-09-29'
DEST = ROOT / 'Prompts/context-window-v6.mp4'
START, END = 6556, 7113
EXPECTED = '6d3e3ff7d2ad4c0019a460a44e250470a47b19ca2998f4eab0f8539300cb7c12'
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
# Source reference frame, panel rectangle, replacement; original labels tracked
# in both the working-memory area and their moving/faded outside copies.
SPECS = [
 ('goal', 6570, (330,271,385,61), 'User: Study Goal', 6556, 'USER'),
 ('topics', 6570, (326,342,385,62), 'User: Exam Topics', 6556, None),
 ('plan', 6570, (326,414,385,62), 'AI: Study Plan', 6556, None),
 ('notes', 6570, (326,486,385,62), 'User: Class Notes', 6556, None),
 ('quiz', 6570, (326,594,385,61), 'User: Practice Quiz', 6556, None),
 ('questions',6750,(326,488,385,62),'AI: Practice Questions',6660,None),
 ('restored',6960,(326,487,385,62),'Restored: Exam Topics',6872,None),
 ('reminder',6870,(316,593,405,41),'Prompt: Remember my exam topics.',6790,None),
]

def references():
    wanted = {s[1] for s in SPECS} | {7112}
    cap = cv2.VideoCapture(str(SRC)); found = {}; i = 0
    while wanted:
        ok, im = cap.read(); assert ok
        if i in wanted:
            found[i] = im; wanted.remove(i)
        i += 1
    cap.release()
    return found

def templates(refs):
    ans=[]
    for key,fi,(x,y,w,h),label,first,badge in SPECS:
        # Match the unique lettering, not the nearly identical card border.
        original=(refs[fi][y+6:y+35,x+28:x+w-12] if key=='reminder' else refs[fi][y+15:y+45,x+94:x+w-8]).copy()
        g=cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
        ink=g>np.median(g)+22
        ink[:3]=False;ink[-3:]=False
        ink_x=np.nonzero(ink)[1]
        cover_width=int(ink_x.max()+6) if len(ink_x) else g.shape[1]
        ans.append(dict(key=key, original=original, gray=g, label=label,
                        first=first, badge=badge, previous=None, samples=[],variants=[(g,1.0)],
                        card=cv2.cvtColor(refs[fi][y:y+h,x:x+w],cv2.COLOR_BGR2GRAY),
                        offset=(28,6) if key=='reminder' else (94,15),cover_width=cover_width,
                        empty=refs[7112]))
        if key in ('goal','topics','plan'):
            xx,yy={'goal':(895,299),'topics':(895,371),'plan':(892,443)}[key]
            small=refs[6960][yy:yy+21,xx:xx+198]
            ans[-1]['variants'].append((cv2.cvtColor(small,cv2.COLOR_BGR2GRAY),.7))
    return ans

def locate(im, spec, wide=False):
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    previous=spec['previous']
    if previous is None or wide:
        x0,y0,x1,y1=300,240,1130,680
        scales=np.r_[np.arange(.68,1.021,.02)]
    else:
        px,py,ps=previous
        x0,y0=max(300,px-24),max(240,py-20)
        th,tw=spec['gray'].shape
        x1,y1=min(1130,px+round(tw*ps)+26),min(680,py+round(th*ps)+22)
        scales=np.arange(max(.68,ps-.015),min(1.025,ps+.015)+.002,.005)
    roi=gray[y0:y1,x0:x1]; best=(-1,None)
    for scale in scales:
        for variant,base_scale in spec['variants']:
            t=cv2.resize(variant,None,fx=float(scale/base_scale),fy=float(scale/base_scale),interpolation=cv2.INTER_LINEAR)
            if t.shape[0]>roi.shape[0] or t.shape[1]>roi.shape[1]:continue
            m=cv2.matchTemplate(roi,t,cv2.TM_CCOEFF_NORMED)
            _,score,_,xy=cv2.minMaxLoc(m)
            if score>best[0]:best=(score,(x0+xy[0],y0+xy[1],float(scale)))
    if best[0]<.8 and previous is not None and not wide:
        return locate(im,spec,True)
    return best

def locate_card(im,spec):
    if spec['previous'] is None:return (-1,None)
    px,py,ps=spec['previous']; ox,oy=spec['offset']
    cx,cy=round(px-ox*ps),round(py-oy*ps)
    h,w=spec['card'].shape
    x0,y0=max(280,cx-24),max(240,cy-20)
    x1,y1=min(1170,cx+round(w*ps)+26),min(685,cy+round(h*ps)+22)
    roi=cv2.cvtColor(im[y0:y1,x0:x1],cv2.COLOR_BGR2GRAY); best=(-1,None)
    for s in np.arange(max(.68,ps-.015),min(1.025,ps+.015)+.002,.005):
        t=cv2.resize(spec['card'],None,fx=float(s),fy=float(s))
        if t.shape[0]>roi.shape[0] or t.shape[1]>roi.shape[1]:continue
        _,score,_,xy=cv2.minMaxLoc(cv2.matchTemplate(roi,t,cv2.TM_CCOEFF_NORMED))
        if score>best[0]:best=(score,(round(x0+xy[0]+ox*s),round(y0+xy[1]+oy*s),float(s)))
    return best

def fill_and_text(im, rect, text, color, size, centered=False):
    x,y,w,h=rect
    patch=im[y:y+h,x:x+w]
    # The old text sits on a flat panel. Interpolate the uncontaminated top and
    # bottom rows to preserve the panel's current opacity during its fade.
    top=np.median(patch[:3].reshape(-1,3),axis=0); bot=np.median(patch[-3:].reshape(-1,3),axis=0)
    rows=np.array([top*(1-t)+bot*t for t in np.linspace(0,1,h)],dtype=np.uint8)
    bg=np.repeat(rows[:,None,:],w,axis=1)
    # Smooth compression noise without sampling glyph pixels.
    bg=cv2.GaussianBlur(bg,(9,3),0)
    rgb=Image.fromarray(cv2.cvtColor(bg,cv2.COLOR_BGR2RGB)).resize((w*3,h*3),Image.Resampling.BICUBIC)
    draw=ImageDraw.Draw(rgb);font=ImageFont.truetype(FONT,max(12,round(size*3)))
    bb=draw.textbbox((0,0),text,font=font)
    tx=(w*3-(bb[2]-bb[0]))/2 if centered else 4*3
    ty=(h*3-(bb[3]-bb[1]))/2-bb[1]
    draw.text((tx,ty),text,font=font,fill=tuple(int(c) for c in color[::-1]))
    im[y:y+h,x:x+w]=cv2.cvtColor(np.asarray(rgb.resize((w,h),Image.Resampling.LANCZOS)),cv2.COLOR_RGB2BGR)

def repair(im, specs, frame, cached=None):
    source=im.copy(); rows=[]
    for spec in specs:
        if frame<spec['first']:continue
        saved=(cached or {}).get(spec['key'])
        method='text'
        if spec['key']=='reminder':
            if frame>=6960:continue
            delta=(spec['empty'][599:628,344:680].astype(float)-source[599:628,344:680]).mean()
            if delta<5:continue
            score,loc=1.0,(344,599,1.0);method='fixed-reminder'
        elif frame>=7065:
            # During the final fade text contrast falls below reliable template
            # matching. Track each still-visible panel against the empty final
            # scene instead; its horizontal motion and fade remain original.
            key=spec['key']; right=key in ('goal','topics','plan')
            y={'goal':299,'topics':371,'plan':443,'notes':286,'quiz':358,'questions':429,'restored':502}[key]
            scale=.7 if right else 1.0
            cy=round(y-15*scale+8*scale)
            delta=(spec['empty'][cy:cy+4].astype(float)-source[cy:cy+4]).mean(axis=(0,2))
            line=(delta>5).astype(np.uint8)[None,:]
            line=cv2.morphologyEx(line,cv2.MORPH_CLOSE,np.ones((1,19),np.uint8))[0]
            runs=[];beg=None
            for xx in range(280,1190):
                if line[xx] and beg is None:beg=xx
                if not line[xx] and beg is not None:
                    if xx-beg>170:runs.append((beg,xx))
                    beg=None
            choices=[r for r in runs if (r[0]>770)==right]
            if not choices:continue
            left=choices[-1 if right else 0][0]
            score,loc=1.0,(round(left+94*scale),y,scale);method='fade-panel'
        elif saved and saved.get('found') and saved['score']>=.8:
            score,loc=saved['score'],(saved['x'],saved['y'],saved['scale']);method='cached-text'
        elif cached and spec['previous'] is not None:
            score,loc=locate_card(source,spec);method='card'
            if score<.72:score,loc=locate(source,spec);method='text'
        else:score,loc=locate(source,spec)
        if score<.8:
            score2,loc2=locate_card(source,spec)
            if score2>.72:score,loc=score2,loc2;method='card'
        if score<(.72 if method=='card' else .8):
            rows.append(dict(key=spec['key'],score=score,found=False));continue
        x,y,scale=loc;spec['previous']=loc
        h,w=spec['gray'].shape;ww,hh=round(w*scale),round(h*scale)
        patch=source[y:y+hh,x:x+ww]
        # Estimate current text brightness directly, including faded cards.
        v=patch.mean(axis=2); flat=patch.reshape(-1,3)
        color=np.median(flat[v.ravel()>np.percentile(v,98)],axis=0)
        bg=np.median(flat,axis=0)
        if np.mean(color-bg)<2:continue
        under=(spec['key']=='reminder' or (spec['key'] in ('goal','topics','plan') and x>440 and frame<7065))
        before=im.copy() if under else None
        text_width=ImageFont.truetype(FONT,39).getlength(spec['label'])/3+10
        cover_width=min(ww,round(max(spec['cover_width'],text_width)*scale))
        fill_and_text(im,(x,y,cover_width,hh),spec['label'],color,13*scale)
        if spec['badge']:
            bx=x-round(80*scale);by=y+round(7*scale)
            fill_and_text(im,(bx,by,round(60*scale),round(17*scale)),spec['badge'],color,10*scale,True)
        if under:
            for other in specs:
                if other['key'] in (spec['key'],'reminder'):continue
                front=(cached or {}).get(other['key'])
                if not front or not front.get('found') or front['x']>440:continue
                xx=round(front['x']-94*front['scale']); yy=round(front['y']-15*front['scale'])
                fw,fh=round(385*front['scale']),round(62*front['scale'])
                im[yy:yy+fh,xx:xx+fw]=before[yy:yy+fh,xx:xx+fw]
        rows.append(dict(key=spec['key'],score=round(score,4),found=True,x=x,y=y,scale=round(scale,4),method=method))
    return im,rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--draft',action='store_true');args=ap.parse_args()
    dest=OUT/'working.mp4' if args.draft else DEST
    assert hashlib.sha256(SRC.read_bytes()).hexdigest()==EXPECTED,'Source changed'
    OUT.mkdir(exist_ok=True,parents=True); (OUT/'preview').mkdir(exist_ok=True)
    specs=templates(references());cap=cv2.VideoCapture(str(SRC));i=0;log=[]
    cached={}
    cache_file=OUT/'tracking.json' if (OUT/'tracking.json').exists() else OUT/'preview-tracking.json'
    if not args.preview and cache_file.exists():
        cached={r['frame']:{s['key']:s for s in r['labels']} for r in json.loads(cache_file.read_text())}
        # Short crossings can occlude the identifying text while the panel
        # continues along the same trajectory. Interpolate its measured path
        # between surrounding confident positions, never jump to another card.
        for key in ('goal','topics','plan'):
            good=[(f,r[key]) for f,r in sorted(cached.items()) if f<7065 and key in r and r[key].get('found') and r[key]['score']>=.8]
            fs=np.array([f for f,r in good]);coords=np.array([[r['x'],r['y'],r['scale']] for f,r in good])
            for f in range(int(fs[0]),int(fs[-1])+1):
                r=cached[f].get(key)
                if not r or not r.get('found') or r['score']<.8:
                    j=int(np.searchsorted(fs,f));a,b=j-1,j
                    dt=fs[b]-fs[a];u=(f-fs[a])/dt
                    l=max(0,a-4);r=min(len(fs)-1,b+4)
                    m0=(coords[a]-coords[l])/max(1,fs[a]-fs[l])
                    m1=(coords[r]-coords[b])/max(1,fs[r]-fs[b])
                    x,y,s=(2*u**3-3*u**2+1)*coords[a]+(u**3-2*u**2+u)*dt*m0+(-2*u**3+3*u**2)*coords[b]+(u**3-u**2)*dt*m1
                    cached[f][key]=dict(key=key,found=True,score=1.0,x=round(x),y=round(y),scale=float(s),method='interpolated-crossing')
    proc=None
    if not args.preview:
        assert args.draft or not dest.exists(), 'Never overwrite an existing candidate'
        proc=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(SRC),'-map','0:v','-map','1:a:0','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(dest)],stdin=subprocess.PIPE)
    while True:
        ok,im=cap.read()
        if not ok:break
        if START<=i<END:
            im,rows=repair(im,specs,i,cached.get(i));log.append(dict(frame=i,labels=rows))
            if i%30==0 or i==START:cv2.imwrite(str(OUT/'preview'/f'{i:05d}.jpg'),im)
        if proc:proc.stdin.write(im.tobytes())
        i+=1
        if i%150==0 and START<i<END:print('processed',i,flush=True)
    cap.release()
    if proc:proc.stdin.close();assert proc.wait()==0
    (OUT/('preview-tracking.json' if args.preview else 'tracking.json')).write_text(json.dumps(log,indent=2)+'\n')
    print('frames',i,'output',dest if proc else OUT/'preview',flush=True)

if __name__=='__main__':main()
