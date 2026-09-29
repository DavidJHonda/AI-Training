#!/usr/bin/env python3
"""Approved Mind Trap repairs, review candidate only. No canonical writes.
Use the stable v3 finished source (raw rolls no longer available), current JPGs,
and the verified v4 audio. One final H.264 encode; one AAC encode for the cut.
"""
from pathlib import Path
import argparse,functools,hashlib,json,subprocess,wave
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
from editspec_build import Build,sha,readwav,writewav
from build_embeddings_v7 import Renderer
cv2.setNumThreads(2)
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/mind-trap-repair-2026-09-29-v5'
DEST=ROOT/'Prompts/mind-trap-v5.mp4'
SRC=ROOT/'video-audit/mind-trap-illustration-sync-2026-09-21/baseline-live-2026-09-21-v3.mp4'
LIVE=ROOT/'course-assets/mind-trap/mind-trap.mp4'
SHA='63c12abcb0235a454894178e457b4e9c5624307f00deebc87e61b3c9bdee3c60'
LIVE_SHA='0b7f49264e5bfbaeb6a3904080c261da08bdc07e711966490f516e7a5c5e3671'
CUT_A,CUT_B=4608,4857 # 153.600–161.900; both inside measured quiet gaps
REMOVED=CUT_B-CUT_A;TOTAL=7213-REMOVED;SPF=1600
FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
ASSETS=ROOT/'course-assets/mind-trap'

def of(f):return f if f<CUT_A else f-REMOVED

def reader(path):
 c=cv2.VideoCapture(str(path),cv2.CAP_FFMPEG,[cv2.CAP_PROP_N_THREADS,2]);assert c.isOpened();return c

def source_frames(wanted):
 c=reader(SRC);out={};i=0
 while i<=max(wanted):
  ok,im=c.read();assert ok
  if i in wanted:out[i]=im.copy()
  i+=1
 c.release();return out

def ease(t):
 t=float(np.clip(t,0,1));return t*t*(3-2*t)

def specs():
 b=Build(ROOT,SRC,OUT,DEST)
 result={}
 for key,asset,old in [('compare','comparison',ROOT/'video-audit/mind-trap-illustration-sync-2026-09-21/leg-compare.json'),('define','comparison',ROOT/'video-audit/mind-trap-illustration-sync-2026-09-21/leg-define.json'),('eliza','eliza',ROOT/'video-audit/mind-trap-comparison-2026-09-21/build-v3/leg-eliza.json')]:
  canvas,cw,ch,ox,oy=b.compose(ASSETS/f'mind-trap-{asset}.jpg',key)
  s=json.loads(old.read_text());s['image']=str(canvas);s['upscale']=2
  if key=='compare':
   full=[1368.,770.,2736.];pair=[1368.,909.,2150.]
   s['beats']=[dict(label='full-board-and-question',frames=250,**{'from':full},to=full),dict(label='enlarge-complete-card-pair',frames=24,to=pair),dict(label='complete-card-pair',frames=952,to=pair)]
  result[key]=s;(OUT/f'leg-{key}.json').write_text(json.dumps(s,indent=2))
 return result

class Label:
 def __init__(self,clean,final):
  self.box=(450,589,835,636);x,y,x1,y1=self.box
  self.clean=clean[y:y1,x:x1].copy();self.final=final[y:y1,x:x1].copy()
  self.delta=cv2.cvtColor(self.clean,cv2.COLOR_BGR2GRAY).astype(float)-cv2.cvtColor(self.final,cv2.COLOR_BGR2GRAY)
  self.mask=self.delta>60
  assert self.mask.sum()>500
  im=Image.new('RGBA',((x1-x)*3,(y1-y)*3));d=ImageDraw.Draw(im)
  font=ImageFont.truetype(str(FONT),24*3);font.set_variation_by_axes([700])
  d.text(((x1-x)*1.5,(y1-y)*1.5),'Could fit almost anyone.',font=font,anchor='mm',fill=(75,80,70,255))
  self.tile=np.array(im.resize((x1-x,y1-y),Image.Resampling.LANCZOS))
 def apply(self,im):
  x,y,x1,y1=self.box;roi=im[y:y1,x:x1]
  delta=cv2.cvtColor(self.clean,cv2.COLOR_BGR2GRAY).astype(float)-cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
  opacity=float(np.clip(np.median(delta[self.mask]/self.delta[self.mask]),0,1))
  if opacity>.005:
   im=im.copy();alpha=self.tile[:,:,3:4]/255*opacity
   im[y:y1,x:x1]=np.rint(self.clean*(1-alpha)+self.tile[:,:,:3][:,:,::-1]*alpha).astype(np.uint8)
  return im,opacity

def photo(ref,n):
 # Same existing illustration, revised camera only: full view -> paper emphasis.
 # Right edge stays at 1280, so the complete reply never leaves the shot.
 t=ease((n-2450)/(3160-2450-1));width=1280-160*t;x=1280-width;y=0+60*t;scale=1280/width
 matrix=np.array([[scale,0,-x*scale],[0,scale,-y*scale]],np.float32)
 return cv2.warpAffine(ref,matrix,(1280,720),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)

