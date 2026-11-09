#!/usr/bin/env python3
"""November reroll hybrid; versioned review candidate, never installs or publishes."""
from pathlib import Path
import argparse, json, subprocess
import cv2, numpy as np, imageio_ffmpeg
from editspec_build import Build, Reader, sha
from build_embeddings_v7 import Renderer
from ken_burns_path import fit_window
from gemini_mark import clean_frame, glyph_mask
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/transformer-build-v16-2026-11-09'
DEST=ROOT/'Prompts/transformer-v16.mp4'
FPS=30; SR=48000; SPF=1600
BLUE='#1652f0';GREEN='#0f7a4a';TEAL='#0e8f86';PURPLE='#6e51ff'
SRC={i:ROOT/f'Prompts/transformer-{i}.mp4' for i in (2,5,6)}
FF=imageio_ffmpeg.get_ffmpeg_exe()
def fr(t):return round(t*30)
def decode(p):return np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-ar','48000','-ac','1','-f','f32le','-']),np.float32).copy()
def active_level(a):
 x=a[:len(a)//960*960].reshape(-1,960);p=np.mean(x*x,axis=1);active=p[p>10**(-35/10)]
 return float(10*np.log10(active.mean()))
def timeline():
 # All boundaries measured in quiet gaps; no speech stretching or inserted pauses.
 spans=[('intro',6,0,21+26/30),('opening',5,31.9,92+23/30),
 ('earlier',6,47+20/30,58.2),('qualifier',2,93.3,98.1),
 ('history_reads',6,62.3,91.6),('numbers_bridge',5,147+5/30,156.7),
 ('mechanisms_return',6,103+4/30,131.6),('repeat_light',6,21+26/30,28.2),
 ('light_clues',6,131.6,144+8/30),('repeat_pronouns',6,28.8,38.6),
 ('pronoun_clues',6,144+8/30,155.1),('sarcasm',6,155.1,170+14/30),
 ('order_close',6,176+22/30,223.3)]
 rows=[];cursor=0
 for tag,k,a,z in spans:
  a,z=fr(a),fr(z);rows.append(dict(tag=tag,source=k,source_start=a,source_end=z,start_frame=cursor,end_frame=cursor+z-a));cursor+=z-a
 return rows,cursor
ROWS,TOTAL=timeline(); BYTAG={r['tag']:r for r in ROWS}
def at(tag,t):r=BYTAG[tag];return r['start_frame']+fr(t)-r['source_start']
def prepare_audio():
 audio={k:decode(p) for k,p in SRC.items()};levels={k:active_level(a) for k,a in audio.items()}
 gains={k:levels[6]-v for k,v in levels.items()};parts=[];joins=[]
 for i,r in enumerate(ROWS):
  x=audio[r['source']][r['source_start']*SPF:r['source_end']*SPF].copy()*10**(gains[r['source']]/20)
  # Five-ms ramps in measured silence suppress sample discontinuity without changing timing.
  ramp=np.linspace(0,1,240)
  if i:x[:240]*=ramp
  if i<len(ROWS)-1:x[-240:]*=ramp[::-1]
  parts.append(x)
  joins.append(dict(tag=r['tag'],gain_db=gains[r['source']],head_rms_db=float(20*np.log10(np.sqrt(np.mean(x[:960]**2))+1e-12)),tail_rms_db=float(20*np.log10(np.sqrt(np.mean(x[-960:]**2))+1e-12))))
 a=np.concatenate(parts);assert len(a)==TOTAL*SPF;assert np.max(abs(a))<1
 subprocess.run([FF,'-y','-v','error','-f','f32le','-ar','48000','-ac','1','-i','pipe:0','-c:a','pcm_f32le',str(OUT/'edited.wav')],input=a.tobytes(),check=True)
 return dict(active_rms_db=levels,donor_gain_db=gains,seams=joins,peak=float(np.max(abs(a))),added_pauses=0,fade_samples=240)

def prepare_boards():
 b=Build(ROOT,SRC[6],OUT,DEST);specs={};meta={};rs={}
 def board(key,file,start,end,points,events,density):
  asset=ROOT/'course-assets/transformer'/file;canvas,cw,ch,ox,oy=b.compose(asset,key);full=[cw/2,ch/2,cw]
  def cam(rect):
   if rect is None:return full
   x,y,x2,y2=rect;return list(fit_window(dict(fit=[x+ox,y+oy,x2-x,y2-y],margin=20),16/9,1280,3))
  pts=[(n-start,cam(rect),label) for n,rect,label in points];assert pts[0][0]==0 and pts[-1][0]==end-start
  spec=dict(image=str(canvas),fps=30,out_w=1280,out_h=720,upscale=2,beats=[],rings=[])
  for (a,c,_),(z,target,label) in zip(pts,pts[1:]):
   if z>a:spec['beats'].append(dict(label=label,frames=z-a,**{'from':c,'to':target}))
  for a,z,rect,color,label in events:
   assert start<=a<z<=end,(key,label,a,z,start,end)
   x,y,x2,y2=rect;spec['rings'].append(dict(start=a-start,end=z-start,rect=[x+ox,y+oy,x2-x,y2-y],color=color,pad=0,radius=12,label=label))
  specs[key]=spec;rs[key]=Renderer(spec);meta[key]=dict(asset=str(asset.relative_to(ROOT)),sha256=sha(asset),start_frame=start,end_frame=end,density=density,canvas_offset=[ox,oy])
  (OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n')
 # Tall cards remain complete. This improves readability modestly; no internal crops.
 s=fr(20.767);e=at('opening',79+14/30);L=[40,127,783,1274];R=[816,127,1559,1274];t=lambda q:at('opening',q)
 board('context','transformer-context-problems.jpg',s,e,
 [(s,None,'full'),(s+60,None,'establish'),(s+84,L,'left complete card'),(t(52),L,'left hold'),(t(52.84),R,'right complete card'),(t(75.64),R,'right hold'),(t(76.44),None,'takeaway'),(e,None,'end')],
 [(t(32.22),t(39.2),L,BLUE,'Different Meanings'),(t(39.2),t(43.52),[74,786,750,919],BLUE,'brightness sentence and meaning'),(t(43.52),t(48.12),[74,933,750,1066],BLUE,'weight sentence and meaning'),(t(48.12),t(52.3),[74,1137,750,1245],BLUE,'meaning question'),(t(52.84),t(57.06),R,GREEN,'Pronouns'),(t(57.06),t(63.38),[850,786,1526,919],GREEN,'cat sentence and meaning'),(t(63.38),t(68.52),[850,933,1526,1066],GREEN,'milk sentence and meaning'),(t(68.52),t(75.64),[850,1137,1526,1245],GREEN,'referent question'),(t(76.44),e,[40,1314,1560,1402],PURPLE,'surrounding words takeaway')],'dense: complete-card framing')
 s=BYTAG['earlier']['start_frame'];e=at('history_reads',62.4);t=lambda q:at('earlier',q)
 # The narrative walks the two sentence rows, then connects IT with CAT.
 xs=[132.5+i*170 for i in range(8)];xs2=[202,372,542,743,913,1083,1253]
 rects=[[x+18,205,x+127,255] for x in xs]+[[x+18,425,x+(158 if i==2 else 127),475] for i,x in enumerate(xs2)]
 words=json.loads((ROOT/'video-audit/transformer-rerolls-2026-11-09/transcripts/transformer-6.json').read_text())['words']
 ww=[w for w in words if 49.88<=w['start']<54.08];ev=[]
 for i,w in enumerate(ww):
  if i>=len(rects):break
  # IT already has its own emphasized border; no second IT outline.
  if i==11:continue
  a=t(w['start']);z=t(ww[i+1]['start']) if i+1<len(ww) else t(54.5)
  if z>a:ev.append((a,z,rects[i],BLUE,w['word']))
 ev += [(t(55.9),BYTAG['qualifier']['start_frame'],rects[2],BLUE,'earlier CAT'),(at('qualifier',93.84),e,[40,558,1560,646],PURPLE,'qualified earlier AI takeaway')]
 board('earlier','transformer-before-transformers.jpg',s,e,[(s,None,'full'),(e,None,'full')],ev,'compact')
 s=at('history_reads',75.7);e=BYTAG['numbers_bridge']['start_frame'];t=lambda q:at('history_reads',q)
 board('reads','transformer-how-transformer-reads.jpg',s,e,[(s,None,'full'),(e,None,'full')],[(t(79.44),t(86.1),[40,127,1560,587],BLUE,'complete message'),(t(86.1),e,[40,627,1560,715],PURPLE,'earlier CAT connection')],'compact')
 s=BYTAG['mechanisms_return']['start_frame'];e=at('mechanisms_return',127.033);t=lambda q:at('mechanisms_return',q)
 board('numbers','transformer-attention-transformation.jpg',s,e,[(s,None,'full'),(e,None,'full')],[(t(107.69),t(117.68),[40,127,783,728],BLUE,'Attention'),(t(117.68),t(123.7),[816,127,1559,728],TEAL,'Transformation'),(t(123.7),e,[40,769,1560,857],PURPLE,'surrounding words update numbers')],'compact')
 s=e;e=BYTAG['sarcasm']['start_frame'];L=[40,127,783,1293];R=[816,127,1559,1293]
 l=lambda q:at('repeat_light',q);c=lambda q:at('light_clues',q);p=lambda q:at('repeat_pronouns',q);r=lambda q:at('pronoun_clues',q)
 board('resolves','transformer-resolves-meaning.jpg',s,e,
 [(s,None,'full'),(l(21.867),None,'establish'),(l(22.667),L,'left complete card'),(c(141.56),L,'left hold'),(c(142.34),R,'right complete card'),(r(148.2),R,'right hold'),(r(149.08),None,'takeaway'),(e,None,'end')],
 [(at('mechanisms_return',129.5),l(22.3),L,BLUE,'Different Meanings'),(l(22.3),l(25.14),[74,691,750,824],BLUE,'brightness example'),(l(25.14),c(131.9),[74,838,750,971],BLUE,'weight example'),(c(131.9),c(138.28),[74,1052,750,1155],BLUE,'turn on clue'),(c(138.28),c(142.0),[74,1160,750,1270],BLUE,'empty clue'),(c(142.34),p(29.08),R,GREEN,'Pronouns'),(p(29.08),p(34.2),[850,691,1526,824],GREEN,'cat example'),(p(34.2),r(144.4),[850,838,1526,971],GREEN,'milk example'),(r(144.4),r(147.28),[850,1052,1526,1155],GREEN,'cat clue'),(r(147.28),r(148.2),[850,1160,1526,1270],GREEN,'milk clue'),(r(149.08),e,[40,1333,1560,1421],PURPLE,'meaning takeaway')],'dense: complete-card framing')
 s=BYTAG['order_close']['start_frame'];e=at('order_close',215+5/30);t=lambda q:at('order_close',q)
 board('order','transformer-word-order.jpg',s,e,[(s,None,'full'),(e,None,'full')],[(t(182.92),t(186.26),[40,127,1560,267],PURPLE,'different word orders'),(t(186.26),t(198.56),[40,299,783,758],TEAL,'Without Position Information'),(t(198.56),t(210.46),[816,299,1559,758],'#4f2fc4','Position Stamps Preserve Order'),(t(210.46),e,[40,799,1560,887],PURPLE,'position takeaway')],'compact')
 b.make_close('attention')
 return specs,meta,rs,b.close_img,e

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args();assert not DEST.exists(),'Never overwrite a candidate'
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 protected={str(p):sha(p) for p in [*SRC.values(),ROOT/'course-assets/transformer/transformer.mp4',ROOT/'lessons/transformer.md',*sorted((ROOT/'course-assets/transformer').glob('*.jpg'))]}
 audio=prepare_audio();specs,meta,renderers,close,close_start=prepare_boards()
 # Selected original illustrations. Retiming affects pictures only, never speech.
 visuals=[dict(tag='intro',start=0,end=fr(20.767),source=6,source_start=0,source_end=fr(20.767),repair=None),
 dict(tag='human-clues',start=at('opening',79+14/30),end=at('opening',84.6),source=5,source_start=2384,source_end=2538,repair=None),
 dict(tag='earlier-sequence',start=at('opening',84.6),end=BYTAG['earlier']['start_frame'],source=5,source_start=2538,source_end=fr(92+23/30),repair=None),
 dict(tag='paper',start=at('history_reads',62.4),end=at('history_reads',71+25/30),source=5,source_start=3348,source_end=3605,repair=None),
 dict(tag='transformer-T',start=at('history_reads',71+25/30),end=at('history_reads',75.7),source=6,source_start=2155,source_end=fr(75.7),repair='cover-specialist-stack'),
 dict(tag='numbers-bridge',start=BYTAG['numbers_bridge']['start_frame'],end=BYTAG['mechanisms_return']['start_frame'],source=5,source_start=fr(147+5/30),source_end=fr(156.7),repair='remove-early-attention-heading'),
 dict(tag='idioms',start=BYTAG['sarcasm']['start_frame'],end=BYTAG['order_close']['start_frame'],source=5,source_start=6107,source_end=6371,repair=None)]
 states=[]
 for key,r in renderers.items():
  wanted={0,len(r.cameras)-1};cursor=0
  for beat in specs[key]['beats']:
   z=cursor+beat['frames'];wanted|={cursor,(cursor+z)//2,z-1};cursor=z
  for a,z,*_ in r.rings:wanted|={a,(a+z)//2,z-1}
  for local in sorted(wanted):
   im,_,geo=r.at(local);n=meta[key]['start_frame']+local;p=OUT/'preview'/f'{n:05d}-{key}.jpg';cv2.imwrite(str(p),im);states.append(dict(frame=n,path=str(p),board=key,rings=geo))
 boundaries=sorted(set([r['start_frame'] for r in ROWS[1:]]+[v[k] for v in meta.values() for k in ['start_frame','end_frame']]+[v[k] for v in visuals for k in ['start','end']]+[close_start])-{0,TOTAL})
 m=dict(candidate=str(DEST),fps=30,frame_count=TOTAL,duration=TOTAL/30,approval='User: Build it please. Approved November 9 combined-roll review plan; build only.',scope='Full production review candidate; not installed, committed, or published.',sources={str(k):dict(path=str(p),sha256=sha(p)) for k,p in SRC.items()},timeline=ROWS,audio=audio,boards=meta,specs=specs,prepared_states=states,supporting_visuals=visuals,boundaries=boundaries,close=dict(start_frame=close_start,hold=48,push=150,endpoint=1.2,settled_frames=TOTAL-close_start-198),protected=protected,direct_listening=False,script_deviation='Number-update banner narration omits AI; intact source sentence retained. Canonical board has approved exact text.',status='prepared')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(f'Prepared {TOTAL} frames, {TOTAL/30:.2f}s; donor gains {audio["donor_gain_db"]}',flush=True)
 if args.prepare_only:return
 proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 readers={v['tag']:Reader(SRC[v['source']]) for v in visuals};mask=glyph_mask();clean_counts={};visual_samples=[]
 for n in range(TOTAL):
  board=next((key for key,x in meta.items() if x['start_frame']<=n<x['end_frame']),None)
  if n>=close_start:
   k=n-close_start;q=np.clip((k-48)/149,0,1);z=1+.2*q*q*(3-2*q);h,w=close.shape[:2];ww=w/z;hh=ww*9/16
   im=cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
  elif board:im=renderers[board].at(n-meta[board]['start_frame'])[0]
  else:
   v=next(v for v in visuals if v['start']<=n<v['end']);f=v['source_start']+int((n-v['start'])*(v['source_end']-v['source_start'])/(v['end']-v['start']));im=readers[v['tag']].at(f)
   im,how=clean_frame(im,mask);clean_counts[how]=clean_counts.get(how,0)+1
   if v['repair']=='remove-early-attention-heading':
    # Same-frame paper clone, no diagram pixels touched. Header fixed throughout source.
    im[65:119,360:920]=im[5:59,360:920]
   elif v['repair']=='cover-specialist-stack':
    # Keep the ChatGPT/T reveal; replace only lower technical stack with same-frame paper.
    im[220:650,320:960]=cv2.resize(im[220:650,0:300],(640,430))
   if n in [v['start'],(v['start']+v['end'])//2,v['end']-1]:
    p=OUT/'preview'/f'{n:05d}-{v["tag"]}.jpg';cv2.imwrite(str(p),im);visual_samples.append(str(p))
  proc.stdin.write(im.tobytes())
  if n%900==899:print(f'Rendered {n+1}/{TOTAL}',flush=True)
 proc.stdin.close();assert proc.wait()==0
 for rd in readers.values():rd.c.release()
 assert all(sha(Path(p))==h for p,h in protected.items())
 m.update(status='built for review',candidate_sha256=sha(DEST),corner_cleanup=clean_counts,supporting_previews=visual_samples);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
