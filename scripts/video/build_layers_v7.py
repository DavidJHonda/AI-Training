#!/usr/bin/env python3
"""Approved Layers repair: complete-column cameras, drawing breaks, full sentence.
Review only. Original canonical source and boards remain untouched.
"""
from pathlib import Path
import argparse,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Build,Reader,sha,readwav,writewav
from build_embeddings_v7 import Renderer
from ken_burns_path import fit_window
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'course-assets/layers/layers.mp4'
EXPECTED='22c403f13e4dcab98aedaf475b91ae6f5af60d1bbb910b8250bcddb2dcdecde5'
DONOR=ROOT/'course-assets/vector-space/vector-space.mp4'
DONOR_SHA='4873fac38f54ff14ebaff06b0787a8922e9e15bb99712b0332d767ad41f5b563'
OLD=ROOT/'video-audit/layers-comparison-2026-09-23/build-v3'
OUT=ROOT/'video-audit/layers-repair-2026-09-28-v7'
DEST=ROOT/'Prompts/layers-v7.mp4'
FPS=30;SPF=1600;FADE=240;TOTAL=5841;INSERT=3240;DA=6037;DZ=6160;EXTRA=DZ-DA
BREAKS=[(2259,2409),(3933,4156)]
def output_frame(f):return f+(EXTRA if f>=INSERT else 0)
def timeline():return [dict(source='layers',source_start=0,source_end=INSERT,start_frame=0,end_frame=INSERT),dict(source='vector-space',source_start=DA,source_end=DZ,start_frame=INSERT,end_frame=INSERT+EXTRA),dict(source='layers',source_start=INSERT,source_end=TOTAL,start_frame=INSERT+EXTRA,end_frame=TOTAL+EXTRA)]
def runs(mapped):
 out=[]
 for i,item in enumerate(mapped):
  label=item[0] if item else 'original'
  if not out or out[-1]['label']!=label:out.append(dict(label=label,start_frame=i,end_frame=i+1))
  else:out[-1]['end_frame']=i+1
 return out

def setup():
 old=json.loads((OLD/'edit-manifest.json').read_text());assert old['render_sha256']==EXPECTED
 snapshot=Path(json.loads((OUT/'source-snapshot.json').read_text())['path']);assert sha(snapshot)==EXPECTED
 b=Build(ROOT,snapshot,OUT,DEST);specs={};renderers={};frames=list(range(INSERT))+[None]*EXTRA+list(range(INSERT,TOTAL));mapped=[None]*len(frames)
 spans={'1-horse':(155,1359),'2-numbers':(1923,3079),'3-it-cat':(INSERT,output_frame(4451))}
 for key,meta in old['boards'].items():
  asset=ROOT/meta['asset'];assert sha(asset)==meta['sha256'];canvas,cw,ch,ox,oy=b.compose(asset,key);assert [ox,oy]==meta['canvas_offset']
  s=json.loads((OLD/f'leg-{key}.json').read_text());s['image']=str(canvas);s['beats'][0]['frames']=spans[key][1]-spans[key][0];specs[key]=s
  for f in range(*spans[key]):mapped[f]=(key,f-spans[key][0])
 # Horse: each original full-height column contains its title, text and drawing.
 h=specs['1-horse'];full=h['beats'][0]['from'];cols=[x['rect'] for x in h['rings'][:3]]
 cams=[fit_window(dict(fit=rect,margin=14),16/9,1280,3) for rect in cols]
 pts=[(155,full,'start'),(302,full,'sentence and setup'),(326,cams[0],'zoom to First Read'),(539,cams[0],'First Read'),(585,cams[1],'pan to More Reads'),(867,cams[1],'More Reads'),(886,cams[2],'pan to Meaning Clicks'),(1251,cams[2],'Meaning Clicks'),(1276,full,'pull back for takeaway'),(1359,full,'takeaway')]
 h['beats']=[dict(label=z[2],frames=z[0]-a[0],**{'from':a[1],'to':z[1]}) for a,z in zip(pts,pts[1:])]
 oldrings=h['rings'];h['rings']=[]
 for a,z,oldring in [(302,539,oldrings[0]),(585,867,oldrings[1]),(886,1276,oldrings[2]),(1276,1359,oldrings[3])]:
  r=oldring.copy();r.update(start=a-155,end=z-155);h['rings'].append(r)
 old['boards']['1-horse']['density']='dense'
 # Numbers: full view, retain the complete diagram and actual number cards.
 num=specs['2-numbers'];num['rings'][0].update(start=60,end=2259-1923)
 for key,index,rect in [('2-numbers',1,[74,860,315,132]),('2-numbers',2,[1212,860,314,132])]:
  ox,oy=old['boards'][key]['canvas_offset'];x,y,w,hh=rect;specs[key]['rings'][index]['rect']=[x+ox,y+oy,w,hh]
 # Exact ASR onset of starting pair; retain later existing onsets from matched build.
 num['rings'][1]['start']=round(81.94*30)-1923
 # IT/CAT: sentence alone during donor, then one whole stage at a time.
 s=specs['3-it-cat'];oldrings=s['rings'];sentence=oldrings[0].copy();sentence.update(start=3,end=EXTRA+8);s['rings']=[sentence]
 for r in oldrings[1:]:
  q=r.copy();q['start']=3243+r['start']-INSERT+EXTRA;q['end']=3243+r['end']-INSERT+EXTRA;s['rings'].append(q)
 # Clearing Repeat for the drawing and returning unmarked before Result is deliberate.
 repeat=s['rings'][4];repeat['end']=output_frame(BREAKS[1][0])-INSERT
 for a,z in BREAKS:
  for f in range(output_frame(a),output_frame(z)):mapped[f]=('drawing',1800)
 for key,s in specs.items():
  (OUT/f'leg-{key}.json').write_text(json.dumps(s,indent=2)+'\n');renderers[key]=Renderer(s)
 rd=Reader(snapshot);drawing=rd.at(1800);rd.c.release()
 return snapshot,old,frames,mapped,specs,renderers,drawing

