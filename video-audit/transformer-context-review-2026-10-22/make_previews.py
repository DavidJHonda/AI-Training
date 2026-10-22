"""Whole-passage donor previews; no video candidate is built or installed."""
from pathlib import Path
import subprocess,json,hashlib
import numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
ff=imageio_ffmpeg.get_ffmpeg_exe();sr=48000;spf=1600
def decode(p):
 return np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(p),'-vn','-ar',str(sr),'-ac','1','-f','f32le','-']),np.float32).copy()
base=ROOT/'Prompts/transformer-v13.mp4';donor=ROOT/'Prompts/transformer-2.mp4'
a=decode(base);d=decode(donor)
def level(x,s,e):
 x=x[round(s*sr):round(e*sr)];r=np.sqrt(np.mean(x[:len(x)//960*960].reshape(-1,960)**2,axis=1));return float(np.median(r[r>.025]))
gain=level(a,23,175)/level(d,30,208)
clips=[
 dict(name='opening-examples',base_frames=[1015,1570],donor_frames=[[1002,1405]],context=[29.0,54.8]),
 dict(name='sequential-reading',base_frames=[1889,2101],donor_frames=[[2187,2421]],context=[54.7,83.3]),
 dict(name='parallel-processing',base_frames=[2803,3114],donor_frames=[[3477,4048]],context=[88.3,113.2]),
 dict(name='return-to-examples',base_frames=[4570,5136],donor_frames=[[1002,1094],[5844,5994],[1094,1405]],context=[146.5,175.55])]
shift=0
for c in clips:
 s,e=c['base_frames'];chunks=[];join_checks=[]
 for ds,de in c['donor_frames']:
  x=d[ds*spf:de*spf].copy()*gain;peak=float(abs(x).max())
  if peak>.96:
   raw=subprocess.check_output([ff,'-v','error','-f','f32le','-ar',str(sr),'-ac','1','-i','pipe:0','-af','alimiter=limit=0.96:level=false:attack=5:release=50:latency=true','-f','f32le','-'],input=x.astype(np.float32).tobytes());x=np.frombuffer(raw,np.float32).copy()
  assert len(x)==(de-ds)*spf
  chunks.append(x);join_checks.append(dict(frames=[ds,de],peak_before=peak,peak_after=float(abs(x).max()),limited=peak>.96))
 insert=np.concatenate(chunks);fade=240;r=np.linspace(0,1,fade)
 insert[:fade]=a[s*spf:s*spf+fade]*(1-r)+insert[:fade]*r
 insert[-fade:]=insert[-fade:]*(1-r)+a[e*spf-fade:e*spf]*r
 # Internal joins are in quiet pauses. Smooth only a 5 ms neighborhood,
 # without inserting or deleting samples or altering any spoken passage.
 cursor=0
 for part in chunks[:-1]:
  cursor+=len(part);insert[cursor-fade:cursor]*=np.linspace(1,0,fade);insert[cursor:cursor+fade]*=r
 preview=np.r_[a[round(c['context'][0]*sr):s*spf],insert,a[e*spf:round(c['context'][1]*sr)]]
 target=OUT/(c['name']+'-preview.wav')
 subprocess.run([ff,'-y','-v','error','-f','f32le','-ar',str(sr),'-ac','1','-i','pipe:0','-c:a','pcm_f32le',str(target)],input=preview.astype(np.float32).tobytes(),check=True)
 count=len(insert)//spf;new_s=s+shift;shift+=count-(e-s)
 c.update(output_frames=[new_s,new_s+count],delta_frames=count-(e-s),gain_db=float(20*np.log10(gain)),donor_processing=join_checks,direct_listening=False,
  cut_rms_dbfs={},preview_graft_start=s/30-c['context'][0],preview_graft_end=s/30-c['context'][0]+count/30,preview_duration=len(preview)/sr)
 for label,arr,points in [('base',a,[s,e]),('donor',d,[p for chunk in c['donor_frames'] for p in chunk])]:
  c['cut_rms_dbfs'][label]=[float(20*np.log10(np.sqrt(np.mean(arr[f*spf-480:f*spf+480]**2))+1e-12)) for f in points]
 c['insert_sha256']=hashlib.sha256(insert.astype(np.float32).tobytes()).hexdigest()
plan=dict(base=str(base),donor=str(donor),base_sha256=hashlib.sha256(base.read_bytes()).hexdigest(),donor_sha256=hashlib.sha256(donor.read_bytes()).hexdigest(),grafts=clips,
 proposed_frames=7046+shift,proposed_duration=(7046+shift)/30,new_pauses='None',status='proposed, not built',direct_listening=False)
(OUT/'proposed-grafts.json').write_text(json.dumps(plan,indent=2)+'\n');print(json.dumps(plan,indent=2))
