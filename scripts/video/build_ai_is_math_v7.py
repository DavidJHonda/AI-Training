#!/usr/bin/env python3
"""Approved repair of published AI Is Math: one sentence cut, canonical boards,
4px highlights and existing illustration donors. Review only; never publishes."""
from pathlib import Path
import argparse, functools, json, shutil, subprocess, tempfile
import cv2, numpy as np, imageio_ffmpeg
from editspec_build import sha, readwav, writewav, Reader
from build_understand_ai_opener_v12 import draw_ring
from ken_burns_path import ring_px
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'course-assets/ai-is-math/ai-is-math.mp4'
OUT=ROOT/'video-audit/ai-is-math-repair-2026-09-27-v7'
DEST=ROOT/'Prompts/ai-is-math-v7.mp4'
EXPECTED='de2305a0df2bd399e3316a554ad0b79c2bb11248521d6ad8912f2be36869ae0d'
CUT=(4452,4578); TOTAL=6310; FPS=30; SPF=1600
# Source-time intervals; cut frames never enter the output. Donors are clean
# sequentially decoded frames, gently pushed only within the approved crop.
ROWS=[(0,463,'chip'),(463,671,'context'),(671,1326,'history'),
      (1326,1834,'math'),(1834,2577,'coins'),(2577,3420,'hands'),
      (3420,4152,'clue'),(4152,4290,'hands'),(4290,4452,'clue'),
      (4578,4995,'context'),(4995,5742,'next'),(5742,6070,'repeat'),(6070,6310,'close')]
DONORS={'chip':(750,[240,110,800,450]),'context':(540,[0,0,1280,720]),
        'history':(900,[0,0,1280,720]),'hands':(3230,[0,0,1280,720]),
        'repeat':(5880,[0,0,1280,720])}
ASSETS={k:ROOT/f'course-assets/ai-is-math/ai-is-math-{v}.jpg' for k,v in
        [('math','the-math'),('coins','two-coins'),('clue','conditional-probability'),('next','what-comes-next'),('close','close')]}
P='#4f2fc4';N='#6e51ff';G='#0f7a4a';R='#c41f28'
# Source narration onsets; explicit ends allow full unmarked re-entry.
EVENTS={
 'math':[(54.3,59.6,[40,127,1560,447],P,'formula')],
 'coins':[(64.2,69.1,[40,127,1560,254],P,'scenario'),(69.1,77.66,[118,346,1518,582],N,'four outcomes'),(77.66,79.8,[116,346,373,582],G,'both heads'),(79.8,83.48,[252,700,1283,852],P,'one over four'),(83.48,85.9,[40,987,1560,1075],N,'25 percent')],
 'clue':[(118,125.66,[846,386,1495,627],R,'ruled out'),(126.36,130.08,[116,386,780,627],N,'remaining pair'),(130.08,134.72,[116,386,373,627],G,'both heads'),(134.72,138.4,[252,740,1285,892],G,'one over two'),(144.1,148.4,[40,1027,1560,1115],N,'50 percent')],
 'next':[(169.5,170.56,[40,127,1560,254],P,'question'),(170.56,177.54,[505,318,1090,440],P,'reply'),(177.54,184.02,[312,510,1288,656],P,'candidates'),(184.02,190.4,[312,510,1288,656],P,'candidate percentages')]
}

