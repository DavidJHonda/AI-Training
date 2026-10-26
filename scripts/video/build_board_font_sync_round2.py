#!/usr/bin/env python3
"""Narrow board refresh for The Next Token and Critical Thinking."""
import argparse
import json
from types import SimpleNamespace

import cv2

import build_board_font_sync as base
from editspec_build import Build
from build_embeddings_v7 import Renderer
from build_wheres_the_line_v3 import Board
import ken_burns_path as kb

ROOT=base.ROOT
OUT=ROOT/'video-audit/board-font-sync-round2-2026-10-23'
CONFIG={
    'the-next-token':dict(version=4,frames=6033,preset='fast',crf=17,
        sha='b68eaf70af2c11a4e8c4d751af283b988e36f90a3231b89a174d44cc6ecddec9',
        encode=[[1600,2304],[2554,2710]],
        boards=[dict(key='five-picks',start=1600,end=2304,asset='the-next-token-draws.jpg',stroke=4,
            spec='the-next-token-build-2026-10-09-v3/five-picks-spec.json'),
            dict(key='spot-once',start=2556,end=2710,asset='the-next-token-draws.jpg',stroke=4,
            spec='the-next-token-build-2026-10-09-v3/spot-once-spec.json')]),
    'critical-thinking':dict(version=16,frames=5593,preset='medium',crf=16,
        sha='10ad9dd4b723533e31269826c2cf6c743134a8b98d43058da359983647636488',
        encode=[[0,1057],[3448,3768],[3922,4454],[4634,5099]],
        cutaways=[[3768,3922],[4454,4634]],
        boards=[dict(key='equation',start=0,end=1057,asset='critical-thinking-equation.jpg',stroke=5,
            spec='critical-thinking-repair-2026-09-17-v11/leg-equation.json'),
            dict(key='habits',start=3468,end=5099,asset='critical-thinking-five-habits.jpg',stroke=5,
            spec='critical-thinking-repair-2026-09-17-v11/leg-habits.json')]),
}

def local_frame(key,n):
    if key=='equation':return min(n+360,1401)  # Retain 12-second opening trim and final 15-frame hold.
    if key=='habits':
        if n<4355:return n-3468
        if n<4373:return 886  # Exact 18-frame hold used by the approved spoken-word repair.
        return n-3486
    return n-(1600 if key=='five-picks' else 2556)

def prepare(slug):
    out=OUT/slug;out.mkdir(parents=True,exist_ok=True);boards=[]
    for item in CONFIG[slug]['boards']:
        spec=json.loads((ROOT/'video-audit'/item['spec']).read_text())
        canvas,cw,ch,ox,oy=Build.compose(SimpleNamespace(out=out),ROOT/'course-assets'/slug/item['asset'],item['key'])
        if slug=='the-next-token':
            # The revised note added 40 board pixels. Keep the original full-board treatment,
            # translate the targets to the new canvas, and extend only the two note-related rings.
            assert (cw,ch,ox,oy)==(1824,1026,112,38)
            for beat in spec['beats']:beat['from']=beat['to']=[cw/2,ch/2,cw]
            for ring in spec['rings']:
                ring['rect'][0]+=ox-74;ring['rect'][1]+=oy-37
            if item['key']=='five-picks':spec['rings'][2]['rect'][3]=492
            else:spec['rings'][0]['rect'][3]=125
        else:
            assert spec['beats'][0]['from']==[cw/2,ch/2,float(cw)]
        spec['image']=str(canvas)
        target=out/f'leg-{item["key"]}.json';target.write_text(json.dumps(spec,indent=2)+'\n')
        renderer=Renderer(spec) if slug=='the-next-token' else Board(target)
        boards.append((item,renderer))
    return boards

def render(slug,boards,n):
    if not base.inside(n,CONFIG[slug]['encode']):return None
    for item,board in boards:
        if item['start']<=n<item['end']:
            local=local_frame(item['key'],n)
            if slug=='the-next-token':return board.at(local)[0]
            original=kb.ring_px
            try:
                kb.ring_px=lambda height:item['stroke']
                return board.frame(local)
            finally:kb.ring_px=original
    return None

def boundaries(slug,boards):
    result={}
    for a,b in CONFIG[slug]['encode']:
        if a:result[a]='replacement-start'
        result[b]='source-resumes'
    for item,board in boards:
        if item['start']:result[item['start']]=item['key']+'-in'
        result[item['end']]=item['key']+'-out'
        # Invert the timeline mapping, retaining cuts and holds rather than shifting events.
        markers={r[k] for r in board.spec['rings'] for k in ('start','end')}
        previous=None
        for n in range(item['start'],item['end']):
            local=local_frame(item['key'],n)
            if n and local!=previous and local in markers and renderable(slug,n):
                result[n]=item['key']+'-highlight-change'
            previous=local
    if slug=='critical-thinking':
        result.update({1042:'retained-opening-hold',4355:'retained-word-hold-in',4373:'retained-word-hold-out'})
    return result

def renderable(slug,n):
    return base.inside(n,CONFIG[slug]['encode']) and any(b['start']<=n<b['end'] for b in CONFIG[slug]['boards'])

def configure():
    base.OUT=OUT;base.CONFIG.update(CONFIG)
    base.prepare=prepare;base.render=render;base.boundaries=boundaries

def preview(slug):
    boards=prepare(slug);selected=set(boundaries(slug,boards))|{0}
    for n in list(selected):selected.update([n+24,n-1])
    for n in sorted(selected):
        im=render(slug,boards,n)
        if im is not None:cv2.imwrite(str(OUT/slug/f'preview-{n:05}.jpg'),im)

if __name__=='__main__':
    cv2.setNumThreads(2);configure()
    parser=argparse.ArgumentParser();parser.add_argument('slug',choices=CONFIG);parser.add_argument('--preview',action='store_true')
    args=parser.parse_args()
    if args.preview:preview(args.slug)
    else:base.build(args.slug)
