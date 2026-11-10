#!/usr/bin/env python3
"""Review-only v15: approved version-4 cuts, complete-beat donors, current boards."""
import argparse,json,subprocess
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
import build_why_answers_vary_v1 as base
from editspec_build import readwav,writewav,sha,fr,Reader
from ken_burns_path import draw_ring,hex_bgr
from make_close_board import compose_canonical_for_video
ROOT=base.ROOT
OUT=ROOT/'video-audit/why-answers-vary-build-v15-2026-11-10'
DEST=ROOT/'Prompts/why-answers-vary-v15.mp4'
SRC={n:ROOT/f'Prompts/why-answers-vary-{n}.mp4' for n in (3,4,5,6)}
ASSET=ROOT/'course-assets/why-answers-vary'
base.OUT=OUT;base.DEST=DEST;base.SRC=SRC
# 30fps boundaries chosen inside measured quiet gaps. Whole sentences only.
AUDIO=[(4,0,1027,'opening-overview'),(4,1351,1608,'single-blank'),
 (3,799,1007,'vocabulary-donor'),(4,1608,2853,'sampling'),
 (4,3223,3813,'variety-review-required'),(5,3238,3327,'choice-shapes-next'),
 (3,3671,3922,'qualified-continuation'),(4,4442,4605,'temperature-bridge'),
 (6,2222,2381,'named-apps-donor'),(4,4748,5765,'temperature-example'),
 (3,5822,5940,'other-vocabulary-donor'),(4,6003,6213,'spot-comparison'),
 (4,6498,6653,'close')]
ROWS=[];cursor=0
for roll,a,z,label in AUDIO:
 ROWS.append(dict(roll=roll,source_start=a,source_end=z,start_frame=cursor,end_frame=cursor+z-a,label=label));cursor+=z-a
SPEECH_END=cursor;TOTAL=cursor+60

def of(t,roll=4):
 f=fr(t)
 for r in ROWS:
  if r['roll']==roll and r['source_start']<=f<r['source_end']:
   return r['start_frame']+f-r['source_start']
 raise ValueError((roll,t))

class Film(base.Film):
 def repair_source(self,im,repair,sf):
  # Preserve the actual branching animation; remove only its technical heading.
  if repair=='branch':
   im[80:120,165:600]=im[20:60,165:600]
  return im
 def frame(self,f):
  r=next(r for r in self.spans if r['start_frame']<=f<r['end_frame'])
  if r['kind']!='temperature':return super().frame(f)
  k=f-r['start_frame'];state=r['state'];im=self.temps[state].copy()
  if r.get('reveal') and k<18:
   im=cv2.addWeighted(self.temps[state-1],1-k/17,im,k/17,0)
  if r.get('target') and k>=r.get('ring_delay',0):
   box=r['target'];draw_ring(im,*box,hex_bgr(r.get('color','#4f2fc4')),12,4)
  return im

