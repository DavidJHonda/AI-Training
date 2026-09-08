from pathlib import Path
import sys,json,subprocess,hashlib,copy
import cv2,numpy as np
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'scripts/video'))
import build_support_trap_reroll_review as b
v=b.v
A=R/'video-audit/avoid-traps-illustration-sync-2026-09-08/support-trap-pilot'
A.mkdir(parents=True,exist_ok=False)
live=R/'videos/support-trap.mp4'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
live_hash=sha(live)
previous=json.loads((R/'video-audit/support-trap-secrecy-repair-2026-09-08/manifest.json').read_text())
assert live_hash==previous['sha256'], 'Live changed; remap before proceeding'
b.AUDIT=A
b.OUT=A/'raw-rebuild.mp4'
# Coordinates measured on the approved 1222x1287 lesson JPEG, not scaled
# estimates from the old 1600x1511 board. Card rails track outer boundaries.
b.left=(33,224,601,1093)
b.right=(624,224,1191,1093)
targets={
 'sister-acts':b.left,
 'chatbot-response':b.right,
 'caring-words':(624,792,1191,881),
 'nothing-changed':(624,987,1191,1077),
 'cannot-show-up':(624,889,1191,981),
 'support-trap-definition':(33,1127,1191,1210),
}
for c in b.chunks:
    if c['board']=='compare' and c['label'] in targets:
        c['rect']=targets[c['label']]
        if c['camera'] is not None:c['camera']=b.cam(b.left if c['label']=='sister-acts' else b.right)
assert cv2.imread(str(b.BOARDS['compare'])).shape[:2]==(1287,1222)
b.main()
out=R/'Prompts/support-trap-illustrations-patched.mp4'
assert not out.exists()
subprocess.run([b.FF,'-v','error','-i',str(A/'picture.mp4'),'-i',str(live),'-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',str(out)],check=True)
def audio_hash(path):
    data=subprocess.check_output([b.FF,'-v','error','-i',str(path),'-map','0:a','-c','copy','-f','data','-'])
    return hashlib.sha256(data).hexdigest()
assert audio_hash(live)==audio_hash(out)
caps=[cv2.VideoCapture(str(p)) for p in [live,out]]
n=0;outside=[];states={405,434,503,528,650,809,834,950,1104,1170,1233,1370,1479,1515,1566,1590,1750,1883,1884}
while True:
    ok,a=caps[0].read();ok2,z=caps[1].read();assert ok==ok2
    if not ok:break
    if not 405<=n<1884 and (n%30==0 or n in states):outside.append(float(np.abs(a.astype(float)-z.astype(float)).mean()))
    if n in states:
        cv2.imwrite(str(A/f'final-{n:06d}.jpg'),z)
    n+=1
assert n==6312 and max(outside)<0.3,(n,max(outside))
assert live_hash==sha(live)
reel=R/'Prompts/support-trap-illustrations-review-reel.mp4'
assert not reel.exists()
subprocess.run([b.FF,'-v','error','-i',str(out),'-ss','11.5','-t','53.5','-c:v','libx264','-crf','18','-preset','fast','-c:a','aac','-b:a','192k','-movflags','+faststart',str(reel)],check=True)
result=dict(candidate=str(out),candidate_sha256=sha(out),baseline=str(live),baseline_sha256=live_hash,frame_count=n,fps=30,duration=n/30,audio_packets_identical=True,audio_packet_sha256=audio_hash(out),changed_frames=[405,1884],changed_seconds=[13.5,62.8],review_reel=str(reel),reel_offset_seconds=11.5,outside_compared_frames=len(outside),max_outside_mean_pixel_difference=max(outside),asset=str(b.BOARDS['compare']),asset_sha256=sha(b.BOARDS['compare']),canonical_bounds=targets,live_and_lesson_files_written=False)
(A/'integrity.json').write_text(json.dumps(result,indent=2)+'\n')
print('PILOT COMPLETE',json.dumps(result),flush=True)
