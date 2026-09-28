#!/usr/bin/env python3
"""V8: geographic-map bridge, shorter drinks, live-style neighborhood framing."""
from pathlib import Path
import argparse,json,subprocess,math,functools
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
from editspec_build import Build,Reader,sha,fr,readwav,writewav,banner_rect
from build_embeddings_v7 import Renderer
from gemini_mark import clean_frame,glyph_mask

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/vector-space-build-2026-09-28-v8'
DEST=ROOT/'Prompts/vector-space-v8.mp4'
R1=ROOT/'Prompts/vector-space-1.mp4';R2=ROOT/'Prompts/vector-space-2.mp4';R3=ROOT/'Prompts/vector-space-3.mp4'
LIVE=ROOT/'course-assets/vector-space/vector-space.mp4'
D=ROOT/'course-assets/vector-space'
ASSETS={k:D/f'vector-space-{v}.jpg' for k,v in dict(cities='cities',closest='cities-closest',taste='taste',nbhd='neighborhoods',drink='closest-drink',ctx='meaning-map').items()}
EXPECTED={R2:'0b4be8e5b296653dbb313a53c41f7347d40b2544c5dc458e5a3a5625acf1012a',R1:'3df4bc45f7b01223bfd7ed8892c0ddae6f68549482f705c3834a11c6984a56b5',R3:'6540e2fa2c8a67753efecaaf7d7a9612e82c812209141f44893ca72acf29e198',LIVE:'4873fac38f54ff14ebaff06b0787a8922e9e15bb99712b0332d767ad41f5b563'}
# Complete-sentence edits; half-open source frames at 30 fps.
AUDIO=[('r3',0,950,'opening through vector space'),
       ('r2',965,1074,'standard geographic map bridge'),
       ('r3',950,1264,'city map introduction and Dallas'),
       ('r1',1452,1709,'Mountain View and New York'),
       ('r3',1398,3517,'city answers drinks and neighborhoods'),
       ('r1',4301,4404,'mystery introduction without number readout'),
       ('r3',3863,5087,'Pepsi calculation training and sentence'),
       ('r1',5973,6617,'complete context board walk without physical'),
       ('r3',5629,5735,'return to the original embedding'),
       ('r3',607,688,'complete relationships sentence from opening'),
       ('r3',5993,6240,'canonical two-line close')]
COL={'blue':'#1652f0','teal':'#0e8f86','purple':'#4f2fc4','neutral':'#6e51ff','green':'#0f7a4a','orange':'#b96108','red':'#c41f28','ink':'#253140'}
MV,NYC,DALLAS=[180,330,495,425],[1025,290,1362,385],[645,500,945,595]
NP1,NP2=[208,695,548,790],[992,695,1332,790]
ROW=[[80,285,1520,459],[80,475,1520,649],[80,665,1520,839]]
SOFT,HOT=[165,154,719,720],[940,350,1420,700]
MYSTERY,PEPSI,COKE=[740,205,1270,320],[245,224,612,378],[235,503,610,625]
CIT_M,CIT_P,CIT_C=[1117,255,1163,305],[531,308,583,364],[531,566,578,616]
PLQ_START,PLQ_LAYERS,PLQ_UPD=[99,780,324,858],[510,791,841,839],[929,670,1117,743]

def plan_audio():
 cursor=0;rows=[]
 for key,a,b,label in AUDIO:
  rows.append(dict(source=key,source_start=a,source_end=b,start_frame=cursor,end_frame=cursor+b-a,label=label))
  cursor+=b-a
 return rows,cursor

def mapf(rows,key,t):
 f=fr(t)
 for r in rows:
  if r['source']==key and r['source_start']<=f<r['source_end']:
   return r['start_frame']+f-r['source_start']
 raise ValueError((key,t))

