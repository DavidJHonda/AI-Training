"""Approved raw-8/raw-9 review candidate. Never installs or overwrites candidates."""
from pathlib import Path
import sys,json,subprocess,functools,math
import numpy as np,cv2
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import Build,Reader,fr,sha,readwav,rms
from gemini_mark import clean_frame,glyph_mask
from build_vector_space_v11 import opening
OUT=Path(__file__).resolve().parent;DEST=ROOT/'Prompts/vector-space-v17.mp4'
S8=ROOT/'Prompts/vector-space-8.mp4';S9=ROOT/'Prompts/vector-space-9.mp4'
D=ROOT/'course-assets/vector-space'; FPS=30
b=Build(ROOT,S8,OUT,DEST,protected=[ROOT/'Prompts/vector-space-v16.mp4',S9,D/'vector-space.mp4',D/'vector-space-meaning-map.jpg',D/'vector-space-close.jpg',D/'vector-space-us-map.svg'])
b.load_audio([(60.65,61.6),(72.2,72.9),(185.85,186.3),(210.0,210.4)])
if not (OUT/'donor.wav').exists():subprocess.run([b.ff,'-v','error','-i',str(S9),'-vn','-ac','1','-ar','48000',str(OUT/'donor.wav')],check=True)
a9=readwav(OUT/'donor.wav')
def level(a,s,e):
 x=a[round(s*48000):round(e*48000)];v=np.sqrt(np.mean(x[:len(x)//960*960].reshape(-1,960)**2,axis=1));return float(np.median(v[v>1000]))
baselevel=level(b.audio,95,142.5);donorlevel=level(a9,110.7,132);gain=20*math.log10(baselevel/donorlevel)
# Exact edges lie in measured silence. All cuts preserve complete narrated beats.
b.graft(S9,0,fr(10.1666667),'Complete embedding opening','opening',picture_from=0,visual='opening',gain_db=gain)
def keep(s,e,label):b.keep(fr(s),fr(e),label)
keep(6.9666667,61.1666667,'Opening question through first city question')
b.pause(15,'City A comparison extension')
keep(61.1666667,72.6,'First city answer and second question')
b.pause(22,'City B comparison extension')
keep(72.6,80.9666667,'Second city answer and exact conclusion')
keep(89.2,105.9666667,'Seven dimensions and Coke introduction; coordinate readout removed')
b.graft(S9,fr(120.3),fr(132.3333333),'Pepsi with correct Citrus 10','pepsi',picture_from=fr(115.2),visual='drinks',gain_db=gain)
keep(125.6,149.2,'Pepsi relationship and hot coffee')
keep(157.3,163.3,'Mystery A introduction')
keep(173.1666667,186.0666667,'Mystery A comparison; coordinate readout removed')
b.pause(34,'Drink A comparison extension')
keep(186.0666667,192.9333333,'Pepsi answer and Mystery B introduction')
keep(202.3,210.2333333,'Mystery B comparison; coordinate readout removed')
b.pause(34,'Drink B comparison extension')
keep(210.2333333,222.3333333,'Coffee answer and vector conclusion')
keep(230.6666667,251.0666667,'Distance and learned-dimensional meaning callback')
keep(261.0666667,301.9,'Context and distinct IT/CAT relationship')
b.mark_close_start();keep(310.9666667,316.5,'Exact two-line close');b.pause(120,'Settled close hold')
b.finish_audio()

def mf(t):
 f=fr(t)
 for r in b.rows:
  if r['kind']=='source' and not r.get('graft_audio') and r['source_start']<=f<r['source_end']:return r['start_frame']+f-r['source_start']
 raise ValueError(t)
pepsi=next(r for r in b.rows if r.get('visual')=='drinks');pepsi_on=pepsi['start_frame']+fr(120.72)-pepsi['audio_start']
city=[(mf(t),i) for i,t in enumerate([28.2,32.18,38.8,44.16,52.44,61.81,65.1,73.133333])]
drink=[(mf(89.2),0),(mf(104.58),1),(pepsi_on,2)]+[(mf(t),i) for i,t in enumerate([131.08,161.2,186.383333,191.28,210.533333],3)]
relation_start=mf(19.08);city_start=city[0][0];scale_start=mf(235.5);context_start=mf(261.0666667)
context_end=b.close_start
# The sentence is a short introductory drawing; canonical illustration follows it.
board_start=mf(272.8)
ctxpath,cw,ch,ox,oy=b.compose(D/'vector-space-meaning-map.jpg','context');ctx=cv2.resize(cv2.imread(str(ctxpath)),(1280,720),interpolation=cv2.INTER_AREA)
close=cv2.imread(str(OUT/'close.png'))
states={k:[cv2.imread(str(OUT/'frames'/f'{k}-{s}.png')) for s in range(8)] for k in ['cities','drinks']}
fontpath=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
@functools.lru_cache(maxsize=30)
def font(n):return ImageFont.truetype(str(fontpath),n)
def label(im,xy,text,size=30,fill='#255575',anchor='mm'):
 p=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));ImageDraw.Draw(p).text(xy,text,font=font(size),fill=fill,anchor=anchor);return cv2.cvtColor(np.array(p),cv2.COLOR_RGB2BGR)
def patch_paper(im,rect):
 x,y,x2,y2=rect;out=im.copy();# clean blank paper from the same source frame
 seed=im[160:210,40:260];out[y:y2,x:x2]=cv2.resize(seed,(x2-x,y2-y),interpolation=cv2.INTER_LINEAR);return out

def sentence():
 im=np.full((720,1280,3),255,np.uint8)
 # Short text drawing from the exact sentence, introduced during its narration.
 for y,segments in [(290,[('The ',False),('CAT',True),(' sat on the mat',False)]),(365,[('during the May rainstorm',False)]),(440,[('because ',False),('IT',True),(' was tired.',False)])]:
  widths=[font(44).getlength(s) for s,_ in segments];x=(1280-sum(widths))/2
  for (s,em),w in zip(segments,widths):im=label(im,(x,y),s,44,'#4f2fc4' if em else '#171329','lm');x+=w
 return im
sentence_im=sentence()
# Existing approved opening drawing, retimed to these particular spoken onsets.
open_states=[opening(t) for t in [0,6,8,13,19]]
open_cues=[(0,0),(fr(4.9),1),(fr(6),2),(mf(7.28),3),(mf(16.22),4)]
ctx_targets=[(mf(282.24),[(90,675,335,865)],'#1652f0'),(mf(289.18),[(500,780,854,851)],'#6e51ff'),(mf(290.6),[(925,678,1128,754)],'#1652f0'),(mf(294.02),[(962,564,1135,674)],'#1652f0'),(mf(297.98),[(40,1023,1560,1111)],'#6e51ff')]
def rounded(im,rect,color):
 x,y,x2,y2=[round((v+(ox if i%2==0 else oy))*1280/cw) for i,v in enumerate(rect)]
 rgb=tuple(int(color[i:i+2],16) for i in (1,3,5));c=rgb[::-1];r=8
 cv2.line(im,(x+r,y),(x2-r,y),c,4,cv2.LINE_AA);cv2.line(im,(x+r,y2),(x2-r,y2),c,4,cv2.LINE_AA);cv2.line(im,(x,y+r),(x,y2-r),c,4,cv2.LINE_AA);cv2.line(im,(x2,y+r),(x2,y2-r),c,4,cv2.LINE_AA)
 for p,a,z in [((x+r,y+r),180,270),((x2-r,y+r),270,360),((x2-r,y2-r),0,90),((x+r,y2-r),90,180)]:cv2.ellipse(im,p,(r,r),0,a,z,c,4,cv2.LINE_AA)
 return im
mask=glyph_mask();rdrel=Reader(S8);rdscale=Reader(S8);clean_counts={};last_source=-1;scale_last=None
# Cache only a small sequential source segment, not the full video.
def cleaned(rd,n):
 im,method=clean_frame(rd.at(n),mask);clean_counts[method or 'declined']=clean_counts.get(method or 'declined',0)+1;return im
@functools.lru_cache(maxsize=4)
def relframe(n):
 im=cleaned(rdrel,n);im=patch_paper(im,(285,62,1020,148));im=label(im,(650,105),'Nearby relationships',32)
 im=patch_paper(im,(946,316,1235,370));return label(im,(1090,339),'Similar meanings can be nearby',16)
@functools.lru_cache(maxsize=4)
def scaleframe(n):
 t=n/30
 im=cleaned(rdscale,n)
 if 237.5<=t<240.6:
  im=cv2.imread(str(OUT/'inspection/raw8-239.jpg'));im,_=clean_frame(im,mask)
  # Remove the invented fixed count and example values; retain the source panel.
  im[304:435,316:967]=(250,252,251)
  im=label(im,(640,345),'Thousands of dimensions',29)
  im=label(im,(640,404),'Values learned during training',23)
 if 240.6<=t<248:
  im=patch_paper(im,(100,50,1180,174));im=label(im,(645,105),'Positions and relationships',30)
 return im

def frame(n):
 if n<relation_start:
  return open_states[next(i for f,i in reversed(open_cues) if n>=f)].copy()
 if n<city_start:
  # Preserve the source map animation, retiming the complete clean map portion.
  source=fr(22.5)+round((n-relation_start)/(city_start-relation_start-1)*(fr(28.1666667)-fr(22.5)))
  return relframe(source).copy()
 if n<drink[0][0]:kind,cues='cities',city
 elif n<scale_start:kind,cues='drinks',drink
 else:kind=None
 if kind:
  f,step=next(c for c in reversed(cues) if c[0]<=n);im=states[kind][step]
  if step and n-f<15:
   q=(n-f+1)/15;q=1-(1-q)**3;im=cv2.addWeighted(states[kind][step-1],1-q,im,q,0)
  return im.copy()
 if n<context_start:
  r=next(r for r in b.rows if r['start_frame']<=n<r['end_frame']);sf=r['source_start']+n-r['start_frame'];return scaleframe(sf).copy()
 if n<board_start:return sentence_im.copy()
 if n<context_end:
  im=ctx.copy();target=next((r for r in reversed(ctx_targets) if r[0]<=n),None)
  if target:
   for rect in target[1]:rounded(im,rect,target[2])
  return im
 f=n-b.close_start;q=np.clip((f-48)/149,0,1);z=1+.2*q*q*(3-2*q);h,w=close.shape[:2];ww=w/z;hh=ww*9/16
 return cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)

