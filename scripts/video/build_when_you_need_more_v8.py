#!/usr/bin/env python3
"""Approved visual-only donor inserts; pristine visual rebuild, copied v7 AAC."""
from pathlib import Path
import argparse
import json
import subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import build_when_you_need_more_v7 as base
from editspec_build import Reader, sha, fr
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import smoothstep

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'video-audit/when-you-need-more-build-v8-2026-11-07'
DEST = ROOT/'Prompts/when-you-need-more-v8.mp4'
LIVE = ROOT/'course-assets/when-you-need-more/when-you-need-more.mp4'
COLLEGE = ROOT/'video-audit/when-you-need-more-build-2026-10-08-v3/assets/college-physics-comparison.png'
INSERTS = [
    dict(kind='thinking-donor', start=fr(97), end=fr(106.9), roll=7, source_start=fr(119)),
    dict(kind='research-donor', start=fr(142), end=fr(148.333333), roll=9, source_start=fr(185.5)),
    dict(kind='college', start=fr(148.333333), end=fr(158.7)),
]
FONTS = {s:ImageFont.truetype(str(base.FONT),s) for s in [14,16,18,24,26]}

def erase(im, rect):
    """Interpolate from the clean left/right border of each scanline."""
    x,y,z,w = rect
    ramp=np.linspace(0,1,z-x+1)[None,:,None]
    im[y:w+1,x:z+1]=(im[y:w+1,x-1:x].astype(float)*(1-ramp)+im[y:w+1,z+1:z+2]*ramp).round().astype(np.uint8)

class Thinking:
    def __init__(self):
        rd=Reader(base.S[7]); early=rd.at(fr(122));late=rd.at(fr(128));rd.c.release()
        self.specs=[]
        for name,first,second,area,onset in [
            ('Steps',(480,329,549,346),(460,392,524,408),(450,310,570,435),120.35),
            ('Weigh',(653,329,708,346),(667,392,713,408),(630,310,740,435),120.7),
            ('Options',(579,459,622,477),(573,392,609,408),(545,370,650,500),121.1),
            ('Check',(748,459,783,477),(773,392,808,408),(715,370,840,500),121.35),
        ]:
            templates=[]
            for source,rect in [(early,first),(late,second)]:
                x,y,z,w=rect;templates.append(cv2.cvtColor(source[y:w,x:z],cv2.COLOR_BGR2GRAY))
            self.specs.append((name,first,area,onset,templates))
        self.matches=[]

    def frame(self, im, sf):
        t=sf/30;gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);paint=[]
        # Replace moving labels at their observed positions, retaining native boxes/arrows.
        for name,rect,area,onset,templates in self.specs:
            if t<onset:continue
            x,y,z,w=rect;score=1
            if t>=123.5:
                sx,sy,ex,ey=area;best=None
                for template in templates:
                    corr=cv2.matchTemplate(gray[sy:ey,sx:ex],template,cv2.TM_CCOEFF_NORMED)
                    iy,ix=np.unravel_index(np.argmax(np.abs(corr)),corr.shape)
                    candidate=(float(abs(corr[iy,ix])),sx+int(ix),sy+int(iy),template.shape)
                    if best is None or candidate[0]>best[0]:best=candidate
                score,x,y,shape=best;w=y+shape[0];z=x+shape[1]
                assert score>.52,(sf,name,score)
                self.matches.append(dict(frame=sf,label=name,score=score))
            # Sample the text's own backing, whether its native box is light or dark.
            bg=tuple(int(v) for v in np.median(im[y-3:y-1,x+3:z-3],axis=(0,1)))
            im[y-1:w+1,x-1:z+1]=bg
            ink='#f4f5ef' if np.mean(bg)<100 else '#29434b'
            paint.append(((x+z)/2,(y+w)/2,name,14,ink,min(1,(t-onset)/.2)))
        for rect in [(183,215,323,275),(478,176,805,231),(473,239,807,257)]:erase(im,rect)
        paint += [(253,230,'Your task',24,'#29434b',1),(253,263,'With steps',18,'#526266',1),
                  (640,193,'More thinking',26,'#29434b',1),(640,220,'Work through the task',18,'#526266',1)]
        if t>=126.2:
            erase(im,(950,214,1110,276))
            opacity=min(1,(t-126.2)/.4)
            paint += [(1027,230,'An answer',24,'#29434b',opacity),
                      (1027,263,'Review before using',14,'#526266',opacity)]
        pic=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
        for x,y,word,size,ink,opacity in paint:
            layer=Image.new('RGBA',pic.size);d=ImageDraw.Draw(layer)
            rgb=tuple(bytes.fromhex(ink[1:]));d.text((x,y),word,font=FONTS[size],fill=(*rgb,round(255*opacity)),anchor='mm')
            pic.paste(layer,(0,0),layer)
        return cv2.cvtColor(np.asarray(pic),cv2.COLOR_RGB2BGR)

