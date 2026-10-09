#!/usr/bin/env python3
"""Narrow update from the approved live guided demonstration; source audio copied."""
from pathlib import Path
import hashlib,json,subprocess
import cv2,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/embeddings-v12.mp4'
DEST=ROOT/'Prompts/embeddings-v13.mp4'
OUT=ROOT/'video-audit/embeddings-guided-2026-10-09'
EXPECTED='b6fcc8211b27ea97ab25b6dedc94eba7c692bb94ff773071aa2e7aa730e19806'
FRAMES=7997
# Half-open source/output spans. Existing cutaways retain their precise cuts.
STATES=[
 (551,1039,'student-id'),
 (1930,2024,'headings'),(2024,2098,'coke'),
 (2098,2138,'coke-0'),(2138,2170,'coke-1'),(2170,2207,'coke-2'),
 (2207,2239,'coke-3'),(2239,2283,'coke-4'),(2283,2371,'coke-5'),
 (2371,2457,'coffee'),(2457,2589,'positions'),
 (2877,2934,'two'),(2934,2987,'vector'),(2987,3101,'dimension'),(3101,3195,'value'),
 (3195,3306,'reorder'),(3306,3355,'pepsi'),(3355,3489,'pepsi-six'),
 (3684,3729,'match'),(3729,3893,'citrus-column'),
 (3893,3955,'citrus-pepsi'),(3955,3999,'citrus-coke'),(3999,4026,'citrus-coffee'),
 (4026,4116,'complete')]
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()
def changed(i):return any(a<=i<z for a,z,_ in STATES)
def main():
 assert sha(SRC)==EXPECTED
 assert not DEST.exists(),'Never overwrite a review candidate'
 images={name:cv2.imread(str(OUT/'captures'/f'{name}.png')) for _,_,name in STATES}
 assert all(im is not None and im.shape==(720,1280,3) for im in images.values())
 protected={str(p):sha(p) for p in [SRC,ROOT/'course-assets/embeddings/embeddings.mp4',ROOT/'index.html',ROOT/'lessons/embeddings.md']}
 c=cv2.VideoCapture(str(SRC));assert c.get(cv2.CAP_PROP_FPS)==30
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 log=open(OUT/'encode.log','w')
 proc=subprocess.Popen([ff,'-hide_banner','-loglevel','warning','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE,stderr=log)
 n=0
 try:
  while True:
   ok,im=c.read()
   if not ok:break
   for a,z,name in STATES:
    if a<=n<z:im=images[name];break
   proc.stdin.write(im.tobytes());n+=1
   if n%1500==0:print('Rendered',n,'frames',flush=True)
 finally:
  c.release();proc.stdin.close()
 assert proc.wait()==0;log.close();assert n==FRAMES
 assert all(sha(Path(p))==h for p,h in protected.items())
 m=dict(source=str(SRC),source_sha256=EXPECTED,candidate=str(DEST),candidate_sha256=sha(DEST),frames=n,fps=30,duration=n/30,
  scope='Approved lesson table and banner-free student-ID visual; narration and timing unchanged. Review candidate only.',
  states=[dict(start=a,end=z,name=name,asset=str(OUT/'captures'/f'{name}.png')) for a,z,name in STATES],
  boundaries=sorted({v for a,z,_ in STATES for v in (a,z)}),
  protected=protected,capture_manifest=str(OUT/'capture-manifest.json'),
  audio='Source AAC copied unchanged; no cuts, synthesis, cleanup, or pauses.',
  source_limitation='Finished v12 source reencoded once. Original raw rolls are absent.',
  preserved_supporting_spans=[[1475,1930],[2589,2877],[3489,3684],[4116,4303]],
  longest_changed_table_run_seconds=(2589-1930)/30,
  listening='No audio edits. Continuous listening of the full candidate not yet performed.')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('Built',DEST,flush=True)
if __name__=='__main__':main()
