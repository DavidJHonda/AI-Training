#!/usr/bin/env python3
"""Build approved Engagement Trap review; never update live video or lesson."""
import sys,json,subprocess,tempfile
from pathlib import Path
ROOT=Path('/Users/davidobrien/Developer/AI-Training')
sys.path.insert(0,str(ROOT/'scripts/video'))
import cv2
import build_your_choices_reroll_review as common
from build_work_changes_hybrid import render_leg
from build_flattery_trap_review import render_illustration
SOURCE=ROOT/'Prompts/engagement-trap.mp4'
OUTPUT=ROOT/'Prompts/engagement-trap-patched.mp4'
AUDIT=ROOT/'video-audit/engagement-trap-repair-2026-09-07'
at=common.at
CUTS=tuple((at(a),at(b)) for a,b in ((58.3,74.4),(105.1,117.933333),(236.833333,246.066667)))
common.CUTS=CUTS
mapped=common.output_frame
END=at(280.333333)
B,A,VP='#1652f0','#a9760c','#6e51ff'

def replacements():
    result=[]
    def add(name,asset,points,states):
        p=tuple(at(t) for t in points)
        result.append((p[0],p[-1],common.make_leg(name,asset,p,tuple(states))))
    compare=ROOT/'illustrations/engagement-trap-comparison-v2.jpg'
    add('follow-up-offer',compare,(16.7,19.4,40.233333),(
        ('establish',None,VP,None,0),
        ('complete-ai-bubble',(96,335,1504,542),B,(800,438.5,1680),30)))
    add('two-endings',compare,(58.3,78.5,82.4,92.833333),(
        ('establish',None,VP,None,0),
        ('you-stop',(40,610,784,1210),B,(800,974,1680),30),
        ('the-trap',(816,610,1560,1210),A,(800,974,1680),0)))
    add('infinite-scroll',ROOT/'illustrations/engagement-trap-scroll-v2.jpg',
        (149.366667,153.4,164.2,179.5,186.166667),(
        ('establish',None,VP,None,0),
        ('before-scroll',(40,127,784,718),B,None,0),
        ('infinite-scroll',(816,127,1560,718),A,None,0),
        ('takeaway',(40,758,1560,846),VP,None,0)))
    # Reuse a clean native phone/paper-ribbon shot, not the unsupported data chart.
    cap=cv2.VideoCapture(str(SOURCE))
    frame=None
    for i in range(at(214)+1):
        ok,frame=cap.read()
        assert ok
    cap.release()
    asset=AUDIT/'assets/native-ribbon.png'
    cv2.imwrite(str(asset),frame)
    add('native-ribbon',asset,(216.133333,221.466667),(
        ('native-ribbon',None,VP,(640,360,1250),150),))
    add('deliberate-stop',ROOT/'illustrations/engagement-trap-stop-v2.jpg',
        (249.8,272.766667),(
        ('full-illustration-title-and-banner',None,VP,None,0),))
    # Audio shoulders precede the source visual cuts by 4 and 6 frames.
    # Advance the approved destination shots over those remnants without
    # changing the audio timing or exposing the deleted graphics.
    for name,a,b,sample in (('bridge-history',105.1,118.1,118.1),('bridge-trap',236.833333,246.3,246.3)):
        cap=cv2.VideoCapture(str(SOURCE))
        for i in range(at(sample)+1):
            ok,frame=cap.read()
            assert ok
        cap.release()
        asset=AUDIT/'assets'/f'{name}.png';cv2.imwrite(str(asset),frame)
        add(name,asset,(a,b),((name,None,VP,(640,360,1280),0),))
    return sorted(result,key=lambda item:item[0])

def splice_audio(graph,labels,start,end):
    label=f'a{len(labels)}';duration=(end-start)/30
    fades=('afade=t=in:d=0.003,' if start else '')
    fades+=(f'afade=t=out:st={duration-.003:.6f}:d=0.003,' if end<END else '')
    graph.append(f'[0:a]atrim=start={start/30:.6f}:end={end/30:.6f},asetpts=PTS-STARTPTS,aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,{fades}apad,atrim=duration={duration:.6f}[{label}]')
    labels.append(f'[{label}]')

