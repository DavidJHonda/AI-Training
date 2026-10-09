#!/usr/bin/env python3
"""Restored Notebook candidate; bound context donor before its unrelated title card."""
import json
import build_whats_an_llm_v5 as prior
base=prior.base
base.OUT=base.ROOT/'video-audit/whats-an-llm-build-2026-10-09-v6'
base.DEST=base.ROOT/'Prompts/whats-an-llm-v6.mp4'
get_source_prior=prior.prior.get_source
prepare_prior=base.prepare

def get_source(key,roll,sf):
 if key=='context':sf=min(sf,4320)
 return get_source_prior(key,roll,sf)

def prepare():
 b,boards,m=prepare_prior()
 m['retiming']['context_donor_last_frame']=4320
 m['retiming']['context_donor_tail']='Hold source 144.00 s for the final fraction of a second to exclude the unrelated title card beginning before the former 144.40 s donor end.'
 (base.OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 return b,boards,m
prior.prior.get_source=get_source;base.prepare=prepare
if __name__=='__main__':base.render()
