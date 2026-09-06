#!/usr/bin/env python3
"""Reproducible review-only Hallucination repair; never touches the live video.

Audio cuts use measured quiet frames, not approximate transcript boundaries.
Visual replacements have independent, scene-complete source intervals.
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
SOURCE = ROOT / 'Prompts/Hallucination.mp4'
OUTPUT = ROOT / 'Prompts/hallucination-patched.mp4'
AUDIT = ROOT / 'video-audit/avoid-traps-rerolls-2026-09-05/Hallucination/patch-flow'
at = common.at
CUTS = ((at(36.4), at(39.7)), (at(45.3), at(51.5)),
        (at(65.8), at(67.733333)), (at(82.433333), at(86.133333)),
        (at(163.966667), at(168.6)))
common.CUTS = CUTS
mapped = common.output_frame
END = 6039
P, B, T, A = '#4f2fc4', '#1652f0', '#0e8f86', '#a9760c'
VP = '#6e51ff'


def replacements(card):
    result = []
    def add(name, asset, points, states):
        points = tuple(at(t) for t in points)
        leg = common.make_leg(name, ROOT / asset, points, tuple(states))
        result.append((points[0], points[-1], leg))
    add('example', 'illustrations/hallucination-example-v2.jpg',
        (9.0, 10.0, 19.8, 25.966667), (
            ('full', None, VP, None, 0),
            ('full-ai-bubble', (80,401,989,618), VP, (550,490,1180), 24),
            ('full-takeaway', (40,697,1560,786), VP, None, 24)))
    add('why', 'illustrations/hallucination-why-v2.jpg',
        (60.533333, 61.1, 67.733333, 73.6, 77.4, 86.133333), (
            ('full', None, P, None, 0),
            ('learns-from-text', (56,164,362,794), P, None, 0),
            ('one-token', (452,164,756,794), B, None, 0),
            ('keeps-answering', (844,164,1150,794), T, None, 0),
            ('probable-not-true', (1234,164,1548,794), A, None, 0)))
    add('real-text', 'illustrations/hallucination-real-text-v2.jpg',
        (121.566667, 135.0, 139.333333), (
            ('full-illustration', None, VP, None, 0),
            ('full-takeaway', (40,1180,1560,1269), VP, None, 0)))
    add('check-claim', str(card), (157.8, 160.5, 170.666667), (
        ('full', None, P, None, 0),
        ('notice-the-claim', (70,175,500,718), P, None, 0)))
    add('check-source', str(card), (177.7, 180.7, 183.866667), (
        ('find-the-source', (585,175,1015,718), B, None, 0),
        ('check-the-match', (1100,175,1530,718), T, None, 0)))
    return result


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    assert common.frame_count(SOURCE) == END
    original_hash = common.file_md5(SOURCE)
    board = ROOT / 'illustrations/hallucination-check-claim-v1.jpg'
    assert common.file_md5(board) == common.file_md5(ROOT/'lessons/hallucination-4-check-claim.jpg')
    items = replacements(board)
    close_start = at(190.1)
    expected = mapped(END)
    boundaries = {mapped(a): 'audio-cut-'+str(i+1) for i,(a,b) in enumerate(CUTS)}
    states = []
    with tempfile.TemporaryDirectory(prefix='hallucination-review-', dir='/private/tmp') as folder:
        work = Path(folder)
        renders = []
        for a,b,leg in items:
            path = work / (leg.name+'.mkv')
            print('Rendering', leg.name, flush=True)
            render_leg(leg, path)
            assert common.frame_count(path) == leg.frames
            renders.append((a,b,path,leg.frames))
            boundaries[mapped(a)] = 'to-'+leg.name
            boundaries[mapped(b)] = 'from-'+leg.name
            cursor = mapped(a)
            for state in leg.states:
                states.append({'name': leg.name+'/'+state.label,
                    'output_frame': cursor+min(state.frames-1, max(30,state.move_frames+5)),
                    'rect': state.ring, 'color': state.color, 'camera': state.camera})
                cursor += state.frames
        # Preserve the standard close's 16:9 layout, scaling its current 4K asset.
        close_image = cv2.imread(str(ROOT/'lessons/hallucination-5-close.jpg'))
        close_png = work/'close.png'
        cv2.imwrite(str(close_png), cv2.resize(close_image,(1600,900),interpolation=cv2.INTER_AREA))
        common.BOARDS['close'] = close_png
        close_video = work/'close.mkv'
        common.render_close(close_video, expected-mapped(close_start))
        renders.append((close_start,END,close_video,expected-mapped(close_start)))
        boundaries[mapped(close_start)] = 'to-standard-close'
        states.extend([{'name':'close/full','output_frame':mapped(close_start)+20},
                       {'name':'close/settled','output_frame':expected-20}])
        graph, vl, al = [], [], []
        def native(a,b):
            for c,d in CUTS:
                if a < c < b:
                    common.source_video(graph,vl,a,c)
                if c <= a < d or a < c < b:
                    a = min(b,d)
            if b > a:
                common.source_video(graph,vl,a,b)
        cursor = 0
        for i,(a,b,path,n) in enumerate(renders,1):
            native(cursor,a)
            common.rendered_video(graph,vl,i,n)
            cursor = b
        graph.append(''.join(vl)+f'concat=n={len(vl)}:v=1:a=0,format=yuv420p[outv]')
        cursor=0
        for a,b in CUTS:
            common.source_audio(graph,al,cursor,a)
            cursor=b
        common.source_audio(graph,al,cursor,END)
        graph.append(''.join(al)+f'concat=n={len(al)}:v=0:a=1[outa]')
        command=[common.FFMPEG,'-y','-hide_banner','-loglevel','error','-i',str(SOURCE)]
        for a,b,path,n in renders:
            command += ['-i',str(path)]
        command += ['-filter_complex',';'.join(graph),'-map','[outv]','-map','[outa]',
            '-r','30','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p',
            '-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUTPUT)]
        print('Encoding review candidate', flush=True)
        subprocess.run(command,check=True)
    assert common.frame_count(OUTPUT) == expected
    assert common.file_md5(SOURCE) == original_hash
    manifest={'source':str(SOURCE),'source_md5':original_hash,'output':str(OUTPUT),
        'output_frames':expected,'seconds':expected/30,
        'cuts':[{'source_start':a/30,'source_end':b/30,'output_frame':mapped(a)} for a,b in CUTS],
        'replacements':[{'name':leg.name,'source_start':a/30,'source_end':b/30} for a,b,leg in items],
        'states':states,'boundaries':boundaries,'live_video_modified':False,
        'check_claim_board':str(board),'check_claim_board_md5':common.file_md5(board)}
    (AUDIT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    command=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(OUTPUT)]
    for f,label in sorted(boundaries.items()):
        command += ['--boundary',f'{f}:{label}']
    command += ['--outdir',str(AUDIT/'transitions')]
    subprocess.run(command,check=True)
    print(f'Review candidate: {OUTPUT} ({expected/30:.2f}s)',flush=True)


if __name__ == '__main__':
    main()
