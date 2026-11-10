from pathlib import Path
import cv2,numpy as np,json
root=Path('/Users/davidobrien/Developer/AI-Training');out=root/'video-audit/how-ai-answers-donor-plan-2026-11-10'
spans={5:[(0,20),(41,73),(115,135),(179,190)],6:[(139,158.3),(194,207.5)],7:[(132,185.7),(217,226.2)]}
for roll,ranges in spans.items():
 c=cv2.VideoCapture(str(root/f'Prompts/how-ai-answers-{roll}.mp4'));fps=c.get(cv2.CAP_PROP_FPS);i=0;groups=[[] for _ in ranges]
 while True:
  ok,im=c.read()
  if not ok:break
  t=i/fps
  if i%round(fps)==0:
   for j,(a,b) in enumerate(ranges):
    if a<=t<b:
     cv2.imwrite(str(out/f'roll-{roll}'/f'motion-{t:06.1f}.jpg'),im)
     tile=cv2.resize(im,(480,270));cv2.rectangle(tile,(0,0),(480,24),(255,255,255),-1);cv2.putText(tile,f'roll {roll} | {t:.1f}s',(8,18),0,.5,(0,0,140),1,cv2.LINE_AA);groups[j].append(tile)
  i+=1
 c.release()
 for j,tiles in enumerate(groups):
  for k in range(0,len(tiles),12):
   batch=tiles[k:k+12]
   while len(batch)%3:batch.append(np.full((270,480,3),255,np.uint8))
   cv2.imwrite(str(out/f'motion-{roll}-{j}-{k//12}.jpg'),cv2.vconcat([cv2.hconcat(batch[n:n+3]) for n in range(0,len(batch),3)]))
 print(roll,'motion strips done',flush=True)
