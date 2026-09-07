"""Build owner-approved Support Trap hybrid, never mutate live/lesson."""
import sys,json,hashlib,subprocess
from pathlib import Path
import cv2,numpy as np
ROOT=Path('/Users/davidobrien/Developer/AI-Training')
sys.path.insert(0,str(ROOT/'scripts/video'))
import build_work_changes_hybrid as v
FF=v.FFMPEG; at=v.at
AUDIT=ROOT/'video-audit/support-trap-hybrid-2026-09-07'
OUT=ROOT/'Prompts/support-trap-patched.mp4'
SOURCES=[ROOT/'Prompts/support-trap.mp4',ROOT/'videos/support-trap.mp4']
P,B,A,T,R='#6e51ff','#1652f0','#a9760c','#0e8f86','#c41f28'
BOARDS={'compare':ROOT/'illustrations/support-trap-comparison-v2.jpg','role':ROOT/'illustrations/support-trap-real-vs-missing-v2.jpg','danger':ROOT/'illustrations/support-trap-danger-v2.jpg'}
states=[];chunks=[]
def keep(src,a,b,board=None,label='native',rect=None,color=P,camera=None,move=0):
    chunks.append(dict(src=src,a=at(a),b=at(b),board=board,label=label,rect=rect,color=color,camera=camera,move=move))
def pause(n=18):chunks.append(dict(src=-1,a=0,b=n,label='pause'))
# Preserve native opening; remove its generated definition diagram atomically.
keep(0,0,30.1)
keep(0,30.1,37.766667,'compare','establish')
keep(0,37.766667,47.6,'compare','takeaway',(40,1383,1560,1471),P)
keep(0,47.6,52.45,'role','establish')
keep(1,83.8,88.85,'role','real-relief',(40,127,784,717),T)
keep(0,56.85,70.2,'role','useful-applications',(40,127,784,717),T)
keep(0,70.4,75.5,'role','why-not',(816,127,1560,717),R)
keep(0,82.9,87.9,'role','human-action',(816,127,1560,717),R)
keep(1,115.35,119.15,'role','organize-thoughts',(40,127,784,717),T)
keep(1,119.15,125.2,'role','not-human-care',(816,127,1560,717),R)
# Content warning retained, with only the warning artwork underneath.
keep(0,96.633333,100.8,None,'warning')
pause(15)
# Start after the dangling "that same year". The live footage adds age,
# duration, inability to alert people, death, mother, and the black-box account.
keep(1,150.7,157.9,None,'sophie-introduction')
keep(0,108.0,112.43,None,'harry')
keep(1,168.45,184.6,None,'sophie-consequence')
pause(18)
keep(0,128.8,130.65,'danger','establish')
# Dense three-card board: complete card framing derived from outer geometry.
first=(40,127,525,733);second=(557,127,1043,733);third=(1075,127,1560,733)
def cam(rect):
    x1,y1,x2,y2=rect
    return ((x1+x2)/2,(y1+y2)/2,max((x2-x1)*1.12,(y2-y1)*16/9*1.12))
