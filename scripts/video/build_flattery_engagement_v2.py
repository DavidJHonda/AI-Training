#!/usr/bin/env python3
"""Apply the owner's approved repetition cuts directly to stable source videos."""
from pathlib import Path
import json,subprocess
import cv2,numpy as np,imageio_ffmpeg
from build_flattery_engagement_v1 import ROOT,SOURCES,FPS,SR,SPF,sha,close_frame
from make_close_board import close_board_asset,compose_canonical_for_video
OUT=ROOT/'video-audit/flattery-engagement-trim-v2-2026-11-02'
DEST=ROOT/'Prompts/flattery-engagement-v2.mp4'
V1_MAP=[('flattery',0,7661),('engagement',0,2900),('engagement',3764,4470),('flattery',7734,7809),('engagement',6876,7148)]
# Half-open v1 frame ranges; all endpoints measured in source silence.
CUTS=[(691,756,'Let’s look at a concrete example.'),
 (1510,1600,'That praise could apply to almost any Gatsby essay.'),
 (1880,2300,'This version is useful … Empty praise only improves how you feel in the moment.'),
 (2484,2622,'This diagram outlines why AI leans so heavily toward flattery.'),
 (4828,4928,'This table outlines ways to fight the flattery trap.'),
 (5181,5260,'Instead, hold back your verdict.'),
 (5402,5552,'A neutral question gives the AI less of your own confidence to reflect back at you.'),
 (6025,6140,'Now you have given the AI specific targets to locate.'),
 (6965,7168,'Each of these moves works because you are replacing a request for validation with a concrete standard for the AI to meet.'),
 (7557,7661,'Ask AI to improve the work, not approve of you.'),
 (7920,8197,'You fall into the trap … This comparison chart shows how easily that happens.'),
 (8440,8650,'Y2 minus Y1 over X2 minus X1. It is a perfectly efficient answer.'),
 (9498,9612,'Both answered the initial question, but only one ended there.'),
 (10005,10076,'This compares two design strategies.')]
# Early unmarked board arrivals preserve setup after removing spoken introductions.
REPAIRS=[dict(v1_frames=[4771,4828],source='flattery',source_frame=4920,reason='Introduce the full Three Ways board during the end of the mitigation bridge.'),
 dict(v1_frames=[7555,7557],source='flattery',source_frame=7554,reason='Avoid a two-frame zoom-out flash before Engagement.'),
 dict(v1_frames=[7866,7920],source='engagement',source_frame=489,reason='Introduce One Answer, Two Endings during the useful-help transition.'),
 dict(v1_frames=[9951,10005],source='engagement',source_frame=2409,reason='Introduce the full Infinite Scroll comparison under the end of its retained setup.'),
 dict(v1_frames=[10561,10563],source='engagement',source_frame=3766,reason='Preserve the v1 two-frame repair at the AI missing-page-break scene.')]

def timeline():
 original=[]
 for key,a,b in V1_MAP:original.extend((key,n) for n in range(a,b))
 keep=np.ones(len(original),dtype=bool)
 for a,b,_ in CUTS:keep[a:b]=False
 ids=np.flatnonzero(keep).tolist()
 segments=[]
 for v in ids:
  key,s=original[v]
  if segments and segments[-1]['source']==key and segments[-1]['source_frames'][1]==s and segments[-1]['v1_frames'][1]==v:
   segments[-1]['source_frames'][1]+=1;segments[-1]['v1_frames'][1]+=1;segments[-1]['output_frames'][1]+=1
  else:
   o=sum(x['output_frames'][1]-x['output_frames'][0] for x in segments)
   segments.append(dict(source=key,source_frames=[s,s+1],v1_frames=[v,v+1],output_frames=[o,o+1]))
 return ids,segments

