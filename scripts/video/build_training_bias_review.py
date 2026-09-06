#!/usr/bin/env python3
"""Approved Training Bias repair. Review candidate only; preserve live/source files.

Sentence cuts use word alignment and measured quiet frames. Board intervals
follow visual scene boundaries independently of narration. No invented board.
"""
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import cv2
import build_your_choices_reroll_review as common
from build_work_changes_hybrid import render_leg

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT/'Prompts/training-bias.mp4'
OUTPUT = ROOT/'Prompts/training-bias-patched.mp4'
AUDIT = ROOT/'video-audit/avoid-traps-rerolls-2026-09-05/training-bias/patch'
at = common.at
CUTS = ((at(151.166667), at(156.433333)),
        (at(181.066667), at(192.9)),
        (at(258.2), at(266.0)))
common.CUTS = CUTS
mapped = common.output_frame
END = 8235
P, B, T, A, VP = '#4f2fc4', '#1652f0', '#0e8f86', '#a9760c', '#6e51ff'


def replacements():
    result=[]
    def add(name, asset, points, states):
        points=tuple(at(t) for t in points)
        item=common.make_leg(name, ROOT/'illustrations'/asset, points, tuple(states))
        result.append((points[0],points[-1],item))
    add('wrong-pattern','training-bias-pattern-v2.jpg',
        (15.1,23.7,28.466667),(
            ('full-illustration',None,VP,None,0),
            ('full-takeaway',(40,1180,1560,1269),VP,None,0)))
    # Exact outer card edges, including image, title, body and bottom padding.
    add('mechanisms','training-bias-mechanisms-v2.jpg',
        (59.366667,65.5,75.6,86.7,99.466667),(
            ('full',None,VP,None,0),
            ('defaults',(40,127,526,652),P,(283,390,1100),24),
            ('blind-spots',(558,127,1044,652),B,(801,390,1100),24),
            ('wrong-patterns',(1076,127,1560,652),A,(1318,390,1100),24)))
    add('questions','training-bias-questions-v2.jpg',
        (113.466667,127.7,132.0,137.0,142.366667),(
            ('full',None,VP,None,0),
            ('whats-missing',(40,127,526,652),P,(283,390,1100),18),
            ('exceptions',(558,127,1044,652),B,(801,390,1100),18),
            ('remove-famous',(1076,127,1560,652),A,(1318,390,1100),18)))
    # Hold the takeaway across the entire unsupported 18-month-cutoff graphic.
    add('stale-chat','training-bias-stale-chat-v2.jpg',
        (168.633333,170.3,178.1,194.55,198.4,204.2,209.866667),(
            ('full',None,VP,None,0),
            ('first-user-bubble',(611,202,1520,338),VP,(1065,270,1100),24),
            ('first-ai-bubble',(80,401,980,537),VP,(530,469,1100),24),
            ('check-current-source',(606,600,1520,735),VP,(1063,668,1100),24),
            ('corrected-answer',(80,799,970,934),VP,(525,867,1100),24),
            ('full-takeaway',(40,1013,1560,1103),VP,(800,942,1650),24)))
    add('rag','training-bias-rag-v2.jpg',
        (223.366667,226.0,230.2,238.0,244.8,258.2),(
            ('full',None,VP,None,0),
            ('retrieve',(40,127,526,611),P,(283,369,1030),24),
            ('add-to-context',(558,127,1044,611),B,(801,369,1030),24),
            ('generate',(1076,127,1560,611),T,(1318,369,1030),24),
            ('full-caveat-banner',(40,650,1560,740),VP,None,24)))
    return result


def main():
    AUDIT.mkdir(parents=True,exist_ok=True)
    assert common.frame_count(SOURCE)==END
    original_hash=common.file_md5(SOURCE)
    live=ROOT/'videos/training-bias.mp4'
    live_hash=common.file_md5(live)
    items=replacements()
    expected=mapped(END)
    boundaries={mapped(a):f'audio-cut-{i+1}' for i,(a,b) in enumerate(CUTS)}
    states=[]
    with tempfile.TemporaryDirectory(prefix='training-bias-review-',dir='/private/tmp') as directory:
        work=Path(directory)
        renders=[]
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
        close_start=CUTS[-1][1]
        close_png=work/'close.png'
        close_image=cv2.imread(str(ROOT/'lessons/training-bias-6-close.jpg'))
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
