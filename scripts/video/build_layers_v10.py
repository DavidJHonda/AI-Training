#!/usr/bin/env python3
"""Approved visual-only readability repair. Reconstruct v9; copy its audio."""
from pathlib import Path
import argparse, copy, json, subprocess, functools
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
import build_layers_v8 as b8
import build_layers_v9 as b9
from build_embeddings_v7 import Renderer
from editspec_build import Reader, sha
from gemini_mark import glyph_mask

ROOT = b8.ROOT
OUT = ROOT / 'video-audit/layers-build-2026-09-29-v10'
DEST = ROOT / 'Prompts/layers-v10.mp4'
BASE = ROOT / 'Prompts/layers-v9.mp4'
EXPECTED = '40b88ef892c5bf0c72490e96544c5f2f31b88dfc1f24a208a3d705bbb952b2ca'
FONT = Path('/Users/davidobrien/Library/Fonts')
TOTAL = 6101
CHANGED = [(2595,3095), (5004,5780)]
BOUNDARIES = [2595,2625,3065,3095,5004,5133,5148,5382,5400,5405,5600,5620,5780]
cv2.setNumThreads(2)
TRACKS = {}
PANELS = [('benefit',(171,543,461,708),'Benefit',['Understanding','Reasoning'],(28,105,128)),
          ('cost',(819,543,1109,708),'Cost',['Computing power','Time'],(147,35,62))]

def track_panels():
    """Track source panel motion, including partially clipped bottom corners."""
    cap=cv2.VideoCapture(str(BASE));frames={};n=0
    while n<5780:
        ok,im=cap.read();assert ok
        if n>=5400:frames[n]=im
        n+=1
    cap.release();sift=cv2.SIFT_create(nfeatures=600,contrastThreshold=.02);bf=cv2.BFMatcher()
    ref=frames[5700];data={}
    for name,(x,y,x1,y1),_,_,_ in PANELS:
        refgray=cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY)
        k,d=sift.detectAndCompute(refgray[y:y1,x:x1],None)
        pts=np.array([z.pt for z in k],np.float32)+[x,y]
        prev=np.array([[1.,0.,0.],[0.,1.,0.]])
        for f,im in frames.items():
            xx,yy=max(0,x-65),450;gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            kk,dd=sift.detectAndCompute(gray[yy:720,xx:x1+65],None)
            good=[] if dd is None else [a for a,b in bf.knnMatch(d,dd,k=2) if a.distance<.7*b.distance]
            err=None;opacity=0.
            if len(good)>=4:
                a=np.float32([pts[z.queryIdx] for z in good]);b=np.float32([kk[z.trainIdx].pt for z in good])+[xx,yy]
                m,inl=cv2.estimateAffinePartial2D(a,b,method=cv2.RANSAC,ransacReprojThreshold=2)
                if m is not None and inl.sum()>=4 and .98<np.hypot(*m[0,:2])<1.02:
                    err=float(np.median(np.linalg.norm(a@m[:,:2].T+m[:,2]-b,axis=1)[inl[:,0]>0]));prev=m
                    aligned=cv2.warpAffine(gray,cv2.invertAffineTransform(m),(1280,720))
                    rr=refgray[y+15:y+115,x+20:x1-20].astype(float)
                    aa=aligned[y+15:y+115,x+20:x1-20].astype(float)
                    ink=rr<140
                    opacity=float(np.clip(np.median((239-aa[ink])/(239-rr[ink])),0,1))
            data.setdefault(str(f),{})[name]=dict(matrix=prev.tolist(),matches=len(good),error=err,opacity=opacity)
    (OUT/'balance-tracking.json').write_text(json.dumps(data,indent=2));return data

@functools.lru_cache(maxsize=2)
def panel_tile(name):
    _,(x,y,x1,y1),title,lines,color=next(p for p in PANELS if p[0]==name)
    # Video overlay in the original panel coordinate system, slightly padded
    # to cover compression fringes. Complete lower corners are restored.
    im=Image.new('RGBA',(1280,860));d=ImageDraw.Draw(im)
    d.rounded_rectangle((x-2,y-2,x1+2,y1+2),radius=11,fill=(238,250,241,255),outline=(*color,255),width=2)
    for words,cy,size,bold in [(title,y+36,27,True),(lines[0],y+81,23,False),(lines[1],y+115,23,False)]:
        tile=Image.fromarray(text_tile(words,size,bold,color if bold else (44,60,56)))
        im.alpha_composite(tile,(round((x+x1-tile.width)/2),round(cy-tile.height/2)))
    a=np.array(im);a[:,:,:3]=a[:,:,:3][:,:,::-1];return a

@functools.lru_cache(maxsize=64)
def text_tile(text, size, bold, color):
    font = ImageFont.truetype(str(FONT / ('AvenirNextforINTUIT-Bold.otf' if bold else 'AvenirNextforINTUIT-Medium.otf')), size*3)
    box = font.getbbox(text)
    im = Image.new('RGBA', (box[2]+12, box[3]-box[1]+12))
    ImageDraw.Draw(im).text((6,6-box[1]),text,font=font,fill=(*color,255))
    im = im.resize((round(im.width/3),round(im.height/3)), Image.Resampling.LANCZOS)
    return np.array(im)

