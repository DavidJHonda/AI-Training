#!/usr/bin/env python3
"""V8 teaching plus the continuous live ending and retimed supporting pictures."""
import copy,json,subprocess
import cv2,numpy as np
import build_support_trap_v8 as repair
b=repair.b
b.OUT=b.ROOT/'video-audit/support-trap-hybrid-2026-09-30-v9'
b.DEST=b.ROOT/'Prompts/support-trap-v9.mp4'
JOIN=4681;LIVE_IN=4026;LIVE_END=7910;OFFSET=JOIN-LIVE_IN
TOTAL=LIVE_END+OFFSET
GAIN=-5.4
EARLY=[copy.deepcopy(r) for r in b.VIS if r['end_frame']<=JOIN]
def at(t):return b.fr(t)+OFFSET

def setup():
 build=repair.specifications()
 def target(label,t,rect):return dict(label=label,at=at(t)/30,rects=[rect],color='#c41f28',cam=rect)
 build.board('danger',b.ROOT/'course-assets/support-trap/support-trap-danger.jpg',at(193.6),at(246.066667),'compact',[
  target('Leave the Chat',203.22,[40,127,525,733]),target('Do It Now',216.24,[557,127,1043,733]),target('Tell Anyway',227.98,[1075,127,1560,733])],banner_at=at(240.8)/30,push=False,banner=[40,773,1560,861])
 b.CLOSE_START=at(252.9);b.TOTAL=TOTAL
 rows=copy.deepcopy(EARLY)
 def native(a,z,key,s,e,label,retime=False,clean=False):rows.append(dict(start_frame=a,end_frame=z,kind='native',label=label,key=key,video_start=b.fr(s),video_end=b.fr(e),retime=retime,clean=clean))
 # Preserve the live story pictures, motion, warning and pause in source sync.
 times=[134.2,142.1,148.833333,157.566667,175.1,193.6]
 labels=['Live warning and original breathing room','Live story attribution','Live private chat with Harry','Live limits of digital support','Live death and black-box account']
 for s,e,label in zip(times,times[1:],labels):native(at(s),at(e),'live',s,e,label)
 rows.append(dict(start_frame=at(193.6),end_frame=at(217.4),kind='board',board='danger',label='Safety introduction, leave chat, do it now'))
 native(at(217.4),at(226.9),'1',142.5,148.2,'Urgency: reach real help now',True,True)
 rows.append(dict(start_frame=at(226.9),end_frame=at(246.066667),kind='board',board='danger',label='Tell anyway and safety takeaway'))
 native(at(246.066667),at(252.9),'1',232.9,240.033333,'Knowing when to leave the chat',True,True)
 rows.append(dict(start_frame=b.CLOSE_START,end_frame=TOTAL,kind='close',label='Canonical close with live narration'))
 assert all(a['end_frame']==z['start_frame'] for a,z in zip(rows,rows[1:]))
 return build,rows

