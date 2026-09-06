#!/usr/bin/env python3
"""Approved Document Trap review repair. Source and live video remain intact.

Narration and visual boundaries are independent. The live opening restores the
tournament setup. Lesson boards are used without video-only explanatory captions.
"""
from pathlib import Path
import json
import subprocess
import tempfile
import sys
import cv2
import build_your_choices_reroll_review as common
from build_work_changes_hybrid import render_leg

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'Prompts/document-trap.mp4'
OUTPUT=ROOT/'Prompts/document-trap-patched.mp4'
AUDIT=ROOT/'video-audit/document-trap-pause-cut-2026-09-06'
LIVE=ROOT/'videos/document-trap.mp4'
at=common.at
LIVE_END=at(65.533333)
REROLL_RESUME=at(67.5)
LIVE_BOARD_START=at(57.8)
CUTS=((at(130.666667),at(142.966667)),
      (at(146.433333),at(156.0)),
      (at(196.5),at(199.633333)),
      (at(208.466667),at(211.066667)),  # Pause-video request and adjacent breaths.
      (at(239.633333),at(245.833333)))
common.CUTS=CUTS
def mapped(frame):
    return common.output_frame(frame)+LIVE_END-REROLL_RESUME
END=7807
P,B,T,A,VP='#4f2fc4','#1652f0','#0e8f86','#a9760c','#6e51ff'
CLOSE_START=at(252.633333)

# Measured canonical v3 asset boundaries, in authored 1600px coordinates.
# Rings follow the outer card/illustration edges, never an inset text area.
FLOW_STEPS=((75,175,385,676),(645,175,955,676),(1215,175,1525,676))
MOVE_CARDS=((40,127,784,676),(816,127,1560,676),
            (40,708,784,1257),(816,708,1560,1257))
FLOW_BANNER=(40,751,1560,839)
MOVES_BANNER=(40,1297,1560,1385)
UPLOADED_BANNER=(40,1180,1560,1268)

def centered_camera(rect, width):
    x1,y1,x2,y2=rect
    assert width*9/16 >= y2-y1+60
    return ((x1+x2)/2,(y1+y2)/2,width)


def replacements():
    result=[]
    def add(name,asset,points,states):
        points=tuple(at(t) for t in points)
        item=common.make_leg(name,ROOT/'illustrations'/asset,points,tuple(states))
        result.append((points[0],points[-1],item))
    add('flow','document-trap-flow-v3.jpg',
        (67.5,80.0,87.55,100.45,113.65,124.866667),(
            ('full',None,VP,None,0),
            ('split',FLOW_STEPS[0],P,centered_camera(FLOW_STEPS[0],1020),24),
            ('search',FLOW_STEPS[1],B,centered_camera(FLOW_STEPS[1],1020),24),
            ('full-takeaway',FLOW_BANNER,VP,None,24),
            ('load',FLOW_STEPS[2],T,centered_camera(FLOW_STEPS[2],1020),24)))
    add('moves','document-trap-moves-v3.jpg',
        (161.6,167.35,178.2,188.25,200.2,211.066667),(
            ('full',None,VP,None,0),
            ('name-section',MOVE_CARDS[0],P,centered_camera(MOVE_CARDS[0],1160),24),
            ('ask-one-thing',MOVE_CARDS[1],B,centered_camera(MOVE_CARDS[1],1160),24),
            ('share-what-matters',MOVE_CARDS[2],T,centered_camera(MOVE_CARDS[2],1160),24),
            ('ask-for-quote',MOVE_CARDS[3],A,centered_camera(MOVE_CARDS[3],1160),24)))
    return result


def render_live_opening(work):
    # Preserve the live story and its regular-season/tournament graphics.
    # Cover its system-error title before its first frame with the lesson art.
    board=common.make_leg('uploaded',ROOT/'illustrations/document-trap-uploaded-v3.jpg',
        (LIVE_BOARD_START,at(60.2),LIVE_END),(
            ('full',None,VP,None,0),
            ('full-takeaway',UPLOADED_BANNER,VP,None,0)))
    board_path=work/'live-uploaded.mkv'
    render_leg(board,board_path)
    target=work/'live-opening.mkv'
    graph=(f'[0:v]trim=end_frame={LIVE_BOARD_START},setpts=PTS-STARTPTS,'
           'scale=1280:720,setsar=1,format=yuv420p[v0];'
           '[1:v]setpts=PTS-STARTPTS,setsar=1,format=yuv420p[v1];'
           '[v0][v1]concat=n=2:v=1:a=0[v];'
           f'[0:a]atrim=end={LIVE_END/30:.6f},asetpts=PTS-STARTPTS,'
           'aresample=44100,aformat=channel_layouts=mono[a]')
    subprocess.run([common.FFMPEG,'-y','-v','error','-i',str(LIVE),'-i',str(board_path),
        '-filter_complex',graph,'-map','[v]','-map','[a]','-c:v','ffv1',
        '-c:a','pcm_s16le',str(target)],check=True)
    assert common.frame_count(target)==LIVE_END
    return target

def main():
    AUDIT.mkdir(parents=True,exist_ok=True)
    assert common.frame_count(SOURCE)==END
    original_hash=common.file_md5(SOURCE)
    live=LIVE
    live_hash=common.file_md5(live)
    items=replacements()
    expected=mapped(END)
    boundaries={mapped(a):f'audio-cut-{i+1}' for i,(a,b) in enumerate(CUTS)}
    boundaries[LIVE_BOARD_START]='live-to-uploaded'
    boundaries[LIVE_END]='live-to-reroll'
    states=[{'name':'live/regular-season','output_frame':at(41)},
            {'name':'live/tournament','output_frame':at(48)},
            {'name':'uploaded/full','output_frame':at(59)},
            {'name':'uploaded/full-takeaway','output_frame':at(62)}]
    with tempfile.TemporaryDirectory(prefix='document-trap-review-',dir='/private/tmp') as directory:
        work=Path(directory)
        renders=[(0,REROLL_RESUME,render_live_opening(work),LIVE_END)]
        for a,b,item in items:
            path=work/(item.name+'.mkv')
            print('Rendering',item.name,flush=True)
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
        close_start=CLOSE_START
        close_png=work/'close.png'
        close_image=cv2.imread(str(ROOT/'lessons/document-trap-4-close.jpg'))
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
        graph.append(f'[1:a]atrim=end={LIVE_END/30:.6f},asetpts=PTS-STARTPTS,'
                     'aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono[a0]')
        al.append('[a0]')
        cursor=REROLL_RESUME
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
        'live_opening':{'source':str(live),'md5':live_hash,'end':LIVE_END/30,
                        'reroll_resume':REROLL_RESUME/30},
        'cuts':[{'source_start':0,'source_end':REROLL_RESUME/30,'output_frame':LIVE_END}]+
               [{'source_start':a/30,'source_end':b/30,'output_frame':mapped(a)} for a,b in CUTS],
        'replacements':[{'name':item.name,'asset':str(item.board),'source_start':a/30,'source_end':b/30} for a,b,item in items],
        'uploaded_asset':'illustrations/document-trap-uploaded-v3.jpg',
        'states':states,'boundaries':boundaries,'live_video_modified':False}
    (AUDIT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    command=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(OUTPUT)]
    for f,label in sorted(boundaries.items()): command+=['--boundary',f'{f}:{label}']
    command+=['--outdir',str(AUDIT/'transitions')]
    subprocess.run(command,check=True)
    print(f'Review candidate: {OUTPUT} ({expected/30:.2f}s)',flush=True)


if __name__=='__main__': main()
