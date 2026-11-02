#!/usr/bin/env python3
"""Approved roll-8 best-of edit, November 2, 2026. Candidate only.

Two complete roll-9 narration grafts; current canonical boards; selected roll-7
and immutable v15 picture donors. See the comparison REVIEW.md for approval plan.
Static compact boards render from shared geometry without large FFV1 scratch legs.
"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

import cv2
import numpy as np

from editspec_build import Build, Reader, fr, sha, readwav, writewav, SPF, SR
from editspec_build import PURPLE, BLUE, GREEN, RED, NEUTRAL
import build_understand_ai_opener_v12 as static_boards
from gemini_mark import clean_frame, glyph_mask

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/ai-is-different-build-2026-11-02-v16'
DEST = ROOT / 'Prompts/ai-is-different-v16.mp4'
R7 = ROOT / 'Prompts/ai-is-different-7.mp4'
R8 = ROOT / 'Prompts/ai-is-different-8.mp4'
R9 = ROOT / 'Prompts/ai-is-different-9.mp4'
LIVE_DONOR = ROOT / 'Prompts/ai-is-different-v15.mp4'
LIVE = ROOT / 'course-assets/ai-is-different/ai-is-different.mp4'
ASSETS = {k: ROOT / f'course-assets/ai-is-different/ai-is-different-{s}.jpg'
          for k, s in [('rules','rules'),('cooking','cooking-analogy'),
                       ('playlist','playlist-formats'),('close','close')]}
TABLE_OUT, TABLE_RETURN = 5722, 5951
TABLE_IN, TABLE_END = 5349, 5600
CLOSE_OUT, CLOSE_IN, CLOSE_END = 7836, 7341, 7558
GAIN_DB = -.09  # roll 8 -20.33 LUFS; roll 9 -20.24 LUFS


def setup():
    OUT.mkdir(parents=True, exist_ok=True)
    assert sha(LIVE_DONOR) == '8ed63f95cf3bd166103544c01489d6f238e2ad14b3c55e0726096b51c3a14444'
    b = Build(ROOT, R8, OUT, DEST,
              protected=[R7,R9,LIVE_DONOR,LIVE,*ASSETS.values(),ROOT/'lessons/ai-is-different.md'])
    for old, new in [('roll8.wav','source.wav'),('roll9.wav','graft-table.wav'),('roll9.wav','graft-close.wav')]:
        if (OUT/old).exists() and not (OUT/new).exists():
            os.link(OUT/old, OUT/new)
    b.load_audio([(190.65,190.85),(198.15,198.65),(260.9,261.3)])
    spans=[]; marks={}

    def keep(s,e,label,board=None,**kw):
        s,e=fr(s),fr(e)
        spans.append(('r8',s,e,b.cursor))
        b.keep(s,e,label,board or 'source',**({'video_from':b.cursor} if board else kw))

    def graft(key,s,e,label,board):
        spans.append((key,s,e,b.cursor))
        b.graft(R9,s,e,label,key,picture_from=b.cursor,gain_db=GAIN_DB,visual=board)

    def mapped(t,key='r8'):
        f=fr(t)
        for k,s,e,o in spans:
            if k==key and s<=f<e:return (o+f-s)/30
        raise ValueError((key,t))

    keep(0,1687/30,'Opening, password, calculator and spreadsheet drawings')
    marks['rules']=b.cursor
    keep(1687/30,64.3,'Rules board introduction and condition','rules')
    keep(64.3,68.8333333333,'Lock and key: entering and checking the password',
         video_src=R8,video_from=1190,video_end=1382)
    keep(68.8333333333,88.4,'Rules board: green branch, red branch, repeatability','rules')
    marks['rules_end']=b.cursor
    keep(88.4,2993/30,'Learned patterns and human-written training code')
    marks['cooking']=b.cursor
    keep(2993/30,110.8,'Cooking introduction and robot card','cooking')
    keep(110.8,118.5333333333,'Live-v15 robot recipe and repeated cupcakes',
         video_src=LIVE_DONOR,video_from=3840,video_end=4080)
    keep(118.5333333333,129,'Same recipe takeaway and chef introduction','cooking')
    keep(129,136,'Roll-7 chef: ingredients and cooking methods',
         video_src=R7,video_from=3694,video_end=3963)
    keep(136,147.3,'Chef substitutions, no recipe, different dishes','cooking')
    marks['cooking_end']=b.cursor
    keep(147.3,5261/30,'Structured fields and unstructured input explanation')
    keep(5261/30,179.6,'Digital organization versus handwritten notes',
         video_src=R7,video_from=7093,video_end=7299)
    marks['playlist']=b.cursor
    keep(179.6,TABLE_OUT/30,'Canonical playlist: full introduction, left label and fields','playlist')
    graft('table',TABLE_IN,TABLE_END,'Roll-9 complete three-song, artist and order read','playlist')
    keep(TABLE_RETURN/30,206.9,'Handwriting, title, arrow and cross-out close-ups',
         video_src=R7,video_from=5176,video_end=5448)
    keep(206.9,6745/30,'Canonical playlist: start here, play last, exclude Shake It Off','playlist')
    marks['playlist_end']=b.cursor
    keep(6745/30,7130/30,'Training patterns and interpretation animation')
    keep(7130/30,243.1,'Lock versus complex patterns replaces malformed phone labels',
         video_src=R9,video_from=6647,video_end=6726)
    keep(243.1,CLOSE_OUT/30,'Harder prediction and inspection; crossed-out-song mistake animation')
    b.mark_close_start()
    graft('close',CLOSE_IN,CLOSE_END,'Roll-9 exact two-line close','close')
    b.finish_audio()

    # Preserve the base audio sample-for-sample across visual-only cuts. The
    # shared keep() helper fades every row; only the three real audio seams need
    # fades here. No pauses are inserted.
    base=readwav(OUT/'source.wav'); donor=readwav(OUT/'graft-table.wav')
    gain=10**(GAIN_DB/20)
    chunks=[base[:TABLE_OUT*SPF].copy(),donor[TABLE_IN*SPF:TABLE_END*SPF].copy()*gain,
            base[TABLE_RETURN*SPF:CLOSE_OUT*SPF].copy(),
            donor[CLOSE_IN*SPF:CLOSE_END*SPF].copy()*gain]
    ramp=np.linspace(0,1,240); tone=b.tone(240)
    seam_frames=[];cursor=0
    for i,c in enumerate(chunks):
        if i:c[:240]=c[:240]*ramp+tone*(1-ramp)
        if i<len(chunks)-1:c[-240:]=c[-240:]*(1-ramp)+tone*ramp
        cursor+=len(c)//SPF
        if i<len(chunks)-1:seam_frames.append(cursor)
    writewav(OUT/'edited.wav',np.concatenate(chunks))

    def T(label,at,rect,color):return dict(label=label,at=mapped(at),rects=[rect],color=color,radius=18)
    b.board('rules',ASSETS['rules'],marks['rules'],marks['rules_end'],'compact',[
        T('IF password matches',60.94,[555,346,1046,437],BLUE),
        T('User enters password (during drawing break)',64.9,[585,170,1016,259],NEUTRAL),
        T('IF password matches',67.84,[555,346,1046,437],BLUE),
        T('Green branch: open app',69.2,[125,592,706,700],GREEN),
        T('Red branch: error message',74.12,[805,565,1516,726],RED),
    ],banner_at=mapped(84.42),push=False)
    b.board('cooking',ASSETS['cooking'],marks['cooking'],marks['cooking_end'],'compact',[
        T('Rule-Based Software whole card',104.82,[40,118,784,880],PURPLE),
        T('Same recipe. Same result every time.',118.56,[58,787,766,862],PURPLE),
        T('AI whole card',122.38,[816,118,1560,880],BLUE),
        T('Learned patterns. Different dishes.',140.4,[834,787,1542,862],BLUE),
    ],push=False)
    b.board('playlist',ASSETS['playlist'],marks['playlist'],marks['playlist_end'],'compact',[
        T('Traditional Software: entire left section',181.82,[40,118,800,707],PURPLE),
        T('AI: entire right section',198.98,[800,118,1560,707],BLUE),
    ],push=False)
    b.make_close('aivscode')
    static_boards.OUT=OUT
    states={k:static_boards.render_states(json.loads((OUT/f'leg-{k}.json').read_text()),k) for k in b.boards}
    m=b.manifest({
        'approval':'User: Build it please, November 2, 2026; approved comparison best-of plan',
        'plan':'video-audit/ai-is-different-rolls-7-9-2026-11-02/REVIEW.md',
        'production_scope':'Full production candidate; no installation, commit, or publication',
        'audio_seam_frames':seam_frames,'donor_gain_db':GAIN_DB,
        'audio_policy':'Only real narration seams have 5ms room-tone fades. Visual-only boundaries preserve contiguous PCM.',
        'selective_pauses':[], 'source_to_output_segments':spans,
        'board_timeline':'Board spec clocks are output frames, source-to-output mapping applied before ring placement.',
        'renderer':'Shared compact-board geometry, fixed 4px supersampled rings, streaming single encode',
        'listening':'Unavailable; donor joins and continuous playback require listening review.',
        'production_refinements':[
            'Frame-aligned audio cuts chosen from measured low-energy gaps; see audio-measurements.json.',
            'Robot break returns at 118.533s before Same recipe at 118.56s.',
            'Closing board enters on the quiet audio join at source 261.2s; before Notebook closing cut.',
            'Playlist ring spans each complete half of shared white card; no bottom captions.',
            'Live donor comes from immutable v15, byte-identical to the live source at evaluation.',
        ],
    })
    return b,states,m


def render(b,states,m):
    assert not DEST.exists(),'Do not overwrite a review candidate'
    readers={}; mask=glyph_mask(); clean_counts={'clone':0,'inpaint':0,'declined':[]}
    if mask is not None:cv2.imwrite(str(OUT/'corner-mask.png'),mask*255)
    proc=subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
        '-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium',
        '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    row_i=0;last=None; close=b.close_img
    try:
        for f in range(b.total):
            while f>=b.rows[row_i]['end_frame']:row_i+=1
            r=b.rows[row_i]; offset=f-r['start_frame']
            if f>=b.close_start:
                k=f-b.close_start;q=float(np.clip((k-48)/149,0,1));z=1+.2*q*q*(3-2*q)
                h,w=close.shape[:2];ww=w/z;hh=ww*9/16
                im=cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),
                    (1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
            elif r['visual'] in states:
                key=r['visual'];lf=r.get('video_start',r['source_start'])+offset-b.boards[key]['src_in']
                im=next(frame for s,e,frame in states[key] if s<=lf<e)
            elif r['kind']=='room_tone':im=last.copy()
            else:
                path=r.get('video_src',str(R8));idx=r.get('video_start',r['source_start'])+offset
                if 'video_end' in r:idx=min(idx,r['video_end']-1)
                if path in readers and readers[path].n>idx:
                    readers[path].c.release();del readers[path]
                if path not in readers:readers[path]=Reader(path)
                im=readers[path].at(idx)
                # v15 is already cleaned; do not retouch the donor unnecessarily.
                if path!=str(LIVE_DONOR):
                    im,how=clean_frame(im,mask)
                    if how:clean_counts[how]+=1
                    else:clean_counts['declined'].append(f)
            proc.stdin.write(im.tobytes());last=im
            if f%600==0:print(f'Rendered {f}/{b.total} frames',flush=True)
    finally:
        proc.stdin.close()
        for reader in readers.values():reader.c.release()
    assert proc.wait()==0
    m['render_sha256']=sha(DEST);m['corner_mark']=clean_counts
    m['protected_files_unchanged']={p:sha(p)==digest for p,digest in b.hashes.items()}
    assert all(m['protected_files_unchanged'].values())
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    print(f'Candidate: {DEST}, {b.total} frames, {b.total/30:.3f}s',flush=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-only',action='store_true');args=parser.parse_args()
    b,states,m=setup()
    print(f'Prepared {b.total} frames, {b.total/30:.3f}s; seams {m["audio_seam_frames"]}',flush=True)
    if not args.prepare_only:render(b,states,m)


if __name__=='__main__':main()