def assemble_audio():
 data={n:readwav(OUT/f'roll-{n}.wav') for n in SRC}
 def speech_level(x):
  x=x[:len(x)//960*960].reshape(-1,960);r=np.sqrt((x*x).mean(1));return float(np.median(r[r>600]))
 ref=speech_level(data[4]);gains={n:float(np.clip(ref/speech_level(a),.80,1.25)) if n!=4 else 1.0 for n,a in data.items()}
 tone=data[4][round(216.3*48000):round(216.4*48000)];tone=tone-tone.mean();tone=np.r_[tone,tone[::-1]]
 parts=[];ramp=np.linspace(0,1,240)
 for i,r in enumerate(ROWS):
  p=data[r['roll']][r['source_start']*1600:r['source_end']*1600].copy()*gains[r['roll']]
  bed=np.resize(tone,len(p))
  if i:p[:240]=p[:240]*ramp+bed[:240]*(1-ramp)
  p[-240:]=p[-240:]*(1-ramp)+bed[-240:]*ramp
  parts.append(p)
 parts.append(np.resize(tone,60*1600));a=np.concatenate(parts)
 assert len(a)==TOTAL*1600
 writewav(OUT/'edited.wav',a)
 for r in ROWS[1:]:
  f=r['start_frame'];writewav(OUT/f'join-{f:06d}.wav',a[max(0,f-60)*1600:min(TOTAL,f+90)*1600])
 return dict(gains_db={n:20*np.log10(g) for n,g in gains.items()},peak_dbfs=20*np.log10(np.max(np.abs(a))/32768),clipped_samples=int(np.sum(np.abs(a)>32767)),midlesson_pauses_added=0,tail_seconds=2,crossfade_ms=5)

def prepare():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 protected={str(p):sha(p) for p in [*SRC.values(),ASSET/'why-answers-vary.mp4',*ASSET.glob('*.jpg'),ROOT/'lessons/why-answers-vary.md',ROOT/'gemini-notebook/why-answers-vary/PROMPT.txt']}
 # index.html has concurrent unrelated work; this build never writes it.
 audio=assemble_audio();film=Film();film.temps=[cv2.imread(str(OUT/f'temperature-{i}.png')) for i in range(4)]
 film.source(0,fr(14.366667),'opening',4,0,14.366667)
 a=fr(14.366667);z=ROWS[0]['end_frame']
 film.board(a,z,'overview',ASSET/'why-answers-vary-overview.jpg',[
  (fr(17.7)-a,fr(21.38)-a,[40,127,485,566],'#1652f0'),
  (fr(21.38)-a,fr(25.82)-a,[557,127,486,566],'#0e8f86'),
  (fr(25.82)-a,z-a,[1075,127,485,566],'#4f2fc4')])
 a=z;z=of(61.1)
 film.board(a,z,'sampling-first',ASSET/'why-answers-vary-draws.jpg',[
  (of(47.34)-a,of(53.6)-a,[80,151,1440,85],'#4f2fc4'),
  (of(53.6)-a,z-a,[95,283,560,413],'#4f2fc4')])
 # Useful weighted-draw animation from roll 5 under the qualified 100-tries explanation.
 a=z;z=of(71.1)
 film.source(a,z,'weighted-draw',5,54.3,60.0)
 a=z;z=ROWS[3]['end_frame']
 film.board(a,z,'sampling-picks',ASSET/'why-answers-vary-draws.jpg',[
  (of(71.58)-a,of(78.56)-a,[95,283,560,413],'#4f2fc4'),
  (of(78.56)-a,of(88.78)-a,[950,282,575,345],'#4f2fc4'),
  (of(88.78)-a,z-a,[950,639,575,110],'#4f2fc4')])
 a=z;z=ROWS[4]['end_frame']
 # Audio starts in the gap; pictures start at the next scene's exact first frame.
 # Do not leak the final six frames of the removed weather diagram.
 film.source(a,z,'variety-drawings',4,107.633333,3813/30)
 a=z;z=ROWS[6]['end_frame']
 film.source(a,z,'branching',4,127.2,138.7,'branch')
 a=z;z=ROWS[8]['end_frame']
 film.source(a,z,'temperature-bridge',4,148.233333,158.233333)
 a=z;z=of(163.4)
 film.board(a,z,'temperature-full',ASSET/'why-answers-vary-temperature.jpg',[])
 a=z;z=of(170.23)
 film.add(a,z,'temperature-baseline','temperature',state=0,target=[605,149,916,654],color='#4f2fc4')
 a=z;z=of(180.38)
 film.add(a,z,'temperature-low','temperature',state=1,reveal=True,target=[286,149,599,654],color='#1652f0',ring_delay=18)
 a=z;z=ROWS[9]['end_frame']
 film.add(a,z,'temperature-high','temperature',state=2,reveal=True,target=[920,149,1230,654],color='#c41f28',ring_delay=18)
 a=z;z=ROWS[10]['end_frame']
 film.add(a,z,'temperature-other','temperature',state=2,target=[50,578,1230,655],color='#6e51ff')
 a=z;z=ROWS[11]['end_frame']
 film.add(a,z,'temperature-spot','temperature',state=2,target=[50,202,1230,270],color='#6e51ff')
 compose_canonical_for_video(ASSET/'why-answers-vary-close.jpg',OUT/'close.png','#ffffff');film.close=cv2.imread(str(OUT/'close.png'))
 film.add(z,TOTAL,'close','close')
 for l,r in zip(film.spans,film.spans[1:]):assert l['end_frame']==r['start_frame']
 assert film.spans[-1]['end_frame']==TOTAL
 boundaries=set(r['start_frame'] for r in film.spans[1:])|set(r['start_frame'] for r in ROWS[1:])
 for t in [5.266667,11.1]:boundaries.add(fr(t))
 for t in [109.866667,117.4]:boundaries.add(of(t))
 m=dict(candidate=str(DEST),fps=30,frames=TOTAL,duration=TOTAL/30,audio_timeline=ROWS,audio=audio,visual_timeline=film.spans,
  boundaries=sorted(boundaries),source_hashes={str(p):sha(p) for p in SRC.values()},protected=protected,
  capture_hashes={str(OUT/f'temperature-{i}.png'):sha(OUT/f'temperature-{i}.png') for i in range(4)},
  close=dict(start_frame=z,prehold=48,push=150,settle=TOTAL-z-198),
  approval='User: build it please. Version-4 evaluation plan; review build only.',
  listening_performed=False,continuous_playback_performed=False,
  remaining_narration=['Required techniques transition paraphrased rather than verbatim; no complete exact donor identified.',
   'Version-4 repetition/creativity rationale still lacks the approved can qualifiers; clean replacement audio is unavailable.'],
  status='Review candidate; not installed or approved for shipping')
 return film,m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Preserve every review candidate'
 film,m=prepare();wanted=set()
 for r in film.spans:wanted|={r['start_frame'],r['start_frame']+min(60,r['end_frame']-r['start_frame']-1),(r['start_frame']+r['end_frame'])//2,r['end_frame']-1}
 for key,ren in film.boards.items():
  a=next(r['start_frame'] for r in film.spans if r['key']==key)
  for ring in ren.rings:wanted.add(a+ring[0]+2)
 for f in sorted(wanted):cv2.imwrite(str(OUT/'preview'/f'{f:06d}.jpg'),film.frame(f))
 film.release();film.clean={};(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('Prepared',TOTAL,'frames;',TOTAL/30,'seconds',flush=True)
 if args.prepare_only:return
 proc=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','4','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for f in range(TOTAL):
  proc.stdin.write(film.frame(f).tobytes())
  if f%600==599:print('Rendered',f+1,'/',TOTAL,flush=True)
 proc.stdin.close();assert proc.wait()==0;film.release()
 m['candidate_sha256']=sha(DEST);m['corner_cleaning']=film.clean
 m['protected_unchanged']={p:sha(p)==h for p,h in m['protected'].items()};assert all(m['protected_unchanged'].values())
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
