from pathlib import Path
import sys,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path('scripts/video').resolve()))
from ken_burns_path import draw_ring,hex_bgr
out=Path('video-audit/does-school-matter-rolls-5-7-2026-11-06');pre=out/'previews';pre.mkdir(exist_ok=True)
im=cv2.imread('course-assets/does-school-matter/does-school-matter-product-launch.jpg')
# Each zoom keeps the complete active card, including portrait, title and all three rows.
def shot(name,cx,cy,width,rect=None,color='#4f2fc4'):
 scale=1280/width;h=width*720/1280;left=cx-width/2;top=cy-h/2
 M=np.float32([[scale,0,-left*scale],[0,scale,-top*scale]])
 frame=cv2.warpAffine(im,M,(1280,720),flags=cv2.INTER_AREA,borderMode=cv2.BORDER_CONSTANT,borderValue=(255,255,255))
 if rect:
  a,b,c,d=rect;draw_ring(frame,(a-left)*scale,(b-top)*scale,(c-left)*scale,(d-top)*scale,hex_bgr(color),10,4)
 cv2.imwrite(str(pre/f'{name}.jpg'),frame)
shot('comparison-full',800,819.5,1639*16/9)
shot('comparison-you-full-card',800,903,2150,(816,335,1560,1471))
shot('comparison-you-sales',800,903,2150,(842,858,1534,1034))
shot('comparison-coworker-email',800,903,2150,(66,1060,758,1238),'#a9760c')
# Full-view skills treatment.
b=cv2.imread('course-assets/does-school-matter/what-school-helps-you-build.jpg');s=720/917;w=round(1600*s);x=(1280-w)//2
frame=np.full((720,1280,3),255,np.uint8);frame[:,x:x+w]=cv2.resize(b,(w,720))
for name,rect,col in [('skills-full',None,None),('skills-card',(816,118,1560,749),'#1652f0')]:
 f=frame.copy()
 if rect:
  a,c,z,d=rect;draw_ring(f,x+a*s,c*s,x+z*s,d*s,hex_bgr(col),10,4)
 cv2.imwrite(str(pre/f'{name}.jpg'),f)
# Donor stills sequentially decoded, no CAP_PROP_POS_* seeking.
for roll,targets in [(5,[162.5,172.5,219.95,229]),(6,[8.5,70,120,138.5,144.5,150,159,175]),(7,[132.5])]:
 cap=cv2.VideoCapture(f'Prompts/does-school-matter-{roll}.mp4');idx=0;pending=[round(t*30) for t in targets]
 while pending:
  ok,f=cap.read()
  if not ok:break
  if idx==pending[0]:
   cv2.imwrite(str(pre/f'roll-{roll}-{idx/30:.2f}.jpg'),f);pending.pop(0)
  idx+=1
 cap.release()
# Audition-only excerpt: source 98 to 102+5/30, then 111+4/30 to117.5.
a=3065/30;z=3334/30
pcm=np.frombuffer(subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i','Prompts/does-school-matter-6.mp4','-vn','-ac','1','-ar','48000','-f','f32le','pipe:1']),np.float32).copy()
parts=[pcm[98*48000:round(a*48000)].copy(),pcm[round(z*48000):round(117.5*48000)].copy()]
parts[0][-240:]*=np.linspace(1,0,240);parts[1][:240]*=np.linspace(0,1,240)
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y','-f','f32le','-ar','48000','-ac','1','-i','pipe:0','-c:a','pcm_s16le',str(pre/'proposed-narration-cut.wav')],input=np.concatenate(parts).tobytes(),check=True)
(out/'cut-proposal.json').write_text(json.dumps(dict(source='Prompts/does-school-matter-6.mp4',remove_frames=[3065,3334],remove_seconds=[a,z],seconds_removed=z-a,expected_duration=(6573-269)/30,source_gaps=[[101.851565,102.497937],[110.756417,111.635283]],predicted_join_gap=(a-101.851565)+(111.635283-z),listening='Not auditioned by agent; review excerpt supplied',status='Proposed, not approved or built'),indent=2)+'\n')
