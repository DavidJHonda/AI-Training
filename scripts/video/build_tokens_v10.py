#!/usr/bin/env python3
"""Approved Tokens hybrid; retain the 989-frame v9 examples. Review only."""
from pathlib import Path
import argparse, json, subprocess, sys
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from editspec_build import Build, Reader, sha, readwav, writewav
from build_tokens_v9 import Renderer
from gemini_mark import clean_frame, glyph_mask

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/tokens-build-2026-09-29-v10'
DEST=ROOT/'Prompts/tokens-v10c.mp4'
SOURCES={k: ROOT/f'Prompts/tokens-{k}.mp4' for k in ['1','2','v9']}
HASHES=dict(zip(['1','2','v9'], ['b003c0f70c7bfd392f3f7024ee17e6ebcca815fa0b9ad7da1bcee6307ca931a1','186d4d6ba38a88ea44edc6632c69b8758fa0444cff77354547f5ac87f9cbde10','d1b7a9e0a5dabb90ec3bbb241518fc5727bab84be6f2bbd3327170b6812a1f16']))
SPF=1600
SPANS=[('1',0,1860,'Opening and definition'),('2',1903,1987,'Whole word or just part'),('1',1939,3359,'Vocabulary, reuse, training'),('1',3635,3992,'Send process; size aside removed'),('2',4080,4402,'Correct IDs and tokenization summary'),('1',4366,4761,'Cat comparison'),('2',4954,5070,'ID identifies; meaning comes later'),('v9',6198,7187,'Approved three examples'),('1',6475,7095,'Return to text and exact close')]

def timeline():
 rows=[];cursor=0
 for key,a,b,label in SPANS:
  rows.append(dict(source=key,source_start=a,source_end=b,start_frame=cursor,end_frame=cursor+b-a,label=label));cursor+=b-a
 return rows

ROWS=timeline()
def at(key,f):
 for r in ROWS:
  if r['source']==key and r['source_start']<=f<r['source_end']:
   return r['start_frame']+f-r['source_start']
 raise ValueError((key,f))
def sec(key,t):return at(key,round(t*30))
CLOSE=at('1',6951)
TOTAL=CLOSE+318

