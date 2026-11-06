from pathlib import Path
import subprocess,json,imageio_ffmpeg,hashlib
root=Path.cwd(); out=root/'video-audit/learn-with-ai-donor-review-2026-11-06'; ff=imageio_ffmpeg.get_ffmpeg_exe()
base=root/'Prompts/learn-with-ai-3.mp4'; donor=root/'Prompts/learn-reroll-2.mp4'
legs=[(0,138.80,145.00,'Base upload list'),(1,25.80,35.15,'Donor complete output list'),(0,154.90,157.90,'Base exact takeaway'),(0,168.75,174.60,'Base four-moves introduction; intervening guarantee removed')]
filters=[]
for i,(src,start,end,label) in enumerate(legs):
 d=end-start
 filters.append(f'[{src}:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=mono,afade=t=in:st=0:d=0.008,afade=t=out:st={d-0.008:.6f}:d=0.008[a{i}]')
filters.append(''.join(f'[a{i}]' for i in range(len(legs)))+f'concat=n={len(legs)}:v=0:a=1[out]')
cmd=[ff,'-hide_banner','-y','-i',str(base),'-i',str(donor),'-filter_complex',';'.join(filters),'-map','[out]','-c:a','pcm_s16le',str(out/'output-splice-preview.wav')]
r=subprocess.run(cmd,capture_output=True,text=True);(out/'preview-encode.log').write_text(r.stderr);assert r.returncode==0
cursor=0;rows=[]
for src,start,end,label in legs:
 rows.append({'source':str([base,donor][src].relative_to(root)),'source_start':start,'source_end':end,'preview_start':round(cursor,4),'preview_end':round(cursor+end-start,4),'purpose':label});cursor+=end-start
(out/'preview-manifest.json').write_text(json.dumps({'scope':'Audio audition preview only; not full video or listening-certified repair','legs':rows,'duration':cursor,'treatment':'48kHz mono; 8ms edge fades at measured quiet boundaries; no gain adjustment, added silence, or synthesized audio','sha256':hashlib.sha256((out/'output-splice-preview.wav').read_bytes()).hexdigest()},indent=2)+'\n')
print('Created',out/'output-splice-preview.wav','duration',cursor)
