#!/usr/bin/env python3
"""Learn with AI narrow pacing repair; owner review 2026-11-06.
Separate audio assembly from visual cuts. Sequential source decodes only.
"""
from pathlib import Path
import argparse, json, subprocess
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from editspec_build import Build, Reader, sha, readwav, writewav, fr, SPF, SR, FPS
from ken_burns_path import window, smoothstep, draw_ring, hex_bgr
from gemini_mark import clean_frame, glyph_mask
from make_close_board import compose_canonical_for_video, close_board_asset
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/learn-with-ai-build-2026-11-06-v15'
DEST=ROOT/'Prompts/learn-with-ai-v15.mp4'
FF=imageio_ffmpeg.get_ffmpeg_exe()
SRC={'base':ROOT/'Prompts/learn-with-ai-3.mp4','donor':ROOT/'Prompts/learn-reroll-2.mp4'}
HASH={'base':'c9ca6b3f9c4a53239066e4fe942d2a5f11811c5f967ec282c1410336744338ac','donor':'6cd66cf07361f6b6c2408117f1b0a00a9e7d028785b36d7b9b8a01aef67dac85'}
ASSETS={k:ROOT/f'course-assets/learn-with-ai/learn-with-ai-{k}.jpg' for k in ['study-toolkit','how-it-works','four-moves','close']}
AUDIO=[('base',0,105.6,'Base through teacher check'),('base',120.2,145.0,'Study tool and upload types; repeated comparison removed'),('donor',25.8,35.15,'Complete study outputs'),('base',154.9,157.9,'Exact materials-to-tools takeaway'),('base',168.75,216.0,'Four moves; guarantee removed'),('base',227.1,268.7,'Learning coach and current close; memory guarantee removed')]
FONT='/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD='/System/Library/Fonts/Supplemental/Arial Bold.ttf'

