"""Visual-only character sync from frozen live files, never candidate-to-candidate."""
from pathlib import Path
import sys,json,subprocess,concurrent.futures
import cv2,numpy as np
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts/video'))
import build_avoid_illustration_sync as base
import build_work_changes_hybrid as v
A=R/'video-audit/embrace-illustration-sync-2026-09-08'
base.BASE=A;base.AUDIT=A/'build';base.REVISION=''
def state(frame,label,rect=None,color='#6e51ff',camera=None,move=0):
    d=base.state(frame,label,rect,color,None,move);d['camera']=camera;return d
def groups():
    result=[]
    for slug in ['opener-embrace','big-downside','rise-of-agents','work-changes']:
        m=json.loads((A/slug/'scan.json').read_text());g=dict(slug=slug,baseline=m['video'],baseline_sha=m['live_sha256'],frames=m['frames'],legs=[])
        if slug=='opener-embrace':
            start,end=1575,2262
            states=[state(f,label) for f,label in [(start,'full-map'),(1731,'map-push'),(1830,'toward-monster'),(1910,'monster-hold'),(2110,'toward-open-water'),(2160,'island-hold')]]
        elif slug=='big-downside':
            start,end=2981,3463
            states=[state(start,'full-illustration'),state(3075,'title',(31,19,1356,95)),state(3180,'defenders',(469,674,688,907),camera=(670,798,1320),move=24),state(3362,'attacker',(688,683,864,890),camera=(670,798,1320))]
        elif slug=='rise-of-agents':
            # Four inherited blank transition frames directly precede the old board.
            # Cover them with the new board, preserving all original audio/timing.
            start,end=950,1152;states=[state(start,'full-comparison')]
        else:
            start,end=2973,5517;P='#4f2fc4';Y='#a9760c'
            states=[state(start,'full-assignment'),
                state(3060,'before-intro',(29,245,588,741),P,(308,493,993),24),
                state(3246,'before-first-pass',(29,741,588,953),P,(308,847,782),18),
                state(3839,'before-then',(29,955,588,1109),P,(308,1032,782),18),
                state(4024,'before-result',(29,1139,588,1273),P,(308,1206,782),18),
                state(4298,'with-intro',(615,245,1173,741),Y,(894,493,993),24),
                state(4422,'ai-first-pass',(615,741,1173,953),Y,(894,847,782),18),
                state(4843,'you-start-here',(615,955,1173,1139),Y,(894,1047,782),18),
                state(5287,'with-result',(615,1139,1173,1273),Y,(894,1206,782),18)]
        leg=dict(asset=m['asset'],asset_sha=m['asset_sha256'],start=start,end=end,states=states)
        if slug=='opener-embrace':leg.update(track=m['video'],old_asset=m['old_asset'])
        g['legs']=[leg];result.append(g)
    return result
def track_map(leg,audit):
    old=cv2.imread(leg['old_asset']);new=cv2.imread(leg['asset']);s=900/old.shape[1]
    sift=cv2.SIFT_create(nfeatures=2500);k,d=sift.detectAndCompute(cv2.cvtColor(cv2.resize(old,None,fx=s,fy=s),cv2.COLOR_BGR2GRAY),None);bf=cv2.BFMatcher()
    cap=cv2.VideoCapture(leg['track']);cap.set(cv2.CAP_PROP_POS_FRAMES,leg['start']);keys=[]
    for f in range(leg['start'],leg['end']):
        ok=cap.grab();assert ok
        if (f-leg['start'])%3 and f!=leg['end']-1:continue
        _,im=cap.retrieve();k2,d2=sift.detectAndCompute(cv2.cvtColor(im,cv2.COLOR_BGR2GRAY),None)
        good=[a for a,b in bf.knnMatch(d,d2,k=2) if a.distance<.68*b.distance]
        p=np.float32([k[a.queryIdx].pt for a in good])/s;q=np.float32([k2[a.trainIdx].pt for a in good])
        H,mask=cv2.estimateAffinePartial2D(p,q,method=cv2.RANSAC,ransacReprojThreshold=2)
        assert H is not None and mask.sum()>25,(f,len(good))
        # The source camera is axis-aligned; discard subpixel feature-fit rotation.
        keys.append([f,float((H[0,0]+H[1,1])/2),float(H[0,2]),float(H[1,2])])
    cap.release();(audit/'camera-track.json').write_text(json.dumps(keys,indent=2)+'\n')
    return old,new,np.array(keys)
def render(leg,path,audit):
    states=leg['states'];qa=[];n=0
    targets={f:s['label'] for i,s in enumerate(states) for f in [s['frame'],min((states[i+1]['frame'] if i+1<len(states) else leg['end'])-1,s['frame']+max(35,s['move']+5)),(states[i+1]['frame'] if i+1<len(states) else leg['end'])-1]}
    if 'track' in leg:old,new,keys=track_map(leg,audit)
    else:canvas,ox,oy,full=v.build_canvas(Path(leg['asset']));previous=full
    process=subprocess.Popen([base.FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','-','-an','-c:v','ffv1','-level','3','-threads','2',str(path)],stdin=subprocess.PIPE)
    for j,s in enumerate(states):
        end=states[j+1]['frame'] if j+1<len(states) else leg['end']
        if 'track' not in leg:target=v.map_camera(s['camera'],ox,oy) if s['camera'] else full
        for f in range(s['frame'],end):
            if 'track' in leg:
                scale,tx,ty=[np.interp(f,keys[:,0],keys[:,i]) for i in [1,2,3]]
                H=np.float32([[scale*old.shape[1]/new.shape[1],0,tx],[0,scale*old.shape[0]/new.shape[0],ty]])
                out=cv2.warpAffine(new,H,(1280,720),flags=cv2.INTER_LANCZOS4,borderMode=cv2.BORDER_CONSTANT,borderValue=v.hex_bgr(v.LAVENDER))
            else:
                k=f-s['frame'];c=target
                if s['move'] and k<s['move']:
                    t=v.smoothstep(k/max(1,s['move']-1));c=tuple(a+(b-a)*t for a,b in zip(previous,target))
                out=v.crop_frame(canvas,c)
                if s['rect']:
                    rect=v.project_rect(v.map_rect(s['rect'],ox,oy),c)
                    v.rounded_ring(out,rect,v.hex_bgr(s['color']),radius=12,thickness=5)
                    if k>=s['move']:assert min(rect[:2])>=12 and rect[2]<=1268 and rect[3]<=708,(s,rect)
            if f in targets:
                p=audit/'states'/f'{f:06d}-{targets[f]}.jpg';cv2.imwrite(str(p),out);qa.append(dict(frame=f,path=str(p),label=targets[f]))
            process.stdin.write(out.tobytes());n+=1
        if 'track' not in leg:previous=target
    process.stdin.close();assert process.wait()==0 and n==leg['end']-leg['start']
    return qa
def main():
    cv2.setNumThreads(1);base.render_leg=render;g=groups();base.AUDIT.mkdir(exist_ok=True)
    (A/'replacement-plan.json').write_text(json.dumps(g,indent=2)+'\n')
    if len(sys.argv)>1:g=[x for x in g if x['slug'] in sys.argv[1:]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:r=list(pool.map(base.encode,g))
    (base.AUDIT/'results.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
