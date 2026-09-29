#!/usr/bin/env python3
"""Approved two-label visual repair; reconstruct v10 picture and copy its audio."""
from pathlib import Path
import argparse,json,subprocess,functools
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
import build_how_ai_answers_v10 as prior
from editspec_build import Reader,sha
cv2.setNumThreads(2)
ROOT=prior.ROOT
OUT=ROOT/'video-audit/how-ai-answers-repair-2026-09-29-v11'
DEST=ROOT/'Prompts/how-ai-answers-v11.mp4'
AUDIO=ROOT/'Prompts/how-ai-answers-v10.mp4'
EXPECTED='451fa414b0e0fbc971e71b6ccb7ae8d1663e001b1a1ed25c297466e373d73b3e'
DOG=(5069,5579);EOS=(5980,6178)
FONT=str(ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf')

class SequentialReader(Reader):
 def __init__(self,p):
  self.c=cv2.VideoCapture(str(p),cv2.CAP_FFMPEG,[cv2.CAP_PROP_N_THREADS,2])
  assert self.c.isOpened()
  self.n=-1;self.im=None
Reader=SequentialReader
prior.prior.Reader=SequentialReader

def font(size,weight=700):
 f=ImageFont.truetype(FONT,size)
 f.set_variation_by_axes([weight]);return f

@functools.lru_cache(maxsize=32)
def dog_overlay(w,h):
 im=Image.new('RGBA',(w*3,h*3));d=ImageDraw.Draw(im)
 d.text((w*1.5,h*1.22),'You',font=font(round(w*.26*3)),fill='#fffaf3',anchor='mm')
 d.text((w*1.5,h*1.98),'First reply token',font=font(round(w*.065*3),600),fill='#fffaf3',anchor='mm')
 return np.array(im.resize((w,h),Image.Resampling.LANCZOS))

def dog(im):
 b,g,r=[im[:,:,j].astype(float) for j in range(3)]
 m=((r-g)>45)&((b-g)>25)&(r>90)
 m[:180]=False;m[580:]=False;m[:,:800]=False;m[:,1140:]=False
 ys,xs=np.nonzero(m);assert len(xs)>5000
 x0,x1=int(np.percentile(xs,1)),int(np.percentile(xs,99));y0,y1=int(np.percentile(ys,1)),int(np.percentile(ys,99))
 w,h=x1-x0+1,y1-y0+1;ov=dog_overlay(w,h);a=ov[:,:,3:4]/255
 im[y0:y1+1,x0:x1+1]=(im[y0:y1+1,x0:x1+1]*(1-a)+ov[:,:,:3][:,:,::-1]*a).round().astype(np.uint8)
 return im,dict(box=[x0,y0,w,h])

ROIS=[(1038,120,1118,230),(223,480,310,635)]

def brighten(im,refs):
 stats=[]
 for (x0,y0,x1,y1),ref in zip(ROIS,refs):
  p=im[y0:y1,x0:x1].astype(float);c=np.maximum(p[:,:,0],p[:,:,2])-p[:,:,1]
  # Exclude long token-border components; retain the original glyphs and fades.
  threshold=max(4,float(c.max())*.24)
  n,labels,st,_=cv2.connectedComponentsWithStats((c>threshold).astype(np.uint8))
  keep=np.zeros(c.shape,np.uint8)
  for k in range(1,n):
   x,y,w,h,area=st[k]
   if 5<=h<=32 and w<79 and area>=8 and w/h<8:keep[labels==k]=1
  keep=cv2.dilate(keep,np.ones((3,3),np.uint8))
  alpha=np.clip((c-2)/(ref['chroma']-2),0,1)*keep
  delta=np.array([246,246,246])-np.array(ref['color'])
  im[y0:y1,x0:x1]=np.clip(p+alpha[:,:,None]*delta,0,255).round().astype(np.uint8)
  stats.append(int(np.sum(alpha>.05)))
 return im,dict(glyph_pixels=stats)

def setup():
 assert sha(AUDIO)==EXPECTED
 prior.OUT=OUT;prior.DEST=DEST
 snap,rs,qr,mapped,title,m=prior.prepare()
 m['based_on']='how-ai-answers-v10'
 m['approval']='User: skip optional suggestion; build the other two into the video. Label dog-comparison square You and brighten EOS labels; no narration/timing changes; review build only.'
 m['audio']='Copy exact v10 AAC stream; no re-encoding, changes, or new audio seams.'
 m['audio_source']=str(AUDIO);m['audio_source_sha256']=EXPECTED
 m['protected'][str(AUDIO)]=EXPECTED
 m['visual_repairs']=[dict(name='Dog comparison label',frames=DOG),dict(name='EOS glyph contrast including fades',frames=EOS)]
 m['boundaries']=sorted(set(m['boundaries']+list(DOG)+list(EOS)))
 donor_ids=sorted({it[1] for it in mapped[:prior.prior.TITLE_START] if it and it[0] not in rs}|{7319})
 rd=Reader(snap);donors={f:rd.at(f).copy() for f in donor_ids};rd.c.release()
 def frame(f,rd):
  if prior.INSERT<=f<prior.INSERT+prior.ADDED:return qr.at(f-prior.INSERT)[0].copy()
  old=f if f<prior.INSERT else f-prior.ADDED
  sf=old if old<prior.prior.CUT_A else old+prior.prior.REMOVED
  if prior.prior.TITLE_START<=old<prior.prior.CUT_A:return title.copy()
  if prior.prior.CUT_A<=old<prior.prior.CUT_A+(7319-prior.prior.CUT_B):return donors[7319].copy()
  item=mapped[sf]
  return rd.at(sf) if item is None else rs[item[0]].at(item[1])[0].copy() if item[0] in rs else donors[item[1]].copy()
 rd=Reader(snap);ref=frame(6090,rd);rd.c.release();refs=[]
 for x0,y0,x1,y1 in ROIS:
  p=ref[y0:y1,x0:x1].astype(float);c=np.maximum(p[:,:,0],p[:,:,2])-p[:,:,1];sel=c>=np.percentile(c,99)
  refs.append(dict(color=np.median(p[sel],axis=0).tolist(),chroma=float(np.median(c[sel]))))
 m['eos_color_references']=refs
 return snap,frame,m,refs

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a candidate'
 snap,frame,m,refs=setup();rd=Reader(snap);log=[];samples={5068,5069,5100,5200,5308,5309,5450,5578,5579,5980,5995,6010,6025,6040,6060,6075,6090,6110,6135,6155,6170,6177,6178}
 (OUT/'preview').mkdir(exist_ok=True)
 proc=None
 if not args.preview:
  proc=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(AUDIO),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','4','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for f in range(prior.TOTAL):
  if args.preview and f not in samples:continue
  im=frame(f,rd);meta={}
  if DOG[0]<=f<DOG[1]:im,meta=dog(im)
  if EOS[0]<=f<EOS[1]:im,meta=brighten(im,refs)
  if meta:log.append(dict(frame=f,**meta))
  if f in samples:cv2.imwrite(str(OUT/'preview'/f'{f:05d}.png'),im)
  if proc:proc.stdin.write(im.tobytes())
  if f%1000==999:print('Rendered',f+1,flush=True)
 if proc:
  proc.stdin.close();assert proc.wait()==0;m['candidate_sha256']=sha(DEST)
 rd.c.release()
 assert all(sha(Path(p))==h for p,h in m['protected'].items())
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 (OUT/('preview-tracking.json' if args.preview else 'tracking.json')).write_text(json.dumps(log,indent=2)+'\n')
 print('Preview ready' if args.preview else str(DEST),flush=True)
if __name__=='__main__':main()
