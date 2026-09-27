from pathlib import Path
import cv2,json,subprocess,numpy as np,sys
cv2.setNumThreads(1)
r=Path('/Users/davidobrien/Developer/AI-Training');o=r/'video-audit/understand-ai-opener-repair-2026-09-27-v12';m=json.loads((o/'edit-manifest.json').read_text());video=Path(m['output']);source=Path(m['source_snapshot']);sys.path.insert(0,str(r/'scripts/video'));import imageio_ffmpeg
ff=imageio_ffmpeg.get_ffmpeg_exe()
def audio_hash(p,decoded=False):
 cmd=[ff,'-v','error','-i',str(p),'-map','0:a:0','-c:a','pcm_s16le' if decoded else 'copy','-f','hash','-hash','sha256','-']
 return subprocess.check_output(cmd,text=True).strip()
audio={'packet_source':audio_hash(source),'packet_candidate':audio_hash(video),'pcm_source':audio_hash(source,True),'pcm_candidate':audio_hash(video,True)}
assert audio['packet_source']==audio['packet_candidate'];assert audio['pcm_source']==audio['pcm_candidate']
cap=cv2.VideoCapture(str(video));src=cv2.VideoCapture(str(source));fps=cap.get(cv2.CAP_PROP_FPS);dims=[int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))];assert fps==30 and dims==[1280,720]
templates={p.stem:cv2.resize(cv2.imread(str(p)),(160,90)) for p in (o/'preview').glob('*.png')}
runs=[];n=0;err=[];close_err=[];unchanged_max=(0,0);selected={0,9,55,94,179,1733,1735,2423,2785,3011,3234,3235,3355,3474,3475,3599,3878,4173,4174,4321,4440};frames=o/'encoded-frames';frames.mkdir(exist_ok=True)
for key,(a,b) in m['board_spans_before_break'].items():
 for ring in m['boards'][key]['rings']:
  t=a+ring['start']+15
  selected.add(3490 if 3235<=t<3475 else t)
while True:
 ok,im=cap.read();ok2,base=src.read();assert ok==ok2
 if not ok:break
 small=cv2.resize(im,(160,90));ds={k:cv2.norm(small,v,cv2.NORM_L1)/small.size for k,v in templates.items()};kind=min(ds,key=ds.get);kind=kind.split('-')[0] if ds[kind]<4 else None
 if kind:
  if runs and runs[-1]['kind']==kind and runs[-1]['end_frame']==n:runs[-1]['end_frame']=n+1
  else:runs.append({'kind':kind,'start_frame':n,'end_frame':n+1})
 changed=any(a<=n<b for a,b in m['board_spans_before_break'].values())
 if not changed:
  e=cv2.norm(im,base,cv2.NORM_L1)/im.size;err.append(e)
  if e>unchanged_max[1]:unchanged_max=(n,e)
  if n>=4174:close_err.append(e)
 if n in selected:cv2.imwrite(str(frames/f'{n:04d}.png'),im)
 n+=1
cap.release();src.release();assert n==4441
expected=[('kind',0,352),('hood',1733,1958),('map',2423,3235),('map',3475,4174)]
assert [(x['kind'],x['start_frame'],x['end_frame']) for x in runs]==expected,runs
for x in runs:x['duration']=(x['end_frame']-x['start_frame'])/30
# Actual encoded settled states: measure four straight sides using color masks
# and the published ring detector's independent connected-component geometry.
from ring_stroke import side_runs
widths=[]
for key,(a,b) in m['board_spans_before_break'].items():
 spec=m['boards'][key]
 for ring in spec['rings']:
  t=a+ring['start']+15
  if 3235<=t<3475:t=3475+15
  frame=cv2.imread(str(frames/f'{t:04d}.png'))
  rgb=ring['color'].lstrip('#');col=np.array([int(rgb[i:i+2],16) for i in (4,2,0)])
  mask=(np.linalg.norm(frame.astype(np.float32)-col,axis=2)<45).astype(np.uint8)
  count,lab,stats,_=cv2.connectedComponentsWithStats(mask)
  candidates=[]
  for k in range(1,count):
   x,y,w,h,area=stats[k]
   if w>100 and h>20 and area<.45*w*h:
    stroke,sides=side_runs(lab,k,x,y,w,h);candidates.append((area,float(stroke),sides,[int(x),int(y),int(w),int(h)]))
  z=max(candidates,key=lambda q:q[0]);widths.append({'board':key,'frame':t,'color':ring['color'],'stroke':z[1],'sides':z[2],'bbox':z[3]})
  cv2.imwrite(str(frames/f'ring-{key}-{ring["start"]:04d}.png'),frame)
  # Color-distance threshold measures the solid core only, not anti-aliased coverage.
  # The independent background-relative profiles in ring-coverage.json verify width.
coverage=json.loads((o/'ring-coverage.json').read_text())
assert all(w==4 for row in coverage for w in row['half_coverage_pixels'].values())
summary={'ring_width_coverage':coverage,'frames':n,'fps':fps,'size':dims,'duration':n/fps,'audio':audio,'audio_packets_identical':True,'decoded_audio_identical':True,'measured_board_runs':runs,'ring_states':widths,'unchanged_visual_encoding_error':{'mean_absolute_pixel_error':float(np.mean(err)),'max_frame_and_error':unchanged_max,'close_mean_error':float(np.mean(close_err))},'checks_not_done':['Real-time end-to-end listening/playback','Mobile playback','Manual every-frame scrutiny outside changed seams']}
(o/'verification.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2),flush=True)