def main():
    (AUDIT/'assets').mkdir(parents=True,exist_ok=True)
    assert common.frame_count(SOURCE)==8480
    sourcehash=common.file_md5(SOURCE)
    live=ROOT/'videos/engagement-trap.mp4';livehash=common.file_md5(live)
    items=replacements();expected=mapped(END)
    boundaries={mapped(a):f'audio-cut-{i+1}' for i,(a,b) in enumerate(CUTS)}
    states=[]
    with tempfile.TemporaryDirectory(prefix='engagement-patch-',dir='/private/tmp') as directory:
        work=Path(directory);renders=[]
        for a,b,item in items:
            path=work/(item.name+'.mkv')
            print('Rendering',item.name,flush=True)
            (render_illustration if item.name=='native-ribbon' or item.name.startswith('bridge-') else render_leg)(item,path)
            assert common.frame_count(path)==item.frames
            renders.append((a,b,path,item.frames))
            boundaries[mapped(a)]='to-'+item.name;boundaries[mapped(b)]='from-'+item.name
            cursor=mapped(a)
            for state in item.states:
                states.append({'name':item.name+'/'+state.label,'output_frame':cursor+min(state.frames-1,max(30,state.move_frames+5)),
                    'rect':state.ring,'camera':state.camera,'highlight_color':state.color if state.ring else None,
                    'color_source':('neutral_video_purple' if state.color==VP else 'card_locked_accent') if state.ring else 'none'})
                cursor+=state.frames
        close_start=at(272.766667)
        close_png=work/'close.png'
        cv2.imwrite(str(close_png),cv2.resize(cv2.imread(str(ROOT/'lessons/engagement-trap-4-close.jpg')),(1600,900),interpolation=cv2.INTER_AREA))
        common.BOARDS['close']=close_png
        close_video=work/'close.mkv';common.render_close(close_video,expected-mapped(close_start))
        renders.append((close_start,END,close_video,expected-mapped(close_start)))
        boundaries[mapped(close_start)]='to-standard-close'
        states.extend([{'name':'close/start','output_frame':mapped(close_start)+20},{'name':'close/last-frame','output_frame':expected-1}])
        graph,vl,al=[],[],[]
        def native(a,b):
            for c,d in CUTS:
                if a<c<b:common.source_video(graph,vl,a,c)
                if c<=a<d or a<c<b:a=min(b,d)
            if b>a:common.source_video(graph,vl,a,b)
        cursor=0
        for i,(a,b,path,n) in enumerate(renders,1):
            native(cursor,a);common.rendered_video(graph,vl,i,n);cursor=b
        graph.append(''.join(vl)+f'concat=n={len(vl)}:v=1:a=0,format=yuv420p[outv]')
        cursor=0
        for a,b in CUTS:splice_audio(graph,al,cursor,a);cursor=b
        splice_audio(graph,al,cursor,END)
        graph.append(''.join(al)+f'concat=n={len(al)}:v=0:a=1[outa]')
        cmd=[common.FFMPEG,'-y','-hide_banner','-loglevel','error','-i',str(SOURCE)]
        for a,b,path,n in renders:cmd+=['-i',str(path)]
        cmd+=['-filter_complex',';'.join(graph),'-map','[outv]','-map','[outa]','-r','30','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUTPUT)]
        print('Encoding review candidate',flush=True);subprocess.run(cmd,check=True)
    assert common.frame_count(OUTPUT)==expected
    assert common.file_md5(SOURCE)==sourcehash and common.file_md5(live)==livehash
    manifest={'source':str(SOURCE),'source_md5':sourcehash,'output':str(OUTPUT),'output_frames':expected,'seconds':expected/30,
        'cuts':[{'source_start':a/30,'source_end':b/30,'output_frame':mapped(a)} for a,b in CUTS],
        'replacements':[{'name':item.name,'source_start':a/30,'source_end':b/30} for a,b,item in items],
        'states':states,'boundaries':boundaries,'live_video_modified':False,'index_modified':False}
    (AUDIT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(OUTPUT)]
    for f,label in sorted(boundaries.items()):cmd+=['--boundary',f'{f}:{label}']
    cmd+=['--outdir',str(AUDIT/'transitions')];subprocess.run(cmd,check=True)
    print('DONE',OUTPUT,expected/30,flush=True)
if __name__=='__main__':main()