def audio_build(rows):
 ff=imageio_ffmpeg.get_ffmpeg_exe();a={}
 for n,p in [(1,R1),(2,R2),(3,R3)]:
  wav=OUT/f'roll{n}.wav'
  if not wav.exists():subprocess.run([ff,'-v','error','-y','-i',str(p),'-vn','-ac','1','-ar','48000',str(wav)],check=True)
  a[f'r{n}']=readwav(wav)
 def level(x):
  v=np.sqrt(np.mean(x[:len(x)//480*480].reshape(-1,480)**2,axis=1));return np.median(v[v>1000])
 gains={key:float(20*np.log10(level(a['r3'])/level(value))) for key,value in a.items()};parts=[];edge=[]
 for i,r in enumerate(rows):
  x=a[r['source']][r['source_start']*1600:r['source_end']*1600].copy()
  x*=10**(gains[r['source']]/20)
  # A 4ms ramp avoids sample discontinuity without masking any whole phoneme.
  if i:x[:192]*=np.linspace(0,1,192)
  if i<len(rows)-1:x[-192:]*=np.linspace(1,0,192)
  parts.append(x);edge.append(dict(label=r['label'],start_rms=float(np.sqrt(np.mean(x[:768]**2))),end_rms=float(np.sqrt(np.mean(x[-768:]**2)))))
 pcm=np.concatenate(parts);writewav(OUT/'edited.wav',pcm)
 return dict(donor_gain_db=gains,edge_rms=edge,sample_rate=48000,ramp_ms=4,added_pauses=0,peak=float(np.max(abs(pcm))))

def donor(name,p,a,b):
 """Decode a stable, clean lossless drawing excerpt; no copy of the live MP4."""
 dest=OUT/f'donor-{name}.mkv'
 if dest.exists():return dest
 assert sha(p)==EXPECTED[p]
 ff=imageio_ffmpeg.get_ffmpeg_exe();rd=Reader(p);mask=glyph_mask();stats={}
 proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-c:v','ffv1','-level','3',str(dest)],stdin=subprocess.PIPE)
 for f in range(fr(a),fr(b)):
  im=rd.at(f)
  if p!=LIVE:
   im,how=clean_frame(im,mask);assert how is not None;stats[how]=stats.get(how,0)+1
  proc.stdin.write(im.tobytes())
 proc.stdin.close();assert proc.wait()==0;rd.c.release()
 (OUT/f'donor-{name}.json').write_text(json.dumps(dict(source=str(p),sha256=sha(p),source_frames=[fr(a),fr(b)],frames=fr(b)-fr(a),corner_cleaning=stats),indent=2))
 return dest

@functools.lru_cache(maxsize=16)
def font(size,bold=False):
 return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf',size)

def paper():
 rng=np.random.default_rng(44);noise=rng.normal(0,.9,(720,1280,1));im=np.clip(np.array([248,245,233])[None,None,:]+noise,0,255).astype(np.uint8)
 p=Image.fromarray(im);d=ImageDraw.Draw(p)
 for y in range(18,720,23):
  for x in range(18,1280,23):d.ellipse((x,y,x+1,y+1),fill='#d9d5c8')
 return p
PAPER=paper()
def text(d,pos,tx,size=32,fill=None,bold=False,anchor=None):d.text(pos,tx,font=font(size,bold),fill=fill or COL['ink'],anchor=anchor)
def arrow(d,a,b,color,width=4):
 d.line([a,b],fill=color,width=width);ang=math.atan2(b[1]-a[1],b[0]-a[0]);l=15
 d.polygon([b,(b[0]-l*math.cos(ang-.5),b[1]-l*math.sin(ang-.5)),(b[0]-l*math.cos(ang+.5),b[1]-l*math.sin(ang+.5))],fill=color)
def tile(d,box,label,color,fill='#fffdf6',size=35):
 x,y,z,w=box;d.rounded_rectangle((x+5,y+6,z+5,w+6),radius=9,fill='#d9d5c8');d.rounded_rectangle(box,radius=9,fill=fill,outline=color,width=3);text(d,((x+z)/2,(y+w)/2),label,size,color,True,'mm')

def sketch(kind,t):
 """Code-native animated paper illustration using only the lesson's own values."""
 im=PAPER.copy();d=ImageDraw.Draw(im)
 if kind=='embedding':
  tile(d,(255,230,430,365),'IT',COL['blue'],'#dce9ff',60)
  arrow(d,(450,300),(525,300),COL['ink'])
  updated=t>=7.2
  vals=['.41','.06','…'] if updated else ['.12','−.34','…']
  text(d,(805,187),'Numbers updated for context' if updated else 'A row of numbers',36,bold=True,anchor='mm')
  for j,v in enumerate(vals):tile(d,(555+j*165,245,695+j*165,350),v,COL['purple'],size=40)
  text(d,(805,394),'Illustrative values from the lesson',22,'#677078',anchor='mm')
  if t>=5.8:
   d.line([(485,450),(490,465),(850,458),(845,443)],fill='#eee3a8',width=18)
   text(d,(660,455),'The layers change the numbers',28,bold=True,anchor='mm')
  if 12.5<=t<18.4:
   text(d,(640,565),'No exact match?',48,COL['purple'],True,'mm')
  if t>=18.4:
   text(d,(640,560),'Relationships matter too.',40,COL['teal'],True,'mm')
 else:
  # Same start/end illustrative values, presented as a schematic relationship.
  text(d,(640,100),'Changed numbers. Contextual meaning.',38,bold=True,anchor='mm')
  tile(d,(80,270,230,395),'IT',COL['blue'],'#eaf0f8',52)
  text(d,(155,438),'.12, −.34, …',27,COL['purple'],True,'mm')
  d.ellipse((665,165,1195,545),fill='#e8edda',outline=COL['teal'],width=3)
  text(d,(930,214),'ANIMALS',23,COL['teal'],True,'mm')
  text(d,(1060,411),'dog',29,COL['teal'],False,'mm');text(d,(979,477),'kitten',29,COL['teal'],False,'mm')
  tile(d,(930,270,1110,360),'CAT',COL['teal'],'#f7faf0',44)
  tile(d,(745,300,895,425),'IT',COL['blue'],'#dce9ff',52)
  text(d,(816,460),'.41, .06, …',25,COL['purple'],True,'mm')
  arrow(d,(255,345),(724,345),COL['purple'],5)
  text(d,(469,283),'updated for context',28,COL['purple'],False,'mm')
  text(d,(640,614),'A schematic of relationships',23,'#677078',False,'mm')
 return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)

def setup():
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 import shutil
 previous=ROOT/'video-audit/vector-space-build-2026-09-28-v7'
 for name in ['roll1.wav','roll3.wav','donor-semantic.mkv','donor-semantic.json','donor-gap.mkv','donor-gap.json','donor-cat.mkv','donor-cat.json']:
  if not (OUT/name).exists():shutil.copy2(previous/name,OUT/name)
 for p,h in EXPECTED.items():assert sha(p)==h,(p,'source changed')
 rows,total=plan_audio();audio=audio_build(rows);m=lambda key,t:mapf(rows,key,t)
 protected={str(p):sha(p) for p in [R1,R2,R3,LIVE,ROOT/'lessons/vector-space.md',*D.glob('*.jpg')]}
 b=Build(ROOT,R3,OUT,DEST);b.total=total
 # Visually meaningful boundaries, including clean donor cutaways.
 spans=[]
 def span(a,z,kind,label):
  assert z>a;spans.append(dict(start_frame=a,end_frame=z,visual=kind,label=label))
 span(0,m('r3',23.2333),'embedding','Illustrative token and contextual number update')
 span(m('r3',23.2333),next(r['start_frame'] for r in rows if r['source']=='r2'),'semantic','Notebook meaning neighborhoods')
 span(next(r['start_frame'] for r in rows if r['source']=='r2'),m('r3',46.9333),'cities','Three cities and coordinate donor')
 span(m('r3',46.9333),m('r3',61.9333),'closest','Two nearest-city answers')
 span(m('r3',61.9333),m('r3',65.4333),'gap','Position still tells us which city is near')
 span(m('r3',65.4333),m('r3',98.5),'taste','Seven drink dimensions and city-to-vector bridge')
 span(m('r3',98.5),next(r['start_frame'] for r in rows if r['label']=='mystery introduction without number readout'),'nbhd','Soft and hot drink neighborhoods')
 span(next(r['start_frame'] for r in rows if r['label']=='mystery introduction without number readout'),m('r3',146.6),'drink','Mystery vector and Citrus comparison')
 span(m('r3',146.6),m('r3',159.7333),'semantic','Learned embeddings at AI scale')
 ctx_start=next(r['start_frame'] for r in rows if r['label']=='complete context board walk without physical')
 span(m('r3',159.7333),ctx_start,'cat','Sentence and IT ambiguity')
 span(ctx_start,m('r3',187.7),'ctx','Numbers and contextual position')
 span(m('r3',187.7),m('r3',200),'relationships','Return to the opening question')
 span(m('r3',200),total,'close','Canonical two-line close')
 for a,z in zip(spans,spans[1:]):assert a['end_frame']==z['start_frame']
 def T(label,key,t,rects,color,**kw):return dict(label=label,at=m(key,t)/30,rects=rects,color=COL[color],**kw)
 tg={
 'cities':[T('Dallas','r3',38.04,[DALLAS],'red'),T('Mountain View','r1',48.92,[MV],'teal'),T('New York City','r1',53.04,[NYC],'blue')],
 'closest':[T('38 N 120 W nearest Mountain View','r3',52.04,[NP1,MV],'orange',colors=[COL['orange'],COL['teal']]),T('40 N 76 W nearest New York','r3',55.06,[NP2,NYC],'orange',colors=[COL['orange'],COL['blue']])],
 'taste':[T('A row of numbers is a vector','r3',72.82,[ROW[0]],'neutral'),T('Coke and Pepsi compared','r3',80.28,[ROW[0],ROW[1]],'neutral'),T('Coffee differs','r3',82.82,[ROW[2]],'neutral')],
 'nbhd':[T('Soft drinks neighborhood','r3',101.90,[SOFT],'blue',radius=280),T('Coffee neighborhood','r3',108.14,[HOT],'purple',radius=175)],
 'drink':[T('First six match Pepsi','r3',132.50,[MYSTERY,PEPSI],'orange',colors=[COL['orange'],COL['blue']]),T('Citrus 9 compared with Pepsi 10','r3',135.94,[CIT_M,CIT_P],'green',radius=8),T('Citrus gap from Coke','r3',141.66,[CIT_M,CIT_C],'green',radius=8)],
 'ctx':[T('Starting position numbers','r1',202.12,[PLQ_START],'blue',radius=8),T('The layers update the numbers','r1',209.00,[PLQ_LAYERS],'neutral',radius=8),T('Updated position numbers','r1',214.62,[PLQ_UPD],'neutral',radius=8)]}
 banners={'closest':m('r3',58.78)/30,'taste':m('r3',85.58)/30,'drink':m('r3',144.64)/30,'ctx':m('r1',218.62)/30}
 rs={}
 for s in spans:
  k=s['visual']
  if k not in ASSETS:continue
  b.tall_margin=k not in ('nbhd','drink')
  b.board(k,ASSETS[k],s['start_frame'],s['end_frame'],'compact',tg[k],banner_at=banners.get(k),push=k=='nbhd')
  spec=json.loads((OUT/f'leg-{k}.json').read_text());spec['upscale']=2;(OUT/f'leg-{k}.json').write_text(json.dumps(spec,indent=2));rs[k]=Renderer(spec)
  for f in sorted({0,s['end_frame']-s['start_frame']-1}|{r['start']+3 for r in spec['rings']}):
   cv2.imwrite(str(OUT/'preview'/f'{k}-{f:04d}.jpg'),rs[k].at(f)[0])
 b.make_close('vectorspace')
 for kind,t in [('embedding',0),('embedding',9),('embedding',16),('embedding',21),('relationships',0)]:cv2.imwrite(str(OUT/'preview'/f'{kind}-{t}.jpg'),sketch(kind,t))
 donors={'semantic':donor('semantic',R3,25.8,32.1),'gap':donor('gap',LIVE,66.0,73.2),'cat':donor('cat',R1,191.0,198.7)}
 boards={k:{**v,'planned_output_frames':[v['src_in'],v['src_out']]} for k,v in b.boards.items()}
 bounds={s['start_frame']:s['label'] for s in spans[1:]}
 for r in rows[1:]:bounds.setdefault(r['start_frame'],'Audio join: '+r['label'])
 manifest=dict(output=str(DEST),fps=30,total_frames=total,duration=total/30,audio_timeline=rows,timeline=spans,boards=boards,
  boundaries=[dict(frame=f,label=l) for f,l in sorted(bounds.items())],audio=audio,protected_hashes=protected,
  close=dict(start_frame=m('r3',200),prehold=48,push=150,endpoint=1.2,settle=total-m('r3',200)-198),
  donor_files={k:str(v) for k,v in donors.items()},scope='Narrow v7 revision: map bridge, remove full drink-vector readouts, live-style neighborhood and mystery framing; live unchanged',
  approval='User requested an available map-transition sentence, removal of full drink number readouts, and the live-style neighborhood presentation. Mystery introduction and citrus comparison remain. Prior approval applies elsewhere.',
  new_visuals='Code-native paper illustration replaces invented opening vectors, using only .12, -.34 and .41, .06 from canonical lesson; returning schematic connects IT and CAT. No generated photos, invented scores or layer/dimension counts.',
  listening='Not directly auditioned; speech edits require listening review. ASR and waveform checks do not certify cadence.')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2))
 print('Prepared',total,'frames',total/30,'seconds',flush=True)
 return b,rs,spans,donors,manifest

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Version the next candidate; do not overwrite'
 b,rs,spans,donors,manifest=setup()
 if args.prepare_only:return
 ff=imageio_ffmpeg.get_ffmpeg_exe();proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for s in spans:
  k=s['visual'];n=s['end_frame']-s['start_frame'];rd=None
  if k in donors:
   rd=Reader(donors[k]);cap=cv2.VideoCapture(str(donors[k]));dn=int(cap.get(cv2.CAP_PROP_FRAME_COUNT));cap.release()
  for f in range(n):
   if k in rs:im=rs[k].at(f)[0]
   elif k in donors:im=rd.at(round(f/(n-1)*(dn-1)))
   elif k=='close':
    q=np.clip((f-48)/149,0,1);z=1+.2*q*q*(3-2*q);ci=b.close_img;h,w=ci.shape[:2];cw=w/z;ch=cw*9/16
    im=cv2.warpAffine(ci,np.float32([[cw/1280,0,(w-cw)/2],[0,ch/720,(h-ch)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
   else:im=sketch(k,f/30)
   proc.stdin.write(im.tobytes())
  if rd:rd.c.release()
  print('Rendered',k,s['end_frame'],'/',b.total,flush=True)
 proc.stdin.close();assert proc.wait()==0
 assert all(sha(Path(p))==h for p,h in manifest['protected_hashes'].items())
 manifest['render_sha256']=sha(DEST);manifest['protected_files_unchanged']=True
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2));print(DEST,flush=True)
if __name__=='__main__':main()
