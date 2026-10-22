"""Approved Layers context repair, reconstructed from v10's retained sources."""
from pathlib import Path
import sys,json,subprocess,inspect,hashlib
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/video'))
import build_layers_v10 as native
from editspec_build import Build,sha,writewav
BASE=ROOT/'Prompts/layers-v10.mp4';DONOR=ROOT/'Prompts/layers-6.mp4';DEST=ROOT/'Prompts/layers-v11.mp4'
ASSET=ROOT/'scripts/video/assets/layers-visual-variety/it-successive-updates-v11.png'
BOARD=ROOT/'course-assets/layers/layers-resolves-it.jpg'
assert not DEST.exists(),'Never overwrite a candidate'
assert sha(BASE)=='67370834ca3117cb69bab6dbad99b2d1b5ed4fcee4344abeb92450268e952c1d'
assert sha(DONOR)=='33cd9b069d8fe6fd4f82d9cc1f439095fbdd91bc3f464f0fb64221171fb7ece2'
protected={str(p):sha(p) for p in [BASE,DONOR,ROOT/'course-assets/layers/layers.mp4',ROOT/'index.html',BOARD,ASSET]}
# Only the CAT/IT board intentionally changed since v10. Other original assets
# retain their identity checks. This adapted setup stays in memory, not in source.
setup_source=inspect.getsource(native.b8.setup)
assert setup_source.count("assert sha(asset) == meta['sha256']")==1
setup_source=setup_source.replace("assert sha(asset) == meta['sha256']", "assert key == '3-it-cat' or sha(asset) == meta['sha256']")
exec(compile(setup_source,'v11-approved-board-setup','exec'),native.b8.__dict__)
native.OUT=OUT
tracking=ROOT/'video-audit/layers-build-2026-09-29-v10/balance-tracking.json'
native.track_panels=lambda:json.loads(tracking.read_text())
context=native.setup()
ff=imageio_ffmpeg.get_ffmpeg_exe();sr=48000;spf=1600
def decode(p):
 return np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(p),'-vn','-ar',str(sr),'-ac','1','-f','f32le','-']),np.float32).copy()
