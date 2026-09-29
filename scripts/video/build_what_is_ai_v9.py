#!/usr/bin/env python3
"""Raw roll 5, required visual corrections and canonical board finishing; audio copied."""
from pathlib import Path
import argparse, json, subprocess
import cv2
import numpy as np
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from editspec_build import Build, Reader, sha, BLUE, PURPLE, NEUTRAL
from build_embeddings_v7 import Renderer
from gemini_mark import clean_frame, glyph_mask

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/what-is-ai-5.mp4'
OUT=ROOT/'video-audit/what-is-ai-build-2026-09-29-v9'
DEST=ROOT/'Prompts/what-is-ai-v9.mp4'
TOTAL=5477
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
ASSETS={k:ROOT/'course-assets/what-is-ai'/v for k,v in {
 'desk':'what-is-ai-ask-the-desk.jpg','types':'what-is-ai-types.jpg',
 'picks':'what-is-ai-same-goal.jpg','close':'what-is-ai-close.jpg'}.items()}

def text(im,words,xy,size=25,color=(35,57,71),bold=False,anchor='mm'):
    p=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
    ImageDraw.Draw(p).text(xy,words,font=ImageFont.truetype(BOLD if bold else FONT,size),fill=color,anchor=anchor)
    return cv2.cvtColor(np.array(p),cv2.COLOR_RGB2BGR)

def label_erase(im,box,donor):
    x,y,w,h=box;dx,dy=donor
    im[y:y+h,x:x+w]=im[dy:dy+h,dx:dx+w].copy()

def setup():
    b=Build(ROOT,SRC,OUT,DEST)
    T=lambda label,at,rect,col,cam=None,full=False:dict(label=label,at=at,rects=[rect],color=col,cam=cam or rect,full_view=full)
    b.board('desk',ASSETS['desk'],641,1577,'compact',[
      T('Desk question',23.92,[402,155,796,288],BLUE),
      T('AI question',28.18,[1142,155,1524,288],PURPLE),
      T('AI list',31.9,[1190,539,1470,792],PURPLE)],banner_at=48.38,push=False)
    left=[40,127,780,1134]; right=[820,127,1560,1134]
    b.board('types-rec',ASSETS['types'],2248,2685,'dense',[
      T('Recommendation card',78.58,left,BLUE,left),
      T('Recommendation job',80.5,[57,625,762,721],BLUE,left),
      T('Recommendation mechanism',84.00,[57,745,762,926],BLUE,left)],push=False)
    b.board('types-summary',ASSETS['types'],3480,3713,'compact',[],banner_at=118.0,push=False)
    pl=[40,282,780,1382];pr=[820,282,1560,1382]
    b.board('picks-rec',ASSETS['picks'],3713,4061,'dense',[
      T('Superhero scenario',128.06,[40,128,1560,248],NEUTRAL,full=True),
      T('Recommendation card',130.30,pl,BLUE,pl),
      T('Find a superhero movie',132.00,[57,882,762,1023],BLUE,pl)],push=False)
    b.board('picks-gen',ASSETS['picks'],4453,4907,'dense',[
      T('Generative card',150.44,pr,PURPLE,pr),
      T('Write disagreeing teammates',152.0,[837,882,1542,1023],PURPLE,pr),
      T('Maya and Leo dialogue',155.86,[837,1060,1542,1263],PURPLE,pr)],push=False)
    b.board('picks-summary',ASSETS['picks'],4991,5138,'compact',[],banner_at=168.37,push=False)
    b.make_close('llms')
    specs={k:json.loads((OUT/f'leg-{k}.json').read_text()) for k in b.boards}
    # Two equally sized complete-card cameras; no text-only crops.
    renderers={k:Renderer(v) for k,v in specs.items()}
    close_spec=dict(image=str(OUT/'close.png'),fps=30,out_w=1280,out_h=720,upscale=1,
      beats=[dict(label='hold',frames=48,**{'from':[1920,1080,3840]},to=[1920,1080,3840]),
             dict(label='push',frames=150,to=[1920,1080,3200]),
             dict(label='settle',frames=TOTAL-5138-198,to=[1920,1080,3200])],rings=[])
    renderers['close']=Renderer(close_spec)
    (OUT/'leg-close.json').write_text(json.dumps(close_spec,indent=2)+'\n')
    intervals=[(641,1020,'desk'),(1320,1577,'desk'),(2248,2685,'types-rec'),
      (3480,3713,'types-summary'),(3713,4061,'picks-rec'),(4453,4907,'picks-gen'),
      (4991,5138,'picks-summary'),(5138,TOTAL,'close')]
    starts={k:v['src_in'] for k,v in b.boards.items()};starts['close']=5138
    # A list-only cutaway reuses this roll's existing ten-topic illustration.
    # Its source is before the unsupported ratings appear.
    cleanlist=cv2.imread(str(OUT/'source/01815.png'))
    cleanlist=history(cleanlist,1815)
    crop=cleanlist[110:530,490:1140]
    listshot=cv2.resize(crop,(1056,672),interpolation=cv2.INTER_LANCZOS4)
    plate=np.full((720,1280,3),tuple(int(v) for v in cleanlist[5,5]),np.uint8)
    plate[24:696,112:1168]=listshot
    cv2.imwrite(str(OUT/'assets/history-list-cutaway.png'),plate)
    keyboard=cv2.imread(str(OUT/'assets/keyboard-clean.png'))
    keyboard=cv2.resize(keyboard,(1280,720),interpolation=cv2.INTER_AREA)
    boundaries=sorted({641,1020,1320,1577,1752,1815,1928,2094,2248,2685,2955,3075,
      3250,3480,3713,4061,4095,4374,4453,4907,4991,5138})
    meta=dict(scope='Visual production from raw roll 5. Required graphics corrections; optional graphics/narration changes declined.',
      approval='User: Let us do those changes that were not optional. And build the video.',
      source=str(SRC),source_sha256=sha(SRC),candidate=str(DEST),fps=30,frames=TOTAL,duration=TOTAL/30,
      audio='Packet copy, no cuts, grafts, processing or added silence.',boards=b.boards,
      board_intervals=intervals,boundaries=boundaries,close=dict(start=5138,hold=48,push=150,settle=141,zoom=1.2),
      changed_graphics=[dict(span=[1752,1928],change='Remove topic quality scores/tints; preserve original list'),
        dict(span=[1928,2094],change='Imagegen cleanup of keyboard marginal annotations'),
        dict(span=[2955,3075],change='Remove originality guarantee while preserving forming-star animation'),
        dict(span=[3250,3480],change='Retitle outputs Examples of Generative AI'),
        dict(span=[4095,4374],change='Track moving catalog tiles and erase fabricated scores')],
      preserved_optional=['AI Processing Pipeline','Prompt + Learned Patterns','CURATION','INVENTION','All original narration'],
      protected={str(p):sha(p) for p in [SRC,*ASSETS.values(),ROOT/'course-assets/what-is-ai/what-is-ai.mp4']})
    return b,renderers,intervals,starts,plate,keyboard,meta

