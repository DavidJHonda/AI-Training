#!/usr/bin/env python3
"""Approved Tokens repair: three narrated examples, original pictures/motion,
corrected vocabulary subtitle, fixed 4px outlines. Review only."""
from pathlib import Path
import argparse,functools,json,subprocess,copy
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
from editspec_build import Build,Reader,sha,readwav,writewav
from ken_burns_path import resolve,rings_for,window,smoothstep,ring_px
from build_understand_ai_opener_v12 import draw_ring
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'course-assets/tokens/tokens.mp4'
EXPECTED='48f170a1ed6794de08903ca578570dab9186d80ac605896bc9718c7e9433aa1f'
OLD=ROOT/'video-audit/tokens-build-2026-09-22'
OUT=ROOT/'video-audit/tokens-repair-2026-09-27-v9'
DEST=ROOT/'Prompts/tokens-v9.mp4'
TOTAL=9158;FPS=30;SPF=1600
# Each boundary selected inside a measured speech-free gap; do not trust ASR
# word ends alone (several actual tails extend ~0.3s beyond their ASR stamp).
KEEP=[(0,6285),(6485,6626),(6874,7629),(8182,9158)]
CUTS=[(6285,6485),(6626,6874),(7629,8182)]
SPLITS_IN,SPLITS_OUT=6198,8188

def mapping():
 return [f for a,b in KEEP for f in range(a,b)]
def output_frame(f):
 cursor=0
 for a,b in KEEP:
  if a<=f<b:return cursor+f-a
  cursor+=b-a
 raise ValueError(f)

class Renderer:
 def __init__(self,spec):
  self.spec=spec;im=cv2.imread(spec['image']);self.ih,self.iw=im.shape[:2];self.up=spec['upscale']
  self.big=cv2.resize(im,(self.iw*self.up,self.ih*self.up),interpolation=cv2.INTER_LANCZOS4);self.rings=rings_for(spec);self.cameras=[]
  for label,n,a,b in resolve(spec,16/9,1280,self.up):
   for k in range(n):
    t=smoothstep(k/(n-1)) if n>1 else 1;self.cameras.append(tuple(a[j]+(b[j]-a[j])*t for j in range(3)))
 @functools.lru_cache(maxsize=12)
 def render(self,camera,active):
  x,y,w,h=window(*camera,16/9,self.iw,self.ih);up=self.up;xx,yy,ww,hh=[round(v*up) for v in (x,y,w,h)]
  base=cv2.resize(self.big[yy:yy+hh,xx:xx+ww],(1280,720),interpolation=cv2.INTER_AREA if ww>1280 else cv2.INTER_LANCZOS4);im=base.copy();geo=[]
  for i in active:
   a,b,(rx,ry,rw,rh),color,pad,radius=self.rings[i];s=1280/w;t=ring_px(720);half=t/2
   box=[(rx-pad-x)*s-half,(ry-pad-y)*s-half,(rx+rw+pad-x)*s+half,(ry+rh+pad-y)*s+half]
   assert box[0]-half>=0 and box[1]-half>=0 and box[2]+half<1280 and box[3]+half<720,(box,camera)
   draw_ring(im,*box,color,radius*s+half,t);geo.append(dict(box=box,color_bgr=color))
  return im,base,geo
 def at(self,n):
  active=tuple(i for i,r in enumerate(self.rings) if r[0]<=n<r[1]);return self.render(self.cameras[n],active)

class ChartLabel:
 """Native video text correction: track the existing subtitle through its
 entrance/exit and replace only its glyphs. Preserve original animation."""
 def __init__(self,reference):
  self.rect=(150,296,190,26);x,y,w,h=self.rect
  self.template=cv2.cvtColor(reference[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY)
  self.mask=(self.template<175).astype(np.uint8)*255
  self.erase=cv2.dilate(self.mask,np.ones((3,3),np.uint8))
  font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',14*4)
  alpha=Image.new('L',(w*4,h*4),0);d=ImageDraw.Draw(alpha)
  text='GPT-4o / o200k_base';bb=d.textbbox((0,0),text,font=font);tw=bb[2]-bb[0];th=bb[3]-bb[1]
  d.text(((w*4-tw)/2,(h*4-th)/2-bb[1]),text,font=font,fill=255)
  self.alpha=np.asarray(alpha.resize((w,h),Image.Resampling.LANCZOS),dtype=np.float32)/255
  self.reference_contrast=float(np.median(self.template[self.mask>0])-np.median(self.template[self.mask==0]))
 def at(self,im,n):
  if not 3715<=n<4070:return im,None
  gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);search=gray[270:370,125:365]
  score=cv2.matchTemplate(search,self.template,cv2.TM_CCOEFF_NORMED);_,peak,_,loc=cv2.minMaxLoc(score)
  if peak<.40:return im,dict(frame=n,score=peak,patched=False)
  x,y=125+loc[0],270+loc[1];w,h=self.rect[2:];patch=gray[y:y+h,x:x+w]
  bg=float(np.median(patch[self.mask==0]));contrast=float(np.median(patch[self.mask>0])-bg);opacity=np.clip(contrast/self.reference_contrast,0,1)
  mask=np.zeros((720,1280),np.uint8);mask[y:y+h,x:x+w]=self.erase
  out=cv2.inpaint(im,mask,3,cv2.INPAINT_TELEA)
  # Dark gray matching the source, with source-measured fade opacity.
  alpha=(self.alpha*opacity)[:,:,None];old=out[y:y+h,x:x+w].astype(float)
  out[y:y+h,x:x+w]=np.rint(old*(1-alpha)+np.array([77,83,76])*alpha).astype(np.uint8)
  return out,dict(frame=n,score=peak,patched=True,box=[x,y,w,h],opacity=float(opacity))