def speech_rms(x):
 chunks=x[:len(x)//960*960].reshape(-1,960);energy=np.mean(chunks*chunks,axis=1);active=energy>32768**2*10**(-35/10)
 return float(np.sqrt(np.mean(energy[active])))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a review candidate';assert sha(SOURCE)==EXPECTED and sha(DONOR)==DONOR_SHA
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 snapshot,old,frames,mapped,specs,renderers,drawing=setup();a=readwav(OUT/'source.wav')[:TOTAL*SPF];donor=readwav(OUT/'donor.wav')[DA*SPF:DZ*SPF]
 target=speech_rms(a[round(102.6*48000):round(111.2*48000)]);gain=target/speech_rms(donor)
 assert .5<gain<2
 writewav(OUT/'donor-selected.wav',donor)
 # The donor has a high crest factor. Match speech level while limiting peaks;
 # latency compensation preserves sample alignment and complete word tails.
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 subprocess.run([ff,'-v','error','-y','-i',str(OUT/'donor-selected.wav'),'-af',f'volume={gain:.12f},alimiter=limit=0.97:attack=5:release=50:level=false:latency=true','-c:a','pcm_s16le',str(OUT/'donor-matched.wav')],check=True)
 donor=readwav(OUT/'donor-matched.wav');assert len(donor)==EXTRA*SPF and max(abs(donor))<32767
 matched_rms=speech_rms(donor)
 parts=[a[:INSERT*SPF].copy(),donor,a[INSERT*SPF:].copy()]
 for i,x in enumerate(parts):
  if i:x[:FADE]*=np.linspace(0,1,FADE)
  if i<2:x[-FADE:]*=np.linspace(1,0,FADE)
 audio=np.concatenate(parts);writewav(OUT/'edited.wav',audio);writewav(OUT/'join-review.wav',audio[102*48000:118*48000]);assert len(audio)==len(frames)*SPF
 protected={str(p):sha(p) for p in [SOURCE,DONOR,ROOT/'index.html',ROOT/'lessons/layers.md',ROOT/'Prompts/layers-video-prompt.txt',*sorted((ROOT/'course-assets/layers').glob('*.jpg'))]}
 states=[]
 for key,r in renderers.items():
  available=[i for i,item in enumerate(mapped) if item and item[0]==key];wanted={0,len(r.cameras)-1};at=0
  for beat in specs[key]['beats']:
   z=at+beat['frames'];wanted|={at,(at+z-1)//2,z-1};at=z
  for ring in r.rings:wanted|={ring[0],min(ring[0]+15,ring[1]-1),ring[1]-1}
  for out in available:
   local=mapped[out][1]
   if local not in wanted:continue
   im,_,geo=r.at(local);p=OUT/'preview'/f'{out:05d}-{key}.jpg';cv2.imwrite(str(p),im);states.append(dict(output_frame=out,key=key,local_frame=local,path=str(p),rings=geo))
 visual=runs(mapped);boundaries=sorted(set([output_frame(x['frame']) for x in old['boundaries']]+[INSERT,INSERT+EXTRA]+[r['start_frame'] for r in visual[1:]]))
 m=dict(source=str(SOURCE),source_sha256=EXPECTED,donor=str(DONOR),donor_sha256=DONOR_SHA,snapshot=str(snapshot),candidate=str(DEST),fps=FPS,frames=len(frames),duration=len(frames)/FPS,timeline=timeline(),visual_timeline=visual,boards=old['boards'],specs=specs,prepared_states=states,boundaries=boundaries,protected=protected,donor_gain=gain,donor_gain_db=float(20*np.log10(gain)),donor_peak_limiter=dict(limit=.97,attack_ms=5,release_ms=50,latency_compensated=True),donor_speech_rms_db_difference=float(20*np.log10(matched_rms/target)),audio_ramp_samples=FADE,close_span_frames=[output_frame(5520),len(frames)],drawing_reuse=dict(source_frame=1800,output_spans_frames=[[output_frame(a),output_frame(z)] for a,z in BREAKS]),approval='David: agree. Build it please. Approved September 28 Layers plan, review only; no publication. Source audio retained except full-sentence insertion; no added pauses.',listening_performed=False)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('Prepared',len(frames),'frames',len(frames)/30,'seconds; donor gain',m['donor_gain_db'],'dB',flush=True)
 if args.prepare_only:return
 ff=imageio_ffmpeg.get_ffmpeg_exe();proc=subprocess.Popen([ff,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 rd=Reader(snapshot)
 for out,f in enumerate(frames):
  item=mapped[out]
  im=(drawing if item[0]=='drawing' else renderers[item[0]].at(item[1])[0]) if item else rd.at(f)
  proc.stdin.write(im.tobytes())
  if out%1000==999:print('Rendered',out+1,flush=True)
 proc.stdin.close();assert proc.wait()==0;rd.c.release();assert all(sha(Path(p))==h for p,h in protected.items())
 m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
