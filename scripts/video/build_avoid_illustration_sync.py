"""Illustration-only retrofit of frozen shipped baselines; no live/lesson writes.

Each full candidate is a single-pass concat from the approved baseline and
lossless replacement legs (RETROFIT-PLAYBOOK section 4), never another candidate.
Approved audio is packet-copied unchanged. Review reels are disposable previews.
"""
from pathlib import Path
import sys,json,hashlib,subprocess,concurrent.futures,argparse
import cv2,numpy as np
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'scripts/video'))
import build_work_changes_hybrid as v
FF=v.FFMPEG; FPS=30
BASE=R/'video-audit/avoid-traps-illustration-sync-2026-09-08'
AUDIT=BASE/'batch'
REVISION=''
P,B,T,A,H='#4f2fc4','#1652f0','#0e8f86','#a9760c','#6e51ff'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def state(frame,label,rect=None,color=H,focus=None,move=0):
    return dict(frame=frame,label=label,rect=rect,color=color,focus=focus,move=move,
                color_source='none' if rect is None else 'neutral_video_purple' if color==H else 'card_locked_accent')
def gold_bounds(asset):
    im=cv2.imread(str(asset));h,w=im.shape[:2]
    hsv=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
    mask=cv2.inRange(hsv,np.array([15,45,170]),np.array([40,255,255]));mask[:int(h*.82)]=0
    _,_,stats,_=cv2.connectedComponentsWithStats(mask)
    choices=[s for s in stats[1:] if s[2]>.8*w and s[3]>20]
    assert choices,asset
    x,y,rw,rh,area=max(choices,key=lambda s:s[4]);return tuple(map(int,(x,y,x+rw-1,y+rh-1)))

def specs():
    entries=json.loads((BASE/'replacement-map.json').read_text());groups={}
    for e in entries:
        slug=Path(e['video']).stem
        if slug=='support-trap':continue
        g=groups.setdefault(slug,dict(slug=slug,baseline=e['video'],baseline_sha=e['live_sha256'],frames=e['frames'],legs=[]))
        asset=Path(e['asset']);assert sha(asset)==e['asset_sha256']
        for a,z in e['spans']:
            states=[state(a,'full-illustration')]
            if slug=='hallucination':states+=[state(3847,'full-takeaway',gold_bounds(asset))]
            if slug=='training-bias':states+=[state(711,'full-takeaway',gold_bounds(asset))]
            if slug=='document-trap':states+=[state(1806,'full-takeaway',gold_bounds(asset))]
            if slug=='mind-trap':
                left=(33,225,652,1150);right=(677,225,1296,1150)
                if a==739:states+=[state(810,'chatbot-answer',right,A,right,24)]
                else:states+=[state(1263,'mom-answer',left,B,left,24),state(1388,'mom-notices',(33,943,652,1036),B,left),state(1568,'mom-shares-stake',(33,1043,652,1137),B,left),state(1686,'compare-both',None,H,None,24)]
            if slug=='flattery-trap':
                left=(31,302,618,1115);right=(643,302,1230,1115)
                scenario=(31,90,1230,276)
                states+=[state(984,'essay',scenario,P,None,0),state(1275,'flattery-response',(31,678,618,818),A,left,30),state(1431,'praised',(31,826,618,909),A,left),state(1563,'false-praise-result',(31,1012,618,1094),A,left),state(1788,'useful-heading-and-response',(643,678,1230,814),B,right,30),state(1887,'missing-thesis',(643,918,1230,1005),B,right),state(2010,'full-takeaway',gold_bounds(asset),H,None,24)]
            if slug=='fake-trap' and 'comparison' in asset.name:
                left=(33,221,590,1162);right=(615,221,1174,1162)
                states=[state(a,'scenario',(33,95,1174,193),P),state(573,'appearance-test',left,A,left,24),state(915,'source-trail-test',right,B,right,24)]
            g['legs'].append(dict(asset=str(asset),asset_sha=sha(asset),start=a,end=z,states=states,push=.035 if slug=='fake-trap' and 'source' in asset.name else 0))
    return groups

