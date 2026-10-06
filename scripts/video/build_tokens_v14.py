#!/usr/bin/env python3
"""Narrow owner-requested repair: bubbles, cat cards, and remove ID recitation.
Reconstruct from original media and canonical boards, encoding only once.
"""
from pathlib import Path
import argparse,copy,functools,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Build,sha,readwav,writewav
from build_tokens_v12 import Video,ROOT,S4,S6,TOTAL as OLD_TOTAL
from build_tokens_v9 import Renderer
from ken_burns_path import window,ring_px
from build_understand_ai_opener_v12 import draw_ring
from gemini_mark import clean_frame

OUT=ROOT/'video-audit/tokens-repair-2026-10-06-v14'
PREV=ROOT/'video-audit/tokens-build-2026-10-04-v13'
DEST=ROOT/'Prompts/tokens-v14.mp4'
CUT_A,CUT_B=6130,6432
TOTAL=OLD_TOTAL-(CUT_B-CUT_A)

def previous_frame(f):return f if f<CUT_A else f+CUT_B-CUT_A
def output_frame(f):
 assert not CUT_A<=f<CUT_B
 return f if f<CUT_A else f-(CUT_B-CUT_A)

class EdgeRenderer(Renderer):
 """Ring outer edge matches the measured component instead of floating outside."""
 @functools.lru_cache(maxsize=12)
 def render(self,camera,active):
  x,y,w,h=window(*camera,16/9,self.iw,self.ih);up=self.up
  xx,yy,ww,hh=[round(v*up) for v in (x,y,w,h)]
  base=cv2.resize(self.big[yy:yy+hh,xx:xx+ww],(1280,720),interpolation=cv2.INTER_AREA if ww>1280 else cv2.INTER_LANCZOS4)
  im=base.copy();geo=[]
  for i in active:
   a,b,(rx,ry,rw,rh),color,pad,radius=self.rings[i];s=1280/w;t=ring_px(720);half=t/2
   outer=[(rx-x)*s,(ry-y)*s,(rx+rw-x)*s,(ry+rh-y)*s]
   assert outer[0]>=0 and outer[1]>=0 and outer[2]<1280 and outer[3]<720,(outer,camera)
   box=[outer[0]+half,outer[1]+half,outer[2]-half,outer[3]-half]
   draw_ring(im,*box,color,max(0,radius*s-half),t)
   geo.append(dict(outer=outer,color_bgr=color,stroke=t))
  return im,base,geo

