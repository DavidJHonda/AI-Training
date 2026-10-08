#!/usr/bin/env python3
"""Approved companion-video edit: original illustrations and a quieter close.

Source narration ends after 'Every mechanical gear of the plan functioned exactly
as designed.' The new AI bridge is a silent reading card, also present as page
text; no synthetic replacement voice is introduced. This is supplementary TRY IT
material, not a replacement for the Unexpected Results overview.
"""
from pathlib import Path
import hashlib,json,subprocess
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/rat story.mp4'
ASSETS=ROOT/'course-assets/unexpected-results/rat-story'
AUDIT=ROOT/'video-audit/rat-story-2026-10-07'
OUT=ASSETS/'rat-story.mp4'
FPS=30
CUT=7656 # 255.2s: measured silence after 'designed', before 'If'.
CLOSE_FRAMES=384 # 12.8 seconds to read the two-sentence bridge.
REPLACEMENTS=[(264,483,'hanoi-street.jpg'),(1057,1235,'hanoi-street.jpg'),(4799,5020,'hanoi-market.jpg')]
BRIDGE='That’s why predicting AI’s effects takes more than understanding the technology. We also have to watch what people do with it.'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def make_close():
    scale=2
    im=Image.new('RGB',(1280*scale,720*scale),'#f7f4eb')
    d=ImageDraw.Draw(im)
    font_path=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
    def font(size,bold=False):
        f=ImageFont.truetype(str(font_path),size*scale)
        f.set_variation_by_axes([700 if bold else 400]);return f
    def text(x,y,t,size,color='#0e0a1f',bold=False):d.text((x*scale,y*scale),t,font=font(size,bold),fill=color)
    text(96,92,'UNEXPECTED RESULTS',22,'#2f7d4f',True)
    text(96,164,'Watch what people do.',56,bold=True)
    d.line((96*scale,265*scale,1184*scale,265*scale),fill='#b8cbb8',width=2*scale)
    for y,t in [(309,'That’s why predicting AI’s effects takes more'),(363,'than understanding the technology.'),(453,'We also have to watch what people do with it.')]:
        text(96,y,t,36,'#3a3550')
    im.resize((1280,720),Image.Resampling.LANCZOS).save(ASSETS/'ai-bridge.jpg',quality=95)

def main():
    ASSETS.mkdir(parents=True,exist_ok=True);AUDIT.mkdir(parents=True,exist_ok=True)
    make_close()
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    graph=['[0:v]trim=end_frame=7656,setpts=PTS-STARTPTS,setsar=1[base]','[1:v]split=2[street1][street2]']
    inputs=['street1','street2','2:v']
    previous='base'
    for i,((start,end,name),inp) in enumerate(zip(REPLACEMENTS,inputs)):
        n=end-start
        graph.append(f"[{inp}]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,zoompan=z='1+0.02*on/{n-1}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={n}:s=1280x720:fps=30,setsar=1,setpts=PTS-STARTPTS+{start}/(30*TB)[art{i}]")
        graph.append(f"[{previous}][art{i}]overlay=eof_action=pass:enable='between(n,{start},{end-1})'[v{i}]")
        previous=f'v{i}'
    graph.append(f'[3:v]zoompan=z=1:d={CLOSE_FRAMES}:s=1280x720:fps=30,setsar=1,setpts=PTS-STARTPTS[close]')
    graph.append(f'[{previous}][close]concat=n=2:v=1:a=0,format=yuv420p[v]')
    graph.append('[0:a]atrim=end=255.2,asetpts=PTS-STARTPTS,afade=t=out:st=255.17:d=0.03,apad=pad_dur=12.8,atrim=end=268[a]')
    cmd=[ff,'-hide_banner','-loglevel','warning','-y','-i',str(SRC),'-i',str(ASSETS/'hanoi-street.jpg'),'-i',str(ASSETS/'hanoi-market.jpg'),'-i',str(ASSETS/'ai-bridge.jpg'),'-filter_complex',';'.join(graph),'-map','[v]','-map','[a]','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','160k','-movflags','+faststart',str(OUT)]
    subprocess.run(cmd,check=True,cwd=ROOT)
    record={'source':str(SRC.relative_to(ROOT)),'source_sha256':sha(SRC),'output':str(OUT.relative_to(ROOT)),'output_sha256':sha(OUT),'fps':30,'expected_frames':CUT+CLOSE_FRAMES,'expected_duration':268,'replacements':[{'start_frame':a,'end_frame_exclusive':b,'asset':c,'asset_sha256':sha(ASSETS/c),'camera':'2 percent centered push'} for a,b,c in REPLACEMENTS],'narration_cut_seconds':255.2,'last_retained_sentence':'Every mechanical gear of the plan functioned exactly as designed.','removed_ending':'If you build a system that rewards a proxy instead of the actual objective, human ingenuity will ruthlessly optimize for that proxy. And in doing so, they will weaponize the system right back against its creators.','bridge':BRIDGE,'bridge_delivery':'12.8-second unvoiced closing card and accessible page text','scope':'Supplementary story edit: replace all three archival-photo spans with two original illustrations, trim harsh ending, remove source outro. Preserve remaining source visuals/audio.','command':cmd}
    (AUDIT/'edit-manifest.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:record[k] for k in ['output','output_sha256','expected_frames','expected_duration']},indent=2))

if __name__=='__main__':main()
