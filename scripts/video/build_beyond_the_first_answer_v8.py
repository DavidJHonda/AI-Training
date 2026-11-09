#!/usr/bin/env python3
"""Cinematic picture throughout, with untouched explainer narration.

Owner correction 2026-11-09: use the narration, not the explainer visual format.
Every output frame comes from cinematic rolls 3/5 or the canonical lesson assets.
The explainer is opened by FFmpeg solely as the mapped audio input.
"""
from pathlib import Path
import argparse, json, subprocess, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_beyond_the_first_answer_v7 as base
from editorial_typography import face
from gemini_mark import clean_frame, glyph_mask

ROOT=base.ROOT
AUDIT=ROOT/'video-audit/beyond-the-first-answer-cinematic-v8-2026-11-09'
DEST=ROOT/'Prompts/beyond-the-first-answer-v8.mp4'
SOURCE=base.SOURCE
FPS,TOTAL,W,H=24,5832,1280,720
base.AUDIT=AUDIT
base.SPANS=dict(base.SPANS,**{'summer-business':(1060,2084)})
SPANS=base.SPANS
# output in/out; roll; source in/out (30fps); label; optional exact lesson title.
SCENES=[
 (0,190,'3',112,290,'perfect-prompt',''),
 (190,267,'3',0,112,'prompt-frustration',''),
 (267,657,'3',290,506,'history-group-project',''),
 (657,1060,'3',686,931,'thought-partner','Thought Partner'),
 (2084,2220,'5',2560,2817,'learn-with-ai','Learn With AI'),
 (2220,2404,'3',2713,3018,'learning-conversation',''),
 (2404,2616,'3',2550,2713,'lawn-mowing-finances',''),
 (3451,3699,'3',4149,4315,'find-a-place-to-start','Find a Place to Start'),
 (3699,3886,'5',3993,4262,'college-first-question',''),
 (4397,4574,'3',5388,5636,'iterate-with-ai','Iterate With AI'),
 (4574,4784,'3',5258,5388,'sketch-to-business-plan',''),
]
ROLLS={k:ROOT/f'Prompts/beyond-the-first-answer-{k}.mp4' for k in ('3','5')}
EXPECTED={'3':base.DONOR_SHA,'5':'8eb356616aa30264ca509ca49d1e5fa5187999f954a708c893b2e831df7f4d2e'}
FONT=face('bold',40)

def coverage():
 spans=[(a,z,label,'cinematic') for a,z,roll,s,e,label,title in SCENES]+[(a,z,slug,'canonical-board') for slug,(a,z) in SPANS.items()]+[(base.CLOSE_IN,TOTAL,'close','canonical-close')]
 spans.sort();n=0
 for a,z,label,kind in spans:assert a==n and z>a,(n,a,z,label);n=z
 assert n==TOTAL
 return spans

def caption(im,scene,n):
 a,z,roll,s,e,label,title=scene
 if not title:return im
 if label=='iterate-with-ai':
  # Replace only the original ITERATION heading, preserving its definition and animation.
  im=im.copy();im[36:88,380:900]=im[36:88,20:21]
  y=43;alpha=1.0;color='#245a80';x=W/2;anchor='ma'
 else:
  # Brief title over existing cinematic art, in its clear top margin.
  elapsed=n-a;alpha=max(0,min(1,(96-elapsed)/12))
  if alpha<=0:return im
  y=34;color='#343a40';x=54;anchor='la'
 canvas=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));draw=ImageDraw.Draw(canvas)
 draw.text((x,y),title,font=FONT,fill=color,anchor=anchor)
 titled=cv2.cvtColor(np.asarray(canvas),cv2.COLOR_RGB2BGR)
 return cv2.addWeighted(titled,alpha,im,1-alpha,0) if alpha<1 else titled

def mapped(scene,n):
 a,z,roll,s,e,label,title=scene
 return s+round((n-a)*(e-s-1)/(z-a-1))

def load_donors():
 cache={};methods={};mask=glyph_mask()
 for roll,path in ROLLS.items():
  needed={mapped(scene,n) for scene in SCENES if scene[2]==roll for n in range(scene[0],scene[1])}
  cap=cv2.VideoCapture(str(path));assert cap.get(cv2.CAP_PROP_FPS)==30;n=0
  while cap.grab():
   if n in needed:
    ok,im=cap.retrieve();assert ok
    im,method=clean_frame(im,mask);assert method is not None
    methods[method]=methods.get(method,0)+1
    cache[(roll,n)]=cv2.imencode('.png',im)[1]
   n+=1
   if n>max(needed):break
  cap.release();assert all((roll,n) in cache for n in needed)
  print(f'Prepared cinematic roll {roll}: {len(needed)} source frames',flush=True)
 return cache,methods