def history(im,n):
    im=im.copy()
    if n>=1815:
      # Remove only the score columns; undo red verdict tints inside those three cards.
      for row,col in [(4,0),(2,1),(4,1)]:
        x0=496+324*col;y0=188+67.5*row
        roi=im[int(y0)+3:int(y0)+53,x0+3:x0+303]
        # Preserve black topic text and blue border; replace pink interior pixels.
        m=(roi[:,:,2].astype(int)-roi[:,:,0].astype(int)>6)&(roi.min(axis=2)>180)
        roi[m]=(231,233,227)
      for x in [730,1054]:
        for y in [202,270,337,405,473]:
          # Blank paper inside each list tile has no annotation.
          color=np.median(im[y:y+27,x-28:x-15],axis=(0,1)).astype('uint8')
          im[y:y+27,x:x+64]=color
    return im

def movie(im,n,tracking):
    im=im.copy()
    delta=tracking.get(n,0)
    if n<4095:return im
    # Five unselected tiles stay the same size; horizontal translation is measured per frame.
    for base,y in [(650,201),(884,201),(416,403),(650,403),(884,403)]:
      x=base+delta
      color=np.median(im[y+28:y+36,x+2:x+65],axis=(0,1)).astype('uint8')
      im[y:y+25,x:x+70]=color
    # The chosen thumbnail scales slightly. Detect its blue fill so the erasure follows it.
    B,G,R=[im[:,:,j].astype(int) for j in range(3)]
    m=((B-G>20)&(G-R>15)&(B>90)).astype('uint8');m[:185]=0;m[291:]=0;m[:,:300+delta]=0;m[:,515+delta:]=0
    _,_,st,_=cv2.connectedComponentsWithStats(m)
    candidates=[(x,y,w,h,a) for x,y,w,h,a in st[1:] if w>100 and h>45]
    if candidates:
      x,y,w,h,_=max(candidates,key=lambda r:r[4]);x=int(x);y=int(y);w=int(w);h=int(h)
      # Preserve the selection badge and the complete star; erase only its digits.
      bx=x+round(w*.565)
      color=np.median(im[y+5:y+18,bx+3:bx+10],axis=(0,1)).astype('uint8')
      im[y+3:y+23,bx+12:x+w-8]=color
      # Once the gold badge is solid, erase its exact rounded silhouette, not a
      # bounding rectangle that could clip the neighboring star illustration.
      if n>=4165:
        roi=im[y:y+27,bx-2:x+w+1]
        cb,cg,cr=[roi[:,:,j].astype(int) for j in range(3)]
        gold=((cr-cb>45)&(cg-cb>35)).astype('uint8')*255
        contours,_=cv2.findContours(gold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if contours:
          contour=max(contours,key=cv2.contourArea)
          if cv2.contourArea(contour)>400:
            filled=np.zeros_like(gold);cv2.drawContours(filled,[contour],-1,255,-1)
            blue=np.median(im[y+8:y+20,x+10:x+45],axis=(0,1)).astype('uint8')
            roi[filled>0]=blue
    # Top-match tab: keep its meaning, suppress the numeric suffix with a tracked label.
    if n>=4155:
      x=321+delta;y=153
      patch=im[y:y+26,x:x+170].copy()
      gold=np.array([90,209,239])
      strength=float(np.clip((np.median(patch[:,:,2]-patch[:,:,0].astype(float))-4)/110,0,1))
      if strength>.03:
        color=np.median(im[156:161,x+8:x+160],axis=(0,1)).astype('uint8')
        im[158:177,x+8:x+164]=color
        im=text(im,'TOP MATCH',(x+85,167),14,(30,30,25),True)
    # Profile's fixed annotation fades in after the grid shifts. Preserve the fade.
    if n>=4245:
      x,y,w,h=136,369,198,27
      strength=float(np.clip((245-float(np.mean(im[y+9:y+17,x+8:x+16])))/185,0,1))
      if strength>.01:
        color=np.median(im[y+7:y+19,x+5:x+15],axis=(0,1)).astype('uint8')
        im[y+4:y+h-3,x+16:x+w-12]=color
        col=tuple(int(235*(1-strength)+25*strength) for _ in range(3))
        im=text(im,'Interest: Action',(235,383),14,col)
    return im

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    assert not DEST.exists(),'Never overwrite a review candidate'
    b,renderers,intervals,starts,plate,keyboard,meta=setup()
    raw=json.loads((OUT/'movie-tracking.json').read_text());tracking={}
    last=0
    for f,boxes in raw:
      if boxes:last=min(x for x,y,w,h,a in boxes)-544
      tracking[f]=last
    rd=Reader(SRC);mask=glyph_mask();corner={'clone':0,'inpaint':0,'declined':[]}
    def visual(n,im):
      for a,z,key in intervals:
        if a<=n<z:return renderers[key].at(n-starts[key])[0]
      if 1020<=n<1320:return plate.copy()
      if 1928<=n<2094:
        # A gentle push retains motion in the cleaned still.
        q=(n-1928)/165;scale=1+.025*q
        return cv2.warpAffine(keyboard,np.float32([[scale,0,640*(1-scale)],[0,scale,360*(1-scale)]]),(1280,720),flags=cv2.INTER_CUBIC)
      if 1752<=n<1928:im=history(im,n)
      if 2955<=n<3075:label_erase(im,(440,553,400,40),(440,615))
      if 3250<=n<3480:
        label_erase(im,(220,43,850,43),(220,0))
        im=text(im,'Examples of Generative AI',(640,66),29,(28,50,67),True)
      if 4061<=n<4374:im=movie(im,n,tracking)
      im,how=clean_frame(im,mask)
      if how:corner[how]+=1
      else:corner['declined'].append(n)
      return im
    wanted=set(range(0,TOTAL,120))|set(range(4061,4374,10))|{n for t in meta['boundaries'] for n in [t-1,t,t+1]}
    for key,board in b.boards.items():
      wanted.add(board['src_in'])
      for r in board['rings']:wanted.add(board['src_in']+r['start']+28)
    wanted|={TOTAL-1,5138+48,5138+198}
    wanted={n for n in wanted if 0<=n<TOTAL}
    meta['preview_frames']=sorted(wanted)
    p=None
    if not args.prepare_only:
      ff=imageio_ffmpeg.get_ffmpeg_exe()
      p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
        '-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-threads','4',
        '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for n in range(TOTAL):
      if args.prepare_only and n not in wanted:continue
      im=visual(n,rd.at(n))
      if n in wanted:cv2.imwrite(str(OUT/'preview'/f'{n:05d}.jpg'),im)
      if p:p.stdin.write(im.tobytes())
      if not args.prepare_only and n%1000==999:print(f'Rendered {n+1}/{TOTAL}',flush=True)
    rd.c.release()
    if p:p.stdin.close();assert p.wait()==0;meta['candidate_sha256']=sha(DEST)
    assert all(sha(Path(p))==h for p,h in meta['protected'].items())
    meta['corner_cleanup']=corner
    (OUT/'edit-manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
    print('Prepared' if args.prepare_only else 'Built',DEST,flush=True)

if __name__=='__main__':main()
