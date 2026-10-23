#!/usr/bin/env python3
"""Three-tactic narrow repair. Preserve the first 4,712 video packets exactly."""
from pathlib import Path
import hashlib,json,subprocess,sys,wave
import av,cv2,numpy as np,imageio_ffmpeg
sys.path.insert(0,str(Path(__file__).resolve().parent))
import ken_burns_path as kb
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/flattery-trap-three-tactics-v11-2026-10-23'
SRC=ROOT/'Prompts/flattery-trap-v10.mp4'
DEST=ROOT/'Prompts/flattery-trap-v11.mp4'
BOARD=ROOT/'course-assets/flattery-trap/flattery-trap-five-moves.jpg'
SOURCE_HASH='db9c8139d51ab6e00c30315346f6078822496c83a97a738737454c802657db50'
FPS=30; PREFIX=4712; SR=48000; FF=imageio_ffmpeg.get_ffmpeg_exe()
# All endpoints are in measured source silences; end frames are exclusive.
RANGES=[(0,4826,'opening'),(4938,6975,'three tactics'),(7831,8035,'concrete standard'),
        (8558,8770,'save the instruction'),(8382,8557,'instruction example'),(9032,9431,'takeaway and close')]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
FULL=[1056,594,2112]
ROW1=[1056,472.5,1680]; ROW2=[1056,470,1680]; ROW3=[1056,700,1680]; TIP=[1056,715.5,1680]
# Native JPG coordinates, complete row bounds inset from the shared stage.
RECTS={'one':[56,143,1544,301],'two':[56,333,1544,520],
       'three':[56,552,1544,739],'tip':[56,771,1544,917], 'takeaway':[40,973,1560,1061]}

def lerp(a,b,t):
 t=kb.smoothstep(max(0,min(1,t)));return [x+(y-x)*t for x,y in zip(a,b)]

class Board:
 def __init__(self):
  im=cv2.imread(str(BOARD));assert im.shape[:2]==(1101,1600)
  self.canvas=np.full((1188,2112,3),im[4,4],np.uint8)
  self.canvas[43:1144,256:1856]=im
  cv2.imwrite(str(OUT/'canvas-three-tactics.png'),self.canvas)
  self.big=cv2.resize(self.canvas,None,fx=2,fy=2,interpolation=cv2.INTER_LANCZOS4)
  self.cache={}
 def draw(self,camera,target):
  key=tuple(camera)+(target,)
  if key in self.cache:return self.cache[key].copy()
  x,y,w,h=kb.window(*camera,1280/720,2112,1188)
  X,Y,CW,CH=[round(a*2) for a in (x,y,w,h)]
  frame=cv2.resize(self.big[Y:Y+CH,X:X+CW],(1280,720),interpolation=cv2.INTER_AREA)
  if target:
   x0,y0,x1,y1=RECTS[target];scale=1280/w;half=kb.ring_px(720)/2
   box=[(x0+256-x)*scale-half,(y0+43-y)*scale-half,
        (x1+256-x)*scale+half,(y1+43-y)*scale+half]
   assert box[0]>=0 and box[1]>=0 and box[2]<1280 and box[3]<720,(target,box)
   color='#6e51ff' if target=='takeaway' else '#0e8f86'
   kb.draw_ring(frame,*box,kb.hex_bgr(color),14*scale+half,kb.ring_px(720))
  self.cache[key]=frame.copy();return frame

