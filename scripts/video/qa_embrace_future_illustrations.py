#!/usr/bin/env python3
import argparse,json,hashlib,itertools,subprocess,sys
import av,cv2,numpy as np
from build_embrace_future_illustrations import ROOT,OUT,FF,SOURCES,paths,sha,render
cv2.setNumThreads(1)
def packets(path,kind):
 with av.open(str(path)) as c:
  stream=next(s for s in c.streams if s.type==kind)
  return [(p.pts,p.dts,p.duration,str(p.time_base),hashlib.sha256(bytes(p)).hexdigest()) for p in c.demux(stream) if p.dts is not None]
def frames(path):
 with av.open(str(path)) as c:
  c.streams.video[0].codec_context.thread_count=1
  for f in c.decode(video=0):yield f

def qa(slug):
 cfg=SOURCES[slug];src,dst=paths(slug,cfg);evidence=OUT/slug/'encoded';evidence.mkdir(parents=True,exist_ok=True)
 aa,ab=packets(src,'audio'),packets(dst,'audio');assert aa==ab,'Audio packets/timestamps differ'
 def untouched(rows):return [p for p in rows if not cfg['encode_start']<=p[0]/512<cfg['encode_end']]
 assert untouched(packets(src,'video'))==untouched(packets(dst,'video')),'Untouched video packets differ'
 for p in [src,dst]:
  with av.open(str(p)) as c:
   v=c.streams.video[0];assert v.average_rate==30 and v.width==1280 and v.height==720
 boundaries={cfg['start']:'insert-in',cfg['end']:'insert-out'}
 boundaries.update({f:f'state-{i+1}' for i,f in enumerate(cfg['changes'])})
 if cfg['end']!=cfg['encode_end']:boundaries[cfg['encode_end']]='copied-video-resumes'
 selected={0,cfg['frames']-1,cfg['start']+45,cfg['end']-20}
 selected.update(f+d for f in boundaries for d in [-1,0,1])
 exact=0;new=0;preserved_reencoded=0;min_render_psnr=100;min_preserved_psnr=100
 for n,pair in enumerate(itertools.zip_longest(frames(src),frames(dst))):
  f,g=pair;assert f is not None and g is not None
  a=f.to_ndarray(format='yuv420p');b=g.to_ndarray(format='yuv420p')
  if not cfg['encode_start']<=n<cfg['encode_end']:
   assert np.array_equal(a,b),f'Unchanged frame differs at {n}';exact+=1
  elif not cfg['start']<=n<cfg['end']:
   score=cv2.PSNR(a,b);min_preserved_psnr=min(score,min_preserved_psnr);preserved_reencoded+=1
   assert score>38,(n,score,'Preserved board differs excessively')
  else:
   score=cv2.PSNR(render(cfg,n),g.to_ndarray(format='rgb24'));min_render_psnr=min(score,min_render_psnr);new+=1
   assert score>32,(n,score,'Wrong scene/state')
  if n in selected:cv2.imwrite(str(evidence/f'{n:05}.jpg'),g.to_ndarray(format='bgr24'),[cv2.IMWRITE_JPEG_QUALITY,96])
 assert n+1==cfg['frames']
 audio=[]
 for path in [src,dst]:
  raw=subprocess.check_output([FF,'-v','error','-i',str(path),'-map','0:a:0','-f','s16le','-'])
  audio.append(dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
 assert audio[0]==audio[1]
 cmd=[sys.executable,'-c','import cv2,runpy;cv2.setNumThreads(1);runpy.run_path("scripts/video/transition_guard.py",run_name="__main__")',str(dst),'--outdir',str(OUT/slug/'transitions')]
 for f,label in sorted(boundaries.items()):cmd+=['--boundary',f'{f}:{label}']
 result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);(OUT/slug/'transition-command.log').write_text(result.stdout+result.stderr)
 assert result.returncode==0,result.stdout+result.stderr
 manifest=json.loads((OUT/f'{slug}-manifest.json').read_text());assert all(sha(p)==h for p,h in manifest['protected_hashes'].items())
 report=dict(slug=slug,candidate=str(dst),candidate_sha256=sha(dst),frames=n+1,duration=(n+1)/30,fps=30,changed_frames=new,untouched_frames_pixel_identical=exact,preserved_reencoded_frames=preserved_reencoded,preserved_reencoded_min_psnr_db=min_preserved_psnr if preserved_reencoded else None,changed_render_min_psnr_db=min_render_psnr,unchanged_video_packets_identical=True,audio_packets_identical=True,audio_packet_count=len(aa),decoded_audio=audio[0],transition_guard_passed=True,boundaries=boundaries,protected_assets_unchanged=True,direct_listening_performed=False,visual_strip_review_completed=False)
 (OUT/slug/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('slug',choices=list(SOURCES));args=p.parse_args();qa(args.slug)
