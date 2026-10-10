#!/usr/bin/env python3
"""Approved calculation graft from One More Thing v14 into Data Centers v6.
Review candidate only. Source frames are decoded sequentially; no shared edits.
"""
from pathlib import Path
import json,subprocess,hashlib,wave
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
from editspec_build import Reader,readwav,writewav
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/data-centers-lesson-update-2026-10-09/build-v7'
BASE=ROOT/'Prompts/data-centers-v6.mp4'
DONOR=ROOT/'Prompts/one-more-thing-v14.mp4'
DEST=ROOT/'Prompts/data-centers-v7.mp4'
BOARD=ROOT/'course-assets/data-centers/data-centers-math.jpg'
EXPECTED={str(BASE):'2b728ffd3fc3d5f61dfa1e6d44d7398fb82c0bac28269b50b3b8cae593eda89c',str(DONOR):'321a52242ce10b86e151a8ffcf000b4684db8a340945da06fe3b317eee8a86ca'}
FPS=30;SPF=1600
BASE_OUT=276;BASE_IN=834;DONOR_IN=4401;DONOR_OUT=5701;BASE_FRAMES=6694
INSERT=DONOR_OUT-DONOR_IN;RESUME=BASE_OUT+INSERT
DELTA=INSERT-(BASE_IN-BASE_OUT);TOTAL=BASE_FRAMES+DELTA
# Donor 177.0–183.5 sec carries the old base's 17.6–24.1 arithmetic build.
CUT_IN=5310;CUT_OUT=5505;CUT_SOURCE=528
# Keep new board through the compute definition; return at the world-demand scene.
VISUAL_RESUME=944
GAIN_DB=-0.28

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dm(f):return BASE_OUT+f-DONOR_IN
def bm(f):return f+DELTA

def boards():
 image=Image.open(BOARD).convert('RGB');assert image.size==(1600,890)
 base=Image.new('RGB',(1280,720),'white');base.paste(image.resize((1280,712),Image.Resampling.LANCZOS),(0,4))
 specs={'none':None,'one':([40,118,525,722],'#1652f0'),'short':([557,118,1043,722],'#4f2fc4'),'long':([1075,118,1560,722],'#0e8f86'),'takeaway':([40,762,1560,850],'#6e51ff')}
 result={}
 for name,spec in specs.items():
  im=base.copy()
  if spec:
   rect,color=spec;rect=[round(rect[0]*.8),round(rect[1]*.8)+4,round(rect[2]*.8),round(rect[3]*.8)+4]
   ImageDraw.Draw(im).rounded_rectangle(rect,radius=11,outline=color,width=4)
  result[name]=cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
  im.save(OUT/f'board-{name}.png')
 return result

