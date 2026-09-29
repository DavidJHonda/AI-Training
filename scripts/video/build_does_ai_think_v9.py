#!/usr/bin/env python3
"""Approved best-of production edit: roll 2 body, roll 3 close, canonical boards.
Review candidate only. No changes to published media or lesson copy.
"""
from pathlib import Path
import argparse,json,subprocess
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
from editspec_build import Build,Reader,sha,readwav,writewav,fr,GREEN
from build_embeddings_v7 import Renderer
from gemini_mark import clean_frame,glyph_mask
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/does-ai-think-build-2026-09-29-v9'
DEST=ROOT/'Prompts/does-ai-think-v9.mp4'
BASE=ROOT/'Prompts/does-ai-think-2mp4.mp4'
D1=ROOT/'Prompts/does-ai-think-1.mp4'
D3=ROOT/'Prompts/does-ai-think-3.mp4'
ASSET=ROOT/'course-assets/does-ai-think'
HASHES={BASE:'3e2e5dfce47649f191b3c99923f7bcd4d47deb01bd67cd60b01c2a090af5b3d4',D1:'9e11a6192e39b2cbe9bb5bea5c00178c7ea627187b84566fd2bbf9fe0fbb0987',D3:'9b85c612b297fa5786dbda2594cbdff369eaf0489127a7a1c153006097c3e5f7'}
CLOSE=6246;TOTAL=6486
# Half-open OUTPUT spans. Retimed cutaways use their own monotonic decoders.
CUTAWAYS=[dict(start=1980,end=2085,source=str(BASE),source_start=1387,source_end=1492,label='Door and incoming note'),
 dict(start=2571,end=2760,source=str(BASE),source_start=1589,source_end=1778,label='Person following rules inside room'),
 dict(start=4215,end=4290,source=str(BASE),source_start=3660,source_end=3735,label='Learned network and input'),
 dict(start=4761,end=4845,source=str(D1),source_start=810,source_end=858,label='Next-word prediction reveal; slowed to retain the complete example'),
 dict(start=5340,end=5445,source=str(OUT/'student-checking-source.png'),label='Student checks answer against a source')]
BOARD_SPANS={'chinese':(1800,3305),'compare':(3839,5697)}

