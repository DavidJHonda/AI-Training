import sys,json,hashlib,subprocess
from pathlib import Path
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path('/Users/davidobrien/Developer/AI-Training')
sys.path.insert(0,str(ROOT/'scripts/video'))
import build_work_changes_hybrid as v
FF=v.FFMPEG;at=v.at
AUDIT=ROOT/'video-audit/fake-trap-repair-2026-09-07'
OUT=ROOT/'Prompts/fake-trap-patched.mp4'
SOURCES=[ROOT/'Prompts/fake-trap.mp4',ROOT/'videos/fake-trap.mp4']
P,B,A,T,R='#4f2fc4','#1652f0','#a9760c','#0e8f86','#c41f28'
BOARDS={'compare':ROOT/'illustrations/fake-trap-comparison-v2.jpg','motives':ROOT/'illustrations/fake-trap-four-reasons-v3.png','source':ROOT/'illustrations/fake-trap-source-v2.jpg','checks':ROOT/'illustrations/fake-trap-three-checks-v2.jpg'}
HOCKEY=AUDIT/'assets/hockey-celebration.png'
CLOSE=ROOT/'lessons/fake-trap-5-close.jpg'
chunks=[]
def keep(src,a,b,board=None,label='native',rect=None,color=P,camera=None,move=0):
    chunks.append(dict(src=src,a=at(a),b=at(b),board=board,label=label,rect=rect,color=color,camera=camera,move=move))
def pause(n=30):chunks.append(dict(src=-1,a=0,b=n,label='transition-pause'))
def cam(r):
    x1,y1,x2,y2=r
    return ((x1+x2)/2,(y1+y2)/2,max((x2-x1)*1.12,(y2-y1)*16/9*1.12))
