#!/usr/bin/env python3
"""Know the App, approved roll-6 production. Original audio copied; review only."""
from pathlib import Path
import json,subprocess,sys
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
from editspec_build import Build,Reader,sha,fr
from build_creative_thinking_v8 import BoardRenderer
from gemini_mark import clean_frame,glyph_mask
from make_close_board import close_board_asset,compose_canonical_for_video
from ken_burns_path import smoothstep
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/know-the-app-build-2026-10-08-v2';DEST=ROOT/'Prompts/know-the-app-v2.mp4';SRC=ROOT/'Prompts/know-the-app-6.mp4';FF=imageio_ffmpeg.get_ffmpeg_exe()
ROWS=[]
def row(s,e,label,visual='source',roll=6,a=None,z=None):
 ROWS.append(dict(start_frame=s,end_frame=e,label=label,visual=visual,source=str(ROOT/f'Prompts/know-the-app-{roll}.mp4'),video_start=s if a is None else a,video_end=e if z is None else z))
def prepare():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 protected=[ROOT/f'Prompts/know-the-app-{r}.mp4' for r in (4,5,6)]+list((ROOT/'course-assets/your-choices').glob('*.jpg'))+[ROOT/'lessons/your-choices.md',ROOT/'course-assets/your-choices/your-choices.mp4']
 b=Build(ROOT,SRC,OUT,DEST,protected=protected)
 for key,asset,s,e,bottom,ons,pull in [('model','choose-tool',1672,2623,914,[60.46,68.64],80.76),('thinking','thinking',3653,4933,996,[125.02,138.08],159.26),('research','research',6182,7420,1037,[209.22,219.76],240.14)]:
  targets=[dict(label=label,at=t,rects=[rect],color=c,radius=14) for label,t,rect,c in zip(['Left complete card','Right complete card'],ons,[(40,118,784,bottom),(816,118,1560,bottom)],['#4f2fc4','#1652f0'])]
  b.board(key,ROOT/f'course-assets/your-choices/your-choices-{asset}.jpg',s,e,'compact',targets,pullback_at=pull,push=False)
 boards={k:BoardRenderer(OUT/f'leg-{k}.json') for k in b.boards}
 compose_canonical_for_video(close_board_asset('choosemodel'),OUT/'close.png','#ffffff')
 # Drawn donor clips preserve their native movement; mapping never crosses a donor scene boundary.
 row(0,195,'Phone camera: point and tap',roll=4,a=0,z=172)
 row(195,234,'Dark photo',roll=4,a=275,z=414)
 row(234,286,'Turn on flash',roll=4,a=414,z=517)
 row(286,350,'High in hockey stands',roll=4,a=517,z=591)
 row(350,456,'Zoom toward player',roll=4,a=591,z=706)
 row(456,662,'Pictures and choices: retained gallery')
 row(662,936,'Optional three-choice schematic; availability label repair')
 row(936,1082,'Useful result drawing')
 row(1082,1254,'LLM inside the app: retain initial engine reveal')
 row(1254,1672,'Drawn engine replaces numeric model benchmark',roll=5,a=1784,z=2161)
 row(1672,2220,'Which Model: title and both cards','model')
 row(2220,2400,'Business planning drawing',roll=4,a=2783,z=2975)
 row(2400,2623,'Which Model: finish example and takeaway','model')
 row(2623,2813,'Retained engine/prompt complexity analogy')
 row(2813,3005,'Retained engine versus human essay drawing')
 row(3005,3653,'Retained outline animation; proposed-answer label repair')
 row(3653,4380,'How Much Thinking: title and card explanations','thinking')
 row(4380,4620,'Project planning papers',roll=5,a=3600,z=3840)
 row(4620,4933,'How Much Thinking: finish constraints and takeaway','thinking')
 row(4933,5280,'Retained thinking process and research transition; answer label repair')
 row(5280,5412,'Burger: familiar information',roll=4,a=4435,z=4656)
 row(5412,5730,'House, map and comparison',roll=4,a=4656,z=4757)
 row(5730,6182,'Retained source gathering and research comparison')
 row(6182,6810,'How Much Research: title and both cards','research')
 row(6810,7050,'University comparison maps and calculator',roll=5,a=5500,z=5740)
 row(7050,7420,'How Much Research: requirements and takeaway','research')
 row(7420,7685,'Retained comparison of sources')
 row(7685,7909,'Canonical close, hold/push/settle','close')
 assert all(ROWS[i]['end_frame']==ROWS[i+1]['start_frame'] for i in range(len(ROWS)-1))
 m=dict(source=str(SRC),source_sha256=sha(SRC),output=str(DEST),total_frames=7909,duration=7909/30,fps=30,audio='Copied unchanged from roll 6',boards=b.boards,timeline=ROWS,boundaries=[dict(frame=r['start_frame'],label=r['label']) for r in ROWS[1:]],protected_hashes=b.hashes,close=dict(start_frame=7685,hold=48,push=150,settled=26,asset=str(close_board_asset('choosemodel'))),adjustments=['Exact donor cut edges tightened so borrowed board frames never leak into cutaways.','More Thinking onset uses word-timed 138.08; Deep Research uses 219.76.','Optional-controls label and proposed-answer labels repaired without changing narration.'])
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
 for k,br in boards.items():
  for i in [0]+[x['start']+20 for x in br.spec['rings']]+[sum(x['frames'] for x in br.spec['beats'])-1]:cv2.imwrite(str(OUT/'preview'/f'{k}-{i}.jpg'),br.frame(i))
 return b,boards