def chinese(b):
 key='chinese';asset=ASSET/'does-ai-think-chinese-room.jpg';p,w,h,ox,oy=b.compose(asset,key);full=[w/2,h/2,float(w)]
 moves=[('step-one',62.88,[50,150,560,420]),('step-two',70.16,[50,405,560,640]),('whole-phrase-chart',75.72,[940,230,1560,690]),('step-three',81.52,[50,628,560,860]),('outside-impression',93,[50,850,560,1125]),('full-takeaway',97.08,'full')]
 def cam(r):
  if r=='full':return full
  x0,y0,x1,y1=r;ww=max(x1-x0,(y1-y0)*16/9)*1.1;hh=ww*9/16
  return [min(max(ox+(x0+x1)/2,ox+40+ww/2),ox+1560-ww/2),min(max(oy+(y0+y1)/2,oy+128+hh/2),oy+1140-hh/2),ww]
 start,end=BOARD_SPANS[key];beats=[dict(label='full-unmarked',frames=fr(moves[0][1])-start,**{'from':full},to=full)]
 for i,(label,at,r) in enumerate(moves):
  nxt=fr(moves[i+1][1]) if i+1<len(moves) else end
  beats += [dict(label='to-'+label,frames=36,to=cam(r)),dict(label=label,frames=nxt-fr(at)-36,to=cam(r))]
 assert sum(x['frames'] for x in beats)==end-start
 spec=dict(image=str(p),fps=30,out_w=1280,out_h=720,upscale=3,beats=beats,rings=[])
 (OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n')
 b.boards[key]=dict(key=key,asset=str(asset.relative_to(ROOT)),sha256=sha(asset),src_in=start,src_out=end,density='dense illustration, approved camera-only exception',canvas_offset=[ox,oy],beats=beats,rings=[],full_view_frames=beats[0]['frames'])

def prepare():
 for p,h in HASHES.items():assert sha(p)==h,(p,'source changed')
 b=Build(ROOT,BASE,OUT,DEST,protected=[D1,D3,ASSET/'does-ai-think.mp4',ROOT/'lessons/does-ai-think.md',*sorted(ASSET.glob('*.jpg'))]);b.tall_margin=False
 if not (OUT/'base.wav').exists():
  subprocess.run([b.ff,'-v','error','-i',str(BASE),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'base.wav')],check=True)
 # Measured base gap 207.8433-208.4962; donor gap 183.4821-184.1149.
 # Source-specific seed, safely inside the speech-free base gap.
 b.audio=readwav(OUT/'base.wav');seed=b.audio[round(207.96*48000):round(208.06*48000)].copy();seed-=seed.mean();b.loop=np.r_[seed,seed[::-1]]
 b.tone_meta=dict(sample_rate=48000,room_tone_source=[207.96,208.06],room_tone_rms=float(np.sqrt(np.mean(seed*seed))),crossfade_ms=5)
 b.keep(0,CLOSE,'Candidate 2 complete teaching body')
 b.mark_close_start();b.graft(D3,5520,5682,'Candidate 3 exact closing lines','clean-close',picture_from=CLOSE,visual='close',gain_db=.6)
 b.pause(78,'Room-tone tail for the standard closing motion and settled hold');b.finish_audio();assert b.total==TOTAL
 writewav(OUT/'closing-join-preview.wav',readwav(OUT/'edited.wav')[round(201.5*48000):])
 writewav(OUT/'pronunciation-review-39s.wav',b.audio[round(33.5*48000):round(46.7*48000)])
 chinese(b)
 rects=[[60,672,1540,800],[60,815,1540,942],[60,958,1540,1085],[60,1102,1540,1228],[60,1245,1540,1372]]
 targets=[dict(label=l,at=t,rects=[r],cam=r,color=GREEN,radius=18) for l,t,r in zip(['Meaning','Experience','Word choice','Beauty','Uncertainty'],[136.32,144.04,153.04,162.52,172.76],rects)]
 b.board('compare',ASSET/'does-ai-think-side-by-side.jpg',3839,5697,'dense',targets,banner_at=185.56,pullback_at=184.56,banner=[40,1430,1560,1518])
 b.make_close('doesaithink')
 boundaries=sorted(set([v for pair in BOARD_SPANS.values() for v in pair]+[v for r in CUTAWAYS for v in (r['start'],r['end'])]+[CLOSE,6165]))
 m=b.manifest(dict(build_scope='Approved full production build for review; no shipping or publishing.',visual_board_spans=BOARD_SPANS,cutaways=CUTAWAYS,visual_boundaries=boundaries,ring_stroke_px=4,listening_performed=False,continuous_playback_review_performed=False,base_narration_unchanged_until_seconds=208.2,donor_gain_db=.6,loudness_measurements=dict(base_lufs=-20.61,donor_lufs=-21.21),close_note='8 seconds: 1.6 second hold, 5 second push, 1.4 second settled hold. Donor audio 5.4 seconds plus 2.6 seconds matched room tone.',label_repair=dict(start=6165,end=CLOSE,old='Internal Process Differs: Pattern Matching != Understanding',new='Similar answers can come from different processes.',reason='Replace a categorical implication with the lesson\'s qualified process comparison; preserve animation.'),cutaway_timing_correction='Evaluation mistakenly cited donor 1 at 2:33-2:40. Sequential inspection shows that is the course-board recreation; the independent prediction reveal is at 0:27-0:28.6.',unresolved_pronunciation='39s: thread/threat. Both ASR models report threat; listening is required. Optional clause retained because the error is unconfirmed.'))
 return b,m