def outframe(n):return n if n<CUT[0] else n-(CUT[1]-CUT[0])
class Render:
 def __init__(self,snapshot):
  self.donors={};rd=Reader(snapshot)
  for f in sorted(set(v[0] for v in DONORS.values())):
   im=rd.at(f)
   for k,(n,rect) in DONORS.items():
    if n==f:
     x,y,w,h=rect;self.donors[k]=cv2.resize(im[y:y+h,x:x+w],(1280,720),interpolation=cv2.INTER_CUBIC)
  rd.c.release();self.bases={};self.geometry={}
  for k,p in ASSETS.items():
   im=cv2.imread(str(p));h,w=im.shape[:2];s=min(1220/w,680/h);nw,nh=round(w*s),round(h*s);x,y=(1280-nw)//2,(720-nh)//2
   base=np.full((720,1280,3),(251,245,246),np.uint8);base[y:y+nh,x:x+nw]=cv2.resize(im,(nw,nh),interpolation=cv2.INTER_AREA)
   self.bases[k]=base;self.geometry[k]=dict(asset=str(p.relative_to(ROOT)),sha256=sha(p),size=[w,h],render_size=[nw,nh],offset=[x,y],scale=[nw/w,nh/h],density='compact',camera='full view, static')
 @functools.lru_cache(maxsize=32)
 def board(self,key,event):
  im=self.bases[key].copy()
  if event>=0:
   _,_,rect,color,label=EVENTS[key][event];g=self.geometry[key];sx,sy=g['scale'];x,y=g['offset'];r=[rect[0]*sx+x,rect[1]*sy+y,rect[2]*sx+x,rect[3]*sy+y]
   assert min(r)>=3 and r[2]<1277 and r[3]<717
   bgr=tuple(int(color[i:i+2],16) for i in (5,3,1));draw_ring(im,*r,bgr,18*sx,ring_px(720))
  return im
 def frame(self,n,row):
  a,b,key=row
  if key in EVENTS:
   hits=[i for i,e in enumerate(EVENTS[key]) if round(e[0]*30)<=n<round(e[1]*30)]
   return self.board(key,hits[-1] if hits else -1)
  im=self.donors[key];progress=(n-a)/max(1,b-a-1);scale=1+.025*progress
  # Pure whole-drawing push. It never resets a board-duration counter.
  return cv2.warpAffine(im,np.array([[scale,0,640*(1-scale)],[0,scale,360*(1-scale)]],np.float32),(1280,720),flags=cv2.INTER_CUBIC)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert sha(SOURCE)==EXPECTED;assert not DEST.exists(),'Never overwrite a candidate'
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 record=OUT/'source-snapshot.json'
 if record.exists():snapshot=Path(json.loads(record.read_text())['path'])
 else:
  snapshot=Path(tempfile.mkdtemp(prefix='math-v7-'))/'published.mp4';shutil.copyfile(SOURCE,snapshot);record.write_text(json.dumps(dict(path=str(snapshot),sha256=EXPECTED),indent=2))
 assert sha(snapshot)==EXPECTED
 protected={str(p):sha(p) for p in [SOURCE,ROOT/'lessons/ai-is-math.md',*ASSETS.values()]}
 render=Render(snapshot);ff=imageio_ffmpeg.get_ffmpeg_exe()
 subprocess.run([ff,'-y','-v','error','-i',str(snapshot),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'source.wav')],check=True)
 audio=readwav(OUT/'source.wav')[:TOTAL*SPF];a,b=[n*SPF for n in CUT];edited=np.concatenate([audio[:a],audio[b:]])
 # Five-ms ramps in measured silence; no speech gain or processing.
 ramp=240;edited[a-ramp:a]*=np.linspace(1,0,ramp);edited[a:a+ramp]*=np.linspace(0,1,ramp)
 writewav(OUT/'edited.wav',edited);expected=TOTAL-(CUT[1]-CUT[0]);assert len(edited)==expected*SPF
 samples=[]
 for row in ROWS:
  a,b,key=row
  if key=='close':continue
  ns=sorted(set([a,b-1]+[max(a,round(e[0]*30)+5) for e in EVENTS.get(key,[]) if a<=round(e[0]*30)<b]))
  for n in ns:
   p=OUT/'preview'/f'{n:05d}-{key}.png';cv2.imwrite(str(p),render.frame(n,row));samples.append(dict(source_frame=n,output_frame=outframe(n),key=key,path=str(p)))
 timeline=[dict(source=[a,b],output=[outframe(a),outframe(b)],key=k,seconds=(b-a)/30) for a,b,k in ROWS]
 # outframe at the removed interval's left edge must refer to its left limit.
 timeline[8]['output'][1]=CUT[0]
 manifest=dict(source=str(SOURCE),source_sha256=EXPECTED,snapshot=str(snapshot),candidate=str(DEST),frames=expected,seconds=expected/30,audio_cut_frames=list(CUT),audio_cut_words='This is exactly how large language models function.',audio_fade_samples=ramp,protected=protected,boards=render.geometry,events=EVENTS,timeline=timeline,donors=DONORS,previews=samples,accepted_exception='Illustrative probabilities and remaining 47% are visible on the canonical dog board; narration retained by owner decision. Coin/clue/dog numerical explanations use ~25s unbroken boards to avoid hiding their calculations.')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 if args.prepare_only:return
 cmd=[ff,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE);reader=Reader(snapshot);count=0
 for row in ROWS:
  a,b,key=row
  for n in range(a,b):
   im=reader.at(n) if key=='close' else render.frame(n,row)
   p.stdin.write(im.tobytes());count+=1
  print(key,count,flush=True)
 p.stdin.close();assert p.wait()==0;reader.c.release();assert count==expected
 assert all(sha(Path(path))==v for path,v in protected.items())
 manifest['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(DEST,flush=True)
if __name__=='__main__':main()
