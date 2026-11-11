from pathlib import Path
import json,cv2,numpy as np
out=Path(__file__).resolve().parent;m=json.loads((out/'edit-manifest.json').read_text())
c=cv2.VideoCapture(m['output']);want={};rows=[]
for key,board in m['boards'].items():
 row=next(r for r in m['timeline'] if r.get('visual')==key)
 base=row['start_frame'];spec=json.loads((out/f'leg-{key}.json').read_text());canvas=cv2.imread(spec['image']);scale=1280/canvas.shape[1]
 want[base]=None
 for ring in spec['rings']:
  at=base+ring['start']+min(15,ring['end']-ring['start']-1);want[at]=None
  rows.append(dict(key=key,base=base,at=at,scale=scale,ring=ring))
i=0
while i<=max(want):
 ok,im=c.read();assert ok
 if i in want:want[i]=im.astype(float)
 i+=1
c.release();result=[]
for row in rows:
 r=row['ring'];scale=row['scale'];x,y,w,h=r['rect'];pad=r.get('pad',0);col=r['color'].lstrip('#');color=np.array([int(col[i:i+2],16) for i in [4,2,0]])
 x0=(x-pad)*scale-2;x1=(x+w+pad)*scale+2;y0=(y-pad)*scale-2;y1=(y+h+pad)*scale+2
 a=want[row['base']];b=want[row['at']];widths={}
 for name,edge,is_horizontal in [('top',y0,True),('bottom',y1,True),('left',x0,False),('right',x1,False)]:
  k0=int(np.floor(edge))-5;k1=int(np.ceil(edge))+6
  if is_horizontal:
   span=np.arange(round(x0+(x1-x0)/3),round(x0+2*(x1-x0)/3));bg=a[k0:k1,span];obs=b[k0:k1,span]
  else:
   span=np.arange(round(y0+(y1-y0)/3),round(y0+2*(y1-y0)/3));bg=a[span,k0:k1].transpose(1,0,2);obs=b[span,k0:k1].transpose(1,0,2)
  direction=color-bg;alpha=np.clip(((obs-bg)*direction).sum(axis=2)/np.maximum((direction*direction).sum(axis=2),1),0,1)
  widths[name]=float(np.median(alpha.sum(axis=0)))
 assert all(3.6<v<4.4 for v in widths.values()),widths
 result.append(dict(board=row['key'],color=r['color'],output_frame=row['at'],effective_width_pixels=widths))
(out/'ring-width-verification.json').write_text(json.dumps(dict(method='Color-projected alpha area across straight edges, referenced to encoded unmarked board; integrated width includes fractional anti-alias coverage',target_pixels=4,pass_=True,measurements=result),indent=2)+'\n')
print(json.dumps(result,indent=2))
