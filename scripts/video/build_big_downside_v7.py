#!/usr/bin/env python3
"""October three-idea review candidate. User: 'Build it'. Never installs/publishes."""
from pathlib import Path
import json, subprocess, sys, hashlib
import cv2
import numpy as np
import imageio_ffmpeg
from editspec_build import Build, Reader, sha, fr, readwav, writewav, SPF, SR
from build_creative_thinking_v8 import BoardRenderer
from gemini_mark import clean_frame, glyph_mask
from make_close_board import compose_canonical_for_video, close_board_asset
from ken_burns_path import smoothstep

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/big-downside-build-2026-10-09-v7'
DEST=ROOT/'Prompts/big-downside-v7.mp4'
SRC={n:ROOT/f'Prompts/big-downside-{n}.mp4' for n in ['1','2','3','v6']}
A=ROOT/'course-assets/big-downside'
FF=imageio_ffmpeg.get_ffmpeg_exe()
ROWS=[]

def lesson_signature(text):
    start=text.index('function BigDownsideSection(')
    end=text.find('\nfunction ',start+10)
    body=text[start:end if end>=0 else len(text)]
    refs='\n'.join(x for x in text.splitlines() if 'bigdownside:' in x)
    return hashlib.sha256((body+'\n'+refs).encode()).hexdigest()

def row(n,a,z,label,visual='source',pic=None,ps=None,pe=None):
    s,e=fr(a),fr(z); cursor=ROWS[-1]['end_frame'] if ROWS else 0
    r=dict(start_frame=cursor,end_frame=cursor+e-s,source=str(SRC[n]),roll=n,
           audio_start=s,audio_end=e,label=label,visual=visual,
           video_source=str(SRC[pic or n]),video_start=fr(ps) if ps is not None else s,
           video_end=fr(pe) if pe is not None else e)
    ROWS.append(r); return r

def at(n,t):
    sf=fr(t)
    r=next(r for r in ROWS if r['roll']==n and r['audio_start']<=sf<r['audio_end'])
    return (r['start_frame']+sf-r['audio_start'])/30

def speech_level(x):
    n=len(x)//2400
    v=20*np.log10(np.sqrt(np.mean(x[:n*2400].reshape(n,2400)**2,axis=1))+1e-6)
    return float(np.median(v[v>45]))

