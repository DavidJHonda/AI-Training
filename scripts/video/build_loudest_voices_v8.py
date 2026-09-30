#!/usr/bin/env python3
"""Approved visual-only Loudest Voices repair. Preserve all audio and untouched GOPs."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

import av
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ken_burns_path import draw_ring, hex_bgr

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/loudest-voices-build-2026-09-30-v8'
LIVE = ROOT / 'course-assets/loudest-voices/loudest-voices.mp4'
SOURCE = OUT / 'source-v7.mp4'
DEST = ROOT / 'Prompts/loudest-voices-v8.mp4'
ASSET = ROOT / 'course-assets/loudest-voices/loudest-voices-experts.jpg'
EXPECTED = 'e671f6bceff6b2e31d1dee294c638c437e951d7cb99a708ffd981ae812f16391'
SPANS = [(712,2080,'experts-a'), (2224,2930,'experts-b'),
         (3005,4142,'experts-c'), (6069,6501,'habits-labels')]
CARDS = [[41,127,524,1522], [558,127,1042,1522], [1076,127,1559,1522]]
COLORS = ['#4f2fc4','#1652f0','#0e8f86']
SECTIONS = [
    [[57,423,508,704],[57,742,508,1073],[57,1118,508,1489]],
    [[574,423,1026,704],[574,742,1026,1073],[574,1118,1026,1325]],
    [[1092,423,1543,704],[1092,742,1543,1073],[1092,1118,1543,1407]],
]
# Output frames, inherited from the verified v7 spoken-onset plan.
EVENTS = [(873,0,0),(1191,0,1),(1500,0,2),(1905,1,0),
          (2234,1,1),(2570,1,2),(2769,2,0),(3036,2,1),(3297,2,2)]
SUMMARY = [(3630,[0,1,2]),(3709,[0]),(3771,[1]),(3827,[2]),(3892,[0,1,2])]
FF = imageio_ffmpeg.get_ffmpeg_exe()
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
cv2.setNumThreads(1)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def fitted(im, box):
    x,y,w,h = box
    scale = min(w/im.shape[1],h/im.shape[0])
    nw,nh = round(im.shape[1]*scale),round(im.shape[0]*scale)
    return cv2.resize(im,(nw,nh),interpolation=cv2.INTER_LANCZOS4), (round(x+(w-nw)/2),round(y+(h-nh)/2),nw,nh),scale

def put(frame,im,box):
    resized,rect,scale = fitted(im,box)
    x,y,w,h = rect
    frame[y:y+h,x:x+w] = resized
    return rect,scale

class Boards:
    def __init__(self):
        self.asset = cv2.imread(str(ASSET))
        self.cache = {}

    def full(self,active=()):
        key = ('full',tuple(active))
        if key in self.cache: return self.cache[key]
        frame = np.full((720,1280,3),250,np.uint8)
        rect,s = put(frame,self.asset,(0,27,1280,666))
        x,y,_,_ = rect
        for k in active:
            a,b,c,d = CARDS[k]
            draw_ring(frame,x+a*s,y+b*s,x+c*s,y+d*s,hex_bgr(COLORS[k]),9,4)
        self.cache[key] = frame
        return frame

    def focus(self,k,section):
        key = (k,section)
        if key in self.cache: return self.cache[key]
        frame = np.full((720,1280,3),250,np.uint8)
        a,b,c,d = CARDS[k]
        # The complete original card stays visible, including illustration,
        # identity, both quotations, and its bottom edge. No reflow/retyping.
        context = self.asset[b-5:d+6,a-5:c+6]
        rect,s = put(frame,context,(36,28,252,664))
        x,y,w,h = rect
        if section == 0:
            draw_ring(frame,x+5*s,y+5*s,x+(c-a+5)*s,y+(d-b+5)*s,hex_bgr(COLORS[k]),9,4)
        # A second viewport provides readable source pixels while retaining
        # the complete card, rather than using a crop as the only view.
        a,b,c,d = SECTIONS[k][section]
        pad = 11
        detail = self.asset[b-pad:d+pad,a-pad:c+pad]
        rect,s = put(frame,detail,(342,76,870,568))
        x,y,w,h = rect
        if section:
            draw_ring(frame,x+pad*s,y+pad*s,x+(c-a+pad)*s,y+(d-b+pad)*s,hex_bgr(COLORS[k]),18,4)
        self.cache[key] = frame
        return frame

    def render(self,n):
        if n >= 3611:
            rings = next((ks for start,ks in reversed(SUMMARY) if n >= start),[])
            return self.full(rings)
        event = next((e for e in reversed(EVENTS) if e[0] <= n),None)
        if event is None: return self.full()
        start,k,section = event
        return self.focus(k,section)

class Labels:
    """Remove only original glyphs, retaining the animated bars and markers."""
    def __init__(self,reference,blank):
        self.blank=blank
        self.reference=reference
        self.specs = [
            ((125,108,666,137),'Machines improve fast',(135,107),27,(56,87,104)),
            ((126,579,666,609),'Habits change more slowly',(135,580),27,(36,43,42)),
            ((511,347,770,375),'Adoption takes time',(0,0),23,(163,58,72)),
        ]
        self.masks=[]
        for i,(roi,text,pos,size,color) in enumerate(self.specs):
            x0,y0,x1,y1=roi
            piece=reference[y0:y1,x0:x1]
            if i==2:
                # Original red glyphs, not the surrounding rounded box.
                mask=((piece[:,:,2].astype(int)-piece[:,:,1].astype(int)>18)&(piece[:,:,1]<180)).astype(np.uint8)*255
            else:
                mask=(piece.min(axis=2)<175).astype(np.uint8)*255
            mask=cv2.dilate(mask,np.ones((3,3),np.uint8))
            big=np.zeros((720,1280),np.uint8);big[y0:y1,x0:x1]=mask
            self.masks.append(big)

    def render(self,frame,n):
        result=frame.copy()
        for i,(roi,text,pos,size,color) in enumerate(self.specs):
            mask=self.masks[i]
            ys,xs=np.where(mask>0)
            # Match original fade-in from actual source glyph contrast.
            if i==2:
                original=frame[ys,xs].astype(float)
                opacity=float(np.clip(np.percentile(original[:,2]-original[:,1],85)/70,0,1))
            else:
                # Compare to the actual blank-paper frame so labels cannot
                # appear before the source animation's text fade begins.
                valid=xs<600
                yy,xx=ys[valid],xs[valid]
                original=frame[yy,xx].astype(float)
                paper=self.blank[yy,xx].astype(float)
                reference=self.reference[yy,xx].astype(float)
                contrast=np.percentile((paper-original).max(axis=1),85)
                full=np.percentile((paper-reference).max(axis=1),85)
                opacity=float(np.clip(contrast/max(full,1),0,1))
            if i<2:
                # Paper is stationary. Clone the exact pre-reveal paper,
                # avoiding outlines left behind by glyph inpainting.
                x0,y0,x1,y1=roi
                result[y0:y1,x0:x1]=self.blank[y0:y1,x0:x1]
                if i==0:
                    badge=frame[84:89,780:820].mean(axis=(0,1))
                    clean=self.blank[84:89,780:820].mean(axis=(0,1))
                    if np.abs(badge-clean).max()>5:
                        # The badge's left corner overlaps the obsolete title.
                        # Restore it from its symmetric clean right corner;
                        # no animation or wording in the badge is replaced.
                        yellow=badge[2]-badge[0]>35 and badge[1]-badge[0]>25
                        left,right,bottom=(630,974,129) if yellow else (639,965,126)
                        width=668-left
                        result[108:bottom,left:668]=frame[108:bottom,right-width+1:right+1][:,::-1]
            else:
                result=cv2.inpaint(result,mask,3,cv2.INPAINT_TELEA)
            if opacity<0.03: continue
            overlay=Image.fromarray(cv2.cvtColor(result,cv2.COLOR_BGR2RGB))
            draw=ImageDraw.Draw(overlay);font=ImageFont.truetype(FONT,size)
            if i==2:
                bb=draw.textbbox((0,0),text,font=font)
                pos=((1280-(bb[2]-bb[0]))/2,344)
            draw.text(pos,text,font=font,fill=color,stroke_width=0)
            colored=cv2.cvtColor(np.array(overlay),cv2.COLOR_RGB2BGR)
            result=cv2.addWeighted(colored,opacity,result,1-opacity,0)
        return result

def frames(path):
    with av.open(str(path)) as c:
        c.streams.video[0].codec_context.thread_count=1
        for n,f in enumerate(c.decode(video=0)):
            yield n,f.to_ndarray(format='bgr24')

def prepare():
    OUT.mkdir(exist_ok=True)
    if not SOURCE.exists():
        assert sha(LIVE)==EXPECTED
        SOURCE.write_bytes(LIVE.read_bytes())
    assert sha(SOURCE)==EXPECTED
    selected={6069,6120,6270,6360,6440,6495}
    samples={n:im for n,im in frames(SOURCE) if n in selected}
    labels=Labels(samples[6270],samples[6069])
    boards=Boards()
    for n in [712,*[x[0]+30 for x in EVENTS],3640,3720,3780,3840,3920]:
        cv2.imwrite(str(OUT/f'preview-{n:05}.png'),boards.render(n))
    for n,im in samples.items():
        cv2.imwrite(str(OUT/f'preview-{n:05}.png'),labels.render(im,n))
    return boards,labels

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
    boards,labels=prepare()
    if args.preview:return
    assert not DEST.exists(),'Never overwrite a review candidate'
    protected={str(p):sha(p) for p in [LIVE,ASSET,ROOT/'lessons/loudest-voices.md',*sorted(ASSET.parent.glob('*.jpg'))]}
    replacements=[]
    readers=frames(SOURCE)
    current=None;proc=None
    for n,frame in readers:
        span=next((s for s in SPANS if s[0]<=n<s[1]),None)
        if span!=current:
            if proc:
                proc.stdin.close();assert proc.wait()==0;proc=None
            current=span
            if span:
                a,b,name=span
                leg=OUT/f'leg-{name}.mp4'
                command=[FF,'-v','error','-y','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720',
                         '-framerate','30','-i','-','-an','-c:v','libx264','-threads','2','-crf','18',
                         '-preset','medium','-pix_fmt','yuv420p','-profile:v','high','-level:v','3.1',
                         '-video_track_timescale','15360',str(leg)]
                proc=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=(OUT/f'encode-{name}.log').open('w'))
                replacements.append((a,b,leg))
                print('Encoding',name,flush=True)
        if span:
            im=labels.render(frame,n) if span[2]=='habits-labels' else boards.render(n)
            proc.stdin.write(im.tobytes())
    if proc:proc.stdin.close();assert proc.wait()==0
    assert n+1==6884
    source=av.open(str(SOURCE));video=source.streams.video[0];audio=source.streams.audio[0]
    packets=[];keys=[]
    for p in source.demux(video,audio):
        if p.dts is None:continue
        isvideo=p.stream.type=='video'
        f=round(float(p.pts*p.time_base)*30) if isvideo else None
        if isvideo and p.is_keyframe:keys.append(f)
        if isvideo and any(a<=f<b for a,b,_ in SPANS):continue
        packets.append((isvideo,p))
    legs=[]
    for a,b,path in replacements:
        assert a in keys and b in keys,'Replacement must align with source GOPs'
        leg=av.open(str(path));legs.append(leg);v=leg.streams.video[0]
        assert v.time_base==video.time_base
        assert v.codec_context.extradata==video.codec_context.extradata,'Incompatible SPS/PPS'
        count=0
        for p in leg.demux(v):
            if p.dts is None:continue
            p.pts+=a*512;p.dts+=a*512;packets.append((True,p));count+=1
        assert count==b-a
    packets.sort(key=lambda item:(item[1].dts*item[1].time_base,not item[0]))
    with av.open(str(DEST),'w',options={'movflags':'+faststart'}) as output:
        ov=output.add_stream_from_template(video);oa=output.add_stream_from_template(audio)
        for isvideo,p in packets:
            p.stream=ov if isvideo else oa;output.mux(p)
    manifest=dict(scope='Approved visual-only expert-board framing and habits-diagram label cleanup.',
                  source=str(SOURCE),source_sha256=EXPECTED,candidate=str(DEST),candidate_sha256=sha(DEST),
                  source_limitation='Raw rolls absent; encode changed spans once from SHA-locked v7, remux all unaffected GOPs.',
                  audio='Every original AAC packet and timestamp remuxed; no narration or pause changes.',
                  fps=30,frames=6884,duration=6884/30,
                  replacements=[dict(start_frame=a,end_frame_exclusive=b,label=name) for a,b,name in SPANS],
                  board_asset=str(ASSET),board_asset_sha256=sha(ASSET),
                  unusual_treatment='Complete original active card at left plus a magnified viewport of the current source section at right. Full card always retained; no text reflow or canonical-asset alteration.',
                  card_rects=CARDS,section_rects=SECTIONS,spoken_onsets=EVENTS,summary_onsets=SUMMARY,
                  ring_stroke_px=4,label_replacements=[dict(old=o,new=s[1]) for o,s in zip(['MACHINE CAPABILITY [EXPONENTIAL / HIGH-FREQ]','HUMAN ADAPTATION [LINEAR / HABIT INERTIA]','STRUCTURAL FRICTION GAP'],labels.specs)],
                  boundaries=[dict(frame=f,label=name+suffix) for a,b,name in SPANS for f,suffix in [(a,'-in'),(b,'-out')]],
                  protected_hashes=protected,pronunciation='Confirmed correct by David; narration preserved.',
                  status='Review candidate only; not installed or published.')
    assert all(sha(p)==h for p,h in protected.items())
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(DEST,flush=True)

if __name__=='__main__':main()
