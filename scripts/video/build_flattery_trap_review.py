#!/usr/bin/env python3
"""Approved fresh Flattery Trap repair. Candidate only; no lesson or live writes."""
import json, subprocess, sys, tempfile
from build_work_changes_hybrid import render_leg, crop_frame, smoothstep
from pathlib import Path
import cv2
import build_your_choices_reroll_review as common

ROOT = Path('/Users/davidobrien/Developer/AI-Training')
SOURCE = ROOT/'Prompts/flattery-trap.mp4'
OUTPUT = ROOT/'Prompts/flattery-trap-patched.mp4'
AUDIT = ROOT/'video-audit/flattery-trap-repair-2026-09-07'
at = common.at
CUTS = tuple((at(a),at(b)) for a,b in (
    (42.5,47.4), (127.8,136.95), (179.8,183.466667),
    (202.6,210.65), (242.233333,253.65)))
common.CUTS = CUTS
mapped = common.output_frame
END = 8511
P,B,T,A,VP = '#4f2fc4','#1652f0','#0e8f86','#a9760c','#6e51ff'

def replacements():
    result=[]
    def add(name,asset,points,states):
        points=tuple(at(t) for t in points)
        result.append((points[0],points[-1],common.make_leg(name,asset,points,tuple(states))))
    add('gatsby',ROOT/'illustrations/flattery-trap-comparison-v2.jpg',
        (28.5,32.8,47.4,52.6,64.5,71.9,80.6),(
        ('establish',None,VP,None,0),
        ('essay',(40,112,1560,351),P,(800,232,1680),30),
        ('flattery-response',(40,383,784,1040),A,(412,712,1330),60),
        ('empty-praise',(40,1040,784,1414),A,(412,1227,1100),30),
        ('useful-feedback',(816,383,1560,1040),B,(1188,712,1330),36),
        ('takeaway',(40,1454,1560,1542),VP,(800,1498,1680),30)))
    add('praise-loop',ROOT/'illustrations/flattery-trap-praise-loop-v2.jpg',
        (87.566667,101.5,109.6,119.1,137.166667),(
        ('establish',None,VP,None,0),
        ('people-rank',(45,155,415,690),P,None,0),
        ('agreement-can-win',(590,155,1010,690),B,None,0),
        ('numbers-move',(1185,155,1555,690),T,None,0)))
    # The definition's incorrect 'personal gain' graphic is replaced by a clean
    # native mirror illustration, not an invented on-page teaching board.
    cap=cv2.VideoCapture(str(SOURCE))
    wanted=at(136.5)
    frame=None
    for i in range(wanted+1):
        ok,frame=cap.read()
        assert ok
    cap.release()
    asset=AUDIT/'assets/native-mirror.png'
    cv2.imwrite(str(asset),frame)
    add('native-mirror',asset,(137.166667,145.333333),(
        ('mirror-illustration',None,VP,(640,360,1250),210),))
    add('sycophancy',ROOT/'illustrations/flattery-trap-sycophancy-v2.jpg',
        (162.066667,167.7,176.8,183.3),(
        ('establish',None,VP,None,0),
        ('brilliant-and-performance-art',(40,218,1560,402),P,None,0),
        ('viral-gold',(40,408,1560,615),P,None,0)))
    add('five-moves',ROOT/'illustrations/flattery-trap-five-moves-v2.jpg',
        (210.633333,212.95,218.05,223.1,227.0,231.266667),(
        ('establish',None,VP,None,0),
        ('ask-dont-tell',(40,139,1560,317),VP,(800,228,1700),24),
        ('ask-for-gaps',(40,317,1560,536),VP,(800,426.5,1700),24),
        ('rubric',(40,536,1560,755),VP,(800,645.5,1700),24),
        ('other-side',(40,755,1560,974),VP,(800,864.5,1700),24)))
    add('standing-instruction',ROOT/'illustrations/flattery-trap-five-moves-v2.jpg',
        (242.233333,255.25,261.2,271.8,276.0),(
        ('introduce-standing-instruction',None,VP,(800,1062,1700),0),
        ('standing-row',(40,974,1560,1150),VP,(800,1062,1700),0),
        ('complete-saved-prompt',(610,1000,1510,1108),T,(1060,1054,1250),30),
        ('takeaway',(40,1190,1560,1278),VP,(800,1234,1680),30)))
    return result

def render_illustration(leg, target):
    """Full-bleed B-roll, without board framing, borders or highlights."""
    im=cv2.imread(str(leg.board))
    h,w=im.shape[:2]
    previous=(w/2,h/2,float(w))
    process=subprocess.Popen([common.FFMPEG,'-y','-hide_banner','-loglevel','error',
        '-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','-',
        '-c:v','ffv1','-level','3',str(target)],stdin=subprocess.PIPE)
    for state in leg.states:
        camera=state.camera or (w/2,h/2,float(w))
        move=min(state.move_frames,state.frames)
        for i in range(state.frames):
            t=smoothstep(i/max(1,move-1)) if move and i<move else 1
            current=tuple(a+(b-a)*t for a,b in zip(previous,camera))
            process.stdin.write(crop_frame(im,current).tobytes())
        previous=camera
    process.stdin.close()
    assert process.wait()==0


def splice_audio(graph, labels, start, end):
    # Three-millisecond edge ramps remove discontinuities at the approved
    # quiet shoulders. No ripple deletion, synthesized speech or added pause.
    label=f"a{len(labels)}"
    duration=(end-start)/30
    fades=("afade=t=in:d=0.003," if start else "")
    fades+=(f"afade=t=out:st={duration-.003:.6f}:d=0.003," if end<END else "")
    graph.append(f"[0:a]atrim=start={start/30:.6f}:end={end/30:.6f},asetpts=PTS-STARTPTS,aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,{fades}apad,atrim=duration={duration:.6f}[{label}]")
    labels.append(f"[{label}]")


def main():
    (AUDIT/'assets').mkdir(parents=True,exist_ok=True)
    assert common.frame_count(SOURCE)==END
    original_hash=common.file_md5(SOURCE)
    live=ROOT/'videos/flattery-trap.mp4'
    live_hash=common.file_md5(live)
    items=replacements()
    expected=mapped(END)
    boundaries={mapped(a):f'audio-cut-{i+1}' for i,(a,b) in enumerate(CUTS)}
    states=[]
    with tempfile.TemporaryDirectory(prefix='flattery-trap-review-',dir='/private/tmp') as directory:
        work=Path(directory)
        renders=[]
        for a,b,item in items:
            path=work/(item.name+'.mkv')
            print('Rendering',item.name,flush=True)
            if item.name=='native-mirror':
                render_illustration(item,path)
            elif item.name.startswith('bridge-'):
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
                    'rect':state.ring,'color':state.color,'camera':state.camera,
                    'highlight_color':state.color if state.ring else None,
                    'color_source':('neutral_video_purple' if state.color==VP else 'card_locked_accent') if state.ring else 'none'})
                cursor+=state.frames
        close_start=at(276.0)
        close_png=work/'close.png'
        close_image=cv2.imread(str(ROOT/'lessons/flattery-trap-5-close.jpg'))
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
            splice_audio(graph,al,cursor,a)
            cursor=b
        splice_audio(graph,al,cursor,END)
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