def text(im, wording, cx, cy, size=28, bold=False, color=(26,78,101), alpha=1):
    tile=text_tile(wording,size,bold,color); h,w=tile.shape[:2]
    x,y=round(cx-w/2),round(cy-h/2)
    assert x>=0 and y>=0 and x+w<=1280 and y+h<=720,(wording,x,y,w,h)
    a=tile[:,:,3:4]/255*alpha
    im[y:y+h,x:x+w]=np.round(im[y:y+h,x:x+w]*(1-a)+tile[:,:,:3][:,:,::-1]*a).astype(np.uint8)

def row_background(im):
    return np.median(np.concatenate([im[:,8:150],im[:,1180:1270]],axis=1),axis=1).astype(np.uint8)

def clear(im, box, bg):
    x0,y0,x1,y1=box; im[y0:y1,x0:x1]=bg[y0:y1,None,:]

def ease(a,b,f):
    t=np.clip((f-a)/(b-a),0,1);return float(t*t*(3-2*t))

def late_frame(original, f, clean_patch):
    im=original.copy();bg=row_background(im)
    # Replace only the title band; the diagrams below retain their source frames.
    clear(im,(180,28,1110,116),bg)
    headings=[('Connecting words','Each layer adds information.'),
              ('Working through harder meaning','Sarcasm, story twists, and complicated reasoning.'),
              ('Why not keep adding layers?','More layers take more computing power and time.')]
    if f<5133:weights=[1,0,0]
    elif f<5148:
        t=ease(5133,5148,f);weights=[1-t,t,0]
    elif f<5382:weights=[0,1,0]
    elif f<5405:
        t=ease(5382,5405,f);weights=[0,1-t,t]
    else:weights=[0,0,1]
    # Cross-fade via a clean middle frame to avoid overlapping two titles.
    k=int(np.argmax(weights));alpha=max(weights)*2-1 if sum(v>0 for v in weights)>1 else 1
    text(im,headings[k][0],640,56,36,True,alpha=alpha)
    text(im,headings[k][1],640,100,24,color=(67,85,84),alpha=alpha)
    # Clean donor pixels from before the unwanted stage label was drawn.
    # This small patch leaves the animated arrow (above y=463) intact.
    if 5011<=f<5150:
        im[466:493,533:713]=clean_patch
    # Preserve example-box outlines and their fades; simplify only the lettering.
    for a,b,y,label in [(5172,5210,243,'Sarcasm'),(5223,5264,360,'Story twists'),(5265,5300,478,'Complicated reasoning')]:
        if f<a or f>=5400:continue
        # Original lettering is neutral gray; surrounding box color is sampled
        # from its own interior. The replacement follows the original fade.
        opacity=ease(a,b,f)*(1-ease(5382,5400,f))
        fill=np.median(im[y-13:y+14,742:765],axis=1).astype(np.uint8)
        im[y-13:y+14,770:1100]=fill[:,None,:]
        text(im,label,928,y,25,True,color=(44,60,56),alpha=opacity)
    if f>=5400:
        # The balance is a moving source drawing, not a replacement still.
        # Translate its foreground upward, keeping the original reveal/tilt.
        if f>=5594:
            # Cover only the central caption interior. Its plaque is stationary.
            roi=im[590:625,480:800]
            if len(roi):
                fill=np.median(im[590:625,468:476],axis=1).astype(np.uint8)
                im[590:625,477:804]=fill[:,None,:]
                text(im,'Benefit vs. cost',640,609,25,True,color=(252,251,239),alpha=ease(5594,5620,f))
        panels=[]
        for name,box,_,_,_ in PANELS:
            track=TRACKS[str(f)][name]
            if track['error'] is None:continue
            matrix=np.array(track['matrix']);opacity=track['opacity']
            x,y,x1,y1=box
            pts=np.array([[x-1,y-1],[x1+1,y-1],[x1+1,y1+1],[x-1,y1+1]],float)
            pts=pts@matrix[:,:2].T+matrix[:,2]
            mask=np.zeros((720,1280),np.uint8);cv2.fillConvexPoly(mask,np.round(pts).astype(np.int32),255)
            im[mask>0]=np.broadcast_to(bg[:,None,:],im.shape)[mask>0]
            shifted=matrix.copy();shifted[1,2]-=140
            layer=cv2.warpAffine(panel_tile(name),shifted,(1280,720),flags=cv2.INTER_LINEAR)
            panels.append((layer,opacity))
        lower=im[120:].astype(np.int16)-bg[120:,None,:].astype(np.int16)
        lower[np.max(np.abs(lower),axis=2)<4]=0
        im[120:]=bg[120:,None,:]
        # All balance foreground starts below y=440; moving it 140 px leaves
        # the whole figure clear of both the title and the bottom edge.
        residual=lower[140:]
        im[120:580]=np.clip(im[120:580].astype(np.int16)+residual,0,255).astype(np.uint8)
        for layer,opacity in panels:
            a=layer[:,:,3:4]/255*opacity
            im=np.round(im*(1-a)+layer[:,:,:3]*a).astype(np.uint8)
    return im