def main():
 b.OUT.mkdir(parents=True,exist_ok=True);(b.OUT/'preview').mkdir(exist_ok=True)
 assert not b.DEST.exists(),'Never overwrite a candidate'
 for key,p in b.SOURCES.items():assert b.sha(p)==b.EXPECTED[key]
 protected={str(p):b.sha(p) for p in [*b.SOURCES.values(),b.ASSET,*list((b.ROOT/'course-assets/support-trap').glob('*.jpg')),b.ROOT/'course-assets/support-trap/support-trap.mp4']}
 build,rows=setup();boards={k:b.BoardRender(k,v) for k,v in build.boards.items()}
 # Reuse pristine assembled opening PCM; decode the live donor directly for one continuous ending.
 opening_path=b.ROOT/'video-audit/support-trap-repair-2026-09-30-v8/edited.wav'
 live_path=b.OUT/'live-source.wav'
 subprocess.run([b.FF,'-y','-v','error','-i',str(b.SOURCES['live']),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(live_path)],check=True)
 live=b.wavread(live_path);opening=b.wavread(opening_path)[:JOIN*b.SPF]
 ending=live[LIVE_IN*b.SPF:LIVE_END*b.SPF]*10**(GAIN/20)
 # Only the initial join receives a 5 ms ramp to matched live room tone. No edits inside the ending.
 seed=live[b.fr(134.1)*b.SPF:b.fr(134.2)*b.SPF]*10**(GAIN/20);bed=np.resize(seed,240);ramp=np.linspace(0,1,240)
 ending[:240]=ending[:240]*ramp+bed*(1-ramp)
 audio=np.r_[opening,ending];assert len(audio)==TOTAL*b.SPF;b.wavwrite(b.OUT/'edited.wav',audio)
 flashrow=next(r for r in rows if r['start_frame']==repair.FLASH_A)
 reader=b.Reader(b.SOURCES['1']);hold,_=b.clean_frame(reader.at(flashrow['video_start']+repair.FLASH_B-repair.FLASH_A),b.MASK);reader.cap.release()
 boundaries={r['start_frame']:r['label'] for r in rows[1:]}
 boundaries.update({r['start_frame']:r['label'] for r in b.AUDIO[1:] if r['start_frame']<JOIN})
 boundaries[repair.QUOTE]='Spoken AI quote highlight';boundaries[repair.FLASH_B]='Resume settled tool-versus-trap graphic'
 m=dict(output=str(b.DEST),approval='User: build it please, following approved live-ending hybrid plan.',fps=30,total_frames=TOTAL,duration=TOTAL/30,source_hashes=b.EXPECTED,visual_timeline=rows,boards=build.boards,boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],audio=dict(opening_PCM=str(opening_path),opening_sha256=b.sha(opening_path),opening_frames=JOIN,live_source=str(b.SOURCES['live']),live_source_start_frame=LIVE_IN,live_source_end_frame=LIVE_END,live_gain_db=GAIN,continuous_live_ending=True,join_ramp_ms=5,sample_rate=48000,added_pauses=False,wording_note='Live narration retained intact, including encouraged her to seek professional help without the lesson qualifier sometimes. No word-level graft introduced.'),close=dict(start_frame=b.CLOSE_START,prehold=48,push=150,endpoint=1.2,settle=TOTAL-b.CLOSE_START-198),longest_board_run=max((r['end_frame']-r['start_frame'])/30 for r in rows if r['kind']=='board'),scope='Review candidate only; not installed or published.')
 proc=subprocess.Popen([b.FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(b.OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(b.DEST)],stdin=subprocess.PIPE)
 readers={};written=0
 wants={f for r in rows for f in [r['start_frame'],r['end_frame']-1,(r['start_frame']+r['end_frame'])//2]}
 for key,meta in build.boards.items():wants.update(s['spoken_onset_source_frame']+15 for s in meta['states'])
 for i,r in enumerate(rows):
  reader=None
  if r['kind']=='native':
   reader=readers.get(r['key'])
   if reader is None or reader.n>r['video_start']:
    if reader:reader.cap.release()
    reader=b.Reader(b.SOURCES[r['key']]);readers[r['key']]=reader
  still=cv2.imread(r['asset']) if r['kind']=='image' else None
  for f in range(r['start_frame'],r['end_frame']):
   if repair.FLASH_A<=f<repair.FLASH_B:im=hold
   else:im,_=b.render_frame(r,f,boards,reader,still,build.close_img)
   if f in wants:cv2.imwrite(str(b.OUT/'preview'/f'{f:06d}.jpg'),im)
   proc.stdin.write(im.tobytes());written+=1
  print(f'Render {i+1}/{len(rows)}: {r["label"]}',flush=True)
 for r in readers.values():r.cap.release()
 proc.stdin.close();assert proc.wait()==0 and written==TOTAL
 m.update(render_sha256=b.sha(b.DEST),encoded_input_frames=written,protected_files_unchanged={p:b.sha(p)==s for p,s in protected.items()});assert all(m['protected_files_unchanged'].values())
 (b.OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('COMPLETE',b.DEST,TOTAL/30,flush=True)
if __name__=='__main__':main()