def camera_for(rect):
    x1,y1,x2,y2=rect
    return ((x1+x2)/2,(y1+y2)/2,max((x2-x1)*1.12,(y2-y1)*16/9*1.12))

def render_leg(leg,path,audit):
    canvas,ox,oy,full=v.build_canvas(Path(leg['asset']));states=leg['states'];n=0;prev_cam=full;prev_focus=canvas
    cmd=[FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','-','-an','-c:v','ffv1','-level','3','-threads','2',str(path)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    qa=[]
    for j,s in enumerate(states):
        end=states[j+1]['frame'] if j+1<len(states) else leg['end'];duration=end-s['frame'];assert duration>0
        target=v.map_camera(camera_for(s['focus']),ox,oy) if s['focus'] else full
        active=canvas
        if s['focus']:
            active=canvas.copy();active[:s['focus'][1]+oy-8]=v.hex_bgr(v.LAVENDER);active[s['focus'][3]+oy+8:]=v.hex_bgr(v.LAVENDER)
        for k in range(duration):
            c=target;im=active
            if s['move'] and k<s['move']:
                t=v.smoothstep(k/max(1,s['move']-1));c=tuple(a+(b-a)*t for a,b in zip(prev_cam,target));im=cv2.addWeighted(prev_focus,1-t,active,t,0)
            if leg.get('push'):
                t=v.smoothstep((s['frame']-leg['start']+k)/max(1,leg['end']-leg['start']-1));c=(c[0],c[1],c[2]/(1+leg['push']*t))
            out=v.crop_frame(im,c)
            if s['rect']:
                rect=v.project_rect(v.map_rect(s['rect'],ox,oy),c)
                v.rounded_ring(out,rect,v.hex_bgr(s['color']),radius=12,thickness=5)
                if k>=s['move']:assert min(rect[:2])>=15 and rect[2]<=1265 and rect[3]<=705,(s,rect)
            if k in {0,min(duration-1,max(35,s['move']+5)),duration-1}:
                f=s['frame']+k;p=audit/'states'/f'{f:06d}-{s["label"]}.jpg';cv2.imwrite(str(p),out);qa.append(dict(frame=f,path=str(p),label=s['label']))
            process.stdin.write(out.tobytes());n+=1
        prev_cam=target;prev_focus=active
    process.stdin.close();assert process.wait()==0;assert n==leg['end']-leg['start']
    return qa

def payload_hash(path,which='a'):
    data=subprocess.check_output([FF,'-v','error','-i',str(path),'-map',f'0:{which}','-c','copy','-f','data','-']);return hashlib.sha256(data).hexdigest()

def encode(g):
    slug=g['slug'];a=AUDIT/slug;a.mkdir(parents=True,exist_ok=False);(a/'states').mkdir()
    baseline=Path(g['baseline']);assert sha(baseline)==g['baseline_sha']
    candidate=R/'Prompts'/f'{slug}-illustrations-patched{REVISION}.mp4';assert not candidate.exists()
    print('RENDER',slug,flush=True);legs=[];qa=[];bounds={}
    for i,leg in enumerate(g['legs']):
        path=a/f'leg-{i}.mkv';qa+=render_leg(leg,path,a);legs.append(path)
        bounds[leg['start']]='illustration-start';bounds[leg['end']]='illustration-end'
        for s in leg['states'][1:]:bounds[s['frame']]=s['label']
    graph=[];labels=[];cursor=0
    def native(start,end):
        if end<=start:return
        name=f'p{len(labels)}';graph.append(f'[0:v]trim=start_frame={start}:end_frame={end},setpts=N/(30*TB),setsar=1[{name}]');labels.append(f'[{name}]')
    for i,leg in enumerate(g['legs'],1):
        native(cursor,leg['start']);name=f'p{len(labels)}'
        graph.append(f'[{i}:v]setpts=N/(30*TB),setsar=1,format=yuv420p[{name}]');labels.append(f'[{name}]');cursor=leg['end']
    native(cursor,g['frames']);graph.append(''.join(labels)+f'concat=n={len(labels)}:v=1:a=0,setpts=N/(30*TB),format=yuv420p[v]')
    cmd=[FF,'-v','error','-threads','2','-i',str(baseline)]
    for leg in legs:cmd+=['-i',str(leg)]
    cmd+=['-filter_complex_threads','2','-filter_complex',';'.join(graph),'-map','[v]','-map','0:a','-c:v','libx264','-profile:v','high','-level:v','3.1','-crf','16','-preset','fast','-threads','2','-pix_fmt','yuv420p','-r','30','-c:a','copy','-movflags','+faststart',str(candidate)]
    subprocess.run(cmd,check=True)
    assert payload_hash(baseline)==payload_hash(candidate)
    cap=cv2.VideoCapture(str(candidate));n=0
    while cap.grab():n+=1
    fps=cap.get(cv2.CAP_PROP_FPS);cap.release();assert n==g['frames'] and fps==30,(slug,n,g['frames'],fps)
    assert sha(baseline)==g['baseline_sha'] and all(sha(x['asset'])==x['asset_sha'] for x in g['legs'])
    # Short reels have two seconds of context on both sides, preserving the
    # approved gaps where adjacent windows overlap.
    windows=[]
    for leg in g['legs']:
        start=max(0,leg['start']-60);end=min(n,leg['end']+60)
        if windows and start<=windows[-1][1]:windows[-1][1]=max(end,windows[-1][1])
        else:windows.append([start,end])
    reel=R/'Prompts'/f'{slug}-illustrations-review-reel{REVISION}.mp4';assert not reel.exists()
    graph=[];labels=[];timeline=[];reel_cursor=0
    for i,(start,end) in enumerate(windows):
        graph += [f'[0:v]trim=start_frame={start}:end_frame={end},setpts=N/(30*TB)[v{i}]',f'[0:a]atrim=start={start/30:.9f}:end={end/30:.9f},asetpts=PTS-STARTPTS[a{i}]'];labels +=[f'[v{i}][a{i}]'];timeline.append(dict(reel_start=reel_cursor/30,full_start=start/30,full_end=end/30));reel_cursor+=end-start
    graph.append(''.join(labels)+f'concat=n={len(windows)}:v=1:a=1[v][a]')
    subprocess.run([FF,'-v','error','-i',str(candidate),'-filter_complex_threads','2','-filter_complex',';'.join(graph),'-map','[v]','-map','[a]','-c:v','libx264','-crf','18','-preset','fast','-threads','2','-c:a','aac','-b:a','192k','-movflags','+faststart',str(reel)],check=True)
    result={**g,'candidate':str(candidate),'candidate_sha256':sha(candidate),'qa':qa,'boundaries':bounds,'audio_packets_identical':True,'audio_payload_sha256':payload_hash(candidate),'decoded_frames':n,'fps':fps,'review_reel':str(reel),'reel_timeline':timeline,'reel_duration':reel_cursor/30,'baseline_and_assets_unchanged':True}
    (a/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    cmd=[sys.executable,str(R/'scripts/video/transition_guard.py'),str(candidate),'--outdir',str(a/'transitions')]
    for f,label in bounds.items():cmd+=['--boundary',f'{f}:{label}']
    ret=subprocess.run(cmd);print('COMPLETE',slug,'frames',n,'audio identical','guard',ret.returncode,flush=True)
    return result

def main():
    global AUDIT,REVISION
    p=argparse.ArgumentParser();p.add_argument('--slugs',nargs='*');p.add_argument('--revision',choices=['base','v2','v3'],default='base');args=p.parse_args()
    REVISION='-'+args.revision if args.revision!='base' else '';AUDIT=BASE/('batch'+REVISION);groups=specs()
    if args.slugs:groups={k:groups[k] for k in args.slugs}
    AUDIT.mkdir(parents=True,exist_ok=True)
    (AUDIT/'batch-plan.json').write_text(json.dumps(list(groups.values()),indent=2)+'\n')
    cv2.setNumThreads(1)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        result=list(pool.map(encode,groups.values()))
    (AUDIT/'batch-results.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