def main():
 assert not DEST.exists(),'Never overwrite a review candidate.'
 OUT.mkdir(exist_ok=True)
 old=json.loads((ROOT/'video-audit/flattery-engagement-merge-2026-11-02/edit-manifest.json').read_text())
 protected={p:sha(p) for p in old['protected']}
 for p,h in SOURCES.values():assert sha(p)==h
 ids,segs=timeline();total=len(ids)
 ff=imageio_ffmpeg.get_ffmpeg_exe();pcm={}
 for k,(p,_) in SOURCES.items():pcm[k]=np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(p),'-vn','-ac','1','-ar',str(SR),'-f','f32le','pipe:1']),'<f4')
 edited=np.concatenate([pcm[s['source']][s['source_frames'][0]*SPF:s['source_frames'][1]*SPF] for s in segs]);joins=[]
 ramp=np.linspace(0,1,480,dtype=np.float32)
 for s in segs[1:]:
  j=s['output_frames'][0];pos=j*SPF;left=edited[pos-480:pos].copy();right=edited[pos:pos+480].copy()
  levels=[float(20*np.log10(np.sqrt(np.mean(x*x))+1e-12)) for x in [left,right]]
  assert max(levels)<-45,(j,levels)
  edited[pos-240:pos+240]=left*(1-ramp)+right*ramp
  joins.append(dict(frame=j,seconds=j/FPS,left_rms_dbfs=levels[0],right_rms_dbfs=levels[1]))
 subprocess.run([ff,'-y','-v','error','-f','f32le','-ar',str(SR),'-ac','1','-i','pipe:0','-c:a','pcm_f32le',str(OUT/'edited.wav')],input=edited.astype('<f4').tobytes(),check=True)
 compose_canonical_for_video(close_board_asset('flattery'),OUT/'canvas-close.png','#ffffff');canvas=cv2.imread(str(OUT/'canvas-close.png'))
 close_start=ids.index(11267);eng_start=ids.index(7661)
 boundaries=[dict(frame=s['output_frames'][0],label=f'join-{i:02d}') for i,s in enumerate(segs[1:],1)]
 for i,r in enumerate(REPAIRS):
  for v in r['v1_frames']:
   if v in ids:boundaries.append(dict(frame=ids.index(v),label=f'picture-{i}-{v}'))
 boundaries=list({b['frame']:b for b in boundaries}.values())
 m=dict(candidate=str(DEST),scope='Approved repetition cuts; review candidate only.',authorization='Keep the 1:49–1:52 baked-in line; apply other proposed cuts and preserve a transition to Engagement.',
  sources={k:dict(path=str(p),sha256=h) for k,(p,h) in SOURCES.items()},source_limitation='Rebuilt directly from finished original v13/v15 sources; raw generations unavailable.',
  fps=FPS,frames=total,duration_seconds=total/FPS,v1_duration_seconds=11614/FPS,removed_seconds=(11614-total)/FPS,
  cuts=[dict(v1_frames=[a,b],v1_seconds=[a/FPS,b/FPS],text=t) for a,b,t in CUTS],preserved_exception='The praise literally gets baked into the system.',
  segments=segs,picture_repairs=REPAIRS,boundaries=boundaries,audio_joins=joins,added_pause_seconds=0,level_changes_db=0,
  bridge=dict(start_frame=eng_start,start_seconds=eng_start/FPS,text='The engagement trap feels like a helpful conversation that keeps going. This extra help may be useful, which makes it easy to accept.',source='Existing original Engagement narration, unchanged.'),
  close=dict(start_frame=close_start,frames=total-close_start,asset=str(close_board_asset('flattery')),sha256=sha(close_board_asset('flattery')),motion='Identical v1 closing: 48-frame hold; 150-frame push; settled hold.'),
  protected=protected,perceptual_listening=False,continuous_motion_playback=False,installed=False,published=False)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 # Decode source frames sequentially. Cache only selected donor stills.
 donors={}
 for r in REPAIRS:
  key=(r['source'],r['source_frame'])
  if key in donors:continue
  cap=cv2.VideoCapture(str(SOURCES[key[0]][0]));cap.set(cv2.CAP_PROP_POS_FRAMES,key[1]);ok,f=cap.read();assert ok;cap.release();donors[key]=f
 cv2.setNumThreads(2)
 proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-video_track_timescale','15360',str(DEST)],stdin=subprocess.PIPE)
 nout=0;caps={};positions={}
 try:
  for s in segs:
   key=s['source'];a,b=s['source_frames']
   if s['output_frames'][0]>=close_start:
    for _ in range(b-a):proc.stdin.write(close_frame(canvas,nout-close_start).tobytes());nout+=1
    continue
   if key not in caps or positions[key]>a:
    if key in caps:caps[key].release()
    caps[key]=cv2.VideoCapture(str(SOURCES[key][0]));positions[key]=0
   cap=caps[key]
   while positions[key]<b:
    sn=positions[key];ok,f=cap.read();assert ok;positions[key]+=1
    if sn<a:continue
    v=s['v1_frames'][0]+sn-a
    for r in REPAIRS:
     if r['v1_frames'][0]<=v<r['v1_frames'][1]:f=donors[(r['source'],r['source_frame'])];break
    proc.stdin.write(f.tobytes());nout+=1
    if nout%1500==0:print(f'Rendered {nout}/{total}',flush=True)
 finally:
  proc.stdin.close()
  for c in caps.values():c.release()
 assert proc.wait()==0 and nout==total
 assert all(sha(p)==h for p,h in protected.items())
 m['candidate_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print(json.dumps(dict(candidate=str(DEST),duration=total/FPS,removed_seconds=m['removed_seconds'],transition_seconds=eng_start/FPS)),flush=True)
if __name__=='__main__':main()
