#!/usr/bin/env python3
"""Approved evaluation improvements; pristine-source assembly, candidate only."""
from pathlib import Path
import argparse,copy,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
import build_vector_space_v8 as base
from build_embeddings_v7 import Renderer
from editspec_build import Build,Reader,sha,readwav,writewav
ROOT=base.ROOT
OUT=ROOT/'video-audit/vector-space-build-2026-09-29-v10'
OLD=ROOT/'video-audit/vector-space-build-2026-09-28-v9'
DEST=ROOT/'Prompts/vector-space-v10.mp4'
LIVE=ROOT/'course-assets/vector-space/vector-space.mp4'
CUT=(4397,4515);DONOR=(5311,5553);DELTA=(DONOR[1]-DONOR[0])-(CUT[1]-CUT[0]);TOTAL=6154+DELTA
BRIDGE=(2921,3187)

def bridge(t):
 im=Image.new('RGB',(1280,720),'#f7f5ee');d=ImageDraw.Draw(im)
 def tx(x,y,s,size=30,col='#253140',bold=False):base.text(d,(x,y),s,size,col,bold,'mm')
 tx(640,65,'Numbers describe a position',42,bold=True)
 # A coordinated comparison, not a new course board.
 tx(260,161,'DALLAS',28,base.COL['red'],True)
 tx(260,212,'2 coordinates',30,bold=True)
 for j,(val,label) in enumerate([('33° N','Latitude'),('97° W','Longitude')]):
  x=88+j*190;base.tile(d,(x,275,x+160,375),val,base.COL['red'],size=35);tx(x+80,412,label,24)
 d.line([(533,250),(533,445)],fill='#d6d0c5',width=2)
 tx(900,161,'COKE',28,base.COL['blue'],True)
 tx(900,212,'7 ratings',30,bold=True)
 labels=['Sweet','Bitter','Fizz','Heat','Caffeine','Dark','Citrus'];values=['9','1','10','2','3','8','1']
 colors=['#c41f28','#0e8f86','#1652f0','#a9760c','#4f2fc4','#253140','#0f7a4a']
 for j,(v,label,col) in enumerate(zip(values,labels,colors)):
  x=604+j*87;base.tile(d,(x,290,x+73,365),v,col,size=32);tx(x+36,408,label,18,col,True)
 if t>=3.4:
  tx(260,525,'A position in 2 dimensions',27,base.COL['purple'],True)
  tx(900,525,'A position in 7 dimensions',27,base.COL['purple'],True)
 if t>=6.2:tx(640,632,'A row of numbers is a vector.',31,bold=True)
 return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)

