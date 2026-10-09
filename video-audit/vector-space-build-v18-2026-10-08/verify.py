from pathlib import Path
import subprocess,json,hashlib,cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
old=ROOT/'Prompts/vector-space-v17.mp4';new=ROOT/'Prompts/vector-space-v18.mp4';ff=imageio_ffmpeg.get_ffmpeg_exe()
manifest=json.loads((OUT/'edit-manifest.json').read_text())
def audiohash(p):
 data=subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-']);return hashlib.sha256(data).hexdigest()
ah,bh=audiohash(old),audiohash(new);assert ah==bh
c=cv2.VideoCapture(str(new));fps=c.get(cv2.CAP_PROP_FPS);w=c.get(cv2.CAP_PROP_FRAME_WIDTH);h=c.get(cv2.CAP_PROP_FRAME_HEIGHT)
assert (fps,w,h)==(30,1280,720)
cues=manifest['drink_cues'];wanted={n+20 for n,s in cues}|set(range(5719,5737))|{0,700,2000,6000,7000,7698};frames={};n=0
while True:
 ok,im=c.read()
 if not ok:break
 if n in wanted:frames[n]=im.copy();cv2.imwrite(str(OUT/'inspection'/f'after-{n:05}.jpg'),im)
 n+=1
assert n==7699
checks=[]
for f,s in cues:
 expected=cv2.imread(str(OUT/'frames'/f'drinks-{s}.png'));err=float(abs(frames[f+20].astype(float)-expected.astype(float)).mean());assert err<4;checks.append({'step':s,'frame':f+20,'mean_absolute_pixel_error':err})
assert abs(frames[5721].astype(float)-frames[5720].astype(float)).mean()<1
assert abs(frames[5722].astype(float)-frames[5720].astype(float)).mean()<1
# Compare unchanged sections against prior encoded candidate.
c=cv2.VideoCapture(str(old));i=0;outside=[]
while True:
 ok,im=c.read()
 if not ok:break
 if i in frames and (i<2562 or i>=5723):
  err=float(abs(im.astype(float)-frames[i].astype(float)).mean());outside.append({'frame':i,'mean_absolute_pixel_error':err});assert err<2
 i+=1
sheet=Image.new('RGB',(1280,1000),'white');draw=ImageDraw.Draw(sheet)
for k,f in enumerate(range(5719,5737)):
 x=(k%4)*320;y=(k//4)*200;sheet.paste(Image.fromarray(cv2.cvtColor(frames[f],cv2.COLOR_BGR2RGB)).resize((320,180)),(x,y+20));draw.text((x+5,y+3),str(f),fill='black')
sheet.save(OUT/'inspection/after-transition.jpg')
result={'decoded_frames':n,'fps':fps,'resolution':[w,h],'duration':n/fps,'audio_sha256':ah,'audio_packets_identical':True,'board_checks':checks,'outside_scope_checks':outside,'flash_frames_covered':True}
(OUT/'verification.json').write_text(json.dumps(result,indent=2))
args=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(new),'--outdir',str(OUT/'transitions')]
for boundary in manifest['boundaries']:args.extend(['--boundary',f"{boundary['frame']}:{boundary['label']}"])
subprocess.run(args,check=True)
print(json.dumps(result,indent=2))
