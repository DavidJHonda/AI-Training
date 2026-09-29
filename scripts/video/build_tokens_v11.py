#!/usr/bin/env python3
"""Narrow owner-requested repair: spoken-element outlines on Building Blocks."""
from pathlib import Path
import argparse, json, subprocess
import cv2, imageio_ffmpeg
from editspec_build import Build, sha
from build_tokens_v9 import Renderer

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/tokens-v10c.mp4'
DEST=ROOT/'Prompts/tokens-v11.mp4'
OUT=ROOT/'video-audit/tokens-element-highlights-2026-09-29-v11'
OLD=ROOT/'video-audit/tokens-build-2026-09-29-v10'
EXPECTED='0b2d7b8e47ca4371f211952a617d29ab1803fc5097a09394d3a59df4572be2f5'
START,END,TOTAL=1787,2275,6337
# Image coordinates, before the existing canvas offset of (657, 61).
# Individual subword onsets come from the contextual medium.en word alignment;
# whole-word ASR had incorrectly collapsed the spoken pieces to one word.
TARGETS=[
 ('input: unbelievable',69.68,71.74,[395,616,230,99],'#6e51ff'),
 ('three output tokens',71.74,73.62,[705,714,435,168],'#6e51ff'),
 ('un',73.62,74.04,[708,716,148,143],'#0f7a4a'),
 ('belie',74.04,74.78,[854,726,147,143],'#a9760c'),
 ('vable',74.78,END/30,[991,737,145,140],'#1652f0'),
]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert sha(SRC)==EXPECTED;assert not DEST.exists(),'Never overwrite a candidate'
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 spec=json.loads((OLD/'leg-blocks.json').read_text());spec['rings']=[]
 # Recreate regenerable canvas scratch after local-shipping cleanup.
 b=Build(ROOT,SRC,OUT,DEST)
 canvas,cw,ch,ox,oy=b.compose(ROOT/'course-assets/tokens/tokens-building-blocks.jpg','blocks')
 assert (cw,ch,ox,oy)==(2914,1640,657,61)
 spec['image']=str(canvas)
 for label,a,b,rect,color in TARGETS:
  x,y,w,h=rect
  spec['rings'].append(dict(start=round(a*30)-START,end=round(b*30)-START,rect=[x+657,y+61,w,h],color=color,pad=0,radius=12))
 renderer=Renderer(spec);(OUT/'leg-blocks.json').write_text(json.dumps(spec,indent=2)+'\n')
 states=[]
 for label,a,b,rect,col in TARGETS:
  n=round(a*30)-START+3;im,_,geometry=renderer.at(n);p=OUT/'preview'/f'{round(a*30):06d}.png';cv2.imwrite(str(p),im)
  states.append(dict(label=label,start_frame=round(a*30),end_frame=round(b*30),image_rect=rect,preview=str(p),geometry=geometry))
 protected=[SRC,ROOT/'course-assets/tokens/tokens.mp4',ROOT/'course-assets/tokens/tokens-building-blocks.jpg']
 manifest=dict(source=str(SRC),source_sha256=EXPECTED,candidate=str(DEST),scope='Narrow visual-only correction to Building Blocks highlights; owner instruction 2026-09-29',frames=TOTAL,fps=30,duration=TOTAL/30,replaced_frames=[START,END],targets=states,camera='Existing complete composition; no added crop or zoom',ring_width_px=4,audio='Copy the original AAC stream without re-encoding',protected={str(p):sha(p) for p in protected},listening='Onsets aligned using existing and contextual ASR; not directly auditioned')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 if args.prepare_only:return
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 p=subprocess.Popen([ff,'-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 cap=cv2.VideoCapture(str(SRC));n=0
 while True:
  ok,im=cap.read()
  if not ok:break
  if START<=n<END:im=renderer.at(n-START)[0]
  p.stdin.write(im.tobytes());n+=1
  if n%1500==0:print('Rendered',n,'/',TOTAL,flush=True)
 p.stdin.close();assert p.wait()==0;cap.release();assert n==TOTAL
 assert all(sha(Path(k))==v for k,v in manifest['protected'].items())
 manifest['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(DEST,flush=True)
if __name__=='__main__':main()
