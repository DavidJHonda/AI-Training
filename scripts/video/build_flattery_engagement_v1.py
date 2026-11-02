#!/usr/bin/env python3
"""Merge the two approved installed videos into a review-only lesson candidate."""
from pathlib import Path
import hashlib,json,subprocess
import cv2,imageio_ffmpeg,numpy as np
from make_close_board import close_board_asset,close_board_copy,compose_canonical_for_video
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/flattery-engagement-merge-2026-11-02'
DEST=ROOT/'Prompts/flattery-engagement-v1.mp4'
FPS,SR,SPF=30,48000,1600
SOURCES={
 'flattery':(ROOT/'Prompts/flattery-trap-v13.mp4','ffec02f6916c47d6226324894af8731a76a1c884cfc9d0922843dbb006bb7031'),
 'engagement':(ROOT/'Prompts/engagement-trap-v15.mp4','2dc69c8a233762e5b6272111432f362d05450bec0931a7ee69adcca388b90a15')}
# Half-open source frames, measured against audio RMS and picture cuts.
RANGES=[('flattery',0,7661,'Flattery teaching through improve the work'),
 ('engagement',0,2900,'Engagement introduction, slope comparison, infinite scroll'),
 ('engagement',3764,4470,'AI missing page break and commercial incentives'),
 ('flattery',7734,7809,'Look for specifics, not approval'),
 ('engagement',6876,7148,'Know what you came for; choose what happens next')]

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def close_frame(canvas,n):
 # House motion: 48 frames still, 150-frame push, then hold at 1.2x.
 z=1+.2*min(1,max(0,(n-48)/150))
 h,w=canvas.shape[:2];scale=1280/w*z
 return cv2.warpAffine(canvas,np.array([[scale,0,640-w/2*scale],[0,scale,360-h/2*scale]]),
  (1280,720),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=(255,255,255))