def prepare():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 assert all(sha(SOURCES[k])==v for k,v in HASHES.items())
 b=Build(ROOT,SOURCES['1'],OUT,DEST);b.make_close('tokens')
 assets={'chat':'tokens-using-ai-feels-like.jpg','blocks':'tokens-building-blocks.jpg','send':'tokens-how-tokenization-works.jpg','cat':'tokens-cat-token-id.jpg'}
 canvases={k:b.compose(ROOT/'course-assets/tokens'/v,k) for k,v in assets.items()}
 renderers={};specs={};boards=[]
 def board(key,asset,start,end,rings):
  p,w,h,ox,oy=canvases[asset];full=[w/2,h/2,float(w)]
  spec=dict(image=str(p),fps=30,out_w=1280,out_h=720,upscale=2,beats=[dict(label='complete board',frames=end-start,**{'from':full,'to':full})],rings=[])
  for onset,finish,rect,col in rings:
   spec['rings'].append(dict(start=onset-start,end=finish-start,rect=rect,color=col,pad=0,radius=18))
  renderers[key]=Renderer(spec);specs[key]=spec
  boards.append(dict(key=key,start_frame=start,end_frame=end,asset=assets[asset],density='compact / complete composition',canvas_offset=[ox,oy]))
  (OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n')
 end=sec('1',23.6)
 board('chat','chat',263,end,[(sec('1',10.42),sec('1',13.32),[780,326,714,92],'#4f2fc4'),(sec('1',13.32),end,[111,507,1209,194],'#1652f0')])
 end=at('1',2270)
 board('blocks','blocks',1787,end,[(sec('1',68.68),end,[697,189,1520,1224],'#6e51ff')])
 # The entire illustrated card remains in view; no isolated machine dive.
 start,end=sec('1',82.8),sec('1',85.7)
 board('reuse-banner','blocks',start,end,[(sec('1',83.8),end,[698,1453,1518,85],'#6e51ff')])
 start,end=at('1',3635),at('1',4366)
 onsets=[sec('1',122.62),sec('1',124.54),sec('1',128.78),sec('2',142.98)]
 # These columns share one white card; outlines span its full 164..778 height.
 rects=[[153,164,455,615],[643,164,460,615],[1133,164,460,615],[113,818,1520,88]]
 board('send','send',start,end,[(a,z,r,c) for a,z,r,c in zip(onsets,onsets[1:]+[end],rects,['#4f2fc4','#1652f0','#0e8f86','#6e51ff'])])
 start,end=at('1',4366),at('v9',6198)
 onsets=[sec('1',147.52),sec('1',151.66),sec('2',165.36)]
 board('cat','cat',start,end,[(a,z,r,c) for a,z,r,c in zip(onsets,onsets[1:]+[end],[[41,135,741,587],[817,135,741,587],[40,764,1520,88]],['#0e8f86','#4f2fc4','#6e51ff'])])
 for key,path in SOURCES.items():
  wav=OUT/f'source-{key}.wav'
  if not wav.exists():subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-i',str(path),'-vn','-ac','1','-ar','48000',str(wav)],check=True)
 audios={k:readwav(OUT/f'source-{k}.wav') for k in SOURCES}
 gains={'1':0.,'2':0.07,'v9':-4.81};parts=[]
 for i,r in enumerate(ROWS):
  part=audios[r['source']][r['source_start']*SPF:r['source_end']*SPF].copy()*10**(gains[r['source']]/20)
  if i:part[:240]*=np.linspace(0,1,240)
  part[-240:]*=np.linspace(1,0,240)
  parts.append(part)
 seed=audios['1'][round(237.0*48000):round(237.2*48000)].copy();seed-=seed.mean()
 tone=np.resize(np.r_[seed,seed[::-1]],(TOTAL-ROWS[-1]['end_frame'])*SPF);tone[:240]*=np.linspace(0,1,240)
 audio=np.concatenate(parts+[tone]);assert len(audio)==TOTAL*SPF
 writewav(OUT/'edited.wav',audio)
 states=[]
 for key,rd in renderers.items():
  ns={0,len(rd.cameras)-1}|{min(r[0]+15,len(rd.cameras)-1) for r in rd.rings}
  for n in sorted(ns):
   im,base,geo=rd.at(n);path=OUT/'preview'/f'{key}-{n:04d}.png';cv2.imwrite(str(path),im);states.append(dict(key=key,local_frame=n,path=str(path),rings=geo))
 manifest=dict(candidate=str(DEST),sources={k:dict(path=str(SOURCES[k]),sha256=HASHES[k]) for k in SOURCES},fps=30,frames=TOTAL,duration=TOTAL/30,timeline=ROWS,boards=boards,prepared_states=states,close=dict(start_frame=CLOSE,prehold=48,push=150,endpoint=1.2,settle=120),audio=dict(gain_db=gains,measured_lufs={'1':-19.84,'2':-19.91,'v9':-15.03},join_ramps_ms=5,added_interlesson_pauses=0,closing_room_tone_source=[237,237.2]),examples=dict(source='v9',source_frames=[6198,7187],frames=989,output_frames=[at('v9',6198),at('v9',7186)+1],scope='basketball, spaces/symbols/SP, URL eight-token count only'),visual_repairs=['Canonical course boards with fixed 4px outlines','Retain complete illustrated building-blocks card','Replace exaggerated dictionary heading only; preserve scene motion','Bring return diagram source frame 6540 forward to cover outgoing URL fade','Standard canonical close'],exceptions=['First-item ring inside two seconds of board arrival follows EDIT-SPEC rule 3','Send -> Cat -> approved examples continuous board run; preserve approved short examples and avoid filler'],protected={str(p):sha(p) for p in [ROOT/'course-assets/tokens/tokens.mp4',*sorted((ROOT/'course-assets/tokens').glob('*.jpg'))]},scope='Approved full hybrid production candidate; no publication',listening='Not directly auditioned; signal checks and ASR cannot certify joins')
 manifest['visual_repairs'].append('Correct early un/belie/vable ID-chip labels to 359/32898/24694 during their original fade, source frames 1698:1787')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 return b,renderers,boards,manifest

class HeaderRepair:
 def __init__(self):
  im=Image.new('RGBA',(1280,720));d=ImageDraw.Draw(im)
  d.rounded_rectangle((335,76,945,132),radius=18,fill=(247,244,231,255),outline=(183,75,77,255),width=2)
  font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',23)
  d.text((640,104),'Whole-word lookup cannot cover every input',font=font,anchor='mm',fill=(174,58,64,255))
  self.overlay=cv2.cvtColor(np.asarray(im),cv2.COLOR_RGBA2BGRA)
 def at(self,im,n):
  if not 1050<=n<1710:return im
  region=im[85:120,300:980].astype(int);blue,green,red=cv2.split(region)
  mask=(red-green>25)&(red-blue>25)&(red>130)
  if mask.sum()<500:return im
  # Replace the heading only, including its distorted entrance/exit lettering.
  out=im.copy();patch=im[140:201,305:976].copy();out[75:136,305:976]=patch
  a=self.overlay[:,:,3:4].astype(float)/255
  return np.rint(out*(1-a)+self.overlay[:,:,:3]*a).astype(np.uint8)

class EarlyIDs:
 """Replace only the three incidental ID-chip labels, preserving their fade."""
 def __init__(self):
  self.labels=[]
  font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16*4)
  for cx,label,color in [(406,'ID: 359',(245,245,245)),(640,'ID: 32898',(25,25,25)),(874,'ID: 24694',(245,245,245))]:
   mask=Image.new('L',(112*4,26*4));d=ImageDraw.Draw(mask);d.text((56*4,13*4),label,font=font,anchor='mm',fill=255)
   alpha=np.asarray(mask.resize((112,26),Image.Resampling.LANCZOS),dtype=float)/255
   self.labels.append((cx,alpha,np.array(color)))
 def at(self,im,n):
  if not 1698<=n<1787:return im
  out=im.copy()
  for cx,mask,col in self.labels:
   # Sample the chip's blank left inset, preserving its source opacity.
   x=cx-56;y=380;bg=np.median(im[383:403,x-7:x-3],axis=(0,1))
   opacity=float(np.clip((bg[2]-bg[0]-25)/115 if cx==640 else (bg[0]-bg[2])/98,0,1))
   if opacity<.015:continue
   a=(mask*opacity)[:,:,None]
   out[y:y+26,x:x+112]=np.rint(bg*(1-a)+col*a).astype(np.uint8)
  return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a review candidate'
 b,renderers,boards,m=prepare()
 repair=HeaderRepair();ids=EarlyIDs();r=Reader(SOURCES['1'])
 for n in [1110,1440,1530,1650,1710,1740,1770]:cv2.imwrite(str(OUT/'preview'/f'heading-{n}.jpg'),ids.at(repair.at(r.at(n),n),n))
 r.c.release()
 if args.prepare_only:print(json.dumps(dict(frames=TOTAL,duration=TOTAL/30,examples=m['examples'],boards=boards),indent=2));return
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 readers={k:Reader(v) for k,v in SOURCES.items() if k!='2'};mask=glyph_mask();counts={'clone':0,'inpaint':0,'declined':[]}
 for f in range(TOTAL):
  board=next((v for v in boards if v['start_frame']<=f<v['end_frame']),None)
  if f>=CLOSE:
   q=np.clip((f-CLOSE-48)/149,0,1);z=1+.2*q*q*(3-2*q);h,w=b.close_img.shape[:2];ww=w/z;hh=ww*9/16
   im=cv2.warpAffine(b.close_img,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  elif board:im=renderers[board['key']].at(f-board['start_frame'])[0]
  else:
   row=next(v for v in ROWS if v['start_frame']<=f<v['end_frame']);key=row['source'];sf=row['source_start']+f-row['start_frame']
   assert key!='2','Donor narration must remain beneath canonical board'
   if key=='1' and 6475<=sf<6540:sf=6540
   im=readers[key].at(sf)
   if key=='1':
    im=ids.at(repair.at(im,sf),sf);im,how=clean_frame(im,mask)
    if how:counts[how]+=1
    else:counts['declined'].append(f)
  p.stdin.write(im.tobytes())
  if f%600==599:print('Rendered',f+1,'/',TOTAL,flush=True)
 p.stdin.close();assert p.wait()==0
 for r in readers.values():r.c.release()
 assert all(sha(Path(k))==v for k,v in m['protected'].items())
 m['corner_cleanup']=counts;m['render_sha256']=sha(DEST)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
