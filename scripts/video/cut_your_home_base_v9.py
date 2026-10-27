#!/usr/bin/env python3
"""Remove the retired real-world example; preserve the rest of the installed v8."""
from pathlib import Path
import json,subprocess
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Reader,sha,writewav
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/your-home-base-cut-v9-2026-10-22'
SOURCE=ROOT/'Prompts/your-home-base-v8.mp4'
DEST=ROOT/'Prompts/your-home-base-v9.mp4'
EXPECTED='28dbb9fbdf3be6cbf2a6fb57a1efb0ccf5b29b4757b66a74714896a41233905f'
KEEP=[(0,5376),(6525,6852)]
def mapping():return [n for a,z in KEEP for n in range(a,z)]
def pcm(p):
 return np.frombuffer(subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','f32le','pipe:1']),np.float32).copy()
def main():
 assert not DEST.exists(),'Do not overwrite reviewed candidates'
 assert sha(SOURCE)==EXPECTED
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 protected={str(p):sha(p) for p in [ROOT/'index.html',ROOT/'lessons/your-home-base.md',ROOT/'course-assets/your-home-base/your-home-base.mp4',*sorted((ROOT/'course-assets/your-home-base').glob('*.jpg'))]}
 a=pcm(SOURCE);parts=[a[x*1600:z*1600].copy() for x,z in KEEP]
 parts[0][-240:]*=np.linspace(1,0,240);parts[1][:240]*=np.linspace(0,1,240)
 edited=np.concatenate(parts);writewav(OUT/'edited.wav',edited*32768)
 frames=mapping();assert len(frames)==5703 and len(edited)==5703*1600
 m=dict(source=str(SOURCE),source_sha256=EXPECTED,candidate=str(DEST),fps=30,frames=5703,duration=5703/30,keep=KEEP,cut=[5376,6525],boundary=5376,protected=protected,
 scope='Remove the full real-world example and How We Used the Big Three board. Preserve every other source frame, narration, timing and existing closing treatment.',
 join='...that does not guarantee they are right. → Pick a home base. Learn it deeply.',
 audio='5 ms ramps within measured silence at the single new join; no gain change or inserted pause.',
 source_limitation='One additional encode from verified finished v8 (the earlier v6 source has been replaced by this installed version); no visual redesign.',publication='Review only; installed course unchanged.')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 r=Reader(SOURCE)
 for out,n in enumerate(frames):
  im=r.at(n);p.stdin.write(im.tobytes())
  if out in [0,3000,4500,5375,5376,5385,5424,5574,5702]:cv2.imwrite(str(OUT/'preview'/f'planned-{out:05d}.jpg'),im)
  if out%1000==999:print('Rendered',out+1,flush=True)
 p.stdin.close();assert p.wait()==0;r.c.release()
 assert all(sha(Path(p))==h for p,h in protected.items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST)
if __name__=='__main__':main()
