#!/usr/bin/env python3
"""Narrow v9 repair: speak the AI-future point at the motivation board entrance."""
import json
import cv2
import build_people_skills_v9 as base
from editspec_build import Build as OriginalBuild

ROOT=base.ROOT
OUT=ROOT/'video-audit/people-skills-transition-v10-2026-10-26'
DEST=ROOT/'Prompts/people-skills-v10.mp4'
PREVIOUS=base.DEST
base.OUT=OUT
base.DEST=DEST
fr=base.fr

class TransitionBuild(OriginalBuild):
    def __init__(self,*args,**kwargs):
        kwargs['protected']=[*kwargs.get('protected',[]),PREVIOUS]
        super().__init__(*args,**kwargs)
    def keep(self,s,e,label,visual='source',**kwargs):
        if s==fr(50.2) and label=='Future: Stand Out and Trust title':
            self.graft(base.LIVE,fr(95),fr(98.033333333),
                'People skills matter even more in the AI future', 'ai-future',
                picture_from=fr(50.2),gain_db=.54,visual='mm')
            s=fr(54.433333333)
        return super().keep(s,e,label,visual,**kwargs)
    def board(self,key,*args,**kwargs):
        if key=='mm':
            args=list(args)
            # Correct first-card onset after the replacement sentence, confirmed
            # against the source waveform and a fresh medium.en transcript.
            targets=[dict(t) for t in args[4]]
            targets[0]['at']=54.8
            args[4]=targets
        return super().board(key,*args,**kwargs)
    def manifest(self,extra=None):
        extra=dict(extra or {})
        extra.update(
            approval='User requested the explicit AI-future transition at the board entrance in v9; narrow repair on 2026-10-26.',
            scope_detail='Replace only the generic board introduction; preserve the approved v9 assembly elsewhere. Review candidate, not installed.',
            transition_repair=dict(previous=str(PREVIOUS),removed_source5=[50.2,54.433333333],
                donor=str(base.LIVE),donor_span=[95,98.033333333],donor_gain_db=.54,
                words='People skills matter even more in the AI future.',
                base_context_lufs=-20.57,donor_lufs=-21.11),
        )
        extra['removed_source_seconds']=[*extra['removed_source_seconds'],[50.2,54.433333333]]
        return super().manifest(extra)

base.Build=TransitionBuild
Picture=base.Picture

if __name__=='__main__':
    cv2.setNumThreads(2)
    m=base.prepare()
    base.render(m)
