#!/usr/bin/env python3
"""Approved narrow repair: remove recap and 'individual syllables'; 4px rings.
Preserve published visuals/camera paths elsewhere. Review candidate only."""
from pathlib import Path
import argparse,json,subprocess,functools
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Build,Reader,sha,readwav,writewav
from ken_burns_path import resolve,rings_for,window,smoothstep,ring_px
from build_understand_ai_opener_v12 import draw_ring
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'course-assets/embeddings/embeddings.mp4'
EXPECTED='a47d96f332712cba24a26bf7483eaaaf184bbac72327cd2499c20ebf5825237e'
OLD=ROOT/'video-audit/embeddings-stitch-2026-09-22/build'
OUT=ROOT/'video-audit/embeddings-repair-2026-09-27-v7'
DEST=ROOT/'Prompts/embeddings-v7.mp4'
TOTAL=8350;SPF=1600;FPS=30
CUTS=[(3195,3506),(7837,7879)]
KEEP=[(0,3195),(3506,7837),(7879,TOTAL)]
# The intra-sentence cut is 256 samples (5.333ms) ahead of the visual cut.
# Both edges sit in the measured gap: 261.228 and 262.628, avoiding the full
# syllables tail that continues beyond the original ASR boundary of 262.18.
AUDIO_CUTS=[(3195*SPF,3506*SPF),(12538944,12606144)]
AUDIO_KEEP=[(0,AUDIO_CUTS[0][0]),(AUDIO_CUTS[0][1],AUDIO_CUTS[1][0]),(AUDIO_CUTS[1][1],TOTAL*SPF)]
def mapping():return [f for a,b in KEEP for f in range(a,b)]
def output_frame(f):
 for i,n in enumerate(mapping()):
  if n==f:return i
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

def setup():
 old=json.loads((OLD/'edit-manifest.json').read_text());assert old['render_sha256']==EXPECTED
 snapshot=Path(json.loads((OUT/'source-snapshot.json').read_text())['path']);assert sha(snapshot)==EXPECTED
 b=Build(ROOT,snapshot,OUT,DEST);renderers={};specs={};mapped=[None]*TOTAL
 for key,meta in old['boards'].items():
  asset=ROOT/meta['asset'];assert sha(asset)==meta['sha256'];canvas,cw,ch,ox,oy=b.compose(asset,key);assert [ox,oy]==meta['canvas_offset']
  spec=json.loads((OLD/f'leg-{key}.json').read_text());spec['image']=str(canvas);specs[key]=spec;renderers[key]=Renderer(spec)
  (OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n')
 for row in old['timeline']:
  key=row.get('visual')
  if key not in old['boards']:continue
  for n in range(row['start_frame'],row['end_frame']):
   local=row.get('video_start',row['source_start'])+n-row['start_frame']-old['boards'][key]['src_in']
   mapped[n]=(key,local)
 return snapshot,old,renderers,specs,mapped

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a review candidate';assert sha(SOURCE)==EXPECTED
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 snapshot,old,renderers,specs,mapped=setup()
 protected={str(p):sha(p) for p in [SOURCE,ROOT/'lessons/embeddings.md',ROOT/'gemini-notebook/embeddings/PROMPT.txt',*sorted((ROOT/'course-assets/embeddings').glob('*.jpg'))]}
 source=readwav(OUT/'source.wav')[:TOTAL*SPF];parts=[source[a:b].copy() for a,b in AUDIO_KEEP];fade=240
 for i,part in enumerate(parts):
  if i:part[:fade]*=np.linspace(0,1,fade)
  if i<len(parts)-1:part[-fade:]*=np.linspace(1,0,fade)
 audio=np.concatenate(parts);writewav(OUT/'edited.wav',audio);frames=mapping();assert len(frames)==7997 and len(audio)==7997*SPF
 samples=[];wanted=set()
 for key,r in renderers.items():
  ns={0};cursor=0
  for beat in specs[key]['beats']:
   ns|={cursor,cursor+beat['frames']//2,cursor+beat['frames']-1};cursor+=beat['frames']
  for ring in r.rings:ns|={ring[0],ring[0]+15,ring[1]-1}
  available=[(i,n,mapped[n][1]) for i,n in enumerate(frames) if mapped[n] and mapped[n][0]==key]
  ns.add(available[-1][2])
  for out,n,local in available:
   if local not in ns:continue
   wanted.add(out);im,_,geo=r.at(local);p=OUT/'preview'/f'{out:05d}-{key}.jpg';cv2.imwrite(str(p),im)
   samples.append(dict(output_frame=out,source_frame=n,key=key,local_frame=local,path=str(p),rings=geo))
 spans={}
 for key in specs:
  ns=[i for i,n in enumerate(frames) if mapped[n] and mapped[n][0]==key];spans[key]=[min(ns),max(ns)+1]
 spans['close']=[output_frame(old['close']['start_frame']),len(frames)]
 boundaries=sorted(set([output_frame(b['frame']) for b in old['boundaries'] if any(a<=b['frame']<z for a,z in KEEP)]+[CUTS[0][0],CUTS[1][0]-(CUTS[0][1]-CUTS[0][0])]))
 m=dict(source=str(SOURCE),source_sha256=EXPECTED,snapshot=str(snapshot),candidate=str(DEST),fps=30,frames=len(frames),duration=len(frames)/30,keep=KEEP,cuts=CUTS,audio_keep_samples=AUDIO_KEEP,audio_cuts_samples=AUDIO_CUTS,audio_ramp_samples=fade,boards=old['boards'],specs=specs,prepared_states=samples,candidate_board_spans_frames=spans,boundaries=boundaries,protected=protected,approval='User approved the two proposed narration cuts and fixed 4px outlines. Preserve original graphics, camera paths, lesson boards, existing pauses and other narration. Build only; no publication.')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 if args.prepare_only:return
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 rd=Reader(snapshot)
 for out,n in enumerate(frames):
  item=mapped[n];im=renderers[item[0]].at(item[1])[0] if item else rd.at(n);p.stdin.write(im.tobytes())
  if out%1000==999:print('Rendered',out+1,flush=True)
 p.stdin.close();assert p.wait()==0;rd.c.release();assert all(sha(Path(p))==h for p,h in protected.items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
