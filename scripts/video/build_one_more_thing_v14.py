#!/usr/bin/env python3
"""Two owner-requested cuts in v13, rebuilt from its pristine picture sources."""
from pathlib import Path
import json,subprocess,sys
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import sha,readwav,writewav
from build_one_more_thing_v13 import Assembly,SOURCES,HASHES
from build_embeddings_v7 import Renderer
ROOT=Path(__file__).resolve().parents[2]
OLD=ROOT/'video-audit/one-more-thing-build-2026-09-28-v13'
OUT=ROOT/'video-audit/one-more-thing-repair-2026-09-29-v14'
DEST=ROOT/'Prompts/one-more-thing-v14.mp4'
SOURCE=ROOT/'Prompts/one-more-thing-v13.mp4'
EXPECTED='b85a6dd6161f8921c695950320236f0597e355961f42fbd37093bca8a992aff0'
CUTS=[(3190,3205),(4284,4379)]
KEEP=[(0,3190),(3205,4284),(4379,6237)]
def mapping(f):return f-sum(z-a for a,z in CUTS if z<=f)
def main():
 assert not DEST.exists(),'Never overwrite a review candidate'
 assert sha(SOURCE)==EXPECTED
 old=json.loads((OLD/'edit-manifest.json').read_text());assert old['render_sha256']==EXPECTED
 for i,p in SOURCES.items():assert sha(p)==HASHES[i]
 OUT.mkdir(exist_ok=True)
 protected={str(p):sha(p) for p in [SOURCE,*SOURCES.values(),ROOT/'course-assets/one-more-thing/one-more-thing.mp4',ROOT/'lessons/one-more-thing.md',*sorted((ROOT/'course-assets/one-more-thing').glob('*.jpg'))]}
 audio=readwav(OLD/'edited.wav');parts=[audio[a*1600:z*1600].copy() for a,z in KEEP];fade=240
 for i,p in enumerate(parts):
  if i:p[:fade]*=np.linspace(0,1,fade)
  if i<len(parts)-1:p[-fade:]*=np.linspace(1,0,fade)
 audio=np.concatenate(parts);frames=[f for a,z in KEEP for f in range(a,z)];assert len(audio)==len(frames)*1600
 writewav(OUT/'edited.wav',audio)
 for ix,(a,z) in enumerate(CUTS):
  at=mapping(a);writewav(OUT/f'after-cut-{ix+1}.wav',audio[(at-100)*1600:(at+160)*1600])
 asm=Assembly();asm.spans=old['visual_timeline'];asm.close=cv2.imread(str(OLD/'close.png'));asm.still=cv2.imread(str(OLD/'donor-scale-clean.png'))
 assert sha(OLD/'donor-scale-clean.png')==old['scale_donor']['clean_snapshot_sha256']
 for row in asm.spans:
  if row['kind']=='board':asm.renderers[row['key']]=Renderer(json.loads(Path(row['spec']).read_text()))
 boundaries=sorted(set([mapping(f) for f in old['boundaries'] if not any(a<=f<z for a,z in CUTS)]+[mapping(a) for a,z in CUTS]))
 m=dict(candidate=str(DEST),parent=str(SOURCE),parent_sha256=EXPECTED,frames=len(frames),fps=30,duration=len(frames)/30,cuts_parent_frames=CUTS,keep_parent_frames=KEEP,new_joins=[mapping(a) for a,z in CUTS],boundaries=boundaries,protected_hashes=protected,scope='Narrow repair: remove stray Up before Spot sentence and redundant When you use AI, these weights stay fixed sentence. Preserve all other narration and visual treatment. No publication.',picture_source='Pristine raw rolls plus v13 canonical board canvases and hash-bound donor still; no generation added to v13 encoded picture.',audio_source=str(OLD/'edited.wav'),audio_source_sha256=sha(OLD/'edited.wav'),splice_ramp_ms=5,listening_performed=False,close_start_frame=mapping(old['close']['start_frame']))
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 for f,orig in enumerate(frames):
  p.stdin.write(asm.frame(orig).tobytes())
  if f%900==899:print('Rendered',f+1,'of',len(frames),flush=True)
 p.stdin.close();assert p.wait()==0;asm.release();m['render_sha256']=sha(DEST)
 m['protected_files_unchanged']={p:sha(p)==h for p,h in protected.items()};assert all(m['protected_files_unchanged'].values())
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
