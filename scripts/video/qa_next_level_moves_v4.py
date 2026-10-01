#!/usr/bin/env python3
"""Check two-board revision against v3 and inspect camera and splice states."""
import json,sys,runpy
import av,cv2,numpy as np
import build_next_level_moves_v4 as v
import build_next_level_moves_v3 as b
import next_level_moves_zoom as z

def main():
 cv2.setNumThreads(2);out=v.OUT/'encoded-qa';out.mkdir(exist_ok=True)
 boards={k:z.Board(k) for k in z.SPANS}
 wants={n for f in v.BOUNDARIES for n in [f-1,f,f+15]}|{v.TOTAL-1}
 for board in boards.values():
  for r in board.rings:wants|={board.start+r['start'],board.start+r['start']+30}
  for a,e,_,_ in board.moves:wants.add(board.start+(a+e)//2)
 err=[];un=[];modified=[];tiles=[];n=0
 with av.open(str(v.ROOT/'Prompts/next-level-moves-v3.mp4')) as a,av.open(str(v.DEST)) as c:
  for x in [a,c]:x.streams.video[0].codec_context.thread_count=2
  ai=iter(a.decode(video=0));ci=iter(c.decode(video=0))
  while True:
   x=next(ai,None);f=next(ci,None);assert (x is None)==(f is None)
   if x is None:break
   board=next((key for key,(start,end) in z.SPANS.items() if start<=n<end),None)
   cutaway=any(start<=n<end for start,end in b.SPANS.values())
   if not board or cutaway:
    old=x.to_ndarray(format='yuv420p')[::4,::4].astype(np.int16);new=f.to_ndarray(format='yuv420p')[::4,::4].astype(np.int16)
    delta=float(np.abs(new-old).mean());un.append(delta)
    if delta>2.5:err.append(dict(frame=n,mae=delta,type='preserved'))
   elif n in wants or n%30==0:
    expected=av.VideoFrame.from_ndarray(boards[board].render(n),format='bgr24').to_ndarray(format='yuv420p').astype(np.int16)
    actual=f.to_ndarray(format='yuv420p').astype(np.int16);delta=float(np.abs(actual-expected).mean());modified.append(dict(frame=n,board=board,mae=delta))
    if delta>2.5:err.append(dict(frame=n,mae=delta,type='new-board'))
   if n in wants:
    frame=f.to_ndarray(format='bgr24');cv2.imwrite(str(out/f'{n:06d}.jpg'),frame)
    tile=cv2.resize(frame,(426,240));cv2.putText(tile,f'{n/30:.2f}s / f{n}',(8,21),cv2.FONT_HERSHEY_SIMPLEX,.55,(0,0,200),2);tiles.append(tile)
   n+=1
   if n%2500==0:print(f'Checked {n}/{v.TOTAL}',flush=True)
 assert n==v.TOTAL
 for i in range(0,len(tiles),12):
  part=tiles[i:i+12]
  while len(part)%3:part.append(np.full_like(part[0],255))
  cv2.imwrite(str(out/f'sheet-{i//12+1}.jpg'),cv2.vconcat([cv2.hconcat(part[j:j+3]) for j in range(0,len(part),3)]))
 result=dict(frames=n,duration=n/30,preserved_frames_compared=len(un),preserved_mean_yuv_error=float(np.mean(un)),preserved_max_yuv_error=float(max(un)),changed_board_samples=modified,errors=err,audio_packets_identical=b.audio_hash(v.SOURCE)==b.audio_hash(v.DEST),decoded_audio_identical=b.audio_hash(v.SOURCE,True)==b.audio_hash(v.DEST,True),source_unchanged=b.sha(v.SOURCE)==b.EXPECTED,candidate_sha256=b.sha(v.DEST))
 (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:w for k,w in result.items() if k!='changed_board_samples'},indent=2),flush=True)
 assert not err and result['audio_packets_identical'] and result['decoded_audio_identical'] and result['source_unchanged']
 args=[str(v.ROOT/'scripts/video/transition_guard.py'),str(v.DEST)]
 for f,label in v.BOUNDARIES.items():args+=['--boundary',f'{f}:{label}']
 args+=['--outdir',str(v.OUT/'transitions')];sys.argv=args;runpy.run_path(args[0],run_name='__main__')
if __name__=='__main__':main()