def prepare():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 old=json.loads((PREV/'edit-manifest.json').read_text())
 assert sha(Path(old['candidate']))==old['render_sha256']
 assert all(sha(Path(k))==v for k,v in old['sources'].items())
 b=Build(ROOT,S4,OUT,DEST);b.make_close('tokens')
 specs={};renderers={}
 for board in old['boards']:
  key=board['key'];spec=json.loads((PREV/f'leg-{key}.json').read_text())
  # Fresh lossless canvases from exactly the same canonical assets.
  asset=ROOT/'course-assets/tokens'/board['asset']
  path,cw,ch,ox,oy=b.compose(asset,key)
  assert [ox,oy]==board['canvas_offset']
  spec['image']=str(path)
  if key=='chat':
   for ring,rect,radius in zip(spec['rings'],[[780,208,711,94],[110,388,1211,196]],[28,30]):
    ring.update(rect=[rect[0]+ox,rect[1]+oy,*rect[2:]],radius=radius)
  if key=='cat':
   # Extra stage around the same JPG permits centering each complete card.
   stage=cv2.imread(str(path));canvas=np.full((1238,2200,3),stage[0,0],np.uint8)
   canvas[169:1069,300:1900]=stage;cv2.imwrite(str(path),canvas)
   for ring,rect in zip(spec['rings'],[[41,126,742,589],[816,126,743,589],[40,756,1520,89]]):
    ring.update(rect=[rect[0]+300,rect[1]+oy+169,*rect[2:]],radius=14)
   full=[1100,619,1600];left=[712,596.5,1140];right=[1487.5,596.5,1140]
   spec['beats']=[
    dict(label='unmarked complete board',frames=139,**{'from':full,'to':full}),
    dict(label='dive to complete human card',frames=24,to=left),
    dict(label='human card',frames=114,to=left),
    dict(label='return through full view',frames=24,to=full),
    dict(label='dive to complete AI card',frames=24,to=right),
    dict(label='AI card',frames=276,to=right),
    dict(label='return for takeaway',frames=24,to=full),
    dict(label='full takeaway',frames=102,to=full)]
   assert sum(x['frames'] for x in spec['beats'])==727
  specs[key]=spec
  renderers[key]=(EdgeRenderer if key in ['chat','cat'] else Renderer)(spec)
  (OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n')
  if key in ['chat','cat']:
   rd=renderers[key]
   samples={0,len(rd.cameras)-1}|{r['start']+30 for r in spec['rings']}
   for f in sorted(samples):cv2.imwrite(str(OUT/'preview'/f'{key}-{f:04d}.png'),rd.at(f)[0])
 # PCM from the previous pristine assembly, not a decode of a lossy candidate.
 audio=readwav(PREV.parent/'tokens-build-2026-10-04-v12/edited.wav')
 audio=np.r_[audio[:CUT_A*1600],audio[CUT_B*1600:]]
 assert len(audio)==TOTAL*1600
 writewav(OUT/'edited.wav',audio)
 protected={str(p):sha(p) for p in [ROOT/'index.html',ROOT/'lessons/tokens.md',ROOT/'course-assets/tokens/tokens.mp4',*sorted((ROOT/'course-assets/tokens').glob('*.jpg'))]}
 m=dict(candidate=str(DEST),parent=old['candidate'],parent_sha256=old['render_sha256'],scope='Narrow authorized bubble/card repair and removal of spoken ID values',sources=old['sources'],frames=TOTAL,fps=30,duration=TOTAL/30,removed_parent_frames=[CUT_A,CUT_B],removed_parent_seconds=[CUT_A/30,CUT_B/30],cut_words='For unbelievable, the ID for un is 359, the ID for belie is 32898, and the ID for vable is 24694.',join_output_frame=CUT_A,protected=protected,boards=copy.deepcopy(old['boards']),close_start=output_frame(old['close_start']),ring_stroke=ring_px(720),audio_source=str(PREV.parent/'tokens-build-2026-10-04-v12/edited.wav'),audio_speed_unchanged=True,extra_pauses=0)
 for board in m['boards']:
  board['parent_start_frame']=board['start_frame'];board['parent_end_frame']=board['end_frame']
  board['start_frame']=output_frame(board['start_frame']);board['end_frame']=output_frame(board['end_frame'])
  if board['key']=='cat':board.update(density='Complete-card zoom at 1.404x after full opening',canvas_offset=[300,176])
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 return b,renderers,old['boards'],m

class Repaired(Video):
 def at(self,f):
  # Preserve both corrections made in v13, but read original rolls.
  if 2054<=f<2266:return clean_frame(self.read(S4,2263+round((f-2054)*125/211),'correct-blocks'),self.mask)[0]
  if 6541<=f<6841:return clean_frame(self.read(S6,6180+round((f-6541)*294/299),'correct-reply'),self.mask)[0]
  return super().at(f)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a review candidate'
 b,r,boards,m=prepare()
 if args.prepare_only:print('Prepared',TOTAL,'frames;',TOTAL/30,'seconds');return
 v=Repaired(b,r,boards);ff=imageio_ffmpeg.get_ffmpeg_exe()
 p=subprocess.Popen([ff,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for f in range(TOTAL):
  p.stdin.write(v.at(previous_frame(f)).tobytes())
  if f%900==899:print('Rendered',f+1,'/',TOTAL,flush=True)
 p.stdin.close();assert p.wait()==0;v.close()
 assert all(sha(Path(k))==val for k,val in m['protected'].items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print(DEST)
if __name__=='__main__':main()