def setup():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 old=json.loads((OLD/'edit-manifest.json').read_text());assert sha(LIVE)==old['render_sha256']
 for p,h in base.EXPECTED.items():
  if p!=base.LIVE:assert sha(p)==h
 protected={str(p):sha(p) for p in [LIVE,ROOT/'Prompts/vector-space-v9.mp4',ROOT/'lessons/vector-space.md',base.R1,base.R2,base.R3,*base.ASSETS.values(),base.D/'vector-space-close.jpg']}
 # Rebuild the approved composite from original rolls, then replace one whole beat.
 base.OUT=OUT;base.audio_build(old['audio_timeline'])
 a=readwav(OUT/'edited.wav');r1=readwav(OUT/'roll1.wav')
 donor=r1[DONOR[0]*1600:DONOR[1]*1600].copy()*10**(old['audio']['donor_gain_db']['r1']/20)
 parts=[a[:CUT[0]*1600].copy(),donor,a[CUT[1]*1600:].copy()]
 edge=[]
 for i,p in enumerate(parts):
  edge.append({'part':i,'start_20ms_rms':float(np.sqrt(np.mean(p[:960]**2))),'end_20ms_rms':float(np.sqrt(np.mean(p[-960:]**2)))})
  if i:p[:192]*=np.linspace(0,1,192)
  if i<2:p[-192:]*=np.linspace(1,0,192)
 edited=np.concatenate(parts);assert len(edited)==TOTAL*1600;writewav(OUT/'edited.wav',edited)
 b=Build(ROOT,base.R3,OUT,DEST);rs={};specs={}
 for k,meta in old['boards'].items():
  b.tall_margin=k not in ('nbhd','drink');canvas,cw,ch,ox,oy=b.compose(base.ASSETS[k],k);assert [ox,oy]==meta['canvas_offset']
  sp=json.loads((OLD/f'leg-{k}.json').read_text());sp['image']=str(canvas);sp['upscale']=2
  if k=='ctx':
   # Whole 1600x1150 asset fits: width 2112 implies 1188 vertical pixels.
   for beat in sp['beats']:beat['from']=beat['to']=[1104,621,2112]
  specs[k]=sp;rs[k]=Renderer(sp);(OUT/f'leg-{k}.json').write_text(json.dumps(sp,indent=2))
  for f in sorted({0,len(rs[k].cameras)-1}|{r[0]+3 for r in rs[k].rings}):cv2.imwrite(str(OUT/'preview'/f'{k}-{f:04d}.jpg'),rs[k].at(f)[0])
 b.make_close('vectorspace')
 for t in [0,4,7]:cv2.imwrite(str(OUT/'preview'/f'bridge-{t}.jpg'),bridge(t))
 timeline=[]
 for s in old['timeline']:
  q=copy.deepcopy(s)
  if q['start_frame']>=CUT[1]:q['start_frame']+=DELTA
  if q['end_frame']>=CUT[1]:q['end_frame']+=DELTA
  if q['visual']=='taste':
   q['end_frame']=BRIDGE[0];timeline.append(q);timeline.append(dict(start_frame=BRIDGE[0],end_frame=BRIDGE[1],visual='bridge',label='Two coordinates to seven ratings'))
  else:timeline.append(q)
 boundaries={x['frame']+(DELTA if x['frame']>=CUT[1] else 0):x['label'] for x in old['boundaries'] if not CUT[0]<=x['frame']<CUT[1]}
 boundaries[BRIDGE[0]]='Coordinates to seven dimensions graphic'
 boundaries[CUT[0]]='Complete Roll 1 scaling-concept sentence starts'
 boundaries[CUT[0]+DONOR[1]-DONOR[0]]='Return to training explanation'
 donors={k:OLD/f'donor-{k}.mkv' for k in ['semantic','gap','cat']}
 protected.update({str(p):sha(p) for p in donors.values()})
 m=dict(output=str(DEST),source_revision=str(ROOT/'Prompts/vector-space-v9.mp4'),source_revision_sha256=old['render_sha256'],fps=30,total_frames=TOTAL,duration=TOTAL/30,timeline=timeline,base_audio_timeline=old['audio_timeline'],audio_graft=dict(source=str(base.R1),source_frames=DONOR,replaced_v9_frames=CUT,output_frames=[CUT[0],CUT[0]+DONOR[1]-DONOR[0]],gain_db=old['audio']['donor_gain_db']['r1'],edge_rms=edge,ramp_ms=4,words='AI systems take this exact mathematical concept and scale it up to thousands of dimensions to measure the distance between complex concepts.'),boards=old['boards'],board_specs=specs,protected_hashes=protected,boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],delta_frames=DELTA,scope='Approved three evaluation improvements: explanatory bridge, less absolute donor narration, larger complete context board. Candidate only.',approval='User: Built it please, with your improvements.',listening='Direct audio audition not available; contextual preview and ASR required. No listening certification.',new_graphic=dict(frames=BRIDGE,renderer=__file__,source_values='Dallas 33 N / 97 W; Coke 9 1 10 2 3 8 1; same seven dimension labels as canonical table'),close={**old['close'],'start_frame':old['close']['start_frame']+DELTA})
 m['actual_board_spans']={s['visual']:[s['start_frame'],s['end_frame']] for s in timeline if s['visual'] in rs}
 m['boards_metadata_note']='boards retains v9 source coordinates and onsets; actual_board_spans is authoritative for this candidate; board_specs uses local frame coordinates.'
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));return old,b,rs,timeline,donors,m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args();assert not DEST.exists(),'Never overwrite a candidate'
 old,b,rs,timeline,donors,m=setup()
 if args.prepare_only:return
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for s in timeline:
  k=s['visual'];n=s['end_frame']-s['start_frame'];rd=None
  if k in donors:
   rd=Reader(donors[k]);dn=int(rd.c.get(cv2.CAP_PROP_FRAME_COUNT))
  for f in range(n):
   if k in rs:im=rs[k].at(f)[0]
   elif k=='bridge':im=bridge(f/30)
   elif k in donors:im=rd.at(round(f/max(1,n-1)*(dn-1)))
   elif k=='close':
    q=np.clip((f-48)/149,0,1);z=1+.2*q*q*(3-2*q);ci=b.close_img;h,w=ci.shape[:2];cw=w/z;ch=cw*9/16;im=cv2.warpAffine(ci,np.float32([[cw/1280,0,(w-cw)/2],[0,ch/720,(h-ch)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   else:im=base.sketch(k,f/30)
   p.stdin.write(im.tobytes())
  if rd:rd.c.release()
  print('Rendered',k,s['end_frame'],'/',TOTAL,flush=True)
 p.stdin.close();assert p.wait()==0
 assert all(sha(Path(p))==h for p,h in m['protected_hashes'].items());m['render_sha256']=sha(DEST)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));print(DEST)
if __name__=='__main__':main()
