#!/usr/bin/env python3
"""Approved visual-only repair of the published How AI Answers. Review only."""
from pathlib import Path
import argparse,json,subprocess
import cv2,imageio_ffmpeg
from editspec_build import Build,Reader,sha
from build_embeddings_v7 import Renderer
from ken_burns_path import fit_window
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'course-assets/how-ai-answers/how-ai-answers.mp4'
EXPECTED='c0e56437479d467ffaea26ff6ca51e93019e7cb18a041f3b980b038f7ff3f1fa'
OUT=ROOT/'video-audit/how-ai-answers-repair-2026-09-28-v7'
DEST=ROOT/'Prompts/how-ai-answers-v7.mp4'
TOTAL=7617;FPS=30
SPANS={'b1':(400,1472),'b2':(1472,2517),'b3':(3106,5008),'b4':(6121,7319)}
ASSETS={'b1':'before-answer-begins','b2':'where-answer-begins','b3':'token-by-token','b4':'building-an-answer'}
P='#4f2fc4';B='#1652f0';T='#0e8f86';G='#0f7a4a';N='#6e51ff'
def fr(t):return round(t*FPS)
def runs(mapped):
 rows=[]
 for f,item in enumerate(mapped):
  label=item[0] if item else 'original'
  if not rows or rows[-1]['label']!=label:rows.append(dict(label=label,start_frame=f,end_frame=f+1))
  else:rows[-1]['end_frame']=f+1
 return rows