def prepare():
    cv2.setNumThreads(2);OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
    b=Build(ROOT,SRC['3'],OUT,DEST,protected=[SRC[n] for n in ['1','2','v6']]+list(A.glob('*.jpg'))+[A/'big-downside.mp4',ROOT/'index.html',ROOT/'lessons/big-downside.md'])
    # All changed audio boundaries are inside word-timed intersentence gaps.
    row('v6',0,11.6,'Opening restored: phone excitement, AI question, capability can create risk',pic='1',ps=0,pe=11.6)
    row('3',12.9666667,48.4,'Three ideas; learned patterns; Spot; researchers can inspect parts')
    row('2',68.2,72.1333333,'Graft: They rely on multiple layers of protection to keep the system acting safely',pic='3',ps=43.2,pe=48.8)
    row('2',72.1333333,89.2,'Graft: safety training, screening, permissions and human approval','protection')
    row('3',77.0,80.7333333,'Each layer helps; no layer catches everything','protection')
    row('3',80.7333333,102.6,'Future protections question; people misuse AI; jailbreaking')
    row('3',102.6,110.9,'Defenders many paths; attacker one opening','jailbreak')
    row('1',114.4,122.0,'Graft: patched vulnerability, new methods, ongoing cat-and-mouse','jailbreak')
    row('3',110.9,130.1,'Ordinary capabilities combine into a harmful plan',ps=111.2666667,pe=130.1)
    row('3',130.1,145.4,'Four-step voice-clone scam','voice')
    row('3',145.4,169.1,'Bad actors grow stronger; benign intent; actions; July test with reduced safeguards')
    row('3',169.1,178.5,'Restricted test assignment and They did not stay within it','goal')
    row('1',203.3,207.6333333,'Graft: unauthorized communication outward; supporting boundary-route drawing',pic='2',ps=187.0,pe=191.3333333)
    row('3',178.5,190.0,'Boundary crossed; Hugging Face intrusion and private information','goal')
    row('3',190.0,194.0,'Retained audit-record drawing: attempted concealment')
    row('3',194.0,197.7666667,'Goal pursued even when that meant cheating','goal')
    row('3',197.7666667,234.4333333,'Safety lag, illustrative capability chart, red teams, ongoing safety')
    close=row('3',234.4333333,245.1,'Canonical close: both correct lines and preceding continuous-testing sentence','close')
    cursor=ROWS[-1]['end_frame'];ROWS.append(dict(start_frame=cursor,end_frame=cursor+72,label='Settled close hold',visual='close',roll='tone'))
    total=ROWS[-1]['end_frame']
    audio={n:readwav(OUT/f'audio-{n}.wav') for n in SRC}
    baselevel=speech_level(audio['3'][20*SR:40*SR]);parts=[];gains={};seams=[]
    tone=audio['3'][round(242.5*SR):round(242.7*SR)].copy();tone-=tone.mean()
    for r in ROWS:
        if r['roll']=='tone':data=np.resize(np.r_[tone,tone[::-1]],(r['end_frame']-r['start_frame'])*SPF);gain=0
        else:
            data=audio[r['roll']][r['audio_start']*SPF:r['audio_end']*SPF].copy()
            if r['roll']=='3':gain=0
            elif r['roll']=='2':gain=baselevel-speech_level(audio['2'][fr(68.2)*SPF:fr(89.2)*SPF])
            else:gain=float(np.clip(baselevel-speech_level(data),-6,6))
            data*=10**(gain/20)
        r['gain_db']=gain;parts.append(data)
    for i in range(1,len(ROWS)):
        l,r=ROWS[i-1],ROWS[i]
        contiguous=l.get('source')==r.get('source') and l.get('audio_end')==r.get('audio_start')
        if contiguous:continue
        ramp=np.linspace(0,1,240);bed=np.resize(tone,240)
        parts[i-1][-240:]=parts[i-1][-240:]*(1-ramp)+bed*ramp
        parts[i][:240]=parts[i][:240]*ramp+bed*(1-ramp)
        seams.append(dict(frame=r['start_frame'],seconds=r['start_frame']/30,left=l['label'],right=r['label'],fade_ms=5))
    edited=np.concatenate(parts);assert len(edited)==total*SPF
    writewav(OUT/'edited.wav',edited)
    def target(label,t,rect,color):return dict(label=label,at=t,rects=[rect],color=color,radius=16)
    def board(key,file,targets,banner=None):
        rs=[r for r in ROWS if r['visual']==key]
        b.board(key,A/file,rs[0]['start_frame'],rs[-1]['end_frame'],'compact',targets,banner_at=banner,push=False)
    board('protection','big-downside-safety-guardrails.jpg',[
        target('Safety Training',at('2',75.52),[40,127,525,733],'#4f2fc4'),
        target('Screen for Harm',at('2',79.56),[558,127,1043,733],'#1652f0'),
        target('Limit What AI Can Do',at('2',83.96),[1075,127,1560,733],'#0e8f86')],at('3',77.46))
    board('jailbreak','big-downside-jailbreak.jpg',[
        target('Defenders must protect many paths',at('3',106.7),[436,674,662,899],'#6e51ff'),
        target('An attacker needs only one opening',at('3',108.78),[684,693,861,881],'#6e51ff')],at('1',114.74))
    # First voice item begins <2 s after the source cut: arrive earlier, over its introductory scene.
    vr=next(r for r in ROWS if r['visual']=='voice');prev=ROWS[ROWS.index(vr)-1]
    # The preview full-view opening is 1.46 s; first item rings at spoken onset, no artificial pause.
    b.board('voice',A/'big-downside-voice-cloning.jpg',vr['start_frame'],vr['end_frame'],'compact',[
        target(label,at('3',t),rect,col) for label,t,rect,col in [
            ('Voice Clip',131.56,[40,127,420,710],'#4f2fc4'),('Voice Cloned',135.12,[420,127,800,710],'#1652f0'),
            ('Fake Call',138.20,[800,127,1180,710],'#c41f28'),('Call Back',142.96,[1180,127,1560,710],'#0e8f86')]],push=False,min_open=0)
    board('goal','big-downside-goal-test.jpg',[
        target('Assignment',at('3',171.1),[40,127,525,693],'#4f2fc4'),
        target('Boundary Crossed',at('3',178.92),[558,127,1043,693],'#1652f0'),
        target('Harm',at('3',185.86),[1075,127,1560,693],'#c41f28')],at('3',194.16))
    boards={k:BoardRenderer(OUT/f'leg-{k}.json') for k in b.boards}
    compose_canonical_for_video(close_board_asset('bigdownside'),OUT/'close.png','#ffffff')
    m=dict(output=str(DEST),source=str(SRC['3']),fps=30,total_frames=total,duration=total/30,timeline=ROWS,
        boards=b.boards,lesson_scope_sha256=lesson_signature((ROOT/'index.html').read_text()),boundaries=[dict(frame=r['start_frame'],label=r['label']) for r in ROWS[1:]],
        audio_seams=seams,protected_hashes=b.hashes,close=dict(start_frame=close['start_frame'],prehold=48,push=150,endpoint=1.2,settled=total-close['start_frame']-198),
        scope='User authorized build after review. Review candidate only; no installation, commit or publication.',
        audio='Original source narration; four donor passages; gain-matched; 5 ms fades only at audio edits. No teaching pauses added.',
        remaining=['No direct listening or real-time motion verification available.', 'Screening outgoing harmful answers remains unspoken.','Callback does not explicitly say the number you already have.','Concrete tools/permissions examples remain unspoken.','Four required wording entries remain paraphrased; opening now restores Because.'])
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    for k,br in boards.items():
        for n in sorted(set([0]+[r[0]+10 for r in br.rings])):cv2.imwrite(str(OUT/'preview'/f'{k}-{n:05}.jpg'),br.frame(n))
    return m,boards