def main():
 assert not DEST.exists(),'Never overwrite a review candidate'
 for p,h in EXPECTED.items():assert sha(p)==h,p
 OUT.mkdir(parents=True,exist_ok=True)
 protected={str(p):sha(p) for p in [BASE,DONOR,BOARD,ROOT/'course-assets/data-centers/data-centers.mp4',ROOT/'course-assets/the-next-token/the-next-token.mp4',ROOT/'lessons/data-centers.md']}
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 for key,source in [('base',BASE),('donor',DONOR)]:
  subprocess.run([ff,'-v','error','-i',str(source),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le','-y',str(OUT/f'{key}.wav')],check=True)
 base=readwav(OUT/'base.wav');donor=readwav(OUT/'donor.wav')
 parts=[base[:BASE_OUT*SPF].copy(),donor[DONOR_IN*SPF:DONOR_OUT*SPF].copy()*10**(GAIN_DB/20),base[BASE_IN*SPF:BASE_FRAMES*SPF].copy()]
 # Five-ms ramps only at the two quiet graft joins, never at picture edits.
 for i,p in enumerate(parts):
  if i:p[:240]*=np.linspace(0,1,240)
  if i<2:p[-240:]*=np.linspace(1,0,240)
 audio=np.concatenate(parts);assert len(audio)==TOTAL*SPF
 writewav(OUT/'edited.wav',audio)
 for name,at in [('join-in',BASE_OUT),('join-out',RESUME)]:writewav(OUT/f'{name}.wav',audio[(at-100)*SPF:(at+150)*SPF])
 images=boards();reader=Reader(BASE)
 boundaries=[dict(frame=BASE_OUT,label='opener-to-new-board-and-donor'),dict(frame=dm(4547),label='one-token-ring'),dict(frame=dm(4844),label='short-answer-ring'),dict(frame=dm(5180),label='long-conversation-ring'),dict(frame=dm(CUT_IN),label='board-to-arithmetic'),dict(frame=dm(CUT_OUT),label='arithmetic-to-board'),dict(frame=dm(5597),label='qualified-takeaway-ring'),dict(frame=RESUME,label='donor-to-base-audio'),dict(frame=bm(VISUAL_RESUME),label='board-to-world-demand')]
 manifest=dict(candidate=str(DEST),fps=FPS,frames=TOTAL,duration=TOTAL/FPS,source_hashes=EXPECTED,board=str(BOARD),board_sha256=sha(BOARD),protected_hashes=protected,
  approval='User: Build it. Approved plan in ../REVIEW.txt.',scope='Replace opening calculation passage and its visuals; preserve the remaining lesson. Review candidate; no installation or publication.',
  audio_timeline=[dict(source=str(BASE),start_frame=0,end_frame=BASE_OUT,output_start=0),dict(source=str(DONOR),start_frame=DONOR_IN,end_frame=DONOR_OUT,output_start=BASE_OUT,gain_db=GAIN_DB),dict(source=str(BASE),start_frame=BASE_IN,end_frame=BASE_FRAMES,output_start=RESUME)],
  visual_timeline=[dict(kind='base',output_start=0,output_end=BASE_OUT,source_start=0),dict(kind='current-board',output_start=BASE_OUT,output_end=dm(CUT_IN)),dict(kind='base-arithmetic-cutaway',output_start=dm(CUT_IN),output_end=dm(CUT_OUT),source_start=CUT_SOURCE),dict(kind='current-board',output_start=dm(CUT_OUT),output_end=bm(VISUAL_RESUME)),dict(kind='base',output_start=bm(VISUAL_RESUME),output_end=TOTAL,source_start=VISUAL_RESUME)],
  boundaries=boundaries,quiet_cuts_seconds=dict(base_out=BASE_OUT/30,base_resume=BASE_IN/30,donor_in=DONOR_IN/30,donor_out=DONOR_OUT/30),splice_ramp_ms=5,additional_pauses=0,density='compact',ring_width_720p=4,longest_new_board_run_seconds=(dm(CUT_IN)-BASE_OUT)/30,
  source_limitation='Retained, hash-locked finished v6/v14 files. Single reencode from those inputs; no pristine-roll reconstruction.',listening_performed=False)
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 log=(OUT/'encode.log').open('w')
 p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','4','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-frames:v',str(TOTAL),'-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE,stderr=log)
 try:
  for f in range(TOTAL):
   if f<BASE_OUT:im=reader.at(f)
   elif f<RESUME:
    d=DONOR_IN+f-BASE_OUT
    if CUT_IN<=d<CUT_OUT:im=reader.at(CUT_SOURCE+d-CUT_IN)
    else:
     name='none' if d<4547 else 'one' if d<4844 else 'short' if d<5180 else 'long' if d<CUT_OUT else 'none' if d<5597 else 'takeaway'
     im=images[name]
   elif f<bm(VISUAL_RESUME):im=images['none']
   else:im=reader.at(f-DELTA)
   p.stdin.write(im.tobytes())
   if f%900==899:print('Rendered',f+1,'/',TOTAL,flush=True)
 finally:p.stdin.close();reader.c.release()
 assert p.wait()==0;log.close()
 manifest['candidate_sha256']=sha(DEST);manifest['protected_unchanged']={p:sha(p)==h for p,h in protected.items()};assert all(manifest['protected_unchanged'].values())
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Built',DEST,'duration',TOTAL/30,flush=True)
if __name__=='__main__':main()
