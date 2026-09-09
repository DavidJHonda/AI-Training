from pathlib import Path
import json,subprocess,concurrent.futures,hashlib,sys
import cv2,numpy as np
R=Path('/Users/davidobrien/Developer/AI-Training');A=R/'video-audit/build-skills-illustration-sync-2026-09-09/build'
def run(path):
    m=json.loads(path.read_text());old=cv2.VideoCapture(m['baseline']);new=cv2.VideoCapture(m['candidate']);n=0;diffs=[];peaks=[];sampleframes=[]
    edges={x for leg in m['legs'] for edge in (leg['start'],leg['end']) for x in range(edge-12,edge+13)}
    states={q['frame'] for q in m['qa']}
    target=path.parent/'final-qa';target.mkdir(exist_ok=True)
    while True:
        ok,im=old.read();ok2,other=new.read();assert ok==ok2
        if not ok:break
        changed=any(leg['start']<=n<leg['end'] for leg in m['legs'])
        if not changed and (n%30==0 or n in edges):
            delta=np.abs(im.astype(np.float32)-other.astype(np.float32));diffs.append(float(delta.mean()));sampleframes.append(n)
        if n in states:cv2.imwrite(str(target/f'{n:06d}.jpg'),other)
        if n in edges and not changed:peaks.append((n,float(np.abs(im.astype(np.float32)-other.astype(np.float32)).mean())))
        n+=1
    old.release();new.release();assert n==m['frames']
    assert max(diffs)<2.5,(m['slug'],max(diffs),sampleframes[int(np.argmax(diffs))])
    native=[]
    for p in [m['candidate'],m['review_reel']]:
        result=subprocess.run(['/private/tmp/check_flattery_playback',p],capture_output=True,text=True);log=result.stdout+result.stderr
        assert result.returncode==0 and 'Playable: YES' in log and 'Native first frame decoded: YES' in log,log
        native.append(log)
    result=dict(slug=m['slug'],decoded_frames=n,expected_frames=m['frames'],outside_samples=len(diffs),maximum_outside_mean_absolute_pixel_difference=max(diffs),worst_outside_frame=sampleframes[int(np.argmax(diffs))],outside_boundary_differences=peaks,native_playback=native)
    (path.parent/'fidelity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['native_playback','outside_boundary_differences']}),flush=True);return result
cv2.setNumThreads(1)
paths=sorted(A.glob('*/manifest.json'))
if len(sys.argv)>1:paths=[p for p in paths if p.parent.name in sys.argv[1:]]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,paths))
