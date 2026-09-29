#!/usr/bin/env python3
"""Decode and inspect the approved Mind Trap candidate without touching the live file."""
from pathlib import Path
import json,sys,subprocess,wave,functools
import cv2,numpy as np,av,imageio_ffmpeg
import build_mind_trap_v5 as b
cv2.setNumThreads(2)
OUT=b.OUT;QA=OUT/'qa';QA.mkdir(exist_ok=True);(QA/'frames').mkdir(exist_ok=True);(QA/'sheets').mkdir(exist_ok=True)
manifest=json.loads((OUT/'edit-manifest.json').read_text());assert b.sha(b.DEST)==manifest['candidate_sha256']
oldcap=cv2.VideoCapture
# Bound decoder threads, especially on shared machines running other renders.
cv2.VideoCapture=lambda p,*a,**kw:oldcap(p,*a,**kw) if a or kw else oldcap(p,cv2.CAP_FFMPEG,[cv2.CAP_PROP_N_THREADS,2])
import transition_guard
argv=['transition_guard',str(b.DEST),'--outdir',str(QA/'transitions')]
for f in manifest['boundaries']+[b.of(7063)]:argv+=['--boundary',f'{f}:declared-boundary']
sys.argv=argv;transition_guard.main()
# Sequential decode, every-frame PTS, fresh contact sheets, encoded state samples,
# and retained-picture comparison at one-second intervals.
container=av.open(str(b.DEST));stream=container.streams.video[0];stream.codec_context.thread_count=2
src=b.reader(b.SRC);sn=-1;sim=None;cells=[];sheet=0;pts=[];diff=[]
samples=json.loads((OUT/'preview-states.json').read_text());wanted={r['output_frame'] for r in samples}
for f in manifest['boundaries']:
 wanted.update([f-1,f,f+1])
modified=lambda n:804<=n<2030 or 2220<=n<2450 or 2450<=n<3160 or 3370<=n<5008
count=0
for n,frame in enumerate(container.decode(stream)):
 im=frame.to_ndarray(format='bgr24');assert im.shape==(720,1280,3);pts.append(float(frame.pts*frame.time_base));count=n+1
 if n in wanted:cv2.imwrite(str(QA/'frames'/f'{n:05d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,95])
 if n%120==0:
  tile=cv2.resize(im,(480,270));cv2.putText(tile,f'{n/30:.2f}s / f{n}',(8,26),cv2.FONT_HERSHEY_SIMPLEX,.7,(0,0,255),2);cells.append(tile)
  if len(cells)==12:
   cv2.imwrite(str(QA/'sheets'/f'sheet-{sheet:02d}.jpg'),cv2.vconcat([cv2.hconcat(cells[i:i+3]) for i in range(0,12,3)]));cells=[];sheet+=1
 if n%30==0:
  sf=n if n<b.CUT_A else n+b.REMOVED
  while sn<sf:
   ok,sim=src.read();assert ok;sn+=1
  if not modified(sf):diff.append(dict(output_frame=n,source_frame=sf,mad=float(np.mean(np.abs(im.astype(float)-sim)))))
last=im.copy();cv2.imwrite(str(QA/'frames'/'final.jpg'),last)
if cells:
 while len(cells)%3:cells.append(np.zeros_like(cells[0]))
 cv2.imwrite(str(QA/'sheets'/f'sheet-{sheet:02d}.jpg'),cv2.vconcat([cv2.hconcat(cells[i:i+3]) for i in range(0,len(cells),3)]));sheet+=1
container.close();src.release()
assert count==b.TOTAL,(count,b.TOTAL);deltas=np.diff(pts);assert np.max(np.abs(deltas-1/30))<1e-7
# Encoded audio matches the planned cut, allowing AAC quantization only.
ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-v','error','-i',str(b.DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(QA/'encoded.wav')],check=True)
a=b.readwav(QA/'encoded.wav');ref=b.readwav(OUT/'edited.wav');assert len(a)>=len(ref);a=a[:len(ref)]
corr=float(np.corrcoef(a,ref)[0,1]);assert corr>.999
outside=np.concatenate([a[:b.CUT_A*1600-240]-ref[:b.CUT_A*1600-240],a[b.CUT_A*1600+240:]-ref[b.CUT_A*1600+240:]])
# Low-floor contiguous run around the edit, 10ms RMS bins.
lo,hi=153.0,154.2;bins=[]
for t in np.arange(lo,hi,.01):
 v=a[round(t*48000):round((t+.01)*48000)]/32768;bins.append((float(t),float(20*np.log10(np.sqrt(np.mean(v*v))+1e-12))))
quiet=[t for t,d in bins if d<-40];run=[]
for t in quiet:
 if not run or t-run[-1]<.011:run.append(t)
 else:
  if run[0]<=153.6<=run[-1]+.01:break
  run=[t]
gap=[round(run[0],3),round(run[-1]+.01,3)] if run else None
for name,lo,hi in [('narration-join',148,159),('label-and-eliza',70,105),('comparison',30,66),('closing',224,232.133333)]:
 subprocess.run([ff,'-v','error','-ss',str(lo),'-i',str(b.DEST),'-t',str(hi-lo),'-c','copy',str(QA/f'{name}.mp4')],check=True)
# ASR uses a short exact WAV context, not keyframe-limited preview clips.
b.writewav(QA/'join.wav',a[148*48000:159*48000]);b.writewav(QA/'word-check.wav',a[58*48000:64*48000])
summary=dict(candidate=str(b.DEST),sha256=b.sha(b.DEST),decoded_frames=count,fps=30,duration=count/30,pts_delta_min=float(deltas.min()),pts_delta_max=float(deltas.max()),contact_sheets=sheet,unchanged_picture_samples=diff,unchanged_picture_mad_max=max(d['mad'] for d in diff),audio_correlation=corr,audio_codec_error_rms=float(np.sqrt(np.mean(outside*outside))),join_quiet_interval=gap,protected_files_unchanged=all(b.sha(Path(p))==h for p,h in manifest['protected'].items()),listening='Not auditioned. See narration-join.mp4 and candidate for human listening.')
assert summary['unchanged_picture_mad_max']<3;assert summary['protected_files_unchanged'];(QA/'summary.json').write_text(json.dumps(summary,indent=2));(QA/'join-rms.json').write_text(json.dumps(bins,indent=2));print(json.dumps({k:v for k,v in summary.items() if k!='unchanged_picture_samples'},indent=2))
