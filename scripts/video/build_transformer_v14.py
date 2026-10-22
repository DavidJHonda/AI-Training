#!/usr/bin/env python3
"""Approved October context update. Versioned review only, never installs.

Canonical boards + four approved contextual audio grafts; original motion retained.
Uses stable v12 visuals to avoid an extra generation through v13's paper repair.
The original pre-edit raw source and v11 snapshot no longer exist.
"""
from pathlib import Path
import argparse,json,subprocess,hashlib
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Build,Reader,sha
from build_embeddings_v7 import Renderer
from ken_burns_path import fit_window
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/transformer-build-v14-2026-10-22'
REVIEW=ROOT/'video-audit/transformer-context-review-2026-10-22'
BASE=ROOT/'Prompts/transformer-v13.mp4'; VIS=ROOT/'Prompts/transformer-v12.mp4'
DEST=ROOT/'Prompts/transformer-v14.mp4'
ASSET=ROOT/'scripts/video/assets/transformer-v14/brain-paper-imagegen.png'
PLAN=json.loads((REVIEW/'proposed-grafts.json').read_text()); FPS=30; SPF=1600
BLUE='#1652f0';GREEN='#0f7a4a';PURPLE='#6e51ff'
ff=imageio_ffmpeg.get_ffmpeg_exe()
def decode(p):
 return np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(p),'-vn','-ar','48000','-ac','1','-f','f32le','-']),np.float32).copy()
def of(f):
 shift=0
 for g in PLAN['grafts']:
  a,b=g['base_frames']
  if f<a:break
  if f<b:raise ValueError(('removed',f))
  shift+=g['delta_frames']
 return f+shift

def prepare_audio():
 a=decode(BASE);parts=[];mapping=[];cursor=0;rows=[];out=0
 for g in PLAN['grafts']:
  s,e=g['base_frames'];parts.append(a[cursor*SPF:s*SPF]);mapping.extend(range(cursor,s))
  rows.append(dict(kind='retained',source_start=cursor,source_end=s,start_frame=out,end_frame=out+s-cursor));out+=s-cursor
  p=decode(REVIEW/(g['name']+'-preview.wav'));x=p[round(g['preview_graft_start']*48000):round(g['preview_graft_end']*48000)]
  assert hashlib.sha256(x.tobytes()).hexdigest()==g['insert_sha256']
  parts.append(x);n=len(x)//SPF;mapping.extend([-1]*n)
  rows.append(dict(kind='donor',label=g['name'],start_frame=out,end_frame=out+n,donor_frames=g['donor_frames']));out+=n;cursor=e
 parts.append(a[cursor*SPF:7046*SPF]);mapping.extend(range(cursor,7046))
 rows.append(dict(kind='retained',source_start=cursor,source_end=7046,start_frame=out,end_frame=len(mapping)))
 audio=np.concatenate(parts);assert len(audio)==7163*SPF
 subprocess.run([ff,'-y','-v','error','-f','f32le','-ar','48000','-ac','1','-i','pipe:0','-c:a','pcm_f32le',str(OUT/'edited.wav')],input=audio.tobytes(),check=True)
 return mapping,rows

