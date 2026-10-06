#!/usr/bin/env python3
"""Approved guided-demo repair; reconstruct retained picture from original sources."""
from pathlib import Path
import json, subprocess
import cv2, numpy as np, imageio_ffmpeg
import build_how_ai_answers_v11 as prior
from editspec_build import sha

ROOT=prior.ROOT
OUT=ROOT/'video-audit/how-ai-answers-guided-2026-10-06-v12'
DEST=ROOT/'Prompts/how-ai-answers-v12.mp4'
BASE=ROOT/'Prompts/how-ai-answers-v11.mp4'
# Half-open frame intervals on the accepted v11 timeline, refined from PCM.
CUTS=[(3214,3238),(3770,3828),(4167,4198),(4619,4648)]
PHRASES=['on the left','Following the arrow to the right','in the top right','Down below']
REPLACE=(3106,5069)
BEATS=[(3106,0),(3172,1),(3719,2),(3833,3),(4012,4),(4029,5),
       (4039,6),(4050,7),(4060,8),(4117,9),(4871,10),(4919,11),(4992,12)]

def frames():
 return [f for f in range(6590) if not any(a<=f<b for a,b in CUTS)]

def main():
 assert not DEST.exists(),'Never overwrite a review candidate'
 OUT.mkdir(exist_ok=True);rebuild=OUT/'reconstruction';rebuild.mkdir(exist_ok=True)
 accepted=json.loads((ROOT/'video-audit/how-ai-answers-repair-2026-09-29-v11/edit-manifest.json').read_text())
 assert sha(BASE)==accepted['candidate_sha256']
 for name,h in accepted['protected'].items():
  if name.endswith('.jpg'):assert sha(Path(name))==h, name
 protected={str(p):sha(p) for p in [BASE,ROOT/'course-assets/how-ai-answers/how-ai-answers.mp4',*sorted((ROOT/'course-assets/how-ai-answers').glob('*.jpg'))]}
 # All earlier preparation writes are redirected into this candidate's own folder.
 prior.OUT=rebuild;prior.DEST=DEST
 source,base_frame,previous,refs=prior.setup()
 protected[str(source)]=sha(source)
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 raw=np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(source),'-vn','-ar','48000','-ac','2','-f','f32le','pipe:1']),np.float32).reshape(-1,2)
 source_spans=[(0,3108),(330,391),(3108,6221),(7309,7617)]
 parts=[raw[a*1600:b*1600].copy() for a,b in source_spans]
 def fades(parts):
  for i,p in enumerate(parts):
   if i:p[:240]*=np.linspace(0,1,240,dtype=np.float32)[:,None]
   if i<len(parts)-1:p[-240:]*=np.linspace(1,0,240,dtype=np.float32)[:,None]
  return np.concatenate(parts)
 base_audio=fades(parts);assert len(base_audio)==6590*1600
 keep=[];last=0
 for a,b in CUTS:keep.append((last,a));last=b
 keep.append((last,6590))
 audio=fades([base_audio[a*1600:b*1600].copy() for a,b in keep])
 audio.tofile(OUT/'edited-audio.f32')
 mapping=frames();reverse={f:i for i,f in enumerate(mapping)}
 states={s:cv2.imread(str(OUT/'states'/f'state-{s}.png')) for _,s in BEATS}
 assert all(im is not None and im.shape==(720,1280,3) for im in states.values())
 boundaries={reverse[x] for x in previous['boundaries'] if x in reverse and not REPLACE[0]<=x<REPLACE[1]}
 boundaries.update(reverse[x] for x,_ in BEATS)
 boundaries.update(reverse[b] for _,b in CUTS)
 boundaries.add(reverse[REPLACE[1]])
 manifest=dict(candidate=str(DEST),based_on=str(BASE),base_sha256=sha(BASE),source=str(source),source_sha256=sha(source),
  fps=30,frames=len(mapping),duration=len(mapping)/30,keep_v11_frames=keep,
  cuts=[dict(words=p,base_frames=[a,b],base_seconds=[a/30,b/30],output_join_frame=reverse[b]) for p,(a,b) in zip(PHRASES,CUTS)],
  source_audio_spans_frames=source_spans,fade_samples=240,added_pauses=0,
  replaced_v11_frames=list(REPLACE),replacement_output_frames=[reverse[REPLACE[0]],reverse[REPLACE[1]]],
  scene_beats=[dict(state=s,base_frame=f,output_frame=reverse[f],output_seconds=reverse[f]/30) for f,s in BEATS],
  camera='Fixed full scene, 1.25x shared component capture. Question retained above reply. Selected row has fixed 4px delivery border.',
  visual_treatment='Replace old token-by-token board and intermediate-token cutaway only; preserve dog illustration, EOS drawing, opening and closing treatment.',
  boundaries=sorted(boundaries),protected=protected,lesson_source_sha256=sha(ROOT/'index.html'),
  scene_capture_sha256={str(OUT/'states'/f'state-{s}.png'):sha(OUT/'states'/f'state-{s}.png') for s in states},
  approval='David: Build it please. Approved four directional narration trims and shared interactive chart/reply synchronized to existing narration. Review candidate only.',
  listening_performed=False)
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
  '-f','f32le','-ar','48000','-ac','2','-i',str(OUT/'edited-audio.f32'),'-map','0:v:0','-map','1:a:0',
  '-c:v','libx264','-threads','4','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 reader=prior.Reader(source)
 for n,f in enumerate(mapping):
  if REPLACE[0]<=f<REPLACE[1]:
   state=next(s for start,s in reversed(BEATS) if start<=f);im=states[state]
  else:
   im=base_frame(f,reader)
   if prior.DOG[0]<=f<prior.DOG[1]:im,_=prior.dog(im)
   if prior.EOS[0]<=f<prior.EOS[1]:im,_=prior.brighten(im,refs)
  proc.stdin.write(im.tobytes())
  if n%1000==999:print('Rendered',n+1,'/',len(mapping),flush=True)
 proc.stdin.close();assert proc.wait()==0;reader.c.release()
 assert all(sha(Path(p))==h for p,h in protected.items())
 manifest['candidate_sha256']=sha(DEST)
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(str(DEST),flush=True)

if __name__=='__main__':main()
