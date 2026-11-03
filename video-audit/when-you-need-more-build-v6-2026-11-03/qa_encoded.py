from pathlib import Path
import json,sys,subprocess
import cv2,numpy as np,imageio_ffmpeg
sys.path.insert(0,str(Path.cwd()/'scripts/video'))
from editspec_build import readwav,sha
root=Path.cwd();out=root/'video-audit/when-you-need-more-build-v6-2026-11-03';m=json.loads((out/'edit-manifest.json').read_text());dest=Path(m['output']);ff=imageio_ffmpeg.get_ffmpeg_exe()
cmd=[sys.executable,'scripts/video/transition_guard.py',str(dest),'--outdir',str(out/'transitions')]
boundaries={r['start_frame']:r['label'] for r in m['visual_timeline'][1:]}
for r in m['audio_timeline'][1:]:boundaries.setdefault(r['start_frame'],r['label'])
for f,label in boundaries.items():cmd+=['--boundary',f'{f}:{label}']
subprocess.run(cmd,check=True)
subprocess.run([ff,'-v','error','-i',str(dest),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(out/'decoded.wav')],check=True)
x=readwav(out/'decoded.wav');joins=[]
for r in m['audio_timeline'][1:]:
 f=r['start_frame'];c=f*1600;w=x[c-240:c+240]
 joins.append(dict(frame=f,seconds=f/30,peak_dbfs=float(20*np.log10(max(1,np.abs(w).max())/32768)),adjacent_sample_jump=int(abs(x[c]-x[c-1]))))
q=dict(expected_frames=m['frames'],duration=m['duration'],decoded_audio_samples=len(x),expected_audio_samples=m['frames']*1600,audio_padding_samples=len(x)-m['frames']*1600,decoded_peak_dbfs=float(20*np.log10(np.abs(x).max()/32768)),joins=joins,protected_unchanged={p:sha(p)==h for p,h in m['protected_hashes'].items()},candidate_sha256=sha(dest))
cap=cv2.VideoCapture(str(dest));q['fps']=cap.get(cv2.CAP_PROP_FPS);q['width']=cap.get(cv2.CAP_PROP_FRAME_WIDTH);q['height']=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frames=set(range(0,m['frames'],150))|{r['start_frame'] for r in m['visual_timeline']}|{r['end_frame']-1 for r in m['visual_timeline']}|{1000,1001,1010,1050,1110,1200,1382,4850,5037,5068}
proof=out/'encoded-frames';proof.mkdir(exist_ok=True);tiles=[];idx=0
while True:
 ok,im=cap.read()
 if not ok:break
 if idx in frames:
  cv2.imwrite(str(proof/f'{idx:05}.jpg'),im)
  tile=cv2.resize(im,(384,216));cv2.rectangle(tile,(0,0),(384,23),(255,255,255),-1);cv2.putText(tile,f'f{idx} | {idx/30:.2f}s',(8,17),cv2.FONT_HERSHEY_SIMPLEX,.45,(0,0,0),1);tiles.append(tile)
 idx+=1
q['decoded_frames']=idx;cap.release()
for n in range(0,len(tiles),12):
 ts=tiles[n:n+12];ts+= [np.full_like(ts[0],255)]*((-len(ts))%3)
 cv2.imwrite(str(out/f'encoded-sheet-{n//12+1}.jpg'),cv2.vconcat([cv2.hconcat(ts[i:i+3]) for i in range(0,len(ts),3)]))
assert idx==m['frames'];assert all(q['protected_unchanged'].values());assert 0<=q['audio_padding_samples']<1024
(out/'encoded-qa.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
