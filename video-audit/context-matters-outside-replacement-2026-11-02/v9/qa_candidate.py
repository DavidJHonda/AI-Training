from pathlib import Path
import json,subprocess,hashlib,cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
R=Path.cwd();O=R/'video-audit/context-matters-outside-replacement-2026-11-02/v9';FF=imageio_ffmpeg.get_ffmpeg_exe()
M=json.loads((O/'edit-manifest.json').read_text());c=cv2.VideoCapture(str(R/M['candidate']));s=cv2.VideoCapture(str(R/'course-assets/context-matters/context-matters.mp4'));si=-1;old=None;stats={'prefix':[],'tail':[]};samples={};wanted={5128,5129,5219,5220,5231,5477,5755,5867,5868,6947};n=0
while True:
 ok,f=c.read()
 if not ok:break
 if n in wanted:samples[n]=f.copy()
 source_n=n if n<5129 else n+513 if n>=5868 else None
 if source_n is not None:
  while si<source_n:
   ok2,old=s.read();assert ok2;si+=1
  # Compare every unchanged frame at thumbnail resolution to expose offset/frame drops.
  err=float(np.mean(abs(cv2.resize(f,(160,90)).astype(float)-cv2.resize(old,(160,90)))))
  stats['prefix' if n<5129 else 'tail'].append(err)
 n+=1
c.release();s.release();assert n==6948
metrics={k:{'frames':len(v),'mean_thumbnail_error':float(np.mean(v)),'max_thumbnail_error':float(max(v))} for k,v in stats.items()}
assert all(v['max_thumbnail_error']<4 for v in metrics.values()),metrics
sheet=Image.new('RGB',(1280,5*390),'white');d=ImageDraw.Draw(sheet)
for i,(frame,im) in enumerate(sorted(samples.items())):
 x=(i%2)*640;y=(i//2)*390;sheet.paste(Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)).resize((640,360)),(x,y));d.text((x+8,y+365),f'output frame {frame} / {frame/30:.3f}s',fill='black')
sheet.save(O/'boundary-and-ring-check.jpg')
# Export exact frame-based preview, including both voice joins.
subprocess.run([FF,'-v','error','-y','-i',str(R/M['candidate']),'-vf','trim=start_frame=4980:end_frame=6075,setpts=PTS-STARTPTS','-af','atrim=start=166:end=202.5,asetpts=PTS-STARTPTS','-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',str(O/'replacement-preview.mp4')],check=True)
r=subprocess.run([FF,'-v','error','-i',str(R/M['candidate']),'-f','null','-'],capture_output=True,text=True,check=True);assert not r.stderr.strip(),r.stderr
subprocess.run([FF,'-v','error','-y','-i',str(R/M['candidate']),'-ss','174','-t','21.6','-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(O/'final-pickup.wav')],check=True)
r=subprocess.run([FF,'-hide_banner','-i',str(O/'final-pickup.wav'),'-af','silencedetect=noise=-35dB:d=0.15,ebur128=peak=true','-f','null','-'],capture_output=True,text=True,check=True);(O/'final-audio-analysis.txt').write_text(r.stderr)
for p,h in M['protected_sources'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
qa={'frame_count':n,'decode_errors':False,'unchanged_video_comparison':metrics,'protected_source_hashes_unchanged':True,'output_length_seconds':n/30,'preview':[166,202.5],'listening':'Pending owner review; no subjective voice-match claim.'};(O/'qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps(qa,indent=2));print(r.stderr[r.stderr.rfind('Summary:'):].split('[out#')[0])