def prepare():
 OUT.mkdir(exist_ok=True);(OUT/'previews').mkdir(exist_ok=True)
 assert sha(SRC)==SHA and sha(LIVE)==LIVE_SHA
 protected={str(p):sha(p) for p in [SRC,LIVE,ROOT/'lessons/mind-trap.md',*ASSETS.glob('*.jpg')]}
 s=specs();rs={k:Renderer(v) for k,v in s.items()}
 refs=source_frames({2220,2280,2450});lab=Label(refs[2220],refs[2280])
 # Decode and cut exact samples; 5ms ramps join at the matching quiet floor.
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 if not (OUT/'source.wav').exists():subprocess.run([ff,'-v','error','-i',str(LIVE),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'source.wav')],check=True)
 a=readwav(OUT/'source.wav')[:7213*SPF];assert len(a)==7213*SPF
 left=a[:CUT_A*SPF].copy();right=a[CUT_B*SPF:].copy();fade=240
 # Quiet floor is ~-68 dBFS. A shared 10ms bed crosses the seam without
 # affecting adjacent words or changing the planned sample count.
 bed=a[round(153.55*48000):round(153.56*48000)].copy()
 ramp=np.linspace(0,1,fade)
 left[-fade:]=left[-fade:]*(1-ramp)+bed[:fade]*ramp
 right[:fade]=bed[fade:]*(1-ramp)+right[:fade]*ramp
 edited=np.concatenate([left,right]);assert len(edited)==TOTAL*SPF;writewav(OUT/'edited.wav',edited)
 gaps={}
 for name,lo,hi in [('left',153.45,153.6),('right',161.9,162.0)]:
  v=a[round(lo*48000):round(hi*48000)]/32768;gaps[name]=dict(seconds=[lo,hi],rms_dbfs=float(20*np.log10(np.sqrt(np.mean(v*v))+1e-12)))
 boundaries=[804,1054,1078,2030,2220,2296,2450,3160,3370,CUT_A,of(5008),of(5336),of(5348),of(6973)]
 m=dict(candidate=str(DEST),source=str(SRC),source_sha256=SHA,audio_source=str(LIVE),audio_source_sha256=LIVE_SHA,
   source_limitation='Raw rolls absent; stable finished v3 is the earliest surviving finished source. All current boards rebuilt directly from canonical JPGs; v4 decoded audio retained except approved cut.',
   approval='User: Agree with all. Build it please. Implements all review refinements; review candidate only.',
   total_frames=TOTAL,fps=30,duration=TOTAL/30,source_cut_frames=[CUT_A,CUT_B],source_cut_seconds=[CUT_A/30,CUT_B/30],removed_seconds=REMOVED/30,
   removed_words='This is a direct psychological reaction to language stimuli. It is a cognitive habit of filling in the blanks when a back-and-forth conversation occurs.',
   audio_join_output_seconds=CUT_A/30,measured_cut_flanks=gaps,planned_resulting_speech_gap_seconds=.54,audio_splice_ramps_ms=5,added_pauses=[],
   comparison=dict(full_open_frames=[804,1054],dive_frames=[1054,1078],complete_card_pair_frames=[1078,2030],scale_gain=2736/2150,complete_card_bounds_canvas=[[609,329,1351,1441],[1385,329,2127,1441]]),
   label=dict(source_scene_frames=[2030,2296],patch_frames=[2220,2296],wording='Could fit almost anyone.',preserve_original_opacity=True),
   eliza_camera=dict(frames=[2450,3160],reference_source_frame=2450,description='Existing illustration with continuous restrained pan/push to paper; complete exchange retained. Replaces only the baked camera path.'),
   board_specs=s,ring_width=4,boundaries=sorted(set(boundaries)),protected=protected,verification_limit='Audio not perceptually auditioned by agent; clips supplied for human listening.')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));return rs,refs,lab,m

def changed(im,n,rs,ref,lab):
 meta={}
 if 804<=n<2030:im,_,geo=rs['compare'].at(n-804);meta['rings']=geo
 elif 2296<=n<2450:im,_,_=rs['define'].at(n-2296)
 elif 2450<=n<3160:im=photo(ref,n)
 elif 3370<=n<5008:im,_,geo=rs['eliza'].at(n-3370);meta['rings']=geo
 elif 2220<=n<2296:im,meta['label_opacity']=lab.apply(im)
 return im,meta

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite review candidates'
 rs,refs,lab,m=prepare()
 wanted={804,930,950,1054,1066,1078,1110,1180,1250,1410,1540,1700,1800,1930,2029,2220,2235,2250,2265,2280,2295,2296,2449,2450,2600,2700,2820,2960,3159,3160,3370,3800,4350,4607,4857,4970,5007,5008,6973,7212}
 c=reader(SRC);proc=None;log=[];out=0
 if not args.preview:
  proc=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','4','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-video_track_timescale','15360',str(DEST)],stdin=subprocess.PIPE)
 for n in range(7213):
  ok,im=c.read();assert ok,n
  if CUT_A<=n<CUT_B:continue
  if not args.preview or n in wanted:
   im,meta=changed(im,n,rs,refs[2450],lab)
   if n in wanted:
    cv2.imwrite(str(OUT/'previews'/f'v5-{out:05d}-source-{n:05d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,95]);log.append(dict(source_frame=n,output_frame=out,**meta))
   if proc:proc.stdin.write(im.tobytes())
  out+=1
  if proc and out%1000==0:print('Rendered',out,'/',TOTAL,flush=True)
 c.release();assert out==TOTAL
 if proc:
  proc.stdin.close();assert proc.wait()==0;m['candidate_sha256']=sha(DEST)
 assert all(sha(Path(p))==h for p,h in m['protected'].items())
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));(OUT/'preview-states.json').write_text(json.dumps(log,indent=2))
 print('Preview ready' if args.preview else str(DEST),flush=True)
if __name__=='__main__':main()
