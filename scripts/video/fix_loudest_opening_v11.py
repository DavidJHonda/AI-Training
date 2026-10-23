#!/usr/bin/env python3
"""Bring the canonical two-expert board in at 'Same field' (19.9s)."""
from pathlib import Path
import json,subprocess
import av,cv2,numpy as np
from build_remove_doubter import ROOT,FF,Boards,frames,sha
OUT=ROOT/'video-audit/loudest-voices-opening-v11-2026-10-22'
SOURCE=ROOT/'Prompts/loudest-voices-v10.mp4';DEST=ROOT/'Prompts/loudest-voices-v11.mp4'
EXPECTED='032b271c36ca0422b884cab0157c4973bc170e036f45824fd65fa002e4bbd368'
A,START,B=369,597,712

def main():
 assert sha(SOURCE)==EXPECTED;assert not DEST.exists()
 OUT.mkdir(exist_ok=True)
 original=ROOT/'Prompts/loudest-voices-v8.mp4'
 assert sha(original)=='d553d341c258f1420b8a5927f6a6cdd2652a12b1f0d6fafe5d55f66089b497a4'
 board=Boards().full();leg=OUT/'opening-leg.mp4'
 cmd=[FF,'-v','error','-n','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','30','-i','-','-an','-c:v','libx264','-threads','4','-crf','18','-preset','medium','-pix_fmt','yuv420p','-r','30','-video_track_timescale','15360',str(leg)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 for n,im in frames(original):
  if n<A:continue
  if n>=B:break
  proc.stdin.write((im if n<START else board).tobytes())
 proc.stdin.close();assert proc.wait()==0
 source=av.open(str(SOURCE));v=source.streams.video[0];audio=source.streams.audio[0]
 patch=av.open(str(leg));pv=patch.streams.video[0]
 assert pv.time_base==v.time_base
 assert pv.codec_context.extradata==v.codec_context.extradata,(pv.codec_context.extradata.hex(),v.codec_context.extradata.hex())
 packets=[];keys=[];nvideo=0;naudio=0
 for p in source.demux(v,audio):
  if p.dts is None:continue
  isvideo=p.stream.type=='video'
  if isvideo:
   f=round(float(p.pts*p.time_base)*30)
   if p.is_keyframe:keys.append(f)
   if A<=f<B:continue
   nvideo+=1
  else:naudio+=1
  packets.append((isvideo,p))
 assert A in keys and B in keys
 for p in patch.demux(pv):
  if p.dts is None:continue
  p.pts+=A*512;p.dts+=A*512;packets.append((True,p))
 packets.sort(key=lambda x:(x[1].dts*x[1].time_base,not x[0]))
 with av.open(str(DEST),'w',options={'movflags':'+faststart'}) as out:
  ov=out.add_stream_from_template(v);oa=out.add_stream_from_template(audio)
  for isvideo,p in packets:p.stream=ov if isvideo else oa;out.mux(p)
 m={'candidate':str(DEST.relative_to(ROOT)),'sha256':sha(DEST),'source':str(SOURCE.relative_to(ROOT)),'source_sha256':EXPECTED,'frames':8458,'duration':8458/30,'scope':'Visual-only opening repair: canonical board starts at 19.9s on Same field, before the three-way split.','changed_visual_frames':[START,B],'reencoded_gop_frames':[A,B],'original_source_for_retained_frames':str(original.relative_to(ROOT)),'unaffected_video_packets_copied':nvideo,'audio_packets_copied':naudio,'audio':'Every AAC packet and timestamp copied from v10; unchanged.','status':'Review candidate; not installed.'}
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(m,indent=2),flush=True)
if __name__=='__main__':main()
