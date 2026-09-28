#!/usr/bin/env python3
"""Approved Transformer repair: reread four sentences, sentence/clue rings, fixed 4 px.
Current published MP4 is the only available narration source. Review candidate only.
"""
from pathlib import Path
import argparse,json,subprocess,copy
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Build,Reader,sha,readwav,writewav
from build_embeddings_v7 import Renderer
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'course-assets/transformer/transformer.mp4'
EXPECTED='d55f0000452087fb4b7993b2e79e06759ef263e147362cbd744a3c44883d9eb6'
OLD=ROOT/'video-audit/transformer-comparison-2026-09-22/build-v10'
OUT=ROOT/'video-audit/transformer-repair-2026-09-28-v12'
DEST=ROOT/'Prompts/transformer-v12.mp4'
TOTAL=6788;FPS=30;SPF=1600;FADE=240
# Half-open 30 fps source-frame intervals. Word tails verified against 5/20 ms RMS.
# The fourth sentence reuses the common prefix and the actual fresh clause.
EDITS=[dict(at=1431,end=1431,key='opening-fresh-prefix',donors=[(1246,1285)]),
       dict(at=4396,end=4396,key='light-brightness',donors=[(908,946)]),
       dict(at=4494,end=4521,key='light-not-heavy',donors=[(1033,1093)]),
       dict(at=4656,end=4656,key='it-thirsty',donors=[(1246,1320)]),
       dict(at=4755,end=4755,key='it-fresh',donors=[(1246,1285),(1431,1466)])]

def timeline():
 rows=[];cursor=0;out=0
 def add(a,b,key,kind):
  nonlocal out
  if b<=a:return
  rows.append(dict(source_start=a,source_end=b,start_frame=out,end_frame=out+b-a,label=key,kind=kind));out+=b-a
 for e in EDITS:
  add(cursor,e['at'],'retained','retained')
  for i,(a,b) in enumerate(e['donors']):add(a,b,e['key']+f'-part-{i+1}','reread')
  cursor=e['end']
 add(cursor,TOTAL,'retained','retained')
 return rows

def output_frame(source_frame):
 for r in timeline():
  if r['kind']=='retained' and r['source_start']<=source_frame<r['source_end']:
   return r['start_frame']+source_frame-r['source_start']
 raise ValueError(source_frame)

