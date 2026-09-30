#!/usr/bin/env python3
"""Repair only the final complete GOP region; retain all earlier v7 packets."""
import json,subprocess
import av,cv2
import build_curious_flexible_v6 as b
BASE=b.ROOT/'Prompts/curious-and-flexible-v7.mp4'
BASE_HASH='19660d45076b5af9f6c7dce3d512ef3e8579781c7f884955569f9398e70084c9'
b.OUT=b.ROOT/'video-audit/curious-and-flexible-build-2026-09-30-v8'
b.DEST=b.ROOT/'Prompts/curious-and-flexible-v8.mp4'
A=5569

def main():
 cv2.setNumThreads(2);b.OUT.mkdir(exist_ok=True)
 assert b.sha(BASE)==BASE_HASH and b.sha(b.SRC)==b.EXPECTED and not b.DEST.exists()
 leg=b.OUT/'leg-reveal.mp4'
 proc=subprocess.Popen([b.FF,'-v','error','-f','rawvideo','-pix_fmt','yuv420p','-s','1280x720','-r','30','-i','pipe:0','-an','-c:v','libx264','-profile:v','high','-level:v','3.1','-crf','16','-preset','fast','-threads','2','-pix_fmt','yuv420p','-video_track_timescale','15360',str(leg)],stdin=subprocess.PIPE)
 count=0
 with av.open(str(b.SRC)) as source:
  source.streams.video[0].codec_context.thread_count=2
  for n,f in enumerate(source.decode(video=0)):
   if n<A:continue
   if n<6073:
    im=b.diagram(f.to_ndarray(format='bgr24'),n)
    raw=av.VideoFrame.from_ndarray(im,format='bgr24').to_ndarray(format='yuv420p')
   else:raw=f.to_ndarray(format='yuv420p')
   proc.stdin.write(raw.tobytes());count+=1
 proc.stdin.close();assert proc.wait()==0 and count==b.N-A
 source=av.open(str(BASE));v=source.streams.video[0];a=source.streams.audio[0];packets=[];keys=[]
 for p in source.demux(v,a):
  if p.dts is None:continue
  isvideo=p.stream.type=='video'
  frame=round(float(p.pts*p.time_base)*30) if isvideo else None
  if isvideo and p.is_keyframe:keys.append(frame)
  if isvideo and frame>=A:continue
  packets.append((isvideo,p))
 assert A in keys
 replacement=av.open(str(leg));rv=replacement.streams.video[0]
 assert rv.time_base==v.time_base and rv.codec_context.extradata==v.codec_context.extradata,'GOP codec mismatch'
 for p in replacement.demux(rv):
  if p.dts is None:continue
  p.pts+=A*512;p.dts+=A*512;packets.append((True,p))
 packets.sort(key=lambda x:(x[1].dts*x[1].time_base,not x[0]))
 with av.open(str(b.DEST),'w',options={'movflags':'+faststart'}) as output:
  ov=output.add_stream_from_template(v);oa=output.add_stream_from_template(a)
  for isvideo,p in packets:p.stream=ov if isvideo else oa;output.mux(p)
 assert b.audio_hash(b.SRC)==b.audio_hash(b.DEST) and b.audio_hash(b.SRC,True)==b.audio_hash(b.DEST,True)
 m=json.loads((b.ROOT/'video-audit/curious-and-flexible-build-2026-09-30-v7/edit-manifest.json').read_text())
 m.update(candidate=str(b.DEST),candidate_sha256=b.sha(b.DEST),builder=str(__file__),repair_from_v7='Overlays appear only after source header has revealed. Source animation frames and all earlier v7 packets retained.',packet_base=str(BASE),packet_base_sha256=BASE_HASH,patched_gop_frames=[A,b.N],codec_extradata_identical=True)
 assert all(b.sha(p)==h for p,h in m['protected'].items())
 (b.OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('BUILT',b.DEST,flush=True)
if __name__=='__main__':main()
