#!/usr/bin/env python3
"""Approved narrow review edit: shorter opening, word repair, two story callbacks."""
from pathlib import Path
import hashlib,json,shutil,subprocess,wave
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/critical-thinking-v14-2026-09-27'
DEST=ROOT/'Prompts/critical-thinking-v14.mp4'
LIVE=ROOT/'course-assets/critical-thinking/critical-thinking.mp4'
EXPECTED='fc07ea211e70f7e499b2546ba30cc90ab550f0e298625a0c55c800f70c7c1016'
SNAP=Path('/private/tmp/critical-thinking-v14-source-fc07ea211e70.mp4')
REPAIR=ROOT/'video-audit/critical-thinking-word-repair-2026-09-26'
FPS=30; SR=48000; SPF=1600; SOURCE_FRAMES=5935; DROP=360; INSERT_AT=4715; EXTRA=18
CALLBACKS=[
 {'name':'Flawed Design during evidence checking','start':4128,'end':4282,'donor':2319},
 {'name':'Chocolate headline during Why am I convinced','start':4796,'end':4976,'donor':1420},
]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd):subprocess.run(cmd,check=True)
def load_wav(p):
 with wave.open(str(p)) as w:
  assert w.getframerate()==SR and w.getnchannels()==1 and w.getsampwidth()==2
  return np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').copy()