keep(1,197.55,202.15,'danger','leave-chat',first,R,cam(first),30)
keep(1,202.3,204.75,'danger','not-another-message',first,R,cam(first))
keep(0,136.45,138.2,'danger','involve-adult',first,R,cam(first))
keep(0,138.2,141.05,'danger','crisis-and-emergency-numbers',first,R,cam(first))
keep(0,141.7,145.65,'danger','do-it-now',second,R,cam(second),30)
keep(0,146.25,147.7,'danger','tell-anyway',third,R,cam(third),30)
keep(1,205.0,220.75,'danger','help-friend-and-break-secrecy',third,R,cam(third))
pause(30)
keep(0,150.0,158.8,'close','standard-close')

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    AUDIT.mkdir(parents=True,exist_ok=True);(AUDIT/'qa').mkdir(exist_ok=True)
    protected={str(p):sha(p) for p in SOURCES+list(BOARDS.values())+[ROOT/'lessons/support-trap-4-close.jpg']}
    canvases={k:v.build_canvas(p) for k,p in BOARDS.items()}
    close=cv2.resize(cv2.imread(str(ROOT/'lessons/support-trap-4-close.jpg')),(1600,900),interpolation=cv2.INTER_AREA)
    picture=AUDIT/'picture.mp4'
    encoder=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','-','-an','-c:v','libx264','-pix_fmt','yuv420p','-profile:v','high','-level:v','3.1','-crf','18','-preset','fast',str(picture)],stdin=subprocess.PIPE)
    # Sequential decode and cache only needed source frames: supports donor
    # passages reused in a new teaching order without unreliable time seeking.
    needed=[set(),set()]
    for c in chunks:
        if c['src']>=0 and c['board'] is None:needed[c['src']].update(range(c['a'],c['b']))
    native={}
    for src in (0,1):
        cap=cv2.VideoCapture(str(SOURCES[src]));fps=cap.get(cv2.CAP_PROP_FPS);assert round(fps)==30
        for f in range(max(needed[src])+1):
            ok,im=cap.read();assert ok
            if f in needed[src]:
                # Restrained native-art crop removes only the Notebook corner
                # branding, not a stock watermark; teaching boards are replaced.
                resized=cv2.resize(im[45:675,80:1200],(1280,720),interpolation=cv2.INTER_AREA)
                native[(src,f)]=cv2.imencode('.jpg',resized,[cv2.IMWRITE_JPEG_QUALITY,98])[1]
        cap.release()
    cursor=0;last=None;prev_board=None;prev_cam=None;boundaries={};qa=[]
    for i,c in enumerate(chunks):
        c['output_start']=cursor
        if cursor:boundaries[cursor]=c['label']
        print('chunk',i,c['label'],cursor/30,flush=True)
        for j,f in enumerate(range(c['a'],c['b'])):
            if c['src']==-1:out=last.copy()
            elif c['board']=='close':
                width=1600 if j<48 else 1600+(1600/1.2-1600)*v.smoothstep(min(1,(j-48)/149))
                out=v.crop_frame(close,(800,450,width))
            elif c['board']:
                canvas,ox,oy,full=canvases[c['board']]
                target=v.map_camera(c['camera'],ox,oy) if c['camera'] else full
                start=prev_cam if prev_board==c['board'] and prev_cam else full
                camera=target
                if c['move'] and j<c['move']:
                    t=v.smoothstep(j/max(1,c['move']-1));camera=tuple(a+(b-a)*t for a,b in zip(start,target))
                out=v.crop_frame(canvas,camera)
                if c['rect']:
                    rect=v.project_rect(v.map_rect(c['rect'],ox,oy),camera)
                    v.rounded_ring(out,rect,v.hex_bgr(c['color']),radius=16,thickness=5)
            else:
                # Picture edit is independent of audio: suppress four residual
                # article frames before the Harry shot begins at source 108.133.
                picture_f=max(f,3244) if c['label']=='harry' else f
                out=cv2.imdecode(native[(c['src'],picture_f)],cv2.IMREAD_COLOR)
            if j==min(c['b']-c['a']-1,max(35,c.get('move',0)+5)) or (c.get('board')=='close' and j==c['b']-c['a']-1):
                path=AUDIT/'qa'/f'{cursor:06d}-{c["label"]}.jpg';cv2.imwrite(str(path),out);qa.append(dict(frame=cursor,path=str(path),label=c['label']))
            encoder.stdin.write(out.tobytes());cursor+=1;last=out
        if c.get('board') in canvases:
            _,ox,oy,full=canvases[c['board']];prev_cam=v.map_camera(c['camera'],ox,oy) if c['camera'] else full;prev_board=c['board']
        elif c['src']!=-1:prev_board=None;prev_cam=None
        c['output_end']=cursor
        c['highlight_color']=c.get('color') if c.get('rect') else None
        c['color_source']=('neutral_video_purple' if c.get('color')==P else 'card_locked_accent') if c.get('rect') else 'none'
    encoder.stdin.close();assert encoder.wait()==0
    graph=[];labels=[]
    for i,c in enumerate(chunks):
        d=(c['b']-c['a'])/30
        if c['src']==-1:graph.append(f'anullsrc=r=44100:cl=mono,atrim=duration={d},asetpts=PTS-STARTPTS[a{i}]')
        else:graph.append(f'[{c["src"]+1}:a]atrim=start={c["a"]/30:.9f}:end={c["b"]/30:.9f},asetpts=PTS-STARTPTS,aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,afade=t=in:d=0.003,afade=t=out:st={d-.003:.9f}:d=0.003,apad,atrim=duration={d:.9f}[a{i}]')
        labels.append(f'[a{i}]')
    graph.append(''.join(labels)+f'concat=n={len(chunks)}:v=0:a=1[a]')
    subprocess.run([FF,'-y','-v','error','-i',str(picture),'-i',str(SOURCES[0]),'-i',str(SOURCES[1]),'-filter_complex',';'.join(graph),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT)],check=True)
    assert all(sha(p)==h for p,h in protected.items())
    manifest=dict(output=str(OUT),frames=cursor,duration=cursor/30,chunks=chunks,boundaries=boundaries,qa=qa,protected=protected,sha256=sha(OUT))
    (AUDIT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(OUT),'--outdir',str(AUDIT/'transitions')]
    for f,l in boundaries.items():cmd+=['--boundary',f'{f}:{l}']
    subprocess.run(cmd,check=False)
    print('COMPLETE',OUT,cursor/30,flush=True)
if __name__=='__main__':main()