boundaries={r['start_frame']:r['label'] for r in b.rows if r['start_frame']>0}
for kind,cues in [('cities',city),('drinks',drink)]:
 for f,s in cues:boundaries[f]=f'{kind}-{s}'
for f,label_ in [(mf(237.5),'Corrected scale panel'),(mf(240.6),'Scale relationships'),(mf(248),'Dimensional drawing'),(relation_start,'Nearby drawing'),(scale_start,'Scale drawing'),(context_start,'Exact sentence'),(board_start,'Canonical context'),(b.close_start,'Canonical close')]+[(x[0],'Context focus') for x in ctx_targets]:boundaries[f]=label_
manifest=dict(output=str(DEST),fps=30,total_frames=b.total,duration=b.total/30,timeline=b.rows,grafts=b.grafts,audio=dict(room_tone=b.tone_meta,gain_db=gain,base_active_rms=baselevel,donor_active_rms=donorlevel,peak=float(np.max(abs(np.concatenate(b.parts))))),city_cues=city,drink_cues=drink,visual_sections=dict(opening=[0,relation_start],relationships=[relation_start,city_start],cities=[city_start,drink[0][0]],drinks=[drink[0][0],scale_start],scale=[scale_start,context_start],sentence=[context_start,board_start],context=[board_start,context_end],close=[b.close_start,b.total]),context_targets=ctx_targets,context_canvas=dict(width=cw,height=ch,offset=[ox,oy]),close=dict(prehold=48,push=150,zoom=1.2,tail=120),boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],protected_hashes=b.hashes,lesson_snapshot_sha256=sha(ROOT/'index.html'),capture_sha256=sha(OUT/'capture.html'),scope='Narrow v16 edit: remove only Coke and Mystery A/B spoken coordinate readouts; preserve introductions, vectors, comparison narration, pauses, and all other treatment. Candidate only.',direct_listening=False,real_time_motion_review=False)
manifest.update(revision_of=str(ROOT/'Prompts/vector-space-v16.mp4'),removed_raw8_seconds=[[105.9666667,114.9666667],[163.3,173.1666667],[192.9333333,202.3]],approval='User: Remove Coke, too. Continuing approved removal of both Mystery Drink coordinate readouts.')
(OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2))
if '--prepare-only' in sys.argv:
 # Increasing source order for sequential readers.
 for n in sorted(set([0,fr(8),relation_start+30,city_start+30,*[f+20 for f,s in city],*[f+20 for f,s in drink],scale_start+30,scale_start+100,scale_start+220,scale_start+350,context_start+30,board_start+30,*[f+5 for f,_,_ in ctx_targets],b.total-1])):
  cv2.imwrite(str(OUT/'preview'/f'f{n:05}.jpg'),frame(n))
 print('Prepared',b.total,'frames',b.total/30,'seconds; donor gain',gain);sys.exit()
assert not DEST.exists(),'Never overwrite review candidates'
p=subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
for n in range(b.total):
 p.stdin.write(frame(n).tobytes())
 if n%900==0:print('Rendered',n,'/',b.total,flush=True)
p.stdin.close();assert p.wait()==0
assert all(sha(Path(p))==h for p,h in b.hashes.items())
manifest.update(render_sha256=sha(DEST),protected_files_unchanged=True,corner_cleaning=clean_counts)
(OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2));print('Finished',DEST,flush=True)
