#!/usr/bin/env python3
"""Approved Mind Trap repair; candidate only, source and live stay untouched.

Visual boundaries are independent of narration cuts. Geometry uses the current
rendered cards' outer edges, not an estimated text area. No index.html writes.
"""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import cv2
from PIL import Image, ImageDraw
from editorial_typography import face
import build_your_choices_reroll_review as common
from build_work_changes_hybrid import render_leg

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT/'Prompts/mind-trap.mp4'
OUTPUT = ROOT/'Prompts/mind-trap-patched.mp4'
AUDIT = ROOT/'video-audit/mind-trap-repair-2026-09-06'
at = common.at
CUTS = tuple((at(a),at(b)) for a,b in (
    (30.266667,34.366667), (50.2,58.366667),
    (100.4,103.2), (122.966667,136.533333),
    (180.5,188.033333), (206.966667,209.433333),
    (228.133333,252.533333)))
common.CUTS = CUTS
mapped = common.output_frame
END = 7771
P, B, T, A, VP = '#4f2fc4', '#1652f0', '#0e8f86', '#a9760c', '#6e51ff'


def terminal_assets():
    """Code-drawn illustrative interface, never an unlicensed archival photo."""
    assets=AUDIT/'assets'
    assets.mkdir(parents=True,exist_ok=True)
    paths=[]
    for stage in range(3):
        im=Image.new('RGB',(1600,900),'#eee9fc')
        d=ImageDraw.Draw(im)
        d.text((60,40),'ELIZA',font=face('heavy',56),fill='#101025')
        d.text((60,115),'1960s · A pattern-matching conversation',font=face('medium',30),fill='#626078')
        d.rounded_rectangle((60,190,1540,805),radius=26,fill='#ffffff')
        d.rounded_rectangle((60,190,1540,275),radius=26,fill='#143778')
        d.rectangle((60,240,1540,275),fill='#143778')
        d.text((100,211),'ELIZA  /  TEXT CONVERSATION',font=face('heavy',25),fill='white')
        if stage>=1:
            d.text((112,315),'USER',font=face('heavy',24),fill=P)
            d.rounded_rectangle((110,362,1490,480),radius=18,fill='#f0eafd')
            d.text((150,390),'I am stressed.',font=face('medium',42),fill='#28253f')
        else:
            d.text((112,340),'A statement goes in.',font=face('medium',40),fill='#57516c')
            d.text((112,410),'A question comes back.',font=face('medium',40),fill='#57516c')
        if stage>=2:
            d.text((112,530),'ELIZA',font=face('heavy',24),fill=T)
            d.rounded_rectangle((110,577,1490,695),radius=18,fill='#e5f4f2')
            d.text((150,605),'Why are you stressed?',font=face('medium',42),fill='#28253f')
        d.text((60,836),'Illustrative example, not an archival screenshot.',font=face('medium',22),fill='#77718b')
        path=assets/f'eliza-terminal-{stage}.png'
        im.save(path)
        paths.append(path)
    return paths


def replacements():
    result=[]
    def add(name,asset,points,states):
        points=tuple(at(t) for t in points)
        item=common.make_leg(name,asset,points,tuple(states))
        result.append((points[0],points[-1],item))
    comparison=ROOT/'illustrations/mind-trap-comparison-v3.jpg'
    add('college-ai',comparison,(24.633333,27.0,40.0),(
        ('full-comparison',None,VP,None,0),
        ('ai-answer',(816,271,1560,1014),A,(1188,642,1450),24)))
    add('college-mom',comparison,(45.366667,46.2,58.54,64.52,68.466667,81.366667),(
        ('full-comparison',None,VP,None,0),
        ('mom-answer',(40,271,784,1014),B,(412,642,1450),24),
        ('mom-notices',(40,1137,784,1248),B,(412,1198,1150),36),
        ('mom-shares-stake',(40,1230,784,1384),B,(412,1198,1150),0),
        ('compare-both',None,VP,None,24)))
    terminals=terminal_assets()
    add('eliza-history',terminals[0],(90.733333,95.0,103.4),(
        ('introduce-eliza',None,VP,None,0),
        ('gentle-push',None,VP,(800,450,1530),100)))
    add('eliza-example-user',terminals[1],(108.833333,114.2),(
        ('full-user-message',(110,362,1490,480),P,None,0),))
    add('eliza-example-reply',terminals[2],(114.2,115.733333),(
        ('full-eliza-message',(110,577,1490,695),T,None,0),))
    add('eliza-effect',ROOT/'illustrations/mind-trap-eliza-effect-v3.jpg',
        (136.533333,145.96,158.12,169.1),(
        ('full-two-part-explanation',None,VP,None,0),
        ('human-language',(816,127,1560,676),P,None,0),
        ('human-response',(40,127,784,676),T,None,0)))
    # Narration cuts precede the next visual cut by a few frames. Hold the
    # last clean native image through those frames so the removed art cannot flash.
    cap=cv2.VideoCapture(str(SOURCE))
    for name,sample,start,end in (
        ('bridge-after-empathy-cut',180.333333,180.4,188.333333),
        ('bridge-after-utility-cut',206.8,206.9,209.7)):
        cap.set(cv2.CAP_PROP_POS_FRAMES,at(sample))
        ok,frame=cap.read()
        assert ok
        path=AUDIT/'assets'/(name+'.png')
        cv2.imwrite(str(path),frame)
        add(name,path,(start,end),((name,None,VP,(640,360,1280),0),))
    cap.release()
    return result


