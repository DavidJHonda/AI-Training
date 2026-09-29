from pathlib import Path
import hashlib,importlib.util,json,subprocess
import cv2,numpy as np
from PIL import Image,ImageDraw
import imageio_ffmpeg
ROOT=Path.cwd();OUT=ROOT/'video-audit/your-home-base-labels-2026-09-29-v7'
spec=importlib.util.spec_from_file_location('build',ROOT/'scripts/video/build_your_home_base_v7.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
ff=imageio_ffmpeg.get_ffmpeg_exe();src=mod.SRC;dst=mod.DEST

def audiohash(p,copy):
 cmd=[ff,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy' if copy else 'pcm_s16le','-f','hash','-hash','sha256','-']
 return subprocess.check_output(cmd,text=True).strip()

def decode(p):
 r=subprocess.run([ff,'-v','error','-i',str(p),'-f','null','-'],capture_output=True,text=True);assert r.returncode==0 and not r.stderr;r={'exit':r.returncode,'errors':r.stderr};return r
p=mod.Patch();a=cv2.VideoCapture(str(src));b=cv2.VideoCapture(str(dst));n=0;outside=[];raw_unchanged=0;patched=0;frames=[]
(OUT/'encoded').mkdir(exist_ok=True)
picks=set([1518,1519,1521,1524,1527,1530,1533,1536,1542,1550,1770,1834,1835,4241,4242,4320,4380,4440,4500,4650,4651,6995])|set(range(1560,1835,30))|set(range(4242,4651,30))
while True:
 oka,fa=a.read();okb,fb=b.read();assert oka==okb
 if not oka:break
 expected=p.apply(fa.copy(),n);mask=np.ones(fa.shape[:2],dtype=bool)
 if mod.TRAIN_START<=n<mod.TRAIN_END:rect=mod.A
 elif mod.APPS_START<=n<mod.APPS_END:rect=mod.B
 else:rect=None
 if rect:
  x,y,r,bt=rect;mask[y:bt,x:r]=False;patched+=1
  assert np.array_equal(expected[mask],fa[mask]),f'Unapproved changed pixels at frame {n}'
 else:
  assert np.array_equal(expected,fa);raw_unchanged+=1
 if n%30==0 or n in picks:
  outside.append([n,float(np.abs(fa.astype('int16')-fb.astype('int16'))[mask].mean())])
 if n in picks:
  cv2.imwrite(str(OUT/'encoded'/f'{n:06d}.jpg'),fb,[cv2.IMWRITE_JPEG_QUALITY,95]);frames.append(n)
 n+=1
fps=b.get(cv2.CAP_PROP_FPS);w=b.get(cv2.CAP_PROP_FRAME_WIDTH);h=b.get(cv2.CAP_PROP_FRAME_HEIGHT);a.release();b.release();assert n==6996 and fps==30 and w==1280 and h==720
q={'frames':n,'fps':fps,'dimensions':[w,h],'duration':n/fps,'raw_unchanged_frames':raw_unchanged,'patched_frames':patched,'outside_patch_pixels_unchanged_before_encoding':True,'encoded_outside_patch_MAE_max':max(x[1] for x in outside),'encoded_outside_patch_MAE_mean':float(np.mean([x[1] for x in outside])),'source_unchanged':mod.sha(src)==mod.SHA,'audio_packet_hash':{'source':audiohash(src,True),'candidate':audiohash(dst,True)},'audio_pcm_hash':{'source':audiohash(src,False),'candidate':audiohash(dst,False)},'full_decode':decode(dst)}
assert q['audio_packet_hash']['source']==q['audio_packet_hash']['candidate'];assert q['audio_pcm_hash']['source']==q['audio_pcm_hash']['candidate']
(OUT/'verification.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2),flush=True)
for page,offset in enumerate(range(0,len(frames),12)):
 sh=Image.new('RGB',(1440,1080),'white')
 for j,n in enumerate(frames[offset:offset+12]):
  im=Image.open(OUT/'encoded'/f'{n:06d}.jpg').resize((480,270));ImageDraw.Draw(im).text((4,4),f'{n/30:.3f}s  f{n}',fill='red',stroke_width=1,stroke_fill='white');sh.paste(im,(j%3*480,j//3*270))
 sh.save(OUT/f'encoded-sheet-{page}.jpg')
cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(dst),'--outdir',str(OUT/'guard')]
for n,label in [(1519,'training-label-fade-start'),(1835,'training-to-monitors'),(4242,'apps-scene-in'),(4651,'apps-to-home-base')]:cmd+=['--boundary',f'{n}:{label}']
subprocess.run(cmd,check=True)
