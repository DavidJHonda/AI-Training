#!/usr/bin/env python3
"""Approved explainer narration + current illustrated boards; review candidate only.

Native 24fps, all 5832 source frames, bit-for-bit copied compressed audio.
Source clips are decoded sequentially. No course files are written.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys, types
import cv2
import numpy as np
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts/video'))
from editspec_build import Build
from ken_burns_path import smoothstep, window, draw_ring, hex_bgr, ring_px
from render_beyond_illustrated import BOARDS, measure, bubble_height
from make_close_board import compose_canonical_for_video
from gemini_mark import clean_frame, glyph_mask

AUDIT=ROOT/'video-audit/beyond-the-first-answer-build-v7-2026-11-07'
SOURCE=ROOT/'Prompts/beyond-the-first-answer-explainer.mp4'
DONOR=ROOT/'Prompts/beyond-the-first-answer-3.mp4'
DEST=ROOT/'Prompts/beyond-the-first-answer-v7.mp4'
ASSETS=ROOT/'course-assets/beyond-the-first-answer'
FF=imageio_ffmpeg.get_ffmpeg_exe()
FPS,TOTAL,W,H=24,5832,1280,720
EXPECTED='2f1c2aad7c18a3e8212a39bbfd1c42849271489a1b917e55b852c05bb892d4e8'
DONOR_SHA='7805d83014439135c1701cb25d23ba2878d153f55c1b0b61f1dd7086d8cc8214'
PURPLE,BLUE,NEUTRAL='#4f2fc4','#1652f0','#6e51ff'
# Half-open output frames, source frames. Donor source is 30fps.
INSERTS=[
 (267,657,290,506,'group-project','Students exchange ideas around a shared history project.'),
 (746,1060,686,931,'thought-partner','Student and illustrated AI collaborate; human makes the decisions.'),
 (2404,2616,2550,2713,'lawn-mowing-finances','Lawn mower with cash and coins grounds the profit example.'),
]
SPANS={'summer-business':(1164,2084),'profit':(2616,3451),'college':(3886,4397),'iteration':(4784,5612)}
CLOSE_IN=5612

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fr(t):return round(t*FPS)
def audio_sha(p):
 data=subprocess.check_output([FF,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','data','-'])
 return hashlib.sha256(data).hexdigest()

def targets(board,bh):
 slug=board.slug; rows=[]
 def add(a,b,rect,label,color=NEUTRAL):rows.append(dict(start=fr(a),end=fr(b),rect=rect,label=label,color=color))
 if slug=='summer-business':
  y=161;bubs=[];positions=[]
  for turn in board.turns:
   positions.append(y);h=bubble_height(turn.text,832,32)-35
   x=694 if turn.role=='YOU' else 586;bubs.append([x,y+35,832,h]);y+=35+h+28
  firsth=240+32+52+41+34; secondh=240+32+52+3*41+34
  add(50.56,54.98,[40,127,480,firsth],'Your strengths',PURPLE)
  add(50.56,54.98,[40,positions[2]-34,480,secondh],'Possible directions',BLUE)
  times=[57.40,63.08,68.92,72.90,82.56]
  for i in range(4):add(times[i],times[i+1],bubs[i],f'Turn {i+1}',PURPLE if i%2==0 else BLUE)
  banner=82.56
 elif slug in ('profit','college'):
  h=339+32+52+max(len(measure(t.text,676)) for t in board.turns)*41+34
  if slug=='profit':
   add(111.04,120.68,[40,127,744,h],'You',PURPLE)
   add(120.68,128.50,[816,127,744,h],'AI',BLUE)
   add(128.50,139.94,[40,127+h+32,1520,134],'Sales minus costs equals profit')
   banner=139.94
  else:
   add(163.94,172.98,[40,127,744,h],'You',PURPLE)
   add(172.98,179.82,[816,127,744,h],'AI',BLUE)
   banner=179.82
 else:
  bubs=[]
  for i,x in enumerate((40,816)):
   y=550
   for turn in board.turns[i*2:i*2+2]:
    h=bubble_height(turn.text,612)-35;bx=x+98 if turn.role=='YOU' else x+34
    bubs.append([bx,y+35,612,h]);y+=35+h+28
  times=[201.46,204.84,213.04,224.16,230.56]
  for i in range(4):add(times[i],times[i+1],bubs[i],f'Turn {i+1}',PURPLE if i%2==0 else BLUE)
  banner=230.56
 if board.takeaway:
  add(banner,SPANS[slug][1]/FPS,[40,bh-128,1520,88],'Takeaway')
 return rows

def prepare():
 AUDIT.mkdir(exist_ok=True);(AUDIT/'previews').mkdir(exist_ok=True)
 boards={}
 for b in BOARDS:
  p=ASSETS/f'beyond-the-first-answer-{b.slug}.jpg';raw=cv2.imread(str(p))
  canvas,cw,ch,ox,oy=Build.compose(types.SimpleNamespace(out=AUDIT),p,b.slug)
  rows=targets(b,raw.shape[0]);start,end=SPANS[b.slug]
  assert min(r['start'] for r in rows)-start>=48
  for r in rows:
   x,y,w,h=r['rect'];assert x>=0 and y>=0 and x+w<=raw.shape[1] and y+h<=raw.shape[0]
  boards[b.slug]=dict(image=cv2.imread(str(canvas)),size=[cw,ch],offset=[ox,oy],rings=rows,asset=str(p),sha256=sha(p),span=[start,end])
 close=AUDIT/'canvas-close.png';compose_canonical_for_video(ASSETS/'beyond-the-first-answer-close.jpg',close,'#ffffff')
 close=cv2.imread(str(close))
 for slug,b in boards.items():
  samples=sorted({b['span'][0],*[r['start']+min(24,(r['end']-r['start'])//2) for r in b['rings']]})
  for n in samples:cv2.imwrite(str(AUDIT/'previews'/f'{slug}-{n:04d}.jpg'),board_frame(b,n))
 for n in (CLOSE_IN,CLOSE_IN+38,CLOSE_IN+158,TOTAL-1):cv2.imwrite(str(AUDIT/'previews'/f'close-{n}.jpg'),close_frame(close,n))
 return boards,close

def board_frame(b,n):
 im=b['image'];cw,ch=b['size'];ox,oy=b['offset'];a,z=b['span']
 # Compact chat: whole board visible, restrained 2% push, no dives.
 progress=smoothstep((n-a)/max(1,z-a-1));width=cw*(1-.02*progress)
 x,y,w,h=window(cw/2,ch/2,width,W/H,cw,ch)
 frame=cv2.warpAffine(im,np.array([[w/W,0,x],[0,h/H,y]],np.float32),(W,H),flags=cv2.INTER_LANCZOS4|cv2.WARP_INVERSE_MAP)
 for r in b['rings']:
  if r['start']<=n<r['end']:
   rx,ry,rw,rh=r['rect'];scale=W/w;x0=(rx+ox-x)*scale;y0=(ry+oy-y)*scale
   x1=x0+rw*scale;y1=y0+rh*scale
   assert min(x0,y0)>ring_px(H) and x1<W-ring_px(H) and y1<H-ring_px(H)
   draw_ring(frame,x0,y0,x1,y1,hex_bgr(r['color']),14*scale,ring_px(H))
 return frame

def close_frame(im,n):
 local=n-CLOSE_IN;z=1+.2*smoothstep(min(1,max(0,(local-38)/119)))
 ih,iw=im.shape[:2];x,y,w,h=window(iw/2,ih/2,iw/z,W/H,iw,ih)
 return cv2.warpAffine(im,np.array([[w/W,0,x],[0,h/H,y]],np.float32),(W,H),flags=cv2.INTER_LANCZOS4|cv2.WARP_INVERSE_MAP)

def donor_frames():
 wanted={i for a,b,s,e,name,why in INSERTS for i in range(s,e)}
 cap=cv2.VideoCapture(str(DONOR));i=0;found={};methods={};mask=glyph_mask()
 while cap.grab():
  if i in wanted:
   ok,im=cap.retrieve();assert ok
   im,method=clean_frame(im,mask);assert method is not None
   methods[method]=methods.get(method,0)+1
   # PNG compression keeps the sequentially decoded donor cache small and lossless.
   found[i]=cv2.imencode('.png',im)[1]
  i+=1
  if i>max(wanted):break
 cap.release();assert len(found)==len(wanted)
 return found,methods

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');ap.add_argument('--verify-existing',action='store_true');args=ap.parse_args()
 assert sha(SOURCE)==EXPECTED and sha(DONOR)==DONOR_SHA
 boards,close=prepare()
 spec={slug:{k:v for k,v in b.items() if k!='image'} for slug,b in boards.items()}
 (AUDIT/'board-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
 if args.prepare_only:return
 assert args.verify_existing or not DEST.exists(),f'Never overwrite review candidate: {DEST}'
 protected={str(p):sha(p) for p in [ROOT/'index.html',ROOT/'lessons/beyond-the-first-answer.md',*ASSETS.glob('*'),ROOT/'course-assets/manifest.json'] if p.is_file()}
 if not args.verify_existing:
  (AUDIT/'protected-before.json').write_text(json.dumps(protected,indent=2)+'\n')
  donors,methods=donor_frames()
  cmd=[FF,'-v','error','-f','rawvideo','-pixel_format','bgr24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(SOURCE),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-profile:v','high','-level:v','3.1','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)]
  (AUDIT/'encode-command.json').write_text(json.dumps(cmd,indent=2)+'\n')
  proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);cap=cv2.VideoCapture(str(SOURCE));n=0;last_donor=-1;cached=None
  while True:
   ok,im=cap.read()
   if not ok:break
   if n>=CLOSE_IN:im=close_frame(close,n)
   else:
    for slug,b in boards.items():
     if b['span'][0]<=n<b['span'][1]:im=board_frame(b,n);break
    else:
     for a,z,s,e,name,why in INSERTS:
      if a<=n<z:
       source_n=s+round((n-a)*(e-s-1)/(z-a-1))
       if source_n!=last_donor:cached=cv2.imdecode(donors[source_n],cv2.IMREAD_COLOR);last_donor=source_n
       im=cached;break
   proc.stdin.write(im.tobytes());n+=1
   if n%720==0:print(f'Rendered {n}/{TOTAL}',flush=True)
  cap.release();proc.stdin.close();assert proc.wait()==0 and n==TOTAL
 else:
  assert DEST.exists()
  methods={'verification_note':'All donor frames cleaned during the completed render; method counts were not saved before its final shared-file check.'}
  # Recover the already completed render; never encode over the candidate.
  for p in ASSETS.glob('*'):
   assert p.stat().st_mtime < DEST.stat().st_birthtime,(p,'changed since render began')
  assert (ROOT/'lessons/beyond-the-first-answer.md').stat().st_mtime < DEST.stat().st_birthtime
 cap=cv2.VideoCapture(str(DEST));fps=cap.get(cv2.CAP_PROP_FPS);count=0
 while cap.grab():count+=1
 cap.release();assert count==TOTAL and fps==FPS
 before,after=audio_sha(SOURCE),audio_sha(DEST);assert before==after
 assert sha(SOURCE)==EXPECTED and sha(DONOR)==DONOR_SHA
 changed=[p for p,digest in protected.items() if sha(p)!=digest]
 assert all(p in [str(ROOT/'index.html'),str(ROOT/'course-assets/manifest.json')] for p in changed),changed
 manifest=dict(scope='Approved visual assembly; review only, not installed',source=str(SOURCE),source_sha256=EXPECTED,donor=str(DONOR),donor_sha256=DONOR_SHA,candidate=str(DEST),candidate_sha256=sha(DEST),fps=fps,frames=count,duration=count/fps,audio_payload_sha256=after,audio_packets_identical=True,protected_scope_assets=protected,concurrent_shared_file_changes=changed,verification_mode='existing completed render' if args.verify_existing else 'fresh render',boards=spec,donor_corner_cleanup=methods,supporting_illustrations=[dict(output_frames=[a,z],output_seconds=[a/FPS,z/FPS],source_frames=[s,e],source_fps=30,name=name,teaching_purpose=why) for a,z,s,e,name,why in INSERTS],close=dict(start_frame=CLOSE_IN,end_frame=TOTAL,hold_frames=38,push_frames=120,zoom=1.2),longest_unbroken_board_run_seconds=max(z-a for a,z in SPANS.values())/FPS,board_hold_reason='Spoken walkthroughs of all twelve turns; full compact boards remain visible. No unrelated filler interrupts the active conversations.',unperformed_checks=['End-to-end human listening: this runtime cannot hear audio.','Continuous real-time viewing with sound; frame-sequence checks do not certify this.'])
 (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 boundaries={a:f'enter-{name}' for a,z,s,e,name,why in INSERTS}
 boundaries.update({z:f'exit-{name}' for a,z,s,e,name,why in INSERTS})
 for slug,(a,z) in SPANS.items():boundaries[a]=f'enter-{slug}';boundaries[z]=f'exit-{slug}'
 boundaries[CLOSE_IN]='standard-close'
 args=[x for f,label in sorted(boundaries.items()) for x in ('--boundary',f'{f}:{label}')]
 subprocess.run([sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),*args,'--outdir',str(AUDIT/'transitions')],check=True)
 print('Complete:',DEST,flush=True)

if __name__=='__main__':main()
