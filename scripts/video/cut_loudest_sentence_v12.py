#!/usr/bin/env python3
"""Remove the redundant highest-levels sentence; preserve untouched video packets."""
import subprocess,json,hashlib,sys
from pathlib import Path
import av, numpy as np,cv2
from build_remove_doubter import ROOT,FF,Boards,pcm,sha
OUT=ROOT/'video-audit/loudest-voices-cut-v12-2026-10-22'
SOURCE=ROOT/'Prompts/loudest-voices-v11.mp4';DEST=ROOT/'Prompts/loudest-voices-v12.mp4'
A,CUT0,CUT1,B=597,708,864,873
SHIFT=CUT1-CUT0

def main():
 assert sha(SOURCE)=='1e420ab82ed3bed141653688d78ed124f9b1bd407d816e4134415d77b96731ff'
 assert not DEST.exists()
 OUT.mkdir(exist_ok=True)
 wav=ROOT/'video-audit/remove-doubter-2026-10-22/loudest-voices-v10-audio.wav'
 # Use the existing pre-AAC assembly rather than encoding an already compressed voice again.
 orig=pcm(wav);current=pcm(SOURCE)[:len(orig)]
 corr=float(np.corrcoef(orig.ravel(),current.ravel())[0,1]);assert corr>.995
 audio=OUT/'edited-audio.m4a'
 filt=f'[0:a]atrim=end_sample={CUT0*1600},asetpts=PTS-STARTPTS,afade=t=out:st={CUT0/30-.005}:d=0.005[a];[0:a]atrim=start_sample={CUT1*1600},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.005[b];[a][b]concat=n=2:v=0:a=1[out]'
 subprocess.run([FF,'-v','error','-n','-i',str(wav),'-filter_complex',filt,'-map','[out]','-c:a','aac','-b:a','192k',str(audio)],check=True)
 board=Boards().full();leg=OUT/'board-leg.mp4';count=B-A-SHIFT
 proc=subprocess.Popen([FF,'-v','error','-n','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','30','-i','-','-an','-c:v','libx264','-threads','4','-crf','18','-preset','medium','-pix_fmt','yuv420p','-r','30','-video_track_timescale','15360',str(leg)],stdin=subprocess.PIPE)
 for _ in range(count):proc.stdin.write(board.tobytes())
 proc.stdin.close();assert proc.wait()==0
 source=av.open(str(SOURCE));v=source.streams.video[0]
 patch=av.open(str(leg));pv=patch.streams.video[0]
 assert pv.time_base==v.time_base and pv.codec_context.extradata==v.codec_context.extradata
 sound=av.open(str(audio));a=sound.streams.audio[0]
 packets=[];keys=[];retained=0
 for p in source.demux(v):
  if p.dts is None:continue
  f=round(p.pts/512)
  if p.is_keyframe:keys.append(f)
  if A<=f<B:continue
  if f>=B:p.pts-=SHIFT*512;p.dts-=SHIFT*512
  packets.append((True,p));retained+=1
 assert A in keys and B in keys
 for p in patch.demux(pv):
  if p.dts is None:continue
  p.pts+=A*512;p.dts+=A*512;packets.append((True,p))
 for p in sound.demux(a):
  if p.dts is not None:packets.append((False,p))
 packets.sort(key=lambda x:(x[1].dts*x[1].time_base,not x[0]))
 with av.open(str(DEST),'w',options={'movflags':'+faststart'}) as dest:
  ov=dest.add_stream_from_template(v);oa=dest.add_stream_from_template(a)
  for isvideo,p in packets:p.stream=ov if isvideo else oa;dest.mux(p)
 m={'candidate':str(DEST.relative_to(ROOT)),'sha256':sha(DEST),'source':str(SOURCE.relative_to(ROOT)),'source_sha256':sha(SOURCE),'cut_source_frames':[CUT0,CUT1],'cut_source_seconds':[CUT0/30,CUT1/30],'removed_seconds':SHIFT/30,'frames':8458-SHIFT,'duration':(8458-SHIFT)/30,'fps':30,'audio_source':str(wav.relative_to(ROOT)),'audio_source_sha256':sha(wav),'audio_source_correlation_to_v11':corr,'retained_video_packets':retained,'rendered_board_frames':count,'boundaries':[A,CUT0,B-SHIFT],'scope':'Remove Even at the highest levels, the experts themselves do not share a unified vision. No added silence; 5 ms fades in quiet handles. Original board and all other source video packets retained.','status':'Review candidate; not installed.'}
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(m,indent=2),flush=True)
if __name__=='__main__':main()
