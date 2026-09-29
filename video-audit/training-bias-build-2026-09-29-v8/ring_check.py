import sys,json,cv2,numpy as np
sys.path.insert(0,'scripts/video')
import build_training_bias_v8 as b
out=b.OUT
rows=[]
for key in ['skew','questions','rag']:
 spec=json.loads((b.OLD/f'leg-{key}.json').read_text())
 for j,r in enumerate(spec['rings']):
  n=b.ORIG_START[key]+r['start']+1
  # The rag Retrieve representative is f6320, also the ring's second frame.
  p=out/'encoded'/f'{n:05d}.jpg'
  if not p.exists():continue
  im=cv2.imread(str(p));x,y,w,h=np.array(r['rect'])*.8
  c=np.array(b.hex_bgr(r['color']));widths=[]
  for yy in np.linspace(y+h*.68,y+h*.87,15).astype(int):
   for xx in [x,x+w]:
    line=im[yy,round(xx)-8:round(xx)+9].astype(float)
    hit=np.linalg.norm(line-c,axis=1)<60;widths.append(int(np.count_nonzero(hit)))
  rows.append(dict(board=key,state=j,frame=n,solid_stroke_px_median=float(np.median(widths)),range=[min(widths),max(widths)],note='Solid-color threshold on the two vertical edges, compression and antialiasing excluded. Design is 4 px.'))
(out/'ring-check.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