def main():
    AUDIT.mkdir(parents=True,exist_ok=True)
    assert common.frame_count(SOURCE)==END
    original_hash=common.file_md5(SOURCE)
    live=ROOT/'videos/mind-trap.mp4'
    live_hash=common.file_md5(live)
    items=replacements()
    expected=mapped(END)
    boundaries={mapped(a):f'audio-cut-{i+1}' for i,(a,b) in enumerate(CUTS)}
    states=[]
    with tempfile.TemporaryDirectory(prefix='mind-trap-review-',dir='/private/tmp') as directory:
        work=Path(directory)
        renders=[]
        for a,b,item in items:
            path=work/(item.name+'.mkv')
            print('Rendering',item.name,flush=True)
            if item.name.startswith('bridge-'):
                # Preserve the native frame edge-to-edge: no board corner mask.
                subprocess.run([common.FFMPEG,'-y','-hide_banner','-loglevel','error',
                    '-loop','1','-framerate','30','-i',str(item.board),
                    '-frames:v',str(item.frames),'-c:v','ffv1','-level','3',str(path)],check=True)
            else:
                render_leg(item,path)
            assert common.frame_count(path)==item.frames
            renders.append((a,b,path,item.frames))
            boundaries[mapped(a)]='to-'+item.name
            boundaries[mapped(b)]='from-'+item.name
            cursor=mapped(a)
            for state in item.states:
                states.append({'name':item.name+'/'+state.label,
                    'output_frame':cursor+min(state.frames-1,max(30,state.move_frames+5)),
                    'rect':state.ring,'color':state.color,'camera':state.camera})
                cursor+=state.frames
        close_start=at(222.6)
        close_png=work/'close.png'
        close_image=cv2.imread(str(ROOT/'lessons/mind-trap-3-close.jpg'))
        cv2.imwrite(str(close_png),cv2.resize(close_image,(1600,900),interpolation=cv2.INTER_AREA))
        common.BOARDS['close']=close_png
        close_video=work/'close.mkv'
        common.render_close(close_video,expected-mapped(close_start))
        renders.append((close_start,END,close_video,expected-mapped(close_start)))
        boundaries[mapped(close_start)]='to-standard-close'
        states.extend([{'name':'close/full','output_frame':mapped(close_start)+20},
                       {'name':'close/settled','output_frame':expected-20}])
        graph,vl,al=[],[],[]
        def native(a,b):
            for c,d in CUTS:
                if a<c<b: common.source_video(graph,vl,a,c)
                if c<=a<d or a<c<b: a=min(b,d)
            if b>a: common.source_video(graph,vl,a,b)
        cursor=0
        for i,(a,b,path,n) in enumerate(renders,1):
            native(cursor,a)
            common.rendered_video(graph,vl,i,n)
            cursor=b
        graph.append(''.join(vl)+f'concat=n={len(vl)}:v=1:a=0,format=yuv420p[outv]')
        cursor=0
        for a,b in CUTS:
            common.source_audio(graph,al,cursor,a)
            cursor=b
        common.source_audio(graph,al,cursor,END)
        graph.append(''.join(al)+f'concat=n={len(al)}:v=0:a=1[outa]')
        command=[common.FFMPEG,'-y','-hide_banner','-loglevel','error','-i',str(SOURCE)]
        for a,b,path,n in renders: command+=['-i',str(path)]
        command+=['-filter_complex',';'.join(graph),'-map','[outv]','-map','[outa]',
            '-r','30','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p',
            '-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUTPUT)]
        print('Encoding review candidate',flush=True)
        subprocess.run(command,check=True)
    assert common.frame_count(OUTPUT)==expected
    assert common.file_md5(SOURCE)==original_hash
    assert common.file_md5(live)==live_hash
    manifest={'source':str(SOURCE),'source_md5':original_hash,'output':str(OUTPUT),
        'output_frames':expected,'seconds':expected/30,
        'cuts':[{'source_start':a/30,'source_end':b/30,'output_frame':mapped(a)} for a,b in CUTS],
        'replacements':[{'name':item.name,'source_start':a/30,'source_end':b/30} for a,b,item in items],
        'states':states,'boundaries':boundaries,'live_video_modified':False}
    (AUDIT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    command=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(OUTPUT)]
    for f,label in sorted(boundaries.items()): command+=['--boundary',f'{f}:{label}']
    command+=['--outdir',str(AUDIT/'transitions')]
    subprocess.run(command,check=True)
    print(f'Review candidate: {OUTPUT} ({expected/30:.2f}s)',flush=True)


if __name__=='__main__': main()
