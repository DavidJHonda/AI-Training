#!/usr/bin/env python3
"""Narrow, hash-pinned removal of five retired opener declarations.

Render new review candidates; never overwrite course videos or existing candidates.
Retained frames are decoded from the current approved finished edits, then encoded
once. Original generation assemblies are not reconstructed for this narrow repair.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image,ImageOps

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/opener-blue-board-cuts-2026-10-27'
FF=imageio_ffmpeg.get_ffmpeg_exe()
FPS=30; SR=48000; SPF=SR//FPS
SOURCES={x['slug']:x for x in json.loads((OUT/'sources.json').read_text())}
PLANS={
 'work-with-ai-opener':dict(version=12,channels=1,blue_end=577,spans=[(569,4096)],
  removed='Opening board commentary, from “Take a look at these four principles” through “which AI scales up and amplifies.”',
  retained='Aiming/details and verification remain in the section map; thinking/multiplication remains in the close.'),
 'understand-ai-opener':dict(version=15,channels=1,blue_end=352,spans=[(345,894),(3,175),(915,4381)],
  inserts={1:dict(hold_frame=893)},
  removed='Opening declaration presentation and “It is entirely its own kind of thing, operating by a completely different set of rules.”',
  retained='Move “It’s not magic, it’s not a person, and it’s definitely not normal software” after the expert/mistake question; hold the existing comparison drawing.'),
 'avoid-traps-opener':dict(version=10,channels=1,blue_end=393,spans=[(389,6458)],
  removed='Opening declaration through “every trap looks completely fine from the inside.”',
  retained='Confident false facts, human susceptibility to agreeableness, convincing fakes, and hidden failure are explained in the retained narration and map.'),
 'embrace-the-future-opener':dict(version=7,channels=2,blue_end=307,spans=[(303,5919)],
  replace=(1062,1291),asset='course-assets/embrace-the-future-opener/embrace-the-future-opener-edge-of-the-map.jpg',
  removed='Initial four speculative quotes and “Who’s right? Nobody knows.”',
  retained='Optimist, worrier, and uncertainty remain at source 35.4–50 s. Replace the board reprise at 35.4–43.033 s with the canonical map illustration, full view, unmarked, stationary.'),
 'build-your-skills-opener':dict(version=6,channels=1,blue_end=473,spans=[(466,2173),(184,359),(2206,4928)],
  inserts={1:dict(video_start=480)},
  removed='“Look at this board” / what makes you valuable preamble and “Together, these mean you’ll always be smarter than the tool.”',
  retained='Move “Your choices and the questions you ask, your judgment, and the permanent skills you bring” after the enduring-human-skills sentence, over the existing student writing scene.'),
}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def frame_at(cap,f):
 cap.set(cv2.CAP_PROP_POS_FRAMES,f);ok,img=cap.read();assert ok,f;return img

def build(slug):
 plan=PLANS[slug];src=Path(SOURCES[slug]['source']);assert sha(src)==SOURCES[slug]['sha256']
 dest=ROOT/'Prompts'/f'{slug}-v{plan["version"]}.mp4';assert not dest.exists(),dest
 work=OUT/slug;work.mkdir(parents=True,exist_ok=True)
 raw=subprocess.check_output([FF,'-v','error','-i',str(src),'-vn','-ar',str(SR),'-ac',str(plan['channels']),'-f','f32le','-'])
 audio=np.frombuffer(raw,dtype='<f4').reshape(-1,plan['channels'])
 total=sum(b-a for a,b in plan['spans']);parts=[];boundaries=[];timeline=[];cursor=0
 for k,(a,b) in enumerate(plan['spans']):
  part=audio[a*SPF:b*SPF].copy();assert len(part)==(b-a)*SPF
  # Only 5 ms within measured silent handles. No speech-level normalization.
  fade=SR//200
  if k==0:part[:fade]*=np.linspace(0,1,fade)[:,None]
  if k>0:
   parts[-1][-fade:]*=np.linspace(1,0,fade)[:,None]
   part[:fade]*=np.linspace(0,1,fade)[:,None]
   boundaries.append(dict(frame=cursor,label='narration-move-'+str(k)))
  parts.append(part);timeline.append(dict(output_frames=[cursor,cursor+b-a],source_frames=[a,b],source_seconds=[a/FPS,b/FPS],visual_override=plan.get('inserts',{}).get(k)))
  cursor+=b-a
 edited=np.concatenate(parts);audiofile=work/'edited-audio.f32';edited.tofile(audiofile)
 if 'replace' in plan:
  a,b=plan['replace'];start=plan['spans'][0][0]
  boundaries.extend([dict(frame=a-start,label='map-illustration-in'),dict(frame=b-start,label='map-illustration-out')])
 manifest=dict(slug=slug,scope=plan.get('scope','User-authorized narrow removal of opening blue boards, preserving analogies and essential narration.'),
  authorization=plan.get('authorization','Let’s cut the blue boards from the 5 middle-section openers, but keep the analogies and fold any essential points into the narration. Update the videos, please.'),
  source=str(src),source_sha256=sha(src),candidate=str(dest),source_frames=SOURCES[slug]['frames'],output_frames=total,
  fps=FPS,duration=total/FPS,saved_seconds=(SOURCES[slug]['frames']-total)/FPS,channels=plan['channels'],sample_rate=SR,
  removed=plan['removed'],retained=plan['retained'],timeline=timeline,boundaries=boundaries,
  clean_heads=plan.get('clean_heads',{}),
  opening_visual='Hold first clean post-board frame only until the source catches up; audio starts in preceding silence.',
  pauses='No new pause. Existing sentence-end silence divided around retained lines; 5 ms edge fades inside quiet handles.',
  board_plan=plan.get('board_plan','All five opening declaration boards removed completely. Other map/highlight/camera/closing treatments preserved. Embrace reprise uses existing canonical analogy illustration without rings or motion.'),
  limitations=['Finished approved MP4s used as sources; retained video/audio encoded once.', 'No direct listening or continuous end-to-end playback claimed.', 'Review candidates only; no installation, commit, or public deployment.'])
 if 'asset' in plan:manifest.update(asset=plan['asset'],asset_sha256=sha(ROOT/plan['asset']))
 (work/'edit-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
 cap=cv2.VideoCapture(str(src));first=frame_at(cap,plan['blue_end']);asset=None
 if 'asset' in plan:
  im=Image.open(ROOT/plan['asset']).convert('RGB');im=ImageOps.contain(im,(1280,720),Image.Resampling.LANCZOS)
  canvas=Image.new('RGB',(1280,720),'#f6f5fb');canvas.paste(im,((1280-im.width)//2,(720-im.height)//2));asset=cv2.cvtColor(np.asarray(canvas),cv2.COLOR_RGB2BGR)
 command=[FF,'-n','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r',str(FPS),'-i','pipe:0','-f','f32le','-ar',str(SR),'-ac',str(plan['channels']),'-i',str(audiofile),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','2','-crf','16','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(dest)]
 process=subprocess.Popen(command,stdin=subprocess.PIPE)
 try:
  for k,(a,b) in enumerate(plan['spans']):
   special=plan.get('inserts',{}).get(k,{});hold=frame_at(cap,special['hold_frame']) if 'hold_frame' in special else None
   clean_at=plan.get('clean_heads',{}).get(k)
   clean_frame=frame_at(cap,clean_at) if clean_at is not None else None
   vstart=special.get('video_start',a)
   if hold is None:cap.set(cv2.CAP_PROP_POS_FRAMES,vstart)
   for j in range(b-a):
    if hold is not None:frame=hold
    else:
     ok,frame=cap.read();assert ok,(slug,k,j)
     source_frame=vstart+j
     if k==0 and source_frame<plan['blue_end']:frame=first
     if clean_at is not None and source_frame<clean_at:frame=clean_frame
     if 'replace' in plan and plan['replace'][0]<=source_frame<plan['replace'][1]:frame=asset
    process.stdin.write(frame.tobytes())
 finally:
  process.stdin.close();cap.release()
 assert process.wait()==0,slug
 manifest['candidate_sha256']=sha(dest);(work/'edit-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
 print(f'{slug}: {total/FPS:.3f}s, saved {manifest["saved_seconds"]:.3f}s -> {dest.name}',flush=True)
 return manifest

if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(build,PLANS))
 (OUT/'edit-manifest.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
