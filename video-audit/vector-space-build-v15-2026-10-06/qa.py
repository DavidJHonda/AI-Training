from pathlib import Path
import json,subprocess,re,cv2,numpy as np,sys
root=Path(__file__).resolve().parents[2];out=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'scripts/video'));from editspec_build import sha
import imageio_ffmpeg
m=json.loads((out/'edit-manifest.json').read_text());src=Path(m['output']);ff=imageio_ffmpeg.get_ffmpeg_exe()
# Decode and analyze the delivered AAC audio, not only the WAV used for assembly.
p=subprocess.run([ff,'-hide_banner','-i',str(src),'-af','silencedetect=noise=-35dB:d=0.15','-f','null','-'],capture_output=True,text=True)
(out/'encoded-silence-log.txt').write_text(p.stderr);intervals=[];s=None
for l in p.stderr.splitlines():
 a=re.search('silence_start: ([0-9.]+)',l);e=re.search('silence_end: ([0-9.]+)',l)
 if a:s=float(a[1])
 if e and s is not None:intervals.append([s,float(e[1])]);s=None
pauses=[]
for row in m['timeline']:
 if row['kind']=='room_tone' and 'comparison' in row['label']:
  at=(row['start_frame']+row['end_frame'])/60
  actual=next(x for x in intervals if x[0]<=at<=x[1]);dur=actual[1]-actual[0]
  pauses.append(dict(label=row['label'],output_interval=actual,duration=dur,target=1.75,within_one_frame=abs(dur-1.75)<1/30))
# Full sequential decode plus sampled encoded frames at reveals, joins, source scenes, and finish.
frames=out/'encoded-frames';frames.mkdir(exist_ok=True)
selected=set(range(0,m['total_frames'],300))|{m['total_frames']-1}
for cues in [m['city_cues'],m['drink_cues']]:
 for f,step in cues:selected.update([max(0,f-1),f,f+15])
for r in m['boundaries']:selected.update([r['frame']-1,r['frame'],r['frame']+1])
a,z=m['visual_sections']['scale'];selected.update(range(a,z,10))
a,z=m['visual_sections']['relationships'];selected.update(range(a,z,10))
cap=cv2.VideoCapture(str(src));i=0;black=[];sizes=set();picked=[]
while True:
 ok,im=cap.read()
 if not ok:break
 sizes.add(im.shape[:2])
 if im.mean()<2:black.append(i)
 if i in selected:
  cv2.imwrite(str(frames/f'{i:05}.jpg'),im)
  picked.append(i)
 i+=1
cap.release()
# At every answer, previous frame must match the unanswered state rather than expose the ring.
answers=[]
for kind,idx in [('cities',5),('cities',7),('drinks',5),('drinks',7)]:
 cue=m['city_cues' if kind=='cities' else 'drink_cues'][idx][0]
 for offset,state in [(-1,idx-1),(15,idx)]:
  observed=cv2.imread(str(frames/f'{cue+offset:05}.jpg'));expected=cv2.imread(str(out/'frames'/f'{kind}-{state}.png'))
  answers.append(dict(kind=kind,answer=idx,frame=cue+offset,expected_state=state,mean_absolute_difference=float(np.abs(observed.astype(float)-expected).mean())))
report=dict(duration=m['duration'],planned_frames=m['total_frames'],decoded_frames=i,frame_count_pass=i==m['total_frames'],dimensions=list(sizes),black_frames=black,pauses=pauses,answer_reveal_checks=answers,protected_files_unchanged=all(sha(Path(p))==h for p,h in m['protected_hashes'].items()),sampled_frames=len(picked),direct_listening=False,real_time_motion_review=False)
(out/'qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
cmd=[str(root/'.video-venv/bin/python'),str(root/'scripts/video/transition_guard.py'),str(src),'--outdir',str(out/'transitions')]
for row in m['boundaries']:cmd+=['--boundary',f"{row['frame']}:{row['label']}"]
subprocess.run(cmd,check=True)
