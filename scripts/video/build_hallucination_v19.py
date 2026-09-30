#!/usr/bin/env python3
"""Shorten both worked applications while retaining their distinct outcomes."""
from pathlib import Path
import argparse,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
import build_hallucination_v18 as previous
from editspec_build import Reader,sha

ROOT=previous.ROOT;SRC=previous.SRC;PRIOR_OUT=previous.OUT;PRIOR=previous.DEST
OUT=ROOT/'video-audit/hallucination-shorten-2026-09-30-v19'
DEST=ROOT/'Prompts/hallucination-v19.mp4'
FPS=30;SR=48000;SPF=1600
# Raw roll-3 frame ranges, cut between complete sentences in measured quiet gaps.
RAW_CUTS=[(6235,6577,'Repeated Stanford details and first/second step announcements'),
 (6727,6783,'Stanford third-step announcement'),
 (7333,7404,'Pizza first-step announcement'),
 (7494,7571,'Pizza second-step announcement'),
 (7713,7787,'Pizza third-step announcement')]
CUTS=[dict(start=a+90,end=b+90,label=label,raw_source_frames=[a,b]) for a,b,label in RAW_CUTS]
REMOVED=sum(c['end']-c['start'] for c in CUTS);TOTAL=previous.TOTAL-REMOVED
def output_frame(p):
 if any(c['start']<=p<c['end'] for c in CUTS):return None
 return p-sum(c['end']-c['start'] for c in CUTS if c['end']<=p)
SPANS=[];cursor=0;out=0
for c in CUTS:
 SPANS.append(dict(previous_start=cursor,previous_end=c['start'],start=out,end=out+c['start']-cursor))
 out+=c['start']-cursor;cursor=c['end']
SPANS.append(dict(previous_start=cursor,previous_end=previous.TOTAL,start=out,end=TOTAL))
def previous_frame(n):
 for s in SPANS:
  if s['start']<=n<s['end']:return s['previous_start']+n-s['start']
 raise ValueError(n)
CLOSE=output_frame(previous.CLOSE)
BOUNDARIES={}
for f,label in previous.BOUNDARIES:
 n=output_frame(f)
 if n is not None:BOUNDARIES.setdefault(n,[]).append(label)
for s,c in zip(SPANS[1:],CUTS):BOUNDARIES.setdefault(s['start'],[]).append(c['label'])
BOUNDARIES.setdefault(6269,[]).append('Stanford settled claim under introduction')
BOUNDARIES.setdefault(6742,[]).append('Hold unverified-study outcome')
BOUNDARIES.setdefault(6912,[]).append('Pizza visual follows spoken handoff')

def audio():
 original=previous.loadwav(PRIOR_OUT/'edited.wav');parts=[];cursor=0;joins=[];removed=0
 for c in CUTS:
  a,b=c['start'],c['end'];parts.append(original[cursor*SPF:a*SPF]);cursor=b
  joins.append(dict(frame=a-removed,seconds=(a-removed)/30,previous_frames=[a,b],raw_source_frames=c['raw_source_frames'],label=c['label']))
  removed+=b-a
 parts.append(original[cursor*SPF:]);edited=np.concatenate(parts)
 for j in joins:
  k=j['frame']*SPF;v=edited[k-960:k+960];rms=float(20*np.log10(max(np.sqrt(np.mean(v*v)),1e-9)/32768))
  assert rms < -55,(j,rms)
  j.update(quiet_window_dbfs=rms,smoothing_ms=5)
  edited[k-120:k+120]=np.linspace(edited[k-120],edited[k+119],240)
 previous.writewav(OUT/'edited.wav',edited)
 return dict(source_pcm=str(PRIOR_OUT/'edited.wav'),source_pcm_sha256=sha(PRIOR_OUT/'edited.wav'),joins=joins,output_samples=len(edited),sample_rate=SR,added_pause_frames=0,subjective_listening_performed=False)