class Assembly:
 def __init__(self,b):
  self.b=b;self.base=Reader(BASE);self.cutread={i:Reader(r['source']) for i,r in enumerate(CUTAWAYS) if r['source'].endswith('.mp4')};self.mask=glyph_mask();self.counts={'clone':0,'inpaint':0,'declined':[]}
  self.renderers={k:Renderer(json.loads((OUT/f'leg-{k}.json').read_text())) for k in BOARD_SPANS}
  self.photo=cv2.imread(str(OUT/'student-checking-source.png'));self.font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
 def cleaned(self,im,f):
  im,how=clean_frame(im,self.mask)
  if how:self.counts[how]+=1
  else:self.counts['declined'].append(f)
  return im
 def frame(self,f):
  if f>=CLOSE:
   k=f-CLOSE;q=np.clip((k-48)/149,0,1);z=1+.2*q*q*(3-2*q);im=self.b.close_img;h,w=im.shape[:2];ww=w/z;hh=ww*9/16
   return cv2.warpAffine(im,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  for i,r in enumerate(CUTAWAYS):
   if r['start']<=f<r['end']:
    if i in self.cutread:
     n=r['source_start']+min(r['source_end']-r['source_start']-1,int((f-r['start'])*(r['source_end']-r['source_start'])/(r['end']-r['start'])))
     return self.cleaned(self.cutread[i].at(n),f)
    # One restrained full-frame push; never replace retained animation with this still.
    h,w=self.photo.shape[:2];q=(f-r['start'])/(r['end']-r['start']-1);ww=min(w,h*16/9)/(1+.03*q);hh=ww*9/16
    return cv2.warpAffine(self.photo,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  for k,(s,e) in BOARD_SPANS.items():
   if s<=f<e:return self.renderers[k].at(f-s)[0]
  im=self.cleaned(self.base.at(f),f)
  if 6165<=f<CLOSE:
   # Video label overlay over cloned blank paper, preserving every animated object.
   x0,x1,y0,y1=330,960,596,640;patch=im[650:694,x0:x1].copy();a=np.ones((44,630,1),np.float32);r=np.linspace(0,1,6)
   a[:6]*=r[:,None,None];a[-6:]*=r[::-1,None,None];a[:,:6]*=r[None,:,None];a[:,-6:]*=r[None,::-1,None]
   im[y0:y1,x0:x1]=(patch*a+im[y0:y1,x0:x1]*(1-a)).astype('uint8')
   pil=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(pil);text='Similar answers can come from different processes.';box=d.textbbox((0,0),text,font=self.font);d.text(((1280-(box[2]-box[0]))/2,609),text,font=self.font,fill=(112,68,52));im=cv2.cvtColor(np.asarray(pil),cv2.COLOR_RGB2BGR)
  return im
 def release(self):
  self.base.c.release()
  for r in self.cutread.values():r.c.release()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');a=ap.parse_args();assert not DEST.exists(),'Version new builds; do not overwrite candidate'
 b,m=prepare();asm=Assembly(b);(OUT/'preview').mkdir(exist_ok=True)
 wanted=set([0,TOTAL-1,6246,6294,6444,6200,6240])
 for k,(s,e) in BOARD_SPANS.items():
  wanted|={s,e-1};cursor=s
  for beat in b.boards[k]['beats']:
   wanted|={cursor,cursor+beat['frames']//2,cursor+beat['frames']-1};cursor+=beat['frames']
 for r in CUTAWAYS:wanted|={r['start'],(r['start']+r['end'])//2,r['end']-1}
 # Validate all rendered camera/ring states before starting the encode.
 for k,r in asm.renderers.items():
  for f in range(len(r.cameras)):r.at(f)
 if a.prepare_only:
  for f in sorted(wanted):cv2.imwrite(str(OUT/'preview'/f'{f:05d}.jpg'),asm.frame(f))
  asm.release();return
 p=subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for f in range(TOTAL):
  im=asm.frame(f);p.stdin.write(im.tobytes())
  if f in wanted:cv2.imwrite(str(OUT/'preview'/f'{f:05d}.jpg'),im)
  if f%900==899:print('Rendered',f+1,'/',TOTAL,flush=True)
 p.stdin.close();assert p.wait()==0;asm.release();m['render_sha256']=sha(DEST);m['corner_mark']=asm.counts;m['protected_files_unchanged']={p:sha(p)==h for p,h in b.hashes.items()};assert all(m['protected_files_unchanged'].values())
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
