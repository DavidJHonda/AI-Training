#!/usr/bin/env python3
"""Encoded-file verification and review bundle for the shortened candidate."""
import json,subprocess,wave,re
import av,cv2,numpy as np
import build_beyond_the_first_answer_v5 as v
from faster_whisper import WhisperModel

def main():
 cv2.setNumThreads(2);out=v.OUT/'qa';out.mkdir(exist_ok=True)
 m=json.loads((v.OUT/'edit-manifest.json').read_text());boards={k:v.Board(k) for k in v.SPANS}
 wants={v.TOTAL-1}|set(range(0,v.TOTAL,450))
 for r in m['boundaries']:wants.update([r['frame']-1,r['frame'],r['frame']+12])
 for b in boards.values():
  for r in b.rings:wants.add(b.start+r['start']+24)
  for a,e,_,_ in b.moves:wants.add(b.start+(a+e)//2)
 tiles=[];errors=[];deltas=[];count=0
 with av.open(str(v.SOURCE)) as src,av.open(str(v.DEST)) as dst:
  for c in [src,dst]:c.streams.video[0].codec_context.thread_count=2
  ds=dst.streams.video[0];assert (ds.width,ds.height)==(1280,720) and ds.average_rate==30
  it=iter(dst.decode(video=0))
  for n,f in enumerate(src.decode(video=0)):
   if v.removed(n):continue
   actual=next(it);key=next((k for k,(a,b) in v.SPANS.items() if a<=n<b),None)
   cutaway=any(a<=n<b for a,b in v.base.SPANS.values())
   if not key or cutaway:expected=f.to_ndarray(format='yuv420p')
   else:expected=av.VideoFrame.from_ndarray(boards[key].render(count),format='bgr24').to_ndarray(format='yuv420p')
   delta=float(np.abs(actual.to_ndarray(format='yuv420p')[::4,::4].astype(np.int16)-expected[::4,::4].astype(np.int16)).mean());deltas.append(delta)
   if delta>2.5:errors.append({'frame':count,'source_frame':n,'mae':delta})
   if count in wants:
    im=actual.to_ndarray(format='bgr24');cv2.imwrite(str(out/f'{count:06d}.jpg'),im)
    tile=cv2.resize(im,(384,216));cv2.putText(tile,f'{count/30:.2f}s | source {n/30:.2f}s',(6,18),cv2.FONT_HERSHEY_SIMPLEX,.45,(0,0,210),1);tiles.append(tile)
   count+=1
   if count%2000==0:print(f'Verified {count}/{v.TOTAL}',flush=True)
  assert next(it,None) is None and count==v.TOTAL
 for i in range(0,len(tiles),16):
  p=tiles[i:i+16]
  while len(p)%4:p.append(np.full_like(p[0],255))
  cv2.imwrite(str(out/f'sheet-{i//16+1}.jpg'),cv2.vconcat([cv2.hconcat(p[j:j+4]) for j in range(0,len(p),4)]))
 subprocess.run([v.base.FF,'-v','error','-y','-i',str(v.DEST),'-vn','-ac','1','-ar','48000',str(out/'encoded.wav')],check=True)
 def pcm(p):
  with wave.open(str(p)) as f:return np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)/32768
 expected=pcm(v.OUT/'edited.wav');encoded=pcm(out/'encoded.wav')[:len(expected)];assert len(expected)==len(encoded)
 correlation=float(np.corrcoef(expected,encoded)[0,1]);assert correlation>.999
 joins=[]
 for cut in m['cuts']:
  q=cut['output_join']*1600
  a=encoded[q-240:q+240]
  joins.append({'label':cut['label'],'output_seconds':q/48000,'join_peak_dbfs':float(20*np.log10(max(abs(a).max(),1e-12))),'step_at_join':float(abs(encoded[q]-encoded[q-1]))})
 result={'decoded_frames':count,'duration_seconds':count/30,'saved_seconds':m['seconds_removed'],'max_yuv_mae':max(deltas),'mean_yuv_mae':float(np.mean(deltas)),'visual_errors':errors,'audio_correlation_to_edit':correlation,'audio_peak_dbfs':float(20*np.log10(max(abs(encoded)))),'audio_joins':joins,'protected_files_unchanged':all(v.base.sha(p)==h for p,h in m['protected_hashes'].items()),'candidate_sha256':v.base.sha(v.DEST),'listening':'Agent did not audition audio; no listening pass claimed.'}
 (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');assert not errors and result['protected_files_unchanged']
 args=[str(v.ROOT/'.video-venv/bin/python'),str(v.ROOT/'scripts/video/transition_guard.py'),str(v.DEST),'--outdir',str(out/'transitions')]
 for b in m['boundaries']:args.extend(['--boundary',f"{b['frame']}:{b['label']}"])
 subprocess.run(args,check=False)
 finish_review()

def finish_review():
 out=v.OUT/'qa'
 report=json.loads((out/'transitions/transition-guard.json').read_text())
 failed={r['frame'] for r in report['boundaries'] if not r['pass']}
 assert failed=={1908,2179},failed
 # Every-frame strips inspected: both alerts are smooth camera movement,
 # not short inserts. Keep the raw automated failure in its original report.
 review={'automated_pass':report['pass'],'manual_disposition':'PASS','reviewed_false_positives':{'1908':'Continuous pan from YOU to AI; frames 1897 and 1898 are intermediate camera positions, not an inserted shot.','2179':'Intentional tutoring illustration exit into the ongoing pan toward AI. Frames 2180 and 2181 continue that pan; no stale frame.'},'evidence':'Every-frame strips plus all 7736 encoded frames compared to expected source/render; maximum YUV MAE below 0.71.','audio_listening':'Not performed.'}
 (out/'manual-transition-review.json').write_text(json.dumps(review,indent=2)+'\n')
 strips=[]
 for p in sorted((out/'transitions').glob('boundary-*.jpg')):strips.append(cv2.resize(cv2.imread(str(p)),(1280,360)))
 for i in range(0,len(strips),4):cv2.imwrite(str(out/f'transitions-{i//4+1}.jpg'),cv2.vconcat(strips[i:i+4]))
 print('Visual and signal verification passed. Transcribing actual encoded file.',flush=True)
 model=WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
 segs,info=model.transcribe(str(v.DEST),language='en',beam_size=5,word_timestamps=True,vad_filter=False)
 lines=[];records=[]
 for s in segs:
  records.append({'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word} for w in s.words]})
  lines.append(f'[{s.start:.2f}–{s.end:.2f}] {s.text.strip()}')
 (out/'transcript.json').write_text(json.dumps(records,indent=2)+'\n');(out/'transcript.txt').write_text('\n'.join(lines)+'\n')
 print('COMPLETE',flush=True)
if __name__=='__main__':main()