class Production(previous.Production):
 def __init__(self):
  previous.OUT=OUT;previous.DEST=DEST;super().__init__()
  self.b.hashes[str(PRIOR)]=sha(PRIOR);self.b.hashes[str(PRIOR_OUT/'edited.wav')]=sha(PRIOR_OUT/'edited.wav')
  self.b.hashes[str(ROOT/'index.html')]=sha(ROOT/'index.html')
  donor=Reader(SRC);self.stanford=super().frame(donor.at(6420),6510)
  self.unverified=super().frame(donor.at(7050),7140)
 def frame(self,im,n):
  p=previous_frame(n)
  # Retain the established Stanford claim as the shortened intro lands;
  # the original opening animation would otherwise barely emerge before the cut.
  if 6269<=p<6325:return self.stanford.copy()
  # Keep the Stanford result through the unverified-claim caveat. The old
  # animation introduced pizza several seconds before its spoken handoff.
  if 7140<=p<7310:return self.unverified.copy()
  return super().frame(im,p)
 def preview(self):
  nums={output_frame(int(p.stem)) for p in (PRIOR_OUT/'preview').glob('*.png')}
  nums.discard(None);nums.update(range(6240,CLOSE+1,30));nums.update([CLOSE,CLOSE+48,CLOSE+197,TOTAL-1])
  for n in BOUNDARIES:nums.update(range(n-2,n+3))
  reader=Reader(SRC);thumbs=[]
  for n in sorted(x for x in nums if 0<=x<TOTAL):
   im=self.frame(reader.at(previous.source_frame(previous_frame(n))),n);cv2.imwrite(str(OUT/'preview'/f'{n:05d}.png'),im)
   tile=cv2.resize(im,(320,180));tile=cv2.copyMakeBorder(tile,24,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255))
   cv2.putText(tile,f'{n/30:.2f}s / f{n}',(6,17),cv2.FONT_HERSHEY_SIMPLEX,.45,(20,20,20),1,cv2.LINE_AA);thumbs.append(tile)
  for k in range(0,len(thumbs),24):
   group=thumbs[k:k+24]
   while len(group)%4:group.append(np.full_like(group[0],255))
   cv2.imwrite(str(OUT/f'preview-sheet-{k//24+1}.jpg'),cv2.vconcat([cv2.hconcat(group[i:i+4]) for i in range(0,len(group),4)]))
  print('Previews ready',flush=True)
 def render(self):
  assert not DEST.exists(),'Never overwrite a candidate'
  aud=audio();self.counts.clear();self.donor_counts.clear();ff=imageio_ffmpeg.get_ffmpeg_exe();temp=OUT/'render.tmp.mp4'
  cmd=[ff,'-y','-v','warning','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(temp)]
  with open(OUT/'encode.log','w') as log:
   proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log);reader=Reader(SRC)
   for n in range(TOTAL):
    proc.stdin.write(self.frame(reader.at(previous.source_frame(previous_frame(n))),n).tobytes())
    if n%900==0:print(f'Rendered {n}/{TOTAL}',flush=True)
   proc.stdin.close();assert proc.wait()==0
  assert all(sha(Path(p))==h for p,h in self.b.hashes.items()),'Protected input changed'
  assert not DEST.exists();temp.rename(DEST)
  retimes=[dict(previous_frames=[6269,6325],output_frames=[6269,6325],raw_picture_frame=6420,purpose='Show established claim during the abbreviated introduction'),dict(previous_frames=[7140,7310],output_frames=[6742,6912],raw_picture_frame=7050,purpose='Keep the unverified study visible through its caveat; reveal pizza at the spoken handoff')]
  m=dict(candidate=str(DEST),sha256=sha(DEST),source=str(SRC),previous_candidate=str(PRIOR),fps=30,total_frames=TOTAL,duration=TOTAL/30,removed_frames=REMOVED,removed_seconds=REMOVED/30,kept_spans=SPANS,cuts=CUTS,audio=aud,boundaries=BOUNDARIES,board_runs=previous.BOARD_RUNS,longest_board_run_seconds=27.8,worked_examples=dict(start=6269,end=CLOSE,duration_seconds=(CLOSE-6269)/30),close=dict(start_frame=CLOSE,prehold=48,push=150,tail=120),visual_retimes=retimes,protected_hashes=self.b.hashes,corner_counts=dict(self.counts),donor_corner_counts=dict(self.donor_counts),scope='Narrow approved shortening of both worked applications. Review candidate; not installed or published.')
  (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(f'Built {DEST}',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--preview',action='store_true');a=p.parse_args();b=Production();b.preview() if a.preview else b.render()