a=decode(BASE);d=decode(DONOR)
grafts=json.loads((ROOT/'video-audit/layers-context-review-2026-10-10/proposed-grafts.json').read_text())
parts=[];cursor=0;outcursor=0
for g in grafts:
 s,e=g['base_frames'];ds,de=g['donor_frames'];gain=10**(g['gain_db']/20)
 kept=a[cursor*spf:s*spf];parts.append(kept);outcursor+=len(kept)//spf
 insert=d[ds*spf:de*spf]*gain
 raw=subprocess.check_output([ff,'-v','error','-f','f32le','-ar',str(sr),'-ac','1','-i','pipe:0',
  '-af','alimiter=limit=0.96:level=false:attack=5:release=50:latency=true','-f','f32le','-'],input=insert.astype(np.float32).tobytes())
 insert=np.frombuffer(raw,np.float32).copy();assert len(insert)==(de-ds)*spf
 r=np.linspace(0,1,240)
 insert[:240]=a[s*spf:s*spf+240]*(1-r)+insert[:240]*r
 insert[-240:]=insert[-240:]*(1-r)+a[e*spf-240:e*spf]*r
 g['output_frames']=[outcursor,outcursor+len(insert)//spf];outcursor+=len(insert)//spf
 parts.append(insert);cursor=e
parts.append(a[cursor*spf:6101*spf]);audio=np.concatenate(parts)
assert len(audio)==6183*spf
# Preserve the base AAC's eight tiny reconstructed overshoots in float PCM;
# converting to int16 would clip them. Peak control applies only to donors.
assert abs(audio).max() <= max(abs(a).max(),0.96)
subprocess.run([ff,'-y','-v','error','-f','f32le','-ar',str(sr),'-ac','1','-i','pipe:0',
 '-c:a','pcm_f32le',str(OUT/'assembled.wav')],input=audio.astype(np.float32).tobytes(),check=True)
for ns,ne,os,oe in [(0,3376,0,3376),(3530,4645,3500,4615),(4780,6183,4698,6101)]:
 assert np.array_equal(audio[ns*spf:ne*spf],a[os*spf:oe*spf])
builder=Build(ROOT,BASE,OUT,DEST)
canvas,cw,ch,ox,oy=builder.compose(BOARD,'updated-it-cat')
board=cv2.resize(cv2.imread(str(canvas)),(1280,720),interpolation=cv2.INTER_AREA)
illustration=cv2.imread(str(ASSET));assert illustration is not None
def old_frame(n):
 if n<3376:return n
 if n<3530:return 3376
 if n<4645:return n-30
 if n<4780:return 4615
 return n-82
def mapped(n):
 assert not (3376<=n<3500 or 4615<=n<4698)
 return n+(0 if n<3376 else 30 if n<4615 else 82)
rects=[(80,158,1520,289),(80,330,353,754),(372,330,645,754),(664,330,937,754),(956,330,1229,754),(1248,330,1521,754)]
cues=[(3382,0),(3539,1),(3809,2),(3984,3),(4205,4),(4497,5)]
def frame(n):
 if 4223<=n<4446:return native.b9.illustration(illustration,(n-4223)/222)
 if 3377<=n<4793:
  im=board.copy();active=next((i for at,i in reversed(cues) if n>=at),None)
  if active is not None:
   x,y,x2,y2=rects[active]
   x,x2=[round((t+ox)*1280/cw) for t in (x,x2)];y,y2=[round((t+oy)*720/ch) for t in (y,y2)]
   color=(196,47,79);r=10
   cv2.line(im,(x+r,y),(x2-r,y),color,4,cv2.LINE_AA);cv2.line(im,(x+r,y2),(x2-r,y2),color,4,cv2.LINE_AA)
   cv2.line(im,(x,y+r),(x,y2-r),color,4,cv2.LINE_AA);cv2.line(im,(x2,y+r),(x2,y2-r),color,4,cv2.LINE_AA)
   for pt,start,end in [((x+r,y+r),180,270),((x2-r,y+r),270,360),((x2-r,y2-r),0,90),((x+r,y2-r),90,180)]:cv2.ellipse(im,pt,(r,r),0,start,end,color,4,cv2.LINE_AA)
  return im
 return native.frame_at(old_frame(n),context)
old=json.loads((ROOT/'video-audit/layers-build-2026-09-29-v10/edit-manifest.json').read_text())
boundaries={mapped(n):'Inherited transition' for n in old['boundaries'] if not (3376<=n<3500 or 4615<=n<4698)}
boundaries.update({3376:'Sentence donor starts',3377:'Updated board',3530:'Original start narration',4223:'Corrected supporting illustration',4446:'Return to board',4645:'Conclusion donor starts',4780:'Original narration resumes',4793:'Layer count scene'})
boundaries.update({n:'Context focus' for n,i in cues})
m=dict(output=str(DEST),base=str(BASE),fps=30,frames=6183,duration=206.1,approval='User: Build the Layer video',
 scope='Two approved narration grafts, current CAT/IT board, corrected sentence on supporting illustration; all other treatment retained.',
 grafts=grafts,protected=protected,board=str(BOARD),board_canvas=[cw,ch,ox,oy],board_rects=rects,board_cues=cues,
 board_spans=[[3377,4223],[4446,4793]],illustration_span=[4223,4446],illustration=str(ASSET),
 source_limit='Original reconstruction uses retained earlier published edit; earliest raw source unavailable.',
 native_setup_sha256=hashlib.sha256(setup_source.encode()).hexdigest(),boundaries=[dict(frame=n,label=l) for n,l in sorted(boundaries.items())],
 unchanged_pcm_identical_before_encoding=True,base_decoded_peak=float(abs(a).max()),
 assembled_peak=float(abs(audio).max()),direct_listening=False,installed=False)
(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'assembled.wav'),
 '-map','0:v','-map','1:a','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
for n in range(6183):
 p.stdin.write(frame(n).tobytes())
 if n%1000==0:print('Rendered',n,'/ 6183',flush=True)
p.stdin.close();assert p.wait()==0
assert all(sha(Path(p))==h for p,h in protected.items())
m.update(render_sha256=sha(DEST),protected_files_unchanged=True)
(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print('Finished',DEST,flush=True)
