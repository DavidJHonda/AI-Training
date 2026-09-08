"""Approved Support Trap reroll repair. Review output only; no live mutation."""
import sys,json,hashlib,subprocess
from pathlib import Path
import cv2,numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/video'))
import build_work_changes_hybrid as v
FF=v.FFMPEG;at=v.at
AUDIT=ROOT/'video-audit/support-trap-reroll-repair-2026-09-07'
OUT=ROOT/'Prompts/support-trap-reroll-patched.mp4'
SOURCE=ROOT/'Prompts/support-trap-reroll.mp4'
P,B,A,T,R,H='#4f2fc4','#1652f0','#a9760c','#0e8f86','#c41f28','#6e51ff'
BOARDS={'compare':ROOT/'illustrations/support-trap-comparison-v2.jpg',
'role':ROOT/'illustrations/support-trap-real-vs-missing-v2.jpg',
'danger':ROOT/'illustrations/support-trap-danger-v2.jpg'}
CLOSE=ROOT/'lessons/support-trap-4-close.jpg'
chunks=[]
def keep(a,b,board=None,label='native',rect=None,color=H,camera=None,move=0):
    chunks.append(dict(src=0,a=at(a),b=at(b),board=board,label=label,rect=rect,color=color,camera=camera,move=move))
def pause(n,label,board=None):
    chunks.append(dict(src=-1,a=0,b=n,board=board,label=label))
def cam(r):
    x1,y1,x2,y2=r
    return ((x1+x2)/2,(y1+y2)/2,max((x2-x1)*1.13,(y2-y1)*16/9*1.13))
