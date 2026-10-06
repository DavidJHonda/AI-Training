"""Build the lesson's geographic SVG from Census-derived US Atlas boundaries.
No runtime mapping library or external map request is needed.
"""
import collections,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'scripts/video/assets/vector-space-map/states-10m.json'
OUT=ROOT/'course-assets/vector-space/vector-space-us-map.svg'
# Albers equal-area conic: standard parallels 29.5/45.5 N, central meridian 96 W.
p1,p2=map(math.radians,[29.5,45.5]);N=(math.sin(p1)+math.sin(p2))/2
C=math.cos(p1)**2+2*N*math.sin(p1)
def project(lon,lat):
    theta=N*math.radians(lon+96);rho=math.sqrt(C-2*N*math.sin(math.radians(lat)))/N
    return rho*math.sin(theta),rho*math.cos(theta)

def main():
    data=json.loads(SOURCE.read_text());scale=data['transform']['scale'];trans=data['transform']['translate']
    arcs=[]
    for arc in data['arcs']:
        x=y=0;points=[]
        for dx,dy in arc:
            x+=dx;y+=dy;points.append(project(x*scale[0]+trans[0],y*scale[1]+trans[1]))
        arcs.append(points)
    states=[s for s in data['objects']['states']['geometries'] if int(s['id'])<=56 and s['id'] not in ['02','15']]
    assert len(states)==49
    counts=collections.Counter()
    def rings(s):
        if s['type']=='Polygon':return s['arcs']
        return [ring for polygon in s['arcs'] for ring in polygon]
    for s in states:
        for ring in rings(s):
            for a in ring:counts[a if a>=0 else ~a]+=1
    points=[p for a in counts for p in arcs[a]]
    xmin,xmax=min(p[0] for p in points),max(p[0] for p in points)
    ymin,ymax=min(p[1] for p in points),max(p[1] for p in points)
    fit=min(644/(xmax-xmin),328/(ymax-ymin))
    tx=360-fit*(xmin+xmax)/2;ty=185-fit*(ymin+ymax)/2
    def xy(p):return (round(tx+fit*p[0],2),round(ty+fit*p[1],2))
    def path(points):return 'M'+'L'.join(','.join(map(str,xy(p))) for p in points)
    paths=[]
    for state in states:
        d=''
        for ring in rings(state):
            pts=[]
            for a in ring:
                segment=arcs[a] if a>=0 else list(reversed(arcs[~a]))
                pts+=segment if not pts else segment[1:]
            d+=path(pts)+'Z'
        paths.append(d)
    coast=''.join(path(arcs[a]) for a,n in counts.items() if n==1)
    borders=''.join(path(arcs[a]) for a,n in counts.items() if n>1)
    svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 370"><title>Contiguous United States with state boundaries</title><desc>U.S. Census Bureau 2017 cartographic boundaries via US Atlas 3.0.1, in an Albers equal-area projection.</desc><rect width="720" height="370" rx="14" fill="#ffffff"/>'
    svg+=''.join('<path d="'+d+'" fill="#faf6ec"/>' for d in paths)
    svg+='<path d="'+borders+'" fill="none" stroke="#b3aec8" stroke-width="0.65" stroke-linejoin="round"/>'
    svg+='<path d="'+coast+'" fill="none" stroke="#6e6986" stroke-width="1.15" stroke-linejoin="round"/></svg>\n'
    OUT.write_text(svg)
    result={'n':N,'c':C,'scale':fit,'translate':[tx,ty]}
    (SOURCE.parent/'projection.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
    for name,lon,lat in [('Mountain View',-122,37),('Dallas',-97,33),('New York City',-74,41),('First position',-120,38),('Second position',-76,40)]:print(name,xy(project(lon,lat)))
    print(OUT)
if __name__=='__main__':main()
