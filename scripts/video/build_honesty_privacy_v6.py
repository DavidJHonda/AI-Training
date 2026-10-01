#!/usr/bin/env python3
"""Remove exactly ten legacy one-second pauses; retain v5's approved diagrams."""
from pathlib import Path
import hashlib,json,re,subprocess,wave
import av,cv2,numpy as np
import build_honesty_privacy_v5 as prior
ROOT=prior.ROOT;FF=prior.FF
OUT=ROOT/'video-audit/honesty-and-privacy-pacing-2026-10-01-v6'
DEST=ROOT/'Prompts/honesty-and-privacy-v6.mp4'
APPROVED=ROOT/'Prompts/honesty-and-privacy-v5.mp4'
APPROVED_SHA='1e99beaf7f3d04c6973af2622bcb59372ef3f83764d23bd7902cafbc0af13144'
TOTAL=6900;SR=48000;SPF=1600
cv2.setNumThreads(1)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
OLD=json.loads((ROOT/'video-audit/honesty-and-privacy-repair-2026-09-12/edit-manifest.json').read_text())
CUTS=[r for r in OLD['timeline'] if r['kind']=='room_tone' and r['label'].startswith('Pause:')]
def mapped(f):return f-sum(max(0,min(f,c['end_frame'])-c['start_frame']) for c in CUTS)
def removed(f):return any(c['start_frame']<=f<c['end_frame'] for c in CUTS)
def get_pcm(path):
 return np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(path),'-map','0:a:0','-f','f32le','-']),dtype=np.float32).copy()
def db(a):return float(20*np.log10(max(float(np.sqrt(np.mean(a*a))),1e-12)))
def main():
 OUT.mkdir(exist_ok=True);assert not DEST.exists();assert sha(APPROVED)==APPROVED_SHA;assert sha(prior.SRC)==prior.EXPECTED
 protected={str(p):sha(p) for p in [APPROVED,prior.SRC,ROOT/'lessons/honesty-and-privacy.md',*prior.SRC.parent.glob('*.jpg')]}
 original=get_pcm(APPROVED)[:7200*SPF];assert len(original)==7200*SPF
 # Visual source release has exactly the same audio as the approved v5.
 assert np.array_equal(original,get_pcm(prior.SRC)[:7200*SPF])
 silences=[tuple(map(float,m)) for m in re.findall(r'silence_end: ([\d.]+) \| silence_duration: ([\d.]+)',(OUT/'source-silences.txt').read_text())]
 spans=[];cursor=0;edited_parts=[];cuts=[]
 for c in CUTS:
  a,b=c['start_frame'],c['end_frame'];assert b-a==30
  s,e=next((end-d,end) for end,d in silences if end-d<=a/30 and end>=b/30)
  clip=original[a*SPF:b*SPF];assert db(clip)<-60
  assert np.max(np.abs(clip))<10**(-45/20)
  spans.append(dict(source_start=cursor,source_end=a,output_start=mapped(cursor),output_end=mapped(a)))
  edited_parts.append(original[cursor*SPF:a*SPF]);cursor=b
  cuts.append(dict(source_start_frame=a,source_end_frame=b,source_seconds=[a/30,b/30],output_join_frame=mapped(a),label=c['label'],
   full_gap_seconds=e-s,target_gap_seconds=e-s-1,removed_seconds=1,removed_rms_dbfs=db(clip),original_gap_start=s,original_gap_end=e))
 edited_parts.append(original[cursor*SPF:]);spans.append(dict(source_start=cursor,source_end=7200,output_start=mapped(cursor),output_end=TOTAL))
 edited=np.concatenate(edited_parts);assert len(edited)==TOTAL*SPF
 for c in cuts:
  k=c['output_join_frame']*SPF
  assert db(edited[k-480:k+480])<-55
  # Five-ms bridge only within retained room tone, without shortening the timeline.
  edited[k-120:k+120]=np.linspace(edited[k-120],edited[k+119],240)
  c['seam_bridge_samples']=240;c['seam_bridge_ms']=5
 np.save(OUT/'edited-pcm.npy',edited)
 with wave.open(str(OUT/'edited.wav'),'wb') as w:
  w.setparams((1,2,SR,0,'NONE','not compressed'));w.writeframes(np.rint(np.clip(edited,-1,1)*32767).astype('<i2').tobytes())
 # Reapply exactly v5's label logic to its pre-edit source to avoid encoding the
 # corrected diagrams twice. Do not rebuild boards or change any remaining frames.
 samples={n:f for n,f in prior.frames(6290) if n in {3054,6258,6288}}
 patch=prior.Patch(samples)
 joins={c['output_join_frame']:c['label'] for c in cuts}
 for b in json.loads((ROOT/'video-audit/honesty-and-privacy-build-2026-09-30-v5/edit-manifest.json').read_text())['boundaries']:
  joins.setdefault(mapped(b['frame']),b['label'])
 # Include each extant picture cut adjacent to a removed freeze on the new timeline.
 for f in [436,704,1736,1959,2880,3054,3704,4510,4844,5519,5939,6124,6258,6522,6716,6876]:joins.setdefault(mapped(f),'retimed-source-scene')
 wants={0,TOTAL-1,mapped(3540),mapped(6480)}
 for f in joins:wants.update([f-1,f,f+12])
 tmp=OUT/'render.tmp.mp4'
 cmd=[FF,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','16','-preset','fast','-threads','2','-vf','setsar=1','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','-video_track_timescale','15360',str(tmp)]
 written=0
 with (OUT/'encode.log').open('w') as log:
  proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
  for n,f in prior.frames():
   if removed(n):continue
   out=mapped(n);assert out==written
   im=patch.render(f,n);proc.stdin.write(im.tobytes());written+=1
   if out in wants:cv2.imwrite(str(OUT/f'expected-{out:05}.jpg'),im)
   if written%900==0:print(f'Rendered {written}/{TOTAL}',flush=True)
  proc.stdin.close();assert proc.wait()==0
 assert written==TOTAL;assert all(sha(p)==h for p,h in protected.items());tmp.rename(DEST)
 manifest=dict(candidate=str(DEST),candidate_sha256=sha(DEST),approved_source=str(APPROVED),approved_source_sha256=APPROVED_SHA,
  visual_source=str(prior.SRC),visual_source_sha256=prior.EXPECTED,visual_processing='Identical v5 patches reapplied before one video encode; original source raw generations unavailable.',
  scope='User approved removal of legacy one-second pauses. No spoken words, natural gaps, board treatment, closing hold or v5 diagram correction removed.',
  source_frames=7200,total_frames=TOTAL,fps=30,duration=TOTAL/30,removed_seconds=10,cuts=cuts,kept_spans=spans,
  boundaries=[dict(frame=f,label=l) for f,l in sorted(joins.items()) if 0<f<TOTAL],
  audio=dict(sample_rate=SR,samples=len(edited),added_silence=0,quiet_seam_bridge_ms=5,source='Decoded approved v5 audio, exactly matching pre-edit visual source audio',reencoded=True),
  close=dict(start_frame=mapped(6876),hold_tail_frames=120,standard_motion_preserved=True),protected_hashes=protected,
  listening_performed=False,status='Review candidate only, not shipped or published')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
