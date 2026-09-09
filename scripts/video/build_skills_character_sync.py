"""Replace approved Build Your Skills art only; freeze narration and shot timing.

Full-card rails are measured on installed art, not copied from old inset rings.
Original graphic cutaways and approved camera/highlight onsets are retained.
No live video, lesson image, or index writes. Review candidates only.
"""
from pathlib import Path
import sys,json,subprocess,concurrent.futures
import cv2,numpy as np
R=Path('/Users/davidobrien/Developer/AI-Training');sys.path.insert(0,str(R/'scripts/video'))
import build_avoid_illustration_sync as base
import build_work_changes_hybrid as v
A=R/'video-audit/build-skills-illustration-sync-2026-09-09'
base.BASE=A;base.AUDIT=A/'build';base.REVISION=''
def state(frame,label,rect=None,color='#6e51ff',camera=None,move=0):
    d=base.state(frame,label,rect,color,None,move);d['camera']=camera;return d
def groups():
    result=[]
    for slug in ['honesty-and-privacy','people-skills','make-your-move']:
        m=json.loads((A/slug/'scan.json').read_text())
        g=dict(slug=slug,baseline=m['video'],baseline_sha=m['live_sha256'],frames=m['frames'],legs=[])
        assets={x['slug']:x for x in m['assets']}
        def leg(key,start,end,states):
            e=assets[key];g['legs'].append(dict(asset=e['asset'],asset_sha=e['asset_sha256'],start=start,end=end,states=states))
        if slug=='honesty-and-privacy':
            asset=assets['honesty-allowed']['asset']
            # Rails are the illustration edges, vertical span includes each
            # complete step underneath, with clearance from its final text line.
            leg('honesty-allowed',1962,2448,[state(1962,'full-flow'),
                state(2010,'understand',(84,184,542,755),'#4f2fc4'),
                state(2112,'process',(624,184,1082,755),'#1652f0'),
                state(2196,'role',(1164,184,1622,755),'#0e8f86'),
                state(2286,'accountability'),state(2352,'full-takeaway',base.gold_bounds(asset))])
        elif slug=='people-skills':
            # Measured photo/body outer rails. Preserve the shipped four-card
            # camera walk, scaling it to the new export's resolution.
            cards=[(34,106,660,604),(691,106,1317,604),(34,631,660,1130),(691,631,1317,1130)]
            points=[2282,2617,3008,3340];names=['listen','notice','matter','challenge'];colors=['#4f2fc4','#1652f0','#0e8f86','#a9760c']
            states=[state(1964,'full-practice')]
            for f,name,c,color in zip(points,names,cards,colors):
                states.append(state(f,name,c,color,((c[0]+c[2])/2,(c[1]+c[3])/2,950),24))
            states.append(state(3665,'summary',move=30));leg('people-skills-four-ways',1964,3860,states)
        else:
            old=json.loads((R/'video-audit/make-your-move-2-review/edit-manifest.json').read_text())
            cuts=old['source_frame_cuts']
            def mapped(f):return f-sum(max(0,min(f,b)-a) for a,b in cuts)
            keymap={'note':'make-your-move-note','a':'make-your-move-careers-1','b':'make-your-move-careers-2'}
            cards={'a':[(39,127,524,942),(559,127,1042,942),(1077,127,1562,942)],'b':[(38,127,525,944),(558,127,1044,944),(1077,127,1563,944)]}
            images={k:cv2.imread(assets[keymap[k]]['asset']) for k in ['a','b']}
            # Heading plus complete paragraph with balanced vertical clearance.
            # Never derive horizontal rails from text extents.
            def section(k,col,top,bottom):
                x1,_,x2,_=cards[k][col];roi=images[k][top:bottom,x1+24:x2-24]
                rows=np.flatnonzero(np.count_nonzero(np.min(roi,axis=2)<180,axis=1)>3);assert len(rows)>10
                return (x1,top+int(rows[0])-18,x2,top+int(rows[-1])+18)
            for s in old['states']:
                k=s['board']
                if k not in keymap:continue
                a,z=mapped(s['start']),mapped(s['end']);rect=None;camera=None
                if s['camera']:
                    col=int(np.argmin([abs((c[0]+c[2])/2-s['camera'][0]) for c in cards[k]]));c=cards[k][col]
                    camera=((c[0]+c[2])/2,(c[1]+c[3])/2,1512)
                    if s['rect']:
                        rect=section(k,col,490,680) if s['label'].endswith('-ai') else section(k,col,695,934) if s['label'].endswith('-people') else c
                st=state(a,s['label'],rect,s['color'] or '#6e51ff',camera,s['move'])
                if g['legs'] and g['legs'][-1]['end']==a and g['legs'][-1]['asset']==assets[keymap[k]]['asset']:
                    g['legs'][-1]['end']=z;g['legs'][-1]['states'].append(st)
                else:leg(keymap[k],a,z,[st])
        result.append(g)
    return result
