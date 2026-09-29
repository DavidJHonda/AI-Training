#!/usr/bin/env python3
"""Accepted live bookends plus whole-beat Notebook narration donors; review only."""
from pathlib import Path
import hashlib,json,subprocess,sys,wave
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Reader
import build_opener_work_fola_review as board_helper
from gemini_mark import clean_frame,glyph_mask
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/work-with-ai-opener-hybrid-2026-09-29-v11'
DEST=ROOT/'Prompts/work-with-ai-opener-v11.mp4'
FF=imageio_ffmpeg.get_ffmpeg_exe();SR=48000;SPF=1600;FPS=30
SOURCES={
 'live':('course-assets/work-with-ai-opener/work-with-ai-opener.mp4','48c90ec931943f0a98464aafe74d5b99c3ff7967db9d4b0af16bde6f146ac4ed'),
 'roll1':('Prompts/work-with-ai-opener-1.mp4','9a814c123cd6b105d31390406053da7639af26db6b97e510f189ccf7c4ff1b03'),
 'roll3':('Prompts/work-with-ai-opener-3.mp4','324776db7d0187d3776615dabad3adb0321bd838760756d46e3046c871cbca79')}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(args):subprocess.run(list(map(str,args)),check=True)
def read(p):
 with wave.open(str(p)) as w:
  assert(w.getnchannels(),w.getframerate(),w.getsampwidth())==(1,SR,2)
  return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)/32768

def main():
 assert not DEST.exists(),'Use a new candidate filename.'
 OUT.mkdir(exist_ok=True)
 paths={k:ROOT/v[0] for k,v in SOURCES.items()}
 protected={str(p):sha(p) for p in [*paths.values(),ROOT/'index.html',*sorted((ROOT/'course-assets/work-with-ai-opener').glob('*.jpg'))]}
 for k,p in paths.items():assert sha(p)==SOURCES[k][1],k
 data={}
 for k,p in paths.items():
  wav=OUT/f'{k}.wav'
  run([FF,'-v','error','-y','-i',p,'-vn','-ac','1','-ar',SR,'-c:a','pcm_s16le',wav]);data[k]=read(wav)
 rows=[dict(source='live',start=0,end=2628,label='Accepted opening, camera comparison and Know What It Is For'),
       dict(source='roll3',start=3240,end=3540,label='Use It Well: qualified context and what the model reads'),
       dict(source='roll1',start=3280,end=4095,label='Verification plus qualified three-step takeaway'),
       dict(source='live',start=4384,end=4737,label='Accepted canonical close and original closing audio')]
 # Match active-speech RMS, not silence-inclusive RMS. Only donor gain changes.
 ref=board_helper.gated_db(data['live'][65*SR:87*SR]);at=0;parts=[]
 seed=data['live'][round(146.3*SR):round(146.5*SR)].copy();seed-=seed.mean();loop=np.r_[seed,seed[::-1]]
 for n,row in enumerate(rows):
  x=data[row['source']][row['start']*SPF:row['end']*SPF].copy();row['gain_db']=0
  if row['source']!='live':
   row['gain_db']=min(ref-board_helper.gated_db(x),20*np.log10(.89125/max(abs(x))))
   x*=10**(row['gain_db']/20)
  row['active_db']=board_helper.gated_db(x);row['output_start']=at;row['frames']=row['end']-row['start'];at+=row['frames'];row['output_end']=at
  # Five-millisecond room-tone crossfades only inside measured quiet joins.
  ramp=np.linspace(0,1,240);bed=np.resize(loop,240)
  if n:x[:240]=x[:240]*ramp+bed*(1-ramp)
  if n<len(rows)-1:x[-240:]=x[-240:]*(1-ramp)+bed*ramp
  parts.append(x)
 audio=np.concatenate(parts);assert len(audio)==at*SPF
 board_helper.write(OUT/'edited.wav',audio)
 board_helper.AUDIT=OUT
 asset=ROOT/'course-assets/work-with-ai-opener/work-with-ai-opener-section-map.jpg'
 leg1,spec1=board_helper.board('use-and-think',asset,515,[
  dict(start=35,end=337,rect=[100,335,1400,162],color='#1652f0'),
  dict(start=337,end=515,rect=[100,527,1400,163],color='#0e8f86')])
 leg2,spec2=board_helper.board('takeaway',asset,180,[dict(start=11,end=180,rect=[40,743,1520,88],color='#6e51ff')])
 visuals=[dict(start=0,end=2628,kind='live',source_start=0),
          dict(start=2628,end=3143,kind='board',file=str(leg1)),
          dict(start=3143,end=3563,kind='donor1',source_start=3495),
          dict(start=3563,end=3743,kind='board',file=str(leg2)),
          dict(start=3743,end=4096,kind='live',source_start=4384)]
 manifest=dict(candidate=str(DEST),scope='Authorized review build: accepted live bookends, donor context/verification, qualified takeaway',
  sources={k:dict(path=str(paths[k]),sha256=SOURCES[k][1]) for k in paths},audio_rows=rows,visual_rows=visuals,
  total_frames=at,duration=at/30,fps=30,board_specs=[spec1,spec2],protected=protected,
  declared_boundaries=[2628,2928,3143,3563,3743],
  new_pauses='none',join_fades_ms=5,listening='not performed; donor voice continuity and joins need review',
  text_note='Approved build uses semantically qualified donor paraphrases; exact prep wording not asserted.')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 readers={'live':Reader(paths['live']),'donor1':Reader(paths['roll1'])}
 mask=glyph_mask();clean={};p=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar',str(SR),'-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 try:
  for row in visuals:
   r=Reader(row['file']) if row['kind']=='board' else readers[row['kind']]
   for j in range(row['end']-row['start']):
    im=r.at(row.get('source_start',0)+j)
    if row['kind']=='donor1':
     im,method=clean_frame(im,mask);clean[method or 'declined']=clean.get(method or 'declined',0)+1
    p.stdin.write(im.tobytes())
   print('Rendered',row['end'],'/',at,flush=True)
 finally:p.stdin.close()
 assert p.wait()==0
 assert all(sha(Path(k))==v for k,v in protected.items())
 manifest['mark_cleanup']=clean;manifest['candidate_sha256']=sha(DEST)
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({'candidate':str(DEST),'frames':at,'duration':at/30,'audio_rows':rows,'cleanup':clean},indent=2))
if __name__=='__main__':main()
