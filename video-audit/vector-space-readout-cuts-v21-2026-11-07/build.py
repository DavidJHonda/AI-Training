"""Three approved readout cuts; native-source pictures and v20 narration."""
from pathlib import Path
import sys,json,subprocess,functools,math,hashlib
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import Build,Reader,fr,sha,readwav,writewav,rms
from gemini_mark import clean_frame,glyph_mask
from build_vector_space_v11 import opening
AUDIT=Path(__file__).resolve().parent
OUT=ROOT/'video-audit/vector-space-build-v18-2026-10-08'
DEST=ROOT/'Prompts/vector-space-v21.mp4'
BASE=ROOT/'Prompts/vector-space-v20.mp4'
LIVE=ROOT/'course-assets/vector-space/vector-space.mp4'
S8=ROOT/'Prompts/vector-space-8.mp4'
D=ROOT/'course-assets/vector-space'
FPS,SR,SPF=30,48000,1600
assert not DEST.exists(),'Never overwrite a review candidate'
assert sha(BASE)==sha(LIVE)=='8fe721214ddc4e279db50edcf5762e8bf205111c4398fb9b5a6e65be7459eb47'
protected=[BASE,LIVE,ROOT/'index.html',D/'vector-space-meaning-map.jpg',D/'vector-space-close.jpg',OUT/'build.py']
b=Build(ROOT,S8,AUDIT,DEST,protected=protected)
old=json.loads((OUT/'edit-manifest.json').read_text())
b.rows=old['timeline'];b.close_start=old['visual_sections']['close'][0];b.total=old['total_frames']
code=(OUT/'build.py').read_text()
native=code[code.index('def mf(t):'):code.index('\nboundaries=')]
exec(compile(native,str(OUT/'build.py')+':native','exec'),globals())
sentence_im=cv2.imread(str(ROOT/'video-audit/vector-space-context-review-2026-10-10/sentence-frame-v20.png'))
assert sentence_im.shape==(720,1280,3)
# Remove highlights whose narration is deleted. Keep IT and concluding highlights.
original_context_targets=list(ctx_targets)
ctx_targets=ctx_targets[3:]
cuts=[(3108,3426,'Pepsi coordinate readout'),(3642,3942,'Coffee coordinate readout'),(6831,7164,'IT before-and-after number readouts')]
base_total=7693
keeps=[];cursor=0;prev=0
for start,end,label_ in cuts:
 keeps.append(dict(source_start=prev,source_end=start,start_frame=cursor,end_frame=cursor+start-prev))
 cursor+=start-prev;prev=end
keeps.append(dict(source_start=prev,source_end=base_total,start_frame=cursor,end_frame=cursor+base_total-prev))
total=keeps[-1]['end_frame']
joins=[r['end_frame'] for r in keeps[:-1]]
def outframe(s):
 for r in keeps:
  if r['source_start']<=s<r['source_end']:return r['start_frame']+s-r['source_start']
 return None
source=readwav(AUDIT/'source.wav')
audio=np.concatenate([source[r['source_start']*SPF:r['source_end']*SPF] for r in keeps])
assert len(audio)==total*SPF
# Every boundary is inside measured quiet; interpolate only 5 ms each side.
seams=[]
for f in joins:
 s=f*SPF;n=240
 before=audio[s-n:s+n].copy()
 audio[s-n:s+n]=np.linspace(audio[s-n],audio[s+n-1],2*n)
 seams.append(dict(output_frame=f,output_seconds=f/FPS,original_rms_dbfs=20*math.log10(max(rms(before),1e-9)/32768),max_change=float(np.max(np.abs(audio[s-n:s+n]-before)))))
writewav(AUDIT/'assembled.wav',audio)
boundaries={f:label_ for f,(_,_,label_) in zip(joins,cuts)}
for row in old['boundaries']:
 n=row['frame'];s=n if n<6370 else n-6
 if row['label']=='Context focus' and n in [x[0] for x in original_context_targets[:3]]:continue
 q=outframe(s)
 if q and q<total-12:boundaries[q]=row['label']
for s,label_ in [(6188,'Lesson sentence card'),(6534,'Context board')]:
 q=outframe(s)
 if q:boundaries[q]=label_
manifest=dict(output=str(DEST),base=str(BASE),scope='Narrow repair: remove Pepsi, coffee, and IT number readouts only.',approval='User: Agree with those 3 cuts. Build it please.',fps=FPS,total_frames=total,duration=total/FPS,removed_frames=base_total-total,removed_seconds=(base_total-total)/FPS,cuts=[dict(source_frames=[s,e],source_seconds=[s/FPS,e/FPS],label=l) for s,e,l in cuts],timeline=keeps,seams=seams,boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],protected_hashes=b.hashes,picture_provenance=str(OUT/'build.py'),native_code_sha256=hashlib.sha256(native.encode()).hexdigest(),picture_treatment='Native-source reconstruction matching v20; remove the three number-specific context highlights with deleted narration; retain IT and conclusion highlights. All other camera, reveal and pause timing retained through cut mapping.',audio_treatment='Current v20 decoded narration, matching picture cuts, 5 ms quiet seam ramps, single AAC encode.',direct_listening=False,full_file_watch=False,installed=False)
(AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if '--prepare-only' in sys.argv:
 print(json.dumps(dict(duration=total/FPS,joins=joins,seams=seams,ctx_targets=ctx_targets),indent=2));sys.exit()
p=subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(AUDIT/'assembled.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
for row in keeps:
 for s in range(row['source_start'],row['source_end']):
  n=s if s<6370 else s+6
  p.stdin.write(frame(n).tobytes())
 print('Rendered through output frame',row['end_frame'],'/',total,flush=True)
p.stdin.close();assert p.wait()==0
assert all(sha(Path(k))==v for k,v in b.hashes.items())
manifest.update(output_sha256=sha(DEST),protected_files_unchanged=True)
(AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Finished',DEST,flush=True)