def render(m,boards):
    assert not DEST.exists(),'Never overwrite a review candidate'
    ci=cv2.imread(str(OUT/'close.png'));mask=glyph_mask();counts={};readers={};previews=[]
    p=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','18','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for r in ROWS:
        n=r['end_frame']-r['start_frame'];key=r['visual'];rd=None
        if key=='source':
            path=r['video_source'];rd=readers.get(path)
            if rd is None or rd.n>r['video_start']:
                if rd:rd.c.release()
                rd=Reader(path);readers[path]=rd
        for j in range(n):
            f=r['start_frame']+j
            if key in boards:im=boards[key].frame(f-m['boards'][key]['src_in'])
            elif key=='close':
                q=np.clip((f-m['close']['start_frame']-48)/149,0,1);z=1+.2*smoothstep(q)
                h,w=ci.shape[:2];ww=w/z;hh=ww*9/16
                im=cv2.warpAffine(ci,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
            else:
                vf=min(r['video_start']+j,r['video_end']-1);im=rd.at(vf)
                im,how=clean_frame(im,mask);counts[str(how)]=counts.get(str(how),0)+1
            if j in (0,n-1) or f%120==0:
                cv2.imwrite(str(OUT/'preview'/f'output-{f:05}.jpg'),im)
            p.stdin.write(im.tobytes())
        print(f"{r['end_frame']}/{m['total_frames']} {r['label']}",flush=True)
    p.stdin.close();assert p.wait()==0
    for rd in readers.values():rd.c.release()
    m.update(render_sha256=sha(DEST),corner_mark=counts,protected_files_unchanged={p:sha(p)==h for p,h in m['protected_hashes'].items()})
    m['lesson_scope_unchanged']=lesson_signature((ROOT/'index.html').read_text())==m['lesson_scope_sha256']
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    assert all(v for p,v in m['protected_files_unchanged'].items() if p!=str(ROOT/'index.html'))
    assert m['lesson_scope_unchanged']
    print('COMPLETE',DEST,flush=True)

if __name__=='__main__':
    m,boards=prepare()
    if '--preview' not in sys.argv:render(m,boards)