def font(n,bold=False): return ImageFont.truetype(BOLD if bold else FONT,n)
def speech_level(a):
 n=len(a)//960;r=np.sqrt(np.mean((a[:n*960].reshape(n,960)/32768)**2,axis=1));r=r[r>.015]
 return float(20*np.log10(np.median(r)))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview-only',action='store_true');args=ap.parse_args()
 cv2.setNumThreads(2);OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 for k,p in SRC.items():assert sha(p)==HASH[k],k
 protected={str(p):sha(p) for p in [*SRC.values(),*ASSETS.values(),ROOT/'lessons/learn-with-ai.md',ROOT/'Prompts/learn-with-ai-v14.mp4']}
 audio={}
 for k,p in SRC.items():
  wav=OUT/f'{k}.wav'
  if not wav.exists():subprocess.run([FF,'-v','error','-y','-i',str(p),'-vn','-ar',str(SR),'-ac','1','-c:a','pcm_s16le',str(wav)],check=True)
  audio[k]=readwav(wav)
 # Compare adjacent narration, not the entire files' varying silence density.
 base_level=speech_level(audio['base'][fr(139.26)*SPF:fr(154.42)*SPF]); donor_level=speech_level(audio['donor'][fr(25.8)*SPF:fr(35.15)*SPF])
 gain=base_level-donor_level
 rows=[];parts=[];cursor=0
 for k,s,e,label in AUDIO:
  a,b=fr(s),fr(e);part=audio[k][a*SPF:b*SPF].copy();assert len(part)==(b-a)*SPF
  if k=='donor':part*=10**(gain/20)
  fade=384;ramp=np.linspace(0,1,fade)
  if a:part[:fade]*=ramp
  if b<len(audio[k])//SPF:part[-fade:]*=ramp[::-1]
  rows.append(dict(source=k,source_start=a,source_end=b,start_frame=cursor,end_frame=cursor+b-a,label=label))
  parts.append(part);cursor+=b-a
 total=cursor;assembled=np.concatenate(parts);assert abs(assembled).max()<32767
 writewav(OUT/'edited.wav',assembled)
 def mapped(k,t):
  f=fr(t)
  for r in rows:
   if r['source']==k and r['source_start']<=f<r['source_end']:return r['start_frame']+f-r['source_start']
  raise ValueError((k,t))
 helper=Build(ROOT,SRC['base'],OUT,DEST)
 boards={}
 def prep(key,rects,states,density):
  path,w,h,ox,oy=helper.compose(ASSETS[key],key);im=cv2.imread(str(path));full=np.array([w/2,h/2,w],float)
  translated=[[x+ox,y+oy,rw,rh] for x,y,rw,rh in rects]
  dw=max(helper.fit_w(r[2],r[3]) for r in rects)
  cams=[np.array([x+rw/2,y+rh/2,dw]) for x,y,rw,rh in translated]
  B={'image':im,'asset':str(ASSETS[key]),'full':full,'offset':[ox,oy],'rects':translated,'cams':cams,'density':density,'states':[]}
  for time,ci,rect,color,label in states:
   f=mapped(*time)
   if rect is None:rr=None
   else:rr=[rect[0]+ox,rect[1]+oy,rect[2],rect[3]]
   B['states'].append(dict(at=f,card=ci,rect=rr,color=color,label=label))
  boards[key]=B
 # Card edges measured on the literal current JPGs, excluding shadows.
 c1=[[40,123,748,830],[817,123,746,830]]
 prep('study-toolkit',c1,[
  (('base',67.48),0,c1[0],'#1652f0','Your Study Tool'),
  (('base',70.64),0,[56,600,716,142],'#1652f0','Uses your materials'),
  (('base',78.70),0,[56,751,716,183],'#1652f0','Best use'),
  (('base',83.60),1,c1[1],'#4f2fc4','Your Learning Coach'),
  (('base',90.72),1,[833,607,715,140],'#4f2fc4','Guided questions and hints'),
  (('base',98.62),None,None,'#6e51ff','Return to full view'),
  (('base',101.84),None,[39,989,1523,95],'#6e51ff','Check class materials and teacher')], 'dense')
 c2=[[40,127,745,548],[817,127,744,548]]
 prep('how-it-works',c2,[
  (('base',136.80),None,c2[0],'#1652f0','You Upload'),
  (('donor',26.43),None,c2[1],'#0e8f86','You Get — all output types'),
  (('base',155.00),None,[39,714,1523,90],'#6e51ff','Materials-to-tools takeaway')], 'compact')
 c3=[[40,127,744,589],[817,127,744,589],[40,750,744,589],[817,750,744,589]]
 prep('four-moves',c3,[
  (('base',175.08),0,c3[0],'#4f2fc4','One Subject per Notebook'),
  (('base',184.26),1,c3[1],'#1652f0','Give It the Full Picture'),
  (('base',192.60),2,c3[2],'#0e8f86','Quiz Yourself Blind'),
  (('base',206.32),3,c3[3],'#a9760c','Trace It Back')], 'dense')
 def render_board(key,f):
  B=boards[key];cam=B['full'].copy();active=None
  # Camera moves begin with the spoken target; section rings share the card camera.
  prev_ci=None;movement=[]
  for s in B['states']:
   if s['card']!=prev_ci:
    target=B['full'] if s['card'] is None else B['cams'][s['card']]
    movement.append((s['at'],target));prev_ci=s['card']
  last=B['full']
  for at,target in movement:
   if f<at:break
   q=smoothstep(float(np.clip((f-at)/23,0,1)));cam=last+(target-last)*q;last=target
  for s in B['states']:
   if f>=s['at']:active=s
  im=B['image'];x,y,ww,hh=window(*cam,16/9,im.shape[1],im.shape[0]);scale=1280/ww
  result=cv2.warpAffine(im,np.float32([[ww/1280,0,x],[0,hh/720,y]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  if active and active['rect']:
   rx,ry,rw,rh=active['rect'];draw_ring(result,(rx-x)*scale,(ry-y)*scale,(rx+rw-x)*scale,(ry+rh-y)*scale,hex_bgr(active['color']),16*scale,thickness=4)
  return result
 closefile=OUT/'close.png';compose_canonical_for_video(close_board_asset('studying'),closefile,'#ffffff');close=cv2.imread(str(closefile));close_start=mapped('base',256.533333)
 def render_close(f):
  q=smoothstep(float(np.clip((f-close_start-48)/149,0,1)));z=1+.2*q;h,w=close.shape[:2];ww,hh=w/z,h/z
  return cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
 # A simple explanatory citation diagram, not a new course board.
 def citation(f):
  q=float(np.clip((f-mapped('base',211))/90,0,1));im=Image.new('RGB',(1280,720),'#f8f7fc');d=ImageDraw.Draw(im)
  d.text((74,68),'Follow the citation',fill='#252a33',font=font(42,True))
  d.rounded_rectangle((72,198,560,560),radius=24,fill='white',outline='#ddd8ed',width=2)
  d.rounded_rectangle((720,170,1208,592),radius=24,fill='white',outline='#ddd8ed',width=2)
  d.text((108,236),'AI answer',fill='#4f2fc4',font=font(30,True));d.text((756,208),'Original class material',fill='#1652f0',font=font(28,True))
  for yy,w in [(314,350),(349,306),(384,270)]:d.rounded_rectangle((108,yy,108+w,yy+10),radius=5,fill='#bbb7c9')
  d.rounded_rectangle((108,438,182,493),radius=12,fill='#ece7ff',outline='#6e51ff',width=3);d.text((126,447),'1',fill='#4f2fc4',font=font(30,True))
  for yy,w in [(289,370),(330,322),(371,370),(412,306),(453,356),(494,300)]:d.rounded_rectangle((756,yy,756+w,yy+10),radius=5,fill='#bbb7c9')
  if q>0.2:
   d.rounded_rectangle((745,355,1173,397),radius=8,fill='#fff0b8',outline='#a9760c',width=2);d.rounded_rectangle((756,371,1126,381),radius=5,fill='#77717e')
  d.line((195,466,634,466,634,376,732,376),fill='#6e51ff',width=5);d.polygon([(733,376),(717,365),(717,387)],fill='#6e51ff')
  x=195+q*420;y=466
  if q>.75:x=634;y=466-(q-.75)*360
  d.ellipse((x-8,y-8,x+8,y+8),fill='#4f2fc4')
  d.text((74,641),'Click the citation. Check the original.',fill='#4c465a',font=font(27))
  return cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
 # Visual treatment in source frame coordinates. Each reused segment has its own clock.
 def shot(r,sf,f):
  if f>=close_start:return ('close',None,None)
  if r['source']=='donor':return ('how-it-works',None,None)
  t=sf/FPS
  if 60.2<=t<106.2:
   if 79.5<=t<82.6:return ('source',fr(113)+(sf-fr(79.5)),'materials-cutaway')
   if 95.8<=t<100.8:return ('source',fr(41.1)+(sf-fr(95.8)),'coach-cutaway')
   return ('study-toolkit',None,None)
  if 133.3<=t<157.9:
   return ('how-it-works',None,None)
  if fr(168.75)<=sf<fr(216):
   if 211<=t<216:return ('citation',None,None)
   return ('four-moves',None,None)
  if 37.9<=t<40.866667:return ('source',fr(34.0)+(sf-fr(37.9)),'late-night-illustration')
  if 3617<=sf<3857:
   return ('source',fr(113.0)+min(round((sf-fr(120.566667))*.92),fr(7.4)),'replace-photo-materials')
  if 227.1<=t<233.5:return ('source',fr(221)+(sf-fr(227.1)),'confused-student-coach-bridge')
  if 7490<=sf<7696:return ('source',fr(41.0)+(sf-fr(249.666667)),'student-thinking-replaces-photo')
  return ('source',sf,'original')
 # Correct the one legible nonsense label while retaining the source illustration/motion.
 patch_refs={}
 for key,sec,box,lines,sz in [('opening',0,(1038,340,1145,410),['MORE','WORK'],23)]:
  ref=cv2.imread(str(OUT/'source-frames'/f'learn-with-ai-3-{sec:06.2f}.jpg'));assert ref is not None
  overlay=np.zeros((720,1280,4),np.uint8);pi=Image.fromarray(overlay,'RGBA');d=ImageDraw.Draw(pi)
  color=(246,240,219,255) if key=='opening' else (255,255,255,255)
  d.rounded_rectangle(box,radius=5,fill=color)
  for n,line in enumerate(lines):
   ff=font(sz,False);bb=d.textbbox((0,0),line,font=ff);xx=(box[0]+box[2]-(bb[2]-bb[0]))/2
   d.text((xx,box[1]+4+n*(sz+3)),line,font=ff,fill=(44,45,49,255))
  rgba=np.array(pi);orb=cv2.ORB_create(nfeatures=1500);kp,ds=orb.detectAndCompute(cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY),None)
  patch_refs[key]=(orb,kp,ds,rgba)
 def patch(im,key):
  orb,kp,ds,rgba=patch_refs[key];ks,dd=orb.detectAndCompute(cv2.cvtColor(im,cv2.COLOR_BGR2GRAY),None)
  pairs=cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(ds,dd,k=2);good=[a for pair in pairs if len(pair)==2 for a,b in [pair] if a.distance<.72*b.distance]
  assert len(good)>=50,(key,len(good))
  H,status=cv2.findHomography(np.float32([kp[m.queryIdx].pt for m in good]),np.float32([ks[m.trainIdx].pt for m in good]),cv2.RANSAC,3.0)
  assert H is not None
  p=cv2.warpPerspective(rgba,H,(1280,720));alpha=p[:,:,3:]/255;rgb=p[:,:,:3][:,:,::-1]
  return (im*(1-alpha)+rgb*alpha).astype(np.uint8)
 def row_for(f):return next(r for r in rows if r['start_frame']<=f<r['end_frame'])
 spans=[]
 for f in range(total):
  r=row_for(f);sf=r['source_start']+f-r['start_frame'];mode,vf,reason=shot(r,sf,f)
  # Track actual discontinuities, including reused picture changes across an audio splice.
  new=not spans or (mode,reason)!=(spans[-1]['visual'],spans[-1]['reason']) or f==r['start_frame']
  if new:spans.append(dict(start_frame=f,end_frame=f+1,visual=mode,video_start=vf,reason=reason))
  else:spans[-1]['end_frame']=f+1
 serial={}
 for k,B in boards.items():
  serial[k]={x:v for x,v in B.items() if x not in ['image','full','cams']};serial[k]['full']=B['full'].tolist();serial[k]['cams']=[x.tolist() for x in B['cams']]
 manifest=dict(output=str(DEST),fps=30,total_frames=total,duration=total/30,audio_timeline=rows,visual_timeline=spans,boards=serial,protected=protected,donor_gain_db=gain,reference_speech_dbfs=base_level,donor_speech_dbfs=donor_level,close=dict(start_frame=close_start,prehold=48,push=150,zoom=1.2,settle=total-close_start-198),additional_pauses=[],listening='Not directly auditioned; user-authorized build, fresh transcript, and signal checks do not certify voice/cadence continuity.',narration_cuts_seconds=[[105.6,120.2],[145,154.9],[157.9,168.75],[216,227.1]])
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 preview=OUT/'preview'
 for key,B in boards.items():
  starts=[s['start_frame'] for s in spans if s['visual']==key];sample=[min(starts)]+[s['at']+35 for s in B['states']]
  for n,f in enumerate(sample):cv2.imwrite(str(preview/f'{key}-{n}.jpg'),render_board(key,f))
 cv2.imwrite(str(preview/'citation.jpg'),citation(mapped('base',213)))
 cv2.imwrite(str(preview/'close-start.jpg'),render_close(close_start));cv2.imwrite(str(preview/'close-end.jpg'),render_close(total-1))
 for key,sec in [('opening',0)]:
  im=cv2.imread(str(OUT/'source-frames'/f'learn-with-ai-3-{sec:06.2f}.jpg'));cv2.imwrite(str(preview/f'patch-{key}.jpg'),patch(im,key))
 print(f'Prepared {total} frames / {total/30:.3f}s; donor gain {gain:+.3f} dB',flush=True)
 if args.preview_only:return
 assert not DEST.exists(),'Use a fresh candidate filename'
 reader=Reader(SRC['base']);mask=glyph_mask();counts={};log=open(OUT/'encode.log','w');render_target=OUT/'rendering.mp4'
 proc=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(render_target)],stdin=subprocess.PIPE,stderr=log)
 try:
  for f in range(total):
   r=row_for(f);sf=r['source_start']+f-r['start_frame'];mode,vf,reason=shot(r,sf,f)
   if mode in boards:im=render_board(mode,f)
   elif mode=='close':im=render_close(f)
   elif mode=='citation':im=citation(f)
   else:
    if vf<reader.n:reader.c.release();reader=Reader(SRC['base'])
    im=reader.at(vf)
    if vf<249:im=patch(im,'opening')
    im,method=clean_frame(im,mask);counts[str(method)]=counts.get(str(method),0)+1
   proc.stdin.write(im.tobytes())
   if f%900==0:print(f'Rendered {f}/{total}',flush=True)
  proc.stdin.close();assert proc.wait()==0
 except BaseException:
  proc.kill();raise
 finally:reader.c.release();log.close()
 render_target.replace(DEST)
 manifest['render_sha256']=sha(DEST);manifest['corner_cleanup']=counts;manifest['protected_unchanged']={p:sha(p)==h for p,h in protected.items()};assert all(manifest['protected_unchanged'].values())
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Built',DEST,flush=True)
if __name__=='__main__':main()