def boards():
 b=Build(ROOT,VIS,OUT,DEST);specs={};meta={};renderers={}
 def board(key,file,start,end,points,events,density):
  asset=ROOT/'course-assets/transformer'/file;canvas,cw,ch,ox,oy=b.compose(asset,key)
  full=[cw/2,ch/2,cw]
  def cam(rect):
   if rect is None:return full
   x,y,z,w=rect;return list(fit_window(dict(fit=[x+ox,y+oy,z-x,w-y],margin=10),16/9,1280,3))
  pts=[(round(t*30)-start,cam(rect),label) for t,rect,label in points]
  assert pts[0][0]==0 and pts[-1][0]==end-start
  spec=dict(image=str(canvas),fps=30,out_w=1280,out_h=720,upscale=3,beats=[],rings=[])
  for (a,c,_),(z,target,label) in zip(pts,pts[1:]):spec['beats'].append(dict(label=label,frames=z-a,**{'from':c,'to':target}))
  for a,z,rect,color,label in events:
   x,y,x2,y2=rect
   spec['rings'].append(dict(start=round(a*30)-start,end=round(z*30)-start,rect=[x+ox,y+oy,x2-x,y2-y],color=color,pad=0,radius=12,label=label))
  (OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n');specs[key]=spec;renderers[key]=Renderer(spec)
  meta[key]=dict(asset=str(asset.relative_to(ROOT)),sha256=sha(asset),start_frame=start,end_frame=end,density=density,canvas_offset=[ox,oy])
 L=[40,127,783,1171];R=[816,127,1560,1171];full=None
 # Continuous board clock across the brief preserved pronoun illustration.
 board('context','transformer-context-problems.jpg',707,1497,
 [(707/30,full,'start'),(25.567,full,'full view'),(26.767,L,'left card'),(36.4,L,'light examples'),(37.2,R,'pronouns'),(47.1,R,'pronoun examples'),(47.8,full,'return to full'),(49.9,full,'takeaway')],
 [(26.86,29.36,L,BLUE,'Different Meanings'),(29.36,34.033,[74,786,750,900],BLUE,'brightness sentence'),(34.033,36.9,[74,913,750,1027],BLUE,'empty suitcase'),(40.733,41.833,[850,786,1526,900],GREEN,'cat sentence'),(41.833,42.75,[866,800,1510,835],GREEN,'cat answer'),(43.113,45.993,[850,913,1526,1027],GREEN,'milk sentence'),(45.993,47.1,[866,926,1510,961],GREEN,'milk answer'),(47.8,49.9,[40,1213,1560,1302],PURPLE,'context takeaway')],'dense')
 # Token positions measured from the canonical renderer, interior bounds avoid
 # doubling baked-in token outlines. Extremely short words receive >=1 frame.
 xs1=[132.5+i*170 for i in range(8)];xs2=[202,372,542,743,913,1083,1253]
 rects=[[x+18,205,x+127,255] for x in xs1]+[[x+18,425,x+(158 if i==2 else 127),475] for i,x in enumerate(xs2)]
 onsets=[74.25,74.38,74.76,75.08,75.38,75.58,75.68,75.86,76.16,76.32,76.46,79.34,79.46,79.80,80.04]
 # THE and TIRED share an ASR onset. THE starts at the preceding quiet boundary,
 # 130 ms earlier; no change to audio.
 times=[57.9+t-72.9 for t in onsets];ev=[]
 for i,t in enumerate(times):
  stop=times[i+1] if i+1<len(times) else 65.6
  if i==10:stop=62.8
  ev.append((t,stop,rects[i],BLUE,'spoken '+str(i)))
 ev += [(66.333,67.533,rects[11],BLUE,'IT reference'),(67.533,70.0,rects[2],BLUE,'earlier CAT'),(70.0,73.8,[600,547,1000,588],PURPLE,'IT refers to CAT'),(73.8,2368/30,[40,606,1560,695],PURPLE,'earlier AI takeaway')]
 board('earlier','transformer-before-transformers.jpg',1735,2368,[(1735/30,None,'start'),(2368/30,None,'full view')],ev,'compact')
 board('reads','transformer-how-transformer-reads.jpg',2672,3247,[(2672/30,None,'start'),(3247/30,None,'full view')],
 [(92.96,101.62,[40,127,1560,587],BLUE,'complete message'),(102.4,104.54,[528,472,590,514],BLUE,'IT'),(104.54,104.96,[641,268,729,310],BLUE,'CAT draws context'),(104.96,3247/30,[40,627,1560,716],PURPLE,'IT draws on CAT')],'compact')
 L=[40,127,783,1233];R=[816,127,1560,1233]
 board('resolves','transformer-resolves-meaning.jpg',4533,5383,
 [(151.1,None,'start'),(153.1,None,'full view'),(153.9,L,'left card'),(164.55,L,'light examples'),(165.6,R,'pronoun card'),(174.9,R,'pronoun examples'),(175.7,None,'pullback'),(5383/30,None,'takeaway')],
 [(151.65,153.6,[74,691,750,805],BLUE,'brightness sentence'),(153.6,156.867,[90,1010,734,1098],BLUE,'TURN ON'),(156.867,159.733,[74,818,750,932],BLUE,'empty suitcase sentence'),(159.733,164.733,[90,1106,734,1196],BLUE,'EMPTY'),(166.247,169.667,[850,691,1526,805],GREEN,'cat sentence'),(169.667,170.7,[866,1010,1510,1098],GREEN,'cat answer'),(170.947,173.827,[850,818,1526,932],GREEN,'milk sentence'),(173.827,175.1,[866,1106,1510,1196],GREEN,'milk answer'),(175.7,5383/30,[40,1275,1560,1363],PURPLE,'meaning takeaway')],'dense')
 return specs,meta,renderers

def paper():
 # Reuse v13's validated tracking algorithm with the new paper interior. All
 # pixels outside the tracked patch remain exact decoded v12 pixels.
 import build_transformer_v13 as p
 p.OUT=OUT/'paper';p.OUT.mkdir(exist_ok=True);p.ASSET=ASSET;p.DEST=DEST
 frames,manifest=p.prepare();return frames,manifest

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a candidate'
 assert sha(BASE)==PLAN['base_sha256'];assert sha(VIS)=='0a972235e9fcaf619d8db34715243a7812a87569091e87092f866666586376b5'
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 mapping,rows=prepare_audio();specs,meta,renderers=boards();repaired,pm=paper()
 protected={str(p):sha(p) for p in [BASE,VIS,ROOT/'Prompts/transformer-2.mp4',ROOT/'course-assets/transformer/transformer.mp4',ROOT/'lessons/transformer.md',*sorted((ROOT/'course-assets/transformer').glob('*.jpg'))]}
 mapped=[None]*len(mapping)
 for key,item in meta.items():
  for out in range(item['start_frame'],item['end_frame']):mapped[out]=(key,out-item['start_frame'])
 for n in range(1107,1222):mapped[n]=None # 3.833 s supporting scene, moved under pronoun intro
 assert all(f>=0 or mapped[n] is not None or 1107<=n<1222 for n,f in enumerate(mapping))
 preview=[]
 for key,r in renderers.items():
  wanted={0,len(r.cameras)-1};at=0
  for beat in specs[key]['beats']:
   z=at+beat['frames'];wanted|={at,(at+z)//2,z-1};at=z
  for a,z,*_ in r.rings:wanted|={a,(a+z)//2,z-1}
  for local in sorted(wanted):
   n=meta[key]['start_frame']+local
   if not mapped[n]:continue
   im,_,geo=r.at(local);path=OUT/'preview'/f'{n:05d}-{key}.jpg';cv2.imwrite(str(path),im);preview.append(dict(frame=n,path=str(path),key=key,rings=geo))
 boundaries=sorted(set([g['output_frames'][i] for g in PLAN['grafts'] for i in [0,1]]+[v[k] for v in meta.values() for k in ['start_frame','end_frame']]+[1107,1222,1497,1735]+[of(f) for f in [3396,4044,4254,5456,6039,6746,6926]]))
 manifest=dict(candidate=str(DEST),fps=30,frame_count=7163,duration=7163/30,visual_source=str(VIS),audio_source=str(BASE),source_limitation='Pristine raw and v11 snapshot unavailable. Retained v12 visuals avoid the extra v13 paper-repair encode; v13 audio supplies unchanged spans. All new visuals encoded directly from current assets.',approval='User: Build it please, approving four donor passages and board/visual plan dated 2026-10-22.',timeline=rows,grafts=PLAN['grafts'],boards=meta,specs=specs,prepared_states=preview,boundaries=boundaries,paper_tracking=pm,protected=protected,pauses='No added pauses or speech stretching',supporting_insert=dict(source_frames=[1171,1286],output_frames=[1107,1222]),direct_listening=False,status='prepared')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Prepared all four boards, tracked paper, and 7163-frame audio timeline.',flush=True)
 if args.prepare_only:return
 proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 rd=Reader(VIS);ins=Reader(VIS)
 for n,f in enumerate(mapping):
  if 1107<=n<1222:im=ins.at(1171+n-1107)
  elif mapped[n]:key,local=mapped[n];im=renderers[key].at(local)[0]
  elif 1497<=n<1735:im=repaired[n-1497]
  else:assert f>=0;im=rd.at(f)
  proc.stdin.write(im.tobytes())
  if n%1000==999:print(f'Rendered {n+1}/7163',flush=True)
 proc.stdin.close();assert proc.wait()==0;rd.c.release();ins.c.release()
 assert all(sha(Path(p))==h for p,h in protected.items())
 manifest.update(status='built for review',candidate_sha256=sha(DEST));(OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