def setup():
 snap=Path(json.loads((OUT/'source-snapshot.json').read_text())['path']);assert sha(snap)==EXPECTED
 build=Build(ROOT,snap,OUT,DEST);specs={};boards={};renderers={};mapped=[None]*TOTAL
 for key,name in ASSETS.items():
  asset=ROOT/f'course-assets/how-ai-answers/how-ai-answers-{name}.jpg'
  canvas,cw,ch,ox,oy=build.compose(asset,key);a,z=SPANS[key];full=[cw/2,ch/2,cw]
  specs[key]=dict(image=str(canvas),fps=30,out_w=1280,out_h=720,upscale=3,beats=[dict(label='full view',frames=z-a,**{'from':full,'to':full})],rings=[])
  boards[key]=dict(asset=str(asset.relative_to(ROOT)),sha256=sha(asset),start_frame=a,end_frame=z,canvas_offset=[ox,oy],density='dense' if key in ['b1','b3'] else 'compact')
  for f in range(a,z):mapped[f]=(key,f-a)
 def rect(key,xyxy):
  x,y,z,w=xyxy;ox,oy=boards[key]['canvas_offset'];return [x+ox,y+oy,z-x,w-y]
 def ring(key,a,z,xyxy,color,label):
  a,z=fr(a),fr(z);start,end=SPANS[key]
  specs[key]['rings'].append(dict(start=a-start,end=z-start,rect=rect(key,xyxy),color=color,pad=0,radius=16,label=label))
 def camera(key,xyxy):return fit_window(dict(fit=rect(key,xyxy),margin=18),16/9,1280,3)
 def path(key,pts):
  specs[key]['beats']=[dict(label=z[2],frames=z[0]-a[0],**{'from':a[1],'to':z[1]}) for a,z in zip(pts,pts[1:])]
  assert sum(x['frames'] for x in specs[key]['beats'])==SPANS[key][1]-SPANS[key][0]
 # Full shared-white-box height. All columns include illustration, number, heading and explanation.
 cols=[[80,280,414,872],[448,280,782,872],[816,280,1150,872],[1184,280,1518,872]]
 cams=[camera('b1',r) for r in cols];full=specs['b1']['beats'][0]['from']
 path('b1',[(400,full,'open'),(fr(16.06),full,'full setup'),(fr(16.86),cams[0],'Tokens zoom'),(fr(20.3),cams[0],'Tokens hold'),(fr(20.98),cams[1],'Positions pan'),(fr(25.6),cams[1],'Positions hold'),(fr(26.24),cams[2],'Starting Vectors pan'),(fr(31.1),cams[2],'Starting Vectors hold'),(fr(31.8),cams[3],'Through Layers pan'),(fr(39.48),cams[3],'Through Layers hold'),(fr(40.3),full,'pull back'),(1472,full,'takeaway')])
 for r,c,a,z,l in zip(cols,[P,B,T,G],[16.06,20.98,26.24,31.8],[20.3,25.6,31.1,42.92],['Tokens','Positions','Starting Vectors','Through Layers']):ring('b1',a,z,r,c,l)
 ring('b1',42.92,1472/30,[40,905,1560,992],N,'takeaway')
 ring('b2',59.06,66.5,[80,120,788,693],P,'The Question')
 ring('b2',66.5,75.08,[818,120,1522,693],B,'The Final Token')
 ring('b2',75.08,2517/30,[40,718,1560,812],N,'takeaway')
 # Include the entire prediction group, including the label and selected token below its table.
 p1=[80,280,600,958];p5=[1000,280,1520,958]
 c1,c5=camera('b3',p1),camera('b3',p5);assert abs(c1[2]-c5[2])<.001
 full=specs['b3']['beats'][0]['from']
 path('b3',[(3106,full,'open'),(fr(105.533333),full,'two-second setup'),(fr(106.333333),c1,'Prediction 1 zoom'),(fr(123.1),c1,'Prediction 1 hold'),(fr(123.78),full,'middle pullback'),(fr(135.9),full,'middle and return setup'),(fr(136.7),c5,'Prediction 5 zoom'),(fr(161.68),c5,'Prediction 5 hold'),(fr(162.48),full,'takeaway pullback'),(5008,full,'takeaway')])
 for a,z,r,c,l in [
  (106.18,112.55,p1,P,'Prediction 1'),(112.55,119.95,[104,528,578,726],P,'first probabilities'),(119.95,123.78,[292,856,390,918],P,'select You'),
  (123.78,134.98,[632,468,968,637],B,'three more predictions'),
  (134.98,138.06,p5,T,'Prediction 5'),(138.06,141.72,[1040,366,1492,458],T,'reply so far'),(141.72,147.32,[1386,393,1480,457],T,'him final token'),
  (147.32,152.04,p5,T,'longer context'),(152.04,158.96,[1022,528,1498,726],T,'dog-name probabilities'),(158.96,162.5,[1203,856,1320,918],T,'select Spot'),
  (162.5,5008/30,[40,995,1560,1090],N,'complete answer')]:ring('b3',a,z,r,c,l)
 for a,z,r,c,l in [(207.92,219.6,[80,315,418,788],P,'Rank'),(219.6,226.96,[450,315,786,788],B,'Pick'),(226.96,233.32,[818,315,1152,788],T,'Add'),(233.32,7319/30,[1185,315,1520,788],G,'Repeat')]:ring('b4',a,z,r,c,l)
 # Reuse only verified non-conflicting drawings from this exact source.
 reuse=[]
 def hold(a,z,src,label):
  aa,zz,ss=fr(a),fr(z),fr(src)
  for f in range(aa,zz):mapped[f]=(label,ss)
  reuse.append(dict(start_frame=aa,end_frame=zz,source_start=ss,source_end=ss+1,kind='hold',label=label))
 hold(54,58,12,'question-break')
 hold(88.3,2819/30,12,'replace-invalid-probabilities')
 hold(174.933333,183.933333,171,'replace-conflicting-probabilities')
 # Existing animation writes could, name, him; freeze before next-prediction graphics enter.
 a,z,ss,stop=fr(125.7),fr(133.9),fr(184.8),fr(186.1)
 for f in range(a,z):mapped[f]=('intermediate-token-break',min(ss+f-a,stop))
 reuse.append(dict(start_frame=a,end_frame=z,source_start=ss,source_end=stop+1,kind='play-then-hold',label='intermediate-token-break'))
 hold(228.5,232.5,195.5,'completed-answer-break')
 for key,s in specs.items():
  (OUT/f'leg-{key}.json').write_text(json.dumps(s,indent=2)+'\n');renderers[key]=Renderer(s)
 return snap,boards,specs,renderers,mapped,reuse

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a candidate';assert sha(SOURCE)==EXPECTED
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 snap,boards,specs,rs,mapped,reuse=setup();protected={str(p):sha(p) for p in [SOURCE,ROOT/'index.html',ROOT/'lessons/how-ai-answers.md',ROOT/'Prompts/how-ai-answers-video-prompt.txt',*sorted((ROOT/'course-assets/how-ai-answers').glob('*.jpg'))]}
 states=[]
 for key,r in rs.items():
  wanted={0,len(r.cameras)-1};at=0
  for beat in specs[key]['beats']:
   z=at+beat['frames'];wanted|={at,(at+z-1)//2,z-1};at=z
  for ring in r.rings:wanted|={ring[0],min(ring[0]+20,ring[1]-1),ring[1]-1}
  for f,item in enumerate(mapped):
   if item and item[0]==key and item[1] in wanted:
    im,_,geo=r.at(item[1]);p=OUT/'preview'/f'{f:05d}-{key}.jpg';cv2.imwrite(str(p),im);states.append(dict(output_frame=f,key=key,local_frame=item[1],path=str(p),rings=geo))
 visual=runs(mapped)
 old=json.loads((ROOT/'video-audit/understand-ai-section-review-2026-09-27/how-ai-answers/guard/transition-guard.json').read_text())
 # Real source cuts plus visual-repair edges; camera moves are not new scenes.
 boundaries=sorted(set([400,1472,2517,2649,2819,3106,5008,5248,5518,6121,7319]+[x['start_frame'] for x in visual[1:]]))
 m=dict(source=str(SOURCE),source_sha256=EXPECTED,snapshot=str(snap),candidate=str(DEST),frames=TOTAL,fps=FPS,duration=TOTAL/FPS,boards=boards,specs=specs,prepared_states=states,visual_timeline=visual,visual_reuse=reuse,boundaries=boundaries,protected=protected,audio='copy source AAC stream unchanged; no audio processing',close_span_frames=[7319,TOTAL],approval='David: build it please. Approved September 28 How AI Answers visual repair plan; review only, no publication.',listening_performed=False)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('Prepared',TOTAL,'frames; preview states',len(states),flush=True)
 if args.prepare_only:return
 # Separate monotonic original reader and cached donor frames; no seek-back errors.
 donor_ids=sorted({it[1] for it in mapped if it and it[0] not in rs});rd=Reader(snap);donors={f:rd.at(f).copy() for f in donor_ids};rd.c.release()
 ff=imageio_ffmpeg.get_ffmpeg_exe();proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(snap),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 rd=Reader(snap)
 for f,item in enumerate(mapped):
  im=rd.at(f) if item is None else rs[item[0]].at(item[1])[0] if item[0] in rs else donors[item[1]]
  proc.stdin.write(im.tobytes())
  if f%1000==999:print('Rendered',f+1,flush=True)
 proc.stdin.close();assert proc.wait()==0;rd.c.release();assert all(sha(Path(p))==h for p,h in protected.items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
