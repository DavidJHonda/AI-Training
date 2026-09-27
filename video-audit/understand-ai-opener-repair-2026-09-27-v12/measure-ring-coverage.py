from pathlib import Path
import cv2,numpy as np,json
p=Path('/Users/davidobrien/Developer/AI-Training/video-audit/understand-ai-opener-repair-2026-09-27-v12');m=json.loads((p/'edit-manifest.json').read_text())
rows=[]
for key,(a,b) in m['board_spans_before_break'].items():
 spec=m['boards'][key];cw=spec['beats'][0]['from'][2];scale=1280/cw;base=cv2.imread(str(p/'preview'/f'{key}-0000.png')).astype(float)
 for ring in spec['rings']:
  t=a+ring['start']+15;t=3490 if 3235<=t<3475 else t;fr=cv2.imread(str(p/'encoded-frames'/f'{t:04d}.png')).astype(float)
  rx,ry,rw,rh=ring['rect'];l,top,r,bottom=[int(round(q)) for q in (rx*scale-4,ry*scale-4,(rx+rw)*scale+4,(ry+rh)*scale+4)];cx=(l+r)//2;cy=(top+bottom)//2;rgb=ring['color'][1:];col=np.array([int(rgb[i:i+2],16) for i in (4,2,0)])
  widths={};sums={}
  for side,ys,xs in [('top',slice(top-3,top+8),cx),('bottom',slice(bottom-8,bottom+3),cx),('left',cy,slice(l-3,l+8)),('right',cy,slice(r-8,r+3))]:
   bg=base[ys,xs];v=col-bg;d=fr[ys,xs]-bg;alpha=np.clip(np.sum(d*v,axis=1)/np.sum(v*v,axis=1),0,1);widths[side]=int((alpha>.5).sum());sums[side]=round(float(alpha.sum()),3)
  row={'key':key,'frame':t,'color':ring['color'],'half_coverage_pixels':widths,'integrated_coverage_pixels':sums};rows.append(row);print(row)
  assert all(w==4 for w in widths.values()),row
(p/'ring-coverage.json').write_text(json.dumps(rows,indent=2))