def render(leg,path,audit):
    states=leg['states'];qa=[];n=0;canvas,ox,oy,full=v.build_canvas(Path(leg['asset']));previous=full
    process=subprocess.Popen([base.FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','-','-an','-c:v','ffv1','-level','3','-threads','2',str(path)],stdin=subprocess.PIPE)
    for j,s in enumerate(states):
        end=states[j+1]['frame'] if j+1<len(states) else leg['end'];target=v.map_camera(s['camera'],ox,oy) if s['camera'] else full
        for f in range(s['frame'],end):
            k=f-s['frame'];c=target
            if s['move'] and k<s['move']:
                t=v.smoothstep(k/max(1,s['move']-1));c=tuple(a+(b-a)*t for a,b in zip(previous,target))
            out=v.crop_frame(canvas,c)
            if s['rect']:
                rect=v.project_rect(v.map_rect(s['rect'],ox,oy),c);v.rounded_ring(out,rect,v.hex_bgr(s['color']),radius=12,thickness=5)
                if k>=s['move']:assert min(rect[:2])>=12 and rect[2]<=1268 and rect[3]<=708,(s,rect)
            if k in {0,min(end-s['frame']-1,max(35,s['move']+5)),end-s['frame']-1}:
                p=audit/'states'/f'{f:06d}-{s["label"]}.jpg';cv2.imwrite(str(p),out);qa.append(dict(frame=f,path=str(p),label=s['label']))
            process.stdin.write(out.tobytes());n+=1
        previous=target
    process.stdin.close();assert process.wait()==0 and n==leg['end']-leg['start'];return qa
def previews(g):
    d=A/'previews';d.mkdir(exist_ok=True)
    for group in g:
        for leg in group['legs']:
            canvas,ox,oy,full=v.build_canvas(Path(leg['asset']))
            for s in leg['states']:
                c=v.map_camera(s['camera'],ox,oy) if s['camera'] else full;out=v.crop_frame(canvas,c)
                if s['rect']:
                    rect=v.project_rect(v.map_rect(s['rect'],ox,oy),c);v.rounded_ring(out,rect,v.hex_bgr(s['color']),radius=12,thickness=5)
                    assert min(rect[:2])>=12 and rect[2]<=1268 and rect[3]<=708,(s,rect)
                cv2.imwrite(str(d/f'{group["slug"]}-{s["frame"]:06d}-{s["label"]}.jpg'),out)
def main():
    cv2.setNumThreads(1);base.render_leg=render;g=groups();base.AUDIT.mkdir(exist_ok=True)
    (A/'replacement-plan.json').write_text(json.dumps(g,indent=2)+'\n');previews(g)
    if '--previews' in sys.argv:return
    if len(sys.argv)>1:g=[x for x in g if x['slug'] in sys.argv[1:]]
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:r=list(pool.map(base.encode,g))
    (base.AUDIT/'results.json').write_text(json.dumps(r,indent=2)+'\n')
if __name__=='__main__':main()
