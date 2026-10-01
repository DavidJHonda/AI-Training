#!/usr/bin/env python3
"""Verify exact pause removal, speech preservation, remapped visuals and joins."""
import json,subprocess,itertools,re,sys
import av,cv2,numpy as np
import build_honesty_privacy_v6 as b
cv2.setNumThreads(1)
def main():
 m=json.loads((b.OUT/'edit-manifest.json').read_text());assert b.sha(b.DEST)==m['candidate_sha256']
 original=b.get_pcm(b.APPROVED)[:7200*b.SPF]
 trimmed=np.concatenate([original[r['source_start']*b.SPF:r['source_end']*b.SPF] for r in m['kept_spans']])
 edited=np.load(b.OUT/'edited-pcm.npy');mask=np.ones(len(edited),dtype=bool)
 for c in m['cuts']:
  k=c['output_join_frame']*b.SPF;mask[k-120:k+120]=False
 assert np.array_equal(trimmed[mask],edited[mask]),'Retained PCM changed outside 5ms room-tone bridges'
 actual=b.get_pcm(b.DEST)[:len(edited)]
 corr=float(np.corrcoef(edited,actual)[0,1]);assert corr>.999
 # Non-silent 100ms windows verify alignment everywhere, not only global correlation.
 x=edited.reshape(-1,4800);y=actual.reshape(-1,4800)
 active=np.sqrt(np.mean(x*x,axis=1))>.01
 mse=np.mean((x-y)**2,axis=1);energy=np.mean(x*x,axis=1)
 relative=np.sqrt(mse[active]/energy[active]);assert np.max(relative)<.12,float(np.max(relative))
 sample_source={n:f for n,f in b.prior.frames(6290) if n in {3054,6258,6288}};patch=b.prior.Patch(sample_source)
 wants={0,b.TOTAL-1,b.mapped(3540),b.mapped(6480),b.mapped(2805)}
 for j in m['boundaries']:wants.update([j['frame']-1,j['frame'],j['frame']+12])
 c=av.open(str(b.DEST));c.streams.video[0].codec_context.thread_count=2
 decoded=iter(c.decode(video=0));count=0;maxerr=0;cells=[]
 for n,src in b.prior.frames():
  if b.removed(n):continue
  f=next(decoded);assert f.pts==count*512
  expected=patch.render(src,n);actual_frame=f.to_ndarray(format='bgr24')
  err=float(np.abs(actual_frame.astype(float)-expected).mean());maxerr=max(maxerr,err);assert err<4,(n,err)
  if count in wants:
   cv2.imwrite(str(b.OUT/f'encoded-{count:05}.jpg'),actual_frame)
   tile=cv2.resize(actual_frame,(320,180));cv2.putText(tile,f'{count} / {count/30:.2f}s',(4,18),0,.48,(0,0,220),1);cells.append(tile)
  count+=1
 assert next(decoded,None) is None and count==b.TOTAL
 for i in range(0,len(cells),20):
  part=cells[i:i+20]
  while len(part)%4:part.append(part[-1]*0)
  cv2.imwrite(str(b.OUT/f'encoded-sheet-{i//20}.jpg'),cv2.vconcat([cv2.hconcat(part[j:j+4]) for j in range(0,len(part),4)]))
 assert c.streams.video[0].duration*c.streams.video[0].time_base==230
 assert c.streams.audio[0].duration*c.streams.audio[0].time_base==230
 c.close()
 r=subprocess.run([b.FF,'-hide_banner','-i',str(b.DEST),'-vn','-af','silencedetect=noise=-35dB:d=0.15','-f','null','-'],capture_output=True,text=True,check=True)
 (b.OUT/'output-silences.txt').write_text(r.stderr)
 silences=[tuple(map(float,a)) for a in re.findall(r'silence_end: ([\d.]+) \| silence_duration: ([\d.]+)',r.stderr)]
 gap_checks=[]
 for cut in m['cuts']:
  seam=cut['output_join_frame']/30
  end,duration=next((e,d) for e,d in silences if e-d<=seam<=e)
  # AAC can move a -35dB threshold crossing on a word tail without shifting samples.
  # Exact retained PCM and active-window alignment are checked above.
  assert abs(duration-cut['target_gap_seconds'])<.05,(cut,duration)
  gap_checks.append(dict(label=cut['label'],output_join_seconds=seam,target=cut['target_gap_seconds'],actual=duration))
 # Keep each shortened transition available for the owner's auditory review.
 for i,c in enumerate(m['cuts']):
  k=c['output_join_frame']/30
  subprocess.run([b.FF,'-v','error','-y','-ss',str(max(0,k-2.5)),'-i',str(b.DEST),'-t','5.5','-vn','-c:a','pcm_s16le',str(b.OUT/f'join-{i+1:02d}.wav')],check=True)
 assert all(b.sha(p)==h for p,h in m['protected_hashes'].items())
 report=dict(candidate_sha256=b.sha(b.DEST),frames=count,fps=30,duration_seconds=230,removed_pause_count=10,removed_seconds=10,
  retained_preencode_pcm_exact_outside_quiet_5ms_seams=True,audio_correlation=corr,max_active_100ms_relative_error=float(np.max(relative)),
  max_visual_mean_encoding_error=maxerr,gap_checks=gap_checks,protected_inputs_unchanged=True,direct_listening_performed=False)
 (b.OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
 # Use single-thread OpenCV for bounded sequential decoding in the shared checker.
 code='import cv2,runpy;cv2.setNumThreads(1);runpy.run_path('+repr(str(b.ROOT/'scripts/video/transition_guard.py'))+',run_name="__main__")'
 cmd=[sys.executable,'-c',code,str(b.DEST),'--outdir',str(b.OUT/'transitions')]
 for j in m['boundaries']:cmd+=['--boundary',str(j['frame'])+':'+j['label']]
 subprocess.run(cmd,check=True)
if __name__=='__main__':main()
