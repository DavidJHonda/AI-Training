import sys,json,hashlib,wave,subprocess,math
from pathlib import Path
import av,cv2,numpy as np
sys.path.insert(0,str(Path('scripts/video').resolve()))
import build_work_changes_v8 as b
p=b.OUT
m=json.loads((p/'edit-manifest.json').read_text())
boards=b.Board(b.ASSIGN),b.Board(b.CONCEPTS)
chosen=[0,379,380,391,392,694,695,698,699,804,805,885,1282,1283,1313,1392,1393,1498,1499,1677,1678,1690,1702,1773,1774,1893,1894,1935,1936,1966,2120,2121,2257,2258,2557,2558,2867,2868,3042,3043,3222,3223,3381,3382,3485,3486,4200,4970]
actual={}
with av.open(str(b.DEST)) as c:
 s=c.streams.video[0]
 info=dict(width=s.width,height=s.height,fps=float(s.average_rate),duration=float(c.duration/1e6),video_duration=float(s.duration*s.time_base))
 count=0
 for f in c.decode(s):
  assert round(f.time*30)==count
  if count in chosen: actual[count]=f.to_ndarray(format='bgr24')
  count+=1
assert count==m['frames']
source_needed={}
checks=[]
for n in chosen:
 ri=next(i for i,r in enumerate(m['rows']) if r['output_start']<=n<r['output_end'])
 r=m['rows'][ri]; sn=r['source_start']+n-r['output_start']
 repair=next((fix for fix in m.get('visual_repairs',[]) if fix['output_start']<=n<fix['output_end']),None)
 expected,label=b.compose_frame(sn,n,ri,boards,m['rows'])
 if repair:
  expected=None; sn=repair['source_frame']
 if expected is None: source_needed.setdefault(sn,[]).append(n)
 else:
  mse=float(np.mean((actual[n].astype(float)-expected.astype(float))**2))
  checks.append(dict(frame=n,label=label,psnr=10*math.log10(255**2/max(mse,1e-9))))
with av.open(str(b.SOURCE)) as c:
 for f in c.decode(video=0):
  n=round(f.time*30)
  if n in source_needed:
   expected=f.to_ndarray(format='bgr24')
   for dest in source_needed[n]:
    mse=float(np.mean((actual[dest].astype(float)-expected.astype(float))**2))
    checks.append(dict(frame=dest,label='preserved-source',source_frame=n,psnr=10*math.log10(255**2/max(mse,1e-9))))
for page,offset in enumerate(range(0,len(chosen),12)):
 tiles=[]
 for n in chosen[offset:offset+12]:
  tile=cv2.resize(actual[n],(480,270)); tile=cv2.copyMakeBorder(tile,26,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255))
  cv2.putText(tile,f'{n/30:.2f}s | f{n}',(8,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,0),1,cv2.LINE_AA); tiles.append(tile)
 while len(tiles)<12: tiles.append(np.full_like(tiles[0],255))
 cv2.imwrite(str(p/f'encoded-contact-{page+1}.jpg'),np.vstack([np.hstack(tiles[i:i+3]) for i in range(0,12,3)]))
for n in [885,1313,1702,2558,2868,3382,4970]: cv2.imwrite(str(p/f'encoded-{n}.png'),actual[n])
subprocess.run([b.FF,'-v','error','-y','-i',str(b.DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(p/'encoded.wav')],check=True)
def audio(path):
 with wave.open(str(path)) as w: return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float64)
a=audio(p/'edited.wav'); d=audio(p/'encoded.wav')[:len(a)]
assert len(a)==len(d)
audio_result=dict(samples=len(a),correlation=float(np.corrcoef(a,d)[0,1]),snr_db=float(10*np.log10(np.sum(a*a)/np.sum((a-d)**2))),max_join_jump=max(abs(j['sample_jump']) for j in m['audio_joins']),max_join_20ms_peak=max(max(j['before_20ms_peak'],j['after_20ms_peak']) for j in m['audio_joins']))
protected=all(b.sha(path)==h for path,h in m['protected'].items())
result=dict(decoded_frames=count,video=info,selected_frame_comparisons=checks,minimum_psnr=min(x['psnr'] for x in checks),audio=audio_result,protected_files_unchanged=protected,full_perceptual_listening=False)
assert all(b.sha(path)==h for path,h in m['protected'].items() if not path.endswith('index.html'))
(p/'qa.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='selected_frame_comparisons'},indent=2))