def setup():
 old=json.loads((OLD/'edit-manifest.json').read_text());assert old['render_sha256']==EXPECTED
 snapshot=Path(json.loads((OUT/'source-snapshot.json').read_text())['path']);assert sha(snapshot)==EXPECTED
 b=Build(ROOT,snapshot,OUT,DEST);specs={};renderers={};original_map=[None]*TOTAL
 rows=timeline();n=rows[-1]['end_frame'];mapped=[None]*n;frames=[None]*n
 for r in rows:
  if r['kind']=='retained':frames[r['start_frame']:r['end_frame']]=range(r['source_start'],r['source_end'])
 for key,meta in old['boards'].items():
  asset=ROOT/meta['asset'];assert sha(asset)==meta['sha256'];canvas,cw,ch,ox,oy=b.compose(asset,key);assert [ox,oy]==meta['canvas_offset']
  spec=json.loads((OLD/f'leg-{key}.json').read_text());spec['image']=str(canvas);specs[key]=spec
 for row in old['timeline']:
  key=row.get('visual')
  if key not in old['boards']:continue
  for f in range(row['start_frame'],row['end_frame']):
   original_map[f]=(key,row['source_start']+f-row['start_frame']-old['boards'][key]['src_in'])
 for out,f in enumerate(frames):
  if f is not None:mapped[out]=original_map[f]
 start=output_frame(4364);end=output_frame(5008)
 spec=specs['resolves'];spec['beats'][0]['frames']=end-start
 ox,oy=old['boards']['resolves']['canvas_offset']
 blue='#1652f0';green='#0f7a4a';purple='#6e51ff'
 # In original JPG coordinates: measured tinted sentence boxes and the two clue paragraphs.
 s1=[74,691,750,805];s2=[74,818,750,932];s3=[850,691,1526,805];s4=[850,818,1526,932]
 c1=[90,1010,734,1098];c2=[90,1106,734,1196];c3=[866,1010,1510,1098];c4=[866,1106,1510,1196]
 inserts={e['key']:next(r['start_frame'] for r in rows if r['label']==e['key']+'-part-1') for e in EDITS}
 events=[(inserts['light-brightness']+1,s1,blue,'read light / brightness'),
         (output_frame(4402),c1,blue,'explain turn on'),
         (inserts['light-not-heavy']+2,s2,blue,'read light / not heavy'),
         (output_frame(4526),c2,blue,'explain carry'),
         (output_frame(4608),[40,127,783,1233],None,'clear at pronoun introduction'),
         (inserts['it-thirsty']+2,s3,green,'read it / thirsty'),
         (output_frame(4664),c3,green,'explain thirsty'),
         (inserts['it-fresh']+2,s4,green,'read it / fresh'),
         (output_frame(4768),c4,green,'explain fresh'),
         (output_frame(4879),[40,1275,1560,1363],purple,'takeaway banner')]
 spec['rings']=[]
 for i,(at,rect,color,label) in enumerate(events):
  if color is None:continue
  stop=events[i+1][0] if i+1<len(events) else end
  x0,y0,x1,y1=rect
  spec['rings'].append(dict(start=at-start,end=stop-start,rect=[x0+ox,y0+oy,x1-x0,y1-y0],color=color,pad=0,radius=12 if color!=purple else 22,label=label))
 for out in range(start,end):mapped[out]=('resolves',out-start)
 # Complete-card cameras share the same geometry-relative fit and smooth moves.
 from ken_burns_path import fit_window
 def card_camera(key,rect):
  ox,oy=old['boards'][key]['canvas_offset'];x0,y0,x1,y1=rect
  return fit_window(dict(fit=[x0+ox,y0+oy,x1-x0,y1-y0],margin=10),16/9,1280,3)
 def beats(key,points):
  spec=specs[key];spec['beats']=[]
  for (a,cam),(z,target,label) in zip([(p[0],p[1]) for p in points],points[1:]):
   spec['beats'].append(dict(label=label,frames=z-a,**{'from':cam,'to':target}))
 full=specs['context1']['beats'][0]['from']
 left=card_camera('context1',[40,127,783,1171]);right=card_camera('context1',[816,127,1560,1171])
 beats('context1',[(0,full,'start'),(60,full,'full board'),(96,left,'zoom to complete light card'),(445,left,'light examples'),(464,right,'pan to pronoun card')])
 specs['context1']['rings'][-1]['end']=445
 # Preserve the intervening illustration, then return to the right-card view.
 start2=output_frame(1286);end2=output_frame(1610)
 for ring in specs['context2']['rings']:
  ring['start']=output_frame(1286+ring['start'])-start2
  ring['end']=output_frame(1286+ring['end'])-start2
 banner=output_frame(1536)-start2
 beats('context2',[(0,right,'start'),(banner-24,right,'pronoun examples'),(banner,full,'return to full board'),(end2-start2,full,'takeaway')])
 for out in range(start2,end2):mapped[out]=('context2',out-start2)
 # Same whole-board, left-card, pan-right, whole-board sequence for explanations.
 full5=specs['resolves']['beats'][0]['from'];left5=card_camera('resolves',[40,127,783,1233]);right5=card_camera('resolves',[816,127,1560,1233])
 pan=output_frame(4608)-start;land=inserts['it-thirsty']-start;banner5=output_frame(4879)-start
 beats('resolves',[(0,full5,'start'),(60,full5,'full board'),(84,left5,'zoom to complete light card'),(pan,left5,'light explanations'),(land,right5,'pan to complete pronoun card'),(banner5-24,right5,'pronoun explanations'),(banner5,full5,'return to full board'),(end-start,full5,'takeaway')])
 # Highlight only words explicitly spoken as examples. Insets avoid redrawing
 # the board's existing chip borders, especially its built-in purple IT border.
 word_rects={'the':[110,206,220,258],'cat':[325,206,433,258],'sat':[541,206,645,258],'it':[980,425,1058,479]}
 word_events=[(62.82,63.82,'the'),(63.82,64.88,'cat'),(64.88,65.62,'sat'),(70.66,71.86,'it'),(71.86,73.88,'cat')]
 earlier=specs['earlier'];earlier['rings']=earlier['rings'][-1:]
 for a,z,word in word_events:
  x0,y0,x1,y1=word_rects[word];ox,oy=old['boards']['earlier']['canvas_offset']
  earlier['rings'].append(dict(start=round(a*30)-1848,end=round(z*30)-1848,rect=[x0+ox,y0+oy,x1-x0,y1-y0],color=blue,pad=0,radius=8,label='spoken word '+word))
 for key in ['context1','context2','resolves']:old['boards'][key]['density']='dense'
 for key,spec in specs.items():
  (OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n');renderers[key]=Renderer(spec)
 assert all(f is not None or mapped[i] for i,f in enumerate(frames))
 return snapshot,old,rows,frames,mapped,specs,renderers

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a review candidate';assert sha(SOURCE)==EXPECTED
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 snapshot,old,rows,frames,mapped,specs,renderers=setup()
 source=readwav(OUT/'source.wav')[:TOTAL*SPF];parts=[]
 for i,r in enumerate(rows):
  a=source[r['source_start']*SPF:r['source_end']*SPF].copy()
  if i:a[:FADE]*=np.linspace(0,1,FADE)
  if i<len(rows)-1:a[-FADE:]*=np.linspace(1,0,FADE)
  parts.append(a)
 audio=np.concatenate(parts);writewav(OUT/'edited.wav',audio);assert len(audio)==len(frames)*SPF
 writewav(OUT/'repaired-section.wav',audio[output_frame(4364)*SPF:output_frame(5008)*SPF])
 protected={str(p):sha(p) for p in [SOURCE,ROOT/'lessons/transformer.md',ROOT/'Prompts/transformer-video-prompt.txt',*sorted((ROOT/'course-assets/transformer').glob('*.jpg'))]}
 states=[];spans={}
 for key,r in renderers.items():
  available=[i for i,item in enumerate(mapped) if item and item[0]==key];spans[key]=[min(available),max(available)+1]
  wanted={0,len(r.cameras)-1}
  at=0
  for beat in specs[key]['beats']:
   z=at+beat['frames'];wanted|={at,(at+z-1)//2,z-1};at=z
  for ring in r.rings:wanted|={ring[0],min(ring[0]+15,ring[1]-1),ring[1]-1}
  for out in available:
   local=mapped[out][1]
   if local not in wanted:continue
   im,_,geo=r.at(local);p=OUT/'preview'/f'{out:05d}-{key}.jpg';cv2.imwrite(str(p),im)
   states.append(dict(output_frame=out,key=key,local_frame=local,path=str(p),rings=geo))
 spans['close']=[output_frame(old['close']['start_frame']),len(frames)]
 boundaries=sorted(set([output_frame(b['frame']) for b in old['boundaries']]+[r['start_frame'] for r in rows[1:]]))
 m=dict(source=str(SOURCE),source_sha256=EXPECTED,snapshot=str(snapshot),candidate=str(DEST),fps=FPS,frames=len(frames),duration=len(frames)/FPS,timeline=rows,edits=EDITS,audio_ramp_samples=FADE,boards=old['boards'],specs=specs,prepared_states=states,candidate_board_spans_frames=spans,boundaries=boundaries,protected=protected,approval='David requested zoom/pan on opening and resolution boards, full fresh sentence in opening, and word highlights on earlier-AI board. Carries forward approved v11 rereads and 4 px outlines. Preserve lesson and illustrative graphics. Build for review; not publication.')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('Prepared',len(frames),'frames;',len(frames)/30,'seconds; board spans',spans,flush=True)
 if args.prepare_only:return
 ff=imageio_ffmpeg.get_ffmpeg_exe();proc=subprocess.Popen([ff,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 rd=Reader(snapshot)
 for out,f in enumerate(frames):
  item=mapped[out];im=renderers[item[0]].at(item[1])[0] if item else rd.at(f);proc.stdin.write(im.tobytes())
  if out%1000==999:print('Rendered',out+1,flush=True)
 proc.stdin.close();assert proc.wait()==0;rd.c.release();assert all(sha(Path(p))==h for p,h in protected.items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
