#!/usr/bin/env python3
"""Three user-requested repairs to v7; retain original-timeline rendering."""
import copy,json,subprocess
import cv2,numpy as np
from build_support_trap_v7 import b
b.OUT=b.ROOT/'video-audit/support-trap-repair-2026-09-30-v8'
b.DEST=b.ROOT/'Prompts/support-trap-v8.mp4'
PRIOR=b.ROOT/'Prompts/support-trap-v7.mp4'
CUT_A,CUT_B=6321,6356
REMOVED=CUT_B-CUT_A
FLASH_A,FLASH_B=4249,4320
QUOTE=1210
LEAVE=6250

def mapped(f):return f if f<CUT_A else max(CUT_A,f-REMOVED)

def specifications():
 build=b.specifications()
 p=b.OUT/'leg-comparison.json';s=json.loads(p.read_text())
 r=s['rings'][5];end=r['end'];r['end']=QUOTE-build.boards['comparison']['src_in']
 # Translate the inset quotation rectangle from the canonical board, preserving camera.
 ox,oy=r['rect'][0]-816,r['rect'][1]-271
 q=dict(start=r['end'],end=end,rect=[848+ox,819+oy,680,138],color=r['color'],pad=0,radius=14)
 s['rings'].insert(6,q);p.write_text(json.dumps(s,indent=2)+'\n')
 build.boards['comparison']['states'].insert(6,dict(spoken_onset_source_frame=QUOTE,highlight_target='Spoken AI response',highlight_mode='ring',highlight_color='#a9760c',highlight_source='card_locked_accent'))
 p=b.OUT/'leg-danger.json';s=json.loads(p.read_text());s['rings'][0]['start']=LEAVE-build.boards['danger']['src_in'];p.write_text(json.dumps(s,indent=2)+'\n')
 build.boards['danger']['states'][0]['spoken_onset_source_frame']=LEAVE
 return build

def main():
 b.OUT.mkdir(parents=True,exist_ok=True);(b.OUT/'preview').mkdir(exist_ok=True)
 assert not b.DEST.exists(),'Never overwrite a review candidate'
 assert b.sha(PRIOR)=='b06ca5534e963cfa73023125a4d2f3431bb1948899bf03b67424cc3cea6c48c1'
 for key,src in b.SOURCES.items():assert b.sha(src)==b.EXPECTED[key]
 protected={str(p):b.sha(p) for p in [PRIOR,*b.SOURCES.values(),b.ASSET,*list((b.ROOT/'course-assets/support-trap').glob('*.jpg')),b.ROOT/'course-assets/support-trap/support-trap.mp4']}
 build=specifications();boards={k:b.BoardRender(k,v) for k,v in build.boards.items()}
 pcm=b.ROOT/'video-audit/support-trap-build-2026-09-30-v6/edited.wav';original=b.wavread(pcm);assert len(original)==b.TOTAL*b.SPF
 audio=np.concatenate([original[:CUT_A*b.SPF],original[CUT_B*b.SPF:]])
 # Five milliseconds at each quiet edge, without changing timing or speech gain.
 seam=CUT_A*b.SPF;ramp=np.linspace(0,1,240)
 audio[seam-240:seam]*=1-ramp;audio[seam:seam+240]*=ramp
 b.wavwrite(b.OUT/'edited.wav',audio)
 row=next(r for r in b.VIS if r['start_frame']==FLASH_A)
 source_frame=row['video_start']+FLASH_B-FLASH_A
 rr=b.Reader(b.SOURCES[row['key']]);hold,_=b.clean_frame(rr.at(source_frame),b.MASK);rr.cap.release()
 boundaries={mapped(r['start_frame']):r['label'] for r in [*b.VIS[1:],*b.AUDIO[1:]]}
 boundaries.update({QUOTE:'AI quote highlight',LEAVE:'Leave chat highlight on retained instruction',FLASH_B:'Resume settled danger graphic',CUT_A:'Remove repeated Leave the chat'})
 vis=[]
 for r in b.VIS:
  v=copy.deepcopy(r);v['original_start_frame']=r['start_frame'];v['original_end_frame']=r['end_frame'];v['start_frame']=mapped(r['start_frame']);v['end_frame']=mapped(r['end_frame']);vis.append(v)
 m=dict(output=str(b.DEST),approval='User requests: highlight AI response at :40; remove flash at 2:22; delete repeated Leave the chat at 3:31.',fps=30,total_frames=b.TOTAL-REMOVED,duration=(b.TOTAL-REMOVED)/30,source_hashes=b.EXPECTED,prior=str(PRIOR),original_visual_timeline=b.VIS,visual_timeline=vis,original_audio_timeline=b.AUDIO,original_timeline_boards=build.boards,boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],repairs=dict(quote=dict(start_frame=QUOTE,end_frame=1387,canonical_rect=[848,819,1528,957],camera='Unchanged complete-card view'),flash=dict(start_frame=FLASH_A,end_frame=FLASH_B,source=row['key'],hold_source_frame=source_frame),deletion=dict(original_start_frame=CUT_A,original_end_frame=CUT_B,removed_frames=REMOVED,silence_edge_fade_ms=5),leave_highlight_original_frame=LEAVE),audio=dict(source_PCM=str(pcm),source_sha256=b.sha(pcm),sample_rate=48000,global_normalization=False),close=dict(start_frame=b.CLOSE_START-REMOVED,prehold=48,push=150,endpoint=1.2,settle=30),scope='Review candidate; not shipped or published.')
 proc=subprocess.Popen([b.FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(b.OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(b.DEST)],stdin=subprocess.PIPE)
 readers={};written=0
 wanted={QUOTE-1,QUOTE,QUOTE+30,FLASH_A-1,FLASH_A,FLASH_B-1,FLASH_B,LEAVE-1,LEAVE,CUT_A-1,CUT_B,b.TOTAL-1}
 for i,r in enumerate(b.VIS):
  reader=None
  if r['kind']=='native':
   key=r['key'];reader=readers.get(key)
   if reader is None or reader.n>r['video_start']:
    if reader:reader.cap.release()
    reader=b.Reader(b.SOURCES[key]);readers[key]=reader
  still=cv2.imread(r['asset']) if r['kind']=='image' else None
  for f in range(r['start_frame'],r['end_frame']):
   if CUT_A<=f<CUT_B:continue
   if FLASH_A<=f<FLASH_B:im=hold
   else:im,_=b.render_frame(r,f,boards,reader,still,build.close_img)
   if f in wanted:cv2.imwrite(str(b.OUT/'preview'/f'{mapped(f):06d}.jpg'),im)
   proc.stdin.write(im.tobytes());written+=1
  print(f'Render {i+1}/{len(b.VIS)}: {r["label"]}',flush=True)
 for r in readers.values():r.cap.release()
 proc.stdin.close();assert proc.wait()==0 and written==b.TOTAL-REMOVED
 m.update(render_sha256=b.sha(b.DEST),encoded_input_frames=written,protected_files_unchanged={p:b.sha(p)==s for p,s in protected.items()})
 assert all(m['protected_files_unchanged'].values())
 (b.OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 print('COMPLETE',b.DEST,m['duration'],flush=True)
if __name__=='__main__':main()