# Source-time edit decisions; video coverage is deliberately independent of words.
keep(0,0,13.4)
keep(0,13.4,19.1,'compare','comparison-establish')
left=(40,271,784,1302);right=(816,271,1560,1302)
keep(0,19.1,30.5,'compare','appearance-test',left,A,cam(left),24)
keep(0,30.5,43.2,'compare','source-trail-test',right,B,cam(right),24)
keep(0,43.2,58.7,None,'two-jaws-definition')
# Discard 59.32–68.46, not the harmless-fake qualification.
keep(0,68.95,74.45,None,'harmless-context')
keep(0,74.45,83.55,'hockey','original-hockey-joke')
keep(0,83.55,92.4,'motives','motives-establish')
# Measured current v3 PNG coordinates, not the legacy 1600px export.
money=(35,105,652,565);power=(678,105,1294,565)
fame=(35,591,652,1051);cruelty=(678,591,1294,1051)
keep(0,92.4,96.5,'motives','money',money,P,cam(money),18)
keep(0,96.5,100.4,'motives','power',power,B,cam(power),18)
keep(0,100.4,104.15,'motives','fame',fame,A,cam(fame),18)
keep(0,104.15,107.7,'motives','cruelty',cruelty,R,cam(cruelty),18)
keep(0,107.7,128.6,None,'detector-is-a-clue')
# Discard 129.24–138.26 categorical algorithm language.
keep(0,138.65,159.4,'source','emotion-stop-source-trail')
keep(0,159.4,162.25,'checks','checks-establish')
c1=(40,127,525,651);c2=(557,127,1043,651);c3=(1075,127,1560,651)
keep(0,162.25,166.5,'checks','source-check',c1,P,cam(c1),20)
keep(0,166.5,171.65,'checks','context-check',c2,B,cam(c2),20)
keep(0,171.65,176.85,'checks','corroboration-check',c3,T,cam(c3),20)
keep(0,176.85,180.5,'checks','independent-verification-banner',(40,691,1560,779),A,None,20)
# Complete donor sentence replaces unsafe, unspecific "call back".
keep(1,195.55,205.85,None,'trusted-number-donor')
keep(0,184.15,188.866667,'checks','verify-viral-video',c3,T,None,0)
keep(0,188.866667,236.0,None,'unverified-and-targeted-help')
# Remove redundant final paragraph, preserve reassurance and full one-second pause.
pause(30)
keep(0,245.0,249.97,'close','standard-close')
pause(18)
chunks[-1]['label']='closing-hold'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    AUDIT.mkdir(parents=True,exist_ok=True);(AUDIT/'qa').mkdir(exist_ok=True)
    protected={str(p):sha(p) for p in SOURCES+list(BOARDS.values())+[CLOSE]}
    canvases={k:v.build_canvas(p) for k,p in BOARDS.items()}
    close=cv2.resize(cv2.imread(str(CLOSE)),(1600,900),interpolation=cv2.INTER_AREA)
    hockey,hox,hoy,hfull=v.build_canvas(HOCKEY)
    picture=AUDIT/'picture.mp4'
    encoder=subprocess.Popen([FF,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','-','-an','-c:v','libx264','-pix_fmt','yuv420p','-profile:v','high','-level:v','3.1','-crf','18','-preset','fast','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',str(picture)],stdin=subprocess.PIPE)
    needed=[set(),set()]
    for c in chunks:
        if c['src']>=0 and c['board'] is None:needed[c['src']].update(range(c['a'],c['b']))
    native={}
    for src in (0,1):
        if not needed[src]:continue
        cap=cv2.VideoCapture(str(SOURCES[src]));assert round(cap.get(cv2.CAP_PROP_FPS))==30
        for f in range(max(needed[src])+1):
            ok,im=cap.read();assert ok
            if f in needed[src]:
                resized=cv2.resize(im[45:675,80:1200],(1280,720),interpolation=cv2.INTER_AREA)
                native[(src,f)]=cv2.imencode('.jpg',resized,[cv2.IMWRITE_JPEG_QUALITY,98])[1]
        cap.release()
    cursor=0;last=None;prev_board=None;prev_cam=None;prev_focus=None;boundaries={};qa=[]
    for i,c in enumerate(chunks):
        c['output_start']=cursor
        if cursor:boundaries[cursor]=c['label']
        print('chunk',i,c['label'],cursor/30,flush=True)
        focus=None;old_focus=None
        if c.get('board') in canvases:
            base,ox,oy,full=canvases[c['board']]
            focus=base
            if c['camera'] and c['rect']:
                # Remove unrelated header/footer fragments from zoom margins.
                # Whole-card horizontal rails and neighbouring columns remain.
                focus=base.copy();top=c['rect'][1]+oy-10;bottom=c['rect'][3]+oy+10
                focus[:top]=v.hex_bgr(v.LAVENDER);focus[bottom:]=v.hex_bgr(v.LAVENDER)
            old_focus=prev_focus if prev_board==c['board'] and prev_focus is not None else base
        for j,f in enumerate(range(c['a'],c['b'])):
            if c['src']==-1:out=last.copy()
            elif c['board']=='close':
                t=v.smoothstep(min(1,max(0,(j-24)/90)))
                out=v.crop_frame(close,(800,450,1600+(1600/1.2-1600)*t))
            elif c['board']=='hockey':
                # Subtle 4% push preserves the complete trophy and all four faces.
                t=v.smoothstep(j/(c['b']-c['a']-1));out=v.crop_frame(hockey,(hfull[0],hfull[1],hfull[2]/(1+.025*t)))
            elif c['board']:
                canvas,ox,oy,full=canvases[c['board']]
                target=v.map_camera(c['camera'],ox,oy) if c['camera'] else full
                start=prev_cam if prev_board==c['board'] and prev_cam else full
                camera=target
                if c['move'] and j<c['move']:
                    t=v.smoothstep(j/max(1,c['move']-1));camera=tuple(a+(b-a)*t for a,b in zip(start,target))
                if c['board']=='source':
                    t=v.smoothstep(j/max(1,c['b']-c['a']-1));camera=(full[0],full[1],full[2]/(1+.035*t))
                active=focus
                if c['move'] and j<c['move']:
                    active=cv2.addWeighted(old_focus,1-t,focus,t,0)
                out=v.crop_frame(active,camera)
                if c['rect']:
                    rect=v.project_rect(v.map_rect(c['rect'],ox,oy),camera)
                    v.rounded_ring(out,rect,v.hex_bgr(c['color']),radius=12,thickness=5)
                    if j>=c['move']:
                        assert min(rect[:2])>=3 and rect[2]<=1277 and rect[3]<=717,(c['label'],rect)
            else:
                pf=f
                # The resumed audio starts in a pause before the new picture.
                # Freeze its first clean frame over the discarded polygraph tail.
                if c['label']=='harmless-context':pf=max(f,at(69.3))
                if c['label']=='detector-is-a-clue':pf=max(f,at(108.5))
                out=cv2.imdecode(native[(c['src'],pf)],cv2.IMREAD_COLOR)
            if j in {0,min(c['b']-c['a']-1,max(35,c.get('move',0)+5)),c['b']-c['a']-1}:
                path=AUDIT/'qa'/f'{cursor:06d}-{c["label"]}.jpg';cv2.imwrite(str(path),out);qa.append(dict(frame=cursor,path=str(path),label=c['label']))
            encoder.stdin.write(out.tobytes());cursor+=1;last=out
        if c.get('board') in canvases:
            _,ox,oy,full=canvases[c['board']];prev_cam=v.map_camera(c['camera'],ox,oy) if c['camera'] else full;prev_board=c['board'];prev_focus=focus
        elif c['src']!=-1:prev_board=None;prev_cam=None;prev_focus=None
        c['output_end']=cursor
        c['highlight_color']=c.get('color') if c.get('rect') else None
        c['color_source']='current-card-or-banner-accent' if c.get('rect') else 'none'
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