def save_wav(p,x):
 with wave.open(str(p),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(x.astype('<i2').tobytes())
def mapped(frame):return frame-DROP+(EXTRA if frame>=INSERT_AT else 0)

def main():
 assert sha(LIVE)==EXPECTED,'Source changed; inspect the new live file before building.'
 assert not DEST.exists(),'Do not overwrite an existing review candidate.'
 OUT.mkdir(parents=True,exist_ok=True)
 protected={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'index.html',*sorted((ROOT/'course-assets/critical-thinking').glob('*'))] if p.is_file()}
 (OUT/'protected-before.json').write_text(json.dumps(protected,indent=2)+'\n')
 if not SNAP.exists():shutil.copyfile(LIVE,SNAP)
 assert sha(SNAP)==EXPECTED
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 run([ff,'-v','error','-y','-i',str(SNAP),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(OUT/'source.wav')])
 x=load_wav(OUT/'source.wav');approved_source=load_wav(REPAIR/'source-pcm16.wav')
 assert np.array_equal(x,approved_source),'Approved repair must match the exact source audio.'
 repaired=load_wav(REPAIR/'habit-three-repaired-review.wav');assert len(repaired)==604800
 if len(x)<SOURCE_FRAMES*SPF:raise AssertionError('Source audio shorter than planned video')
 audio=np.concatenate([x[DROP*SPF:4500*SPF],repaired,x[4860*SPF:SOURCE_FRAMES*SPF]])
 total=SOURCE_FRAMES-DROP+EXTRA
 assert len(audio)==total*SPF
 save_wav(OUT/'edited.wav',audio)
 # Cache only the selected drawing frames, sequentially decoded and PNG-compressed.
 needed=set()
 for c in CALLBACKS:needed.update(range(c['donor'],c['donor']+c['end']-c['start']))
 cache={};cap=cv2.VideoCapture(str(SNAP));f=0
 while f<=max(needed):
  ok,frame=cap.read();assert ok
  if f in needed:
   ok,png=cv2.imencode('.png',frame,[cv2.IMWRITE_PNG_COMPRESSION,1]);assert ok;cache[f]=png
  f+=1
 cap.release();assert len(cache)==len(needed)
 picture=OUT/'picture.mp4'
 proc=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','-',
  '-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p',str(picture)],stdin=subprocess.PIPE)
 cap=cv2.VideoCapture(str(SNAP));frame_map=[];written=0;f=0
 while True:
  ok,frame=cap.read()
  if not ok:break
  if f>=DROP:
   actual=f;kind='source'
   for c in CALLBACKS:
    if c['start']<=f<c['end']:
     actual=c['donor']+f-c['start'];frame=cv2.imdecode(cache[actual],cv2.IMREAD_COLOR);kind=c['name'];break
   proc.stdin.write(frame.tobytes());frame_map.append(actual);written+=1
   if f==INSERT_AT-1:
    for _ in range(EXTRA):proc.stdin.write(frame.tobytes());frame_map.append(actual);written+=1
  f+=1
 cap.release();proc.stdin.close();assert proc.wait()==0
 assert f==SOURCE_FRAMES and written==total,(f,written,total)
 np.save(OUT/'source-frame-map.npy',np.array(frame_map,dtype=np.int32))
 # Preserve the earlier whistle fix's AAC encoder settings. New audio is encoded once.
 run([ff,'-v','error','-y','-i',str(picture),'-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a',
  '-c:v','copy','-c:a','aac','-b:a','256k','-aac_pns','0','-aac_tns','0','-movflags','+faststart',str(DEST)])
 boundaries=[]
 for f,label in [(1417,'equation-to-newspaper'),(1659,'newspaper-to-headline'),(1710,'headline-to-reactions'),
  (2315,'reactions-to-study'),(2514,'study-to-data-diagram'),(3057,'data-to-website'),
  (3828,'drawings-to-habits'),(4708,'word-replacement-start'),(4715,'word-hold-end'),
  (5441,'habits-to-AI-diagram'),(5674,'diagram-to-close')]:boundaries.append({'frame':mapped(f),'label':label})
 # Freeze begins before the insertion mapping advances.
 boundaries.append({'frame':INSERT_AT-DROP,'label':'word-hold-start'})
 for c in CALLBACKS:
  for k in ['start','end']:boundaries.append({'frame':mapped(c[k]),'label':c['name']+'-'+k})
 boundaries=sorted(boundaries,key=lambda b:b['frame'])
 boards=[
  {'name':'What You Know. How You Think.','source':[0,1417],'output':[[0,mapped(1417)]]},
  {'name':'Same Claim. Different Thinking.','source':[1710,2315],'output':[[mapped(1710),mapped(2315)]]},
  {'name':'Five Habits of Critical Thinking','source':[3828,5441],'output':[[mapped(3828),mapped(4128)],[mapped(4282),mapped(4796)],[mapped(4976),mapped(5441)]]},
  {'name':'Closing message','source':[5674,5935],'output':[[mapped(5674),total]]},
 ]
 for b in boards:
  b['before_seconds']=(b['source'][1]-b['source'][0])/FPS
  b['after_appearances_seconds']=[(end-start)/FPS for start,end in b['output']]
 record={'source':str(SNAP),'source_sha256':EXPECTED,'output':str(DEST),'output_sha256':sha(DEST),
  'fps':FPS,'source_frames':SOURCE_FRAMES,'total_frames':total,'duration_seconds':total/FPS,
  'opening_removed_seconds':[0,12],'opening_new_first_words':'Look at the left side. Knowledge forms your baseline.',
  'approved_word_repair':{'recipe':str(REPAIR/'build_preview.py'),'pcm_sha256':sha(REPAIR/'habit-three-repaired-review.wav'),'added_frames':EXTRA,'owner_audition':'Approved join before this build'},
  'callbacks':CALLBACKS,'boundaries':boundaries,'boards':boards,
  'visual_policy':'Preserve current source boards, rings and camera; insert original drawing footage only. No new rings rendered.',
  'scope':'Review candidate only; no live changes. Existing legacy ring widths retained in narrow edit.',
  'listening':'Approved word preview retained. New full candidate not directly listened to in this environment.'}
 for path,h in protected.items():assert sha(ROOT/path)==h,path
 (OUT/'edit-manifest.json').write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({'output':str(DEST),'frames':total,'seconds':total/FPS,'board_durations':boards},indent=2),flush=True)
if __name__=='__main__':main()