def setup():
 old=json.loads((OLD/'edit-manifest.json').read_text());assert old['render_sha256']==EXPECTED
 snapshot=Path(json.loads((OUT/'source-snapshot.json').read_text())['path']);assert sha(snapshot)==EXPECTED
 b=Build(ROOT,snapshot,OUT,DEST);b.tall_margin=True;renderers={};specs={}
 for key,meta in old['boards'].items():
  asset=ROOT/meta['asset'];assert sha(asset)==meta['sha256'];canvas,cw,ch,ox,oy=b.compose(asset,key);assert [ox,oy]==meta['canvas_offset']
  spec=json.loads((OLD/f'leg-{key}.json').read_text());spec['image']=str(canvas)
  if key=='5-splits':
   # Full opening followed by three purposeful whole-row views. All five rows
   # remain in the canonical asset. No dive into the two omitted walkthroughs.
   full=[1237.,696.,2474.];basket=[1249.5,484.5,1586.5546218487395];heart=[1249.5,864.5,1586.5546218487395];url=[1249.5,1094.5,1586.5546218487395]
   duration=output_frame(SPLITS_OUT)-SPLITS_IN
   heart_at=output_frame(6874)-SPLITS_IN;url_at=output_frame(7398)-SPLITS_IN
   spec['beats']=[dict(label='full opening',frames=90,**{'from':full,'to':full}),dict(label='to basketball',frames=24,to=basket),dict(label='basketball',frames=heart_at-114,to=basket),dict(label='to spaces and symbols',frames=24,to=heart),dict(label='spaces and symbols',frames=url_at-heart_at-24,to=heart),dict(label='to web address',frames=24,to=url),dict(label='web address count',frames=duration-url_at-24,to=url)]
   saved=copy.deepcopy(spec['rings']);spec['rings']=[saved[1],saved[3],saved[4]]
   for r,start,end in zip(spec['rings'],[90,heart_at+24,url_at+24],[heart_at,url_at,duration]):r.update(start=start,end=end)
  specs[key]=spec;renderers[key]=Renderer(spec);(OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n')
 # Map the published file's boards back to their retained raw-leg local frame.
 mapped=[None]*TOTAL
 for row in old['timeline']:
  for n in range(row['start_frame'],row['end_frame']):
   if n>=old['close']['start_frame']:continue
   if row['kind']=='room_tone':mapped[n]=mapped[n-1]
   elif row.get('visual') in old['boards']:
    key=row['visual'];mapped[n]=(key,row['source_start']+n-row['start_frame']-old['boards'][key]['src_in'])
 rd=Reader(snapshot);chart=ChartLabel(rd.at(3975));rd.c.release()
 return snapshot,old,renderers,specs,mapped,chart

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a review candidate';assert sha(SOURCE)==EXPECTED
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 snapshot,old,renderers,specs,mapped,chart=setup();protected={str(p):sha(p) for p in [SOURCE,ROOT/'lessons/tokens.md',*sorted((ROOT/'course-assets/tokens').glob('*.jpg'))]}
 source=readwav(OUT/'source.wav')[:TOTAL*SPF];parts=[source[a*SPF:b*SPF].copy() for a,b in KEEP];fade=240;joins=[];count=0
 for i,part in enumerate(parts):
  if i:part[:fade]*=np.linspace(0,1,fade);joins.append(count)
  if i<len(parts)-1:part[-fade:]*=np.linspace(1,0,fade)
  count+=len(part)//SPF
 audio=np.concatenate(parts);writewav(OUT/'edited.wav',audio);assert count==8157
 # Prepared states are inspected before the long render; chart corrections are
 # inspected throughout both fades, not only on the settled card.
 samples=[]
 for key,renderer in renderers.items():
  spec=specs[key];ns={0,len(renderer.cameras)-1};cursor=0
  for beat in spec['beats']:ns|={cursor,cursor+beat['frames']-1};cursor+=beat['frames']
  for r in renderer.rings:ns.add(min(len(renderer.cameras)-1,r[0]+30))
  for n in sorted(ns):
   im,_,geo=renderer.at(n);p=OUT/'preview'/f'{key}-{n:04d}.png';cv2.imwrite(str(p),im);samples.append(dict(key=key,local_frame=n,path=str(p),rings=geo))
 rd=Reader(snapshot);chart_checks=[]
 for n in range(3715,4070):
  im=rd.at(n);patched,info=chart.at(im,n);chart_checks.append(info)
  if n%15==0:cv2.imwrite(str(OUT/'preview'/f'chart-{n}.png'),patched)
 rd.c.release()
 manifest=dict(source=str(SOURCE),source_sha256=EXPECTED,snapshot=str(snapshot),candidate=str(DEST),fps=30,frames=count,duration=count/30,keep=KEEP,cuts=CUTS,joins=joins,audio_ramp_samples=fade,boards=old['boards'],specs=specs,prepared_states=samples,chart_checks=chart_checks,protected=protected,approval='Three narrated examples (basketball, I heart AI, URL count without fragment recitation), retain all five board rows; existing graphics and motion; correct tokenizer subtitle; 4px rings. No publication.')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 if args.prepare_only:return
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 rd=Reader(snapshot)
 for out,n in enumerate(mapping()):
  item=mapped[n]
  if item:
   key,local=item
   if key=='5-splits':local=out-SPLITS_IN
   im=renderers[key].at(local)[0]
  else:im=chart.at(rd.at(n),n)[0]
  p.stdin.write(im.tobytes())
  if out%1000==999:print('Rendered',out+1,flush=True)
 p.stdin.close();assert p.wait()==0;rd.c.release();assert all(sha(Path(p))==v for p,v in protected.items())
 manifest['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
