from pathlib import Path
import sys,json,subprocess,math
import cv2,numpy as np,imageio_ffmpeg
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import readwav,sha
m=json.loads((HERE/'edit-manifest.json').read_text());ff=imageio_ffmpeg.get_ffmpeg_exe();dest=Path(m['output'])
cap=cv2.VideoCapture(str(dest));base=cv2.VideoCapture(m['base']);base_n=-1;out_n=0;errors=[];changed=[];snapshots={}
joinframes=[x['output_frame'] for x in m['seams']]
for row in m['timeline']:
 for s in range(row['source_start'],row['source_end']):
  while base_n<s:
   ok,bi=base.read();assert ok;base_n+=1
  ok,im=cap.read();assert ok
  if out_n%15==0 or any(abs(out_n-j)<=2 for j in joinframes):
   err=float(np.abs(cv2.resize(im,(160,90)).astype(float)-cv2.resize(bi,(160,90))).mean())
   (changed if 6817<=s<7171 else errors).append(err)
  if out_n in [j+d for j in joinframes for d in [-2,-1,0,1,8,20]]:
   cv2.imwrite(str(HERE/'preview'/f'f{out_n:05d}.jpg'),im)
  out_n+=1
assert not cap.read()[0];assert out_n==m['total_frames']
cap.release();base.release()
assert max(errors)<1.0,max(errors)
subprocess.run([ff,'-v','error','-i',str(dest),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(HERE/'encoded.wav')],check=True)
a=readwav(HERE/'encoded.wav');assembled=readwav(HERE/'assembled.wav');src=readwav(HERE/'source.wav')
original=np.concatenate([src[r['source_start']*1600:r['source_end']*1600] for r in m['timeline']]);mask=np.ones(len(original),bool)
for j in joinframes:mask[j*1600-240:j*1600+240]=False
assert np.array_equal(assembled[mask],original[mask])
corr=float(np.corrcoef(assembled,a[:len(assembled)])[0,1]);assert corr>.999
log=subprocess.run([ff,'-hide_banner','-i',str(dest),'-af','silencedetect=noise=-40dB:d=0.12','-f','null','-'],capture_output=True,text=True,check=True)
(HERE/'encoded-silences.log').write_text(log.stderr)
clips=HERE/'qa';clips.mkdir(exist_ok=True)
for n,(j,label) in enumerate(zip(joinframes,['pepsi','coffee','it']),1):
 start=j/30-4;dur=10
 subprocess.run([ff,'-v','error','-ss',str(start),'-i',str(dest),'-t',str(dur),'-c:v','libx264','-crf','18','-c:a','aac','-b:a','192k',str(clips/f'{label}-join.mp4')],check=True)
cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(dest),'--outdir',str(HERE/'transitions')]
for row in m['boundaries']:cmd+=['--boundary',f"{row['frame']}:{row['label']}"]
subprocess.run(cmd,check=True)
assert all(sha(Path(k))==v for k,v in m['protected_hashes'].items())
report=dict(output_sha256=sha(dest),decoded_frames=out_n,duration=out_n/30,unaffected_picture_samples=len(errors),max_unaffected_picture_mad=max(errors),intentional_highlight_change_samples=len(changed),retained_pcm_identical_outside_5ms_seams=True,encoded_audio_correlation=corr,encoded_peak=float(np.max(abs(a))/32768),protected_files_unchanged=True,direct_listening=False,full_file_watch=False)
(HERE/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