class Inserts:
    def __init__(self):
        self.readers={};self.mask=glyph_mask();self.cleaning={'clone':0,'inpaint':0,'declined':0}
        self.thinking=Thinking();self.college=cv2.imread(str(COLLEGE))
    def frame(self, row, f):
        if row['kind']=='college':
            # Gentle motion on the previously approved college comparison illustration.
            u=(f-row['start'])/(row['end']-row['start']-1);zoom=1+.035*smoothstep(u)
            h,w=self.college.shape[:2];ww=min(w,h*16/9)/zoom;hh=ww*9/16
            return cv2.warpAffine(self.college,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),
                                 (1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
        roll=row['roll']
        if roll not in self.readers:self.readers[roll]=Reader(base.S[roll])
        sf=row['source_start']+f-row['start'];im=self.readers[roll].at(sf)
        im,method=clean_frame(im,self.mask);self.cleaning[method or 'declined']+=1
        if row['kind']=='thinking-donor':im=self.thinking.frame(im,sf)
        return im

def setup():
    assert sha(LIVE)=='ae5499e7373e2cbd5231c4cebbdd1b3df3a5814c1e540729b427ba9a0cb8eaf3'
    base.OUT=OUT;base.DEST=DEST

def prepare():
    setup();m=base.prepare()
    m.update(scope='Visual-only engagement repair authorized by user: agree. Build the video please.',
             inserts=INSERTS,audio='AAC packets copied from installed v7; no audio/timing edits',
             longest_unbroken_board_seconds=18.3666666667,
             board_seconds_before=82.6333333333,board_seconds_after=56.0333333333)
    m['protected_hashes'][str(COLLEGE)]=sha(COLLEGE)
    boundaries={r['start_frame']:r['label'] for r in m['visual_timeline'][1:]}
    for r in INSERTS:
        boundaries[r['start']]=r['kind'];boundaries[r['end']]='return to retained picture'
    # Two inserts are adjacent: the entry label takes precedence.
    for r in INSERTS:boundaries[r['start']]=r['kind']
    m['boundaries']=[dict(frame=f,label=label) for f,label in sorted(boundaries.items())]
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');return m

def render(m, preview=False):
    setup();p=base.Pictures(m);ins=Inserts()
    if preview:
        for r in INSERTS:
            for f in range(r['start'],r['end']):
                im=ins.frame(r,f)
                if (f-r['start'])%15==0 or f==r['end']-1:cv2.imwrite(str(OUT/'preview'/f'insert-{f:05d}.jpg'),im)
        (OUT/'label-tracking.json').write_text(json.dumps(ins.thinking.matches,indent=2)+'\n')
        return
    assert not DEST.exists()
    proc=subprocess.Popen([base.FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
        '-r','30','-i','pipe:0','-i',str(LIVE),'-map','0:v','-map','1:a','-c:v','libx264',
        '-preset','fast','-crf','17','-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for r in m['visual_timeline']:
        for f in range(r['start_frame'],r['end_frame']):
            override=next((i for i in INSERTS if i['start']<=f<i['end']),None)
            im=ins.frame(override,f) if override else p.frame(r,f)
            proc.stdin.write(im.tobytes())
        print(r['end_frame'],m['frames'],r['label'],flush=True)
    proc.stdin.close();assert proc.wait()==0
    m.update(candidate_sha256=sha(DEST),insert_corner_cleaning=ins.cleaning,
             source_corner_cleaning=p.counts,protected_unchanged={k:sha(k)==v for k,v in m['protected_hashes'].items()})
    assert all(m['protected_unchanged'].values()) and ins.cleaning['declined']==0 and p.counts['declined']==0
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    (OUT/'label-tracking.json').write_text(json.dumps(ins.thinking.matches,indent=2)+'\n')
    print('BUILT',DEST,flush=True)

if __name__=='__main__':
    cv2.setNumThreads(2);ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--render-prepared',action='store_true');args=ap.parse_args()
    m=json.loads((OUT/'edit-manifest.json').read_text()) if args.render_prepared else prepare()
    render(m,args.preview)
