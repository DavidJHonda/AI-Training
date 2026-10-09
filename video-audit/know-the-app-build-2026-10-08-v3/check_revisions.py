from pathlib import Path
import cv2,json
D=Path(__file__).resolve().parent
ROOT=D.parents[1]
m=json.loads((D/'edit-manifest.json').read_text())
c=cv2.VideoCapture(m['output'])
rows=[]
checks=[]
for name,t in [('model',83.82),('thinking',159.52),('research',242.54)]:
 f=round(t*30);strip=[];ims=[]
 for ff in [f-1,f,f+30]:
  c.set(cv2.CAP_PROP_POS_FRAMES,ff);ok,im=c.read();assert ok
  ims.append(im);cv2.imwrite(str(D/f'{name}-banner-{ff}.jpg'),im)
  tile=cv2.resize(im,(640,360));cv2.putText(tile,f'{name} {ff/30:.2f}s',(12,26),cv2.FONT_HERSHEY_SIMPLEX,.6,(0,0,200),2);strip.append(tile)
 delta=cv2.absdiff(ims[0][610:685],ims[1][610:685]);changed=int((delta.max(axis=2)>35).sum());assert changed>2000,(name,changed)
 rows.append(cv2.hconcat(strip));checks.append({'banner':name,'onset_frame':f,'onset_seconds':f/30,'changed_banner_pixels':changed})
cv2.imwrite(str(D/'revision-banner-checks.jpg'),cv2.vconcat(rows))
strip=[]
for ff in [6810,6930,7049]:
 c.set(cv2.CAP_PROP_POS_FRAMES,ff);ok,im=c.read();assert ok
 cv2.imwrite(str(D/f'college-{ff}.jpg'),im);tile=cv2.resize(im,(640,360));cv2.putText(tile,f'{ff/30:.2f}s',(12,26),cv2.FONT_HERSHEY_SIMPLEX,.6,(0,0,200),2);strip.append(tile)
cv2.imwrite(str(D/'revision-college-checks.jpg'),cv2.hconcat(strip));c.release()
(D/'revision-checks.json').write_text(json.dumps(checks,indent=2));print(checks)
