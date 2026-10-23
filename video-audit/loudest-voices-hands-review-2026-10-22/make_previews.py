from pathlib import Path
import subprocess,json
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
FF=imageio_ffmpeg.get_ffmpeg_exe()
LV=ROOT/'course-assets/loudest-voices/loudest-voices.mp4'
HANDS=ROOT/'course-assets/in-your-hands/in-your-hands.mp4'
def run(args):
 subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*args],check=True)
def encode_end(dest):
 return ['-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT/dest)]
# Whole spoken thoughts with cuts inside measured quiet gaps, frame-aligned at 30 fps.
run(['-ss','208','-t',str(216+8/30-208),'-i',str(LV),'-ss','35.8','-t','15','-i',str(HANDS),'-filter_complex','[0:v]setpts=PTS-STARTPTS[v0];[0:a]asetpts=PTS-STARTPTS[a0];[1:v]setpts=PTS-STARTPTS[v1];[1:a]asetpts=PTS-STARTPTS[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]','-map','[v]','-map','[a]',*encode_end('01-into-in-your-hands.mp4')])
# The canonical current close replaces the donor's preceding Three Moves image.
run(['-i',str(OUT/'close-canvas.png'),'-ss','167.3','-t','16.3','-i',str(HANDS),'-filter_complex',"[0:v]zoompan=z='if(lt(on,48),1,if(lt(on,198),1+0.2*(on-48)/149,1.2))':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=489:s=1280x720:fps=30,setsar=1[v]",'-map','[v]','-map','1:a','-t','16.3',*encode_end('close-preview.mp4')])
run(['-ss','104','-t','11.9','-i',str(HANDS),'-i',str(OUT/'close-preview.mp4'),'-filter_complex','[0:v]setpts=PTS-STARTPTS[v0];[0:a]asetpts=PTS-STARTPTS[a0];[1:v]setpts=PTS-STARTPTS[v1];[1:a]asetpts=PTS-STARTPTS[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]','-map','[v]','-map','[a]',*encode_end('02-into-close.mp4')])
plan={'status':'proposed; previews only; no full candidate or installation','segments':[{'source':str(LV.relative_to(ROOT)),'start':0,'end':216+8/30},{'source':str(HANDS.relative_to(ROOT)),'start':35.8,'end':115.9},{'source':str(HANDS.relative_to(ROOT)),'start':167.3,'end':183.6,'visual':'Current canonical Loudest Voices close with standard hold/push/hold'}]}
plan['duration']=sum(x['end']-x['start'] for x in plan['segments'])
(OUT/'proposed-edit.json').write_text(json.dumps(plan,indent=2)+'\n')
print('Transition previews complete; proposed duration',plan['duration'])
