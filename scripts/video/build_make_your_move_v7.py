#!/usr/bin/env python3
"""Title-only revision of v6, reconstructed from its original finished source.

Track the original board's scale/translation and replace only its title strip.
All v6 scenes and timings are reproduced; its approved audio is packet-copied.
"""
from pathlib import Path
import json, subprocess
import av, cv2, numpy as np
import build_make_your_move_v6 as base
ROOT=base.ROOT
OUT=ROOT/'video-audit/make-your-move-title-2026-10-01-v7'
DEST=ROOT/'Prompts/make-your-move-v7.mp4'
V6=ROOT/'Prompts/make-your-move-v6.mp4'
OLD=OUT/'skills-before.jpg'
NEW=ROOT/'course-assets/make-your-move/make-your-move-skills.jpg'
RECT=(64,1114,748,1180)

def track():
 cv2.setNumThreads(2)
 orb=cv2.ORB_create(nfeatures=4000)
 old=cv2.imread(str(OLD));kp,des=orb.detectAndCompute(cv2.cvtColor(old,cv2.COLOR_BGR2GRAY),None)
 bf=cv2.BFMatcher(cv2.NORM_HAMMING)
 result={}
 with av.open(str(base.SRC)) as c:
  c.streams.video[0].codec_context.thread_count=2
  for n,f in enumerate(c.decode(video=0)):
   if n<4980:continue
   if n>6650:break
   im=f.to_ndarray(format='bgr24');k,d=orb.detectAndCompute(cv2.cvtColor(im,cv2.COLOR_BGR2GRAY),None)
   matches=[a for a,b in bf.knnMatch(des,d,k=2) if a.distance<.72*b.distance] if d is not None else []
   if len(matches)<18:continue
   a=np.float32([kp[m.queryIdx].pt for m in matches]);b=np.float32([k[m.trainIdx].pt for m in matches])
   mat,inside=cv2.estimateAffinePartial2D(a,b,method=cv2.RANSAC,ransacReprojThreshold=1.5,maxIters=2000)
   if mat is None or inside.sum()<16:continue
   a=a[inside.ravel().astype(bool)];b=b[inside.ravel().astype(bool)]
   # Camera only scales/translates. Remove noisy rotation from the feature fit.
   A=np.zeros((len(a)*2,3));A[::2,0]=a[:,0];A[1::2,0]=a[:,1];A[::2,1]=1;A[1::2,2]=1
   scale,tx,ty=np.linalg.lstsq(A,b.ravel(),rcond=None)[0]
   error=np.sqrt(np.mean((a*scale+[tx,ty]-b)**2))
   if not (.35<scale<1.5 and error<1.5):continue
   result[n]=dict(scale=float(scale),tx=float(tx),ty=float(ty),inliers=len(a),error=float(error))
   if n%300==0:print('Tracked source frame',n,flush=True)
 (OUT/'tracking.json').write_text(json.dumps(result,indent=2)+'\n')
 return result

def patched(picture,t):
 # The replacement uses the exact new canonical title strip. Its white perimeter
 # lies inside the card, so the rest of the scene and all rings remain untouched.
 im=av.VideoFrame.from_ndarray(picture,format='yuv420p').to_ndarray(format='bgr24')
 s,tx,ty=t['scale'],t['tx'],t['ty'];x0,y0,x1,y1=RECT
 M=np.float32([[s,0,tx],[0,s,ty]])
 new=cv2.imread(str(NEW))
 warped=cv2.warpAffine(new,M,(1280,720),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
 left=max(0,round(x0*s+tx));right=min(1280,round(x1*s+tx))
 top=max(0,round(y0*s+ty));bottom=min(720,round(y1*s+ty))
 if left<right and top<bottom:im[top:bottom,left:right]=warped[top:bottom,left:right]
 return base.yuv(im)

def main():
 cv2.setNumThreads(2);OUT.mkdir(exist_ok=True)
 assert base.sha(base.SRC)==base.EXPECTED
 assert base.sha(V6)=='3162a39fa46d8fe2bca309a3af0bb905c34db439b111e22791a72a8aeb4949bd'
 assert not DEST.exists()
 tracks=track() if not (OUT/'tracking.json').exists() else {int(k):v for k,v in json.loads((OUT/'tracking.json').read_text()).items()}
 print('Tracked board frames',len(tracks),flush=True)
 base.OUT=OUT;(OUT/'states').mkdir(exist_ok=True)
 states={b['key']:base.board_states(b) for b in base.BOARDS}
 photos={p['key']:cv2.imread(str(base.ART/(p['key']+'.png'))) for p in base.PHOTOS}
 cmd=[base.FF,'-v','error','-n','-f','rawvideo','-pix_fmt','yuv420p','-s','1280x720','-r','30','-i','pipe:0','-i',str(V6),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-profile:v','high','-level:v','3.1','-crf','16','-preset','fast','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);written=0;freeze=None
 with av.open(str(base.SRC)) as c:
  c.streams.video[0].codec_context.thread_count=2
  for n,f in enumerate(c.decode(video=0)):
   if base.CUT[0]<=n<base.CUT[1]:continue
   picture=f.to_ndarray(format='yuv420p')
   if n==750:freeze=picture.copy()
   if 751<=n<base.CUT[0]:picture=freeze
   cfg=next((b for b in base.BOARDS if b['span'][0]<=n<b['span'][1]),None)
   if cfg:picture=states[cfg['key']][max(k for k in states[cfg['key']] if k<=n)]
   photo=next((p for p in base.PHOTOS if p['span'][0]<=n<p['span'][1]),None)
   if photo:
    a,b=photo['span'];picture=base.yuv(base.photo_frame(photos[photo['key']],n-a,b-a))
   if n in tracks:picture=patched(picture,tracks[n])
   proc.stdin.write(picture.tobytes());written+=1
   if written%1500==0:print('Rendered',written,flush=True)
 proc.stdin.close();assert proc.wait()==0;assert written==8825
 spans=[]
 for n in sorted(tracks):
  if not spans or spans[-1][1]!=n:spans.append([n,n+1])
  else:spans[-1][1]=n+1
 manifest=dict(candidate=str(DEST),sha256=base.sha(DEST),source=str(base.SRC),source_sha256=base.EXPECTED,audio_source=str(V6),audio_source_sha256=base.sha(V6),old_board_sha256=base.sha(OLD),new_board_sha256=base.sha(NEW),title='Create and Solve',title_rect=RECT,source_spans=spans,output_spans=[[base.mapped(a),base.mapped(b)] for a,b in spans],frames=written,fps=30,scope='Title only; v6 timing/cameras/highlights retained, audio packet copied',tracking='Isotropic scale and translation from original asset feature matches; title strip only')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('COMPLETE',DEST,spans,flush=True)
if __name__=='__main__':main()
