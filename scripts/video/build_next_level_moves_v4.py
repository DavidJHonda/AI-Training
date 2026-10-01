#!/usr/bin/env python3
"""Owner-requested zoom/pan on two conversation boards, retaining v3 inserts.
Re-render from the same v2 baseline plus original assets to avoid stacking v3 encoding.
No narration cut: the user's wording question remains a separate editorial choice.
"""
import json,subprocess
import av,cv2
import build_next_level_moves_v3 as b
import next_level_moves_zoom as zoom
ROOT=b.ROOT
OUT=zoom.OUT
DEST=ROOT/'Prompts/next-level-moves-v4.mp4'
SOURCE=b.SOURCE
TOTAL=b.TOTAL
BOARD_SPANS=zoom.SPANS
BOUNDARIES={**b.BOUNDARIES,**{f:f'{key}-board-{side}' for key,(a,e) in BOARD_SPANS.items() for f,side in [(a,'in'),(e,'out')]}}

def main():
 cv2.setNumThreads(2);OUT.mkdir(exist_ok=True);(OUT/'render-preview').mkdir(exist_ok=True)
 assert not DEST.exists(),'Never overwrite a candidate.'
 assert b.sha(SOURCE)==b.EXPECTED
 boards={k:zoom.Board(k) for k in BOARD_SPANS}
 photos={k:cv2.imread(str(b.ASSETS/f'{k}.png')) for k in ['history','tutoring','lawn']}
 protected={str(p):b.sha(p) for p in [SOURCE,ROOT/'Prompts/next-level-moves-v3.mp4',ROOT/'lessons/next-level-moves.md',*sorted((ROOT/'course-assets/next-level-moves').glob('*.jpg'))]}
 proc=subprocess.Popen([b.FF,'-v','error','-f','rawvideo','-pix_fmt','yuv420p','-s','1280x720','-r','30','-i','pipe:0','-i',str(SOURCE),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-profile:v','high','-level:v','3.1','-crf','15','-preset','fast','-threads','2','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
 wants={x for f in BOUNDARIES for x in [f-1,f,f+15]}|{TOTAL-1}
 for board in boards.values():
  for r in board.rings:wants|={board.start+r['start'],board.start+r['start']+30}
 count=0
 with av.open(str(SOURCE)) as c:
  c.streams.video[0].codec_context.thread_count=2
  for n,frame in enumerate(c.decode(video=0)):
   raw=frame.to_ndarray(format='yuv420p');insert=None
   which=next((k for k,(a,e) in b.SPANS.items() if a<=n<e),None)
   board=next((k for k,(a,e) in BOARD_SPANS.items() if a<=n<e),None)
   if which:insert=b.expected_frame(which,n,photos)
   elif board:insert=boards[board].render(n)
   if insert is not None:raw=av.VideoFrame.from_ndarray(insert,format='bgr24').to_ndarray(format='yuv420p')
   if n in wants:cv2.imwrite(str(OUT/'render-preview'/f'{n:06d}.jpg'),av.VideoFrame.from_ndarray(raw,format='yuv420p').to_ndarray(format='bgr24'))
   proc.stdin.write(raw.tobytes());count+=1
   if count%1500==0:print(f'Rendered {count}/{TOTAL}',flush=True)
 proc.stdin.close();assert proc.wait()==0 and count==TOTAL
 assert b.audio_hash(SOURCE)==b.audio_hash(DEST)
 assert b.audio_hash(SOURCE,True)==b.audio_hash(DEST,True)
 assert all(b.sha(p)==h for p,h in protected.items())
 m=dict(source=str(SOURCE),source_sha256=b.EXPECTED,candidate=str(DEST),candidate_sha256=b.sha(DEST),scope='Two-board camera change explicitly requested by user; overrides full-view-only chat convention.',approval='User: the board that appears at :55. Let\'s do the zoom and pan. Do the same for the board that appears at 4:12.',frames=count,fps=30,duration=count/30,boards={k:z.log for k,z in boards.items()},retained_v3_inserts=b.SPANS,boundaries=[dict(frame=f,label=s) for f,s in sorted(BOUNDARIES.items())],audio_packets_identical=True,decoded_audio_identical=True,narration_changes=[],added_pauses=[],pending_editorial_choice='Only redundant check-whether-you-understand phrase versus whole explain-back idea; not removed without selecting scope.',protected_hashes=protected,protected_files_unchanged=True,limitations='Full-file listening remains unperformed. Candidate only; no local ship or publish.')
 (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('COMPLETE',DEST,flush=True)

if __name__=='__main__':main()