def main():
 assert not DEST.exists(),'Never overwrite a review candidate.'
 OUT.mkdir(exist_ok=True)
 for key,(p,h) in SOURCES.items():
  assert sha(p)==h
  assert sha(ROOT/f'course-assets/{key}-trap/{key}-trap.mp4')==h
 assets=[ROOT/'index.html',ROOT/'lessons/flattery-trap.md',ROOT/'course-assets/manifest.json']
 assets += list((ROOT/'course-assets/flattery-trap').glob('*.jpg'))+list((ROOT/'course-assets/engagement-trap').glob('*.jpg'))
 protected={str(p):sha(p) for p in assets}
 ff=imageio_ffmpeg.get_ffmpeg_exe(); pcm={}
 for key,(p,h) in SOURCES.items():
  raw=subprocess.check_output([ff,'-v','error','-i',str(p),'-vn','-ac','1','-ar',str(SR),'-f','f32le','pipe:1'])
  pcm[key]=np.frombuffer(raw,'<f4').copy()
 edited=np.concatenate([pcm[key][a*SPF:b*SPF] for key,a,b,_ in RANGES])
 segments=[];cursor=0
 for key,a,b,label in RANGES:
  segments.append(dict(source=key,source_frames=[a,b],source_seconds=[a/FPS,b/FPS],output_frames=[cursor,cursor+b-a],output_seconds=[cursor/FPS,(cursor+b-a)/FPS],label=label))
  cursor+=b-a
 assert cursor==11614 and len(edited)==cursor*SPF
 joins=[s['output_frames'][0] for s in segments[1:]]
 # A 10ms crossfade of the two quiet shoulders, preserving every sample's position
 # and total duration. There are no added pauses, global level changes, or new speech.
 ramp=np.linspace(0,1,480,dtype=np.float32); stats=[]
 for j in joins:
  pos=j*SPF;left=edited[pos-480:pos].copy();right=edited[pos:pos+480].copy()
  assert max(np.sqrt(np.mean(left**2)),np.sqrt(np.mean(right**2))) < .004
  bridge=left*(1-ramp)+right*ramp
  edited[pos-240:pos+240]=bridge
  stats.append(dict(frame=j,seconds=j/FPS,left_rms_dbfs=float(20*np.log10(np.sqrt(np.mean(left**2))+1e-12)),right_rms_dbfs=float(20*np.log10(np.sqrt(np.mean(right**2))+1e-12))))
 subprocess.run([ff,'-y','-v','error','-f','f32le','-ar',str(SR),'-ac','1','-i','pipe:0','-c:a','pcm_f32le',str(OUT/'edited.wav')],input=edited.astype('<f4').tobytes(),check=True)
 compose_canonical_for_video(close_board_asset('flattery'),OUT/'canvas-close.png','#ffffff')
 canvas=cv2.imread(str(OUT/'canvas-close.png'))
 close_start=segments[3]['output_frames'][0]
 boundaries=[dict(frame=s['output_frames'][0],label=l) for s,l in zip(segments[1:],['flattery-to-engagement','scroll-to-ai-bridge','merged-close-in','closing-audio-handoff'])]
 manifest=dict(candidate=str(DEST),scope='Review-only merge using existing installed narration and imagery; no installation or publishing.',
  authorization='User: OK. Do you want to try and build the video from the current live videos?',
  sources={k:dict(path=str(v[0]),sha256=v[1]) for k,v in SOURCES.items()},
  source_limitation='Finished v13/v15 are the available stable sources, verified byte-identical to installed MP4s. Retained pictures and audio receive one encode.',
  fps=FPS,frames=cursor,duration_seconds=cursor/FPS,original_combined_duration_seconds=(7954+7148)/FPS,
  segments=segments,boundaries=boundaries,audio_joins=stats,added_pause_seconds=0,level_changes_db=0,
  close=dict(start_frame=close_start,frames=cursor-close_start,asset=str(close_board_asset('flattery')),sha256=sha(close_board_asset('flattery')),copy=close_board_copy('flattery'),motion='48-frame hold; 150-frame linear push to 1.2x; settled hold to literal final frame'),
  picture_repairs=[dict(output_frames=[10561,10563],source='engagement',source_frame=3766,reason='Cover two preceding phone frames before the AI-chat scene; audio cut is in silence before the picture cut.')],
  bridge='Existing Engagement opening retained as the spoken transition; the newly written transition has no recorded donor.',
  preserved='Six teaching boards with approved camera/ring treatments, all original retained animations, three feedback tactics and saved instruction.',
  removed='Separate Flattery closing, Raskin regret/lifetimes/autoplay/streak detour, Meta settlement/stopping-points section, social-media conclusion.',
  protected=protected,perceptual_listening=False,continuous_motion_playback=False,installed=False,published=False)
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 cv2.setNumThreads(2)
 proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-video_track_timescale','15360',str(DEST)],stdin=subprocess.PIPE)
 nout=0
 try:
  for seg in segments[:3]:
   cap=cv2.VideoCapture(str(SOURCES[seg['source']][0]));a,b=seg['source_frames']
   # Sequentially decode from the start, avoiding inaccurate time seeks.
   hold=None
   if seg is segments[2]:
    donor=cv2.VideoCapture(str(SOURCES['engagement'][0]));donor.set(cv2.CAP_PROP_POS_FRAMES,3766);ok,hold=donor.read();assert ok;donor.release()
   for n in range(b):
    ok,frame=cap.read();assert ok,(seg,n)
    if n<a:continue
    if seg is segments[2] and n<3766:frame=hold
    proc.stdin.write(frame.tobytes());nout+=1
    if nout%1500==0:print(f'Rendered {nout}/{cursor}',flush=True)
   cap.release()
  for n in range(cursor-close_start):
   proc.stdin.write(close_frame(canvas,n).tobytes());nout+=1
 finally:proc.stdin.close()
 assert proc.wait()==0 and nout==cursor
 assert all(sha(p)==h for p,h in protected.items())
 assert all(sha(p)==h for p,h in SOURCES.values())
 manifest['candidate_sha256']=sha(DEST)
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps(dict(candidate=str(DEST),frames=nout,duration=nout/FPS,sha256=manifest['candidate_sha256'])),flush=True)
if __name__=='__main__':main()
