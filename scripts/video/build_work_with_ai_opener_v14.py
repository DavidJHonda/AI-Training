#!/usr/bin/env python3
"""Approved roll-5 cut-only Work With AI opener; review candidate, never installs."""
from pathlib import Path
import argparse
from editspec_build import Build, fr, sha, CLOSE_PREHOLD, CLOSE_PUSH, CLOSE_TAIL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/work-with-ai-opener-5.mp4'
DEST = ROOT / 'Prompts/work-with-ai-opener-v14.mp4'
OUT = ROOT / 'video-audit/work-with-ai-opener-v14-2026-11-04'
ASSETS = ROOT / 'course-assets/work-with-ai-opener'
SAME = ASSETS / 'work-with-ai-opener-same-tool.jpg'
MAP = ASSETS / 'work-with-ai-opener-section-map.jpg'
CLOSE = ASSETS / 'work-with-ai-opener-close.jpg'
LIVE = ASSETS / 'work-with-ai-opener.mp4'


def split_at_source(b, point):
    rows = []
    for row in b.rows:
        if row['kind'] != 'source' or not row['source_start'] < point < row['source_end']:
            rows.append(row)
            continue
        delta = point - row['source_start']
        cut = row['start_frame'] + delta
        left = dict(row, source_end=point, end_frame=cut)
        right = dict(row, source_start=point, start_frame=cut)
        if 'video_start' in right:
            right['video_start'] += delta
        rows += [left, right]
    b.rows = rows


def visual(b, start, end, key):
    split_at_source(b, start)
    split_at_source(b, end)
    for row in b.rows:
        if row['kind'] == 'source' and start <= row['source_start'] and row['source_end'] <= end:
            row['visual'] = key


def cover_lead(b, start, scene):
    """Hold the incoming scene over its short pre-cut audio gap; no stale flash."""
    split_at_source(b, scene)
    for row in b.rows:
        if row['kind'] == 'source' and row['source_start'] == start:
            row.update(video_start=scene, video_end=scene + 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare-only', action='store_true')
    args = ap.parse_args()
    assert not DEST.exists(), 'Candidate exists; use a new version.'
    assert sha(SRC) == 'd307f2b4f61ce5b606160f9225a03a59a3f654d8e21b032745c776f7acd18f0c'
    b = Build(ROOT, SRC, OUT, DEST, protected=[SAME, MAP, CLOSE, LIVE])
    # Measured low-level gaps, not speech regions. Every cut falls inside one.
    b.load_audio([(22.4,22.9),(42.8,43.3),(83.8,84.3)])
    b.keep(0,fr(22.6),'Opening and contrasting drafts')
    b.keep(fr(43.3),fr(63.6),'Camera example and unchanged hardware')
    b.keep(fr(73.1),fr(80.533333),'Clear goal and verify before use')
    b.keep(fr(84.2),fr(121.4),'Thinking, map introduction, suitable tasks and application')
    b.keep(fr(131.5),fr(161.466667),'Questions, details, evaluation and model/thinking/research')
    b.keep(fr(173.6),fr(176.2),'Map takeaway')
    b.mark_close_start()
    b.keep(fr(196),fr(203.2),'Exact two-line closing','close')
    close_audio = b.cursor - b.close_start
    b.pause(max(CLOSE_TAIL,CLOSE_PREHOLD+CLOSE_PUSH+CLOSE_TAIL-close_audio),'Settled standard close')
    b.finish_audio()

    cover_lead(b,fr(43.3),1307)
    cover_lead(b,fr(73.1),2197)
    visual(b,fr(84.2),fr(93.4),'same')
    visual(b,fr(93.4),fr(176.2),'map')
    # Useful source illustrations interrupt the map without new narration.
    visual(b,3488,fr(121.4),'source')
    visual(b,4093,4259,'source')
    b.tall_margin = True
    b.board('same',SAME,fr(84.2),fr(93.4),'compact',[
        dict(label='Same tool, different results',at=86.3,rects=[[40,127,1560,982]],color='#6e51ff'),
    ],banner_at=89.54,banner=[40,1023,1560,1110],push=False)
    b.tall_margin = False
    b.board('map',MAP,fr(93.4),fr(176.2),'compact',[
        dict(label='Find Where AI Helps',at=104.3,rects=[[100,143,1500,263]],color='#4f2fc4'),
        dict(label='Ask Better Questions',at=134.46,rects=[[100,295,1500,455]],color='#1652f0'),
        dict(label='Evaluate and Improve',at=152.06,rects=[[100,487,1500,647]],color='#0e8f86'),
    ],banner_at=173.82,banner=[40,702,1560,790],push=False)
    b.make_close('openerworkwith')
    b.manifest(dict(
        authorization='2026-11-04: build it please; approved roll-5 cut-only plan',
        narration_source='Raw roll 5 only; no narration grafts or new recording',
        source_cut_gaps_seconds=[[22.6,43.3],[63.6,73.1],[80.533333,84.2],[121.4,131.5],[161.466667,173.6],[176.2,196]],
        closing_audio_end_seconds=203.2,
        new_instructional_pauses='None; standard closing hold only',
        direct_listening_performed=False,continuous_motion_review_performed=False,installed=False))
    print('Prepared',b.total,'frames;',b.total/30,'seconds',flush=True)
    if args.prepare_only:
        return
    b.render_legs()
    b.render()
    print(DEST,flush=True)


if __name__ == '__main__':
    main()
