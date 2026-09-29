#!/usr/bin/env python3
"""Visual-only v10 repair: clean opening and trace neighborhood silhouettes."""
import copy,json,subprocess,functools,argparse
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
from PIL import ImageDraw
import build_vector_space_v10 as previous
from editspec_build import Reader,sha
from ken_burns_path import window
from build_embeddings_v7 import Renderer
ROOT=previous.ROOT;OUT=ROOT/'video-audit/vector-space-build-2026-09-29-v11';DEST=ROOT/'Prompts/vector-space-v11.mp4'
SOURCE=ROOT/'Prompts/vector-space-v10.mp4';EXPECTED='5a735042f7c25a5ccaad2747058ef3c9653eec3d457e85201f9b29eba077e296'
base=previous.base

def opening(t):
 im=base.PAPER.copy();d=ImageDraw.Draw(im);C=base.COL
 base.tile(d,(255,230,430,365),'IT',C['blue'],'#dce9ff',60);base.arrow(d,(450,300),(525,300),C['ink'])
 updated=t>=7.2;vals=['.41','.06','…'] if updated else ['.12','−.34','…']
 base.text(d,(805,187),'Numbers updated for context' if updated else 'A row of numbers',36,bold=True,anchor='mm')
 for j,v in enumerate(vals):base.tile(d,(555+j*165,245,695+j*165,350),v,C['purple'],size=40)
 base.text(d,(805,394),'Illustrative values from the lesson',22,'#677078',anchor='mm')
 if t>=5.8:base.text(d,(660,455),'The layers change the numbers',28,bold=True,anchor='mm')
 if 12.5<=t<18.4:base.text(d,(640,565),'No exact match?',48,C['purple'],True,'mm')
 if t>=18.4:base.text(d,(640,560),'Relationships matter too.',40,C['teal'],True,'mm')
 return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)

def contours():
 im=cv2.imread(str(base.ASSETS['nbhd']));result=[]
 for rect,color in [((140,170,675,745),(254,245,242)),((940,325,1445,725),(250,244,245))]:
  x,y,x2,y2=rect;roi=im[y:y2,x:x2];dist=np.linalg.norm(roi.astype(float)-np.array(color),axis=2)
  mask=np.uint8(dist<6)*255;mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
  cs,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE);c=max(cs,key=cv2.contourArea);hull=cv2.convexHull(c)
  # The shaded neighborhoods are ellipses. Fit their outside silhouettes,
  # ignoring text and dotted lines that interrupt the pale fill.
  (cx,cy),(aw,ah),angle=cv2.fitEllipse(hull);theta=np.linspace(0,2*np.pi,721)[:-1];rot=np.deg2rad(angle)
  local=np.column_stack([aw/2*np.cos(theta),ah/2*np.sin(theta)])
  matrix=np.array([[np.cos(rot),-np.sin(rot)],[np.sin(rot),np.cos(rot)]])
  c=local@matrix.T+np.array([cx+x,cy+y]);result.append(c)
 return result

class Neighborhood:
 def __init__(self,spec,paths):
  self.original=copy.deepcopy(spec);clean=copy.deepcopy(spec);clean['rings']=[];self.r=Renderer(clean);self.paths=paths
 @functools.lru_cache(maxsize=4)
 def at(self,n):
  im=self.r.at(0)[0].copy()
  ring=next((i for i,r in enumerate(self.original['rings']) if r['start']<=n<r['end']),None)
  if ring is None:return im
  c=self.paths[ring]+np.array([34,1]);x,y,w,h=window(*self.r.cameras[n],16/9,self.r.iw,self.r.ih);points=(c-np.array([x,y]))*(1280/w)
  up=4;mask=np.zeros((720*up,1280*up),np.uint8)
  cv2.polylines(mask,[np.round(points*up).astype(np.int32)],True,255,4*up,lineType=cv2.LINE_AA)
  alpha=cv2.resize(mask,(1280,720),interpolation=cv2.INTER_AREA).astype(float)/255
  hx=self.original['rings'][ring]['color'].lstrip('#');rgb=[int(hx[i:i+2],16) for i in [0,2,4]];bgr=np.array(rgb[::-1])
  return np.uint8(np.round(im*(1-alpha[:,:,None])+bgr*alpha[:,:,None]))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');a=ap.parse_args();assert not DEST.exists();assert sha(SOURCE)==EXPECTED
 previous.OUT=OUT;previous.DEST=DEST
 old,b,rs,timeline,donors,m=previous.setup();paths=contours();nb=Neighborhood(m['board_specs']['nbhd'],paths)
 (OUT/'neighborhood-contours.json').write_text(json.dumps([c.round(3).tolist() for c in paths]))
 for n in [0,105,292]:cv2.imwrite(str(OUT/'preview'/f'neighborhood-{n}.jpg'),nb.at(n))
 for t in [6,16,21]:cv2.imwrite(str(OUT/'preview'/f'opening-{t}.jpg'),opening(t))
 m.update(source_revision=str(SOURCE),source_revision_sha256=EXPECTED,scope='Visual-only: remove opening yellow marker; follow actual soft/hot neighborhood shapes with 4px outlines.',approval='User requested removal of opening yellow highlight and neighborhood outlines matching the shaded shapes.',audio_treatment='Copy exact v10 compressed AAC; no timing or narration change.',changed_frames=[[174,697],[3289,3749]],neighborhood_contour_source=str(base.ASSETS['nbhd']),neighborhood_contours_file=str(OUT/'neighborhood-contours.json'))
 m['protected_hashes'][str(SOURCE)]=EXPECTED
 if a.prepare_only:
  (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));return
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(SOURCE),'-map','0:v','-map','1:a','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 # Three fixed neighborhood states; cache them rather than a full-frame cache per timestamp.
 nbframes={-1:nb.at(0),0:nb.at(105),1:nb.at(292)}
 for s in timeline:
  k=s['visual'];n=s['end_frame']-s['start_frame'];rd=None
  if k in donors:rd=Reader(donors[k]);dn=int(rd.c.get(cv2.CAP_PROP_FRAME_COUNT))
  for f in range(n):
   if k=='embedding':im=opening(f/30)
   elif k=='nbhd':im=nbframes[-1 if f<102 else 0 if f<289 else 1]
   elif k in rs:im=rs[k].at(f)[0]
   elif k=='bridge':im=previous.bridge(f/30)
   elif k in donors:im=rd.at(round(f/max(1,n-1)*(dn-1)))
   elif k=='close':
    q=np.clip((f-48)/149,0,1);z=1+.2*q*q*(3-2*q);ci=b.close_img;h,w=ci.shape[:2];cw=w/z;ch=cw*9/16;im=cv2.warpAffine(ci,np.float32([[cw/1280,0,(w-cw)/2],[0,ch/720,(h-ch)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   else:im=base.sketch(k,f/30)
   p.stdin.write(im.tobytes())
  if rd:rd.c.release()
  print('Rendered',k,s['end_frame'],flush=True)
 p.stdin.close();assert p.wait()==0;assert all(sha(Path(p))==h for p,h in m['protected_hashes'].items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));print(DEST)
if __name__=='__main__':main()
