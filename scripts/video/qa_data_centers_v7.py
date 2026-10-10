#!/usr/bin/env python3
"""Check the actual v7 candidate against the approved source mapping."""
from pathlib import Path
import json,subprocess,hashlib
import av,cv2,numpy as np,imageio_ffmpeg
from editspec_build import Reader,readwav
from build_data_centers_v7 import OUT,DEST,BASE,BASE_OUT,DELTA,TOTAL,VISUAL_RESUME,SPF

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(DEST)==m['candidate_sha256']
 errors=[];times=[];source=Reader(BASE);samples=[];last=None
 with av.open(str(DEST)) as c:
  for i,f in enumerate(c.decode(video=0)):
   times.append(float(f.pts*f.time_base));last=f
   if (i<BASE_OUT or i>=VISUAL_RESUME+DELTA) and (i%30==0 or i==TOTAL-1):
    a=f.to_ndarray(format='bgr24');b=source.at(i if i<BASE_OUT else i-DELTA)
    samples.append(dict(output_frame=i,source_frame=i if i<BASE_OUT else i-DELTA,mae=float(np.abs(a.astype(float)-b).mean())))
 source.c.release();assert len(times)==TOTAL
 deltas=np.diff(times);assert np.max(np.abs(deltas-1/30))<.000002
 assert max(x['mae'] for x in samples)<4,'Unexpected changed picture outside insert'
 cv2.imwrite(str(OUT/'final-frame.png'),last.to_ndarray(format='bgr24'))
 ff=imageio_ffmpeg.get_ffmpeg_exe();subprocess.run([ff,'-v','error','-i',str(DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le','-y',str(OUT/'candidate-audio.wav')],check=True)
 actual=readwav(OUT/'candidate-audio.wav');expected=readwav(OUT/'edited.wav');assert len(actual)>=len(expected)
 actual=actual[:len(expected)];correlation=float(np.corrcoef(actual,expected)[0,1]);assert correlation>.995
 segments=[]
 for row in m['audio_timeline']:
  a=row['output_start']*SPF;z=a+(row['end_frame']-row['start_frame'])*SPF
  segments.append(dict(start=a/48000,end=z/48000,correlation=float(np.corrcoef(actual[a:z],expected[a:z])[0,1])))
 assert min(x['correlation'] for x in segments)>.995
 protected={p:sha(p)==h for p,h in m['protected_hashes'].items()};assert all(protected.values())
 result=dict(frames=len(times),duration=len(times)/30,pts_delta_min=float(deltas.min()),pts_delta_max=float(deltas.max()),unchanged_visual_samples=samples,max_visual_mae=max(x['mae'] for x in samples),audio_correlation=correlation,audio_segment_correlations=segments,decoded_audio_peak=float(np.max(np.abs(actual))),protected_unchanged=protected,listening='Not auditioned; join clips retained. Automated checks do not certify voice continuity.')
 (OUT/'qa.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS',len(times),'frames;',len(samples),'retained visual samples; max MAE',result['max_visual_mae'],'audio correlation',correlation,flush=True)
 cmd=[str(Path('.video-venv/bin/python')),'scripts/video/transition_guard.py',str(DEST),'--outdir',str(OUT/'guard')]
 for row in m['boundaries']:cmd+=['--boundary',str(row['frame'])+':'+row['label']]
 subprocess.run(cmd,check=True)
if __name__=='__main__':main()
