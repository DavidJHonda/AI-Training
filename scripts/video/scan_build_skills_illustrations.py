from pathlib import Path
import cv2,numpy as np,json,hashlib,concurrent.futures
from PIL import Image,ImageDraw
R=Path('/Users/davidobrien/Developer/AI-Training');A=R/'video-audit/build-skills-illustration-sync-2026-09-09'
entries=json.loads((R/'archive/illustration-backups/build-your-skills-character-update-2026-09-09/manifest.json').read_text())['images']
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def scan(slug):
    d=A/slug;d.mkdir(parents=True,exist_ok=True)
    selected=[e for e in entries if e['slug'].startswith('honesty' if slug=='honesty-and-privacy' else slug)]
    sift=cv2.SIFT_create(nfeatures=2000);matcher=cv2.BFMatcher();features=[]
    for e in selected:
        im=cv2.imread(e['backup']);scale=900/im.shape[1];small=cv2.resize(im,None,fx=scale,fy=scale)
        kp,desc=sift.detectAndCompute(cv2.cvtColor(small,cv2.COLOR_BGR2GRAY),None)
        features.append((e,scale,kp,desc,[]))
    video=R/'videos'/f'{slug}.mp4';cap=cv2.VideoCapture(str(video));fps=cap.get(cv2.CAP_PROP_FPS);n=0;samples=[]
    while cap.grab():
        if n%15==0:
            _,frame=cap.retrieve();k2,d2=sift.detectAndCompute(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),None)
            for e,scale,kp,desc,hits in features:
                good=[] if d2 is None else [a for pair in matcher.knnMatch(desc,d2,k=2) if len(pair)==2 for a,b in [pair] if a.distance<.68*b.distance]
                if len(good)<10:continue
                H,mask=cv2.findHomography(np.float32([kp[g.queryIdx].pt for g in good]),np.float32([k2[g.trainIdx].pt for g in good]),cv2.RANSAC,3)
                count=int(mask.sum()) if mask is not None else 0
                if count>=15:hits.append(dict(frame=n,inliers=count,H=(H@np.diag([scale,scale,1])).tolist()))
            if n%300==0:samples.append((n,Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)).resize((320,180))))
        n+=1
    cap.release();out=Image.new('RGB',(1280,((len(samples)+3)//4)*204),'white');draw=ImageDraw.Draw(out)
    for i,(f,im) in enumerate(samples):
        x=i%4*320;y=i//4*204;out.paste(im,(x,y+24));draw.text((x+4,y+4),f'{slug} {f/30:.1f}s f{f}',fill='black')
    out.save(d/'overview.jpg',quality=85)
    result=dict(slug=slug,video=str(video),frames=n,fps=fps,live_sha256=sha(video),assets=[])
    for e,scale,kp,desc,hits in features:
        runs=[]
        for h in hits:
            if h['inliers']<50:continue
            if not runs or h['frame']>runs[-1][-1]+30:runs.append([h['frame']])
            else:runs[-1].append(h['frame'])
        result['assets'].append(dict(slug=e['slug'],asset=e['target'],asset_sha256=e['new_sha256'],old_asset=e['backup'],hits=hits,runs=[(r[0],r[-1]) for r in runs]))
    (d/'scan.json').write_text(json.dumps(result,indent=2)+'\n')
    print(slug,n,fps,[(e['slug'],e['runs']) for e in result['assets']],flush=True)
cv2.setNumThreads(1)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(scan,['honesty-and-privacy','people-skills','make-your-move']))
