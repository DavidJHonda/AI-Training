#!/usr/bin/env python3
"""Narrow repair requested by David: first banner bounds and spoken question reprise."""
from pathlib import Path
import argparse,json,subprocess,copy
import cv2,numpy as np,imageio_ffmpeg
import build_how_ai_answers_v9 as prior
from editspec_build import Reader,sha
from build_embeddings_v7 import Renderer
ROOT=prior.ROOT
OUT=ROOT/'video-audit/how-ai-answers-repair-2026-09-28-v10'
DEST=ROOT/'Prompts/how-ai-answers-v10.mp4'
INSERT=3108;DONOR_A=330;DONOR_B=391;ADDED=DONOR_B-DONOR_A
TOTAL=prior.TOTAL+ADDED
RING_START=3113

def prepare():
 prior.OUT=OUT;prior.DEST=DEST
 snap,rs,mapped,title,m=prior.prepare()
 b1=json.loads((OUT/'leg-b1.json').read_text())
 # Canonical JPG measurement, not the old outline: x40..1560, y911..999.
 # Carry the measured padding offset in both axes from the existing spec.
 ring=b1['rings'][-1];oy=ring['rect'][1]-905;ring['rect'][1]=911+oy;ring['rect'][3]=88
 rs['b1']=Renderer(b1);(OUT/'leg-b1.json').write_text(json.dumps(b1,indent=2)+'\n')
 q=copy.deepcopy(json.loads((OUT/'leg-b3.json').read_text()))
 q['beats']=[dict(label='full question reprise',frames=ADDED,**{'from':q['beats'][0]['from'],'to':q['beats'][0]['from']})]
 # Padded canvas x-offset from the complete Prediction 1 group's original ring.
 ox=q['rings'][0]['rect'][0]-80;oy=q['rings'][0]['rect'][1]-280
 q['rings']=[dict(start=RING_START-INSERT,end=ADDED,rect=[40+ox,127+oy,1520,123],color='#4f2fc4',pad=0,radius=16,label='What should I name my new dog?')]
 qr=Renderer(q);(OUT/'leg-question.json').write_text(json.dumps(q,indent=2)+'\n')
 cv2.imwrite(str(OUT/'first-banner-preview.png'),rs['b1'].at(1350-400)[0])
 cv2.imwrite(str(OUT/'question-preview.png'),qr.at(20)[0])
 m.update(based_on='how-ai-answers-v9',frames=TOTAL,duration=TOTAL/30,insert_output_frames=[INSERT,INSERT+ADDED],question_donor_source_frames=[DONOR_A,DONOR_B],question_donor_source_seconds=[DONOR_A/30,DONOR_B/30],question_ring_output_frames=[RING_START,INSERT+ADDED],added_seconds=ADDED/30,title_output_frames=[prior.TITLE_START+ADDED,prior.CUT_A+ADDED],close_output_start=prior.CUT_A+ADDED,audio='Original-source PCM plus complete opening-question donor; existing v9 cut retained. Five-ms edge fades in measured silence at all three joins. AAC 192k.',approval='David identified the first-board banner and requested the question be repeated and highlighted before the Prediction 1 explanation. Narrow repair, review only.')
 m['protected'][str(ROOT/'Prompts/how-ai-answers-v9.mp4')]=sha(ROOT/'Prompts/how-ai-answers-v9.mp4')
 m['boundaries']=sorted(set([b+(ADDED if b>=INSERT else 0) for b in m['boundaries']]+[1288,INSERT,RING_START,INSERT+ADDED]))
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 return snap,rs,qr,mapped,title,m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a review candidate'
 snap,rs,qr,mapped,title,m=prepare()
 if args.prepare_only:return
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 a=np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(snap),'-vn','-ar','48000','-ac','2','-f','f32le','pipe:1']),np.float32).reshape(-1,2)
 spans=[(0,INSERT),(DONOR_A,DONOR_B),(INSERT,prior.CUT_A),(prior.CUT_B,prior.base.TOTAL)]
 parts=[a[x*1600:y*1600].copy() for x,y in spans]
 fade=240
 for i,part in enumerate(parts):
  if i:part[:fade]*=np.linspace(0,1,fade,dtype=np.float32)[:,None]
  if i<len(parts)-1:part[-fade:]*=np.linspace(1,0,fade,dtype=np.float32)[:,None]
 pcm=np.concatenate(parts);assert len(pcm)==TOTAL*1600
 (OUT/'audio-reference.f32').write_bytes(pcm.tobytes());m['audio_source_spans_frames']=spans
 proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-f','f32le','-ar','48000','-ac','2','-i',str(OUT/'audio-reference.f32'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 donor_ids=sorted({it[1] for it in mapped[:prior.TITLE_START] if it and it[0] not in rs}|{7319})
 rd=Reader(snap);donors={f:rd.at(f).copy() for f in donor_ids};rd.c.release();rd=Reader(snap)
 for f in range(TOTAL):
  if INSERT<=f<INSERT+ADDED:im=qr.at(f-INSERT)[0]
  else:
   old=f if f<INSERT else f-ADDED
   sf=old if old<prior.CUT_A else old+prior.REMOVED
   if prior.TITLE_START<=old<prior.CUT_A:im=title
   elif prior.CUT_A<=old<prior.CUT_A+(7319-prior.CUT_B):im=donors[7319]
   else:
    item=mapped[sf]
    im=rd.at(sf) if item is None else rs[item[0]].at(item[1])[0] if item[0] in rs else donors[item[1]]
  proc.stdin.write(im.tobytes())
  if f%1000==999:print('Rendered',f+1,'/',TOTAL,flush=True)
 proc.stdin.close();assert proc.wait()==0;rd.c.release()
 assert all(sha(Path(p))==h for p,h in m['protected'].items())
 m['candidate_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