def setup():
    global TRACKS
    assert sha(BASE)==EXPECTED
    prior=json.loads((b9.OUT/'edit-manifest.json').read_text())
    for p,h in prior['protected'].items():
        if p.endswith('/transformer/transformer.mp4'):
            b8.TRANSFORMER=ROOT/'Prompts/transformer-v12.mp4'
            assert sha(b8.TRANSFORMER)==h
        elif p.endswith('.mp4') and 'course-assets/layers/' not in p:assert sha(Path(p))==h,p
    b8.OUT=OUT
    TRACKS=track_panels()
    old,snapshot,specs,renderers,mapped,stack=b8.setup()
    spec=copy.deepcopy(specs['2-numbers'])
    wide=[1141.,642.,2282.];zoom=[1141.,834.,1600.]
    spec['density']='dense numeric row; complete four-card row in one window'
    spec['beats']=[dict(label='full opening and return',frames=535,**{'from':wide,'to':wide}),
                   dict(label='dive to complete number-card row',frames=30,**{'from':wide,'to':zoom}),
                   dict(label='hold all four number cards',frames=440,**{'from':zoom,'to':zoom}),
                   dict(label='return before takeaway',frames=30,**{'from':zoom,'to':wide}),
                   dict(label='full takeaway',frames=121,**{'from':wide,'to':wide})]
    renderers['2-numbers']=Renderer(spec)
    (OUT/'leg-2-numbers.json').write_text(json.dumps(spec,indent=2))
    readers={'base':Reader(snapshot)}
    for row in b8.OVERRIDES:
        if row['kind']!='stack':readers[row['start']]=Reader(b8.ROLL1 if row['kind']=='horse' else b8.TRANSFORMER)
    # V9 local output frame 5010 maps to original snapshot frame 4750.
    patch_reader=Reader(snapshot);patch=patch_reader.at(4750)[466:493,533:713].copy();patch_reader.c.release()
    cv2.imwrite(str(OUT/'stage-label-clean-donor.png'),patch)
    images={s['asset']:cv2.imread(str(b9.ASSETS/s['asset'])) for s in b9.SPANS}
    return prior,readers,renderers,mapped,stack,patch,images,spec

def frame_at(f,context):
    prior,readers,renderers,mapped,stack,patch,images,spec=context
    span=next((s for s in b9.SPANS if s['start']<=f<s['end']),None)
    if span:
        im=b9.illustration(images[span['asset']],(f-span['start'])/(span['end']-span['start']-1))
    else:im,_=b8.frame_at(f,renderers,mapped,stack,readers,glyph_mask(),dict(clone=0,inpaint=0,declined=0))
    if 5004<=f<5780:im=late_frame(im,f,patch)
    return im

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    assert not DEST.exists(),'Never overwrite an owner review candidate'
    OUT.mkdir(exist_ok=True,parents=True);(OUT/'preview').mkdir(exist_ok=True)
    context=setup();prior=context[0]
    protected={str(p):sha(p) for p in [BASE,ROOT/'course-assets/layers/layers.mp4',*sorted((ROOT/'course-assets/layers').glob('*.jpg'))]}
    wanted={0,TOTAL-1,2546,2595,2609,2624,2700,2850,3000,3065,3080,3094,3100,
            5004,5010,5025,5040,5115,5132,5140,5148,5150,5180,5200,5228,5250,5280,5300,5350,5382,5390,5400,5405,5410,5430,5490,5520,5580,5594,5600,5610,5620,5700,5779,5780}
    for f in BOUNDARIES:wanted.update([f-1,f,f+1])
    if args.prepare_only:
        for f in sorted(wanted):cv2.imwrite(str(OUT/'preview'/f'{f:05d}.png'),frame_at(f,context))
    else:
        proc=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(BASE),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
        for f in range(TOTAL):
            im=frame_at(f,context);proc.stdin.write(im.tobytes())
            if f in wanted:cv2.imwrite(str(OUT/'preview'/f'{f:05d}.png'),im)
            if f%1000==999:print('Rendered',f+1,flush=True)
        proc.stdin.close();assert proc.wait()==0
    for r in context[1].values():r.c.release()
    assert all(sha(Path(p))==h for p,h in protected.items())
    manifest=dict(candidate=str(DEST),base=str(BASE),base_sha256=EXPECTED,frames=TOTAL,fps=30,duration=TOTAL/30,
                  scope='Approved narrow visual-only repair: number-card camera and late label/readability cleanup.',
                  approval='User: Build it please, following the September 29 live review.',
                  source_limit='Reconstructed from v9 original-source pipeline; the retained original snapshot is itself an earlier published edit. Earlier raw rolls are unavailable.',
                  changed_spans=CHANGED,boundaries=sorted(set(prior['boundaries']+BOUNDARIES)),spec=context[-1],
                  protected=protected,audio='v9 AAC stream copied unchanged',published=False,
                  final_sha256=sha(DEST) if DEST.exists() else None)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2))
    print(str(DEST) if DEST.exists() else 'Previews ready',flush=True)

if __name__=='__main__':main()
