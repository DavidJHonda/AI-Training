"""Rebuild the v9 edit from its originals with the two approved cuts and new spreadsheet shot."""
from bisect import bisect_right
from copy import copy
import json

import cv2

import build_where_ai_lives_v9 as base
from editspec_build import Build, FPS, H, W, sha

AUDIT = base.ROOT/'video-audit/where-ai-lives-build-2026-11-19-v10'
DEST = base.ROOT/'Prompts/where-ai-lives-v10.mp4'
ART = base.ROOT/'scripts/video/assets/where-ai-lives-march-expenses.png'
# Half-open ranges on v9's 30 fps timeline. Resume the first cut at the phone scene.
CUTS = [(1717,2354),(5928,6142)]
ART_START = 1479


def main():
    if DEST.exists():
        raise SystemExit(f'Candidate already exists: {DEST}')
    cv2.setNumThreads(2)
    old=json.loads((base.AUDIT/'edit-manifest.json').read_text())
    assert all(sha(p)==h for p,h in old['protected_hashes'].items())
    b=Build(base.ROOT,base.RAW[3],AUDIT,DEST,[base.RAW[1],base.RAW[2],ART,*base.ASSETS.values()])
    b.load_audio([(190.58,191.48),(280.32,281.05)])
    old_positions=[]
    keeps=[(0,CUTS[0][0]),(CUTS[0][1],CUTS[1][0]),(CUTS[1][1],old['total_frames'])]
    for start,end in keeps:
        for row in old['timeline']:
            lo=max(start,row['start_frame'])
            hi=min(end,row['end_frame'])
            if lo>=hi:
                continue
            old_positions.append(lo)
            label=row['label']
            if row['kind']=='room_tone':
                b.pause(hi-lo,label)
                continue
            s=row.get('audio_start',row['source_start'])+lo-row['start_frame']
            if row.get('graft_audio'):
                take=old['grafts'][label]
                b.graft(row['graft_audio'],s,s+hi-lo,label,label,picture_from=s,gain_db=take['gain_db'])
            else:
                b.keep(s,s+hi-lo,label)
    removed=sum(end-start for start,end in CUTS)
    b.close_start=old['close']['start_frame']-removed
    b.finish_audio()
    b.make_close('computecost')

    # Reuse the approved picture timeline in its own time coordinates.
    original=copy(b)
    original.rows=old['timeline']
    original.close_start=old['close']['start_frame']
    picture=base.Picture(original)
    starts=[row['start_frame'] for row in b.rows]
    art=cv2.imread(str(ART))
    assert art is not None
    # Center-crop the few excess pixels to 16:9 before scaling to video size.
    ah,aw=art.shape[:2]
    height=round(aw*H/W)
    y=(ah-height)//2
    replacement=cv2.resize(art[y:y+height],(W,H),interpolation=cv2.INTER_AREA)

    class Revision:
        readers=picture.readers
        def scene(self,f):
            i=bisect_right(starts,f)-1
            source=old_positions[i]+f-starts[i]
            if ART_START<=source<CUTS[0][0]:
                return replacement,'Spreadsheet shared with ChatGPT'
            return picture.scene(source)

    base.encode(b,Revision(),dict(v9_removed_frames=CUTS,v9_kept_frame_starts=old_positions,
                                  v9_illustration_frames=[ART_START,CUTS[0][0]]))


if __name__=='__main__':
    main()