left=(40,271,784,1343);right=(816,271,1560,1343)
keep(0,13.5)
keep(13.5,16.8,'compare','comparison-establish')
keep(16.8,27.0,'compare','sister-acts',left,B,cam(left),24)
keep(27.0,36.8,'compare','chatbot-response',right,A,cam(right),24)
keep(36.8,41.1,'compare','caring-words',(816,974,1560,1082),A,cam(right))
keep(41.1,49.3,'compare','nothing-changed',(816,1212,1560,1322),A,cam(right))
keep(49.3,52.2,'compare','cannot-show-up',(816,1093,1560,1203),A,cam(right))
keep(52.2,62.8,'compare','support-trap-definition',(40,1383,1560,1471),H,None,24)
keep(62.8,65.8,'role','role-establish')
keep(65.8,81.066667,'role','real-help',(40,127,784,717),T)
keep(81.066667,101.966667,None,'grades-and-ordinary-venting')
keep(101.966667,115.6,'role','missing-person',(816,127,1560,717),R)
keep(115.6,120.633333,'role','prepare-not-replace',(40,757,1560,845),H)
keep(120.633333,129.033333,None,'content-note-and-pause')
# Reuse the face-free Harry phone artwork, not an invented portrait/article
# or an apparently verbatim chat excerpt. One continuous restrained push.
keep(129.033333,144.8,'phone','sophie-and-harry')
keep(144.8,150.166667,None,'no-person-alerted')
keep(150.166667,153.5,None,'black-box')
# Remove the complete unsupported "completely invisible" sentence.
keep(159.65,163.65,'room','comfort-does-not-replace-action')
# Remove "Reassurance means nothing..." and its entire visual span.
# Begin the approved board ahead of source's old-graphic transition at 168.433.
keep(168.2,171.9,'danger','danger-establish')
c1=(40,127,525,733);c2=(557,127,1043,733);c3=(1075,127,1560,733)
keep(171.9,184.9,'danger','leave-chat-and-numbers',c1,R,cam(c1),24)
keep(184.9,197.1,'danger','do-it-now',c2,R,cam(c2),24)
keep(197.1,209.5,'danger','tell-anyway',c3,R,cam(c3),24)
keep(209.5,212.2,'danger','safety-outranks-secrecy',(40,773,1560,861),H,None,24)
pause(30,'pause-before-close')
keep(212.9,218.866667,'close','standard-close')
# The close has fixed 48f orientation + 150f push + 30f settled finish.
pause(228-(at(218.866667)-at(212.9)),'closing-settle','close')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    AUDIT.mkdir(parents=True,exist_ok=True);(AUDIT/'qa').mkdir(exist_ok=True)
    protected={str(p):sha(p) for p in [SOURCE,ROOT/'videos/support-trap.mp4',*BOARDS.values(),CLOSE]}
    canvases={k:v.build_canvas(p) for k,p in BOARDS.items()}
    close=cv2.resize(cv2.imread(str(CLOSE)),(1600,900),interpolation=cv2.INTER_AREA)
    needed=set()
    for c in chunks:
        if c['src']==0 and c['board'] is None:needed.update(range(c['a'],c['b']))
    # These single frames are from restrained native artwork, not a course board.
    still_frames={'phone':at(136),'room':at(147)}
    needed.update(still_frames.values())
    native={};cap=cv2.VideoCapture(str(SOURCE))
    assert round(cap.get(cv2.CAP_PROP_FPS))==30
    for f in range(max(needed)+1):
        ok,im=cap.read();assert ok
        if f in needed:
            # Removes only Notebook corner branding, never a stock watermark.
            im=cv2.resize(im[45:675,80:1200],(1280,720),interpolation=cv2.INTER_AREA)
            native[f]=cv2.imencode('.jpg',im,[cv2.IMWRITE_JPEG_QUALITY,98])[1]
    cap.release()
    stills={k:cv2.imdecode(native[f],cv2.IMREAD_COLOR) for k,f in still_frames.items()}
    picture=AUDIT/'picture.mp4'
    encoder=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','-','-an','-c:v','libx264','-pix_fmt','yuv420p','-profile:v','high','-level:v','3.1','-crf','18','-preset','fast','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(picture)],stdin=subprocess.PIPE)
    cursor=0;last=None;prev_board=None;prev_cam=None;prev_focus=None;close_n=0;boundaries={};qa=[]
    for i,c in enumerate(chunks):
        c['output_start']=cursor
        if cursor:boundaries[cursor]=c['label']
        print('chunk',i,c['label'],cursor/30,flush=True)
        focus=None
        if c['board'] in canvases:
            base,ox,oy,full=canvases[c['board']];focus=base
            if c['camera']:
                # Mask unrelated heading/banner fragments while keeping full
                # column geometry intact, including when only a row is ringed.
                target_card=left if c['board']=='compare' and c['camera'][0]<800 else right if c['board']=='compare' else c['rect']
                focus=base.copy()
                focus[:target_card[1]+oy-10]=v.hex_bgr(v.LAVENDER)
                focus[target_card[3]+oy+10:]=v.hex_bgr(v.LAVENDER)
            old_focus=prev_focus if prev_board==c['board'] and prev_focus is not None else base
        for j,f in enumerate(range(c['a'],c['b'])):
            if c['board']=='close':
                t=v.smoothstep(min(1,max(0,(close_n-48)/149)))
                out=v.crop_frame(close,(800,450,1600+(1600/1.2-1600)*t));close_n+=1
            elif c['src']==-1:out=last.copy()
            elif c['board'] in stills:
                t=v.smoothstep(j/max(1,c['b']-c['a']-1))
                out=v.crop_frame(stills[c['board']],(640,360,1280/(1+.035*t)))
            elif c['board']:
                canvas,ox,oy,full=canvases[c['board']]
                target=v.map_camera(c['camera'],ox,oy) if c['camera'] else full
                start=prev_cam if prev_board==c['board'] and prev_cam else full
                camera=target;active=focus
                if c['move'] and j<c['move']:
                    t=v.smoothstep(j/max(1,c['move']-1))
                    camera=tuple(a+(b-a)*t for a,b in zip(start,target))
                    active=cv2.addWeighted(old_focus,1-t,focus,t,0)
                out=v.crop_frame(active,camera)
                if c['rect']:
                    rect=v.project_rect(v.map_rect(c['rect'],ox,oy),camera)
                    v.rounded_ring(out,rect,v.hex_bgr(c['color']),radius=12,thickness=5)
                    if j>=c['move']:
                        assert min(rect[:2])>=24 and rect[2]<=1256 and rect[3]<=696,(c['label'],rect)
            else:out=cv2.imdecode(native[f],cv2.IMREAD_COLOR)
            if j in {0,min(c['b']-c['a']-1,max(35,c.get('move',0)+5)),c['b']-c['a']-1}:
                p=AUDIT/'qa'/f'{cursor:06d}-{c["label"]}.jpg';cv2.imwrite(str(p),out)
                qa.append(dict(frame=cursor,path=str(p),label=c['label']))
            encoder.stdin.write(out.tobytes());cursor+=1;last=out
        if c['board'] in canvases:
            _,ox,oy,full=canvases[c['board']]
            prev_cam=v.map_camera(c['camera'],ox,oy) if c['camera'] else full
            prev_board=c['board'];prev_focus=focus
        elif c['src']!=-1:prev_board=None;prev_cam=None;prev_focus=None
        c['output_end']=cursor
        c['highlight_color']=c.get('color') if c.get('rect') else None
        c['color_source']=('neutral_video_purple' if c.get('color')==H else 'card_locked_accent') if c.get('rect') else 'none'
    encoder.stdin.close();assert encoder.wait()==0
    # Group contiguous original audio, so visual highlight boundaries do not
    # introduce extra audio edits. Edge fades apply only to true edit joins.
    audio=[]
    for c in chunks:
        if audio and c['src']==0 and audio[-1]['src']==0 and audio[-1]['b']==c['a']:
            audio[-1]['b']=c['b']
        else:audio.append({k:c[k] for k in ('src','a','b')})
    graph=[];labels=[]
    for i,c in enumerate(audio):
        d=(c['b']-c['a'])/30
        if c['src']==-1:
            graph.append(f'anullsrc=r=44100:cl=mono,atrim=duration={d:.9f},asetpts=PTS-STARTPTS[a{i}]')
        else:
            graph.append(f'[1:a]atrim=start={c["a"]/30:.9f}:end={c["b"]/30:.9f},asetpts=PTS-STARTPTS,aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,afade=t=in:d=0.005,afade=t=out:st={d-.005:.9f}:d=0.005,apad,atrim=duration={d:.9f}[a{i}]')
        labels.append(f'[a{i}]')
    graph.append(''.join(labels)+f'concat=n={len(audio)}:v=0:a=1[a]')
    subprocess.run([FF,'-y','-v','error','-i',str(picture),'-i',str(SOURCE),'-filter_complex',';'.join(graph),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT)],check=True)
    assert all(sha(p)==h for p,h in protected.items())
    m=dict(output=str(OUT),source=str(SOURCE),frames=cursor,duration=cursor/30,chunks=chunks,audio=audio,boundaries=boundaries,qa=qa,protected=protected,sha256=sha(OUT))
    (AUDIT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    command=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(OUT),'--outdir',str(AUDIT/'transitions')]
    for f,l in boundaries.items():command+=['--boundary',f'{f}:{l}']
    subprocess.run(command,check=False)
    print('COMPLETE',OUT,cursor/30,flush=True)
if __name__=='__main__':main()
