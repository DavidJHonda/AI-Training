#!/usr/bin/env python3
"""Approved November 6 full production edit of Does School Matter, raw roll 6.

Single encode from pristine sources. Audio removes exactly [3065,3334), with
5ms seam ramps only. All frame intervals are half-open source intervals.
"""
from pathlib import Path
import argparse,json,subprocess,hashlib,re
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Reader,sha
from ken_burns_path import hex_bgr
from build_understand_ai_opener_v12 import draw_ring
from gemini_mark import clean_frame,glyph_mask

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/does-school-matter-v14-2026-11-06'
REVIEW=ROOT/'video-audit/does-school-matter-rolls-5-7-2026-11-06'
SOURCE=ROOT/'Prompts/does-school-matter-6.mp4'
DONOR=ROOT/'Prompts/does-school-matter-5.mp4'
DEST=ROOT/'Prompts/does-school-matter-v14.mp4'
BOARD1=ROOT/'course-assets/does-school-matter/does-school-matter-product-launch.jpg'
BOARD2=ROOT/'course-assets/does-school-matter/what-school-helps-you-build.jpg'
FPS=30;SR=48000;SPF=1600;CUT_A=3065;CUT_Z=3334;REMOVED=CUT_Z-CUT_A;TOTAL=6573-REMOVED
FF=imageio_ffmpeg.get_ffmpeg_exe()
# start, end, kind, donor start (if any), donor end (if bounded), label
SPANS=[
 (0,134,'source',None,None,'student-question'),
 (134,288,'donor',0,154,'phone-fast-access'),
 (288,1365,'source',None,None,'school-and-shared-assignment'),
 (1365,1886,'board1',None,None,'comparison-sales'),
 (1886,2174,'source',None,None,'pricing-improvement-animation'),
 (2174,2441,'board1',None,None,'comparison-email'),
 (2441,2562,'donor',5142,5263,'drafting-cutaway'),
 (2562,3065,'board1',None,None,'comparison-research-and-takeaway'),
 (3334,3350,'board1',None,None,'takeaway-after-audio-cut'),
 (3350,4089,'source',None,None,'different-work-and-school-bridge'),
 (4089,4247,'donor',5142,5300,'writing-papers'),
 (4247,4389,'donor',4950,5046,'working-through-math'),
 (4389,4567,'donor',5142,5320,'research-notes'),
 (4567,4864,'source',None,None,'practice-builds-problem-solving'),
 (4864,5234,'board2',None,None,'knowledge'),
 (5234,5342,'donor',6870,6871,'subject-depth-bridge'),
 (5342,5839,'board2',None,None,'skills-and-school-takeaway'),
 (5839,6066,'retime',5857,6066,'future-facing-interest'),
 (6066,6294,'source',None,None,'knowledge-remains-yours'),
 (6294,6573,'close',None,None,'canonical-close'),
]
RINGS1=[
 (1571,'coworker-card',(40,335,784,1471),'#a9760c'),
 (1613,'coworker-sales',(66,858,758,1034),'#a9760c'),
 (1693,'you-card',(816,335,1560,1471),'#4f2fc4'),
 (1752,'you-sales',(842,858,1534,1034),'#4f2fc4'),
 (2229,'coworker-email',(66,1060,758,1238),'#a9760c'),
 (2366,'you-email',(842,1060,1534,1238),'#4f2fc4'),
 (2606,'coworker-research',(66,1264,758,1446),'#a9760c'),
 (2743,'you-research',(842,1264,1534,1446),'#4f2fc4'),
 (2954,'comparison-takeaway',(40,1511,1560,1599),'#6e51ff'),
]
RINGS2=[
 (5071,'knowledge-card',(40,118,784,749),'#4f2fc4'),
 (5404,'skills-card',(816,118,1560,749),'#1652f0'),
 (5749,'school-takeaway',(40,789,1560,877),'#6e51ff'),
]

def output_frame(s):return s if s<CUT_A else s-REMOVED

def pcm(p):
 return np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-ac','1','-ar',str(SR),'-f','f32le','pipe:1']),np.float32).copy()

def rows():
 result=[];cursor=0
 for a,z,kind,ds,de,label in SPANS:
  result.append(dict(source_start=a,source_end=z,start_frame=cursor,end_frame=cursor+z-a,kind=kind,donor_start=ds,donor_end=de,label=label))
  cursor+=z-a
 assert cursor==TOTAL
 return result

def ease(x):
 x=np.clip(x,0,1);return x*x*(3-2*x)

