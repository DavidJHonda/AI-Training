#!/usr/bin/env python3
"""Closest workable roll-8 review cut, authorized 2026-11-04.

Owner accepted paraphrases and requested a build without new narration. Every
spoken word comes from raw roll 8. Review only; never installs the candidate.
"""
from pathlib import Path
import argparse, json
from editspec_build import Build, fr, sha, CLOSE_PREHOLD, CLOSE_PUSH, CLOSE_TAIL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/build-your-skills-opener-8.mp4'
DEST = ROOT / 'Prompts/build-your-skills-opener-v9.mp4'
OUT = ROOT / 'video-audit/build-your-skills-opener-v9-2026-11-04'
ASSETS = ROOT / 'course-assets/build-your-skills-opener'
MAP = ASSETS / 'build-your-skills-opener-section-map.jpg'
CLOSE = ASSETS / 'build-your-skills-opener-close.jpg'
LIVE = ASSETS / 'build-your-skills-opener.mp4'
SELECTS = ROOT / 'video-audit/build-your-skills-opener-rerolls-2026-11-04/round-2/controlled-build/silent-selects'
MAP_IN, MAP_OUT = 3290, 4968

def split_at_source(b, point):
    rows = []
    for row in b.rows:
        if row['kind'] != 'source' or not row['source_start'] < point < row['source_end']:
            rows.append(row); continue
        delta = point - row['source_start']; cut = row['start_frame'] + delta
        left = dict(row, source_end=point, end_frame=cut)
        right = dict(row, source_start=point, start_frame=cut)
        if 'video_start' in right: right['video_start'] += delta
        rows += [left, right]
    b.rows = rows

def picture(b, start, end, key, frames):
    split_at_source(b, start); split_at_source(b, end)
    used = 0
    for row in b.rows:
        if row['kind'] == 'source' and start <= row['source_start'] and row['source_end'] <= end:
            row.update(video_src=str(SELECTS/f'{key}.mp4'), video_start=used, video_end=frames)
            used += row['end_frame'] - row['start_frame']

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args=ap.parse_args()
    assert not DEST.exists(), 'Candidate exists; choose a new version.'
    assert sha(SRC) == 'e62bf8e81aa4f76911668e667eb2aa29a5656fac5824727fa949085d5ff25681'
    banks = [SELECTS/f'{key}.mp4' for key in ['cyclist','practicing-balance','skating','basketball','ai-practice']]
    b = Build(ROOT, SRC, OUT, DEST, protected=[MAP,CLOSE,LIVE,*banks])
    b.tall_margin = False
    b.load_audio([(9.5,10.1),(114.1,114.6),(196.45,196.7)])
    b.keep(0,fr(5.1),'Opening: AI tools change')
    # Complete closing clause supplies an economical, same-voice opening contrast.
    b.graft(SRC,fr(194.4),fr(196.6),'Opening: but the skills are yours to keep',
            'opening',picture_from=158,visual='source')
    b.keep(304,fr(26.5),'Bike analogy: outgrowing the bike; taught you')
    b.keep(fr(28.5),fr(47.6),'Balance; cycling, skating, basketball, serious and casual riders')
    b.keep(fr(48.2),fr(88.4),'Practice, collaboration, ideas, curiosity, school/work/life')
    b.keep(fr(101.6),fr(106.7),'Your personal choices, specific questions, independent judgment')
    b.keep(fr(108.433333),fr(170.5),'Matter; complete map; keep a question in mind')
    b.keep(fr(177.7),5746,'Personal contribution; build your answer')
    b.mark_close_start()
    b.keep(5746,fr(196.6),'Closing: tools change; skills are yours to keep','close')
    close_audio=b.cursor-b.close_start
    b.pause(max(CLOSE_TAIL,CLOSE_PREHOLD+CLOSE_PUSH+CLOSE_TAIL-close_audio),'Settled standard close')
    b.finish_audio()

    picture(b,589,683,'cyclist',86)  # remove the visible production label on the handlebars
    picture(b,683,899,'practicing-balance',125)  # replace basketball on a skateboard
    picture(b,985,fr(37.2),'skating',165)  # remove sports drawing production annotations
    picture(b,fr(37.2),1208,'basketball',150)
    picture(b,1690,1839,'ai-practice',113)  # replace AI computer diagram with gibberish
    # Avoid a short return to the equal-access grid after removing that prediction.
    split_at_source(b,5343)
    for row in b.rows:
        if row['kind']=='source' and row['source_start']==fr(177.7):
            row.update(video_src=str(SELECTS/'your-contribution.mp4'),video_start=0,video_end=156)
    b.protected.append(SELECTS/'your-contribution.mp4')
    b.hashes[str(SELECTS/'your-contribution.mp4')]=sha(SELECTS/'your-contribution.mp4')
    split_at_source(b,MAP_IN);split_at_source(b,MAP_OUT)
    for row in b.rows:
        if row['kind']=='source' and MAP_IN<=row['source_start'] and row['source_end']<=MAP_OUT:
            row['visual']='map'
    b.board('map',MAP,MAP_IN,MAP_OUT,'compact',[
        dict(label='Judgment and Responsibility',at=115.6,rects=[[100,143,1500,303]],color='#4f2fc4'),
        dict(label='People Skills and Creative Thinking',at=130.64,rects=[[100,335,1500,495]],color='#1652f0'),
        dict(label='Curiosity and Your Next Steps',at=144.7,rects=[[100,527,1500,647]],color='#0e8f86'),
    ],banner_at=157.16,banner=[40,702,1560,790],push=False)
    b.make_close('openerskills')
    b.manifest(dict(
        authorization='2026-11-04: There is no narration service. Build the closest version for evaluation.',
        narration_source='Raw roll 8 only; no external voice and no cross-roll narration',
        removed_claims=['skills are permanent','an invisible permanent skill','permanently',
            'universal software access and only variables that matter','identical technological capabilities'],
        opening_graft='Complete but the skills are yours to keep clause from this same roll',
        accepted_compromises=['Narration paraphrases the approved script.',
            'Build Your Skills appears on the map but is not spoken as a distinct title.',
            'Formal phrases including cognitive endurance and relentless state of curiosity remain.',
            'The close is a complete sentence with The simple truth is that and but, rather than two standalone lines.'],
        direct_listening_performed=False, continuous_motion_review_performed=False,
        new_instructional_pauses='None; standard closing hold only',installed=False))
    print('Audio prepared:',b.total,'frames',b.total/30,'seconds',flush=True)
    if args.prepare_only:return
    b.render_legs();b.state_sheet('map');b.render();print(DEST,flush=True)

if __name__=='__main__':main()