def patch(im,f):
 # All rectangles are stable output-pixel positions, inspected in the source detail sequences.
 pic=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(pic)
 def box(rect,text,size=18,bg='#eeefe4',color='#365069'):
  d.rectangle(rect,fill=bg);font=ImageFont.truetype(str(ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'),size)
  x0,y0,x1,y1=rect;d.text(((x0+x1)/2,(y0+y1)/2),text,font=font,fill=color,anchor='mm',align='center')
 if 780<=f<936:box((826,158,1008,211),'If available',18)
 if 3540<=f<3653:
  box((870,212,1080,253),'Proposed answer',19)
  box((873,347,1080,443),'Review before using',17)
  box((390,469,578,500),'Working through the task',14,bg='#252b2e',color='#eeeeee')
 if 5100<=f<5195:
  box((995,375,1085,409),'Review it',16)
 return cv2.cvtColor(np.array(pic),cv2.COLOR_RGB2BGR)

def render(b,boards):
 assert not DEST.exists(),'Never overwrite candidate'
 close=cv2.imread(str(OUT/'close.png'));mask=glyph_mask();counts={};readers={}
 proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','17','-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for r in ROWS:
  n=r['end_frame']-r['start_frame'];rd=None
  if r['visual']=='source':rd=Reader(r['source'])
  for j in range(n):
   f=r['start_frame']+j
   if r['visual'] in boards:im=boards[r['visual']].frame(f-b.boards[r['visual']]['src_in'])
   elif r['visual']=='close':
    z=1+.2*smoothstep(float(np.clip((f-7685-48)/149,0,1)));h,w=close.shape[:2];ww=w/z;hh=ww*9/16
    im=cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   else:
    vf=r['video_start']+round(j*(r['video_end']-r['video_start']-1)/max(1,n-1));im=rd.at(vf)
    im,how=clean_frame(im,mask);counts[how]=counts.get(how,0)+1
    if r['source']==str(SRC):im=patch(im,f)
   if f%180==0 or f in [1814,2059,3752,4162,6277,6600,7908]:cv2.imwrite(str(OUT/'preview'/f'output-{f:05}.jpg'),im)
   proc.stdin.write(im.tobytes())
  if rd:rd.c.release()
  print(f'{r["end_frame"]}/7909 {r["label"]}',flush=True)
 proc.stdin.close();assert proc.wait()==0
 m=json.loads((OUT/'edit-manifest.json').read_text());m.update(render_sha256=sha(DEST),corner_mark=counts,protected_unchanged={p:sha(p)==h for p,h in b.hashes.items()});assert all(m['protected_unchanged'].values());(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
 print('COMPLETE',DEST,flush=True)
if __name__=='__main__':
 cv2.setNumThreads(2);b,boards=prepare()
 if '--preview' not in sys.argv:render(b,boards)