def picture(f,part,local,board,native):
 if part==0:return native[f], 'source'
 if part==1:
  if f<5415:
   camera=FULL if f<4998 else lerp(FULL,ROW1,(f-4998)/30)
   return board.draw(camera,'one' if f>=4973 else None),'board-one'
  if f<5558:return native[f],'neutral-input-drawing'
  if f<6036:return board.draw(ROW2,'two' if f>=5573 else None),'board-two'
  # Reuse the existing concrete-criteria illustration under the specific-targets sentence.
  if f<6150:return native[7831+f-6036],'specific-targets-drawing'
  if f<6746:
   return board.draw(ROW3,'three' if f>=6155 else None),'board-three'
  # Preserve the complete rubric animation, slowed 1.46x to cover the whole caveat.
  donor=6818+min(156,round((f-6746)*156/(6975-6746-1)))
  return native[donor],'work-vs-rubric-drawing'
 if part==2:return native[f],'concrete-standard-drawing'
 if part in (3,4):
  tiplocal=local if part==3 else 212+local
  camera=FULL if tiplocal<60 else lerp(FULL,TIP,(tiplocal-60)/30)
  return board.draw(camera,'tip' if tiplocal>=60 else None),'board-tip'
 if f<9138:return board.draw(FULL,'takeaway' if f>=9039 else None),'board-takeaway'
 return native[f],'standard-close'

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 assert not DEST.exists(),'Never overwrite a review candidate'
 assert sha(SRC)==SOURCE_HASH
 asset_hash=sha(BOARD)
 native={};cap=cv2.VideoCapture(str(SRC));n=0
 while True:
  ok,im=cap.read()
  if not ok:break
  if n>=PREFIX and (n<4826 or 5415<=n<5558 or 6818<=n<6975 or 7831<=n<8035 or n>=9138):native[n]=im
  n+=1
 assert n==9431;cap.release()
 board=Board();tail=OUT/'tail-picture.mp4'
 cmd=[FF,'-v','error','-y','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720',
      '-framerate','30','-i','-','-an','-c:v','libx264','-threads','2','-crf','16','-preset','fast',
      '-pix_fmt','yuv420p','-profile:v','high','-level:v','3.1','-video_track_timescale','15360',str(tail)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 cursor=0;boundaries=[];runs=[];last=None;segments=[];previewed=set()
 for part,(a,b,label) in enumerate(RANGES):
  segments.append({'source_frames':[a,b],'output_frames':[cursor,cursor+b-a],'label':label})
  if cursor:boundaries.append({'frame':cursor,'label':'audio-splice-'+label.replace(' ','-')})
  for f in range(a,b):
   if cursor<PREFIX:cursor+=1;continue
   frame,kind=picture(f,part,f-a,board,native)
   if kind!=last:
    if last is not None:boundaries.append({'frame':cursor,'label':kind})
    runs.append({'kind':kind,'start':cursor,'end':cursor+1});last=kind
   else:runs[-1]['end']=cursor+1
   if kind not in previewed and (not kind.startswith('board') or (kind=='board-one' and f>=5030) or (kind=='board-tip' and part==3 and f-a>=91) or kind in ['board-two','board-three','board-takeaway']):
    cv2.imwrite(str(OUT/f'preview-{kind}.jpg'),frame);previewed.add(kind)
   if cursor in [4826,4826+60,7067,7067+60,7454]:cv2.imwrite(str(OUT/f'preview-frame-{cursor}.jpg'),frame)
   proc.stdin.write(frame.tobytes());cursor+=1
  print(label,'output end',cursor,flush=True)
 proc.stdin.close();assert proc.wait()==0
 # Only the editorial joins receive a 5ms fade, wholly inside measured silence.
 raw=subprocess.check_output([FF,'-v','error','-i',str(SRC),'-map','0:a:0','-f','f32le','-acodec','pcm_f32le','-ac','1','-ar',str(SR),'-'])
 samples=np.frombuffer(raw,np.float32)[:9431*1600];chunks=[]
 for i,(a,b,_) in enumerate(RANGES):
  chunk=samples[a*1600:b*1600].copy();fade=np.linspace(0,1,240)
  if i:chunk[:240]*=fade
  if i<len(RANGES)-1:chunk[-240:]*=fade[::-1]
  chunks.append(chunk)
 pcm=np.concatenate(chunks);assert len(pcm)==cursor*1600
 wav=OUT/'audio-edited.wav'
 with wave.open(str(wav),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
  w.writeframes(np.rint(np.clip(pcm,-1,1)*32767).astype('<i2').tobytes())
 aac=OUT/'audio-edited.m4a'
 subprocess.run([FF,'-v','error','-y','-i',str(wav),'-c:a','aac','-b:a','192k',str(aac)],check=True)
 # Prefix H.264 packets are copied exactly; only the changed tail is re-encoded.
 source=av.open(str(SRC));v=source.streams.video[0]
 tailc=av.open(str(tail));tv=tailc.streams.video[0]
 assert tv.codec_context.extradata==v.codec_context.extradata,'Codec configurations must match'
 assert tv.frames==cursor-PREFIX,(tv.frames,cursor-PREFIX)
 audioc=av.open(str(aac));ta=audioc.streams.audio[0];packets=[]
 for p in source.demux(v):
  if p.dts is not None and p.pts< PREFIX*512:packets.append(('video',p))
 for p in tailc.demux(tv):
  if p.dts is not None:p.pts+=PREFIX*512;p.dts+=PREFIX*512;packets.append(('video',p))
 for p in audioc.demux(ta):
  if p.dts is not None:packets.append(('audio',p))
 packets.sort(key=lambda item:item[1].dts*item[1].time_base)
 with av.open(str(DEST),'w',options={'movflags':'+faststart'}) as c:
  ov=c.add_stream_from_template(v);oa=c.add_stream_from_template(ta)
  for kind,p in packets:p.stream=ov if kind=='video' else oa;c.mux(p)
 for c in [source,tailc,audioc]:c.close()
 manifest={'source':str(SRC),'source_sha256':SOURCE_HASH,'candidate':str(DEST),'candidate_sha256':sha(DEST),
  'board':str(BOARD),'board_sha256':asset_hash,'board_dimensions':[1600,1101],
  'canvas_dimensions':[2112,1188],'board_offset':[256,43],'density':'dense','ring_px':4,
  'rectangles':RECTS,'frames':cursor,'fps':30,'duration_seconds':cursor/30,'copied_prefix_frames':PREFIX,
  'segments':segments,'boundaries':sorted({(r['frame'],r['label']) for r in boundaries}),
  'visual_runs':runs,'longest_changed_board_run_seconds':max((r['end']-r['start'])/30 for r in runs if r['kind'].startswith('board')),
  'added_pause_seconds':0,'direct_listening_performed':False,
  'scope':'Three tactics and brief saved-instruction tip. Original raw rolls unavailable; stable finished v10 source. No shipping or publication.'}
 assert sha(SRC)==SOURCE_HASH and sha(BOARD)==asset_hash
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({k:manifest[k] for k in ['candidate','frames','duration_seconds','longest_changed_board_run_seconds']},indent=2))
if __name__=='__main__':main()
