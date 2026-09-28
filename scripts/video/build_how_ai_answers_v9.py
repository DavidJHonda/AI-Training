#!/usr/bin/env python3
"""Approved narrow repair: banner fit and abbreviated Inference ending. Review only."""
from pathlib import Path
import sys,json,subprocess,hashlib,wave,argparse
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
import build_how_ai_answers_v8 as base
from editspec_build import Reader,sha
from build_embeddings_v7 import Renderer
ROOT=base.ROOT
OUT=ROOT/'video-audit/how-ai-answers-repair-2026-09-28-v9'
DEST=ROOT/'Prompts/how-ai-answers-v9.mp4'
CUT_A=6221;CUT_B=7309;REMOVED=CUT_B-CUT_A;TOTAL=base.TOTAL-REMOVED
TITLE_START=6117

def prepare():
 OUT.mkdir(exist_ok=True)
 original_out=ROOT/'video-audit/how-ai-answers-repair-2026-09-28-v8'
 snap=json.loads((original_out/'source-snapshot.json').read_text())
 (OUT/'source-snapshot.json').write_text(json.dumps(snap))
 base.OUT=OUT;base.DEST=DEST
 snap,boards,specs,rs,mapped,reuse=base.setup()
 # Measured canonical yellow banner edges: x40..1560, y725..813.
 ox,oy=boards['b2']['canvas_offset']
 specs['b2']['rings'][-1]['rect']=[40+ox,725+oy,1520,88]
 rs['b2']=Renderer(specs['b2'])
 (OUT/'leg-b2.json').write_text(json.dumps(specs['b2'],indent=2)+'\n')
 rd=Reader(snap);donor=rd.at(5865).copy();rd.c.release()
 # A title overlay on the source drawing, not a replacement course board.
 # Use source paper as the stage and preserve the existing five token chips.
 paper=donor[390:710,0:1280].copy()
 canvas=cv2.resize(paper,(1280,720),interpolation=cv2.INTER_LINEAR)
 row=donor[125:235,145:902].copy()
 canvas[310:420,261:1018]=row
 im=Image.fromarray(cv2.cvtColor(canvas,cv2.COLOR_BGR2RGB))
 font=ImageFont.truetype(str(ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'),52)
 try:font.set_variation_by_axes([700])
 except Exception:pass
 d=ImageDraw.Draw(im);d.text((640,200),'Inference',font=font,fill='#202929',anchor='mt')
 title=cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
 cv2.imwrite(str(OUT/'inference-title.png'),title)
 fixed=rs['b2'].at(2400-base.SPANS['b2'][0])[0]
 cv2.imwrite(str(OUT/'banner-preview.png'),fixed)
 protected={str(p):sha(p) for p in [base.SOURCE,ROOT/'Prompts/how-ai-answers-v8.mp4',ROOT/'index.html',ROOT/'lessons/how-ai-answers.md',*sorted((ROOT/'course-assets/how-ai-answers').glob('*.jpg'))]}
 boundaries=[400,1472,1620,1740,2252,2517,2649,2819,3106,3771,4017,5008,5248,5518,TITLE_START,CUT_A]
 m=dict(source=str(snap),source_sha256=sha(snap),based_on='how-ai-answers-v8',candidate=str(DEST),fps=30,frames=TOTAL,duration=TOTAL/30,cut_source_frames=[CUT_A,CUT_B],cut_source_seconds=[CUT_A/30,CUT_B/30],removed_seconds=REMOVED/30,title_output_frames=[TITLE_START,CUT_A],close_output_start=CUT_A,boundaries=boundaries,protected=protected,approval='Build approved after exact repair proposal: correct banner, retain inference naming sentence, cut repeated walkthrough, retain close. Review only.',audio='Source PCM spans concatenated at measured silence; 5 ms edge fades inside silence at join; AAC 192k. No added pause.',listening_performed=False)
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 return snap,rs,mapped,title,m

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
 assert not DEST.exists(),'Never overwrite a review candidate'
 snap,rs,mapped,title,m=prepare()
 if args.prepare_only:return
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 raw=subprocess.check_output([ff,'-v','error','-i',str(snap),'-vn','-ar','48000','-ac','2','-f','f32le','pipe:1'])
 a=np.frombuffer(raw,np.float32).reshape(-1,2)
 aa=CUT_A*1600;bb=CUT_B*1600
 pcm=np.concatenate([a[:aa],a[bb:base.TOTAL*1600]]).copy()
 assert len(pcm)==TOTAL*1600
 n=240;pcm[aa-n:aa]*=np.linspace(1,0,n,dtype=np.float32)[:,None];pcm[aa:aa+n]*=np.linspace(0,1,n,dtype=np.float32)[:,None]
 (OUT/'audio-reference.f32').write_bytes(pcm.tobytes())
 proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-f','f32le','-ar','48000','-ac','2','-i',str(OUT/'audio-reference.f32'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 donor_ids=sorted({it[1] for it in mapped[:TITLE_START] if it and it[0] not in rs}|{7319})
 rd=Reader(snap);donors={f:rd.at(f).copy() for f in donor_ids};rd.c.release();rd=Reader(snap)
 for f in range(TOTAL):
  sf=f if f<CUT_A else f+REMOVED
  if TITLE_START<=f<CUT_A:im=title
  elif CUT_A<=f<CUT_A+(7319-CUT_B):im=donors[7319]
  else:
   item=mapped[sf]
   im=rd.at(sf) if item is None else rs[item[0]].at(item[1])[0] if item[0] in rs else donors[item[1]]
  proc.stdin.write(im.tobytes())
  if f%1000==999:print('Rendered',f+1,'/',TOTAL,flush=True)
 proc.stdin.close();assert proc.wait()==0;rd.c.release()
 assert all(sha(Path(p))==h for p,h in m['protected'].items())
 m['candidate_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