class Visuals:
 def __init__(self,clean=True):
  self.timeline=rows();self.readers={};self.mask=glyph_mask();self.clean=clean
  self.counts={'clone':0,'inpaint':0,'declined':[]}
  self.b1=cv2.imread(str(BOARD1));self.b2=cv2.imread(str(BOARD2));self.close=cv2.imread(str(OUT/'close.png'))
  assert self.b1.shape[:2]==(1639,1600) and self.b2.shape[:2]==(917,1600)
  self.skills_base=np.full((720,1280,3),255,np.uint8)
  self.ss=720/917;self.sw=round(1600*self.ss);self.sx=(1280-self.sw)//2
  self.skills_base[:,self.sx:self.sx+self.sw]=cv2.resize(self.b2,(self.sw,720),interpolation=cv2.INTER_AREA)
  self.static={}
 def board1(self,s):
  # Keep both complete tall cards visible during the shared detail view.
  full=np.array([800,819.5,1639*16/9]);detail=np.array([800,903,2150.0])
  q=ease((s-1485)/24)
  camera=full+(detail-full)*q
  if s>=2924:camera=detail+(full-detail)*ease((s-2924)/30)
  cx,cy,width=camera;scale=1280/width;left=cx-width/2;top=cy-width*9/32
  M=np.float32([[scale,0,-left*scale],[0,scale,-top*scale]])
  im=cv2.warpAffine(self.b1,M,(1280,720),flags=cv2.INTER_AREA,borderMode=cv2.BORDER_CONSTANT,borderValue=(255,255,255))
  active=next((r for r in reversed(RINGS1) if s>=r[0]),None)
  # Clear the row outline during the pullback, then ring the banner at its spoken onset.
  if 2924<=s<2954:active=None
  key=('board1',tuple(camera),active[1] if active else None)
  if key in self.static:return self.static[key].copy()
  if active:
   _,_,(a,b,c,d),color=active
   draw_ring(im,(a-left)*scale,(b-top)*scale,(c-left)*scale,(d-top)*scale,hex_bgr(color),12*scale,4)
  self.static[key]=im.copy()
  return im
 def board2(self,s):
  im=self.skills_base.copy();active=next((r for r in reversed(RINGS2) if s>=r[0]),None)
  key=('board2',active[1] if active else None)
  if key in self.static:return self.static[key].copy()
  if active:
   _,_,(a,b,c,d),color=active
   draw_ring(im,self.sx+a*self.ss,b*self.ss,self.sx+c*self.ss,d*self.ss,hex_bgr(color),14*self.ss,4)
  self.static[key]=im.copy()
  return im
 def close_frame(self,s):
  k=s-6294;z=1+.2*ease((k-48)/149)
  h,w=self.close.shape[:2];ww=w/z;hh=ww*9/16
  return cv2.warpAffine(self.close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
 def at(self,n):
  row=next(r for r in self.timeline if r['start_frame']<=n<r['end_frame']);s=row['source_start']+n-row['start_frame'];kind=row['kind']
  if kind=='board1':return self.board1(s)
  if kind=='board2':return self.board2(s)
  if kind=='close':return self.close_frame(s)
  # Separate sequential readers allow repeated donor selections without seeking.
  key=row['label'] if kind in ('donor','retime') else 'base'
  path=DONOR if kind=='donor' else SOURCE
  reader=self.readers.setdefault(key,Reader(path)) if key not in self.readers else self.readers[key]
  idx=s if kind=='source' else min(row['donor_start']+n-row['start_frame'],row['donor_end']-1)
  frame=reader.at(idx)
  if self.clean:
   frame,method=clean_frame(frame,self.mask)
   if method:self.counts[method]+=1
   else:self.counts['declined'].append(dict(output_frame=n,source_frame=idx,path=str(path)))
  return frame
 def release(self):
  for r in self.readers.values():r.c.release()

def lesson_fingerprint():
 page=(ROOT/'index.html').read_text()
 section=page[page.index('function WhyBotherSection('):page.index('function MessyNotesLab(')]
 refs='\n'.join(line for line in page.splitlines() if re.match(r'  whybother:',line))
 manifest=json.loads((ROOT/'course-assets/manifest.json').read_text())
 found=[]
 def visit(obj):
  if isinstance(obj,dict):
   if any(isinstance(x,str) and 'course-assets/does-school-matter/' in x for x in obj.values()):found.append(obj)
   else:
    for x in obj.values():visit(x)
  elif isinstance(obj,list):
   for x in obj:visit(x)
 visit(manifest)
 return hashlib.sha256((section+refs+json.dumps(found,sort_keys=True,ensure_ascii=False)).encode()).hexdigest()

def make_manifest():
 protected=[SOURCE,DONOR,BOARD1,BOARD2,ROOT/'course-assets/does-school-matter/does-school-matter-close.jpg',ROOT/'course-assets/does-school-matter/does-school-matter.mp4',ROOT/'lessons/does-school-matter.md']
 boundaries={r['start_frame']:r['label'] for r in rows()[1:]}
 for s,label,_,_ in RINGS1+RINGS2:
  if CUT_A<=s<CUT_Z:continue
  # Only emit a highlight boundary when a course board is actually on screen.
  of=output_frame(s);row=next(r for r in rows() if r['start_frame']<=of<r['end_frame'])
  if row['kind'] in ('board1','board2'):boundaries[of]=label
 boundaries[CUT_A]='audio-cut-on-settled-takeaway'
 return dict(candidate=str(DEST),source=str(SOURCE),donor=str(DONOR),approval='User: Yes. Build it please. November 6, 2026.',
  scope='Approved full production build; candidate only. No installation or publication.',shared_lesson_fingerprint=lesson_fingerprint(),fps=30,frames=TOTAL,duration=TOTAL/30,
  timeline=rows(),audio=dict(remove_source_frames=[CUT_A,CUT_Z],seam_output_frame=CUT_A,edge_ramp_ms=5,added_pause=0,predicted_gap=.8170513333333389),
  boards=[dict(asset=str(BOARD1),density='dense',detail_camera=[800,903,2150],full_view_frames=120,rings=RINGS1),dict(asset=str(BOARD2),density='compact',full_view_frames=5071-4864,rings=RINGS2)],
  close=dict(start_frame=output_frame(6294),hold=48,push=150,endpoint=1.2,settled_frames=81),
  boundaries=[dict(frame=k,label=v) for k,v in sorted(boundaries.items())],protected={str(p):sha(p) for p in protected},
  longest_continuous_board_seconds=max(521,267,519,370,497)/30,
  limitation='No direct listening available; encoded transcription, waveform, frame and transition checks required. Real-time motion review remains outstanding.')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preview-only',action='store_true');args=ap.parse_args()
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 assert sha(SOURCE)=='8511c7583258d55637b977068672a5327497a28277df7c0e44e6380e2fc1c053'
 assert sha(DONOR)=='180ed3c0aa014ba0b4254e8bb8685862d0ecbc0f81330598693a01e3b45eaea0'
 if not (OUT/'close.png').exists():subprocess.run([str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/make_close_board.py'),'--lesson','whybother','--out',str(OUT/'close.png')],check=True)
 v=Visuals();m=make_manifest()
 for s in [1365,1509,1571,1613,1693,1752,2229,2366,2606,2743,2954,4864,5071,5404,5749,6294,6492,6572]:
  n=output_frame(s);im=v.at(n);cv2.imwrite(str(OUT/'preview'/f'planned-{n:05d}.jpg'),im)
 v.release()
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 if args.preview_only:return
 assert not DEST.exists(),'Never overwrite an existing candidate'
 audio=pcm(SOURCE);assert len(audio)>=6573*SPF
 head=audio[:CUT_A*SPF].copy();tail=audio[CUT_Z*SPF:6573*SPF].copy()
 head[-240:]*=np.linspace(1,0,240);tail[:240]*=np.linspace(0,1,240)
 edited=np.concatenate([head,tail]);assert len(edited)==TOTAL*SPF
 subprocess.run([FF,'-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','pipe:0','-c:a','pcm_f32le',str(OUT/'edited.wav')],input=edited.tobytes(),check=True)
 # Render to an explicit scratch path; publish the candidate only after the encoder succeeds.
 temp=OUT/'rendering.mp4'
 p=subprocess.Popen([FF,'-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(temp)],stdin=subprocess.PIPE)
 v=Visuals()
 try:
  for n in range(TOTAL):
   p.stdin.write(v.at(n).tobytes())
   if n%600==0:print(f'Rendered {n}/{TOTAL}',flush=True)
  p.stdin.close();assert p.wait()==0
 finally:v.release()
 assert all(sha(Path(k))==h for k,h in m['protected'].items())
 assert lesson_fingerprint()==m['shared_lesson_fingerprint'],'Relevant lesson changed during render'
 temp.rename(DEST)
 m.update(candidate_sha256=sha(DEST),bytes=DEST.stat().st_size,corner_mark=v.counts,protected_sources_unchanged=True)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print(DEST,flush=True)

if __name__=='__main__':main()
