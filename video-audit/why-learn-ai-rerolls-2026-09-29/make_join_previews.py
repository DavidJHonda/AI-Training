from pathlib import Path
import json,subprocess
import imageio_ffmpeg
p=Path(__file__).parent;ff=imageio_ffmpeg.get_ffmpeg_exe()
plan=[
 {'name':'press','base':[26.997506,33.396724],'donor':[25.408118,37.587471]},
 {'name':'practice-design','base':[95.938810,139.204909],'donor':[70.163866,117.921712]},
 {'name':'history-quote','base':[193.754989,222.732120],'donor':[154.253277,178.639705]},
]
for g in plan:
 a,b=g['base'];c,d=g['donor'];g['duration_change']=(d-c)-(b-a)
 filt=f'[0:a]atrim=start={a-4}:end={a},asetpts=PTS-STARTPTS[pre];[1:a]atrim=start={c}:end={d},asetpts=PTS-STARTPTS[donor];[0:a]atrim=start={b}:end={b+4},asetpts=PTS-STARTPTS[post];[pre][donor][post]concat=n=3:v=0:a=1[out]'
 target=p/f"join-preview-{g['name']}.mp3"
 subprocess.run([ff,'-v','error','-y','-i','Prompts/why-learn-ai-2.mp4','-i','Prompts/why-learn-ai-1.mp4','-filter_complex',filt,'-map','[out]','-c:a','libmp3lame','-q:a','3',str(target)],check=True)
 g['preview']=target.name
 g['status']='proposed; cut points inside measured silence; not auditioned; no level or cadence certification'
(p/'proposed-grafts.json').write_text(json.dumps({'base':'Prompts/why-learn-ai-2.mp4','donor':'Prompts/why-learn-ai-1.mp4','grafts':plan,'raw_duration_after_grafts':229.13333333333333+sum(g['duration_change'] for g in plan)},indent=2)+'\n')
print('Three unprocessed audio context previews saved; no production video built.')