def scene_frame(scene,n,cache):
 return caption(cv2.imdecode(cache[(scene[2],mapped(scene,n))],cv2.IMREAD_COLOR),scene,n)

def prepare():
 AUDIT.mkdir(exist_ok=True);spans=coverage();boards,close=base.prepare()
 return boards,close,spans

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert base.sha(SOURCE)==base.EXPECTED
 for k,p in ROLLS.items():assert base.sha(p)==EXPECTED[k]
 boards,close,spans=prepare()
 protected={str(p):base.sha(p) for p in [ROOT/'index.html',ROOT/'course-assets/manifest.json',ROOT/'lessons/beyond-the-first-answer.md',*base.ASSETS.glob('*')] if p.is_file()}
 (AUDIT/'protected-before.json').write_text(json.dumps(protected,indent=2)+'\n')
 spec={slug:{k:v for k,v in b.items() if k!='image'} for slug,b in boards.items()}
 (AUDIT/'board-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
 cache,methods=load_donors()
 for scene in SCENES:
  a,z,roll,s,e,label,title=scene
  for n in sorted({a,min(a+48,z-1),(a+z)//2,z-1}):
   cv2.imwrite(str(AUDIT/'previews'/f'{label}-{n:04d}.jpg'),scene_frame(scene,n,cache))
 plan=dict(scope='Visual correction: cinematic pictures throughout, approved explainer audio retained',duration_seconds=243,fps=24,frames=5832,explainer_visual_frames=0,segments=[dict(start=a,end=z,label=label,kind=kind) for a,z,label,kind in spans],scenes=[dict(output_frames=[a,z],source=str(ROLLS[roll]),source_frames=[s,e],source_fps=30,label=label,title=title) for a,z,roll,s,e,label,title in SCENES],boards=spec,corner_cleanup=methods)
 (AUDIT/'picture-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
 if args.prepare_only:return
 assert not DEST.exists(),f'Never overwrite a candidate: {DEST}'
 cmd=[base.FF,'-v','error','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','24','-i','pipe:0','-i',str(SOURCE),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-profile:v','high','-level:v','3.1','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)]
 (AUDIT/'encode-command.json').write_text(json.dumps(cmd,indent=2)+'\n')
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for n in range(TOTAL):
  if n>=base.CLOSE_IN:im=base.close_frame(close,n)
  else:
   for slug,b in boards.items():
    if b['span'][0]<=n<b['span'][1]:im=base.board_frame(b,n);break
   else:
    matches=[scene for scene in SCENES if scene[0]<=n<scene[1]];assert len(matches)==1
    im=scene_frame(matches[0],n,cache)
  proc.stdin.write(im.tobytes())
  if (n+1)%720==0:print(f'Rendered {n+1}/{TOTAL}',flush=True)
 proc.stdin.close();assert proc.wait()==0
 cap=cv2.VideoCapture(str(DEST));fps=cap.get(cv2.CAP_PROP_FPS);count=0
 while cap.grab():count+=1
 cap.release();assert count==TOTAL and fps==FPS
 audio=base.audio_sha(DEST);assert audio==base.audio_sha(SOURCE)
 for k,p in ROLLS.items():assert base.sha(p)==EXPECTED[k]
 assert base.sha(SOURCE)==base.EXPECTED
 changes=[p for p,h in protected.items() if base.sha(p)!=h]
 assert all(p in [str(ROOT/'index.html'),str(ROOT/'course-assets/manifest.json')] for p in changes),changes
 plan.update(candidate=str(DEST),candidate_sha256=base.sha(DEST),audio_source_sha256=base.EXPECTED,audio_payload_sha256=audio,audio_packets_identical=True,source_hashes=EXPECTED,protected_lesson_files_unchanged=True,concurrent_shared_file_changes=changes,publication='Review candidate only; installed v7 unchanged',limitations=['Audio input unavailable: no full listening pass claimed.','Frame samples and transition strips do not establish continuous audiovisual review.'])
 (AUDIT/'edit-manifest.json').write_text(json.dumps(plan,indent=2)+'\n')
 args=[x for a,z,label,kind in spans if a>0 for x in ('--boundary',f'{a}:{label}')]
 subprocess.run([sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),*args,'--outdir',str(AUDIT/'transitions')],check=True)
 print('Complete:',DEST,flush=True)

if __name__=='__main__':main()
